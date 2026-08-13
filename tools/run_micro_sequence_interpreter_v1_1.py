#!/usr/bin/env python3
from pathlib import Path
import argparse, hashlib, json, re

ROOT=Path(__file__).resolve().parents[1]
ROUTING=ROOT/'machine/runtime/MICRO_SEQUENCE_ENGINE_ROUTING_V1.json'
HUMAN=ROOT/'registries/human/HUMAN_CONTAINER_INDEX_80_APPROVED_V1.json'
RUBRICS=ROOT/'machine/rubrics/RUBRIC_REGISTRY_R01_R52.json'

RX={
 'REQUEST':re.compile(r"\b(?:ask(?:ed|s|ing)?|request(?:ed|s|ing)?|please|drop|take|help|ride|can you|could you|would you)\b",re.I),
 'RESOURCE':re.compile(r"\b(?:car|vehicle|money|time|ride|transport|help|resource|place|phone|tool)\b",re.I),
 'DISCLOSURE':re.compile(r"\b(?:tell|tells|telling|told|explain|explains|explaining|explained|plan|where|what|context|detail|details|disclose|disclosed|disclosure)\b",re.I),
 'INCOMPLETE_DISCLOSURE':re.compile(r"\b(?:never\s+(?:explain(?:ed|s|ing)?|tell(?:s|ing)?|told)|(?:didn['’]t|doesn['’]t|don['’]t|not)\s+(?:explain|tell|disclose)|without\s+(?:explaining|telling|disclosing)|incomplete|partial|later\s+(?:told|explained|disclosed)|after\b.{0,80}\bcommit(?:ted|ment)?)\b",re.I),
 'PERSON_TRANSFER_OR_PRESENCE':re.compile(r"\b(?:leave|leaves|leaving|left|person|someone|somebody|with me|with him|with her|with them)\b",re.I),
 'INTENT_LANGUAGE':re.compile(r"\b(?:intent|intention|motive|wants? to|wanted to|trying to|use people|using people|use me|using me|use my help)\b",re.I),
 'EMOTION_LANGUAGE':re.compile(r"\b(?:feel|feeling|felt|angry|upset|sad|uncomfortable|irritated|resent|resentment|distrust|trust|used|disrespected|afraid|fear)\b",re.I),
 'REPETITION':re.compile(r"\b(?:again|always|often|repeated|repetition|multiple times|many times|\d+\s*[-–]\s*\d+\s*times|\d+\s*times|every time|keeps? doing)\b",re.I),
 'DECISION_LANGUAGE':re.compile(r"\b(?:decide|decision|cut off|stop|avoid|continue|boundary|refuse|say no)\b",re.I),
 'NEGATION':re.compile(r"\b(?:no|not|never|cannot|without)\b|\b(?:didn['’]t|doesn['’]t|don['’]t|can['’]t)\b",re.I)
}
USER_INTENT=re.compile(r"\b(?:his|her|their|your|its)\s+(?:intent|intention|motive)\b|\b(?:he|she|they)\s+(?:wants?|wanted|intends?|intended|is trying|was trying)\b",re.I)
FIRST_FEEL=re.compile(r"\b(?:i feel|i felt|makes? me feel|i am feeling|i['’]m feeling)\b",re.I)

RMAP={
 'REQUEST':['R10','R15','R24'],'RESOURCE':['R18','R19','R20'],'DISCLOSURE':['R06','R07','R08','R09'],
 'INCOMPLETE_DISCLOSURE':['R07','R09','R18','R48','R50'],'INTENT_LANGUAGE':['R07','R10','R43'],
 'EMOTION_LANGUAGE':['R04','R07','R43'],'REPETITION':['R39','R42','R45'],'DECISION_LANGUAGE':['R13','R24','R33'],
 'PERSON_TRANSFER_OR_PRESENCE':['R02','R08','R26'],'NEGATION':['R07','R13']
}
BASE_R=['R01','R02','R06','R07','R08','R09','R38']
HMAP={
 'DISCLOSURE':['CON-052','CON-054'],'INCOMPLETE_DISCLOSURE':['CON-032','CON-054','CON-075'],
 'INTENT_LANGUAGE':['CON-063','CON-064','CON-069'],'EMOTION_LANGUAGE':['CON-057','CON-058','CON-061'],
 'REPETITION':['CON-033','CON-075'],'DECISION_LANGUAGE':['CON-047','CON-063','CON-075'],
 'REQUEST':['CON-054','CON-063','CON-069'],'PERSON_TRANSFER_OR_PRESENCE':['CON-069','CON-071']
}
ALT=['poor communication','assumed familiarity','convenience-driven behavior','instrumental use of relationship','deliberate withholding','unknown/other']

def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sid(prefix,*parts): return prefix+'-'+hashlib.sha256('\x1f'.join(map(str,parts)).encode()).hexdigest()[:12].upper()
def clauses(t): return [x.strip() for x in re.split(r'(?<=[.!?;])\s+|\s*,\s*(?=(?:but|so|because|while|then)\b)',t.strip(),flags=re.I) if x.strip()]

def human_index():
 d=load(HUMAN); out={}
 for s in d['segments']:
  for r in s['containers']: out[r[0]]={'name':r[1],'segment_id':s['segment_id']}
 return out

def features(t):
 f={'SOURCE_LOCK','CLAUSE_SPLIT','RUBRIC_DRILLDOWN','MULTI_LOCAL_RESULTS','OUTPUT_READY'}
 for k,rx in RX.items():
  if rx.search(t): f.add(k)
 if '?' in t: f.add('QUESTION')
 if 'REQUEST' in f: f.add('AMBIGUOUS_SCOPE')
 if f & {'DISCLOSURE','INCOMPLETE_DISCLOSURE','PERSON_TRANSFER_OR_PRESENCE'}: f.add('RELATION')
 if f & {'EMOTION_LANGUAGE','INCOMPLETE_DISCLOSURE'}: f.add('STATE')
 if {'RESOURCE','REQUEST'} <= f: f.add('DEPENDENCY')
 if 'REPETITION' in f: f |= {'PATTERN_COMPARE','PRIOR_CASES'}
 if 'INTENT_LANGUAGE' in f: f |= {'INTENT_INFERENCE','UNCERTAINTY','PROOF_DEBT'}
 if 'INCOMPLETE_DISCLOSURE' in f: f |= {'UNCERTAINTY','PROOF_DEBT'}
 return f

def hist(path):
 if not path: return []
 d=load(path)
 if isinstance(d,list): return d
 for k in ('records','micro_sequences','items','history'):
  if isinstance(d.get(k),list): return d[k]
 return []

def fp(f):
 order=['REQUEST','RESOURCE','DISCLOSURE','INCOMPLETE_DISCLOSURE','PERSON_TRANSFER_OR_PRESENCE','INTENT_LANGUAGE','EMOTION_LANGUAGE','REPETITION','DECISION_LANGUAGE','NEGATION']
 return [x for x in order if x in f]

def matches(records,cur):
 a=set(cur); out=[]
 if not a: return out
 for r in records:
  b=set(r.get('pattern_fingerprint') or r.get('features') or [])
  if not b: continue
  s=len(a&b)/len(a|b)
  if s>=.5: out.append({'sequence_id':r.get('sequence_id') or r.get('intake',{}).get('sequence_id'),'score':round(s,3),'fingerprint':sorted(b)})
 return sorted(out,key=lambda z:z['score'],reverse=True)

def main():
 ap=argparse.ArgumentParser(); ap.add_argument('--text',required=True); ap.add_argument('--speaker',default='USER'); ap.add_argument('--sequence-id'); ap.add_argument('--history'); ap.add_argument('--review-decision'); ap.add_argument('--output'); a=ap.parse_args()
 t=a.text.strip(); seq=a.sequence_id or sid('SEQ-MICRO',a.speaker,t); intake=sid('INTAKE',seq,t)
 f=features(t); prior=matches(hist(a.history),fp(f))
 if prior: f |= {'PRIOR_CASES','PATTERN_COMPARE'}
 mus=[]
 for i,c in enumerate(clauses(t),1):
  facets=[k for k,rx in RX.items() if rx.search(c)] or ['CLAUSE']
  mus.append({'micro_unit_id':f'{seq}-MU-{i:03d}','sequence_id':seq,'source_span':{'clause_index':i},'exact_text':c,'unit_type':'CLAUSE','detected_facets':facets,'linked_object_ids':[],'relation_ids':[],'order_types':[],'view_state_refs':[],'epistemic_status':'REPORTED','confidence':None})
 ridx=load(RUBRICS)['rubrics']; rids=set(BASE_R)
 for x in f: rids.update(RMAP.get(x,[]))
 racts=[{'activation_id':sid('ACT',seq,r),'sequence_id':seq,'micro_unit_ids':[m['micro_unit_id'] for m in mus],'rubric_path':[r],'rubric_name':ridx[r]['name'],'domain':'UNIVERSAL_SEQUENCE','activation_evidence_refs':[intake],'activation_status':'CANDIDATE','weight_or_relevance':None,'engine_candidate_ids':[],'asi_node_candidate_ids':[]} for r in sorted(rids) if r in ridx]
 hidx=human_index(); hids=set()
 for x in f: hids.update(HMAP.get(x,[]))
 hacts=[{'activation_id':sid('ACT-H',seq,c),'sequence_id':seq,'micro_unit_ids':[m['micro_unit_id'] for m in mus],'rubric_path':[hidx[c]['segment_id'],c],'native_name':hidx[c]['name'],'domain':'HUMAN','activation_status':'CANDIDATE','activation_note':'Container-level candidate only. No atomic Human parameter is asserted by V1.1.','activation_evidence_refs':[intake]} for c in sorted(hids) if c in hidx]
 inter=[]
 if 'INTENT_LANGUAGE' in f:
  inter.append({'interpretation_id':sid('INTP',seq,'intent'),'sequence_id':seq,'claim':'Input contains an attribution/hypothesis about another actor intent or motive.','claim_type':'INTENT','supporting_micro_unit_ids':[m['micro_unit_id'] for m in mus],'supporting_sequence_ids':[],'contradicting_sequence_ids':[],'alternative_interpretation_ids':[],'epistemic_status':'USER_ATTRIBUTED' if USER_INTENT.search(t) else 'INFERRED','confidence':None,'direct_action_authority':False})
 if 'EMOTION_LANGUAGE' in f:
  inter.append({'interpretation_id':sid('INTP',seq,'feeling'),'sequence_id':seq,'claim':'Input contains affect/feeling language relevant to actor state.','claim_type':'FEELING','supporting_micro_unit_ids':[m['micro_unit_id'] for m in mus],'supporting_sequence_ids':[],'contradicting_sequence_ids':[],'alternative_interpretation_ids':[],'epistemic_status':'USER_ATTRIBUTED' if FIRST_FEEL.search(t) else 'HYPOTHESIZED','confidence':None,'direct_action_authority':False})
 routes=[]; eng=[]
 for r in load(ROUTING)['routes']:
  hit=sorted(set(r.get('activation_tags',[])) & f)
  if hit:
   routes.append({'route_id':r['route_id'],'matched_tags':hit,'engine_ids':r['engine_ids'],'purpose':r['purpose']}); eng += r['engine_ids']
 repeated='REPETITION' in f or len(prior)>=2
 structural='INCOMPLETE_DISCLOSURE' in f or ('REQUEST' in f and 'RESOURCE' in f)
 justified=repeated and structural
 contrib={'contribution_id':sid('PAT-CONTRIB',seq,*fp(f)),'sequence_id':seq,'target_pattern_id':None,'contribution_type':'NEW_CANDIDATE_SIGNAL' if justified else ('ACTIVATE_EXISTING' if prior else 'NO_MEANINGFUL_PATTERN'),'evidence_refs':[intake],'difference_refs':[],'relation_refs':[],'context_scope':{'speaker':a.speaker},'repetition_count':len(prior)+(1 if 'REPETITION' in f else 0),'counterfactual_weight':None,'candidate_creation_requested':bool(justified)}
 pc=None
 if justified:
  pc={'pattern_candidate_id':sid('PAT-CAND',*fp(f)),'name':'REPEATED_PARTIAL_CONTEXT_OR_RESOURCE_COMMITMENT_PATTERN','machine_description':'Repeated structure may involve commitment/resource use before complete context is available. Candidate structural interpretation only; not a character judgment or observed hidden intent.','status':'REVIEW_REQUIRED','supporting_sequence_ids':[x['sequence_id'] for x in prior if x.get('sequence_id')]+[seq],'contradicting_sequence_ids':[],'parameter_refs':[],'rubric_refs':sorted(rids),'relation_signature':'resource/request + information timing + commitment/context asymmetry','order_signature':'request/commitment may precede fuller context','context_bounds':{'scope':'CURRENT_ACTOR_RELATIONSHIP_OR_USER_DEFINED_SCOPE','requires_review':True},'alternative_interpretations':ALT,'intent_status':'USER_ATTRIBUTED' if USER_INTENT.search(t) else ('INFERRED' if 'INTENT_LANGUAGE' in f else 'UNKNOWN'),'confidence':None,'approval_status':'NOT_REVIEWED','approval_scope':None,'approved_pattern_id':None,'direct_action_authority':False}
 review_id=sid('RUBRIC-REVIEW',seq)
 review={'review_id':review_id,'sequence_id':seq,'machine_proposal':{'interpretations':inter,'pattern_candidate':pc,'summary':'V1.1 deterministic structural proposal; ambiguity requires correction or deeper Engines.'},'activated_rubric_paths':racts+hacts,'prior_sequence_refs':[x['sequence_id'] for x in prior if x.get('sequence_id')],'engine_trace_ids':sorted(set(eng)),'node_trace_ids':['ASI-NODE-02','ASI-NODE-06','ASI-NODE-08','ASI-NODE-12','ASI-NODE-15','ASI-NODE-16','ASI-NODE-17','ASI-NODE-20','ASI-NODE-21'],'unknowns':['exact intent/motive unless directly evidenced','full actor history unless supplied','atomic Human parameters not resolved by V1.1'],'editable_fields':{'interpretation':None,'feeling':None,'emotion':None,'meaning':None,'intent_attribution':None,'motive_attribution':None,'boundary':None,'rule_or_principle':None,'pattern_name':pc.get('name') if pc else None,'applies_when':None,'does_not_apply_when':None,'approval_scope':None},'source_proposal_immutable':True}
 wb=None
 if a.review_decision:
  d=load(a.review_decision); targets={'OCCURRENCE_ONLY':'OCCURRENCE_MEMORY','PERSONAL_PATTERN':'PERSONAL_PATTERN_REGISTRY','RELATIONSHIP_SPECIFIC_PATTERN':'RELATIONSHIP_PATTERN_REGISTRY','DOMAIN_PATTERN':'DOMAIN_PATTERN_REGISTRY','GENERAL_PATTERN_CANDIDATE':'GENERAL_PATTERN_CANDIDATES','RUBRIC_CHANGE_CANDIDATE':'RUBRIC_CHANGE_CANDIDATES'}; target=targets.get(d.get('scope'),'OCCURRENCE_MEMORY'); ws=sid('SEQ-WRITEBACK',seq,d.get('decision_id','decision')); no=d.get('decision') in {'REJECT','NEEDS_MORE_EVIDENCE'}
  wb={'writeback_id':sid('LEARN-WB',ws),'writeback_sequence_id':ws,'source_review_id':review_id,'source_decision_id':d.get('decision_id'),'prior_closed_sequence_refs':[seq],'target_store':target,'version_action':'NO_WRITEBACK' if no else 'CREATE','new_object_id':None if no else sid('PATTERN-V1',target,seq),'supersedes_object_id':None,'provenance_refs':[intake,review_id],'closure_status':'CLOSED_SUCCESS'}
 result={'runtime_id':'SENTENCE-MICRO-SEQUENCE-RUNTIME-V1','interpreter_version':'P2-MICRO-SEQUENCE-LIVE-INTERPRETER-001/V1.1','supersedes_interpreter':'P2-MICRO-SEQUENCE-LIVE-INTERPRETER-001/V1','correction':'Inflection-tolerant incomplete-disclosure detection; no authority/inference contracts changed.','sequence_id':seq,'intake':{'intake_id':intake,'sequence_id':seq,'raw_text':t,'source_type':'USER_UTTERANCE','speaker_or_source_id':a.speaker,'time_ref':None,'context_ref_ids':[],'declared_end':'Represent and interpret this input under the local conversation/task contract.','scope':{'resolution':'progressive ultra-micro'},'closure_scope':'LOCAL_INPUT_ANALYSIS'},'features':sorted(f),'pattern_fingerprint':fp(f),'micro_units':mus,'rubric_activations':racts,'human_container_activations':hacts,'interpretation_candidates':inter,'prior_sequence_matches':prior,'engine_routes':routes,'pattern_contribution':contrib,'pattern_candidate':pc,'reviewable_rubric_view':review,'learning_writeback':wb,'epistemic_guard':'Machine structural output is candidate/inference unless source-observed. User attributions remain user-attributed. Pattern candidates have no direct action authority.'}
 payload=json.dumps(result,ensure_ascii=False,indent=2)
 if a.output: Path(a.output).write_text(payload,encoding='utf-8')
 else: print(payload)

if __name__=='__main__': main()
