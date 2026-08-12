#!/usr/bin/env python3
from pathlib import Path
import json
from collections import Counter

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'generated/registry_views'
OUT.mkdir(parents=True,exist_ok=True)

def load(rel):
    return json.loads((ROOT/rel).read_text(encoding='utf-8'))

dec=load('generated/registry_views/ai_new_64_structural_decomposition_v1.json')
patch=load('registries/ai/AI_NEW_64_MINIMAL_PRIMARY_ROUTE_PATCH_V2.json')
ai=load('registries/ai/AI_RUBRIC_V0.json')
asi=load('registries/asi/ASI_RUBRIC_V0.json')
nodes=load('registries/asi/asi_node_registry.json')

patch_by={r['ai_only_id']:r for r in patch['records']}
ai_ids={r['ai_segment_id'] for r in ai['segments']}
asi_ids={r['asi_segment_id'] for r in asi['segments']}
node_ids={r['asi_node_id'] for r in nodes['nodes']}

records=[]
for r in dec['records']:
    rid=r['ai_only_id']
    p=patch_by.get(rid)
    if p:
        unknown_ai=set(p['primary_ai_segments'])-ai_ids
        unknown_asi=set(p['primary_asi_segments'])-asi_ids
        unknown_nodes=set(p['primary_service_nodes'])-node_ids
        if unknown_ai or unknown_asi or unknown_nodes:
            raise ValueError(f'{rid}: invalid patch refs ai={unknown_ai} asi={unknown_asi} nodes={unknown_nodes}')
        primary_ai=p['primary_ai_segments']
        primary_asi=p['primary_asi_segments']
        service_nodes=p['primary_service_nodes']
        runtime_anchor=p['runtime_anchor']
        route_status='NARROWED_PRIMARY_ROUTE_V2'
        route_reason=p['reason']
    else:
        primary_ai=r['phase2_ai_segments']
        primary_asi=r['phase2_asi_segments']
        service_nodes=r['phase2_asi_nodes']
        runtime_anchor='INHERITED_V1_RUNTIME_ROUTE'
        route_status='INHERITED_V1_ACCEPTABLE_BREADTH'
        route_reason='V1 route did not exceed the orphan/overlap breadth-review thresholds; preserved unchanged.'
    records.append({
        'ai_only_id':rid,
        'source_name':r['source_name'],
        'source_structural_level':r['source_structural_level'],
        'runtime_form':r['runtime_form'],
        'mechanism_ownership':r['mechanism_ownership'],
        'route_status':route_status,
        'runtime_anchor':runtime_anchor,
        'route_reason':route_reason,
        'primary_ai_segments':primary_ai,
        'primary_asi_segments':primary_asi,
        'primary_service_nodes':service_nodes,
        'router_node':patch['router_node'],
        'meta_governor_node':patch['meta_governor_node'] if primary_asi else None,
        'primary_sequence_roles_inherited':r['primary_sequence_roles'],
        'secondary_sequence_roles_inherited':r['secondary_sequence_roles'],
        'state_ownership_candidates':r['state_ownership_candidates'],
        'memory_read_candidates':r['memory_read_candidates'],
        'memory_write_candidates':r['memory_write_candidates'],
        'activation_contract':r['activation_contract'],
        'closure_contract':r['closure_contract'],
        'engine_binding_status':r['engine_binding_status'],
        'direct_engine_ids':r['direct_engine_ids'],
        'secondary_inherited_ai_segments':r['phase2_ai_segments'] if p else [],
        'secondary_inherited_asi_segments':r['phase2_asi_segments'] if p else [],
        'secondary_inherited_service_nodes':r['phase2_asi_nodes'] if p else [],
        'source_record_sha256':r['source_record_sha256'],
    })

patched=[r for r in records if r['route_status']=='NARROWED_PRIMARY_ROUTE_V2']
summary={
    'record_count':len(records),
    'narrowed_record_count':len(patched),
    'inherited_record_count':len(records)-len(patched),
    'patched_primary_ai_segment_edges':sum(len(r['primary_ai_segments']) for r in patched),
    'patched_primary_asi_segment_edges':sum(len(r['primary_asi_segments']) for r in patched),
    'patched_primary_service_node_edges':sum(len(r['primary_service_nodes']) for r in patched),
    'patched_inherited_ai_segment_edges_retained':sum(len(r['secondary_inherited_ai_segments']) for r in patched),
    'patched_inherited_asi_segment_edges_retained':sum(len(r['secondary_inherited_asi_segments']) for r in patched),
    'patched_inherited_service_node_edges_retained':sum(len(r['secondary_inherited_service_nodes']) for r in patched),
    'engine_binding_counts':dict(Counter(r['engine_binding_status'] for r in records))
}
payload={
    'view_id':'AI-NEW-64-RUNTIME-ROUTES-V2',
    'status':'PRIMARY_ROUTE_BREADTH_REPAIRED_SECONDARY_LINEAGE_PRESERVED',
    'source_decomposition':'generated/registry_views/ai_new_64_structural_decomposition_v1.json',
    'repair_patch':'registries/ai/AI_NEW_64_MINIMAL_PRIMARY_ROUTE_PATCH_V2.json',
    'rule':'Primary runtime routing is narrow. V1 AI-CAP-derived breadth remains secondary inherited context and is not deleted. Source AI-NEW identity is unchanged.',
    'summary':summary,
    'records':records,
}
(OUT/'ai_new_64_runtime_routes_v2.json').write_text(json.dumps(payload,indent=2),encoding='utf-8')
print(json.dumps(summary,sort_keys=True))
