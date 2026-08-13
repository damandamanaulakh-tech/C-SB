#!/usr/bin/env python3
from pathlib import Path
import json, sys

ROOT=Path(__file__).resolve().parents[1]
GEN=ROOT/'generated/tests'
GEN.mkdir(parents=True,exist_ok=True)

paths={
    'runtime':ROOT/'machine/runtime/SENTENCE_MICRO_SEQUENCE_RUNTIME_V1.json',
    'routing':ROOT/'machine/runtime/MICRO_SEQUENCE_ENGINE_ROUTING_V1.json',
    'schema':ROOT/'machine/schemas/micro_sequence_learning.schema.json',
    'pattern':ROOT/'registries/sourceborn/PATTERN_REGISTRY_CONTROL_V1.json',
    'ui':ROOT/'machine/ui/RUBRIC_MICROSCOPE_CONTRACT_V1.json',
    'overlay':ROOT/'registries/asi/node_brains/MICRO_SEQUENCE_PATTERN_RESPONSIBILITY_OVERLAY_V1.json',
    'fixture':ROOT/'phase2/tests/MICRO_SEQUENCE_PATTERN_FIXTURE_001.json',
    'engines':ROOT/'registries/asi/ENGINE_LIBRARY_75_APPROVED_V1.json',
    'nodes':ROOT/'registries/asi/asi_node_registry.json',
}
errors=[]
findings=[]
obj={}
for k,p in paths.items():
    if not p.exists():
        errors.append(f'missing:{p.relative_to(ROOT)}')
        continue
    try:
        obj[k]=json.loads(p.read_text(encoding='utf-8'))
    except Exception as e:
        errors.append(f'invalid_json:{p.relative_to(ROOT)}:{e}')

if errors:
    report={'report_id':'P2-MICRO-SEQUENCE-PATTERN-RFR-V1','status':'FAIL','errors':errors,'findings':findings}
    (GEN/'P2_MICRO_SEQUENCE_PATTERN_RFR_V1.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2)); sys.exit(1)

runtime=obj['runtime']; routing=obj['routing']; schema=obj['schema']; pattern=obj['pattern']; ui=obj['ui']; overlay=obj['overlay']; fixture=obj['fixture']
engine_ids={r[0] for r in obj['engines'].get('records',[]) if isinstance(r,list) and r}
node_ids={r.get('asi_node_id') for r in obj['nodes'].get('nodes',[]) if isinstance(r,dict)}

# Pass 0: declared architecture
required_stages=[f'MS-{i:02d}' for i in range(13)]
stages=runtime.get('execution_stages',[])
stage_ids=[s.get('stage') for s in stages]
if stage_ids!=required_stages:
    errors.append(f'runtime stages mismatch expected={required_stages} actual={stage_ids}')
if runtime.get('core_rule')!='EVERY_INPUT_UTTERANCE_CREATES_AT_LEAST_ONE_LOCAL_MICRO_SEQUENCE':
    errors.append('missing every-input local micro-sequence core rule')
if runtime.get('pattern_formation_rule',{}).get('automatic_promotion') is not False:
    errors.append('pattern automatic promotion must be false')

# Engine + node references must be real existing approved registry IDs.
referenced_engines=[]; referenced_nodes=[]
for s in stages:
    referenced_engines += s.get('engine_ids',[])
    referenced_nodes += s.get('asi_node_ids',[])
routing_engine_refs=[]
for route in routing.get('routes',[]):
    routing_engine_refs += route.get('engine_ids',[])
referenced_engines += routing_engine_refs
missing_engines=sorted(set(referenced_engines)-engine_ids)
missing_nodes=sorted(set(referenced_nodes)-node_ids)
if missing_engines: errors.append('unknown engine refs:'+','.join(missing_engines))
if missing_nodes: errors.append('unknown ASI node refs:'+','.join(missing_nodes))

route_ids=[r.get('route_id') for r in routing.get('routes',[])]
expected_route_ids=[f'MER-{i:02d}' for i in range(1,13)]
if route_ids!=expected_route_ids:
    errors.append(f'engine routing IDs mismatch expected={expected_route_ids} actual={route_ids}')
routing_laws=' '.join(routing.get('routing_laws',[]))
for law_text in ['Engine result is evidence/output, not execution authority','META is invoked for meta-governance/conflict/priority','RGL recursion cannot become an unbounded in-place loop','Pattern Engines create Pattern Contributions/Candidates, never automatic approved rubrics']:
    if law_text not in routing_laws:
        errors.append('missing engine-routing law:'+law_text)

# Schema objects required for machine execution/review/writeback.
required_defs={'SentenceIntakePacket','MicroUnit','RubricActivationPacket','InterpretationCandidate','PatternContributionPacket','PatternCandidate','ReviewableRubricView','RubricEditDecision','LearningWritebackPacket'}
defs=set(schema.get('$defs',{}))
missing_defs=sorted(required_defs-defs)
if missing_defs: errors.append('missing schema defs:'+','.join(missing_defs))

# Required epistemic and approval separation.
non_eq=set(runtime.get('non_equivalences',[]))
for invariant in ['OBSERVATION != INTERPRETATION','INTERPRETATION != INTENT_FACT','PATTERN_CANDIDATE != APPROVED_RUBRIC','ENGINE_OUTPUT != EXECUTION_AUTHORITY']:
    if invariant not in non_eq: errors.append('missing non-equivalence:'+invariant)

namespaces={n.get('namespace') for n in pattern.get('pattern_namespaces',[])}
for ns in ['OCCURRENCE_MEMORY','PATTERN_CANDIDATES','PERSONAL_PATTERNS','RELATIONSHIP_PATTERNS','DOMAIN_PATTERNS','GENERAL_PATTERN_CANDIDATES','RUBRIC_CHANGE_CANDIDATES']:
    if ns not in namespaces: errors.append('missing pattern namespace:'+ns)

immut=' '.join(pattern.get('immutability_rules',[]))
if 'Machine interpretation proposal is immutable' not in immut:
    errors.append('machine proposal immutability missing')
if 'Closed supporting Sequences never reopen' not in immut:
    errors.append('closed supporting Sequence immutability missing')

# UI microscope coverage.
panel_ids=[p.get('panel_id') for p in ui.get('panels',[])]
expected_panels=[f'RM-{i:02d}' for i in range(1,10)]
if panel_ids!=expected_panels: errors.append(f'Rubric Microscope panel mismatch actual={panel_ids}')
editable=' '.join(str(p.get('editable',[])) for p in ui.get('panels',[]))
for field in ['emotion','feeling','intent attribution','boundary','pattern name']:
    if field not in editable: errors.append('UI editable field missing:'+field)

# Small-brain bounded ownership.
overlay_nodes={x.get('asi_node_id') for x in overlay.get('node_overlays',[])}
for nid in ['ASI-NODE-02','ASI-NODE-06','ASI-NODE-08','ASI-NODE-12','ASI-NODE-15','ASI-NODE-16','ASI-NODE-17','ASI-NODE-20','ASI-NODE-21']:
    if nid not in overlay_nodes: errors.append('missing small-brain responsibility overlay:'+nid)

# Synthetic repeated-behavior fixture: 5 closed-case inputs, alternatives, inferred intent, versioned writeback.
occ=fixture.get('occurrences',[])
if len(occ)!=5: errors.append(f'fixture occurrence count !=5 actual={len(occ)}')
if fixture.get('expected_pattern_contribution',{}).get('repetition_evidence_count')!=5:
    errors.append('fixture repetition evidence count must be 5')
alts=fixture.get('required_alternative_interpretations',[])
if len(alts)<4: errors.append('fixture needs multiple alternative interpretations')
if fixture.get('required_intent_status_before_user_review')=='OBSERVED':
    errors.append('fixture incorrectly treats intent as observed')
review=fixture.get('review_simulation',{})
if review.get('expected_writeback')!='NEW_VERSIONED_RELATIONSHIP_PATTERN':
    errors.append('fixture writeback must be versioned relationship pattern')
if review.get('user_edit_example',{}).get('approval_scope')!='RELATIONSHIP_SPECIFIC_PATTERN':
    errors.append('fixture approval scope should remain relationship-specific')

# Pattern creation is not a forced numerical threshold.
minimum_rule=pattern.get('candidate_creation',{}).get('minimum_rule','')
if 'not a universal fixed threshold' not in minimum_rule:
    errors.append('repetition count was accidentally made a universal fixed threshold')

# User edits do not rewrite native rubrics directly.
prom=pattern.get('promotion_rules',{})
if 'formal registry adoption/version migration' not in prom.get('RUBRIC_CHANGE_CANDIDATE',''):
    errors.append('rubric-change candidate bypasses formal adoption/version migration')

# Engine routing is derived from structured activation, not authority inversion.
node20=next((x for x in overlay.get('node_overlays',[]) if x.get('asi_node_id')=='ASI-NODE-20'),{})
if 'assign execution authority to a reasoning Engine' not in ' '.join(node20.get('must_not_do',[])):
    errors.append('Node-20 missing Engine-authority guard')

report={
  'report_id':'P2-MICRO-SEQUENCE-PATTERN-RFR-V1',
  'status':'PASS' if not errors else 'FAIL',
  'pass0':{
    'declared_end':'Every sentence/event is represented as a local micro-Sequence and can contribute to versioned, reviewable patterns without inference/fact or candidate/rubric collapse.',
    'scope':'runtime + schema + small-brain ownership + Engine routing + editable review + pattern writeback'
  },
  'pass1':{
    'runtime_stage_count':len(stages),
    'engine_route_count':len(route_ids),
    'schema_object_count':len(required_defs),
    'pattern_namespace_count':len(namespaces),
    'ui_panel_count':len(panel_ids),
    'small_brain_overlay_count':len(overlay_nodes),
    'fixture_occurrence_count':len(occ)
  },
  'pass2':{
    'engine_refs':sorted(set(referenced_engines)),
    'engine_ref_count':len(set(referenced_engines)),
    'asi_node_refs':sorted(set(referenced_nodes)),
    'asi_node_ref_count':len(set(referenced_nodes)),
    'fixture_pattern_candidate_creation_justified':fixture.get('expected_pattern_contribution',{}).get('candidate_creation_justified'),
    'fixture_user_approval_scope':review.get('user_edit_example',{}).get('approval_scope')
  },
  'pass3':{
    'invariants':{
      'EVERY_INPUT_CREATES_LOCAL_MICRO_SEQUENCE':runtime.get('core_rule')=='EVERY_INPUT_UTTERANCE_CREATES_AT_LEAST_ONE_LOCAL_MICRO_SEQUENCE',
      'OBSERVATION_INTERPRETATION_SEPARATED':'OBSERVATION != INTERPRETATION' in non_eq,
      'INTENT_NOT_AUTO_FACT':'INTERPRETATION != INTENT_FACT' in non_eq,
      'PATTERN_CANDIDATE_NOT_APPROVED_RUBRIC':'PATTERN_CANDIDATE != APPROVED_RUBRIC' in non_eq,
      'NO_AUTOMATIC_PATTERN_PROMOTION':runtime.get('pattern_formation_rule',{}).get('automatic_promotion') is False,
      'USER_EDIT_VERSIONED':review.get('expected_writeback')=='NEW_VERSIONED_RELATIONSHIP_PATTERN',
      'ENGINE_NOT_AUTHORITY':'ENGINE_OUTPUT != EXECUTION_AUTHORITY' in non_eq,
      'RGL_NOT_IN_PLACE_LOOP':'RGL recursion cannot become an unbounded in-place loop' in routing_laws,
      'META_NOT_DEFAULT_LOCAL_ANALYSIS':'META is invoked for meta-governance/conflict/priority' in routing_laws,
      'CLOSED_SEQUENCES_NOT_REOPENED':'Closed supporting Sequences never reopen' in immut
    }
  },
  'errors':errors,
  'findings':findings
}
(GEN/'P2_MICRO_SEQUENCE_PATTERN_RFR_V1.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
sys.exit(1 if errors else 0)
