#!/usr/bin/env python3
from pathlib import Path
import json, sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "generated/tests"
OUT.mkdir(parents=True, exist_ok=True)

errors = []

def load(rel):
    p = ROOT / rel
    if not p.exists():
        errors.append(f"missing:{rel}")
        return {}
    return json.loads(p.read_text(encoding="utf-8"))

fx = load("phase2/tests/P2_MULTI_RUBRIC_INTEGRATION_FIXTURE_001.json")
human = load("raw/human/HUMAN_CONTAINER_SOURCE_SLICE_MR_001.json")
ai = load("registries/ai/AI_RUBRIC_V0.json")
wis = load("phase2/wisdom/WISDOM_BATCH_001_DERIVATION.json")
asi = load("registries/asi/ASI_RUBRIC_V0.json")
nodes = load("registries/asi/asi_node_registry.json")
wiring = load("machine/wiring/MULTI_RUBRIC_WIRING_V0.json")

human_source = {r.get("container_id"): r.get("name") for r in human.get("records", [])}
ai_ids = {r.get("ai_segment_id") for r in ai.get("segments", [])}
wisdom_by_id = {r.get("wisdom_id"): r for r in wis.get("wisdom_candidates", [])}
asi_ids = {r.get("asi_segment_id") for r in asi.get("segments", [])}
node_ids = {r.get("asi_node_id") for r in nodes.get("nodes", [])}

# Pass 0 / source and scope locks.
if fx.get("fixture_is_source_fact") is not False:
    errors.append("fixture must remain synthetic and not source fact")
if fx.get("normal_rule") != "TEST_RULE_R1" or fx.get("candidate_action") != "TEST_ACTION_X":
    errors.append("test identities changed")
if set(wiring.get("domains", {})) != {"HUMAN", "AI", "WISDOM", "ASI"}:
    errors.append("multi-rubric wiring lost one or more domains")

# Pass 1 / reverse trace every domain input.
for cid, name in zip(fx.get("human_activation", {}).get("container_ids", []), fx.get("human_activation", {}).get("container_names", [])):
    if human_source.get(cid) != name:
        errors.append(f"Human source mismatch:{cid}:{name}")
for aid in fx.get("ai_activation", {}).get("ai_segment_ids", []):
    if aid not in ai_ids:
        errors.append(f"unknown AI segment:{aid}")
for wid in fx.get("wisdom_activation", {}).get("wisdom_candidate_ids", []):
    if wid not in wisdom_by_id:
        errors.append(f"unknown Wisdom candidate:{wid}")
for sid in fx.get("asi_activation", {}).get("asi_segment_ids", []):
    if sid not in asi_ids:
        errors.append(f"unknown ASI segment:{sid}")
for nid in fx.get("asi_activation", {}).get("asi_node_ids", []):
    if nid not in node_ids:
        errors.append(f"unknown ASI node:{nid}")

w2 = wisdom_by_id.get("WIS-CAND-002", {})
if "SOURCE_LINKED_CANDIDATE" not in set(w2.get("epistemic_status", [])):
    errors.append("WIS-CAND-002 lost candidate status")
if not w2.get("source_refs"):
    errors.append("WIS-CAND-002 has no source refs")
if fx.get("ai_activation", {}).get("forbidden_output") != "permission or final authority":
    errors.append("AI authority guard missing")
if fx.get("wisdom_activation", {}).get("forbidden_output") != "direct execution authority":
    errors.append("Wisdom authority guard missing")

# Pass 2 / deterministic forward execution for each variant.
def run_variant(v):
    events = [
        "MULTI_RUBRIC_ROUTER_ACTIVATED",
        "HUMAN_STATE_READ",
        "AI_ALTERNATIVES_AND_CONSEQUENCES_RETURNED",
        "WISDOM_CANDIDATE_RETRIEVED",
    ]
    normal_rule_after = fx["normal_rule"]
    action_fired = False
    if not v.get("wisdom_applicable"):
        events += ["WISDOM_APPLICABILITY_FALSE", "WISDOM_NOT_APPLIED", "OPEN_RULE_CHANGE_SEQUENCE"]
        result = "ROUTE_TO_RULE_CHANGE_SEQUENCE"
        barrier = "BLOCKED_FOR_CURRENT_ACTION"
    else:
        events.append("WISDOM_APPLICABILITY_TRUE")
        if not v.get("authority"):
            events += ["ASI_AUTHORITY_CHECK_FALSE", "BARRIER_BLOCKED"]
            result = "BLOCKED_NO_AUTHORITY"
            barrier = "BLOCKED"
        elif not v.get("alternatives_evaluated"):
            events += ["ASI_AUTHORITY_CHECK_TRUE", "EXCEPTION_CONTRACT_INCOMPLETE", "BARRIER_BLOCKED"]
            result = "BLOCKED_INCOMPLETE_EXCEPTION_CONTRACT"
            barrier = "BLOCKED"
        else:
            complete = all([
                v.get("trigger_true"),
                v.get("scope_bounded"),
                v.get("exact_action_matches", False),
                v.get("consequence_recorded", False),
                v.get("closure_condition_defined", False),
            ])
            if not complete:
                events += ["EXCEPTION_CONTRACT_INCOMPLETE", "BARRIER_BLOCKED"]
                result = "BLOCKED_INCOMPLETE_EXCEPTION_CONTRACT"
                barrier = "BLOCKED"
            else:
                events += [
                    "EXCEPTION_CONTRACT_COMPLETE",
                    "ASI_AUTHORITY_CHECK_TRUE",
                    "TRIGGER_OBSERVED",
                    "THRESHOLD_TRUE",
                    "BARRIER_CLEAR",
                    "BOUNDED_ACTION_EDGE_FIRED",
                    "NORMAL_RULE_PRESERVED",
                ]
                result = "BOUNDED_ACTION_PERMITTED"
                barrier = "CLEAR"
                action_fired = True
    return {
        "variant_id": v.get("variant_id"),
        "expected_result": v.get("expected_result"),
        "actual_result": result,
        "status": "PASS" if result == v.get("expected_result") else "FAIL",
        "action_fired": action_fired,
        "barrier_state": barrier,
        "normal_rule_after": normal_rule_after,
        "events": events,
    }

variant_results = [run_variant(v) for v in fx.get("variants", [])]
for r in variant_results:
    if r["status"] != "PASS":
        errors.append(f"variant failed:{r['variant_id']}:{r['actual_result']} != {r['expected_result']}")
    if r["normal_rule_after"] != fx.get("normal_rule"):
        errors.append(f"normal rule replaced:{r['variant_id']}")

permitted = next((r for r in variant_results if r["variant_id"] == "MR-BOUNDED-EXCEPTION-GRANTED"), {})
if not permitted.get("action_fired"):
    errors.append("bounded granted variant did not fire")
for rid in ["MR-NO-AUTHORITY", "MR-ALTERNATIVES-OPEN", "MR-WISDOM-NOT-APPLICABLE"]:
    r = next((x for x in variant_results if x["variant_id"] == rid), {})
    if r.get("action_fired"):
        errors.append(f"blocked/routed variant fired action:{rid}")

# Pass 3 / ownership and closure audit.
invariants = {
    "HUMAN_STATE_REMAINS_HUMAN_OWNED": fx.get("human_activation", {}).get("ownership_rule", "").startswith("Human state remains Human-owned"),
    "AI_HAS_NO_PERMISSION_AUTHORITY": fx.get("ai_activation", {}).get("forbidden_output") == "permission or final authority",
    "WISDOM_HAS_NO_PERMISSION_AUTHORITY": fx.get("wisdom_activation", {}).get("forbidden_output") == "direct execution authority",
    "WISDOM_APPLICABILITY_IS_CHECKED": all("WISDOM_CANDIDATE_RETRIEVED" in r["events"] for r in variant_results),
    "ASI_GOVERNS_AUTHORITY": all("ASI_AUTHORITY_CHECK_TRUE" in r["events"] or "ASI_AUTHORITY_CHECK_FALSE" in r["events"] or r["variant_id"] == "MR-WISDOM-NOT-APPLICABLE" for r in variant_results),
    "NORMAL_RULE_SURVIVES_EXCEPTION": all(r["normal_rule_after"] == fx.get("normal_rule") for r in variant_results),
    "THRESHOLD_AND_BARRIER_REQUIRED_FOR_ACTION": "THRESHOLD_TRUE" in permitted.get("events", []) and "BARRIER_CLEAR" in permitted.get("events", []),
    "NON_APPLICABLE_WISDOM_ROUTES_NOT_FORCES": "WISDOM_NOT_APPLIED" in next(r for r in variant_results if r["variant_id"] == "MR-WISDOM-NOT-APPLICABLE")["events"],
}
for name, ok in invariants.items():
    if not ok:
        errors.append(f"invariant failed:{name}")

report = {
    "report_id": "P2-MULTI-RUBRIC-INTEGRATION-RFR-001",
    "status": "FAIL" if errors else "PASS",
    "scope_note": "Synthetic control-law integration test using source-backed Human container identities and a source-linked Wisdom Candidate. PASS proves routing/ownership/governance behavior in this fixture, not real-world moral correctness or scripture validation.",
    "domains": ["HUMAN", "AI", "WISDOM", "ASI"],
    "pass0": {
        "declared_end": fx.get("declared_end"),
        "scope": fx.get("scope"),
        "fixture_is_source_fact": fx.get("fixture_is_source_fact")
    },
    "pass1": {
        "human_source_bound": len(human_source) == 4,
        "ai_segments_source_bound": not any(e.startswith("unknown AI") for e in errors),
        "wisdom_source_bound": bool(w2.get("source_refs")),
        "asi_segments_and_nodes_source_bound": not any(e.startswith("unknown ASI") for e in errors)
    },
    "pass2": {
        "runtime_route": fx.get("runtime_route", []),
        "variants": variant_results
    },
    "pass3": {
        "invariant_checks": invariants,
        "wisdom_epistemic_status": w2.get("epistemic_status", []),
        "wisdom_law_status": "NOT_PROMOTED",
        "normal_rule_final": fx.get("normal_rule")
    },
    "errors": errors
}

(OUT / "P2_MULTI_RUBRIC_INTEGRATION_RFR_001.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print(report["status"], "variants", len(variant_results), "errors", len(errors))
sys.exit(1 if errors else 0)
