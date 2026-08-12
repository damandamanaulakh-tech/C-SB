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

fx = load("phase2/tests/P2_CLOSURE_SCOPE_INHERITANCE_FIXTURE_001.json")
vocab = load("machine/vocab/core_vocab.json")

if fx.get("fixture_is_source_fact") is not False:
    errors.append("fixture must remain synthetic")

terminal = set(vocab.get("terminal_sequence_statuses", []))
if "CLOSED_SUCCESS" not in terminal:
    errors.append("CLOSED_SUCCESS missing from terminal vocabulary")

hierarchy = fx.get("scope_hierarchy", [])
ids = [r.get("sequence_id") for r in hierarchy]
if ids != ["S-PROJECT-001", "S-PROMISE-001", "S-ACTION-001"]:
    errors.append("scope hierarchy changed")
if len(set(ids)) != 3:
    errors.append("scope sequence IDs must be unique")

results = []
for v in fx.get("variants", []):
    events = []
    action = "OPEN"
    promise = "OPEN"
    project = "OPEN"

    if v.get("action_terminal"):
        action = "CLOSED_SUCCESS"
        events.append("ACTION_SCOPE_CLOSED_SUCCESS")
        events.append("ACTION_RETURN_PACKET_CREATED")

    if action == "CLOSED_SUCCESS":
        if not v.get("action_return_accepted"):
            promise = "WAITING_FOR_RETURN"
            events += ["ACTION_RETURN_UNACCEPTED", "PROMISE_SCOPE_BLOCKED"]
        else:
            events += ["ACTION_RETURN_ACCEPTED", "PROMISE_CONTRACT_REEVALUATED"]
            if v.get("promise_confirmation"):
                promise = "CLOSED_SUCCESS"
                events += ["PROMISE_CONFIRMATION_COMPLETE", "PROMISE_SCOPE_CLOSED_SUCCESS", "PROMISE_RETURN_PACKET_CREATED"]
            else:
                promise = "OPEN"
                events += ["PROMISE_CONFIRMATION_OPEN", "PROMISE_SCOPE_REMAINS_OPEN"]

    if promise == "CLOSED_SUCCESS":
        if v.get("promise_return_accepted"):
            events += ["PROMISE_RETURN_ACCEPTED_BY_PROJECT", "PROJECT_CONTRACT_REEVALUATED"]
            if v.get("project_result_b_accepted"):
                project = "CLOSED_SUCCESS"
                events += ["PROJECT_RESULT_B_ACCEPTED", "PROJECT_SCOPE_CLOSED_SUCCESS"]
            else:
                project = "OPEN"
                events += ["PROJECT_RESULT_B_MISSING", "PROJECT_SCOPE_REMAINS_OPEN"]
        else:
            project = "WAITING_FOR_RETURN"
            events += ["PROMISE_RETURN_UNACCEPTED_BY_PROJECT", "PROJECT_SCOPE_BLOCKED"]
    else:
        project = "OPEN"
        events.append("PROJECT_SCOPE_REMAINS_OPEN")

    actual = {"action": action, "promise": promise, "project": project}
    expected = v.get("expected", {})
    status = "PASS" if actual == expected else "FAIL"
    if status != "PASS":
        errors.append(f"variant failed:{v.get('variant_id')} actual={actual} expected={expected}")
    results.append({
        "variant_id": v.get("variant_id"),
        "status": status,
        "actual": actual,
        "expected": expected,
        "events": events
    })

v1 = next(r for r in results if r["variant_id"] == "CS-ACTION-CLOSED-RETURN-UNACCEPTED")
v2 = next(r for r in results if r["variant_id"] == "CS-ACTION-RETURN-ACCEPTED-PROMISE-INCOMPLETE")
v3 = next(r for r in results if r["variant_id"] == "CS-PROMISE-CLOSED-PROJECT-INCOMPLETE")
v4 = next(r for r in results if r["variant_id"] == "CS-ALL-REQUIRED-RESULTS-ACCEPTED")

invariants = {
    "ACTION_CLOSURE_DOES_NOT_AUTO_CLOSE_PROMISE": v1["actual"]["action"] == "CLOSED_SUCCESS" and v1["actual"]["promise"] != "CLOSED_SUCCESS",
    "ACCEPTED_ACTION_RETURN_STILL_REQUIRES_PROMISE_CONTRACT": v2["actual"]["action"] == "CLOSED_SUCCESS" and v2["actual"]["promise"] == "OPEN",
    "PROMISE_CLOSURE_DOES_NOT_AUTO_CLOSE_PROJECT": v3["actual"]["promise"] == "CLOSED_SUCCESS" and v3["actual"]["project"] == "OPEN",
    "PROJECT_CLOSES_ONLY_WITH_ALL_REQUIRED_RESULTS": v4["actual"]["project"] == "CLOSED_SUCCESS",
    "PARENT_REEVALUATION_USED": all("PROMISE_CONTRACT_REEVALUATED" in r["events"] for r in [v2, v3, v4]) and all("PROJECT_CONTRACT_REEVALUATED" in r["events"] for r in [v3, v4]),
    "CLOSED_LOWER_SCOPE_NOT_REOPENED": all(r["actual"]["action"] == "CLOSED_SUCCESS" for r in results),
    "RETURN_ACCEPTANCE_SEPARATE_FROM_SUB_SEQUENCE_CLOSURE": "ACTION_RETURN_UNACCEPTED" in v1["events"] and v1["actual"]["action"] == "CLOSED_SUCCESS",
}
for name, ok in invariants.items():
    if not ok:
        errors.append(f"invariant failed:{name}")

report = {
    "report_id": "P2-CLOSURE-SCOPE-INHERITANCE-RFR-001",
    "status": "FAIL" if errors else "PASS",
    "scope_note": "Synthetic nested-closure control-law test. PASS proves closure-scope isolation and return propagation behavior for this fixture only.",
    "pass0": {
        "declared_end": fx.get("declared_end"),
        "closure_scopes": [r.get("closure_scope") for r in hierarchy]
    },
    "pass1": {
        "scope_hierarchy": hierarchy,
        "required_return_routes": fx.get("required_return_routes", []),
        "independent_project_result_source": fx.get("project_result_b_source")
    },
    "pass2": {"variants": results},
    "pass3": {
        "invariant_checks": invariants,
        "closed_sequence_reopen_used": False,
        "closure_status_propagation_mode": "RETURN_PACKET_PLUS_PARENT_REEVALUATION_NOT_STATUS_INHERITANCE"
    },
    "errors": errors
}

(OUT / "P2_CLOSURE_SCOPE_INHERITANCE_RFR_001.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print(report["status"], "variants", len(results), "errors", len(errors))
sys.exit(1 if errors else 0)
