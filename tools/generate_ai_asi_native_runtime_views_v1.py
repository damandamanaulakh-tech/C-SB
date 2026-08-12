#!/usr/bin/env python3
from pathlib import Path
import json
from collections import defaultdict, Counter

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'generated/registry_views'
OUT.mkdir(parents=True,exist_ok=True)

def load(rel):
    return json.loads((ROOT/rel).read_text(encoding='utf-8'))

dec=load('generated/registry_views/ai_new_64_structural_decomposition_v1.json')
ai_rubric=load('registries/ai/AI_RUBRIC_V0.json')
asi_rubric=load('registries/asi/ASI_RUBRIC_V0.json')

ai_defs={r['ai_segment_id']:r for r in ai_rubric['segments']}
asi_defs={r['asi_segment_id']:r for r in asi_rubric['segments']}

ai_records=[]
for r in dec['records']:
    ai_records.append({
        'ai_only_id':r['ai_only_id'],
        'source_name':r['source_name'],
        'source_structural_level':r['source_structural_level'],
        'runtime_form':r['runtime_form'],
        'atomicity':r['atomicity'],
        'composite_components':r['composite_components'],
        'mechanism_ownership':r['mechanism_ownership'],
        'ai_segments':[{'ai_segment_id':sid,'name':ai_defs[sid]['name']} for sid in r['phase2_ai_segments']],
        'primary_sequence_roles':r['primary_sequence_roles'],
        'secondary_sequence_roles':r['secondary_sequence_roles'],
        'state_ownership_candidates':r['state_ownership_candidates'],
        'memory_read_candidates':r['memory_read_candidates'],
        'memory_write_candidates':r['memory_write_candidates'],
        'activation_contract':r['activation_contract'],
        'closure_contract':r['closure_contract'],
        'engine_binding_status':r['engine_binding_status'],
        'direct_engine_ids':r['direct_engine_ids'],
        'governance_interface_refs':r['phase2_asi_segments'],
        'asi_node_refs':r['phase2_asi_nodes'],
        'source_record_sha256':r['source_record_sha256'],
    })

ai_payload={
    'view_id':'AI-NATIVE-RUNTIME-VIEW-V1',
    'status':'SOURCE_PRESERVING_RUNTIME_VIEW_NOT_NEW_SOURCE_AUTHORITY',
    'source_registry':'registries/ai/AI_ONLY_RECORDS_64_APPROVED_V1.json',
    'semantic_rubric':'registries/ai/AI_RUBRIC_V0.json',
    'structural_decomposition':'generated/registry_views/ai_new_64_structural_decomposition_v1.json',
    'record_count':len(ai_records),
    'rule':'AI-NEW source identity stays authoritative. This view assembles implementable runtime metadata and AI semantic routing; ASI refs remain governance interfaces, not AI ownership.',
    'records':ai_records,
}
(OUT/'ai_native_runtime_view_v1.json').write_text(json.dumps(ai_payload,indent=2),encoding='utf-8')

interfaces=defaultdict(list)
for r in dec['records']:
    for sid in r['phase2_asi_segments']:
        interfaces[sid].append({
            'ai_only_id':r['ai_only_id'],
            'source_name':r['source_name'],
            'runtime_form':r['runtime_form'],
            'mechanism_ownership':r['mechanism_ownership'],
            'asi_node_refs':r['phase2_asi_nodes'],
            'authority_reason':'Governance interface derived from existing Phase-2 AI-CAP lineage/patch binding; it does not convert the AI-NEW record into an ASI source record.'
        })

asi_segments=[]
for sid in [f'ASI-{i:02d}' for i in range(1,21)]:
    d=asi_defs[sid]
    refs=interfaces.get(sid,[])
    asi_segments.append({
        'asi_segment_id':sid,
        'name':d['name'],
        'purpose':d['purpose'],
        'ai_new_interface_count':len(refs),
        'ai_new_interfaces':refs,
    })

asi_payload={
    'view_id':'ASI-GOVERNANCE-INTERFACE-VIEW-FROM-AI-NEW-V1',
    'status':'ASI_SOURCE_PLUS_DERIVED_AI_INTERFACE_VIEW',
    'asi_source_registry':'registries/asi/ASI_RUBRIC_V0.json',
    'ai_interface_source':'generated/registry_views/ai_new_64_structural_decomposition_v1.json',
    'rule':'ASI segment definitions come only from ASI_RUBRIC_V0. AI-NEW records appear only as governed interface references and never become ASI source definitions.',
    'segment_count':20,
    'segments':asi_segments,
    'summary':{
        'segments_with_ai_new_interfaces':sum(1 for s in asi_segments if s['ai_new_interface_count']),
        'segments_without_ai_new_interfaces':sum(1 for s in asi_segments if not s['ai_new_interface_count']),
        'total_ai_new_interface_edges':sum(s['ai_new_interface_count'] for s in asi_segments),
        'per_segment_counts':{s['asi_segment_id']:s['ai_new_interface_count'] for s in asi_segments}
    }
}
(OUT/'asi_governance_interface_view_from_ai_new_v1.json').write_text(json.dumps(asi_payload,indent=2),encoding='utf-8')
print(json.dumps({'ai_records':len(ai_records),'asi_interface_edges':asi_payload['summary']['total_ai_new_interface_edges'],'asi_segments_with_interfaces':asi_payload['summary']['segments_with_ai_new_interfaces']},sort_keys=True))
