#!/usr/bin/env python3
from pathlib import Path
import hashlib, json, sys

ROOT = Path(__file__).resolve().parents[1]
CUSTODY = ROOT / "phase2/sources/GROWTH_BATCH_003_SOURCE_CUSTODY.json"
REG = ROOT / "registries/sourceborn/GROWTH_BATCH_003_DERIVED_OBJECTS_V1.json"
OUT = ROOT / "generated/tests/P2_GROWTH_BATCH_003_RFR_V1.json"
OUT.parent.mkdir(parents=True, exist_ok=True)

errors = []
custody = json.loads(CUSTODY.read_text(encoding="utf-8"))
growth = json.loads(REG.read_text(encoding="utf-8"))

if custody.get("source_id") != "SRC-GROW-003-001": errors.append("wrong source id")
if custody.get("source_sha256") != "700ad067f8d79be52ec14510d4b67428dde8760b444502ab7a20d3770e4460d0": errors.append("source fingerprint mismatch")
if custody.get("source_unit_count") != 9 or len(custody.get("source_units", [])) != 9: errors.append("source unit count must be 9")
if len(growth.get("event_ids", [])) != 9 or len(set(growth.get("event_ids", []))) != 9: errors.append("event id count mismatch")
if len(growth.get("event_memory_ids", [])) != 9 or len(set(growth.get("event_memory_ids", []))) != 9: errors.append("event memory count mismatch")
if len(growth.get("pattern_contribution_ids", [])) != 9 or len(set(growth.get("pattern_contribution_ids", []))) != 9: errors.append("pattern contribution count mismatch")
if len(growth.get("relation_ids", [])) != 10: errors.append("relation count mismatch")
if len(growth.get("path_ids", [])) != 4: errors.append("path count mismatch")
if len(growth.get("intent_signatures", [])) != 3: errors.append("intent signature count mismatch")
if len(growth.get("combination_signatures", [])) != 5: errors.append("combination signature count mismatch")
if len(growth.get("pattern_candidates", [])) != 6: errors.append("pattern candidate count mismatch")
if len(growth.get("primitive_candidates", [])) != 4: errors.append("primitive candidate count mismatch")

all_ids = []
all_ids += growth.get("event_ids", [])
all_ids += growth.get("event_memory_ids", [])
all_ids += growth.get("pattern_contribution_ids", [])
all_ids += [x.get("relation_id") for x in growth.get("relation_ids", [])]
all_ids += [x.get("path_id") for x in growth.get("path_ids", [])]
all_ids += [x.get("intent_signature_id") for x in growth.get("intent_signatures", [])]
all_ids += [x.get("combination_id") for x in growth.get("combination_signatures", [])]
all_ids += [x.get("pattern_candidate_id") for x in growth.get("pattern_candidates", [])]
all_ids += [x.get("candidate_id") for x in growth.get("primitive_candidates", [])]
if None in all_ids or len(all_ids) != len(set(all_ids)): errors.append("duplicate or missing growth IDs")

for x in growth.get("primitive_candidates", []):
    if x.get("canonical") is not False or x.get("status") != "REVIEW_REQUIRED": errors.append(f"primitive candidate not review-gated: {x.get('candidate_id')}")
    if x.get("direct_action_authority") is not False: errors.append(f"primitive candidate has direct authority: {x.get('candidate_id')}")

follower_rel = next((x for x in growth.get("relation_ids", []) if x.get("relation_id") == "REL-GROW-003-010"), None)
if not follower_rel or follower_rel.get("epistemic_status") != "SOURCE_DEFINED_PERSONAL_THEORY_NOT_UNIVERSAL_FACT": errors.append("follower theory lost source-only epistemic guard")

d = growth.get("count_delta", {})
computed = sum([
    d.get("event_memory_ids_added", 0), d.get("pattern_contribution_ids_added", 0), d.get("relation_ids_added", 0), d.get("path_ids_added", 0),
    d.get("intent_signature_ids_added", 0), d.get("combination_signature_ids_added", 0), d.get("pattern_candidate_ids_added", 0), d.get("primitive_candidate_ids_added", 0)
])
if computed != 50 or d.get("persistent_brain_objects_added") != 50: errors.append("persistent Brain-object delta must be exactly 50")
if d.get("human_derived_source_parameters_before") != 3204 or d.get("human_derived_source_parameters_after") != 3204: errors.append("Human source count must remain 3204")
if d.get("persistent_brain_objects_added", 0) <= 0: errors.append("monotonic growth failed")

report = {
  "report_id": "P2-GROWTH-BATCH-003-RFR-V1",
  "status": "PASS" if not errors else "FAIL",
  "source_id": "SRC-GROW-003-001",
  "source_event_units": 9,
  "persistent_growth": {
    "event_memory_ids": 9,
    "pattern_contribution_ids": 9,
    "relation_ids": 10,
    "path_ids": 4,
    "intent_signature_ids": 3,
    "combination_signature_ids": 5,
    "pattern_candidate_ids": 6,
    "primitive_candidate_ids": 4,
    "total_persistent_brain_objects_added": 50
  },
  "human_source_parameter_count": 3204,
  "parameter_inflation": 0,
  "errors": errors
}
OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
print(report["status"], "persistent_growth", 50, "errors", len(errors))
sys.exit(1 if errors else 0)
