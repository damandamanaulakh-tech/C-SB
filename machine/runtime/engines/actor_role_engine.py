#!/usr/bin/env python3
"""Actor-role separation engine.

The purpose of this engine is not named-entity recognition.  Its purpose is to
keep operational roles distinct while Sourceborn reconstructs an Event:
SUBJECT != REQUESTER != CONTROLLER != AUTHOR != PERFORMER != BENEFICIARY !=
AUDIENCE.  Explicit structured hints are preferred; lexical cues may create
reviewable hypotheses but never source facts.
"""
from __future__ import annotations

from typing import Any, Iterable, Mapping, Sequence
import re

from .runtime_core import EngineResult, RuntimeContractError, TraceStep, ensure_point_zero_locked, stable_id, tokenize

ENGINE_ID = "SB-RT-ENG-ACTOR-ROLE-001"
RULES = [
    "SUBJECT_NE_REQUESTER",
    "REQUESTER_NE_CONTROLLER",
    "CONTROLLER_NE_PERFORMER",
    "AUTHOR_NE_PERFORMER",
    "BENEFICIARY_NE_AUDIENCE",
    "ROLE_HYPOTHESIS_NE_ROLE_FACT",
]

ROLE_TYPES = (
    "SUBJECT", "REQUESTER", "CONTROLLER", "AUTHOR", "DESIGNER", "PERFORMER",
    "CARRIER", "BENEFICIARY", "AUDIENCE", "OBSERVER", "WRITER", "UNKNOWN",
)

ROLE_CUES: dict[str, set[str]] = {
    "REQUESTER": {"ask", "asked", "request", "requested", "order", "ordered", "commission", "commissioned", "instruct", "instructed"},
    "CONTROLLER": {"authorize", "authorized", "approve", "approved", "permit", "permitted", "control", "controlled", "govern", "governed"},
    "AUTHOR": {"author", "authored", "write", "wrote", "compose", "composed", "scribe", "drafted"},
    "DESIGNER": {"design", "designed", "plan", "planned", "architect", "layout"},
    "PERFORMER": {"perform", "performed", "make", "made", "carve", "carved", "build", "built", "execute", "executed", "deliver", "delivered"},
    "CARRIER": {"carry", "carried", "transport", "transported", "bearer", "vehicle"},
    "BENEFICIARY": {"benefit", "beneficiary", "for_him", "for_her", "for_them", "receive", "received"},
    "AUDIENCE": {"audience", "display", "displayed", "public", "viewer", "readers", "worshippers"},
    "OBSERVER": {"observe", "observed", "witness", "witnessed", "saw", "seen"},
    "WRITER": {"record", "recorded", "inscribe", "inscribed", "write", "wrote", "scribe"},
}


def _event_text(event: Mapping[str, Any]) -> str:
    values: list[str] = []
    for obs in event.get("observations", []):
        if isinstance(obs, Mapping) and isinstance(obs.get("value"), str):
            values.append(obs["value"])
    return "\n".join(values)


def _normalize_actor_hint(hint: Mapping[str, Any], event_id: str) -> dict[str, Any]:
    role = str(hint.get("role", "UNKNOWN")).upper()
    if role not in ROLE_TYPES:
        raise RuntimeContractError(f"Unsupported actor role: {role}")
    actor_ref = hint.get("actor_ref") or hint.get("actor_id") or hint.get("name")
    if not actor_ref:
        raise RuntimeContractError("Actor-role hint requires actor_ref/actor_id/name")
    epistemic = str(hint.get("epistemic_status", "SOURCE_STATED"))
    return {
        "assignment_id": stable_id("AROLE", event_id, role, actor_ref, epistemic),
        "role": role,
        "actor_ref": str(actor_ref),
        "actor_type": hint.get("actor_type", "UNKNOWN"),
        "view_ref": hint.get("view_ref"),
        "state_ref": hint.get("state_ref"),
        "supporting_evidence_refs": sorted(set(hint.get("supporting_evidence_refs", []))),
        "epistemic_status": epistemic,
        "origin_distance": int(hint.get("origin_distance", 0 if epistemic in {"OBSERVED", "SOURCE_STATED"} else 1)),
        "confidence": hint.get("confidence"),
        "source": "EXPLICIT_ROLE_HINT",
    }


def infer_actor_roles(
    event: Mapping[str, Any],
    *,
    actor_hints: Sequence[Mapping[str, Any]] = (),
    actor_dictionary: Mapping[str, str] | None = None,
    lexical_hypotheses: bool = True,
) -> EngineResult:
    ensure_point_zero_locked(event)
    event_id = str(event.get("event_id", ""))
    if not event_id:
        raise RuntimeContractError("Actor-role engine requires event_id")

    assignments: list[dict[str, Any]] = []
    warnings: list[str] = []
    for hint in actor_hints:
        assignments.append(_normalize_actor_hint(hint, event_id))

    # Preserve already attached roles as first-class inputs.
    for existing in event.get("actor_roles", []):
        if isinstance(existing, Mapping) and existing.get("actor_ref"):
            merged = dict(existing)
            merged.setdefault("assignment_id", stable_id("AROLE", event_id, merged.get("role"), merged.get("actor_ref"), "EXISTING"))
            merged.setdefault("source", "EXISTING_EVENT_ROLE")
            assignments.append(merged)

    text = _event_text(event)
    lower = text.lower()
    tokens = tokenize(text)
    actor_dictionary = actor_dictionary or {}

    # Lexical hypotheses are deliberately weak. They only run for actor names
    # supplied by the caller; the engine does not invent a person from a pronoun.
    if lexical_hypotheses and actor_dictionary:
        for actor_ref, actor_surface in actor_dictionary.items():
            surface = actor_surface.lower().strip()
            if not surface or surface not in lower:
                continue
            window_start = max(0, lower.find(surface) - 120)
            window_end = min(len(lower), lower.find(surface) + len(surface) + 120)
            local_tokens = tokenize(lower[window_start:window_end])
            for role, cues in ROLE_CUES.items():
                matched = sorted(local_tokens & cues)
                if not matched:
                    continue
                assignments.append({
                    "assignment_id": stable_id("AROLE", event_id, role, actor_ref, matched),
                    "role": role,
                    "actor_ref": actor_ref,
                    "actor_type": "UNKNOWN",
                    "view_ref": None,
                    "state_ref": None,
                    "supporting_evidence_refs": [],
                    "epistemic_status": "INFERRED",
                    "origin_distance": 1,
                    "confidence": min(0.65, 0.30 + 0.10 * len(matched)),
                    "matched_cues": matched,
                    "source": "LEXICAL_ROLE_HYPOTHESIS",
                })

    # Deduplicate exact actor-role pairs while preserving stronger epistemic
    # records. Never collapse different roles for the same actor.
    rank = {"OBSERVED": 5, "SOURCE_STATED": 4, "APPROVED": 4, "INFERRED": 2, "SYNTHETIC": 1, "UNKNOWN": 0}
    chosen: dict[tuple[str, str], dict[str, Any]] = {}
    for assignment in assignments:
        key = (str(assignment.get("actor_ref")), str(assignment.get("role")))
        previous = chosen.get(key)
        if previous is None or rank.get(str(assignment.get("epistemic_status")), 0) > rank.get(str(previous.get("epistemic_status")), 0):
            chosen[key] = assignment
    final = sorted(chosen.values(), key=lambda a: (str(a.get("actor_ref")), str(a.get("role"))))

    if not final:
        warnings.append("No actor role could be established; role state remains UNKNOWN rather than inventing an actor.")

    # Detect multi-role actors but do not treat that as conflict: one actor may
    # legitimately be requester+controller, for example, if separately supported.
    roles_by_actor: dict[str, list[str]] = {}
    for assignment in final:
        roles_by_actor.setdefault(str(assignment["actor_ref"]), []).append(str(assignment["role"]))
    role_matrix = [
        {"actor_ref": actor, "roles": sorted(roles), "role_count": len(roles)}
        for actor, roles in sorted(roles_by_actor.items())
    ]

    trace = TraceStep.create(
        ENGINE_ID,
        "SEPARATE_EVENT_ACTOR_ROLES",
        input_refs=[event_id],
        output_refs=[a["assignment_id"] for a in final],
        rule_refs=RULES,
        notes=[f"assignments={len(final)}", f"actors={len(role_matrix)}"],
    )
    return EngineResult(
        ENGINE_ID,
        "COMPLETE" if final else "PARTIAL",
        {
            "event_id": event_id,
            "actor_role_assignments": final,
            "role_matrix": role_matrix,
            "unassigned_role_types": [role for role in ROLE_TYPES if role != "UNKNOWN" and role not in {a["role"] for a in final}],
        },
        [trace],
        warnings=warnings,
    )
