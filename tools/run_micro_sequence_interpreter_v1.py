#!/usr/bin/env python3
from pathlib import Path
import argparse, hashlib, json, re, sys

ROOT=Path(__file__).resolve().parents[1]
ROUTING_PATH=ROOT/'machine/runtime/MICRO_SEQUENCE_ENGINE_ROUTING_V1.json'
HUMAN_PATH=ROOT/'registries/human/HUMAN_CONTAINER_INDEX_80_APPROVED_V1.json'
RUBRIC_PATH=ROOT/'machine/rubrics/RUBRIC_REGISTRY_R01_R52.json'

NEG_RX=re.compile(r"\b(no|not|never|didn't|doesn't|don't|cannot|can't|without)\b",re.I)
REQUEST_RX=re.compile(r"\b(ask(?:ed|ing)?|request(?:ed|ing)?|please|drop|take|help|ride|can you|could you|would you)\b",re.I)
RESOURCE_RX=re.compile(r"\b(car|vehicle|money|time|ride|transport|help|resource|place|phone|tool)\b",re.I)
DISCLOSURE_RX=re.compile(r"\b(tell|told|explain|explained|plan|where|what|context|detail|details|disclose|disclosure)\b",re.I)
INCOMPLETE_RX=re.compile(r"\b(never explain|didn't explain|doesn't explain|not explain|without explaining|incomplete|partial|didn't tell|doesn't tell|not tell|later told|after.*commit)\b",re.I)
PERSON_LEFT_RX=re.compile(r"\b(leave|left|leaving|person|someone|somebody|with me|with him|with her)\b",re.I)
INTENT_RX=re.compile(r"\b(intent|intention|motive|wants? to|wanted to|trying to|use people|using people|use me|using me)\b",re.I)
EMOTION_RX=re.compile(r"\b(feel|feeling|angry|upset|sad|uncomfortable|irritated|resent|resentment|distrust|trust|used|disrespected|afraid|fear)\b",re.I)
REPEAT_RX=re.compile(r"\b(again|always|often|repeated|repetition|multiple times|many times|\d+\s*[-–]\s*\d+\s*times|\d+\s*times|every time|keeps? doing)\b",re.I)
DECISION_RX=re.compile(r"\b(decide|decision|cut off|stop|avoid|continue|leave|boundary|refuse|say no)\b",re.I)
QUESTION_RX=re.compile(r"\?")
FIRST_PERSON_FEEL_RX=re.compile(r"\b(i feel|i felt|makes? me feel|i am feeling|i'm feeling)\b",re.I)
USER_INTENT_ATTR_RX=re.compile(r"\b(his|her|their|your|its)\s+(intent|intention|motive)\b|\b(he|she|they)\s+(wants?|wanted|intends?|intended|is trying|was trying)\b",re.I)

FEATURE_RULES=[
    ('REQUEST',REQUEST_RX),('RESOURCE',RESOURCE_RX),('DISCLOSURE',DISCLOSURE_RX),
    ('INCOMPLETE_DISCLOSURE',INCOMPLETE_RX),('PERSON_TRANSFER_OR_PRESENCE',PERSON_LEFT_RX),
    ('INTENT_LANGUAGE',INTENT_RX),('EMOTION_LANGUAGE',EMOTION_RX),('REPETITION',REPEAT_RX),
    ('DECISION_LANGUAGE',DECISION_RX),('NEGATION',NEG_RX)
]

RUBRIC_FEATURE_MAP={
    'REQUEST':['R10','R15','R24'],
    'RESOURCE':['R18','R19','R20'],
    'DISCLOSURE':['R06','R07','R08','R09'],
    'INCOMPLETE_DISCLOSURE':['R07','R09','R18','R48','R50'],
    'INTENT_LANGUAGE':['R07','R10','R43'],
    'EMOTION_LANGUAGE':['R04','R07','R43'],
    'REPETITION':['R39','R42','R45'],
    'DECISION_LANGUAGE':['R13','R24','R33'],
    'PERSON_TRANSFER_OR_PRESENCE':['R02','R08','R26'],
    'NEGATION':['R07','R13']
}
BASE_RUBRICS=['R01','R02','R06','R07','R08','R09','R38']

HUMAN_FEATURE_MAP={
    'DISCLOSURE':['CON-052','CON-054'],
    'INCOMPLETE_DISCLOSURE':['CON-054','CON-032','CON-075'],
    'INTENT_LANGUAGE':['CON-063','CON-064','CON-069'],
    'EMOTION_LANGUAGE':['CON-057','CON-058','CON-061'],
    'REPETITION':['CON-033','CON-075'],
    'DECISION_LANGUAGE':['CON-047','CON-063','CON-075'],
    'REQUEST':['CON-054','CON-063','CON-069'],
    'PERSON_TRANSFER_OR_PRESENCE':['CON-069','CON-071']
}

ALTERNATIVES=[
    'poor communication',
    'assumed familiarity',
    'convenience-driven behavior',
    'instrumental use of relationship',
    'deliberate withholding',
    'unknown/other'
]

def load_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))

def stable_id(prefix,*parts):
    h=hashlib.sha256('\x1f'.join(str(x) for x in parts).encode('utf-8')).hexdigest()[:12].upper()
    return f'{prefix}-{h}'

def split_clauses(text):
    chunks=re.split(r'(?<=[.!?;])\s+|\s*,\s*(?=(?:but|so|because|while|then)\b)',text.strip(),flags=re.I)
    return [c.strip() for c in chunks if c.strip()]

def container_index():
    data=load_json(HUMAN_PATH)
    out={}
    for seg in data.get('segments',[]):
        for row in seg.get('containers',[]):
            out[row[0]]={'name':row[1],'segment_id':seg['segment_id'],'segment_name':seg['name']}
    return out

def rubric_index():
    data=load_json(RUBRIC_PATH)
    return {rid:r for rid,r in data.get('rubrics',{}).items()}

def detect_features(text):
    feats={'SOURCE_LOCK','CLAUSE_SPLIT','RUBRIC_DRILLDOWN','MULTI_LOCAL_RESULTS','OUTPUT_READY'}
    for name,rx in FEATURE_RULES:
        if rx.search(text): feats.add(name)
    if QUESTION_RX.search(text): feats.add('QUESTION')
    if 'REQUEST' in feats: feats.add('AMBIGUOUS_SCOPE')
    if any(x in feats for x in ['DISCLOSURE','INCOMPLETE_DISCLOSURE','PERSON_TRANSFER_OR_PRESENCE']): feats.add('RELATION')
    if any(x in feats for x in ['EMOTION_LANGUAGE','INCOMPLETE_DISCLOSURE']): feats.add('STATE')
    if 'RESOURCE' in feats and 'REQUEST' in feats: feats.add('DEPENDENCY')
    if 'REPETITION' in feats: feats.update({'PATTERN_COMPARE','PRIOR_CASES'})
    if 'INTENT_LANGUAGE' in feats: feats.update({'INTENT_INFERENCE','UNCERTAINTY','PROOF_DEBT'})
    if 'INCOMPLETE_DISCLOSURE' in feats: feats.update({'UNCERTAINTY','PROOF_DEBT'})
    return feats

def history_records(path):
    if not path: return []
    d=load_json(path)
    if isinstance(d,list): return d
    for k in ('records','micro_sequences','items','history'):
        if isinstance(d.get(k),list): return d[k]
    return []

def fingerprint(features):
    keep=['REQUEST','RESOURCE','DISCLOSURE','INCOMPLETE_DISCLOSURE','PERSON_TRANSFER_OR_PRESENCE','INTENT_LANGUAGE','EMOTION_LANGUAGE','REPETITION','DECISION_LANGUAGE','NEGATION']
    return [x for x in keep if x in features]

def history_matches(records,current_fp):
    cur=set(current_fp); out=[]
    if not cur: return out
    for r in records:
        fp=set(r.get('pattern_fingerprint') or r.get('features') or [])
        if not fp: continue
        score=len(cur & fp)/len(cur | fp)
        if score>=0.5:
            out.append({'sequence_id':r.get('sequence_id') or r.get('intake',{}).get('sequence_id'),'score':round(score,3),'fingerprint':sorted(fp)})
    return sorted(out,key=lambda x:x['score'],reverse=True)

def main():
    ap=argparse.ArgumentParser(description='Sourceborn deterministic Micro-Sequence interpreter V1')
    ap.add_argument('--text',required=True)
    ap.add_argument('--speaker',default='USER')
    ap.add_argument('--sequence-id')
    ap.add_argument('--history')
    ap.add_argument('--review-decision',help='Optional RubricEditDecision JSON to generate a write-back packet')
    ap.add_argument('--output')
    args=ap.parse_args()

    text=args.text.strip()
    seq=args.sequence_id or stable_id('SEQ-MICRO',args.speaker,text)
    intake_id=stable_id('INTAKE',seq,text)
    clauses=split_clauses(text)
    features=detect_features(text)
    hidx=container_index(); ridx=rubric_index(); routing=load_json(ROUTING_PATH)
    history=history_records(args.history)
    current_fp=fingerprint(features)
    matches=history_matches(history,current_fp)
    if matches:
        features.update({'PRIOR_CASES','PATTERN_COMPARE'})

    micro=[]
    for i,c in enumerate(clauses,1):
        cid=f'{seq}-MU-{i:03d}'
        local=[]
        if NEG_RX.search(c): local.append('NEGATION')
        if REQUEST_RX.search(c): local.append('ACTION')
        if DISCLOSURE_RX.search(c): local.append('INFORMATION_STATE')
        if EMOTION_RX.search(c): local.append('STATE')
        if REPEAT_RX.search(c): local.append('RECURRENCE')
        if not local: local=['CLAUSE']
        micro.append({
            'micro_unit_id':cid,
            'sequence_id':seq,
            'source_span':{'clause_index':i},
            'exact_text':c,
            'unit_type':'CLAUSE',
            'detected_facets':local,
            'linked_object_ids':[],
            'relation_ids':[],
            'order_types':[],
            'view_state_refs':[],
            'epistemic_status':'REPORTED',
            'confidence':None
        })

    rubric_ids=set(BASE_RUBRICS)
    for f in features: rubric_ids.update(RUBRIC_FEATURE_MAP.get(f,[]))
    rubric_acts=[]
    for rid in sorted(rubric_ids):
        if rid not in ridx: continue
        rubric_acts.append({
            'activation_id':stable_id('ACT',seq,rid),
            'sequence_id':seq,
            'micro_unit_ids':[m['micro_unit_id'] for m in micro],
            'rubric_path':[rid],
            'rubric_name':ridx[rid].get('name'),
            'domain':'UNIVERSAL_SEQUENCE',
            'activation_evidence_refs':[intake_id],
            'activation_status':'CANDIDATE',
            'weight_or_relevance':None,
            'engine_candidate_ids':[],
            'asi_node_candidate_ids':[]
        })

    human_ids=set()
    for f in features: human_ids.update(HUMAN_FEATURE_MAP.get(f,[]))
    human_acts=[]
    for cid in sorted(human_ids):
        if cid not in hidx: continue
        rec=hidx[cid]
        human_acts.append({
            'activation_id':stable_id('ACT-H',seq,cid),
            'sequence_id':seq,
            'micro_unit_ids':[m['micro_unit_id'] for m in micro],
            'rubric_path':[rec['segment_id'],cid],
            'native_name':rec['name'],
            'domain':'HUMAN',
            'activation_status':'CANDIDATE',
            'activation_note':'Container-level candidate only. No atomic Human parameter is asserted by this V1 interpreter.',
            'activation_evidence_refs':[intake_id]
        })

    interpretations=[]
    if 'INTENT_LANGUAGE' in features:
        status='USER_ATTRIBUTED' if USER_INTENT_ATTR_RX.search(text) else 'INFERRED'
        interpretations.append({
            'interpretation_id':stable_id('INTP',seq,'intent'),
            'sequence_id':seq,
            'claim':'The input contains an attribution or hypothesis about another actor’s intent/motive.',
            'claim_type':'INTENT',
            'supporting_micro_unit_ids':[m['micro_unit_id'] for m in micro],
            'supporting_sequence_ids':[],
            'contradicting_sequence_ids':[],
            'alternative_interpretation_ids':[],
            'epistemic_status':status,
            'confidence':None,
            'direct_action_authority':False
        })
    if 'EMOTION_LANGUAGE' in features:
        status='USER_ATTRIBUTED' if FIRST_PERSON_FEEL_RX.search(text) else 'HYPOTHESIZED'
        interpretations.append({
            'interpretation_id':stable_id('INTP',seq,'emotion'),
            'sequence_id':seq,
            'claim':'The input contains affect/feeling language that may be relevant to the actor state.',
            'claim_type':'FEELING',
            'supporting_micro_unit_ids':[m['micro_unit_id'] for m in micro],
            'supporting_sequence_ids':[],
            'contradicting_sequence_ids':[],
            'alternative_interpretation_ids':[],
            'epistemic_status':status,
            'confidence':None,
            'direct_action_authority':False
        })

    selected_routes=[]; selected_engines=[]
    for route in routing.get('routes',[]):
        tags=set(route.get('activation_tags',[]))
        if tags & features:
            selected_routes.append({'route_id':route['route_id'],'matched_tags':sorted(tags & features),'engine_ids':route.get('engine_ids',[]),'purpose':route.get('purpose')})
            selected_engines.extend(route.get('engine_ids',[]))

    repeated_basis=('REPETITION' in features) or len(matches)>=2
    structural_basis=('REQUEST' in features and ('RESOURCE' in features or 'INCOMPLETE_DISCLOSURE' in features)) or ('INCOMPLETE_DISCLOSURE' in features)
    candidate_justified=bool(repeated_basis and structural_basis)
    contribution_type='NEW_CANDIDATE_SIGNAL' if candidate_justified else ('ACTIVATE_EXISTING' if matches else 'NO_MEANINGFUL_PATTERN')
    contribution={
        'contribution_id':stable_id('PAT-CONTRIB',seq,*current_fp),
        'sequence_id':seq,
        'target_pattern_id':None,
        'contribution_type':contribution_type,
        'evidence_refs':[intake_id],
        'difference_refs':[],
        'relation_refs':[],
        'context_scope':{'speaker':args.speaker},
        'repetition_count':len(matches)+(1 if 'REPETITION' in features else 0),
        'counterfactual_weight':None,
        'candidate_creation_requested':candidate_justified
    }

    pattern_candidate=None
    if candidate_justified:
        intent_status='USER_ATTRIBUTED' if USER_INTENT_ATTR_RX.search(text) else ('INFERRED' if 'INTENT_LANGUAGE' in features else 'UNKNOWN')
        pattern_candidate={
            'pattern_candidate_id':stable_id('PAT-CAND',*current_fp),
            'name':'REPEATED_PARTIAL_CONTEXT_OR_RESOURCE_COMMITMENT_PATTERN',
            'machine_description':'Repeated structure may involve commitment/resource use occurring before complete context is available. This is a candidate structural interpretation, not a character judgment or observed hidden intent.',
            'status':'REVIEW_REQUIRED',
            'supporting_sequence_ids':[m['sequence_id'] for m in matches if m.get('sequence_id')]+[seq],
            'contradicting_sequence_ids':[],
            'parameter_refs':[],
            'rubric_refs':sorted(rubric_ids),
            'relation_signature':'resource/request + information timing + commitment/context asymmetry',
            'order_signature':'request/commitment may precede fuller context',
            'context_bounds':{'scope':'CURRENT_ACTOR_RELATIONSHIP_OR_USER_DEFINED_SCOPE','requires_review':True},
            'alternative_interpretations':ALTERNATIVES,
            'intent_status':intent_status,
            'confidence':None,
            'approval_status':'NOT_REVIEWED',
            'approval_scope':None,
            'approved_pattern_id':None,
            'direct_action_authority':False
        }

    review_id=stable_id('RUBRIC-REVIEW',seq)
    review={
        'review_id':review_id,
        'sequence_id':seq,
        'machine_proposal':{
            'interpretations':interpretations,
            'pattern_candidate':pattern_candidate,
            'summary':'V1 deterministic structural proposal. Unknown/ambiguous semantics require user correction or deeper Engines.'
        },
        'activated_rubric_paths':rubric_acts+human_acts,
        'prior_sequence_refs':[m.get('sequence_id') for m in matches if m.get('sequence_id')],
        'engine_trace_ids':sorted(set(selected_engines)),
        'node_trace_ids':['ASI-NODE-02','ASI-NODE-06','ASI-NODE-08','ASI-NODE-12','ASI-NODE-15','ASI-NODE-16','ASI-NODE-17','ASI-NODE-20','ASI-NODE-21'],
        'unknowns':['exact intent/motive unless directly evidenced','full actor history unless supplied','atomic Human parameters not resolved by V1'],
        'editable_fields':{
            'interpretation':None,'feeling':None,'emotion':None,'meaning':None,'intent_attribution':None,'motive_attribution':None,'boundary':None,'rule_or_principle':None,'pattern_name':pattern_candidate.get('name') if pattern_candidate else None,'applies_when':None,'does_not_apply_when':None,'approval_scope':None
        },
        'source_proposal_immutable':True
    }

    writeback=None
    if args.review_decision:
        decision=load_json(args.review_decision)
        valid={'APPROVE_AS_IS','EDIT_AND_APPROVE','REJECT','KEEP_OCCURRENCE_ONLY','NEEDS_MORE_EVIDENCE','CREATE_NEW_PATTERN_CANDIDATE','PROPOSE_RUBRIC_CHANGE'}
        if decision.get('decision') not in valid:
            raise SystemExit('invalid review decision')
        target_map={
            'OCCURRENCE_ONLY':'OCCURRENCE_MEMORY','PERSONAL_PATTERN':'PERSONAL_PATTERN_REGISTRY','RELATIONSHIP_SPECIFIC_PATTERN':'RELATIONSHIP_PATTERN_REGISTRY','DOMAIN_PATTERN':'DOMAIN_PATTERN_REGISTRY','GENERAL_PATTERN_CANDIDATE':'GENERAL_PATTERN_CANDIDATES','RUBRIC_CHANGE_CANDIDATE':'RUBRIC_CHANGE_CANDIDATES'
        }
        target=target_map.get(decision.get('scope'),'OCCURRENCE_MEMORY')
        wb_seq=stable_id('SEQ-WRITEBACK',seq,decision.get('decision_id','decision'))
        writeback={
            'writeback_id':stable_id('LEARN-WB',wb_seq),
            'writeback_sequence_id':wb_seq,
            'source_review_id':review_id,
            'source_decision_id':decision.get('decision_id'),
            'prior_closed_sequence_refs':[seq],
            'target_store':target,
            'version_action':'NO_WRITEBACK' if decision.get('decision') in {'REJECT','NEEDS_MORE_EVIDENCE'} else 'CREATE',
            'new_object_id':None if decision.get('decision') in {'REJECT','NEEDS_MORE_EVIDENCE'} else stable_id('PATTERN-V1',target,seq),
            'supersedes_object_id':None,
            'provenance_refs':[intake_id,review_id],
            'closure_status':'CLOSED_SUCCESS'
        }

    result={
        'runtime_id':'SENTENCE-MICRO-SEQUENCE-RUNTIME-V1',
        'interpreter_version':'P2-MICRO-SEQUENCE-LIVE-INTERPRETER-001/V1',
        'sequence_id':seq,
        'intake':{
            'intake_id':intake_id,'sequence_id':seq,'raw_text':text,'source_type':'USER_UTTERANCE','speaker_or_source_id':args.speaker,'time_ref':None,'context_ref_ids':[],'declared_end':'Represent and interpret this input under the local conversation/task contract.','scope':{'resolution':'progressive ultra-micro'},'closure_scope':'LOCAL_INPUT_ANALYSIS'
        },
        'features':sorted(features),
        'pattern_fingerprint':current_fp,
        'micro_units':micro,
        'rubric_activations':rubric_acts,
        'human_container_activations':human_acts,
        'interpretation_candidates':interpretations,
        'prior_sequence_matches':matches,
        'engine_routes':selected_routes,
        'pattern_contribution':contribution,
        'pattern_candidate':pattern_candidate,
        'reviewable_rubric_view':review,
        'learning_writeback':writeback,
        'epistemic_guard':'Machine structural output is candidate/inference unless explicitly source-observed. User attributions remain user-attributed. Pattern candidates have no direct action authority.'
    }
    payload=json.dumps(result,ensure_ascii=False,indent=2)
    if args.output:
        Path(args.output).write_text(payload,encoding='utf-8')
    else:
        print(payload)

if __name__=='__main__':
    main()
