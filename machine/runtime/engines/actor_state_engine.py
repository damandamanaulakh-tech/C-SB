#!/usr/bin/env python3
"""Parallel actor-state hypothesis engine.

One actor can occupy many plausible states at the same historical Event.  This
engine creates bounded state hypotheses without splitting identity.  Human
container activations are treated as evidence/context for a state dimension,
not proof that a specific internal state existed.
"""
from __future__ import annotations

from typing import Any, Iterable, Mapping, Sequence

from .runtime_core import EngineResult, RuntimeContractError, TraceStep, stable_id

ENGINE_ID = "SB-RT-ENG-ACTOR-STATE-001"
RULES = [
    "SAME_ACTOR_MAY_HAVE_MULTIPLE_BRAIN_STATES",
    "ACTOR_STATE_HYPOTHESIS_NE_HISTORICAL_FACT",
    "HUMAN_PARAMETER_ACTIVATION_NE_STATE_PROOF",
    "ACTOR_IDENTITY_MUST_NOT_SPLIT_WITH_STATE",
]

# Source-supported Human containers most useful for actor-state reconstruction.
CONTAINER_DIMENSIONS: dict[str, tuple[str, ...]] = {
    "CON-057": ("AFFECTIVE_STATE", "AROUSAL_VALENCE"),
    "CON-058": ("EMOTION_RECOGNITION",),
    "CON-059": ("EMOTION_REGULATION", "COPING"),
    "CON-060": ("REWARD_APPROACH",),
    "CON-061": ("THREAT_LOSS", "VIGILANCE", "AVOIDANCE"),
    "CON-062": ("MOTIVATION", "EFFORT", "PERSISTENCE"),
    "CON-063": ("INTENT_COMMITMENT",),
    "CON-064": ("MOTIVE_PRIORITY", "NEED_VALUE_CONFLICT"),
    "CON-065": ("CONSCIOUS_ACCESS",),
    "CON-066": ("IDENTITY_SELF_MODEL",),
    "CON-067": ("TEMPERAMENT_TRAIT_TENDENCY",),
    "CON-068": ("AGENCY_OWNERSHIP",),
    "CON-069": ("SOCIAL_PREDICTION", "THEORY_OF_MIND"),
    "CON-071": ("BELONGING_STATUS_GROUP",),
    "CON-072": ("MORAL_NORM_MEANING",),
    "CON-075": ("METACOGNITION", "SELF_MONITORING"),
    "CON-076": ("BIAS_HEURISTIC_PRESSURE",),
    "CON-077": ("RESILIENCE_REPAIR",),
}


def _activation_dimensions(activation_refs: Iterable[Mapping[str, Any]]) -> list[dict[str, Any]]:
    dimensions: list[dict[str, Any]] = []
    for activation in activation_refs:
        object_id = str(activation.get("object_id", ""))
        mapped = CONTAINER_DIMENSIONS.get(object_id)
        if not mapped:
            continue
        for dimension in mapped:
            dimensions.append({
                "dimension": dimension,
                "source_object_id": object_id,
                "activation_id": activation.get("activation_id"),
                "activation_strength": activation.get("activation_strength"),
                "value": "ACTIVE_CONTEXT",
                "epistemic_status": "INFERRED_CONTEXT",
            })
    return dimensions


def _normalize_explicit_state(state: Mapping[str, Any]) -> dict[str, Any]:
    if not state.get("dimension"):
        raise RuntimeContractError("Explicit actor-state dimension requires 'dimension'")
    return {
        "dimension": str(state["dimension"]),
        "value": state.get("value"),
        "source_object_id": state.get("source_object_id"),
        "supporting_evidence_refs": sorted(set(state.get("supporting_evidence_refs", []))),
        "contradicting_evidence_refs": sorted(set(state.get("contradicting_evidence_refs", []))),
        "epistemic_status": str(state.get("epistemic_status", "INFERRED")),
        "confidence": state.get("confidence"),
    }


def build_actor_state_hypotheses(
    event: Mapping[str, Any],
    actor_role_assignments: Sequence[Mapping[str, Any]],
    *,
    explicit_state_dimensions: Mapping[str, Sequence[Mapping[str, Any]]] | None = None,
    scenario_variants: Mapping[str, Sequence[Mapping[str, Any]]] | None = None,
    max_variants_per_actor: int = 12,
) -> EngineResult:
    event_id = str(event.get("event_id", ""))
    if not event_id:
        raise RuntimeContractError("Actor-state engine requires event_id")
    explicit_state_dimensions = explicit_state_dimensions or {}
    scenario_variants = scenario_variants or {}

    actors = sorted({str(a.get("actor_ref")) for a in actor_role_assignments if a.get("actor_ref")})
    activation_dimensions = _activation_dimensions(event.get("activation_refs", []))
    states: list[dict[str, Any]] = []
    warnings: list[str] = []

    for actor_ref in actors:
        roles = sorted({str(a.get("role")) for a in actor_role_assignments if str(a.get("actor_ref")) == actor_ref})
        base_dimensions = list(activation_dimensions)
        for item in explicit_state_dimensions.get(actor_ref, ()):
            base_dimensions.append(_normalize_explicit_state(item))

        # Base actor-state hypothesis. It may be sparse; sparse/UNKNOWN is legal.
        base_id = stable_id("ASTATE", event_id, actor_ref, "BASE", base_dimensions, roles)
        states.append({
            "actor_state_id": base_id,
            "event_id": event_id,
            "actor_ref": actor_ref,
            "identity_ref": actor_ref,
            "roles": roles,
            "variant_label": "BASE_AVAILABLE_STATE",
            "dimensions": base_dimensions,
            "current_state_summary": None if not base_dimensions else "State dimensions activated from current Event context; values remain bounded by evidence.",
            "supporting_evidence_refs": sorted({e for d in base_dimensions for e in d.get("supporting_evidence_refs", [])}),
            "contradicting_evidence_refs": sorted({e for d in base_dimensions for e in d.get("contradicting_evidence_refs", [])}),
            "epistemic_status": "INFERRED" if base_dimensions else "UNKNOWN",
            "maturity": "M1" if any(d.get("epistemic_status") in {"OBSERVED", "SOURCE_STATED"} for d in base_dimensions) else "M0",
            "proof_debt": [] if base_dimensions else ["ACTOR_STATE_NOT_ESTABLISHED"],
            "same_identity_across_variants": True,
        })

        # Caller-provided scenario variants are explicit search-space branches,
        # e.g. same king under secure-legitimacy vs threatened-legitimacy state.
        variants = list(scenario_variants.get(actor_ref, ()))[:max_variants_per_actor]
        for idx, variant in enumerate(variants, start=1):
            dimensions = list(base_dimensions)
            for dimension in variant.get("dimensions", []):
                dimensions.append(_normalize_explicit_state(dimension))
            variant_label = str(variant.get("label") or f"VARIANT_{idx:02d}")
            state_id = stable_id("ASTATE", event_id, actor_ref, variant_label, dimensions)
            states.append({
                "actor_state_id": state_id,
                "event_id": event_id,
                "actor_ref": actor_ref,
                "identity_ref": actor_ref,
                "roles": roles,
                "variant_label": variant_label,
                "dimensions": dimensions,
                "current_state_summary": variant.get("summary"),
                "supporting_evidence_refs": sorted(set(variant.get("supporting_evidence_refs", []))),
                "contradicting_evidence_refs": sorted(set(variant.get("contradicting_evidence_refs", []))),
                "epistemic_status": str(variant.get("epistemic_status", "NEW_SYNTHETIC")),
                "maturity": str(variant.get("maturity", "M0")),
                "proof_debt": list(variant.get("proof_debt", ["SCENARIO_STATE_REQUIRES_EVIDENCE"])),
                "same_identity_across_variants": True,
            })

    if not actors:
        warnings.append("No actor roles available; actor-state generation deferred rather than inventing actor identity.")

    trace = TraceStep.create(
        ENGINE_ID,
        "BUILD_PARALLEL_ACTOR_STATE_HYPOTHESES",
        input_refs=[event_id] + actors,
        output_refs=[s["actor_state_id"] for s in states],
        rule_refs=RULES,
        notes=[f"actors={len(actors)}", f"state_variants={len(states)}"],
    )
    return EngineResult(
        ENGINE_ID,
        "COMPLETE" if states else "PARTIAL",
        {
            "event_id": event_id,
            "actor_state_hypotheses": states,
            "actor_count": len(actors),
            "state_variant_count": len(states),
            "identity_splits_created": 0,
        },
        [trace],
        warnings=warnings,
    )
