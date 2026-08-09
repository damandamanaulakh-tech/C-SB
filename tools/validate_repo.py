#!/usr/bin/env python3
from pathlib import Path
import json, re, sys

ROOT = Path(__file__).resolve().parents[1]
errors = []
warnings = []

def load(path):
    p = ROOT / path
    if not p.exists():
        errors.append(f"Missing required file: {path}")
        return {}
    return json.loads(p.read_text(encoding="utf-8"))

canonical = load("CANONICALITY.json")
if canonical.get("phase2", {}).get("ai_capability_map_status") != "REVIEW_ONLY":
    errors.append("AI capability map must remain REVIEW_ONLY until explicit AI adoption closure.")
if canonical.get("phase2", {}).get("status") != "ACTIVE":
    errors.append("Phase 2 is expected to be ACTIVE.")

for key in ["canonical_sequence_execution_manifest", "canonical_phase2_adoption_manifest"]:
    rel = canonical.get("phase1", {}).get(key)
    if not rel or not (ROOT / rel).exists():
        errors.append(f"Canonical manifest missing or invalid: {key}={rel}")

for manifest_path in ROOT.rglob("*.manifest.json"):
    if "generated" in manifest_path.parts:
        continue
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    for rel in data.get("parts_in_order", []):
        p = manifest_path.parent / rel
        if not p.exists():
            errors.append(f"Manifest part missing: {p.relative_to(ROOT)}")

human = load("registries/human/HUMAN_REGISTRY_ADOPTION_CONTRACT.json")
if human.get("locked_shape") != {"segments": 10, "containers": 80, "active_parameters": 2560}:
    errors.append("Human native shape changed.")

vocab = load("machine/vocab/core_vocab.json")
for required in ["CLOSED_SUCCESS", "CLOSED_FAILURE", "CLOSED_NOT_APPLICABLE"]:
    if required not in vocab.get("terminal_sequence_statuses", []):
        errors.append(f"Missing terminal status: {required}")
if "META" not in vocab.get("controller_types", []):
    errors.append("META controller missing.")
if "WANT" not in vocab.get("driver_types", []):
    errors.append("WANT incorrectly removed from driver registry.")
if "ALWAYS" not in vocab.get("threshold_types", []):
    errors.append("Threshold vocabulary must include ALWAYS for edges with no special gate.")

asi = load("registries/asi/asi_node_registry.json")
asi_ids = [n.get("asi_node_id") for n in asi.get("nodes", [])]
if len(asi_ids) != 18 or len(set(asi_ids)) != 18:
    errors.append(f"ASI service registry must contain 18 unique nodes; found {len(asi_ids)} / {len(set(asi_ids))} unique.")

brains = load("registries/asi/node_brains_v0.json")
brain_rows = brains.get("node_brains", [])
brain_ids = [n.get("node_brain_id") for n in brain_rows]
brain_asi_ids = [n.get("asi_node_id") for n in brain_rows]
if len(brain_ids) != 18 or len(set(brain_ids)) != 18:
    errors.append(f"Node Brain v0 must contain 18 unique brains; found {len(brain_ids)} / {len(set(brain_ids))} unique.")
if set(brain_asi_ids) != set(asi_ids):
    errors.append("Node Brain v0 must bind exactly once to every ASI service node.")
for row in brain_rows:
    for required_key in ["inputs","outputs","reads","writes","threshold_evaluators","closure_responsibilities"]:
        if not row.get(required_key):
            errors.append(f"{row.get('node_brain_id')} missing required contract field {required_key}.")

# V2 rubric registry
rubric_doc = load("machine/rubrics/RUBRIC_REGISTRY_R01_R52.json")
rubrics = rubric_doc.get("rubrics", {})
expected_rubric_ids = {f"R{i:02d}" for i in range(1, 53)}
if set(rubrics) != expected_rubric_ids:
    errors.append(f"V2 rubric registry must contain exactly R01..R52. Missing={sorted(expected_rubric_ids-set(rubrics))}, extra={sorted(set(rubrics)-expected_rubric_ids)}")
calc_dimensions = sum(len(v.get("dimensions", [])) for v in rubrics.values())
if rubric_doc.get("dimension_count") != 987 or calc_dimensions != 987:
    errors.append(f"V2 rubric registry must contain 987 dimensions; declared={rubric_doc.get('dimension_count')} calculated={calc_dimensions}.")
pack_members = []
for pack_name, ids in rubric_doc.get("packs", {}).items():
    pack_members.extend(ids)
if len(pack_members) != 52 or len(set(pack_members)) != 52 or set(pack_members) != expected_rubric_ids:
    errors.append("V2 rubric packs must cover R01..R52 exactly once.")

pack_bindings = load("machine/rubrics/RUBRIC_PACK_ASI_NODE_BINDINGS_v0.json")
if set(pack_bindings.get("bindings", {})) != set(rubric_doc.get("packs", {})):
    errors.append("Rubric-pack ASI binding coverage must exactly match rubric-pack registry.")
for pack, bind in pack_bindings.get("bindings", {}).items():
    unknown_nodes = (set(bind.get("primary_asi_nodes", [])) | set(bind.get("secondary_asi_nodes", []))) - set(asi_ids)
    if unknown_nodes:
        errors.append(f"{pack} references unknown ASI nodes: {sorted(unknown_nodes)}")
    if bind.get("rubrics") != rubric_doc.get("packs", {}).get(pack):
        errors.append(f"{pack} rubric list differs between registry and ASI binding.")

# V2 typed-null and service contracts
typed_nulls = load("machine/v2/TYPED_NULL_SEMANTICS.json")
required_nulls = {"UNKNOWN","UNAVAILABLE","CONTRADICTORY","NOT_APPLICABLE","ABSENT","UNDECLARED","REDACTED","ERROR"}
if set(typed_nulls.get("values", {})) != required_nulls:
    errors.append("Typed null semantics must contain the exact V2 eight-state set.")
services = load("machine/v2/CROSS_CUTTING_SERVICES_SVC01_SVC18.json")
svc_ids = [s.get("service_id") for s in services.get("services", [])]
if svc_ids != [f"SVC-{i:02d}" for i in range(1, 19)]:
    errors.append("Cross-cutting services must be exactly SVC-01..SVC-18 in order.")

records = load("machine/v2/FIRST_CLASS_RECORD_SCHEMAS.json")
for required_schema in ["SEQUENCE_TEMPLATE","SEQUENCE_INSTANCE","NODE_TEMPLATE","NODE_INSTANCE","EDGE_TEMPLATE","EDGE_INSTANCE","CLAIM","IDENTITY_DECISION_PACKET","COMPRESSION_CONTRACT","GAP_RECORD","CONTRADICTION_RECORD","EVIDENCE_RECORD","PROOF_DEBT_RECORD","OPEN_SEQUENCE_LEDGER_RECORD","SEED_RECORD","ACTOR_VIEW_RECORD","CLOSURE_PACKET"]:
    if required_schema not in records.get("schemas", {}):
        errors.append(f"Missing V2 first-class schema: {required_schema}")

param_doc = load("machine/parameters/PARAMETER_AND_SUBPARAMETER_V2.json")
required_split_statuses = {"OBSERVED","CANDIDATE_SPLIT","UNDER_REVIEW","URR_CHALLENGED","VALIDATED","APPROVED","CANONICAL","MERGED","REJECTED","DEPRECATED"}
if set(param_doc.get("candidate_statuses", [])) != required_split_statuses:
    errors.append("Parameter split candidate statuses differ from V2 source contract.")
if param_doc.get("split_score_rubric", {}).get("weights_status") != "UNDECLARED_NOT_FIXED":
    errors.append("Split-score weights must remain undeclared until explicitly defined; do not fabricate weights.")

v2graph = load("machine/v2/CANONICAL_GRAPH_V2_LOCK_CANDIDATE.json")
if set(v2graph.get("mode_router", {})) != {"RECONSTRUCTION","EXECUTION","DISCOVERY","AUDIT"}:
    errors.append("V2 Mode Router must contain RECONSTRUCTION, EXECUTION, DISCOVERY, AUDIT.")
if v2graph.get("status") != "V2_LOCK_CANDIDATE_NOT_CANONICAL_YET":
    errors.append("V2 graph must remain a lock candidate until explicit canonical adoption.")

# AI review source and proposed candidate layer
ai_path = ROOT / "raw/rubrics/AI_CAPABILITY_TO_SOURCEBORN_CONTAINERS_REVIEW.md"
ai_ids = []
if ai_path.exists():
    ai_ids = sorted(set(re.findall(r"\bAI-CAP-\d{3}\b", ai_path.read_text(encoding="utf-8"))))
    if len(ai_ids) != 74:
        errors.append(f"AI review map expected 74 unique capability families; found {len(ai_ids)}.")
else:
    errors.append("AI capability review source missing.")

rules = load("phase2/reviews/AI_CAPABILITY_DECISION_RULES_v0.json")
layer_ids = []
for ids in rules.get("layer_groups", {}).values():
    layer_ids.extend(ids)
if len(layer_ids) != 74 or len(set(layer_ids)) != 74:
    errors.append(f"AI decision rules must classify exactly 74 unique source families; found {len(layer_ids)} / {len(set(layer_ids))} unique.")
if ai_ids and set(layer_ids) != set(ai_ids):
    errors.append("AI decision rule coverage does not exactly match source AI-CAP IDs.")
if rules.get("status") != "P2_REVIEW_PROPOSAL_NOT_ADOPTED":
    errors.append("AI decision rules must remain a non-adopted review proposal until closure.")

ai_layer_bindings = load("registries/ai/AI_LAYER_SEQUENCE_BINDINGS_v0.json")
if set(ai_layer_bindings.get("bindings", {})) != set(rules.get("layer_groups", {})):
    errors.append("AI layer Sequence bindings must exactly cover the AI candidate layer groups.")

native_dir = ROOT / "registries/human/native"
if not native_dir.exists() or not any(p.is_file() for p in native_dir.rglob("*")):
    warnings.append("Approved Human 2,560-row native registry not present yet; full parameter relinking remains blocked by design.")

print("errors:", len(errors))
for e in errors:
    print("ERROR", e)
print("warnings:", len(warnings))
for w in warnings:
    print("WARN", w)
sys.exit(1 if errors else 0)
