#!/usr/bin/env python3
from pathlib import Path
import json, re

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "raw/rubrics/AI_CAPABILITY_TO_SOURCEBORN_CONTAINERS_REVIEW.md"
RULES = ROOT / "phase2/reviews/AI_CAPABILITY_DECISION_RULES_v0.json"
OUT = ROOT / "generated/registry_views/ai_native_candidate_registry_v0.json"
OUT.parent.mkdir(parents=True, exist_ok=True)

text = SRC.read_text(encoding="utf-8")
rules = json.loads(RULES.read_text(encoding="utf-8"))

row_rx = re.compile(r"^\|\s*(AI-CAP-\d{3})\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|\s*(.*?)\s*\|$", re.M)
rows = []
for m in row_rx.finditer(text):
    cid, name, primary, secondary = [x.strip() for x in m.groups()]
    rows.append({
        "source_id": cid,
        "source_name": name,
        "human_crosswalk_primary_raw": primary,
        "human_crosswalk_secondary_raw": secondary,
        "human_crosswalk_relation_type": "FUNCTIONAL_ANALOGY"
    })

expected = rules["source_expected_count"]
if len(rows) != expected:
    raise SystemExit(f"Expected {expected} AI capability rows, found {len(rows)}")

layer_for = {}
for layer, ids in rules["layer_groups"].items():
    for cid in ids:
        if cid in layer_for:
            raise SystemExit(f"Duplicate layer assignment: {cid}")
        layer_for[cid] = layer

source_ids = {r["source_id"] for r in rows}
if set(layer_for) != source_ids:
    missing = sorted(source_ids - set(layer_for))
    extra = sorted(set(layer_for) - source_ids)
    raise SystemExit(f"Layer coverage mismatch missing={missing} extra={extra}")

layer_to_asi = {
    "CORE_REASONING": ["ASI-NODE-02","ASI-NODE-07","ASI-NODE-08","ASI-NODE-16"],
    "KNOWLEDGE_RETRIEVAL": ["ASI-NODE-01","ASI-NODE-07","ASI-NODE-12"],
    "MEMORY_STATE": ["ASI-NODE-12","ASI-NODE-13","ASI-NODE-14"],
    "PERCEPTION_GROUNDING": ["ASI-NODE-02","ASI-NODE-07","ASI-NODE-09"],
    "LANGUAGE_COMMUNICATION": ["ASI-NODE-09","ASI-NODE-10","ASI-NODE-15"],
    "PLANNING_CONTROL": ["ASI-NODE-03","ASI-NODE-04","ASI-NODE-05","ASI-NODE-08","ASI-NODE-17"],
    "TOOL_EXECUTION": ["ASI-NODE-05","ASI-NODE-09","ASI-NODE-10","ASI-NODE-11"],
    "SOCIAL_MODELING": ["ASI-NODE-02","ASI-NODE-03","ASI-NODE-08","ASI-NODE-17"],
    "VALUE_RISK_SAFETY": ["ASI-NODE-03","ASI-NODE-04","ASI-NODE-05","ASI-NODE-07","ASI-NODE-11","ASI-NODE-17"],
    "SELF_MONITORING": ["ASI-NODE-07","ASI-NODE-10","ASI-NODE-11","ASI-NODE-12","ASI-NODE-16"],
    "LEARNING_ADAPTATION": ["ASI-NODE-12","ASI-NODE-13","ASI-NODE-14","ASI-NODE-16"],
    "TRAINING_OPTIMIZATION": ["ASI-NODE-12","ASI-NODE-13","ASI-NODE-15","ASI-NODE-16"],
    "SECURITY_ROBUSTNESS": ["ASI-NODE-04","ASI-NODE-05","ASI-NODE-07","ASI-NODE-11","ASI-NODE-17"],
    "EVALUATION_OVERSIGHT": ["ASI-NODE-07","ASI-NODE-11","ASI-NODE-15","ASI-NODE-16","ASI-NODE-17"],
    "SYSTEM_RELIABILITY": ["ASI-NODE-05","ASI-NODE-10","ASI-NODE-11","ASI-NODE-12","ASI-NODE-14","ASI-NODE-17"],
    "POLICY_OUTPUT_CONTROL": ["ASI-NODE-03","ASI-NODE-04","ASI-NODE-08","ASI-NODE-09","ASI-NODE-11","ASI-NODE-17"],
    "COMPOSITE_OUTCOME": ["ASI-NODE-10","ASI-NODE-15","ASI-NODE-16","ASI-NODE-17"]
}

candidates = []
for row in rows:
    cid = row["source_id"]
    decision = rules["decision_overrides"].get(cid, rules["default_decision"])
    layer = layer_for[cid]
    mode = rules["mode_overrides"].get(cid, rules["default_runtime_or_training"])
    record = {
        **row,
        "candidate_status": "REVIEW_ONLY_NOT_ADOPTED",
        "proposed_decision": decision,
        "proposed_name": rules["proposed_name_overrides"].get(cid, row["source_name"]),
        "capability_layer": layer,
        "runtime_or_training": mode,
        "primary_asi_nodes": layer_to_asi[layer],
        "notes": rules.get("notes", {}).get(cid),
        "split_children": rules.get("split_children", {}).get(cid, [])
    }
    candidates.append(record)

out = {
    "status": "P2_AI_NATIVE_CANDIDATE_V0_REVIEW_ONLY",
    "source": str(SRC.relative_to(ROOT)),
    "decision_rules": str(RULES.relative_to(ROOT)),
    "source_count": len(rows),
    "adoption_rule": "No candidate is native/adopted until an explicit AI adoption closure packet changes registry authority.",
    "candidates": candidates
}
OUT.write_text(json.dumps(out, indent=2), encoding="utf-8")
print(f"wrote {OUT.relative_to(ROOT)} with {len(candidates)} source families")
