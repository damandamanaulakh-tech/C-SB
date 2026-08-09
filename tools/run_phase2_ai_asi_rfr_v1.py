#!/usr/bin/env python3
from pathlib import Path
import json, sys, re

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'generated/tests'
OUT.mkdir(parents=True,exist_ok=True)
errors=[]

def load(rel):
    p=ROOT/rel
    if not p.exists():
        errors.append(f'Missing {rel}')
        return {}
    return json.loads(p.read_text(encoding='utf-8'))

ai_src=load('registries/ai/AI_ONLY_RECORDS_64_APPROVED_V1.json')
ai_map=load('generated/registry_views/ai_only_64_phase2_bindings_v1.json')
eng_src=load('registries/asi/ENGINE_LIBRARY_75_APPROVED_V1.json')
eng_seg=load('registries/asi/ENGINE_SEGMENT_BINDINGS_75_APPROVED_V1.json')
eng_map=load('generated/registry_views/engine_75_phase2_asi_node_bindings_v1.json')
exp_idx=load('registries/expansion/EXPANSION_CONTAINERS_081_160_INDEX_V1.json')
exp_cls=load('registries/expansion/EXPANSION_103_120_AI_ASI_CLASSIFICATION_V1.json')
nodes=load('registries/asi/asi_node_registry.json')
valid_nodes={n['asi_node_id'] for n in nodes.get('nodes',[])}

# -------- AI-NEW R-F-R --------
ai_src_by={r[0]:r for r in ai_src.get('records',[])}
ai_tests=[]
for b in ai_map.get('records',[]):
    rid=b['ai_only_id']; src=ai_src_by.get(rid); findings=[]; hard=[]
    # Pass 0: declared end / scope.
    pass0={
        'declared_end':'Source AI-only record has an auditable additive AI/ASI/Sequence/Node binding without source rewrite.',
        'scope':'one AI-NEW record and its declared AI-CAP lineage',
        'closure_scope':'mapping integrity only; not behavioral capability proof'
    }
    # Pass 1: reverse trace from binding to source.
    if src is None: hard.append('missing_source_record')
    if not b.get('source_ai_cap_ids'): hard.append('missing_source_ai_cap_lineage')
    if b.get('unknown_source_cap_ids'): hard.append('unknown_source_ai_cap_lineage')
    pass1={
        'source_record_present':src is not None,
        'source_ai_cap_ids':b.get('source_ai_cap_ids',[]),
        'unknown_source_cap_ids':b.get('unknown_source_cap_ids',[])
    }
    # Pass 2: forward reconstruction.
    bad_nodes=sorted(set(b.get('phase2_asi_nodes',[]))-valid_nodes)
    if bad_nodes: hard.append('unknown_asi_node')
    if not b.get('phase2_ai_segments') and not b.get('phase2_asi_segments'):
        findings.append('no_ai_or_asi_segment_mapping_yet')
    if b.get('governance_interface_expected_from_source_level') and not b.get('phase2_asi_segments'):
        findings.append('governance_expected_but_no_asi_segment_mapping')
    pass2={
        'ai_segments':b.get('phase2_ai_segments',[]),
        'asi_segments':b.get('phase2_asi_segments',[]),
        'asi_nodes':b.get('phase2_asi_nodes',[]),
        'primary_sequence_roles':b.get('primary_sequence_roles',[]),
        'bad_nodes':bad_nodes
    }
    # Pass 3: source-boundary audit.
    if src:
        if b.get('name') != src[1]: hard.append('source_name_rewritten')
        if b.get('source_structural_level') != src[2]: hard.append('source_structural_level_rewritten')
    pass3={
        'source_name_preserved':bool(src and b.get('name')==src[1]),
        'source_level_preserved':bool(src and b.get('source_structural_level')==src[2]),
        'mapping_authority':'additive_not_source_rewrite'
    }
    status='FAIL' if hard else ('PASS_WITH_FINDING' if findings else 'PASS')
    ai_tests.append({'id':rid,'status':status,'hard_failures':hard,'findings':findings,'pass0':pass0,'pass1':pass1,'pass2':pass2,'pass3':pass3})

# -------- Engine R-F-R --------
eng_src_by={r[0]:r for r in eng_src.get('records',[])}
seg_by={r[0]:r for r in eng_seg.get('records',[])}
expected_unbound={
    'ENG-ARD-002','ENG-URR-001','ENG-SB-002','ENG-SB-003','ENG-SB-004',
    'ENG-WLD-006','ENG-SUP-005','ENG-SUP-006','ENG-SUP-007','ENG-SUP-008'
}
engine_tests=[]
for b in eng_map.get('records',[]):
    eid=b['engine_id']; hard=[]; findings=[]
    source_bound=bool(b.get('source_operational_container_ids'))
    pass0={
        'declared_end':'Engine remains a bounded source operator and reaches ASI Nodes only through source container use + operational-spine mapping.',
        'scope':'one Engine Master record',
        'closure_scope':'routing integrity, not proof that the Engine implementation is correct'
    }
    if eid not in eng_src_by: hard.append('missing_engine_master_record')
    if eid not in seg_by: hard.append('missing_engine_segment_source_record')
    pass1={'source_engine_present':eid in eng_src_by,'source_segment_record_present':eid in seg_by,'source_containers':b.get('source_operational_container_ids',[])}
    bad_nodes=sorted(set(b.get('phase2_asi_nodes_from_elements',[]))-valid_nodes)
    if bad_nodes: hard.append('unknown_asi_node')
    if source_bound and not b.get('phase2_asi_nodes_from_elements'): hard.append('source_bound_engine_has_no_node_route')
    if not source_bound:
        if eid not in expected_unbound: hard.append('unexpected_unbound_engine')
        else: findings.append('source_engine_not_used_in_400_engine_container_map')
    pass2={'element_codes':b.get('source_operational_element_codes',[]),'asi_nodes':b.get('phase2_asi_nodes_from_elements',[]),'bad_nodes':bad_nodes,'source_usage_count':b.get('source_usage_count')}
    if b.get('binding_status')=='UNBOUND_IN_SOURCE_400_RELATION_MAP' and source_bound: hard.append('binding_status_conflicts_with_source_use')
    if b.get('binding_status')!='UNBOUND_IN_SOURCE_400_RELATION_MAP' and not source_bound: hard.append('unbound_source_use_not_marked')
    pass3={'engine_identity_preserved':eid in eng_src_by,'boundedness':'No Node binding inferred directly from name; mapping comes from source container use','gap_preserved':(eid in expected_unbound)==(not source_bound)}
    status='FAIL' if hard else ('GAP_EXPECTED' if findings else 'PASS')
    engine_tests.append({'id':eid,'status':status,'hard_failures':hard,'findings':findings,'pass0':pass0,'pass1':pass1,'pass2':pass2,'pass3':pass3})

# -------- Named CROSS CON-103..120 R-F-R --------
idx_by={r[0]:r for r in exp_idx.get('records',[])}
exp_tests=[]
for b in exp_cls.get('records',[]):
    cid=b['container_id']; src=idx_by.get(cid); hard=[]; findings=[]
    pass0={'declared_end':'Named CROSS expansion container has a source-preserving AI/ASI classification suitable for later runtime testing.','scope':cid,'closure_scope':'classification integrity only'}
    if not src: hard.append('missing_source_container')
    if src and src[2] != b.get('name'): hard.append('source_name_rewritten')
    pass1={'source_present':bool(src),'source_name':src[2] if src else None,'source_ai_cap_links':src[3] if src else None}
    bad_nodes=sorted(set(b.get('asi_nodes',[]))-valid_nodes)
    if bad_nodes: hard.append('unknown_asi_node')
    if not b.get('ai_segments') and not b.get('asi_segments'): hard.append('empty_domain_mapping')
    pass2={'domain_role':b.get('domain_role'),'ai_segments':b.get('ai_segments',[]),'asi_segments':b.get('asi_segments',[]),'asi_nodes':b.get('asi_nodes',[]),'bad_nodes':bad_nodes}
    pass3={'source_identity_preserved':bool(src and src[2]==b.get('name')),'mapping_is_additive':True,'placeholder_boundary_preserved':int(cid.split('-')[-1])<121}
    status='FAIL' if hard else ('PASS_WITH_FINDING' if findings else 'PASS')
    exp_tests.append({'id':cid,'status':status,'hard_failures':hard,'findings':findings,'pass0':pass0,'pass1':pass1,'pass2':pass2,'pass3':pass3})

report={
    'report_id':'P2-AI-ASI-STRUCTURAL-RFR-V1',
    'status':'FAIL' if errors or any(t['status']=='FAIL' for t in ai_tests+engine_tests+exp_tests) else 'PASS_WITH_EXPECTED_GAPS',
    'scope_note':'These are structural R-F-R tests of source custody and routing. They do not prove cognitive quality, external truth or implementation correctness.',
    'summary':{
        'ai_only':{'total':len(ai_tests),'pass':sum(t['status']=='PASS' for t in ai_tests),'pass_with_finding':sum(t['status']=='PASS_WITH_FINDING' for t in ai_tests),'fail':sum(t['status']=='FAIL' for t in ai_tests)},
        'engines':{'total':len(engine_tests),'pass':sum(t['status']=='PASS' for t in engine_tests),'expected_gap':sum(t['status']=='GAP_EXPECTED' for t in engine_tests),'fail':sum(t['status']=='FAIL' for t in engine_tests)},
        'cross_expansion':{'total':len(exp_tests),'pass':sum(t['status']=='PASS' for t in exp_tests),'pass_with_finding':sum(t['status']=='PASS_WITH_FINDING' for t in exp_tests),'fail':sum(t['status']=='FAIL' for t in exp_tests)}
    },
    'ai_only_tests':ai_tests,
    'engine_tests':engine_tests,
    'cross_expansion_tests':exp_tests,
    'loader_errors':errors
}
(OUT/'P2_AI_ASI_STRUCTURAL_RFR_V1.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report['summary']))
if report['status']=='FAIL':
    sys.exit(1)
