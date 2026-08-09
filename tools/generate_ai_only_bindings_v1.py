#!/usr/bin/env python3
from pathlib import Path
import json, re
from collections import defaultdict

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'generated/registry_views'
OUT.mkdir(parents=True, exist_ok=True)

def load(rel):
    return json.loads((ROOT / rel).read_text(encoding='utf-8'))

src = load('registries/ai/AI_ONLY_RECORDS_64_APPROVED_V1.json')
ai_cross = load('registries/ai/AI_CONTAINER_CANDIDATES_V0.json')
asi_cross = load('registries/asi/ASI_CONTAINER_CANDIDATES_FROM_AI_SOURCES_V0.json')
cap_view = load('generated/registry_views/ai_native_candidate_registry_v0.json')
gov_patch = load('registries/ai/AI_ONLY_GOVERNANCE_BINDING_PATCH_V1.json')
patch_by_id = {r['ai_only_id']: r for r in gov_patch.get('records', [])}

cap_nodes = {}
cap_primary_roles = {}
cap_secondary_roles = {}
cap_state = {}
cap_mem_read = {}
cap_mem_write = {}
for row in cap_view.get('candidates', []):
    sid = row.get('source_id')
    if not sid: continue
    cap_nodes[sid] = row.get('primary_asi_nodes', [])
    cap_primary_roles[sid] = row.get('primary_sequence_roles', [])
    cap_secondary_roles[sid] = row.get('secondary_sequence_roles', [])
    cap_state[sid] = row.get('state_owned_by', [])
    cap_mem_read[sid] = row.get('memory_read', [])
    cap_mem_write[sid] = row.get('memory_write', [])

cap_ai_containers = defaultdict(set)
cap_ai_segments = defaultdict(set)
cap_asi_interfaces = defaultdict(set)
for c in ai_cross.get('containers', []):
    refs = list(c.get('source_ids', [])) + list(c.get('source_parent_ids', []))
    for ref in refs:
        if re.fullmatch(r'AI-CAP-\d{3}', ref):
            cap_ai_containers[ref].add(c['container_id'])
            cap_ai_segments[ref].update(c.get('parent_ai_segments', []))
            cap_asi_interfaces[ref].update(c.get('asi_interface', []))

cap_asi_containers = defaultdict(set)
cap_asi_segments = defaultdict(set)
for c in asi_cross.get('containers', []):
    refs = list(c.get('source_ids', [])) + list(c.get('source_parent_ids', []))
    for ref in refs:
        if re.fullmatch(r'AI-CAP-\d{3}', ref):
            cap_asi_containers[ref].add(c['container_id'])
            cap_asi_segments[ref].update(c.get('parent_asi_segments', []))

bindings=[]
for rid, name, structural_level, lineage in src.get('records', []):
    caps = re.findall(r'AI-CAP-\d{3}', lineage)
    ai_cons=set(); ai_segs=set(); asi_cons=set(); asi_segs=set(); nodes=set()
    proles=set(); sroles=set(); states=set(); mread=set(); mwrite=set()
    unknown_caps=[]
    for cap in caps:
        if cap not in cap_nodes:
            unknown_caps.append(cap)
        ai_cons.update(cap_ai_containers.get(cap, ()))
        ai_segs.update(cap_ai_segments.get(cap, ()))
        asi_cons.update(cap_asi_containers.get(cap, ()))
        asi_segs.update(cap_asi_segments.get(cap, ()))
        asi_segs.update(cap_asi_interfaces.get(cap, ()))
        nodes.update(cap_nodes.get(cap, ()))
        proles.update(cap_primary_roles.get(cap, ()))
        sroles.update(cap_secondary_roles.get(cap, ()))
        states.update(cap_state.get(cap, ()))
        mread.update(cap_mem_read.get(cap, ()))
        mwrite.update(cap_mem_write.get(cap, ()))

    patch = patch_by_id.get(rid)
    patch_applied = False
    patch_reason = None
    if patch:
        if patch.get('source_name') != name:
            raise ValueError(f"Governance patch source name mismatch for {rid}")
        if patch.get('source_level') != structural_level:
            raise ValueError(f"Governance patch source level mismatch for {rid}")
        asi_segs.update(patch.get('add_asi_segments', []))
        nodes.update(patch.get('add_asi_nodes', []))
        patch_applied = True
        patch_reason = patch.get('reason')

    governance_hint = structural_level in {
        'Control parameter','Universal filter','Evidence-control parameter','Master control parameter','Operating state'
    }
    binding_status = 'GAP_REVIEW_REQUIRED'
    if caps and not unknown_caps:
        binding_status = 'SOURCE_LINEAGE_PLUS_GOVERNANCE_PATCH' if patch_applied else 'SOURCE_LINEAGE_DERIVED_CROSSWALK'

    bindings.append({
        'ai_only_id': rid,
        'name': name,
        'source_structural_level': structural_level,
        'source_ai_cap_ids': caps,
        'phase2_ai_segments': sorted(ai_segs),
        'phase2_ai_container_crosswalk': sorted(ai_cons),
        'phase2_asi_segments': sorted(asi_segs),
        'phase2_asi_container_crosswalk': sorted(asi_cons),
        'phase2_asi_nodes': sorted(nodes),
        'primary_sequence_roles': sorted(proles),
        'secondary_sequence_roles': sorted(sroles),
        'state_ownership_candidates': sorted(states),
        'memory_read_candidates': sorted(mread),
        'memory_write_candidates': sorted(mwrite),
        'governance_interface_expected_from_source_level': governance_hint,
        'governance_patch_applied': patch_applied,
        'governance_patch_reason': patch_reason,
        'binding_status': binding_status,
        'unknown_source_cap_ids': unknown_caps,
        'authority_note': 'AI-NEW identity/name/level are approved source records. AI/ASI segments, candidate containers, Sequence roles and ASI Nodes are additive Phase-2 mappings. Where source AI-CAP lineage did not expose required governance for a source Control parameter/Universal filter, AI_ONLY_GOVERNANCE_BINDING_PATCH_V1 supplies the missing ASI layer without rewriting the source record.'
    })

assert len(bindings) == 64
assert [b['ai_only_id'] for b in bindings] == [f'AI-NEW-{i:03d}' for i in range(1,65)]
assert set(patch_by_id) == {b['ai_only_id'] for b in bindings if b['governance_patch_applied']}

payload={
    'registry_id':'AI-ONLY-64-PHASE2-BINDINGS-V1',
    'status':'GENERATED_ADDITIVE_MAPPING_NOT_SOURCE_REWRITE',
    'source_registry':'registries/ai/AI_ONLY_RECORDS_64_APPROVED_V1.json',
    'mapping_sources':[
        'registries/ai/AI_CONTAINER_CANDIDATES_V0.json',
        'registries/asi/ASI_CONTAINER_CANDIDATES_FROM_AI_SOURCES_V0.json',
        'generated/registry_views/ai_native_candidate_registry_v0.json',
        'registries/ai/AI_ONLY_GOVERNANCE_BINDING_PATCH_V1.json'
    ],
    'record_count':64,
    'rule':'Approved AI-NEW records stay native. Phase-2 AI/ASI/Sequence/Node bindings are derived through source AI-CAP lineage; explicit additive governance patches may resolve R-F-R mapping gaps when the source record is itself a control/filter and lineage-only mapping omits ASI authority.',
    'records':bindings
}
(OUT/'ai_only_64_phase2_bindings_v1.json').write_text(json.dumps(payload,indent=2),encoding='utf-8')
print('Generated AI-NEW bindings:',len(bindings),'gaps:',sum(b['binding_status']=='GAP_REVIEW_REQUIRED' for b in bindings),'governance_patches:',sum(b['governance_patch_applied'] for b in bindings))
