#!/usr/bin/env python3
from pathlib import Path
import json
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "generated/registry_views"
OUT.mkdir(parents=True, exist_ok=True)

def load(rel):
    return json.loads((ROOT / rel).read_text(encoding="utf-8"))

params = load("generated/registry_views/operational_subparameters_2593_3072_v1.json")
spine = load("machine/wiring/BRAIN_ENGINE_OPERATIONAL_SPINE_V1.json")
contract = load("machine/parameters/AI_ASI_OPERATIONAL_OWNERSHIP_CONTRACT_V1.json")

elements = {e["element_code"]: e for e in spine.get("elements", [])}
local_rules = contract.get("local_operation_rules", {})
element_rules = contract.get("element_rules", {})

records = []
for p in params.get("records", []):
    ecode = p["element_code"]
    local = str(p["local_number"])
    e = elements[ecode]
    er = element_rules[ecode]
    lr = local_rules[local]
    records.append({
        "parameter_id": p["parameter_id"],
        "source_system_owner": "SOURCEBORN",
        "segment_id": p["segment_id"],
        "container_id": p["container_id"],
        "container_name": p["container_name"],
        "element_code": ecode,
        "element_name": e["name"],
        "local_number": p["local_number"],
        "operational_subparameter": p["operational_subparameter"],
        "source_sequence_role": p.get("sequence_role"),
        "functional_domain_role": er["functional_domain_role"],
        "ai_mechanism_active": er["ai_active"],
        "asi_governance_required": er["asi_governance_required"],
        "ai_segment_bindings": e.get("primary_ai_segments", []),
        "asi_segment_bindings": e.get("primary_asi_segments", []),
        "asi_node_bindings": e.get("asi_nodes", []),
        "runtime_operation_owner": lr["runtime_owner"],
        "sequence_runtime_bindings": lr["sequence_runtime_binding"],
        "authority_rule": lr["authority_rule"],
        "source_identity_preserved": True,
        "source_approval_status": p.get("approval_status"),
        "source_evidence_status": p.get("evidence_status")
    })

assert len(records) == 480
assert [r["parameter_id"] for r in records] == [f"SB-ASI-P{i:04d}" for i in range(2593, 3073)]

# 48 archetypes = 8 elements x 6 local operations.
archetypes = []
for ecode in [f"E0{i}" for i in range(1, 9)]:
    e = elements[ecode]
    er = element_rules[ecode]
    for local in range(1, 7):
        lr = local_rules[str(local)]
        sample = next(r for r in records if r["element_code"] == ecode and r["local_number"] == local)
        archetypes.append({
            "archetype_id": f"OP-ARCH-{ecode}-{local:02d}",
            "element_code": ecode,
            "element_name": e["name"],
            "local_number": local,
            "local_operation": lr["name"],
            "source_sequence_role": sample["source_sequence_role"],
            "functional_domain_role": er["functional_domain_role"],
            "ai_segment_bindings": e.get("primary_ai_segments", []),
            "asi_segment_bindings": e.get("primary_asi_segments", []),
            "asi_node_bindings": e.get("asi_nodes", []),
            "runtime_operation_owner": lr["runtime_owner"],
            "sequence_runtime_bindings": lr["sequence_runtime_binding"],
            "authority_rule": lr["authority_rule"],
            "instance_count": 10
        })
assert len(archetypes) == 48

role_counts = Counter(r["functional_domain_role"] for r in records)
runtime_owner_counts = Counter(r["runtime_operation_owner"] for r in records)

payload = {
    "registry_id": "AI-ASI-OPERATIONAL-PARAMETER-BINDINGS-V1",
    "status": "GENERATED_ADDITIVE_MAPPING_NOT_SOURCE_REWRITE",
    "source_parameter_registry": "generated/registry_views/operational_subparameters_2593_3072_v1.json",
    "ownership_contract": "machine/parameters/AI_ASI_OPERATIONAL_OWNERSHIP_CONTRACT_V1.json",
    "record_count": 480,
    "archetype_count": 48,
    "summary": {
        "functional_domain_role_counts": dict(sorted(role_counts.items())),
        "runtime_operation_owner_counts": dict(sorted(runtime_owner_counts.items())),
        "source_system_owner": "SOURCEBORN"
    },
    "archetypes": archetypes,
    "records": records
}

(OUT / "ai_asi_operational_parameter_bindings_v1.json").write_text(json.dumps(payload, indent=2), encoding="utf-8")
print(json.dumps(payload["summary"], sort_keys=True), "archetypes", len(archetypes), "records", len(records))
