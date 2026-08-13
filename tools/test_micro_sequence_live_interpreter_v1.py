#!/usr/bin/env python3
from pathlib import Path
import json, subprocess, sys, tempfile

ROOT=Path(__file__).resolve().parents[1]
SCRIPT=ROOT/'tools/run_micro_sequence_interpreter_v1.py'
GEN=ROOT/'generated/tests'
GEN.mkdir(parents=True,exist_ok=True)

text=(
    'Over 4-5 times, they asked me to drop them somewhere in a car and never explained the full plan; '
    'they left another person with me after I was already committed, and I think their intention was to use my help.'
)
seq='SYN-LIVE-MICRO-001'
errors=[]

with tempfile.TemporaryDirectory() as td:
    out=Path(td)/'out.json'
    cmd=[sys.executable,str(SCRIPT),'--text',text,'--speaker','SYNTHETIC-USER','--sequence-id',seq,'--output',str(out)]
    p=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True)
    if p.returncode!=0:
        errors.append('interpreter failed:'+p.stderr)
        data={}
    else:
        data=json.loads(out.read_text(encoding='utf-8'))

    if data:
        if data.get('sequence_id')!=seq: errors.append('sequence ID mismatch')
        if not data.get('micro_units'): errors.append('no MicroUnits produced')
        pc=data.get('pattern_candidate')
        if not pc: errors.append('repeated structural case did not produce Pattern Candidate')
        else:
            if pc.get('intent_status')!='USER_ATTRIBUTED': errors.append('user intent attribution was not preserved as USER_ATTRIBUTED')
            if pc.get('direct_action_authority') is not False: errors.append('Pattern Candidate gained action authority')
            if pc.get('approval_status')!='NOT_REVIEWED': errors.append('Pattern Candidate auto-promoted before review')
        rv=data.get('reviewable_rubric_view',{})
        if rv.get('source_proposal_immutable') is not True: errors.append('machine proposal not immutable in review view')
        if 'R42' not in {a.get('rubric_path',[None])[0] for a in data.get('rubric_activations',[])}: errors.append('Pattern/Generalization rubric R42 not activated')
        if 'R48' not in {a.get('rubric_path',[None])[0] for a in data.get('rubric_activations',[])}: errors.append('Gap rubric R48 not activated for incomplete disclosure')
        human={a.get('rubric_path',[])[-1] for a in data.get('human_container_activations',[]) if a.get('rubric_path')}
        for cid in ['CON-054','CON-063','CON-069']:
            if cid not in human: errors.append('expected candidate Human container not activated:'+cid)
        engines={eid for r in data.get('engine_routes',[]) for eid in r.get('engine_ids',[])}
        for eid in ['ENG-CORE-001','ENG-SB-005','ENG-ARD-001','ENG-PAT-001','ENG-URR-002']:
            if eid not in engines: errors.append('expected Engine route absent:'+eid)
        if any('SB-ASI-P' in json.dumps(a) for a in data.get('human_container_activations',[])):
            errors.append('V1 interpreter invented/claimed atomic Human parameter IDs')

        decision={
            'decision_id':'SYN-DECISION-001',
            'review_id':rv.get('review_id'),
            'editor_id':'SYNTHETIC-USER',
            'decision':'EDIT_AND_APPROVE',
            'scope':'RELATIONSHIP_SPECIFIC_PATTERN',
            'edits':{
                'interpretation':'I experience this repeated structure as instrumental use of the relationship.',
                'feeling':'used / loss of trust',
                'boundary':'do not accept requests under incomplete context'
            }
        }
        dec=Path(td)/'decision.json'; dec.write_text(json.dumps(decision),encoding='utf-8')
        out2=Path(td)/'out2.json'
        p2=subprocess.run([sys.executable,str(SCRIPT),'--text',text,'--speaker','SYNTHETIC-USER','--sequence-id',seq,'--review-decision',str(dec),'--output',str(out2)],cwd=ROOT,text=True,capture_output=True)
        if p2.returncode!=0:
            errors.append('interpreter review/writeback failed:'+p2.stderr)
        else:
            d2=json.loads(out2.read_text(encoding='utf-8'))
            wb=d2.get('learning_writeback')
            if not wb: errors.append('explicit approved review did not create LearningWritebackPacket')
            else:
                if wb.get('target_store')!='RELATIONSHIP_PATTERN_REGISTRY': errors.append('writeback target scope mismatch')
                if wb.get('writeback_sequence_id')==seq: errors.append('writeback reused/reopened original Sequence')
                if wb.get('version_action')!='CREATE': errors.append('approved edit did not create versioned object')
                if seq not in wb.get('prior_closed_sequence_refs',[]): errors.append('writeback does not reference prior analysis Sequence')

report={
    'report_id':'P2-MICRO-SEQUENCE-LIVE-INTERPRETER-TEST-V1',
    'status':'PASS' if not errors else 'FAIL',
    'fixture_sequence_id':seq,
    'checks':{
        'micro_units_produced':bool(data.get('micro_units')) if data else False,
        'pattern_candidate_produced':bool(data.get('pattern_candidate')) if data else False,
        'intent_user_attributed':(data.get('pattern_candidate') or {}).get('intent_status')=='USER_ATTRIBUTED' if data else False,
        'pattern_no_action_authority':(data.get('pattern_candidate') or {}).get('direct_action_authority') is False if data else False,
        'review_view_present':bool(data.get('reviewable_rubric_view')) if data else False,
        'explicit_review_creates_separate_writeback':not any('writeback reused/reopened original Sequence' in e for e in errors)
    },
    'errors':errors
}
(GEN/'P2_MICRO_SEQUENCE_LIVE_INTERPRETER_TEST_V1.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
sys.exit(1 if errors else 0)
