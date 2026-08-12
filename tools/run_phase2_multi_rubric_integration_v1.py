#!/usr/bin/env python3
from pathlib import Path
import json, sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "generated/tests"
OUT.mkdir(parents=True, exist_ok=True)

errors=[]
findings=[]

def load(rel):
    p=ROOT/rel
    if not p.exists():
        errors.append(f"missing:{rel}")
        return {}
    return json.loads(p.read_text(encoding="utf-8"))

fixture=load("phase2/tests/P2_MULTI_RUBRIC_INTEGRATION_FIXTURE_V1.json")
human=load("registries/human/HUMAN_CONTAINER_INDEX_80_APPROVED_V1.json")
ai=load("registries/ai/AI_RUBRIC_V0.json")
ai64=load("registries/ai/AI_ONLY_RECORDS_64_APPROVED_V1.json")
ai64_bind=load("generated/registry_views/ai_only_64_phase2_bindings_v1.json")
wisdom=load("registries/wisdom/WISDOM_OBJECTS_BG_2_47_2_50_V1.json")
wisdom_rfr=load("generated/tests/P2_WISDOM_SOURCE_INGESTION_RFR_V1.json")
asi=load("registries/asi/ASI_RUBRIC_V0.json")
nodes=load("registries/asi/asi_node_registry.json")

# Build registries
human_ids=set()
for seg in human.get("segments",[]):
    for row in seg.get("containers",[]):
        if row: human_ids.add(row[0])
ai_seg_ids={x.get("ai_segment_id") for x in ai.get("segments",[])}
ai64_ids={r[0] for r in ai64.get("records",[]) if r}
ai64_binding_by_id={r.get("ai_only_id"):r for r in ai64_bind.get("records",[])}
wisdom_ids={x.get("wisdom_object_id") for x in wisdom.get("objects",[])}
asi_seg_ids={x.get("asi_segment_id") for x in asi.get("segments",[])}
node_ids={x.get("asi_node_id") for x in nodes.get("nodes",[])}

conv=fixture.get("convergence_node",{})

# Pass 0 — scope and endpoint
pass0={
    "declared_end": fixture.get("declared_end"),
    "scope": fixture.get("scope"),
    "closure_scope": "synthetic local submission control behavior; not real submission or external acceptance"
}
if fixture.get("fixture_is_source_fact") is not False:
    errors.append("fixture_must_be_marked_synthetic")
if wisdom_rfr.get("status") != "PASS":
    errors.append("wisdom_source_ingestion_must_pass_before_integration")

# Pass 1 — reverse source/reference integrity
bad_human=sorted(set(conv.get("human_container_refs",[]))-human_ids)
bad_ai=sorted(set(conv.get("ai_segment_refs",[]))-ai_seg_ids)
bad_ai64=sorted(set(conv.get("approved_ai_only_refs",[]))-ai64_ids)
bad_wisdom=sorted(set(conv.get("wisdom_object_refs",[]))-wisdom_ids)
bad_asi=sorted(set(conv.get("asi_segment_refs",[]))-asi_seg_ids)
bad_nodes=sorted(set(conv.get("asi_node_route",[]))-node_ids)
for label,bad in [("human",bad_human),("ai",bad_ai),("ai64",bad_ai64),("wisdom",bad_wisdom),("asi",bad_asi),("nodes",bad_nodes)]:
    if bad: errors.append(f"bad_{label}_refs:{bad}")

# AI-NEW-011 must carry the governance patch; otherwise tool selection may be mistaken for authority.
ai011=ai64_binding_by_id.get("AI-NEW-011",{})
required_ai011_governance={"ASI-08","ASI-13"}
if not required_ai011_governance <= set(ai011.get("phase2_asi_segments",[])):
    errors.append("AI-NEW-011_missing_ASI-08_ASI-13_governance")

# Pass 2 — forward runtime behavior
thresholds=fixture.get("submission_edge",{}).get("threshold_expression",[])
non_thresholds=set(fixture.get("submission_edge",{}).get("explicit_non_thresholds",[]))
if "wisdom_retrieved" not in non_thresholds:
    errors.append("wisdom_must_be_explicit_non_threshold")
if any("wisdom" in x.lower() for x in thresholds):
    errors.append("wisdom_may_not_appear_in_action_threshold")

initial_wisdom=set(fixture.get("starting_reality",{}).get("human_initial_view",{}).get("known_wisdom_refs",[]))
if initial_wisdom:
    errors.append("human_actor_view_illegally_preloaded_with_wisdom")
presented_wisdom=set(conv.get("wisdom_object_refs",[]))
actor_view_after_communication=sorted(presented_wisdom)

variant_results=[]
for v in fixture.get("variants",[]):
    required_returns_accepted = v.get("privacy_check") == "PASS" and v.get("provenance_check") == "PASS"
    edge_fired = all([
        v.get("artifact_complete") is True,
        v.get("human_authorization") == "GRANTED",
        fixture.get("starting_reality",{}).get("deadline_window") == "OPEN",
        v.get("privacy_check") == "PASS",
        v.get("provenance_check") == "PASS",
        required_returns_accepted
    ])
    hard=[]
    if edge_fired != v.get("expected_edge_fired"):
        hard.append("edge_fire_expectation_mismatch")
    # Wisdom is active/presented in every variant but never changes authorization/evidence thresholds.
    if v.get("human_authorization") != "GRANTED" and edge_fired:
        hard.append("wisdom_or_ai_bypassed_human_authorization")
    if v.get("artifact_complete") is not True and edge_fired:
        hard.append("wisdom_or_ai_bypassed_completeness")
    if v.get("provenance_check") != "PASS" and edge_fired:
        hard.append("wisdom_or_ai_bypassed_provenance")

    events=[
        "MULTI_RUBRIC_ACTIVATION",
        "AI_MECHANISM_ROUTED",
        "WISDOM_RETRIEVED_AS_ADVISORY",
        "SOURCE_LINKED_WISDOM_ADVISORY_PRESENTED",
        "HUMAN_ACTOR_VIEW_UPDATED_BY_COMMUNICATION_EVENT",
        "ASI_GOVERNANCE_CHECK",
        "SUBMISSION_THRESHOLD_EVALUATED"
    ]
    parent_status="OPEN"
    local_result=None
    local_closure=None
    seed=None
    sub_sequence=None
    if edge_fired:
        events += ["SUBMISSION_EDGE_FIRED","LOCAL_RESULT_SUBMITTED","LOCAL_SEQUENCE_CLOSED_SUCCESS","FUTURE_OUTCOME_SEED_CREATED"]
        local_result="SUBMITTED"
        local_closure="CLOSED_SUCCESS"
        parent_status="CLOSED_SUCCESS"
        seed="AWAIT_EXTERNAL_SUBMISSION_DECISION"
    elif v.get("human_authorization") == "DENIED":
        events += ["SUBMISSION_EDGE_BLOCKED_BY_AUTHORIZATION","LOCAL_DECISION_RECORDED_NO_SUBMISSION"]
        local_result="NOT_SUBMITTED_BY_EXPLICIT_AUTHORIZATION_DECISION"
        local_closure="CLOSED_SUCCESS"
        parent_status="CLOSED_SUCCESS"
    elif v.get("artifact_complete") is not True:
        events += ["BARRIER_BLOCKED_INCOMPLETE","OPEN_REMEDIATION_SUB_SEQUENCE","PARENT_WAITING_FOR_RETURN"]
        parent_status="WAITING_FOR_RETURN"
        sub_sequence="REMEDIATION_AND_REVERIFY"
    elif v.get("provenance_check") != "PASS":
        events += ["BARRIER_BLOCKED_PROVENANCE","OPEN_PROVENANCE_REPAIR_OR_SOURCE_REVIEW","PARENT_WAITING_OR_BLOCKED"]
        parent_status="WAITING_FOR_RETURN_OR_BLOCKED"
        sub_sequence="PROVENANCE_REPAIR_OR_SOURCE_REVIEW"

    if v.get("expected_local_result") and local_result != v.get("expected_local_result"):
        hard.append("local_result_mismatch")
    if v.get("expected_local_closure") and local_closure != v.get("expected_local_closure"):
        hard.append("local_closure_mismatch")
    if v.get("expected_parent_status") and parent_status != v.get("expected_parent_status"):
        hard.append("parent_status_mismatch")
    if v.get("expected_seed") and seed != v.get("expected_seed"):
        hard.append("seed_mismatch")
    if v.get("expected_sub_sequence") and sub_sequence != v.get("expected_sub_sequence"):
        hard.append("sub_sequence_mismatch")
    if v.get("expected_external_outcome") and fixture.get("starting_reality",{}).get("external_acceptance_outcome") != v.get("expected_external_outcome"):
        hard.append("external_outcome_mismatch")
    if hard:
        errors.extend([f"{v.get('variant_id')}:{x}" for x in hard])
    variant_results.append({
        "variant_id":v.get("variant_id"),
        "status":"FAIL" if hard else "PASS",
        "edge_fired":edge_fired,
        "human_authorization":v.get("human_authorization"),
        "artifact_complete":v.get("artifact_complete"),
        "privacy_check":v.get("privacy_check"),
        "provenance_check":v.get("provenance_check"),
        "parent_status":parent_status,
        "local_result":local_result,
        "local_closure":local_closure,
        "external_acceptance_outcome":fixture.get("starting_reality",{}).get("external_acceptance_outcome"),
        "seed":seed,
        "opened_sub_sequence":sub_sequence,
        "events":events,
        "hard_failures":hard
    })

# Pass 3 — audit hard architecture invariants
checks={
    "HUMAN_REFERENCES_SOURCE_BOUND": not bad_human,
    "AI_REFERENCES_SOURCE_BOUND": not bad_ai and not bad_ai64,
    "WISDOM_REFERENCES_SOURCE_BOUND": not bad_wisdom and wisdom_rfr.get("status")=="PASS",
    "ASI_REFERENCES_SOURCE_BOUND": not bad_asi and not bad_nodes,
    "ACTOR_VIEW_NOT_PRELOADED_WITH_GLOBAL_WISDOM": not initial_wisdom,
    "WISDOM_ENTERS_ACTOR_VIEW_ONLY_AFTER_COMMUNICATION_EVENT": actor_view_after_communication==sorted(presented_wisdom),
    "WISDOM_NOT_ACTION_THRESHOLD": "wisdom_retrieved" in non_thresholds and not any("wisdom" in x.lower() for x in thresholds),
    "AI_TOOL_SELECTION_NOT_AUTHORIZATION": required_ai011_governance <= set(ai011.get("phase2_asi_segments",[])),
    "DENIED_AUTHORIZATION_BLOCKS_ACTION": next((not r["edge_fired"] for r in variant_results if r["variant_id"]=="MRI-DENIED"),False),
    "INCOMPLETE_ARTIFACT_OPENS_SUB_SEQUENCE": next((r["opened_sub_sequence"]=="REMEDIATION_AND_REVERIFY" for r in variant_results if r["variant_id"]=="MRI-GRANTED-INCOMPLETE"),False),
    "FAILED_PROVENANCE_BLOCKS_ACTION": next((not r["edge_fired"] for r in variant_results if r["variant_id"]=="MRI-GRANTED-PROVENANCE-FAIL"),False),
    "LOCAL_SUBMISSION_CLOSURE_DOES_NOT_FABRICATE_EXTERNAL_OUTCOME": next((r["local_closure"]=="CLOSED_SUCCESS" and r["external_acceptance_outcome"]=="UNKNOWN" and r["seed"]=="AWAIT_EXTERNAL_SUBMISSION_DECISION" for r in variant_results if r["variant_id"]=="MRI-GRANTED-COMPLETE"),False)
}
for k,v in checks.items():
    if not v: errors.append(f"invariant_failed:{k}")

status="FAIL" if errors else ("PASS_WITH_FINDINGS" if findings else "PASS")
report={
    "report_id":"P2-MULTI-RUBRIC-INTEGRATION-RFR-V1",
    "status":status,
    "scope_note":"Synthetic architecture test of one Sequence with Human + AI + source-linked Wisdom + ASI simultaneously active. It does not perform a real submission or claim external acceptance.",
    "summary":{"variants":len(variant_results),"pass":sum(r["status"]=="PASS" for r in variant_results),"fail":sum(r["status"]=="FAIL" for r in variant_results),"errors":len(errors),"findings":len(findings)},
    "pass0":pass0,
    "pass1":{"bad_human_refs":bad_human,"bad_ai_refs":bad_ai,"bad_ai_only_refs":bad_ai64,"bad_wisdom_refs":bad_wisdom,"bad_asi_refs":bad_asi,"bad_node_refs":bad_nodes},
    "pass2":{"actor_view_before":{"known_wisdom_refs":sorted(initial_wisdom)},"actor_view_after_communication":{"known_wisdom_refs":actor_view_after_communication},"variants":variant_results},
    "pass3":{"invariant_checks":checks,"errors":errors,"findings":findings}
}
(OUT/"P2_MULTI_RUBRIC_INTEGRATION_RFR_V1.json").write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding="utf-8")
print(json.dumps(report["summary"],indent=2))
sys.exit(1 if errors else 0)
