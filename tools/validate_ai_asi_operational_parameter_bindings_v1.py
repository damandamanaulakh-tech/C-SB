#!/usr/bin/env python3
from pathlib import Path
import json, sys
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
errors = []

def load(rel):
    p = ROOT / rel
    if not p.exists():
        errors.append(f"missing:{rel}")
        return {}
    return json.loads(p.read_text(encoding="utf-8"))

src = load("generated/registry_views/operational_subparameters_2593_3072_v1.json")
bind = load("generated/registry_views/ai_asi_operational_parameter_bindings_v1.json")
contract = load("machine/parameters/AI_ASI_OPERATIONAL_OWNERSHIP_CONTRACT_V1.json")
spine = load("machine/wiring/BRAIN_ENGINE_OPERATIONAL_SPINE_V1.json")

src_rows = src.get("records", [])
rows = bind.get("records", [])
arches = bind.get("archetypes", [])

expected_ids = [f"SB-ASI-P{i:04d}" for i in range(2593,3073)]
if [r.get("parameter_id") for r in src_rows] != expected_ids:
    errors.append("source operational parameter range changed")
if [r.get("parameter_id") for r in rows] != expected_ids:
    errors.append("binding registry must preserve P2593..P3072 exactly")
if len(rows) != 480 or len(arches) != 48:
    errors.append(f"expected 480 records / 48 archetypes; found {len(rows)} / {len(arches)}")

src_by_id = {r["parameter_id"]: r for r in src_rows}
spine_by_code = {e["element_code"]: e for e in spine.get("elements", [])}
contract_er = contract.get("element_rules", {})
contract_lr = contract.get("local_operation_rules", {})

for r in rows:
    pid = r.get("parameter_id")
    s = src_by_id.get(pid)
    if not s:
        errors.append(f"missing source row:{pid}")
        continue
    for key in ["segment_id","container_id","container_name","element_code","local_number","operational_subparameter"]:
        if r.get(key) != s.get(key):
            errors.append(f"source identity mismatch:{pid}:{key}")
            break
    if r.get("source_system_owner") != "SOURCEBORN":
        errors.append(f"source system owner changed:{pid}")
    ecode = r.get("element_code")
    if r.get("functional_domain_role") != contract_er.get(ecode,{}).get("functional_domain_role"):
        errors.append(f"element ownership mismatch:{pid}")
    if r.get("ai_segment_bindings") != spine_by_code.get(ecode,{}).get("primary_ai_segments",[]):
        errors.append(f"AI segment binding mismatch:{pid}")
    if r.get("asi_segment_bindings") != spine_by_code.get(ecode,{}).get("primary_asi_segments",[]):
        errors.append(f"ASI segment binding mismatch:{pid}")
    local = str(r.get("local_number"))
    if r.get("runtime_operation_owner") != contract_lr.get(local,{}).get("runtime_owner"):
        errors.append(f"runtime owner mismatch:{pid}")

# Exactly 10 instances for every E-code/local-number archetype.
counts = Counter((r.get("element_code"),r.get("local_number")) for r in rows)
if len(counts) != 48 or any(v != 10 for v in counts.values()):
    errors.append("every one of the 48 operational archetypes must have exactly 10 segment instances")

expected_role_counts = {
    "AI_PRIMARY": 180,
    "AI_PRIMARY_UNDER_ASI_PERMISSION": 60,
    "SHARED_AI_ASI": 180,
    "ASI_PRIMARY": 60
}
actual_role_counts = dict(Counter(r.get("functional_domain_role") for r in rows))
if actual_role_counts != expected_role_counts:
    errors.append(f"functional role counts changed:{actual_role_counts}")

# Six local operation owners repeated through 8 elements x 10 segments = 80 instances each.
local_owner_counts = Counter(r.get("runtime_operation_owner") for r in rows)
expected_local_owner_counts = Counter()
for local in range(1,7):
    expected_local_owner_counts[contract_lr[str(local)]["runtime_owner"]] += 80
if local_owner_counts != expected_local_owner_counts:
    errors.append(f"runtime owner counts changed:{dict(local_owner_counts)}")

# Guard against rebranding source IDs as native AI-P / ASI-P.
if any(str(r.get("parameter_id","")).startswith(("AI-P","ASI-P")) for r in rows):
    errors.append("source IDs were illegally rebranded")

print("errors:",len(errors))
for e in errors:
    print("ERROR",e)
sys.exit(1 if errors else 0)
