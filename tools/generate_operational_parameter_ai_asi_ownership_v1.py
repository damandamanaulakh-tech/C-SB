#!/usr/bin/env python3
from pathlib import Path
import json
from collections import Counter

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"generated/registry_views"
OUT.mkdir(parents=True,exist_ok=True)

def load(rel):
    return json.loads((ROOT/rel).read_text(encoding="utf-8"))

params=load("generated/registry_views/operational_subparameters_2593_3072_v1.json")
containers=load("registries/asi/OPERATIONAL_CONTAINERS_161_240_APPROVED_V1.json")
ownership=load("machine/wiring/OPERATIONAL_ELEMENT_AI_ASI_OWNERSHIP_V1.json")

container_to_element={r[0]:r[2] for r in containers.get("records",[]) if len(r)>=3}
element_map={r["element_code"]:r for r in ownership.get("elements",[])}

records=[]
for p in params.get("records",[]):
    cid=p.get("container_id")
    ecode=container_to_element[cid]
    m=element_map[ecode]
    records.append({
        "parameter_id":p.get("parameter_id"),
        "source_parameter_record":p,
        "container_id":cid,
        "operational_element_code":ecode,
        "operational_element_name":m["name"],
        "ownership_class":m["ownership_class"],
        "phase2_ai_segments":m["ai_segments"],
        "phase2_asi_segments":m["asi_segments"],
        "phase2_asi_nodes":m["asi_nodes"],
        "functional_boundary":m["boundary"],
        "mapping_authority":"ADDITIVE_PHASE2_NOT_SOURCE_REWRITE"
    })

counts=Counter(r["ownership_class"] for r in records)
element_counts=Counter(r["operational_element_code"] for r in records)
payload={
    "registry_id":"OPERATIONAL-PARAMETER-AI-ASI-OWNERSHIP-V1",
    "status":"GENERATED_ADDITIVE_MAPPING_FOR_RFR",
    "source_parameters":"generated/registry_views/operational_subparameters_2593_3072_v1.json",
    "source_containers":"registries/asi/OPERATIONAL_CONTAINERS_161_240_APPROVED_V1.json",
    "ownership_map":"machine/wiring/OPERATIONAL_ELEMENT_AI_ASI_OWNERSHIP_V1.json",
    "record_count":len(records),
    "ownership_counts":dict(sorted(counts.items())),
    "element_counts":dict(sorted(element_counts.items())),
    "rule":"Source parameter records are embedded unchanged. Ownership/segment/Node fields are additive Phase-2 mappings only.",
    "records":records
}
assert len(records)==480
assert [r["parameter_id"] for r in records]==[f"SB-ASI-P{i:04d}" for i in range(2593,3073)]
assert counts==Counter({"AI_PRIMARY":180,"SHARED_AI_ASI":240,"ASI_PRIMARY":60})
assert all(element_counts[f"E0{i}"]==60 for i in range(1,9))
(OUT/"operational_parameter_ai_asi_ownership_v1.json").write_text(json.dumps(payload,indent=2,ensure_ascii=False),encoding="utf-8")
print(json.dumps({"record_count":len(records),"ownership_counts":dict(counts),"element_counts":dict(element_counts)},indent=2))
