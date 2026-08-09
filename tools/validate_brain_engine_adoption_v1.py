#!/usr/bin/env python3
from pathlib import Path
import json, sys

ROOT = Path(__file__).resolve().parents[1]
errors = []

def load(rel):
    p = ROOT / rel
    if not p.exists():
        errors.append(f"Missing {rel}")
        return {}
    return json.loads(p.read_text(encoding="utf-8"))

adopt = load("phase2/sources/BRAIN_ENGINE_LIBRARY_ADOPTION_V1.json")
ai64 = load("registries/ai/AI_ONLY_RECORDS_64_APPROVED_V1.json")
eng = load("registries/asi/ENGINE_LIBRARY_75_APPROVED_V1.json")
engseg = load("registries/asi/ENGINE_SEGMENT_BINDINGS_75_APPROVED_V1.json")
containers = load("registries/asi/OPERATIONAL_CONTAINERS_161_240_APPROVED_V1.json")
spine = load("machine/wiring/BRAIN_ENGINE_OPERATIONAL_SPINE_V1.json")
generated = load("generated/registry_views/operational_subparameters_2593_3072_v1.json")
rels = load("generated/registry_views/brain_engine_relationships_compact_v1.json")
ai_bind = load("generated/registry_views/ai_only_64_phase2_bindings_v1.json")
eng_bind = load("generated/registry_views/engine_75_phase2_asi_node_bindings_v1.json")

if adopt.get("primary_operational_artifact", {}).get("declared_architecture", {}).get("master_containers") != 240:
    errors.append("Primary corpus must declare 240 master containers.")
if adopt.get("primary_operational_artifact", {}).get("declared_architecture", {}).get("operational_parameters") != 3072:
    errors.append("Primary corpus must declare 3072 operational parameters.")
if adopt.get("primary_operational_artifact", {}).get("declared_architecture", {}).get("canonical_engines") != 75:
    errors.append("Primary corpus must declare 75 canonical engines.")

ai_rows = ai64.get("records", [])
ai_ids = [r[0] for r in ai_rows]
expected_ai = [f"AI-NEW-{i:03d}" for i in range(1, 65)]
if ai_ids != expected_ai:
    errors.append("AI-only registry must contain AI-NEW-001..AI-NEW-064 exactly in order.")

eng_rows = eng.get("records", [])
eng_ids = [r[0] for r in eng_rows]
if len(eng_ids) != 75 or len(set(eng_ids)) != 75:
    errors.append(f"Engine registry must contain 75 unique engines; found {len(eng_ids)} / {len(set(eng_ids))} unique.")
seg_ids = [r[0] for r in engseg.get('records', [])]
if seg_ids != eng_ids:
    errors.append("Engine-Segment source binding registry must cover the 75 Engine IDs exactly in Engine Master order.")

crows = containers.get("records", [])
cids = [r[0] for r in crows]
expected_cids = [f"CON-{i:03d}" for i in range(161, 241)]
if cids != expected_cids:
    errors.append("Operational container registry must contain CON-161..CON-240 exactly in order.")
if any(r[2] not in {f"E0{i}" for i in range(1,9)} for r in crows):
    errors.append("Operational containers must use only E01..E08.")

els = spine.get("elements", [])
if len(els) != 8:
    errors.append("Operational spine must contain exactly 8 elements.")
covered = []
for e in els:
    covered.extend(e.get("container_ids", []))
if len(covered) != 80 or set(covered) != set(expected_cids):
    errors.append("Operational spine must cover CON-161..CON-240 exactly once.")

prows = generated.get("records", [])
pids = [r.get("parameter_id") for r in prows]
expected_pids = [f"SB-ASI-P{i:04d}" for i in range(2593, 3073)]
if pids != expected_pids:
    errors.append("Generated operational sub-parameters must contain SB-ASI-P2593..SB-ASI-P3072 exactly in order.")
for r in prows:
    cnum = int(r["container_id"].split("-")[-1])
    expected_start = 2593 + (cnum - 161) * 6
    expected_pid = f"SB-ASI-P{expected_start + int(r['local_number']) - 1:04d}"
    if r["parameter_id"] != expected_pid:
        errors.append(f"Parameter/container formula mismatch: {r['parameter_id']} -> {r['container_id']} local {r['local_number']}")
        break

# Exact source relationship preservation.
if rels.get('engine_container_relationship_count') != 400:
    errors.append('Brain Engine relationship registry must expand to exactly 400 engine-container relationships.')
if rels.get('parameter_engine_source_relationship_count') != 1440:
    errors.append('Brain Engine relationship registry must expand to exactly 1,440 parameter-engine/source relationships.')
if [r.get('container_id') for r in rels.get('containers', [])] != expected_cids:
    errors.append('Compact Brain Engine relationship registry must cover CON-161..CON-240 exactly in order.')
for row in rels.get('containers', []):
    if len(row.get('engine_ids', [])) != 5:
        errors.append(f"{row.get('container_id')} must have exactly five source Engine relations.")
        break
    if len(row.get('parameter_source_bundle', [])) != 3:
        errors.append(f"{row.get('container_id')} must have exactly three parameter/source bundle relations.")
        break

# Approved AI-only records remain native; mapping is additive.
aib = ai_bind.get('records', [])
if [r.get('ai_only_id') for r in aib] != expected_ai:
    errors.append('AI-only Phase-2 binding view must contain AI-NEW-001..AI-NEW-064 exactly in order.')
for row in aib:
    if row.get('unknown_source_cap_ids'):
        errors.append(f"{row.get('ai_only_id')} has unknown source AI-CAP lineage: {row.get('unknown_source_cap_ids')}")
        break
    if not row.get('source_ai_cap_ids'):
        errors.append(f"{row.get('ai_only_id')} lost its source AI-CAP lineage.")
        break

# Engine-to-Node binding is derived from real source container use; ten source engines are not used in the 400 map.
egb = eng_bind.get('records', [])
if [r.get('engine_id') for r in egb] != eng_ids:
    errors.append('Engine Phase-2 binding view must preserve all 75 Engine IDs in source order.')
expected_unbound = {
    'ENG-ARD-002','ENG-URR-001','ENG-SB-002','ENG-SB-003','ENG-SB-004',
    'ENG-WLD-006','ENG-SUP-005','ENG-SUP-006','ENG-SUP-007','ENG-SUP-008'
}
actual_unbound = {r.get('engine_id') for r in egb if r.get('binding_status') == 'UNBOUND_IN_SOURCE_400_RELATION_MAP'}
if actual_unbound != expected_unbound:
    errors.append(f"Source 400-map unbound Engine set changed. Expected={sorted(expected_unbound)} actual={sorted(actual_unbound)}")
for row in egb:
    if row.get('engine_id') not in expected_unbound and not row.get('phase2_asi_nodes_from_elements'):
        errors.append(f"Source-bound engine {row.get('engine_id')} has no derived ASI Node binding.")
        break

print("errors:", len(errors))
for e in errors:
    print("ERROR", e)
sys.exit(1 if errors else 0)
