#!/usr/bin/env python3
"""Live compositional Intent engine.

Intent is generated from the current Event constellation rather than looked up
as one static label.  The engine keeps Intent separate from Motive and from
actor identity, and it performs structural novelty comparison so paraphrased
wording does not inflate the Intent count.
"""
from __future__ import annotations

from typing import Any, Iterable, Mapping, Sequence

from .runtime_core import EngineResult, RuntimeContractError, TraceStep, canonicalize, jaccard, stable_id, tokenize

ENGINE_ID = "SB-RT-ENG-LIVE-INTENT-001"
RULES = [
    "EVENT_HAS_INTENT_FIELD",
    "INTENT_NE_MOTIVE",
    "NEW_WORDING_NE_NEW_INTENT",
    "LIVE_INTENT_FROM_ACTIVE_CONSTELLATION",
    "INTENT_HYPOTHESIS_NE_INTENT_FACT",
]

ROLE_ACTION_TENDENCY = {
    "REQUESTER": "REQUEST_STATE_CHANGE",
    "CONTROLLER": "AUTHORIZE_REGULATE_OR_BLOCK_STATE_CHANGE",
    "AUTHOR": "CREATE_OR_FORMALIZE_REPRESENTATION",
    "DESIGNER": "SHAPE_FUTURE_CONFIGURATION",
    "PERFORMER": "EXECUTE_STATE_CHANGE",
    "CARRIER": "TRANSPORT_OR_PRESERVE_STATE",
    "BENEFICIARY": "RECEIVE_OR_GAIN_FROM_STATE_CHANGE",
    "AUDIENCE": "RECEIVE_INTERPRET_OR_RESPOND_TO_REPRESENTATION",
    "OBSERVER": "ACQUIRE_OR_RECORD_INFORMATION",
    "WRITER": "PERSIST_INFORMATION_OR_INSTRUCTION",
    "SUBJECT": "PARTICIPATE_IN_EVENT_STATE_CHANGE",
}

PRESSURE_DIMENSIONS = {
    "THREAT_LOSS", "VIGILANCE", "AVOIDANCE", "BIAS_HEURISTIC_PRESSURE",
    "NEED_VALUE_CONFLICT", "BELONGING_STATUS_GROUP", "MOTIVE_PRIORITY",
    "REWARD_APPROACH", "EFFORT", "PERSISTENCE",
}

NOVELTY_DIMENSIONS = (
    "actor_ref",
    "desired_state_change",
    "target",
    "action_tendency",
    "constraint_signature",
    "relationship_signature",
    "time_horizon",
    "expected_consequence",
)


def _future_states(event: Mapping[str, Any]) -> list[Mapping[str, Any]]:
    return [
        state for state in event.get("state_refs", [])
        if isinstance(state, Mapping) and state.get("state_role") in {"RESULTING_STATE", "EXPECTED_FUTURE_STATE", "COUNTERFACTUAL_STATE"}
    ]


def _constraints_from_state(actor_state: Mapping[str, Any]) -> list[str]:
    constraints: list[str] = []
    for dimension in actor_state.get("dimensions", []):
        if not isinstance(dimension, Mapping):
            continue
        name = str(dimension.get("dimension", ""))
        if name in PRESSURE_DIMENSIONS:
            constraints.append(f"{name}:{dimension.get('value')}")
    return sorted(set(constraints))


def _intent_signature(intent: Mapping[str, Any]) -> dict[str, Any]:
    return {
        "actor_ref": intent.get("actor_ref") or (intent.get("actor") or {}).get("actor_ref") if isinstance(intent.get("actor"), Mapping) else intent.get("actor_ref"),
        "desired_state_change": intent.get("desired_state_change"),
        "target": intent.get("target"),
        "action_tendency": intent.get("action_tendency"),
        "constraint_signature": sorted(intent.get("pressure_constraints", [])),
        "relationship_signature": sorted(intent.get("relationship_history_refs", [])),
        "time_horizon": intent.get("time_horizon"),
        "expected_consequence": intent.get("expected_consequence"),
    }


def _structural_similarity(a: Mapping[str, Any], b: Mapping[str, Any]) -> float:
    sa, sb = _intent_signature(a), _intent_signature(b)
    scores: list[float] = []
    for key in NOVELTY_DIMENSIONS:
        va, vb = sa.get(key), sb.get(key)
        if isinstance(va, list) or isinstance(vb, list):
            scores.append(jaccard(tokenize(va), tokenize(vb)))
        elif va is None and vb is None:
            scores.append(1.0)
        elif va == vb:
            scores.append(1.0)
        else:
            scores.append(jaccard(tokenize(va), tokenize(vb)))
    return sum(scores) / max(1, len(scores))


def _candidate(
    event: Mapping[str, Any],
    role: Mapping[str, Any],
    actor_state: Mapping[str, Any] | None,
    future_state: Mapping[str, Any] | None,
    combination_refs: Sequence[str],
) -> dict[str, Any]:
    event_id = str(event["event_id"])
    actor_ref = str(role.get("actor_ref"))
    role_name = str(role.get("role", "SUBJECT"))
    action_tendency = ROLE_ACTION_TENDENCY.get(role_name, "PARTICIPATE_IN_EVENT_STATE_CHANGE")
    desired = future_state.get("state_payload") if future_state else None
    target = future_state.get("entity_ref") if future_state else (event.get("object_ids", [None])[0] if event.get("object_ids") else None)
    constraints = _constraints_from_state(actor_state or {})
    relationship_refs = [
        str(rid) for rid in event.get("relation_ids", []) if rid
    ]
    expected_consequence = desired
    time_horizon = None
    if future_state:
        time_horizon = "EVENT_FUTURE" if future_state.get("state_role") == "EXPECTED_FUTURE_STATE" else "EVENT_RESULT"
    signature_payload = {
        "event_id": event_id,
        "actor_ref": actor_ref,
        "role": role_name,
        "desired": desired,
        "target": target,
        "action_tendency": action_tendency,
        "constraints": constraints,
        "actor_state_ref": actor_state.get("actor_state_id") if actor_state else None,
        "future_state_ref": future_state.get("state_id") if future_state else None,
        "combination_refs": sorted(combination_refs),
    }
    intent_id = stable_id("INT", signature_payload)
    proof_debt = []
    if desired is None:
        proof_debt.append("DESIRED_STATE_CHANGE_NOT_EXPLICIT")
    if role.get("epistemic_status") not in {"OBSERVED", "SOURCE_STATED", "APPROVED"}:
        proof_debt.append("ACTOR_ROLE_IS_HYPOTHESIS")
    if actor_state and actor_state.get("epistemic_status") in {"NEW_SYNTHETIC", "UNKNOWN"}:
        proof_debt.append("ACTOR_STATE_IS_HYPOTHESIS")
    return {
        "intent_id": intent_id,
        "event_id": event_id,
        "intent_type": "DERIVED_INTENT_HYPOTHESIS",
        "actor_ref": actor_ref,
        "actor": {
            "actor_ref": actor_ref,
            "role": role_name,
            "actor_state_ref": actor_state.get("actor_state_id") if actor_state else None,
        },
        "desired_state_change": desired,
        "target": target,
        "action_tendency": action_tendency,
        "trigger_context": event_id,
        "pressure_constraints": constraints,
        "relationship_history_refs": relationship_refs,
        "time_horizon": time_horizon,
        "expected_consequence": expected_consequence,
        "stated_intent": None,
        "inferred_intent": {
            "role_tendency": action_tendency,
            "future_state_ref": future_state.get("state_id") if future_state else None,
        },
        "stated_motive": None,
        "operating_motive_hypothesis": None,
        "goal": desired,
        "method": None,
        "conditions": constraints,
        "typed_order_refs": [],
        "actor_view_refs": [],
        "supporting_evidence_refs": sorted(set(role.get("supporting_evidence_refs", []))),
        "contradicting_evidence_refs": [],
        "alternative_intent_ids": [],
        "combination_refs": sorted(set(combination_refs)),
        "falsifiers": [],
        "proof_debt": proof_debt or ["INTENT_REQUIRES_RFR"],
        "epistemic_status": "INFERRED",
        "review_status": "OPEN",
        "source_refs": [str(ref.get("source_id")) for ref in event.get("source_refs", []) if isinstance(ref, Mapping) and ref.get("source_id")],
        "point_zero_ref": event.get("point_zero", {}).get("point_zero_id"),
        "maturity": "M0" if proof_debt else "M1",
    }


def generate_live_intents(
    event: Mapping[str, Any],
    actor_role_assignments: Sequence[Mapping[str, Any]],
    *,
    actor_states: Sequence[Mapping[str, Any]] = (),
    combination_records: Sequence[Mapping[str, Any]] = (),
    existing_intents: Sequence[Mapping[str, Any]] = (),
    similarity_threshold: float = 0.88,
    max_intents: int = 64,
) -> EngineResult:
    event_id = str(event.get("event_id", ""))
    if not event_id:
        raise RuntimeContractError("Live Intent engine requires event_id")
    states_by_actor: dict[str, list[Mapping[str, Any]]] = {}
    for state in actor_states:
        if state.get("actor_ref"):
            states_by_actor.setdefault(str(state["actor_ref"]), []).append(state)
    future_states = _future_states(event)
    combo_refs = [str(c.get("combination_id")) for c in combination_records if c.get("combination_id")]

    candidates: list[dict[str, Any]] = []
    seen: set[str] = set()
    for role in actor_role_assignments:
        actor_ref = role.get("actor_ref")
        if not actor_ref:
            continue
        states = states_by_actor.get(str(actor_ref), [None]) or [None]
        futures = future_states or [None]
        for state in states:
            for future in futures:
                if len(candidates) >= max_intents:
                    break
                candidate = _candidate(event, role, state, future, combo_refs)
                signature_key = stable_id("INTSIG", _intent_signature(candidate))
                if signature_key in seen:
                    continue
                seen.add(signature_key)
                nearest = None
                nearest_score = 0.0
                for existing in existing_intents:
                    score = _structural_similarity(candidate, existing)
                    if score > nearest_score:
                        nearest, nearest_score = existing, score
                if nearest is not None and nearest_score >= similarity_threshold:
                    candidate["novelty"] = {
                        "status": "EXISTING_INTENT_STRUCTURE",
                        "nearest_intent_ref": nearest.get("intent_id"),
                        "similarity": round(nearest_score, 6),
                        "count_as_new_intent": False,
                    }
                else:
                    candidate["novelty"] = {
                        "status": "NEW_LIVE_INTENT_CANDIDATE",
                        "nearest_intent_ref": nearest.get("intent_id") if nearest else None,
                        "similarity": round(nearest_score, 6),
                        "count_as_new_intent": True,
                    }
                candidates.append(candidate)

    # If no actor is known, preserve the mandatory unknown Intent rather than
    # forcing an actor. The Event's existing Intent record is returned as-is.
    warnings: list[str] = []
    if not candidates:
        existing_event_intent = event.get("intent")
        if isinstance(existing_event_intent, Mapping):
            candidates.append(dict(existing_event_intent))
            warnings.append("No actor-role path available; retained Event's UNKNOWN/NOT_YET_DECODED Intent.")

    ids = [str(c.get("intent_id")) for c in candidates if c.get("intent_id")]
    for candidate in candidates:
        candidate["alternative_intent_ids"] = sorted(i for i in ids if i != candidate.get("intent_id"))

    trace = TraceStep.create(
        ENGINE_ID,
        "GENERATE_LIVE_INTENT_CANDIDATES",
        input_refs=[event_id],
        output_refs=ids,
        rule_refs=RULES,
        notes=[
            f"candidate_count={len(candidates)}",
            f"new_count={sum(1 for c in candidates if c.get('novelty', {}).get('count_as_new_intent') is True)}",
        ],
    )
    return EngineResult(
        ENGINE_ID,
        "COMPLETE" if candidates else "PARTIAL",
        {
            "event_id": event_id,
            "intent_candidates": candidates,
            "intent_candidate_count": len(candidates),
            "new_intent_structure_count": sum(1 for c in candidates if c.get("novelty", {}).get("count_as_new_intent") is True),
            "paraphrase_or_existing_count": sum(1 for c in candidates if c.get("novelty", {}).get("count_as_new_intent") is False),
        },
        [trace],
        warnings=warnings,
    )
