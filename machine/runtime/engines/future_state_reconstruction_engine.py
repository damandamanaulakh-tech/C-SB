#!/usr/bin/env python3
"""Future-state reconstruction engine.

Sourceborn reconstructs Intent partly by asking which future difference an actor
may have been trying to produce.  This engine converts explicit Event future
states and live Intent desired-state structures into separately tagged future
state hypotheses.  It does not assert a desired future merely because an
artifact survived.
"""
from __future__ import annotations

from typing import Any, Mapping, Sequence

from .runtime_core import EngineResult, RuntimeContractError, TraceStep, canonicalize, stable_id

ENGINE_ID = "SB-RT-ENG-FUTURE-STATE-001"
RULES = [
    "FUTURE_STATE_HYPOTHESIS_NE_FACT",
    "SURVIVAL_NE_ORIGINAL_INTENT",
    "FUTURE_STATE_MAY_REVERSE_LINK_TO_INTENT",
    "OBSERVED_RESULT_NE_EXPECTED_RESULT",
]


def _from_event_state(event_id: str, state: Mapping[str, Any]) -> dict[str, Any]:
    state_id = str(state.get("state_id"))
    role = str(state.get("state_role"))
    direct = role in {"RESULTING_STATE", "EXPECTED_FUTURE_STATE"} and str(state.get("epistemic_status", "")) in {"OBSERVED", "SOURCE_STATED"}
    return {
        "future_state_id": stable_id("FSTATE", event_id, state_id, "EVENT_STATE"),
        "event_id": event_id,
        "source_state_ref": state_id,
        "source_intent_ref": None,
        "entity_ref": state.get("entity_ref"),
        "state_payload": canonicalize(state.get("state_payload")),
        "future_role": role,
        "time_horizon": "EVENT_RESULT" if role == "RESULTING_STATE" else "EVENT_FUTURE",
        "epistemic_status": str(state.get("epistemic_status", "UNKNOWN")),
        "maturity": "M2" if direct else "M1",
        "proof_debt": [] if direct else ["FUTURE_STATE_REQUIRES_EVIDENCE"],
        "supporting_evidence_refs": list(state.get("source_refs", [])),
        "contradicting_evidence_refs": [],
        "origin_distance": 1,
    }


def _from_intent(event_id: str, intent: Mapping[str, Any]) -> dict[str, Any] | None:
    desired = intent.get("desired_state_change")
    if desired is None:
        return None
    intent_id = str(intent.get("intent_id"))
    return {
        "future_state_id": stable_id("FSTATE", event_id, intent_id, desired, intent.get("target")),
        "event_id": event_id,
        "source_state_ref": None,
        "source_intent_ref": intent_id,
        "entity_ref": intent.get("target"),
        "state_payload": canonicalize(desired),
        "future_role": "INTENDED_FUTURE_STATE",
        "time_horizon": intent.get("time_horizon"),
        "epistemic_status": "DERIVED_HYPOTHESIS",
        "maturity": "M0" if intent.get("maturity") == "M0" else "M1",
        "proof_debt": ["INTENT_DERIVED_FUTURE_REQUIRES_EVIDENCE"],
        "supporting_evidence_refs": list(intent.get("supporting_evidence_refs", [])),
        "contradicting_evidence_refs": list(intent.get("contradicting_evidence_refs", [])),
        "origin_distance": int(intent.get("origin_distance", 1)) + 1,
    }


def reconstruct_future_states(
    event: Mapping[str, Any],
    *,
    intent_candidates: Sequence[Mapping[str, Any]] = (),
    explicit_templates: Sequence[Mapping[str, Any]] = (),
    max_candidates: int = 64,
) -> EngineResult:
    event_id = str(event.get("event_id", ""))
    if not event_id:
        raise RuntimeContractError("Future-state engine requires event_id")
    states: list[dict[str, Any]] = []

    for state in event.get("state_refs", []):
        if not isinstance(state, Mapping):
            continue
        if state.get("state_role") in {"RESULTING_STATE", "EXPECTED_FUTURE_STATE", "COUNTERFACTUAL_STATE"}:
            states.append(_from_event_state(event_id, state))

    for intent in intent_candidates:
        if len(states) >= max_candidates:
            break
        if not isinstance(intent, Mapping):
            continue
        candidate = _from_intent(event_id, intent)
        if candidate:
            states.append(candidate)

    # Domain adapters may provide explicit templates, but each remains a
    # hypothesis unless its own epistemic status is direct/source-stated.
    for template in explicit_templates:
        if len(states) >= max_candidates:
            break
        payload = template.get("state_payload")
        if payload is None:
            continue
        epistemic = str(template.get("epistemic_status", "NEW_SYNTHETIC"))
        states.append({
            "future_state_id": stable_id("FSTATE", event_id, "TEMPLATE", template),
            "event_id": event_id,
            "source_state_ref": template.get("source_state_ref"),
            "source_intent_ref": template.get("source_intent_ref"),
            "entity_ref": template.get("entity_ref"),
            "state_payload": canonicalize(payload),
            "future_role": str(template.get("future_role", "SYNTHETIC_FUTURE_STATE")),
            "time_horizon": template.get("time_horizon"),
            "epistemic_status": epistemic,
            "maturity": str(template.get("maturity", "M0")),
            "proof_debt": list(template.get("proof_debt", ["DOMAIN_TEMPLATE_REQUIRES_TESTING"])),
            "supporting_evidence_refs": list(template.get("supporting_evidence_refs", [])),
            "contradicting_evidence_refs": list(template.get("contradicting_evidence_refs", [])),
            "origin_distance": int(template.get("origin_distance", 2)),
        })

    deduped: dict[str, dict[str, Any]] = {s["future_state_id"]: s for s in states}
    states = list(deduped.values())[:max_candidates]
    states.sort(key=lambda s: (s["future_role"], s["future_state_id"]))

    # Reverse links are candidate paths; they do not prove the Intent.
    reverse_links = [
        {
            "relation_id": stable_id("REL", s["future_state_id"], "POSSIBLE_FUTURE_OF_INTENT", s.get("source_intent_ref")),
            "source_ref": s["future_state_id"],
            "relation_type": "OTHER",
            "extended_relation_type": "POSSIBLE_FUTURE_OF_INTENT",
            "target_ref": s.get("source_intent_ref"),
            "status": "CANDIDATE",
            "epistemic_status": "DERIVED_HYPOTHESIS",
        }
        for s in states if s.get("source_intent_ref")
    ]
    trace = TraceStep.create(
        ENGINE_ID,
        "RECONSTRUCT_POSSIBLE_FUTURE_STATES",
        input_refs=[event_id] + [str(i.get("intent_id")) for i in intent_candidates if i.get("intent_id")],
        output_refs=[s["future_state_id"] for s in states],
        rule_refs=RULES,
        notes=[f"future_state_count={len(states)}"],
    )
    return EngineResult(
        ENGINE_ID,
        "COMPLETE" if states else "PARTIAL",
        {"event_id": event_id, "future_state_candidates": states, "reverse_intent_links": reverse_links, "future_state_count": len(states)},
        [trace],
        warnings=[] if states else ["No explicit or derived future state available; future-state reconstruction remains open."],
    )
