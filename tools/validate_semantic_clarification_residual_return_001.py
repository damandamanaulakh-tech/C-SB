#!/usr/bin/env python3
from pathlib import Path
import json, sys

ROOT=Path(__file__).resolve().parents[1]
FIX=ROOT/'phase2/tests/SEMANTIC_CLARIFICATION_RESIDUAL_RETURN_001.json'
HUM=ROOT/'registries/human/HUMAN_CONTAINER_INDEX_80_APPROVED_V1.json'
RUB=ROOT/'machine/rubrics/RUBRIC_REGISTRY_R01_R52.json'
SCH=ROOT/'machine/schemas/semantic_clarification.schema.json'
GEN=ROOT/'generated/tests'
GEN.mkdir(parents=True,exist_ok=True)

errors=[]; findings=[]

def load(p): return json.loads(p.read_text(encoding='utf-8'))

for p in [FIX,HUM,RUB,SCH]:
    if not p.exists(): errors.append(f'missing required file: {p.relative_to(ROOT)}')

if errors:
    report={'report_id':'P2-SEMANTIC-CLARIFICATION-RESIDUAL-RETURN-RFR-001','status':'FAIL','errors':errors,'findings':findings}
    (GEN/'P2_SEMANTIC_CLARIFICATION_RESIDUAL_RETURN_RFR_001.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
    print(json.dumps(report,indent=2)); sys.exit(1)

fx=load(FIX); human=load(HUM); rub=load(RUB)

# Approved Human container IDs/names.
hidx={row[0]:row[1] for seg in human.get('segments',[]) for row in seg.get('containers',[])}
ridx=set(rub.get('rubrics',{}).keys())

if fx.get('source',{}).get('source_immutable') is not True:
    errors.append('raw source is not locked immutable')

sc={x.get('clarification_id'):x for x in fx.get('semantic_clarifications',[])}
for req in ['SC-LEFT-001','SC-NOTHING-001','SC-GOOD-001']:
    if req not in sc: errors.append(f'missing semantic clarification {req}')

left=sc.get('SC-LEFT-001',{})
if left:
    if 'RESIDUAL_OUTCOME' not in str(left.get('semantic_relation_type','')):
        errors.append('left clarification is not residual-outcome typed')
    rejected={str(x).lower() for x in left.get('rejected_senses',[])}
    for term in ['departed','died','walked away']:
        if term not in rejected: errors.append(f'left clarification does not reject {term}')
    if left.get('downstream_recompute_required') is not True:
        errors.append('left clarification does not force downstream recompute')
    if left.get('source_remains_immutable') is not True or left.get('universalization_allowed') is not False:
        errors.append('left clarification violates source/scope guard')

nothing=sc.get('SC-NOTHING-001',{})
if nothing:
    dims=set(nothing.get('dimension_scope',[]))
    if 'MATERIAL_RETURN' not in dims:
        errors.append('nothing clarification is not scoped to MATERIAL_RETURN')
    text=json.dumps(nothing).lower()
    for guard in ['zero emotional return','zero experiential return','zero memory value by definition']:
        if guard not in text: errors.append(f'nothing clarification missing rejected totalization guard: {guard}')
    if nothing.get('universalization_allowed') is not False:
        errors.append('nothing clarification can universalize')

good=sc.get('SC-GOOD-001',{})
if good:
    if good.get('scope')!='USER_VALUE_LABEL_CANDIDATE':
        errors.append('good-person clarification is not kept as USER_VALUE_LABEL_CANDIDATE')
    if good.get('universalization_allowed') is not False:
        errors.append('good-person label can universalize')
    rejected=' '.join(str(x).lower() for x in good.get('rejected_senses',[]))
    if 'automatically good' not in rejected or 'self-sacrifice alone' not in rejected:
        errors.append('good-person overgeneralization guards missing')

ret=fx.get('dimensional_return',{})
if ret.get('zero_in_one_dimension_does_not_imply_zero_total') is not True:
    errors.append('return dimensions permit one zero dimension to erase total return')
if ret.get('total_return_unknown') is not True:
    errors.append('total return is falsely treated as fully known')
for d in ['material','emotional','experiential','memory']:
    if d not in ret.get('dimensions',{}): errors.append(f'missing return dimension {d}')

hrc=fx.get('human_rubric_change_candidate',{})
if hrc.get('status')!='REVIEW_REQUIRED': errors.append('Human rubric change candidate auto-promoted')
if hrc.get('direct_action_authority') is not False: errors.append('Human rubric change candidate gained action authority')
stmt=str(hrc.get('statement','')).lower()
if 'separately from positive/negative valence' not in stmt:
    errors.append('memory significance/valence separation missing from Human rubric candidate')
if 'user_review_required' not in str(hrc.get('approval_authority','')).lower():
    errors.append('Human rubric candidate lacks explicit user approval authority')

for cid in fx.get('candidate_human_container_activation',[]):
    if cid not in hidx: errors.append(f'unknown Human container ref {cid}')
for rid in fx.get('candidate_universal_rubrics',[]):
    if rid not in ridx: errors.append(f'unknown rubric ref {rid}')

for p in fx.get('pattern_candidates',[]):
    if p.get('status')!='REVIEW_REQUIRED': errors.append(f"pattern {p.get('pattern_candidate_id')} auto-promoted")
    if p.get('direct_action_authority') is not False: errors.append(f"pattern {p.get('pattern_candidate_id')} gained action authority")
comb=fx.get('combined_pattern_candidate',{})
if comb.get('status')!='REVIEW_REQUIRED' or comb.get('direct_action_authority') is not False:
    errors.append('combined care/residue/duty pattern is not review-only/advisory')
if comb.get('counter_cases_required_before_generalization') is not True:
    errors.append('combined pattern lacks counter-case gate')

rec=fx.get('sequence_recurrence_model',{})
valid=' '.join(rec.get('sourceborn_model',[])).lower()
if 'closes' not in valid or 'seed' not in valid or 'sequence s_n+1' not in valid or 'immutable' not in valid:
    errors.append('responsibility recurrence is not encoded as close -> Seed -> new Sequence')
if 'in-place loop' not in str(rec.get('invalid_model','')).lower():
    errors.append('invalid in-place loop form is not explicitly rejected')

# Semantic clarification schema must contain all three first-class object types.
defs=load(SCH).get('$defs',{})
for name in ['SemanticClarificationPacket','DimensionalReturnPacket','HumanRubricChangeCandidate']:
    if name not in defs: errors.append(f'semantic schema missing {name}')

report={
  'report_id':'P2-SEMANTIC-CLARIFICATION-RESIDUAL-RETURN-RFR-001',
  'status':'PASS' if not errors else 'FAIL',
  'checks':{
    'source_immutable':fx.get('source',{}).get('source_immutable') is True,
    'semantic_clarification_count':len(fx.get('semantic_clarifications',[])),
    'human_container_refs_checked':len(fx.get('candidate_human_container_activation',[])),
    'rubric_refs_checked':len(fx.get('candidate_universal_rubrics',[])),
    'pattern_candidates':len(fx.get('pattern_candidates',[])),
    'memory_significance_separate_from_valence':'separately from positive/negative valence' in stmt,
    'return_is_dimensional':ret.get('zero_in_one_dimension_does_not_imply_zero_total') is True,
    'recurrence_uses_seed_new_sequence':('seed' in valid and 'sequence s_n+1' in valid)
  },
  'errors':errors,
  'findings':findings
}
(GEN/'P2_SEMANTIC_CLARIFICATION_RESIDUAL_RETURN_RFR_001.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
sys.exit(1 if errors else 0)
