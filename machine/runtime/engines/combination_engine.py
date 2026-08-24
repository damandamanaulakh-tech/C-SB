#!/usr/bin/env python3
"""Bounded Sourceborn Combination Engine.

The engine assembles existing primitives into candidate structures through six
approved modes.  It deliberately avoids a Cartesian product over the Brain.
Every CombinationRecord carries component lineage, generation pass, budget,
novelty status and candidate outputs.
"""
from __future__ import annotations

from itertools import combinations
from typing import Any, Iterable, Mapping, Sequence

from .runtime_core import EngineResult, RuntimeContractError, TraceStep, canonicalize, stable_id, tokenize

ENGINE_ID = "SB-RT-ENG-COMBINATION-001"
RULES = [
    "COMBINATION_NE_NEW_PRIMITIVE",
    "NEW_WORDING_NE_NEW_INTENT",
    "BOUNDED_GENERATION_NOT_CARTESIAN_EXPLOSION",
    "CONTRADICTIONS_REMAIN_SEPARATE",
    "NOVELTY_REQUIRES_COMPARISON_TO_EXISTING_MEMORY",
]

MODE_MAP = {
    "ADJACENCY": "ADJACENCY_COMBINATION",
    "PATTERN_SUPPORTED": "PATTERN_SUPPORTED_COMBINATION",
    "CONTRADICTION": "CONTRADICTION_COMBINATION",
    "COUNTERFACTUAL": "COUNTERFACTUAL_COMBINATION",
    "CROSS_DOMAIN": "CROSS_DOMAIN_COMBINATION",
    "NOVELTY": "NOVELTY_COMBINATION",
}

DOMAIN_BY_OBJECT_TYPE = {
    "HUMAN_PARAMETER": "HUMAN",
    "HUMAN_CONTAINER": "HUMAN",
    "HUMAN_SEGMENT": "HUMAN",
    "AI_FUNCTION": "AI",
    "AI_PARAMETER": "AI",
    "WISDOM_OBJECT": "WISDOM",
    "ASI_GOVERNANCE": "ASI",
    "ASI_NODE": "ASI",
    "UNIVERSAL_RUBRIC": "SEQUENCE",
    "ENGINE": "ENGINE",
}


def _component(component_id: str, component_type: str, role: str, *, source_refs: Iterable[str] = (), origin_distance: int = 1, relevance: float | None = None, epistemic_status: str | None = None) -> dict[str, Any]:
    return {
        "component_id": component_id,
        "component_type": component_type,
        "component_role": role,
        "source_refs": sorted(set(source_refs)),
        "origin_distance": max(0, int(origin_distance)),
        "relevance": relevance,
        "epistemic_status": epistemic_status,
    }


def _activation_components(event: Mapping[str, Any]) -> list[dict[str, Any]]:
    result: list[dict[str, Any]] = []
    for activation in event.get("activation_refs", []):
        if not isinstance(activation, Mapping) or not activation.get("object_id"):
            continue
        result.append(_component(
            str(activation["object_id"]),
            str(activation.get("object_type", "OTHER")),
            "INPUT",
            source_refs=[str(activation.get("registry_source_file"))] if activation.get("registry_source_file") else [],
            origin_distance=int(activation.get("source_distance", 1)),
            relevance=activation.get("activation_strength"),
            epistemic_status=str(activation.get("epistemic_status", "EXISTING_REGISTRY_ACTIVATION")),
        ))
    return result


def _actor_state_components(actor_states: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        _component(
            str(state["actor_state_id"]), "ACTOR_STATE", "CONTEXT",
            origin_distance=1,
            epistemic_status=str(state.get("epistemic_status", "UNKNOWN")),
        )
        for state in actor_states
        if state.get("actor_state_id")
    ]


def _relation_components(relations: Sequence[Mapping[str, Any]]) -> list[dict[str, Any]]:
    return [
        _component(
            str(rel["relation_id"]), "RELATION", "CONSTRAINT" if rel.get("status") == "ACTIVE" else "ALTERNATIVE",
            source_refs=rel.get("supporting_evidence_refs", []),
            origin_distance=1 if rel.get("status") == "ACTIVE" else 2,
            epistemic_status=str(rel.get("epistemic_status", "UNKNOWN")),
        )
        for rel in relations
        if rel.get("relation_id")
    ]


def _pair_signature(left: Mapping[str, Any], right: Mapping[str, Any], mode: str) -> str:
    return stable_id("CSIG", mode, sorted([str(left["component_id"]), str(right["component_id"])]))


def _output(output_type: str, combination_id: str, payload: Mapping[str, Any], *, epistemic_status: str = "NEW_SYNTHETIC", maturity: str = "M0", status: str = "NEW_SYNTHETIC") -> dict[str, Any]:
    output_id = stable_id("COUT", combination_id, output_type, payload)
    return {
        "output_id": output_id,
        "output_type": output_type,
        "summary": None,
        "payload": canonicalize(payload),
        "status": status,
        "epistemic_status": epistemic_status,
        "origin_distance": 2,
        "maturity": maturity,
        "proof_debt": ["REQUIRES_EVIDENCE_PREDICTION", "REQUIRES_RFR"],
        "supporting_evidence_refs": [],
        "contradicting_evidence_refs": [],
        "falsifier_refs": [],
        "memory_write_ref": None,
    }


def _make_record(
    event: Mapping[str, Any],
    mode: str,
    components: Sequence[Mapping[str, Any]],
    *,
    output_specs: Sequence[tuple[str, Mapping[str, Any]]],
    existing_signatures: set[str],
    max_candidates: int,
    max_depth: int,
    reason: str,
) -> dict[str, Any]:
    if mode not in MODE_MAP:
        raise RuntimeContractError(f"Unsupported combination mode: {mode}")
    event_id = str(event.get("event_id"))
    sequence_id = str(event.get("sequence_id"))
    component_ids = sorted(str(c["component_id"]) for c in components)
    signature = stable_id("CSIG", mode, component_ids)
    combination_id = stable_id("COMB", event_id, signature)
    novelty_status = "EXISTING_EXACT" if signature in existing_signatures else "NEW_COMBINATION_EXISTING_PRIMITIVES"
    outputs = [_output(output_type, combination_id, payload) for output_type, payload in output_specs]
    return {
        "combination_id": combination_id,
        "version": "1.0.0",
        "combination_type": MODE_MAP[mode],
        "status": "CANDIDATE",
        "source_refs": sorted({ref for c in components for ref in c.get("source_refs", [])}),
        "point_zero_refs": [str(event.get("point_zero", {}).get("point_zero_id"))],
        "event_refs": [event_id],
        "sequence_ref": sequence_id,
        "node_brain_refs": [],
        "components": list(components),
        "component_signature": signature,
        "passes": [{
            "pass_id": stable_id("CPASS", combination_id, mode, 1),
            "pass_type": mode,
            "iteration": 1,
            "input_component_refs": component_ids,
            "new_information_entered": True,
            "generator_ref": ENGINE_ID,
            "rule_refs": RULES,
            "objects_created": [o["output_id"] for o in outputs],
            "status": "COMPLETE",
            "stop_reason": None,
        }],
        "constraints": [
            {"constraint_type": "SOURCE_PROVENANCE", "condition": "all components preserve lineage", "hard_or_soft": "HARD", "status": "PASS", "rule_ref": "SOURCE_LINEAGE"},
            {"constraint_type": "CANDIDATE_BUDGET", "condition": {"max_candidates": max_candidates}, "hard_or_soft": "HARD", "status": "PASS", "rule_ref": "BOUNDED_GENERATION"},
        ],
        "budget": {
            "max_candidates": max_candidates,
            "max_candidates_per_pass": max_candidates,
            "max_depth": max_depth,
            "max_origin_distance": 8,
            "max_cross_domain_edges": 8,
            "max_counterfactuals": 8,
            "minimum_relevance": 0.0,
            "novelty_threshold": 0.5,
            "compute_budget_ref": None,
        },
        "relation_refs": [str(c["component_id"]) for c in components if c.get("component_type") == "RELATION"],
        "path_refs": [],
        "actor_role_refs": [],
        "actor_state_refs": [str(c["component_id"]) for c in components if c.get("component_type") == "ACTOR_STATE"],
        "actor_view_refs": [],
        "intent_refs": [],
        "future_state_refs": [],
        "pattern_refs": [str(c["component_id"]) for c in components if c.get("component_type") == "PATTERN"],
        "memory_refs": [str(c["component_id"]) for c in components if c.get("component_type") == "MEMORY"],
        "evidence_refs": [],
        "contradiction_refs": [],
        "novelty": {
            "novelty_status": novelty_status,
            "comparison_scope": "GLOBAL_MEMORY",
            "nearest_existing_refs": [],
            "matching_dimensions": [],
            "novel_dimensions": component_ids if novelty_status.startswith("NEW_") else [],
            "novelty_score": 1.0 if novelty_status.startswith("NEW_") else 0.0,
            "requires_new_primitive_review": False,
        },
        "outputs": outputs,
        "evidence_prediction_ids": [],
        "falsifier_ids": [],
        "epistemic_status": "NEW_SYNTHETIC",
        "maturity": "M0",
        "proof_debt": ["COMBINATION_REQUIRES_TESTING"],
        "lineage": [
            {"step_type": "EVENT", "object_ref": event_id, "notes": "Combination source Event"},
            *[{"step_type": "INPUT_COMPONENT", "object_ref": cid, "notes": reason} for cid in component_ids],
            {"step_type": "COMBINATION_PASS", "object_ref": stable_id("CPASS", combination_id, mode, 1), "notes": mode},
        ],
    }


def generate_combinations(
    event: Mapping[str, Any],
    *,
    relations: Sequence[Mapping[str, Any]] = (),
    actor_states: Sequence[Mapping[str, Any]] = (),
    pattern_priors: Sequence[Mapping[str, Any]] = (),
    memory_priors: Sequence[Mapping[str, Any]] = (),
    existing_signatures: Iterable[str] = (),
    max_candidates: int = 48,
    max_candidates_per_mode: int = 12,
    max_depth: int = 4,
) -> EngineResult:
    event_id = str(event.get("event_id", ""))
    if not event_id:
        raise RuntimeContractError("Combination engine requires event_id")
    existing = set(existing_signatures)
    activation_components = _activation_components(event)
    relation_components = _relation_components(relations)
    state_components = _actor_state_components(actor_states)
    pattern_components = [
        _component(str(p.get("pattern_id") or p.get("id")), "PATTERN", "PATTERN_PRIOR", epistemic_status=str(p.get("epistemic_status", "UNKNOWN")))
        for p in pattern_priors if p.get("pattern_id") or p.get("id")
    ]
    memory_components = [
        _component(str(m.get("memory_id") or m.get("id")), "MEMORY", "MEMORY_PRIOR", epistemic_status=str(m.get("epistemic_status", "UNKNOWN")))
        for m in memory_priors if m.get("memory_id") or m.get("id")
    ]

    records: list[dict[str, Any]] = []

    def add(record: dict[str, Any]) -> None:
        if len(records) >= max_candidates:
            return
        if record["combination_id"] not in {r["combination_id"] for r in records}:
            records.append(record)

    # C1: adjacency = pairs already linked by an ACTIVE relation.
    adjacency_count = 0
    component_by_id = {c["component_id"]: c for c in activation_components + state_components + pattern_components + memory_components}
    for rel in relations:
        if adjacency_count >= max_candidates_per_mode or len(records) >= max_candidates:
            break
        if rel.get("status") != "ACTIVE":
            continue
        left, right = str(rel.get("source_ref", "")), str(rel.get("target_ref", ""))
        if left in component_by_id and right in component_by_id:
            comps = [component_by_id[left], component_by_id[right]]
            add(_make_record(event, "ADJACENCY", comps, output_specs=[("RELATION_CANDIDATE", {"relation_ref": rel.get("relation_id"), "reason": "existing active adjacency"})], existing_signatures=existing, max_candidates=max_candidates, max_depth=max_depth, reason="ACTIVE_RELATION_ADJACENCY"))
            adjacency_count += 1

    # If no explicit adjacency exists, pair the strongest PRIMARY activations by
    # shared matched features. This remains a candidate, not an asserted relation.
    if adjacency_count == 0:
        primaries = [a for a in event.get("activation_refs", []) if isinstance(a, Mapping) and a.get("primary_or_secondary") == "PRIMARY"]
        for left, right in combinations(primaries[:8], 2):
            if adjacency_count >= max_candidates_per_mode or len(records) >= max_candidates:
                break
            shared = set(left.get("matched_features", [])) & set(right.get("matched_features", []))
            if not shared:
                continue
            comps = [
                _component(str(left["object_id"]), str(left.get("object_type", "OTHER")), "INPUT", relevance=left.get("activation_strength")),
                _component(str(right["object_id"]), str(right.get("object_type", "OTHER")), "INPUT", relevance=right.get("activation_strength")),
            ]
            add(_make_record(event, "ADJACENCY", comps, output_specs=[("RELATION_CANDIDATE", {"shared_features": sorted(shared), "status": "CANDIDATE"})], existing_signatures=existing, max_candidates=max_candidates, max_depth=max_depth, reason="SHARED_EVENT_FEATURES"))
            adjacency_count += 1

    # C2: pattern-supported combinations connect an activated component with an
    # existing pattern prior.  The pattern is context, never automatic proof.
    pattern_count = 0
    for pattern in pattern_components:
        for component in activation_components[:6]:
            if pattern_count >= max_candidates_per_mode or len(records) >= max_candidates:
                break
            add(_make_record(event, "PATTERN_SUPPORTED", [component, pattern], output_specs=[("PATTERN_CANDIDATE", {"prior_pattern_ref": pattern["component_id"], "new_event_ref": event_id, "status": "REQUIRES_COUNTER_CASE"})], existing_signatures=existing, max_candidates=max_candidates, max_depth=max_depth, reason="PATTERN_PRIOR_REUSE"))
            pattern_count += 1

    # C3: contradiction combinations explicitly preserve both sides.
    contradiction_count = 0
    for rel, rel_component in zip(relations, relation_components):
        relation_name = str(rel.get("extended_relation_type") or rel.get("relation_type"))
        if relation_name not in {"CONTRADICTS", "COUNTEREXAMPLE_TO", "FALSIFIES"}:
            continue
        if contradiction_count >= max_candidates_per_mode or len(records) >= max_candidates:
            break
        add(_make_record(event, "CONTRADICTION", [rel_component, _component(event_id, "EVENT", "ANCHOR", origin_distance=0, epistemic_status=str(event.get("epistemic_status", "UNKNOWN")))], output_specs=[("SEQUENCE_VARIANT", {"kind": "CONTRADICTION_BRANCH", "relation_ref": rel.get("relation_id"), "preserve_both_sides": True})], existing_signatures=existing, max_candidates=max_candidates, max_depth=max_depth, reason="EXPLICIT_CONTRADICTION"))
        contradiction_count += 1

    # C4: actor-state variants create one-change counterfactual branches.
    counterfactual_count = 0
    states_by_actor: dict[str, list[Mapping[str, Any]]] = {}
    for state in actor_states:
        if state.get("actor_ref"):
            states_by_actor.setdefault(str(state["actor_ref"]), []).append(state)
    for actor_ref, states in states_by_actor.items():
        base = next((s for s in states if s.get("variant_label") == "BASE_AVAILABLE_STATE"), states[0] if states else None)
        if not base:
            continue
        for variant in states:
            if variant is base or counterfactual_count >= max_candidates_per_mode or len(records) >= max_candidates:
                continue
            comps = [_component(str(base["actor_state_id"]), "ACTOR_STATE", "ANCHOR"), _component(str(variant["actor_state_id"]), "ACTOR_STATE", "COUNTERFACTUAL_CHANGE")]
            add(_make_record(event, "COUNTERFACTUAL", comps, output_specs=[("ACTOR_BRAIN_VARIANT", {"actor_ref": actor_ref, "base_state_ref": base["actor_state_id"], "variant_state_ref": variant["actor_state_id"]})], existing_signatures=existing, max_candidates=max_candidates, max_depth=max_depth, reason="ONE_ACTOR_MULTIPLE_STATE_BRANCH"))
            counterfactual_count += 1

    # C5: cross-domain pairs only when both are already activated in this Event.
    cross_count = 0
    by_domain: dict[str, list[dict[str, Any]]] = {}
    for component in activation_components:
        domain = DOMAIN_BY_OBJECT_TYPE.get(str(component.get("component_type")))
        if domain:
            by_domain.setdefault(domain, []).append(component)
    domains = sorted(by_domain)
    for d1, d2 in combinations(domains, 2):
        if cross_count >= max_candidates_per_mode or len(records) >= max_candidates:
            break
        c1, c2 = by_domain[d1][0], by_domain[d2][0]
        add(_make_record(event, "CROSS_DOMAIN", [c1, c2], output_specs=[("SEQUENCE_VARIANT", {"domains": [d1, d2], "rule": "cross-domain activation without ownership merge"})], existing_signatures=existing, max_candidates=max_candidates, max_depth=max_depth, reason="MULTI_DOMAIN_EVENT_ACTIVATION"))
        cross_count += 1

    # C6: novelty candidates combine one prior-memory component with one current
    # activation only when that exact signature has not appeared before.
    novelty_count = 0
    for memory in memory_components:
        for component in activation_components[:6]:
            if novelty_count >= max_candidates_per_mode or len(records) >= max_candidates:
                break
            signature = stable_id("CSIG", "NOVELTY", sorted([memory["component_id"], component["component_id"]]))
            if signature in existing:
                continue
            add(_make_record(event, "NOVELTY", [component, memory], output_specs=[("EVENT_HYPOTHESIS", {"new_combination": True, "current_component": component["component_id"], "memory_prior": memory["component_id"]})], existing_signatures=existing, max_candidates=max_candidates, max_depth=max_depth, reason="NEW_COMBINATION_EXISTING_PRIMITIVES"))
            novelty_count += 1

    traces = [TraceStep.create(
        ENGINE_ID,
        "GENERATE_BOUNDED_COMBINATIONS",
        input_refs=[event_id],
        output_refs=[r["combination_id"] for r in records],
        rule_refs=RULES,
        notes=[
            f"total={len(records)}",
            f"adjacency={adjacency_count}",
            f"pattern={pattern_count}",
            f"contradiction={contradiction_count}",
            f"counterfactual={counterfactual_count}",
            f"cross_domain={cross_count}",
            f"novelty={novelty_count}",
        ],
    )]

    return EngineResult(
        ENGINE_ID,
        "COMPLETE" if records else "PARTIAL",
        {
            "event_id": event_id,
            "combination_records": records,
            "combination_count": len(records),
            "counts_by_mode": {
                "ADJACENCY": adjacency_count,
                "PATTERN_SUPPORTED": pattern_count,
                "CONTRADICTION": contradiction_count,
                "COUNTERFACTUAL": counterfactual_count,
                "CROSS_DOMAIN": cross_count,
                "NOVELTY": novelty_count,
            },
            "budget": {"max_candidates": max_candidates, "max_candidates_per_mode": max_candidates_per_mode, "max_depth": max_depth},
            "cartesian_product_performed": False,
        },
        traces,
        warnings=[] if records else ["No legal bounded combination path produced a candidate."],
    )
