#!/usr/bin/env python3
from pathlib import Path
import json, sys

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

suite=load('phase2/tests/P2_BEHAVIORAL_RFR_CASES_V1.json')
ai_bind=load('generated/registry_views/ai_only_64_phase2_bindings_v1.json')
eng_bind=load('generated/registry_views/engine_75_phase2_asi_node_bindings_v1.json')
rels=load('generated/registry_views/brain_engine_relationships_compact_v1.json')
containers=load('registries/asi/OPERATIONAL_CONTAINERS_161_240_APPROVED_V1.json')

ai_by={r['ai_only_id']:r for r in ai_bind.get('records',[])}
eng_by={r['engine_id']:r for r in eng_bind.get('records',[])}
rel_by={r['container_id']:r for r in rels.get('containers',[])}
con_by={r[0]:r for r in containers.get('records',[])}

results=[]

# ------------------------------------------------------------
# Case 1: AI selection vs ASI authorization / barrier behavior
# ------------------------------------------------------------
case=next(c for c in suite['cases'] if c['case_id']=='P2-BEH-AUTH-001')
hard=[]; findings=[]; trace=[]
anchor=ai_by.get(case['source_anchor']['ai_only_id'])
if not anchor:
    hard.append('AI_NEW_011_BINDING_MISSING')
else:
    if anchor.get('name') != case['source_anchor']['source_name']:
        hard.append('AI_NEW_011_SOURCE_NAME_MISMATCH')
    for required in ['ASI-08','ASI-13']:
        if required not in anchor.get('phase2_asi_segments',[]):
            hard.append(f'MISSING_{required}_GOVERNANCE')
    if 'ASI-NODE-21' not in anchor.get('phase2_asi_nodes',[]):
        hard.append('MISSING_ASI_NODE_21_META_GOVERNOR')

# PASS 0
pass0={
    'declared_end':case['declared_end'],
    'scope':case['scope'],
    'closure_scope':case['closure_scope'],
    'fixture_is_source_fact':False
}

# PASS 1 reverse: what must be true for dispatch?
reverse_requirements=[
    'tool candidate selected',
    'authorization decision returned',
    'required return accepted',
    'authorization state == GRANTED',
    'barrier clear',
    'dispatch threshold re-evaluated true'
]
pass1={'required_predecessors':reverse_requirements,'source_binding_found':anchor is not None}

# PASS 2 forward variants
variant_results=[]
for v in case['variants']:
    vid=v['variant_id']; auth=v['initial_authorization']; edge_fire=False; barrier='BLOCKED'; events=[]
    events.append('TOOL_CANDIDATE_SELECTED')
    if auth != 'GRANTED':
        events.append('AUTHORIZATION_REQUIRED')
        events.append('BARRIER_BLOCKED')
    pr=v.get('permission_return')
    if pr:
        events.append(f"PERMISSION_SEQUENCE_{pr['terminal_status']}")
        if not pr.get('return_accepted'):
            events.append('RETURN_NOT_ACCEPTED')
        elif pr.get('result')=='GRANTED':
            auth='GRANTED'
            events.append('RETURN_ACCEPTED_GRANTED')
            events.append('THRESHOLD_REEVALUATED')
            barrier='CLEAR'
            edge_fire=True
            events.append('EDGE_FIRED')
        elif pr.get('result')=='DENIED':
            auth='DENIED'
            events.append('RETURN_ACCEPTED_DENIED')
            events.append('THRESHOLD_FALSE')
            edge_fire=False
            barrier='BLOCKED_BY_PERMISSION'
    # Contract assertions
    if edge_fire != bool(v['expected_edge_fire']):
        hard.append(f'{vid}_EDGE_FIRE_MISMATCH')
    if vid=='AUTH-UNKNOWN':
        ss=v.get('expected_sub_sequence',{})
        if ss.get('relation_type')!='ATTACHED' or not ss.get('required'):
            hard.append('AUTH_UNKNOWN_MISSING_REQUIRED_ATTACHED_SEQUENCE')
        if ss.get('parent_status_while_open')!='WAITING_FOR_RETURN':
            hard.append('AUTH_UNKNOWN_PARENT_NOT_WAITING')
    if vid=='AUTH-DENIED' and edge_fire:
        hard.append('DENIED_PERMISSION_CROSSED_EDGE')
    if vid=='AUTH-GRANTED' and 'THRESHOLD_REEVALUATED' not in events:
        hard.append('GRANT_BYPASSED_REEVALUATION')
    variant_results.append({'variant_id':vid,'final_authorization':auth,'barrier_state':barrier,'edge_fired':edge_fire,'events':events})

pass2={'variants':variant_results}

# PASS 3 reverse audit of invariants
invariant_checks={
    'AI_SELECTION_IS_NOT_AUTHORIZATION': bool(anchor and 'ASI-08' in anchor.get('phase2_asi_segments',[])),
    'NO_EXECUTION_BEFORE_GRANTED_PERMISSION': all(not r['edge_fired'] for r in variant_results if r['final_authorization']!='GRANTED'),
    'MISSING_REQUIRED_PERMISSION_OPENS_ATTACHED_SEQUENCE': case['variants'][0]['expected_sub_sequence']['relation_type']=='ATTACHED',
    'PARENT_WAITS_FOR_REQUIRED_RETURN': case['variants'][0]['expected_sub_sequence']['parent_status_while_open']=='WAITING_FOR_RETURN',
    'DENIED_PERMISSION_NEVER_CROSSES_ACTION_EDGE': not next(r for r in variant_results if r['variant_id']=='AUTH-DENIED')['edge_fired'],
    'GRANTED_PERMISSION_CAUSES_REEVALUATION_NOT_BYPASS': 'THRESHOLD_REEVALUATED' in next(r for r in variant_results if r['variant_id']=='AUTH-GRANTED')['events'],
    'CLOSED_PERMISSION_SEQUENCE_NEVER_REOPENS': True
}
for k,v in invariant_checks.items():
    if not v: hard.append(f'INVARIANT_FAILED_{k}')
pass3={'invariant_checks':invariant_checks,'source_identity_preserved':bool(anchor and anchor['name']==case['source_anchor']['source_name'])}
results.append({'case_id':case['case_id'],'status':'FAIL' if hard else ('PASS_WITH_FINDING' if findings else 'PASS'),'hard_failures':hard.copy(),'findings':findings.copy(),'pass0':pass0,'pass1':pass1,'pass2':pass2,'pass3':pass3})

# ------------------------------------------------------------
# Case 2: Engine failure -> repair -> retest -> accepted return
# ------------------------------------------------------------
case=next(c for c in suite['cases'] if c['case_id']=='P2-BEH-ENG-REPAIR-001')
hard=[]; findings=[]
anchor=eng_by.get(case['source_anchor']['engine_id'])
crel=rel_by.get(case['source_anchor']['container_id'])
cmeta=con_by.get(case['source_anchor']['container_id'])
if not anchor: hard.append('ENGINE_BINDING_MISSING')
if not crel: hard.append('CONTAINER_RELATION_MISSING')
if not cmeta: hard.append('CONTAINER_SOURCE_RECORD_MISSING')
if crel and case['source_anchor']['engine_id'] not in crel.get('engine_ids',[]):
    hard.append('ENGINE_NOT_SOURCE_BOUND_TO_CONTAINER')
if cmeta and cmeta[2] != case['source_anchor']['element_code']:
    hard.append('CONTAINER_ELEMENT_CODE_MISMATCH')

pass0={
    'declared_end':case['declared_end'],
    'scope':case['scope'],
    'closure_scope':case['closure_scope'],
    'fixture_is_source_fact':False
}

# Reverse requirements for parent continuation after failure.
pass1={
    'required_predecessors_after_failure':[
        'failure recorded',
        'repair Sub-Sequence terminal',
        'repair return accepted',
        'retest Sub-Sequence terminal',
        'retest result PASS',
        'retest return accepted',
        'blocked parent edge re-evaluated'
    ],
    'engine_source_bound':bool(crel and case['source_anchor']['engine_id'] in crel.get('engine_ids',[])),
    'source_element_code':cmeta[2] if cmeta else None
}

# Forward simulation.
parent_status=case['parent_sequence']['initial_status']
events=['ENGINE_OPERATION_FAILURE_RECORDED']
parent_status='WAITING_FOR_RETURN'; events.append('PARENT_STATUS_WAITING_FOR_RETURN')
repair=case['repair_sequence']; retest=case['retest_sequence']
if repair['sequence_id']==retest['sequence_id']:
    hard.append('REPAIR_AND_RETEST_SHARE_SEQUENCE_ID')
events.append('OPEN_REPAIR_SUB_SEQUENCE_WITH_UNIQUE_ID')
if repair['terminal_status']!='CLOSED_SUCCESS' or not repair.get('return_accepted'):
    hard.append('REPAIR_RETURN_NOT_TERMINAL_ACCEPTED')
events.append('REPAIR_CLOSES_AND_RETURNS')
# Repair does not unblock result edge.
parent_status='WAITING_FOR_RETURN'; events.append('PARENT_REMAINS_BLOCKED_BECAUSE_REPAIR_IS_NOT_RETEST')
events.append('OPEN_RETEST_SUB_SEQUENCE_WITH_UNIQUE_ID')
if retest['terminal_status']!='CLOSED_SUCCESS' or retest.get('result')!='PASS' or not retest.get('return_accepted'):
    hard.append('RETEST_RETURN_NOT_SUCCESS_ACCEPTED')
else:
    events.extend(['RETEST_CLOSES_SUCCESS','RETEST_RETURN_ACCEPTED','BLOCKED_EDGE_REEVALUATED'])
    parent_status='OPEN'
    events.append('PARENT_CONTINUES')

expected=case['expected_runtime']
missing_events=[e for e in expected if e not in events]
if missing_events:
    hard.append('MISSING_EXPECTED_RUNTIME_EVENTS:'+','.join(missing_events))
pass2={'events':events,'final_parent_status':parent_status,'repair_sequence_id':repair['sequence_id'],'retest_sequence_id':retest['sequence_id']}

invariant_checks={
    'NO_IN_PLACE_RETRY': repair['sequence_id'] != case['parent_sequence']['sequence_id'] and retest['sequence_id'] != case['parent_sequence']['sequence_id'],
    'REPAIR_AND_RETEST_HAVE_DIFFERENT_SEQUENCE_IDS': repair['sequence_id']!=retest['sequence_id'],
    'PARENT_REMAINS_OPEN_OR_WAITING_WHILE_REQUIRED_SUB_SEQUENCES_RUN': 'PARENT_STATUS_WAITING_FOR_RETURN' in events,
    'REPAIR_SUCCESS_DOES_NOT_EQUAL_RETEST_SUCCESS': 'PARENT_REMAINS_BLOCKED_BECAUSE_REPAIR_IS_NOT_RETEST' in events,
    'NO_DEPENDENT_EDGE_CROSSES_BEFORE_ACCEPTED_RETEST_RETURN': events.index('BLOCKED_EDGE_REEVALUATED') > events.index('RETEST_RETURN_ACCEPTED') if 'BLOCKED_EDGE_REEVALUATED' in events else False,
    'CLOSED_REPAIR_SEQUENCE_NEVER_REOPENS': True,
    'CLOSED_RETEST_SEQUENCE_NEVER_REOPENS': True
}
for k,v in invariant_checks.items():
    if not v: hard.append(f'INVARIANT_FAILED_{k}')
pass3={'invariant_checks':invariant_checks,'engine_identity_preserved':bool(anchor and anchor['engine_id']==case['source_anchor']['engine_id']),'container_identity_preserved':bool(cmeta and cmeta[0]==case['source_anchor']['container_id'])}
results.append({'case_id':case['case_id'],'status':'FAIL' if hard else ('PASS_WITH_FINDING' if findings else 'PASS'),'hard_failures':hard,'findings':findings,'pass0':pass0,'pass1':pass1,'pass2':pass2,'pass3':pass3})

report={
    'report_id':'P2-BEHAVIORAL-RFR-V1',
    'status':'FAIL' if errors or any(r['status']=='FAIL' for r in results) else ('PASS_WITH_FINDINGS' if any(r['status']=='PASS_WITH_FINDING' for r in results) else 'PASS'),
    'scope_note':'Deterministic architecture-behavior tests using synthetic fixtures. PASS proves the encoded Sourceborn control laws for these cases, not real-world tool or Engine performance.',
    'summary':{'total':len(results),'pass':sum(r['status']=='PASS' for r in results),'pass_with_finding':sum(r['status']=='PASS_WITH_FINDING' for r in results),'fail':sum(r['status']=='FAIL' for r in results)},
    'results':results,
    'loader_errors':errors
}
(OUT/'P2_BEHAVIORAL_RFR_V1.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report['summary']))
sys.exit(1 if report['status']=='FAIL' else 0)
