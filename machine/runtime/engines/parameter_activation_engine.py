#!/usr/bin/env python3
"""Registry-grounded activation engine.

The activation engine asks which *existing* Sourceborn objects are relevant to
an Event.  It never manufactures an ID to satisfy coverage.  Search is a
transparent lexical/structural baseline suitable for the native prototype;
later engines may add stronger retrieval mechanisms while preserving the same
ActivationRef contract and provenance.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Iterable, Mapping, Sequence

from .runtime_core import (
    EngineResult,
    RegistryIndex,
    RuntimeContractError,
    TraceStep,
    ensure_point_zero_locked,
    stable_id,
    tokenize,
)

ENGINE_ID = "SB-RT-ENG-ACTIVATION-001"
RULES = [
    "EXISTING_ID_BEFORE_NEW_ID",
    "ACTIVATION_NE_NEW_PARAMETER",
    "SOURCE_MAPPING_ADDITIVE",
    "UNKNOWN_OVER_INVENTED_COVERAGE",
]

DEFAULT_REGISTRY_ROOTS = (
    "registries/human",
    "registries/ai",
    "registries/wisdom",
    "registries/asi",
    "registries/sourceborn",
    "machine/rubrics",
)

ACTIVATABLE_TYPES = {
    "HUMAN_PARAMETER",
    "HUMAN_CONTAINER",
    "HUMAN_SEGMENT",
    "AI_FUNCTION",
    "WISDOM_OBJECT",
    "ASI_GOVERNANCE",
    "ASI_NODE",
    "ENGINE",
    "UNIVERSAL_RUBRIC",
    "PATTERN",
    "INTENT",
    "RELATION",
    "PATH",
    "OTHER",
}


def build_default_activation_index(repo_root: Path) -> RegistryIndex:
    """Index active registry JSON recursively, preserving exact source files."""
    index = RegistryIndex()
    for relative_root in DEFAULT_REGISTRY_ROOTS:
        root = repo_root / relative_root
        if not root.exists():
            continue
        for path in sorted(root.rglob("*.json")):
            # Generated reports/checkpoints do not belong in native activation.
            if any(part in {"generated", "tests", "checkpoints"} for part in path.parts):
                continue
            try:
                index.add_file(path, root=repo_root)
            except Exception:
                # One malformed/nonstandard registry must not silently poison the
                # whole activation pass.  Validator tooling reports such files;
                # this runtime simply omits unreadable JSON from this index.
                continue
    return index


def _event_query(event: Mapping[str, Any]) -> dict[str, Any]:
    observations = []
    for observation in event.get("observations", []):
        if isinstance(observation, Mapping):
            observations.append(observation.get("value"))
    state_payloads = []
    for state in event.get("state_refs", []):
        if isinstance(state, Mapping):
            state_payloads.append(state.get("state_payload"))
    actor_roles = []
    for role in event.get("actor_roles", []):
        if isinstance(role, Mapping):
            actor_roles.extend([role.get("role"), role.get("actor_ref"), role.get("actor_type")])
    intent = event.get("intent") if isinstance(event.get("intent"), Mapping) else {}
    return {
        "event_type": event.get("event_type"),
        "observations": observations,
        "states": state_payloads,
        "actor_roles": actor_roles,
        "intent": {
            "intent_type": intent.get("intent_type"),
            "goal": intent.get("goal"),
            "target": intent.get("target"),
            "desired_state_change": intent.get("desired_state_change"),
            "inferred_intent": intent.get("inferred_intent"),
        },
    }


def activate_event(
    event: Mapping[str, Any],
    registry_index: RegistryIndex,
    *,
    min_score: float = 0.12,
    limit_per_type: int = 8,
    primary_threshold: float = 0.42,
    secondary_threshold: float = 0.22,
    object_types: set[str] | None = None,
) -> EngineResult:
    ensure_point_zero_locked(event)
    event_id = str(event.get("event_id", ""))
    if not event_id:
        raise RuntimeContractError("Activation requires event_id")
    query = _event_query(event)
    query_tokens = tokenize(query)
    if not query_tokens:
        return EngineResult(
            ENGINE_ID,
            "PARTIAL",
            {
                "event_id": event_id,
                "activation_refs": [],
                "residual": {"reason": "NO_SEARCHABLE_EVENT_FEATURES", "tokens": []},
            },
            [TraceStep.create(ENGINE_ID, "ACTIVATE_EXISTING_REGISTRY_OBJECTS", input_refs=[event_id], rule_refs=RULES, status="PARTIAL")],
            warnings=["Event contains no searchable features; no IDs were invented."],
        )

    allowed_types = object_types or ACTIVATABLE_TYPES
    all_hits = registry_index.search(query, object_types=allowed_types, min_score=min_score, limit=max(50, limit_per_type * len(allowed_types)))

    by_type: dict[str, list[Any]] = {}
    for hit in all_hits:
        by_type.setdefault(hit.object_type, []).append(hit)

    selected = []
    for object_type, hits in by_type.items():
        selected.extend(hits[:limit_per_type])
    selected.sort(key=lambda h: (-h.score, h.object_type, h.object_id))

    activation_refs: list[dict[str, Any]] = []
    matched_tokens: set[str] = set()
    for hit in selected:
        matched_tokens.update(hit.matched_tokens)
        if hit.score >= primary_threshold:
            tier = "PRIMARY"
        elif hit.score >= secondary_threshold:
            tier = "SECONDARY"
        else:
            tier = "CONTEXT_ONLY"
        activation_id = stable_id("ACT", event_id, hit.object_id, round(hit.score, 6), tier)
        activation_refs.append({
            "activation_id": activation_id,
            "object_id": hit.object_id,
            "object_type": hit.object_type,
            "activation_reason": "REGISTRY_FEATURE_OVERLAP",
            "matched_features": list(hit.matched_tokens),
            "activation_strength": round(hit.score, 6),
            "primary_or_secondary": tier,
            "source_distance": 1,
            "registry_source_file": hit.source_file,
            "registry_json_path": list(hit.json_path),
            "epistemic_status": "EXISTING_REGISTRY_ACTIVATION",
        })

    residual_tokens = sorted(query_tokens - matched_tokens)
    residual = {
        "residual_id": stable_id("RESID", event_id, residual_tokens),
        "event_id": event_id,
        "unmatched_tokens": residual_tokens,
        "coverage_token_count": len(matched_tokens),
        "query_token_count": len(query_tokens),
        "coverage_ratio": round(len(matched_tokens) / max(1, len(query_tokens)), 6),
        "new_primitive_status": "NOT_EVALUATED",
        "rule": "Residual does not imply a new primitive. Combination/relation reuse must be tested first.",
    }
    output_refs = [a["activation_id"] for a in activation_refs] + [residual["residual_id"]]
    trace = TraceStep.create(
        ENGINE_ID,
        "ACTIVATE_EXISTING_REGISTRY_OBJECTS",
        input_refs=[event_id],
        output_refs=output_refs,
        rule_refs=RULES,
        notes=[f"registry_objects={len(registry_index)}", f"activations={len(activation_refs)}", f"coverage={residual['coverage_ratio']:.3f}"],
    )
    payload = {
        "event_id": event_id,
        "activation_refs": activation_refs,
        "activation_count": len(activation_refs),
        "activation_counts_by_type": {
            object_type: sum(1 for a in activation_refs if a["object_type"] == object_type)
            for object_type in sorted({a["object_type"] for a in activation_refs})
        },
        "residual": residual,
    }
    status = "COMPLETE" if activation_refs else "PARTIAL"
    warnings = [] if activation_refs else ["No existing registry object crossed activation threshold; residual preserved without invented IDs."]
    return EngineResult(ENGINE_ID, status, payload, [trace], warnings=warnings)


def apply_activations_to_event(event: Mapping[str, Any], activation_result: EngineResult) -> dict[str, Any]:
    """Return a copied Event with additive activation refs; never mutate source input."""
    import json
    copied = json.loads(json.dumps(event, ensure_ascii=False))
    existing = {a.get("activation_id") for a in copied.get("activation_refs", []) if isinstance(a, Mapping)}
    for activation in activation_result.payload.get("activation_refs", []):
        if activation.get("activation_id") not in existing:
            copied.setdefault("activation_refs", []).append(activation)
    copied["last_updated_by"] = ENGINE_ID
    return copied
