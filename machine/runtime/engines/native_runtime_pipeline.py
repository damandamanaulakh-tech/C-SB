#!/usr/bin/env python3
"""End-to-end Sourceborn native runtime pipeline, Batch-3.

This composes the deterministic engines implemented in Batch-3.  It is an
executable structural prototype, not an LLM wrapper.  Persistent memory
writeback, new-node promotion and scheduling are intentionally deferred to the
next batch; the pipeline marks that boundary explicitly.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Sequence
import argparse
import json

from .actor_role_engine import infer_actor_roles
from .actor_state_engine import build_actor_state_hypotheses
from .combination_engine import generate_combinations
from .event_decomposition_engine import decompose_source
from .evidence_prediction_engine import generate_evidence_predictions
from .falsifier_engine import evaluate_falsifiers
from .future_state_reconstruction_engine import reconstruct_future_states
from .live_intent_engine import generate_live_intents
from .maturity_engine import evaluate_maturity
from .parameter_activation_engine import activate_event, apply_activations_to_event, build_default_activation_index
from .relation_graph_engine import build_event_relation_graph
from .rfr_engine import run_rfr
from .runtime_core import EngineResult, RuntimeContractError, TraceStep, canonicalize, stable_id, utc_now, write_json
from .source_lock_engine import lock_text_source

PIPELINE_ID = "SOURCEBORN-NATIVE-RUNTIME-PIPELINE-BATCH3-V1"
PIPELINE_VERSION = "1.0.0"


def _copy(value: Any) -> Any:
    return json.loads(json.dumps(value, ensure_ascii=False))


def _apply_actor_roles(event: Mapping[str, Any], role_result: EngineResult) -> dict[str, Any]:
    copied = _copy(event)
    copied["actor_roles"] = list(role_result.payload.get("actor_role_assignments", []))
    copied["last_updated_by"] = role_result.engine_id
    return copied


def _hypothesis_index(intents, future_states, combinations) -> dict[str, Mapping[str, Any]]:
    result: dict[str, Mapping[str, Any]] = {}
    for collection, key in ((intents, "intent_id"), (future_states, "future_state_id"), (combinations, "combination_id")):
        for item in collection:
            if isinstance(item, Mapping) and item.get(key):
                result[str(item[key])] = item
    return result


def run_event_pipeline(
    event: Mapping[str, Any],
    *,
    registry_index,
    actor_hints: Sequence[Mapping[str, Any]] = (),
    actor_dictionary: Mapping[str, str] | None = None,
    explicit_state_dimensions: Mapping[str, Sequence[Mapping[str, Any]]] | None = None,
    scenario_variants: Mapping[str, Sequence[Mapping[str, Any]]] | None = None,
    pattern_priors: Sequence[Mapping[str, Any]] = (),
    memory_priors: Sequence[Mapping[str, Any]] = (),
    existing_combination_signatures: Sequence[str] = (),
    existing_intents: Sequence[Mapping[str, Any]] = (),
    domain_future_templates: Sequence[Mapping[str, Any]] = (),
    domain_evidence_predictions: Sequence[Mapping[str, Any]] = (),
    evidence_results: Mapping[str, Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    evidence_results = evidence_results or {}
    stage_results: dict[str, Any] = {}

    activation = activate_event(event, registry_index)
    stage_results["activation"] = activation.to_dict()
    working_event = apply_activations_to_event(event, activation)

    roles = infer_actor_roles(
        working_event,
        actor_hints=actor_hints,
        actor_dictionary=actor_dictionary,
    )
    stage_results["actor_roles"] = roles.to_dict()
    working_event = _apply_actor_roles(working_event, roles)

    actor_states = build_actor_state_hypotheses(
        working_event,
        roles.payload.get("actor_role_assignments", []),
        explicit_state_dimensions=explicit_state_dimensions,
        scenario_variants=scenario_variants,
    )
    stage_results["actor_states"] = actor_states.to_dict()

    relation_graph = build_event_relation_graph(working_event)
    stage_results["relation_graph"] = relation_graph.to_dict()
    working_event["relation_ids"] = sorted({
        *working_event.get("relation_ids", []),
        *[str(r["relation_id"]) for r in relation_graph.payload.get("relations", [])],
    })

    combinations = generate_combinations(
        working_event,
        relations=relation_graph.payload.get("relations", []),
        actor_states=actor_states.payload.get("actor_state_hypotheses", []),
        pattern_priors=pattern_priors,
        memory_priors=memory_priors,
        existing_signatures=existing_combination_signatures,
    )
    stage_results["combinations"] = combinations.to_dict()
    combination_records = combinations.payload.get("combination_records", [])
    working_event["combination_ids"] = [str(c["combination_id"]) for c in combination_records]

    live_intents = generate_live_intents(
        working_event,
        roles.payload.get("actor_role_assignments", []),
        actor_states=actor_states.payload.get("actor_state_hypotheses", []),
        combination_records=combination_records,
        existing_intents=existing_intents,
    )
    stage_results["live_intents"] = live_intents.to_dict()
    intent_candidates = live_intents.payload.get("intent_candidates", [])

    future_states = reconstruct_future_states(
        working_event,
        intent_candidates=intent_candidates,
        explicit_templates=domain_future_templates,
    )
    stage_results["future_states"] = future_states.to_dict()
    future_candidates = future_states.payload.get("future_state_candidates", [])

    predictions = generate_evidence_predictions(
        working_event,
        intent_candidates=intent_candidates,
        future_states=future_candidates,
        combination_records=combination_records,
        domain_predictions=domain_evidence_predictions,
    )
    stage_results["evidence_predictions"] = predictions.to_dict()
    evidence_predictions = predictions.payload.get("evidence_predictions", [])
    working_event["evidence_prediction_ids"] = [str(p["evidence_prediction_id"]) for p in evidence_predictions]

    rfr = run_rfr(
        working_event,
        intent_candidates=intent_candidates,
        future_states=future_candidates,
        combination_records=combination_records,
        evidence_predictions=evidence_predictions,
        evidence_results=evidence_results,
    )
    stage_results["rfr"] = rfr.to_dict()
    rfr_by_hypothesis = {str(a["hypothesis_ref"]): a for a in rfr.payload.get("assessments", [])}

    hypotheses = _hypothesis_index(intent_candidates, future_candidates, combination_records)
    falsifier_results: dict[str, Any] = {}
    maturity_results: dict[str, Any] = {}
    for href, hypothesis in hypotheses.items():
        declared = hypothesis.get("falsifiers", [])
        context = {
            "event": working_event,
            "hypothesis": hypothesis,
            "rfr": rfr_by_hypothesis.get(href, {}),
            "evidence_results": evidence_results,
        }
        falsifier = evaluate_falsifiers(hypothesis_ref=href, falsifiers=declared, context=context)
        falsifier_results[href] = falsifier.to_dict()

        related_prediction_ids = {
            str(p["evidence_prediction_id"])
            for p in evidence_predictions
            if str(p.get("hypothesis_ref")) == href
        }
        evidence_records = [
            {"evidence_prediction_id": pid, **dict(evidence_results[pid])}
            for pid in related_prediction_ids if pid in evidence_results
        ]
        provenance_complete = bool(working_event.get("source_refs")) and bool(working_event.get("point_zero", {}).get("point_zero_id"))
        counter_case_tested = any(
            str(p.get("test_type")) == "COUNTER_CASE_SEARCH" and str(evidence_results.get(str(p.get("evidence_prediction_id")), {}).get("result", "")).upper() in {"PASS", "SUPPORTED", "CONFIRMED"}
            for p in evidence_predictions if str(p.get("hypothesis_ref")) == href
        )
        domain_anchor = any(
            str(p.get("domain", "GENERAL")) != "GENERAL"
            for p in evidence_predictions if str(p.get("hypothesis_ref")) == href
        )
        anchored = any(
            str(p.get("test_type")) in {"SOURCE_LINEAGE_AUDIT", "FUTURE_STATE_TRACE", "EXPECTED_DOWNSTREAM_TRACE", "DOMAIN_SPECIFIC_TEST"}
            and str(evidence_results.get(str(p.get("evidence_prediction_id")), {}).get("result", "")).upper() in {"PASS", "SUPPORTED", "CONFIRMED"}
            for p in evidence_predictions if str(p.get("hypothesis_ref")) == href
        )
        maturity = evaluate_maturity(
            hypothesis,
            rfr_assessment=rfr_by_hypothesis.get(href),
            falsifier_assessment=falsifier.payload,
            evidence_records=evidence_records,
            provenance_complete=provenance_complete,
            counter_case_tested=counter_case_tested,
            domain_anchor_present=domain_anchor,
            textual_or_operational_anchor_present=anchored,
        )
        maturity_results[href] = maturity.to_dict()

    stage_results["falsifiers"] = falsifier_results
    stage_results["maturity"] = maturity_results

    working_event["intent"] = intent_candidates[0] if intent_candidates else working_event.get("intent")
    working_event["candidate_brain_state_ids"] = [str(s["actor_state_id"]) for s in actor_states.payload.get("actor_state_hypotheses", [])]
    working_event["last_updated_by"] = PIPELINE_ID

    all_traces = []
    for result in (activation, roles, actor_states, relation_graph, combinations, live_intents, future_states, predictions, rfr):
        all_traces.extend(t.to_dict() for t in result.traces)
    pipeline_trace = TraceStep.create(
        PIPELINE_ID,
        "RUN_EVENT_THROUGH_BATCH3_NATIVE_PIPELINE",
        input_refs=[str(event.get("event_id"))],
        output_refs=[str(working_event.get("event_id"))] + sorted(hypotheses),
        rule_refs=["BATCH3_NATIVE_RUNTIME_NO_LLM_DEPENDENCY"],
        notes=["Persistent memory writeback/new-node promotion intentionally deferred to Batch-4."],
    )
    all_traces.append(pipeline_trace.to_dict())

    return {
        "pipeline_id": PIPELINE_ID,
        "pipeline_version": PIPELINE_VERSION,
        "event_id": working_event.get("event_id"),
        "working_event": canonicalize(working_event),
        "stages": stage_results,
        "trace": all_traces,
        "writeback_boundary": {
            "status": "NOT_IMPLEMENTED_IN_BATCH3",
            "next_batch": "BATCH4_MEMORY_WRITEBACK_AUTO_LINK_NODE_GROWTH",
            "automatic_persistent_writes_performed": 0,
        },
    }


def run_text_pipeline(
    text: str,
    *,
    sequence_id: str,
    repo_root: Path,
    decomposition_strategy: str = "HYBRID",
    source_type: str = "USER_INPUT",
    source_locator: str | None = None,
    actor_hints: Sequence[Mapping[str, Any]] = (),
    actor_dictionary: Mapping[str, str] | None = None,
    explicit_state_dimensions: Mapping[str, Sequence[Mapping[str, Any]]] | None = None,
    scenario_variants: Mapping[str, Sequence[Mapping[str, Any]]] | None = None,
    pattern_priors: Sequence[Mapping[str, Any]] = (),
    memory_priors: Sequence[Mapping[str, Any]] = (),
    existing_combination_signatures: Sequence[str] = (),
    existing_intents: Sequence[Mapping[str, Any]] = (),
    domain_future_templates: Sequence[Mapping[str, Any]] = (),
    domain_evidence_predictions: Sequence[Mapping[str, Any]] = (),
    evidence_results: Mapping[str, Mapping[str, Any]] | None = None,
) -> dict[str, Any]:
    source_lock = lock_text_source(text, source_type=source_type, locator=source_locator, scope={"sequence_id": sequence_id, "kind": "RUNTIME_INPUT"})
    decomposition = decompose_source(source_lock.payload, sequence_id=sequence_id, strategy=decomposition_strategy)
    registry_index = build_default_activation_index(repo_root)
    event_runs = [
        run_event_pipeline(
            event,
            registry_index=registry_index,
            actor_hints=actor_hints,
            actor_dictionary=actor_dictionary,
            explicit_state_dimensions=explicit_state_dimensions,
            scenario_variants=scenario_variants,
            pattern_priors=pattern_priors,
            memory_priors=memory_priors,
            existing_combination_signatures=existing_combination_signatures,
            existing_intents=existing_intents,
            domain_future_templates=domain_future_templates,
            domain_evidence_predictions=domain_evidence_predictions,
            evidence_results=evidence_results,
        )
        for event in decomposition.payload.get("events", [])
    ]
    return {
        "runtime_execution_id": stable_id("RUN", sequence_id, source_lock.payload.get("source_lock_id"), [r["event_id"] for r in event_runs]),
        "pipeline_id": PIPELINE_ID,
        "pipeline_version": PIPELINE_VERSION,
        "system_identity": "REAL_TIME_GROWING_ASI_PROTOTYPE",
        "sequence_id": sequence_id,
        "started_at": utc_now(),
        "source_lock": source_lock.to_dict(),
        "decomposition": decomposition.to_dict(),
        "registry_index_size": len(registry_index),
        "event_runs": event_runs,
        "event_count": len(event_runs),
        "persistent_write_count": 0,
        "next_runtime_boundary": "BATCH4_MEMORY_WRITEBACK_AUTO_LINK_NODE_GROWTH",
    }


def _load_optional(path: str | None, default: Any) -> Any:
    if not path:
        return default
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def main() -> int:
    parser = argparse.ArgumentParser(description="Run Sourceborn Batch-3 native runtime pipeline")
    parser.add_argument("--text", required=True)
    parser.add_argument("--sequence-id", required=True)
    parser.add_argument("--repo-root", default=str(Path(__file__).resolve().parents[3]))
    parser.add_argument("--strategy", default="HYBRID", choices=["WHOLE", "PARAGRAPH", "SENTENCE", "HYBRID", "LINE"])
    parser.add_argument("--actor-hints")
    parser.add_argument("--actor-dictionary")
    parser.add_argument("--state-dimensions")
    parser.add_argument("--scenario-variants")
    parser.add_argument("--memory-priors")
    parser.add_argument("--pattern-priors")
    parser.add_argument("--existing-intents")
    parser.add_argument("--evidence-results")
    parser.add_argument("--output", required=True)
    args = parser.parse_args()

    result = run_text_pipeline(
        args.text,
        sequence_id=args.sequence_id,
        repo_root=Path(args.repo_root),
        decomposition_strategy=args.strategy,
        actor_hints=_load_optional(args.actor_hints, []),
        actor_dictionary=_load_optional(args.actor_dictionary, {}),
        explicit_state_dimensions=_load_optional(args.state_dimensions, {}),
        scenario_variants=_load_optional(args.scenario_variants, {}),
        memory_priors=_load_optional(args.memory_priors, []),
        pattern_priors=_load_optional(args.pattern_priors, []),
        existing_intents=_load_optional(args.existing_intents, []),
        evidence_results=_load_optional(args.evidence_results, {}),
    )
    write_json(Path(args.output), result)
    print(json.dumps({
        "runtime_execution_id": result["runtime_execution_id"],
        "event_count": result["event_count"],
        "registry_index_size": result["registry_index_size"],
        "persistent_write_count": result["persistent_write_count"],
        "output": args.output,
    }, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
