#!/usr/bin/env python3
"""Typed relation-graph construction for Sourceborn Batch-3.

The engine distinguishes ACTIVE structural links from CANDIDATE semantic links.
It never turns similarity into identity or temporal order into causality.
"""
from __future__ import annotations

from typing import Any, Iterable, Mapping

from .runtime_core import EngineResult, RuntimeContractError, TraceStep, ensure_point_zero_locked, stable_id

ENGINE_ID = "SB-RT-ENG-RELATION-GRAPH-001"
RULES = [
    "LINK_NE_MERGE",
    "SIMILAR_NE_SAME",
    "TEMPORAL_NE_CAUSAL",
    "CANDIDATE_LINKS_REQUIRE_RECHECK",
    "SOURCE_LINEAGE_MUST_BE_PRESERVED",
]

IDENTITY_RELATIONS = {"SAME_AS"}
CAUSAL_RELATIONS = {"PRODUCED_BY", "RESULT_OF"}


def _relation(
    source_ref: str,
    relation_type: str,
    target_ref: str,
    *,
    category: str,
    status: str,
    epistemic_status: str,
    evidence_refs: Iterable[str] = (),
    source_independence_groups: Iterable[str] = (),
    order_type: str | None = None,
    extended_relation_type: str | None = None,
    rule_refs: Iterable[str] = (),
    notes: Iterable[str] = (),
) -> dict[str, Any]:
    if not source_ref or not target_ref:
        raise RuntimeContractError("Relation endpoints must be non-empty")
    if relation_type in IDENTITY_RELATIONS and status == "ACTIVE" and not list(evidence_refs):
        raise RuntimeContractError("SAME_AS cannot become ACTIVE without identity evidence")
    if relation_type in CAUSAL_RELATIONS and status == "ACTIVE" and not list(evidence_refs):
        raise RuntimeContractError(f"{relation_type} cannot become ACTIVE without evidence")
    relation_id = stable_id("REL", source_ref, relation_type, target_ref, status, sorted(evidence_refs))
    return {
        "relation_id": relation_id,
        "source_ref": source_ref,
        "relation_type": relation_type,
        "extended_relation_type": extended_relation_type,
        "target_ref": target_ref,
        "category": category,
        "status": status,
        "epistemic_status": epistemic_status,
        "order_type": order_type,
        "supporting_evidence_refs": sorted(set(evidence_refs)),
        "source_independence_group_refs": sorted(set(source_independence_groups)),
        "rule_refs": sorted(set(rule_refs)),
        "notes": list(notes),
        "auto_merge": False,
    }


def build_event_relation_graph(event: Mapping[str, Any]) -> EngineResult:
    ensure_point_zero_locked(event)
    event_id = str(event.get("event_id", ""))
    if not event_id:
        raise RuntimeContractError("Relation graph requires event_id")
    relations: list[dict[str, Any]] = []
    pz = event.get("point_zero", {})
    point_zero_id = str(pz.get("point_zero_id"))

    # Source → Event provenance.
    for source in event.get("source_refs", []):
        if isinstance(source, Mapping) and source.get("source_id"):
            relations.append(_relation(
                str(source["source_id"]), "SOURCE_OF", event_id,
                category="PROVENANCE", status="ACTIVE", epistemic_status="DIRECT_SOURCE_LINK",
                rule_refs=RULES,
            ))

    # Point Zero → Event bounded-origin link. Encoded as extended relation so the
    # stable MemoryLink enum need not grow for every graph-specific relation.
    relations.append(_relation(
        point_zero_id, "OTHER", event_id,
        extended_relation_type="POINT_ZERO_OF",
        category="PROVENANCE", status="ACTIVE", epistemic_status="STRUCTURAL_RUNTIME_LINK",
        rule_refs=RULES,
    ))

    # Existing activation IDs are structural links, not claims that the object
    # caused the Event.
    for activation in event.get("activation_refs", []):
        if not isinstance(activation, Mapping):
            continue
        object_id = activation.get("object_id")
        activation_id = activation.get("activation_id")
        if not object_id:
            continue
        relations.append(_relation(
            event_id, "OTHER", str(object_id),
            extended_relation_type="ACTIVATES",
            category="RUNTIME", status="ACTIVE", epistemic_status="RUNTIME_ACTIVATION",
            evidence_refs=[str(activation_id)] if activation_id else [],
            rule_refs=RULES,
        ))

    # Actor-role assignments remain role-specific. A SUBJECT edge never implies
    # CONTROLLER, REQUESTER, AUTHOR or PERFORMER.
    actor_relation_map = {
        "SUBJECT": "ACTOR_OF",
        "REQUESTER": "REQUESTED_BY",
        "CONTROLLER": "CONTROLLED_BY",
        "AUTHOR": "AUTHORED_BY",
        "DESIGNER": "DESIGNED_BY",
        "PERFORMER": "PERFORMED_BY",
        "CARRIER": "CARRIED_BY",
        "BENEFICIARY": "BENEFITS",
        "AUDIENCE": "AUDIENCE_OF",
        "OBSERVER": "OBSERVED_BY",
        "WRITER": "WRITTEN_BY",
    }
    for assignment in event.get("actor_roles", []):
        if not isinstance(assignment, Mapping):
            continue
        actor_ref = assignment.get("actor_ref")
        role = str(assignment.get("role", "UNKNOWN"))
        if not actor_ref or role == "UNKNOWN":
            continue
        extended = actor_relation_map.get(role, f"ACTOR_ROLE_{role}")
        status = "ACTIVE" if assignment.get("epistemic_status") in {"OBSERVED", "SOURCE_STATED"} else "CANDIDATE"
        relations.append(_relation(
            event_id, "OTHER", str(actor_ref),
            extended_relation_type=extended,
            category="ACTOR_ROLE", status=status,
            epistemic_status=str(assignment.get("epistemic_status", "UNKNOWN")),
            evidence_refs=assignment.get("supporting_evidence_refs", []),
            rule_refs=RULES,
            notes=[f"role={role}"],
        ))

    # State links preserve state role and do not imply causal direction.
    for state in event.get("state_refs", []):
        if not isinstance(state, Mapping) or not state.get("state_id"):
            continue
        role = str(state.get("state_role", "CURRENT_STATE"))
        relations.append(_relation(
            event_id, "OTHER", str(state["state_id"]),
            extended_relation_type=role,
            category="STATE", status="ACTIVE",
            epistemic_status=str(state.get("epistemic_status", "STRUCTURAL_RUNTIME_LINK")),
            rule_refs=RULES,
        ))

    # Intent is always linked, including UNKNOWN intent, because Event→Intent is
    # a mandatory field of investigation.
    intent = event.get("intent")
    if isinstance(intent, Mapping) and intent.get("intent_id"):
        status = "ACTIVE" if intent.get("intent_type") in {"UNKNOWN", "NOT_YET_DECODED"} else "CANDIDATE"
        relations.append(_relation(
            event_id, "OTHER", str(intent["intent_id"]),
            extended_relation_type="HAS_INTENT_FIELD",
            category="INTENT", status=status,
            epistemic_status=str(intent.get("epistemic_status", "UNKNOWN")),
            evidence_refs=intent.get("supporting_evidence_refs", []),
            rule_refs=RULES,
        ))

    # Deduplicate structurally identical relations.
    deduped: dict[str, dict[str, Any]] = {r["relation_id"]: r for r in relations}
    final_relations = list(deduped.values())
    final_relations.sort(key=lambda r: (r["category"], r["source_ref"], r.get("extended_relation_type") or r["relation_type"], r["target_ref"]))

    trace = TraceStep.create(
        ENGINE_ID,
        "BUILD_EVENT_RELATION_GRAPH",
        input_refs=[event_id],
        output_refs=[r["relation_id"] for r in final_relations],
        rule_refs=RULES,
        notes=[f"relation_count={len(final_relations)}"],
    )
    return EngineResult(
        ENGINE_ID,
        "COMPLETE",
        {
            "event_id": event_id,
            "relations": final_relations,
            "active_count": sum(1 for r in final_relations if r["status"] == "ACTIVE"),
            "candidate_count": sum(1 for r in final_relations if r["status"] == "CANDIDATE"),
            "identity_merges": 0,
        },
        [trace],
    )


def propose_relation(
    source_ref: str,
    target_ref: str,
    relation_type: str,
    *,
    evidence_refs: Iterable[str] = (),
    source_independence_groups: Iterable[str] = (),
    epistemic_status: str = "DERIVED_HYPOTHESIS",
    category: str = "DERIVED",
    order_type: str | None = None,
    activate_if_evidenced: bool = False,
) -> dict[str, Any]:
    """Create a bounded derived relation with identity/causality guards."""
    evidence = list(evidence_refs)
    status = "ACTIVE" if activate_if_evidenced and evidence else "CANDIDATE"
    base_type = relation_type
    extended = None
    stable_enum = {
        "SOURCE_OF", "MEMORY_OF", "DERIVED_FROM", "SUPPORTS", "CONTRADICTS", "SIMILAR_TO",
        "SPECIALIZES", "GENERALIZES", "INSTANCE_OF", "COUNTEREXAMPLE_TO", "PRECEDES", "FOLLOWS",
        "DEPENDS_ON", "PRODUCED_BY", "RESULT_OF", "FUTURE_OF", "REPAIRED_BY", "RETESTED_BY",
        "SUPERSEDES", "COMPRESSED_FROM", "INDEXES", "OTHER",
    }
    if relation_type not in stable_enum:
        base_type, extended = "OTHER", relation_type
    return _relation(
        source_ref, base_type, target_ref,
        extended_relation_type=extended,
        category=category,
        status=status,
        epistemic_status=epistemic_status,
        evidence_refs=evidence,
        source_independence_groups=source_independence_groups,
        order_type=order_type,
        rule_refs=RULES,
    )
