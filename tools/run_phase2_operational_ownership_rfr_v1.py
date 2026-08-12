#!/usr/bin/env python3
from pathlib import Path
import json, sys
from collections import Counter

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/"generated/tests"
OUT.mkdir(parents=True,exist_ok=True)
errors=[]
findings=[]

def load(rel):
    p=ROOT/rel
    if not p.exists():
        errors.append(f"missing:{rel}")
        return {}
    return json.loads(p.read_text(encoding="utf-8"))

source=load("generated/registry_views/operational_subparameters_2593_3072_v1.json")
view=load("generated/registry_views/operational_parameter_ai_asi_ownership_v1.json")
containers=load("registries/asi/OPERATIONAL_CONTAINERS_161_240_APPROVED_V1.json")
ownership=load("machine/wiring/OPERATIONAL_ELEMENT_AI_ASI_OWNERSHIP_V1.json")
ai=load("registries/ai/AI_RUBRIC_V0.json")
asi=load("registries/asi/ASI_RUBRIC_V0.json")
nodes=load("registries/asi/asi_node_registry.json")

source_by_id={r.get("parameter_id"):r for r in source.get("records",[])}
container_to_element={r[0]:r[2] for r in containers.get("records",[]) if len(r)>=3}
element_map={r.get("element_code"):r for r in ownership.get("elements",[])}
ai_ids={r.get("ai_segment_id") for r in ai.get("segments",[])}
asi_ids={r.get("asi_segment_id") for r in asi.get("segments",[])}
node_ids={r.get("asi_node_id") for r in nodes.get("nodes",[])}
rows=view.get("records",[])

# Pass 0
if len(rows)!=480:
    errors.append(f"expected_480_records_found_{len(rows)}")
expected_ids=[f"SB-ASI-P{i:04d}" for i in range(2593,3073)]
if [r.get("parameter_id") for r in rows]!=expected_ids:
    errors.append("parameter_id_sequence_mismatch")

# Pass 1 + Pass 2
for r in rows:
    pid=r.get("parameter_id")
    cid=r.get("container_id")
    ecode=r.get("operational_element_code")
    src=source_by_id.get(pid)
    if src is None:
        errors.append(f"orphan_parameter:{pid}")
        continue
    if r.get("source_parameter_record")!=src:
        errors.append(f"source_record_rewrite_or_drift:{pid}")
    if src.get("container_id")!=cid:
        errors.append(f"parameter_container_mismatch:{pid}")
    if container_to_element.get(cid)!=ecode:
        errors.append(f"container_element_mismatch:{pid}")
    m=element_map.get(ecode)
    if not m:
        errors.append(f"unknown_element:{pid}:{ecode}")
        continue
    if r.get("ownership_class")!=m.get("ownership_class"):
        errors.append(f"ownership_class_mismatch:{pid}")
    if set(r.get("phase2_ai_segments",[]))!=set(m.get("ai_segments",[])):
        errors.append(f"ai_mapping_drift:{pid}")
    if set(r.get("phase2_asi_segments",[]))!=set(m.get("asi_segments",[])):
        errors.append(f"asi_mapping_drift:{pid}")
    if set(r.get("phase2_asi_nodes",[]))!=set(m.get("asi_nodes",[])):
        errors.append(f"node_mapping_drift:{pid}")
    bad_ai=set(r.get("phase2_ai_segments",[]))-ai_ids
    bad_asi=set(r.get("phase2_asi_segments",[]))-asi_ids
    bad_nodes=set(r.get("phase2_asi_nodes",[]))-node_ids
    if bad_ai: errors.append(f"unknown_ai_segments:{pid}:{sorted(bad_ai)}")
    if bad_asi: errors.append(f"unknown_asi_segments:{pid}:{sorted(bad_asi)}")
    if bad_nodes: errors.append(f"unknown_asi_nodes:{pid}:{sorted(bad_nodes)}")
    if not r.get("phase2_ai_segments"):
        findings.append(f"no_ai_mechanism_interface:{pid}")
    if not r.get("phase2_asi_segments"):
        findings.append(f"no_asi_governance_interface:{pid}")

# Pass 3
ownership_counts=Counter(r.get("ownership_class") for r in rows)
element_counts=Counter(r.get("operational_element_code") for r in rows)
expected_ownership=Counter({"AI_PRIMARY":180,"SHARED_AI_ASI":240,"ASI_PRIMARY":60})
if ownership_counts!=expected_ownership:
    errors.append(f"ownership_distribution_changed:{dict(ownership_counts)}")
for i in range(1,9):
    if element_counts[f"E0{i}"]!=60:
        errors.append(f"element_E0{i}_expected_60_found_{element_counts[f'E0{i}']}")

checks={
    "ALL_480_SOURCE_RECORDS_PRESERVED": not any(e.startswith("source_record_rewrite_or_drift") or e.startswith("orphan_parameter") for e in errors),
    "EVERY_PARAMETER_TRACES_TO_CONTAINER_AND_ELEMENT": not any("container_" in e or "unknown_element" in e for e in errors),
    "AI_SEGMENTS_VALID": not any(e.startswith("unknown_ai_segments") for e in errors),
    "ASI_SEGMENTS_VALID": not any(e.startswith("unknown_asi_segments") for e in errors),
    "ASI_NODES_VALID": not any(e.startswith("unknown_asi_nodes") for e in errors),
    "OWNERSHIP_IS_ADDITIVE_NOT_SOURCE_REWRITE": all(r.get("mapping_authority")=="ADDITIVE_PHASE2_NOT_SOURCE_REWRITE" for r in rows),
    "EXPECTED_OWNERSHIP_DISTRIBUTION": ownership_counts==expected_ownership,
    "EACH_E01_E08_HAS_60_PARAMETERS": all(element_counts[f"E0{i}"]==60 for i in range(1,9))
}
for k,v in checks.items():
    if not v and f"invariant_failed:{k}" not in errors:
        errors.append(f"invariant_failed:{k}")

status="FAIL" if errors else ("PASS_WITH_FINDINGS" if findings else "PASS")
report={
  "report_id":"P2-OPERATIONAL-PARAMETER-AI-ASI-OWNERSHIP-RFR-V1",
  "status":status,
  "scope_note":"R-F-R of additive AI/ASI ownership over approved SB-ASI-P2593..P3072. Does not change parameter source identity and does not declare final AI or ASI native parameter counts.",
  "summary":{"records":len(rows),"ownership_counts":dict(ownership_counts),"element_counts":dict(element_counts),"errors":len(errors),"findings":len(findings)},
  "pass0":{"declared_end":"Every approved operational parameter has an auditable AI/ASI ownership/interface mapping without source rewrite.","scope":"SB-ASI-P2593..SB-ASI-P3072","closure_scope":"ownership/routing integrity only"},
  "pass1":{"source_trace":"parameter -> approved generated source record -> CON-161..240 -> E01..E08"},
  "pass2":{"forward_route":"E01..E08 -> ownership class -> AI segments + ASI segments + ASI Nodes"},
  "pass3":{"invariant_checks":checks,"errors":errors,"findings":findings}
}
(OUT/"P2_OPERATIONAL_PARAMETER_AI_ASI_OWNERSHIP_RFR_V1.json").write_text(json.dumps(report,indent=2,ensure_ascii=False),encoding="utf-8")
print(json.dumps(report["summary"],indent=2))
sys.exit(1 if errors else 0)
