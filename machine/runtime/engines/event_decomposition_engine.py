#!/usr/bin/env python3
"""Source-bound Event decomposition for the Sourceborn native runtime.

The engine creates EventRecord-compatible units from a source-lock packet.  It
is deliberately conservative: decomposition boundaries are structural, while
semantic Intent remains UNKNOWN until a later engine has enough evidence.
"""
from __future__ import annotations

from typing import Any, Iterable, Mapping
import re

from .runtime_core import (
    EngineResult,
    RuntimeContractError,
    TraceStep,
    canonicalize,
    stable_id,
    utc_now,
)

ENGINE_ID = "SB-RT-ENG-EVENT-DECOMPOSE-001"
RULES = [
    "EVERYTHING_HAPPENING_IS_EVENT",
    "ALL_EVENTS_HAVE_TYPED_INTENT_FIELD",
    "SOURCE_SPAN_MUST_SURVIVE_DECOMPOSITION",
    "UNKNOWN_OVER_INVENTED_INTENT",
]

SENTENCE_BOUNDARY_RE = re.compile(r"(?<=[.!?])(?:[\"'”’)]*)\s+(?=[A-Z0-9\"'“‘(])")
LIST_LINE_RE = re.compile(r"^\s*(?:[-*•]|\d+[.)]|[A-Za-z][.)])\s+")


def _span_offsets(text: str, fragments: list[str]) -> list[tuple[int, int]]:
    offsets: list[tuple[int, int]] = []
    cursor = 0
    for fragment in fragments:
        idx = text.find(fragment, cursor)
        if idx < 0:
            idx = text.find(fragment)
        if idx < 0:
            raise RuntimeContractError("Unable to preserve source span during decomposition")
        end = idx + len(fragment)
        offsets.append((idx, end))
        cursor = end
    return offsets


def split_source_text(text: str, strategy: str = "HYBRID") -> list[str]:
    """Return non-empty exact substrings from the source.

    HYBRID first respects paragraph/list boundaries, then sentence boundaries.
    No words are rewritten, normalized, or synthesized.
    """
    strategy = strategy.upper()
    if strategy not in {"WHOLE", "PARAGRAPH", "SENTENCE", "HYBRID", "LINE"}:
        raise RuntimeContractError(f"Unsupported decomposition strategy: {strategy}")
    if strategy == "WHOLE":
        return [text] if text.strip() else []
    if strategy == "LINE":
        return [line for line in text.splitlines(keepends=False) if line.strip()]
    if strategy == "PARAGRAPH":
        return [p for p in re.split(r"\n\s*\n", text) if p.strip()]
    if strategy == "SENTENCE":
        return [s for s in SENTENCE_BOUNDARY_RE.split(text) if s.strip()]

    # HYBRID: paragraph/list line first, then conservative sentence split.
    blocks: list[str] = []
    for paragraph in re.split(r"\n\s*\n", text):
        if not paragraph.strip():
            continue
        lines = paragraph.splitlines()
        if len(lines) > 1 and any(LIST_LINE_RE.match(line) for line in lines):
            blocks.extend(line for line in lines if line.strip())
        else:
            blocks.append(paragraph)
    fragments: list[str] = []
    for block in blocks:
        parts = [s for s in SENTENCE_BOUNDARY_RE.split(block) if s.strip()]
        fragments.extend(parts or [block])
    return fragments


def _unknown_intent(event_id: str, source_refs: list[str], point_zero_id: str) -> dict[str, Any]:
    intent_id = stable_id("INT", event_id, "NOT_YET_DECODED")
    return {
        "intent_id": intent_id,
        "event_id": event_id,
        "intent_type": "NOT_YET_DECODED",
        "actor": {"status": "UNKNOWN"},
        "desired_state_change": None,
        "target": None,
        "trigger_context": None,
        "pressure_constraints": [],
        "relationship_history_refs": [],
        "time_horizon": None,
        "expected_consequence": None,
        "supporting_evidence_refs": [],
        "contradicting_evidence_refs": [],
        "alternative_intent_ids": [],
        "falsifiers": [],
        "proof_debt": ["INTENT_NOT_YET_DECODED"],
        "epistemic_status": "UNKNOWN",
        "review_status": "OPEN",
        "source_refs": source_refs,
        "point_zero_ref": point_zero_id,
    }


def decompose_source(
    source_lock_packet: Mapping[str, Any],
    *,
    sequence_id: str,
    strategy: str = "HYBRID",
    event_type: str = "SOURCE_DERIVED_EVENT_UNIT",
    parent_event_id: str | None = None,
    create_local_point_zero: bool = True,
) -> EngineResult:
    raw_content = source_lock_packet.get("raw_content")
    source_refs_raw = source_lock_packet.get("source_refs")
    parent_pz = source_lock_packet.get("point_zero")
    if not isinstance(source_refs_raw, list) or not source_refs_raw:
        raise RuntimeContractError("Event decomposition requires source_refs")
    if not isinstance(parent_pz, Mapping) or parent_pz.get("status") not in {"LOCKED", "DECLARED", "LOCAL"}:
        raise RuntimeContractError("Event decomposition requires a locked Point Zero")
    if raw_content is None:
        raise RuntimeContractError("This decomposition engine requires textual raw_content; binary sources require an observation adapter first")
    if not isinstance(raw_content, str):
        raise RuntimeContractError("raw_content must be UTF-8 text")

    source_ids = [str(ref.get("source_id")) for ref in source_refs_raw if isinstance(ref, Mapping) and ref.get("source_id")]
    fragments = split_source_text(raw_content, strategy)
    if not fragments:
        raise RuntimeContractError("No Event units produced from source")
    offsets = _span_offsets(raw_content, fragments)
    events: list[dict[str, Any]] = []

    for index, (fragment, (start, end)) in enumerate(zip(fragments, offsets), start=1):
        event_id = stable_id("EVT", sequence_id, source_ids, start, end, fragment)
        local_pz_id = stable_id("PZ", event_id, parent_pz.get("point_zero_id")) if create_local_point_zero else str(parent_pz.get("point_zero_id"))
        point_zero = {
            "point_zero_id": local_pz_id,
            "scope": {
                "kind": "EVENT_SOURCE_SPAN",
                "source_ids": source_ids,
                "char_start": start,
                "char_end": end,
                "unit_index": index,
            },
            "status": "LOCAL" if create_local_point_zero else parent_pz.get("status"),
            "source_refs": source_ids,
            "parent_point_zero_id": parent_pz.get("point_zero_id") if create_local_point_zero else parent_pz.get("parent_point_zero_id"),
            "origin_distance_base": 0,
            "notes": "Local Event Point Zero preserves exact source-span custody.",
        }
        observation_id = stable_id("OBS", event_id, start, end)
        event = {
            "event_id": event_id,
            "version": "1.0.0",
            "event_type": event_type,
            "event_status": "OBSERVED",
            "source_refs": [
                {
                    **dict(ref),
                    "fragment_ref": f"chars:{start}-{end}",
                }
                for ref in source_refs_raw
                if isinstance(ref, Mapping)
            ],
            "point_zero": point_zero,
            "sequence_id": sequence_id,
            "subsequence_contract_id": None,
            "parent_event_id": parent_event_id,
            "child_event_ids": [],
            "observations": [
                {
                    "observation_id": observation_id,
                    "observation_type": "DIRECT_TEXTUAL",
                    "value": fragment,
                    "source_ref": source_ids[0] if len(source_ids) == 1 else None,
                    "location_or_span": {"char_start": start, "char_end": end},
                    "epistemic_status": "OBSERVED",
                    "damage_or_uncertainty": None,
                    "origin_distance": 0,
                }
            ],
            "actor_roles": [],
            "object_ids": [],
            "state_refs": [],
            "relation_ids": [],
            "order_types": ["REPRESENTATION"],
            "intent": _unknown_intent(event_id, source_ids, local_pz_id),
            "activation_refs": [],
            "node_brain_refs": [],
            "candidate_brain_state_ids": [],
            "combination_ids": [],
            "evidence_prediction_ids": [],
            "supporting_evidence_refs": [],
            "contradicting_evidence_refs": [],
            "falsifier_ids": [],
            "pattern_contribution_ids": [],
            "pattern_candidate_ids": [],
            "memory_write_refs": [],
            "seed_ids": [],
            "origin_distance": 0,
            "proof_debt": ["INTENT_NOT_YET_DECODED", "ACTOR_ROLES_NOT_YET_DECODED"],
            "maturity": "M0",
            "epistemic_status": "OBSERVED",
            "review_status": "OPEN",
            "lineage": [
                {"step_type": "SOURCE", "object_ref": sid, "notes": "Exact source custody"}
                for sid in source_ids
            ] + [
                {"step_type": "POINT_ZERO", "object_ref": local_pz_id, "notes": "Bounded Event origin"},
                {"step_type": "EVENT", "object_ref": event_id, "notes": "Structural decomposition only"},
            ],
            "created_at": utc_now(),
            "updated_at": utc_now(),
            "created_by": ENGINE_ID,
            "last_updated_by": ENGINE_ID,
        }
        events.append(event)

    # Add temporal/representation order only between source-neighbor units.
    relations: list[dict[str, Any]] = []
    for left, right in zip(events, events[1:]):
        relation_id = stable_id("REL", left["event_id"], "PRECEDES", right["event_id"])
        relations.append({
            "relation_id": relation_id,
            "relation_type": "PRECEDES",
            "order_type": "REPRESENTATION",
            "source_ref": left["source_refs"][0].get("source_id") if left["source_refs"] else None,
            "source_event_id": left["event_id"],
            "target_event_id": right["event_id"],
            "epistemic_status": "OBSERVED_SOURCE_ORDER",
            "status": "ACTIVE",
        })
        left["relation_ids"].append(relation_id)
        right["relation_ids"].append(relation_id)

    output_refs = [e["event_id"] for e in events] + [r["relation_id"] for r in relations]
    trace = TraceStep.create(
        ENGINE_ID,
        "DECOMPOSE_LOCKED_SOURCE_TO_EVENTS",
        input_refs=source_ids + [str(parent_pz.get("point_zero_id"))],
        output_refs=output_refs,
        rule_refs=RULES,
        notes=[f"strategy={strategy}", f"event_count={len(events)}"],
    )
    payload = {
        "decomposition_id": stable_id("EVTDEC", sequence_id, output_refs),
        "sequence_id": sequence_id,
        "strategy": strategy,
        "events": events,
        "relations": relations,
        "event_count": len(events),
        "source_character_count": len(raw_content),
        "all_source_content_preserved": True,
    }
    return EngineResult(ENGINE_ID, "COMPLETE", canonicalize(payload), [trace])
