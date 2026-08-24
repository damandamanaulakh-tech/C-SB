#!/usr/bin/env python3
"""Evidence-prediction engine.

Every non-trivial synthetic hypothesis should predict something that could
support, weaken, or falsify it.  This engine produces structural tests from
Intent, future-state, relation, actor-role and combination candidates.  Domain
adapters may add stronger predictions later, but cannot remove the generic
source/provenance and contradiction tests.
"""
from __future__ import annotations

from typing import Any, Iterable, Mapping, Sequence

from .runtime_core import EngineResult, RuntimeContractError, TraceStep, canonicalize, stable_id

ENGINE_ID = "SB-RT-ENG-EVIDENCE-PREDICTION-001"
RULES = [
    "HYPOTHESIS_REQUIRES_PREDICTED_EVIDENCE",
    "SUPPORT_NE_PROOF_BY_REPETITION",
    "INDEPENDENT_SOURCE_GROUPS_REQUIRED",
    "FALSIFIER_MUST_BE_DECLARABLE",
]


def _prediction(
    event_id: str,
    hypothesis_ref: str,
    test_type: str,
    expected: Any,
    *,
    failure_implication: str,
    priority: str = "NORMAL",
    domain: str = "GENERAL",
    source_independence_required: bool = False,
    evidence_scope: str = "CURRENT_AND_FUTURE_SOURCES",
) -> dict[str, Any]:
    prediction_id = stable_id("EPRED", event_id, hypothesis_ref, test_type, expected)
    return {
        "evidence_prediction_id": prediction_id,
        "event_id": event_id,
        "hypothesis_ref": hypothesis_ref,
        "test_type": test_type,
        "domain": domain,
        "expected_observation": canonicalize(expected),
        "evidence_scope": evidence_scope,
        "source_independence_required": source_independence_required,
        "priority": priority,
        "status": "OPEN",
        "test_result": "NOT_RUN",
        "supporting_evidence_refs": [],
        "contradicting_evidence_refs": [],
        "failure_implication": failure_implication,
        "epistemic_status": "PREDICTION",
    }


def _generic_intent_predictions(event_id: str, intent: Mapping[str, Any]) -> list[dict[str, Any]]:
    intent_id = str(intent.get("intent_id"))
    predictions: list[dict[str, Any]] = []
    actor = intent.get("actor_ref") or (intent.get("actor", {}) if isinstance(intent.get("actor"), Mapping) else {}).get("actor_ref")
    if actor:
        predictions.append(_prediction(
            event_id, intent_id, "ACTOR_ROLE_SUPPORT",
            {"actor_ref": actor, "required_role": (intent.get("actor") or {}).get("role") if isinstance(intent.get("actor"), Mapping) else None},
            failure_implication="Weakens the actor-specific Intent branch; does not falsify the Event itself.",
            priority="HIGH",
        ))
    if intent.get("desired_state_change") is not None:
        predictions.append(_prediction(
            event_id, intent_id, "FUTURE_STATE_TRACE",
            {"desired_state_change": intent.get("desired_state_change"), "target": intent.get("target")},
            failure_implication="Weakens the proposed desired-state reconstruction; alternative Intent remains open.",
            priority="HIGH",
        ))
    if intent.get("pressure_constraints"):
        predictions.append(_prediction(
            event_id, intent_id, "CONSTRAINT_CONTEXT_SUPPORT",
            {"constraints": list(intent.get("pressure_constraints", []))},
            failure_implication="Weakens the proposed pressure/constraint component of Intent.",
        ))
    predictions.append(_prediction(
        event_id, intent_id, "COUNTER_CASE_SEARCH",
        {"find_case_where_same_observed_event_features_occur_without_this_intent": True},
        failure_implication="A valid counter-case reduces generality or may falsify the Intent inference rule.",
        priority="HIGH",
        source_independence_required=True,
    ))
    return predictions


def _future_state_predictions(event_id: str, state: Mapping[str, Any]) -> list[dict[str, Any]]:
    sid = str(state.get("future_state_id"))
    return [
        _prediction(
            event_id, sid, "EXPECTED_DOWNSTREAM_TRACE",
            {"entity_ref": state.get("entity_ref"), "state_payload": state.get("state_payload"), "time_horizon": state.get("time_horizon")},
            failure_implication="Weakens or falsifies the future-state branch depending on trace completeness and time horizon.",
            priority="HIGH",
        ),
        _prediction(
            event_id, sid, "ALTERNATIVE_CAUSE_SEARCH",
            {"same_future_state_possible_from_other_intents_or_events": True},
            failure_implication="If alternatives explain the same state equally well, this future state cannot uniquely identify Intent.",
            source_independence_required=True,
        ),
    ]


def _combination_predictions(event_id: str, combination: Mapping[str, Any]) -> list[dict[str, Any]]:
    cid = str(combination.get("combination_id"))
    ctype = str(combination.get("combination_type"))
    component_ids = [str(c.get("component_id")) for c in combination.get("components", []) if isinstance(c, Mapping) and c.get("component_id")]
    predictions = [
        _prediction(
            event_id, cid, "COMPONENT_RELATION_SUPPORT",
            {"components": component_ids, "combination_type": ctype},
            failure_implication="Without a legal relation/context, the combination is arbitrary and should be rejected or weakened.",
        ),
        _prediction(
            event_id, cid, "NOVELTY_RECHECK",
            {"signature": combination.get("component_signature"), "not_already_explicitly_stored": True},
            failure_implication="If an equivalent combination already exists, novelty count must not increase.",
        ),
    ]
    if ctype == "CONTRADICTION_COMBINATION":
        predictions.append(_prediction(
            event_id, cid, "CONTRADICTION_RESOLUTION_TEST",
            {"preserve_both_sides_until_scope_or_evidence_resolves": True},
            failure_implication="Silent merge is invalid; branch must remain unresolved.",
            priority="HIGH",
        ))
    if ctype == "COUNTERFACTUAL_COMBINATION":
        predictions.append(_prediction(
            event_id, cid, "COUNTERFACTUAL_DIFFERENCE_TEST",
            {"one_material_state_change_should_change_predicted_outcome_or_intent": True},
            failure_implication="If nothing changes, the varied state may not be causally/relevantly active.",
            priority="HIGH",
        ))
    return predictions


def generate_evidence_predictions(
    event: Mapping[str, Any],
    *,
    intent_candidates: Sequence[Mapping[str, Any]] = (),
    future_states: Sequence[Mapping[str, Any]] = (),
    combination_records: Sequence[Mapping[str, Any]] = (),
    domain_predictions: Sequence[Mapping[str, Any]] = (),
    max_predictions: int = 256,
) -> EngineResult:
    event_id = str(event.get("event_id", ""))
    if not event_id:
        raise RuntimeContractError("Evidence prediction engine requires event_id")

    predictions: list[dict[str, Any]] = []
    for intent in intent_candidates:
        predictions.extend(_generic_intent_predictions(event_id, intent))
    for state in future_states:
        predictions.extend(_future_state_predictions(event_id, state))
    for combination in combination_records:
        predictions.extend(_combination_predictions(event_id, combination))

    for domain in domain_predictions:
        hypothesis_ref = str(domain.get("hypothesis_ref", ""))
        if not hypothesis_ref:
            continue
        predictions.append(_prediction(
            event_id,
            hypothesis_ref,
            str(domain.get("test_type", "DOMAIN_SPECIFIC_TEST")),
            domain.get("expected_observation"),
            failure_implication=str(domain.get("failure_implication", "Domain-specific hypothesis should be weakened or falsified according to its declared rule.")),
            priority=str(domain.get("priority", "NORMAL")),
            domain=str(domain.get("domain", "DOMAIN_ADAPTER")),
            source_independence_required=bool(domain.get("source_independence_required", False)),
            evidence_scope=str(domain.get("evidence_scope", "CURRENT_AND_FUTURE_SOURCES")),
        ))

    # Generic provenance and source-independence tests apply to the entire Event.
    predictions.extend([
        _prediction(
            event_id, event_id, "SOURCE_LINEAGE_AUDIT",
            {"all_derived_objects_trace_to_locked_source_and_Point_Zero": True},
            failure_implication="Derived branch is invalid until provenance is repaired.",
            priority="CRITICAL",
        ),
        _prediction(
            event_id, event_id, "DUPLICATE_SOURCE_INDEPENDENCE_AUDIT",
            {"copies_or_derivatives_do_not_count_as_independent_evidence": True},
            failure_implication="Evidence strength must be reduced; duplicated lineage cannot increase corroboration count.",
            priority="CRITICAL",
            source_independence_required=True,
        ),
    ])

    deduped: dict[str, dict[str, Any]] = {p["evidence_prediction_id"]: p for p in predictions}
    final = list(deduped.values())[:max_predictions]
    final.sort(key=lambda p: ({"CRITICAL": 0, "HIGH": 1, "NORMAL": 2}.get(p["priority"], 3), p["hypothesis_ref"], p["test_type"]))

    trace = TraceStep.create(
        ENGINE_ID,
        "GENERATE_HYPOTHESIS_EVIDENCE_PREDICTIONS",
        input_refs=[event_id],
        output_refs=[p["evidence_prediction_id"] for p in final],
        rule_refs=RULES,
        notes=[f"prediction_count={len(final)}"],
    )
    return EngineResult(
        ENGINE_ID,
        "COMPLETE",
        {
            "event_id": event_id,
            "evidence_predictions": final,
            "prediction_count": len(final),
            "critical_count": sum(1 for p in final if p["priority"] == "CRITICAL"),
            "high_count": sum(1 for p in final if p["priority"] == "HIGH"),
        },
        [trace],
    )
