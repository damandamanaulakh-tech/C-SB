#!/usr/bin/env python3
from pathlib import Path
import json, sys

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'generated/tests'
OUT.mkdir(parents=True,exist_ok=True)
errors=[]
findings=[]

def load(rel):
    p=ROOT/rel
    if not p.exists():
        errors.append(f'missing:{rel}')
        return {}
    return json.loads(p.read_text(encoding='utf-8'))

attack=load('generated/tests/P2_AI_NEW_64_ORPHAN_OVERLAP_ATTACK_V1.json')
dec=load('generated/registry_views/ai_new_64_structural_decomposition_v1.json')
routes=load('generated/registry_views/ai_new_64_runtime_routes_v2.json')
patch=load('registries/ai/AI_NEW_64_MINIMAL_PRIMARY_ROUTE_PATCH_V2.json')

attack_ids={r['ai_only_id'] for r in attack.get('pass2',{}).get('over_broad_mapping_review',[])}
patch_ids={r['ai_only_id'] for r in patch.get('records',[])}
route_by={r['ai_only_id']:r for r in routes.get('records',[])}
dec_by={r['ai_only_id']:r for r in dec.get('records',[])}
expected={f'AI-NEW-{i:03d}' for i in range(1,65)}

if attack_ids != patch_ids:
    errors.append(f'patch set differs from attack finding set attack={sorted(attack_ids)} patch={sorted(patch_ids)}')
if set(route_by)!=expected: errors.append('runtime route view does not preserve exact 64 IDs')
if set(dec_by)!=expected: errors.append('decomposition does not preserve exact 64 IDs')

patched=[]
for rid in sorted(expected):
    r=route_by[rid]
    d=dec_by[rid]
    if r['source_name']!=d['source_name'] or r['source_structural_level']!=d['source_structural_level'] or r['source_record_sha256']!=d['source_record_sha256']:
        errors.append(f'{rid}:source identity drift')
    if rid in patch_ids:
        patched.append(r)
        if r['route_status']!='NARROWED_PRIMARY_ROUTE_V2': errors.append(f'{rid}:not marked narrowed')
        if len(r['primary_ai_segments'])>2: errors.append(f'{rid}:primary AI breadth >2')
        if len(r['primary_asi_segments'])>2: errors.append(f'{rid}:primary ASI breadth >2')
        if len(r['primary_service_nodes'])>3: errors.append(f'{rid}:primary service-node breadth >3')
        if not r['secondary_inherited_ai_segments'] and d['phase2_ai_segments']:
            errors.append(f'{rid}:broad AI lineage not retained')
        if r['secondary_inherited_ai_segments']!=d['phase2_ai_segments']:
            errors.append(f'{rid}:secondary AI lineage changed')
        if r['secondary_inherited_asi_segments']!=d['phase2_asi_segments']:
            errors.append(f'{rid}:secondary ASI lineage changed')
        if r['secondary_inherited_service_nodes']!=d['phase2_asi_nodes']:
            errors.append(f'{rid}:secondary node lineage changed')
    else:
        if r['route_status']!='INHERITED_V1_ACCEPTABLE_BREADTH': errors.append(f'{rid}:unflagged record changed route status')
        if r['primary_ai_segments']!=d['phase2_ai_segments'] or r['primary_asi_segments']!=d['phase2_asi_segments'] or r['primary_service_nodes']!=d['phase2_asi_nodes']:
            errors.append(f'{rid}:unflagged route changed')
    if r['engine_binding_status']!=d['engine_binding_status'] or r['direct_engine_ids']!=d['direct_engine_ids']:
        errors.append(f'{rid}:Engine gap/binding changed during breadth repair')

special={rid:route_by[rid] for rid in ['AI-NEW-014','AI-NEW-021','AI-NEW-041','AI-NEW-061']}
if special['AI-NEW-014']['runtime_anchor']!='REPAIR_SUB_SEQUENCE_POLICY': errors.append('AI-NEW-014 lost repair Sub-Sequence anchor')
if 'WITHOUT_ACTION_AUTHORITY' not in special['AI-NEW-021']['runtime_anchor']: errors.append('AI-NEW-021 authority boundary lost')
if special['AI-NEW-041']['runtime_anchor']!='COMPLETION_CLAIM_ACCEPTANCE_EVIDENCE': errors.append('AI-NEW-041 completion verification anchor drift')
if special['AI-NEW-061']['runtime_anchor']!='CORRECTION_WRITEBACK_PROPAGATION': errors.append('AI-NEW-061 correction writeback anchor drift')

before_ai=sum(len(dec_by[rid]['phase2_ai_segments']) for rid in patch_ids)
before_asi=sum(len(dec_by[rid]['phase2_asi_segments']) for rid in patch_ids)
before_nodes=sum(len(dec_by[rid]['phase2_asi_nodes']) for rid in patch_ids)
after_ai=sum(len(route_by[rid]['primary_ai_segments']) for rid in patch_ids)
after_asi=sum(len(route_by[rid]['primary_asi_segments']) for rid in patch_ids)
after_nodes=sum(len(route_by[rid]['primary_service_nodes']) for rid in patch_ids)
if after_ai>=before_ai: errors.append('AI primary route breadth was not reduced')
if after_asi>=before_asi: errors.append('ASI primary route breadth was not reduced')
if after_nodes>=before_nodes: errors.append('service-node primary route breadth was not reduced')

engine_open=sum(1 for r in route_by.values() if r['engine_binding_status']=='ENGINE_BINDING_OPEN_NO_EXACT_SOURCE_RELATION')
if engine_open!=64: errors.append(f'Engine source gap count changed:{engine_open}')

invariants={
    'EXACT_17_BREADTH_FINDINGS_REPAIRED':attack_ids==patch_ids=={r['ai_only_id'] for r in patched},
    'SOURCE_IDENTITIES_PRESERVED':not any('source identity drift' in e for e in errors),
    'PRIMARY_ROUTE_NARROWED':after_ai<before_ai and after_asi<before_asi and after_nodes<before_nodes,
    'SECONDARY_LINEAGE_PRESERVED':not any('lineage' in e and ('not retained' in e or 'changed' in e) for e in errors),
    'UNFLAGGED_47_UNCHANGED':not any('unflagged' in e for e in errors),
    'ENGINE_GAPS_PRESERVED':engine_open==64,
    'RETRY_IS_SUB_SEQUENCE_POLICY':special['AI-NEW-014']['runtime_anchor']=='REPAIR_SUB_SEQUENCE_POLICY',
    'SAFETY_ROUTE_HAS_NO_ACTION_AUTHORITY': 'WITHOUT_ACTION_AUTHORITY' in special['AI-NEW-021']['runtime_anchor'],
    'CORRECTION_IS_EXPLICIT_WRITEBACK':special['AI-NEW-061']['runtime_anchor']=='CORRECTION_WRITEBACK_PROPAGATION'
}
for k,v in invariants.items():
    if not v: errors.append(f'invariant failed:{k}')

report={
    'report_id':'P2-AI-NEW-64-BREADTH-REPAIR-RFR-V2',
    'status':'FAIL' if errors else 'PASS',
    'scope_note':'Repairs only the 17 over-broad primary runtime routes found in V1. Broad AI-CAP-derived mappings remain secondary provenance; source identities and Engine gaps remain unchanged.',
    'pass0':{
        'declared_end':'Exactly the 17 mapping-breadth findings have narrow executable primary routes without source or lineage loss.',
        'repair_scope':'17 records only'
    },
    'pass1':{
        'finding_ids':sorted(attack_ids),
        'patch_ids':sorted(patch_ids),
        'source_record_count':len(route_by)
    },
    'pass2':{
        'breadth_before':{'ai_segment_edges':before_ai,'asi_segment_edges':before_asi,'service_node_edges':before_nodes},
        'breadth_after_primary':{'ai_segment_edges':after_ai,'asi_segment_edges':after_asi,'service_node_edges':after_nodes},
        'reduction':{'ai_segment_edges':before_ai-after_ai,'asi_segment_edges':before_asi-after_asi,'service_node_edges':before_nodes-after_nodes},
        'engine_source_gaps':engine_open
    },
    'pass3':{
        'invariant_checks':invariants,
        'source_rewrite_performed':False,
        'secondary_lineage_deleted':False,
        'engine_force_fit_performed':False,
        'closed_sequence_reopen_used':False
    },
    'errors':errors,
    'findings':findings
}
(OUT/'P2_AI_NEW_64_BREADTH_REPAIR_RFR_V2.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(report['status'],'errors',len(errors),'reduction',report['pass2']['reduction'])
sys.exit(1 if errors else 0)
