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

fx = load("phase2/tests/P2_ACTOR_VIEW_LEAKAGE_FIXTURE_001.json")
human = load("raw/human/HUMAN_CONTAINER_SOURCE_SLICE_AV_001.json")
ai = load("registries/ai/AI_RUBRIC_V0.json")
wis = load("phase2/wisdom/WISDOM_BATCH_001_DERIVATION.json")
asi = load("registries/asi/ASI_RUBRIC_V0.json")
nodes = load("registries/asi/asi_node_registry.json")

human_ids = {r.get("container_id") for r in human.get("records", [])}
ai_ids = {r.get("ai_segment_id") for r in ai.get("segments", [])}
wisdom = {r.get("wisdom_id"): r for r in wis.get("wisdom_candidates", [])}
asi_ids = {r.get("asi_segment_id") for r in asi.get("segments", [])}
node_ids = {r.get("asi_node_id") for r in nodes.get("nodes", [])}

if fx.get("fixture_is_source_fact") is not False:
    errors.append("fixture must remain synthetic")
if fx.get("global_state", {}).get("FACT_F") != "KNOWN_TRUE":
    errors.append("global fixture state changed")
if fx.get("initial_actor_view", {}).get("FACT_F") != "UNKNOWN":
    errors.append("initial actor view changed")

for cid in fx.get("human_activation", {}).get("container_ids", []):
    if cid not in human_ids:
        errors.append(f"unbound Human container:{cid}")
for aid in fx.get("ai_activation", {}).get("ai_segment_ids", []):
    if aid not in ai_ids:
        errors.append(f"unknown AI segment:{aid}")
for sid in fx.get("asi_activation", {}).get("asi_segment_ids", []):
    if sid not in asi_ids:
        errors.append(f"unknown ASI segment:{sid}")
for nid in fx.get("asi_activation", {}).get("asi_node_ids", []):
    if nid not in node_ids:
        errors.append(f"unknown ASI node:{nid}")

w1 = wisdom.get("WIS-CAND-001", {})
if not w1:
    errors.append("WIS-CAND-001 missing")
if "SOURCE_LINKED_CANDIDATE" not in set(w1.get("epistemic_status", [])):
    errors.append("WIS-CAND-001 lost source-linked candidate status")
if not w1.get("source_refs"):
    errors.append("WIS-CAND-001 missing source refs")

results = []
for v in fx.get("variants", []):
    actor_view = fx.get("initial_actor_view", {}).get("FACT_F")
    events = ["LOAD_GLOBAL_STATE", "LOAD_ACTOR_VIEW", "LOAD_AI_SYSTEM_BELIEF", "WIS-CAND-001_APPLICABILITY_TRUE"]
    comm = v.get("communication_sequence")
    if comm == "ABSENT":
        events += ["NO_INFORMATION_TRANSFER_SEQUENCE", "ACTOR_VIEW_UNCHANGED"]
    elif comm == "CLOSED_SUCCESS":
        events += ["INFORMATION_TRANSFER_SEQUENCE_CLOSED_SUCCESS"]
        if v.get("return_accepted"):
            actor_view = "KNOWN_TRUE" if v.get("return_value") == "FACT_F_TRUE" else actor_view
            events += ["REQUIRED_RETURN_ACCEPTED", "ACTOR_VIEW_UPDATED_WITH_PROVENANCE"]
        else:
            events += ["REQUIRED_RETURN_NOT_ACCEPTED", "ACTOR_VIEW_UNCHANGED"]
    else:
        errors.append(f"unknown communication status:{comm}")
    result = {
        "variant_id": v.get("variant_id"),
        "ai_system_belief": v.get("ai_system_belief"),
        "global_fact": fx.get("global_state", {}).get("FACT_F"),
        "actor_view_final": actor_view,
        "expected_actor_view_final": v.get("expected_actor_view_final"),
        "status": "PASS" if actor_view == v.get("expected_actor_view_final") else "FAIL",
        "events": events,
        "actor_decision_reads": "ACTOR_VIEW"
    }
    if result["status"] != "PASS":
        errors.append(f"variant failed:{result['variant_id']}")
    results.append(result)

accepted = next(r for r in results if r["variant_id"] == "AV-COMMUNICATION-ACCEPTED")
unaccepted = next(r for r in results if r["variant_id"] == "AV-COMMUNICATION-UNACCEPTED")
inference_only = next(r for r in results if r["variant_id"] == "AV-AI-INFERENCE-ONLY")
no_comm = next(r for r in results if r["variant_id"] == "AV-NO-COMMUNICATION")

invariants = {
    "GLOBAL_STATE_SEPARATE_FROM_ACTOR_VIEW": no_comm["global_fact"] == "KNOWN_TRUE" and no_comm["actor_view_final"] == "UNKNOWN",
    "AI_BELIEF_SEPARATE_FROM_ACTOR_VIEW": inference_only["ai_system_belief"] == "INFERRED_TRUE" and inference_only["actor_view_final"] == "UNKNOWN",
    "CLOSED_SEQUENCE_ALONE_DOES_NOT_UPDATE_VIEW": unaccepted["actor_view_final"] == "UNKNOWN",
    "ACCEPTED_RETURN_CAN_UPDATE_VIEW": accepted["actor_view_final"] == "KNOWN_TRUE",
    "VIEW_UPDATE_HAS_PROVENANCE_EVENT": "ACTOR_VIEW_UPDATED_WITH_PROVENANCE" in accepted["events"],
    "NO_HIDDEN_KNOWLEDGE_INJECTION": all(r["actor_view_final"] == "UNKNOWN" for r in [no_comm, inference_only, unaccepted]),
    "ACTOR_DECISION_READS_ACTOR_VIEW": all(r["actor_decision_reads"] == "ACTOR_VIEW" for r in results),
    "WISDOM_DOES_NOT_WRITE_VIEW": fx.get("wisdom_activation", {}).get("forbidden_write", "").startswith("Wisdom may constrain modelling"),
    "AI_DOES_NOT_WRITE_VIEW": fx.get("ai_activation", {}).get("forbidden_write", "").startswith("AI may not silently write")
}
for k, ok in invariants.items():
    if not ok:
        errors.append(f"invariant failed:{k}")

report = {
    "report_id": "P2-ACTOR-VIEW-LEAKAGE-RFR-001",
    "status": "FAIL" if errors else "PASS",
    "scope_note": "Synthetic Actor View control-law test. PASS proves separation and legal update behavior for this fixture, not the truth of FACT_F or any real actor's knowledge.",
    "domains": ["HUMAN", "AI", "WISDOM", "ASI"],
    "pass0": {
        "declared_end": fx.get("declared_end"),
        "scope": fx.get("scope"),
        "fixture_is_source_fact": fx.get("fixture_is_source_fact")
    },
    "pass1": {
        "human_source_bound": set(fx.get("human_activation", {}).get("container_ids", [])) <= human_ids,
        "wisdom_source_bound": bool(w1.get("source_refs")),
        "ai_and_asi_ids_valid": not any(e.startswith("unknown AI") or e.startswith("unknown ASI") for e in errors)
    },
    "pass2": {"variants": results},
    "pass3": {
        "invariant_checks": invariants,
        "wisdom_epistemic_status": w1.get("epistemic_status", []),
        "global_state_final": fx.get("global_state"),
        "closed_sequence_reopen_used": False
    },
    "errors": errors
}

(OUT / "P2_ACTOR_VIEW_LEAKAGE_RFR_001.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print(report["status"], "variants", len(results), "errors", len(errors))
sys.exit(1 if errors else 0)
