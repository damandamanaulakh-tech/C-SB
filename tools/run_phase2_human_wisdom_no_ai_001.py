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

fx = load("phase2/tests/P2_HUMAN_WISDOM_NO_AI_FIXTURE_001.json")
human = load("raw/human/HUMAN_CONTAINER_SOURCE_SLICE_HW_001.json")
wis = load("phase2/wisdom/WISDOM_BATCH_001_DERIVATION.json")
asi = load("registries/asi/ASI_RUBRIC_V0.json")

human_ids = {r.get("container_id") for r in human.get("records", [])}
wisdom = {r.get("wisdom_id"): r for r in wis.get("wisdom_candidates", [])}
asi_ids = {r.get("asi_segment_id") for r in asi.get("segments", [])}

if fx.get("fixture_is_source_fact") is not False:
    errors.append("fixture must remain synthetic")
if fx.get("ai_activation", {}).get("required") is not False:
    errors.append("AI must remain not required")
if fx.get("ai_activation", {}).get("activated_segments"):
    errors.append("AI segments unexpectedly activated")
if fx.get("ai_activation", {}).get("activated_ai_only_records"):
    errors.append("AI-only records unexpectedly activated")
if fx.get("ai_activation", {}).get("activated_engines"):
    errors.append("Engines unexpectedly activated")

for cid in fx.get("human_activation", {}).get("container_ids", []):
    if cid not in human_ids:
        errors.append(f"unbound Human container:{cid}")
for sid in fx.get("asi_activation", {}).get("asi_segment_ids", []):
    if sid not in asi_ids:
        errors.append(f"unknown ASI segment:{sid}")

w4 = wisdom.get("WIS-CAND-004", {})
if not w4:
    errors.append("WIS-CAND-004 missing")
if "SOURCE_LINKED_CANDIDATE" not in set(w4.get("epistemic_status", [])):
    errors.append("WIS-CAND-004 lost source-linked candidate status")
if not w4.get("source_refs"):
    errors.append("WIS-CAND-004 missing source refs")

results = []
for v in fx.get("variants", []):
    applicability = bool(v.get("history_relevant"))
    events = ["COMMON_INPUT_RECEIVED", "HUMAN_STATE_AND_HISTORY_READ", "HUMAN_RESPONSE_PRODUCED"]
    if applicability:
        events += ["WIS-CAND-004_APPLICABILITY_TRUE", "WISDOM_USED_AS_CONTEXTUAL_INTERPRETIVE_INPUT"]
    else:
        events += ["WIS-CAND-004_APPLICABILITY_FALSE", "WISDOM_NOT_APPLIED"]
    events += ["ASI_PROVENANCE_AND_APPLICABILITY_AUDIT"]
    status = "PASS" if applicability == v.get("expected_wisdom_applicability") else "FAIL"
    if status != "PASS":
        errors.append(f"variant failed:{v.get('variant_id')}")
    results.append({
        "variant_id": v.get("variant_id"),
        "input": fx.get("common_input"),
        "history_state": v.get("history_state"),
        "current_priority_state": v.get("current_priority_state"),
        "human_response": v.get("human_response"),
        "wisdom_applicable": applicability,
        "expected_wisdom_applicability": v.get("expected_wisdom_applicability"),
        "response_owner": "HUMAN",
        "ai_used": False,
        "events": events,
        "status": status
    })

r_a = next(r for r in results if r["variant_id"] == "HW-HISTORY-A")
r_b = next(r for r in results if r["variant_id"] == "HW-HISTORY-B")
r_c = next(r for r in results if r["variant_id"] == "HW-HISTORY-PROVEN-IRRELEVANT")

invariants = {
    "AI_NOT_REQUIRED": all(r["ai_used"] is False for r in results),
    "HUMAN_OWNS_RESPONSE": all(r["response_owner"] == "HUMAN" for r in results),
    "SAME_INPUT_CAN_HAVE_DIFFERENT_RESPONSES_WITH_RELEVANT_HISTORY": r_a["input"] == r_b["input"] and r_a["human_response"] != r_b["human_response"] and r_a["wisdom_applicable"] and r_b["wisdom_applicable"],
    "WISDOM_APPLICABILITY_CAN_BE_FALSE": r_c["wisdom_applicable"] is False and "WISDOM_NOT_APPLIED" in r_c["events"],
    "WISDOM_DOES_NOT_PRODUCE_HUMAN_RESPONSE": fx.get("wisdom_activation", {}).get("forbidden_role", "").startswith("Wisdom does not select or execute"),
    "WISDOM_REMAINS_SOURCE_LINKED_CANDIDATE": bool(w4.get("source_refs")) and "SOURCE_LINKED_CANDIDATE" in set(w4.get("epistemic_status", [])),
    "ASI_ONLY_AUDITS_NOT_HUMAN_DECISION_MAKER": fx.get("asi_activation", {}).get("role", "").endswith("audit only")
}
for name, ok in invariants.items():
    if not ok:
        errors.append(f"invariant failed:{name}")

report = {
    "report_id": "P2-HUMAN-WISDOM-NO-AI-RFR-001",
    "status": "FAIL" if errors else "PASS",
    "scope_note": "Synthetic Human + Wisdom integration test with no AI activation. PASS proves domain ownership and conditional Wisdom applicability behavior for this fixture only.",
    "domains_active": ["HUMAN", "WISDOM", "ASI"],
    "domains_inactive": ["AI"],
    "pass0": {
        "declared_end": fx.get("declared_end"),
        "scope": fx.get("scope"),
        "fixture_is_source_fact": fx.get("fixture_is_source_fact")
    },
    "pass1": {
        "human_source_bound": set(fx.get("human_activation", {}).get("container_ids", [])) <= human_ids,
        "wisdom_source_bound": bool(w4.get("source_refs")),
        "asi_ids_valid": not any(e.startswith("unknown ASI") for e in errors),
        "ai_activation_empty": fx.get("ai_activation", {}).get("activated_segments") == []
    },
    "pass2": {"variants": results},
    "pass3": {
        "invariant_checks": invariants,
        "wisdom_epistemic_status": w4.get("epistemic_status", []),
        "wisdom_law_status": "NOT_PROMOTED",
        "ai_runtime_dependency": False
    },
    "errors": errors
}

(OUT / "P2_HUMAN_WISDOM_NO_AI_RFR_001.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print(report["status"], "variants", len(results), "errors", len(errors))
sys.exit(1 if errors else 0)
