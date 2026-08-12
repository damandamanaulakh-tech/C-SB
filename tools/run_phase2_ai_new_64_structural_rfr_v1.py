#!/usr/bin/env python3
from pathlib import Path
import json, sys, re, hashlib
from collections import Counter

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'generated/tests'
OUT.mkdir(parents=True, exist_ok=True)
errors=[]
findings=[]

def load(rel):
    p=ROOT/rel
    if not p.exists():
        errors.append(f'missing:{rel}')
        return {}
    return json.loads(p.read_text(encoding='utf-8'))

src=load('registries/ai/AI_ONLY_RECORDS_64_APPROVED_V1.json')
contract=load('machine/ai/AI_NEW_64_STRUCTURAL_DECOMPOSITION_CONTRACT_V1.json')
dec=load('generated/registry_views/ai_new_64_structural_decomposition_v1.json')

src_by={r[0]:r for r in src.get('records',[])}
dec_by={r.get('ai_only_id'):r for r in dec.get('records',[])}
expected_ids=[f'AI-NEW-{i:03d}' for i in range(1,65)]
if list(src_by) != expected_ids: errors.append('source IDs are not exact AI-NEW-001..064 ordered set')
if list(dec_by) != expected_ids: errors.append('decomposition IDs are not exact AI-NEW-001..064 ordered set')
if dec.get('record_count') != 64: errors.append('decomposition record_count != 64')

expected_form_counts=Counter()
for rid in expected_ids:
    row=src_by.get(rid)
    d=dec_by.get(rid)
    if not row or not d: continue
    _,name,level,lineage=row
    if d.get('source_name') != name: errors.append(f'{rid}:source name drift')
    if d.get('source_structural_level') != level: errors.append(f'{rid}:source level drift')
    expected_form=contract.get('runtime_form_by_source_level',{}).get(level)
    if d.get('runtime_form') != expected_form: errors.append(f'{rid}:runtime form mismatch')
    expected_form_counts[expected_form]+=1
    source_payload=json.dumps(row,ensure_ascii=False,separators=(',',':')).encode('utf-8')
    if d.get('source_record_sha256') != hashlib.sha256(source_payload).hexdigest(): errors.append(f'{rid}:source record hash drift')
    is_comp=rid in contract.get('composite_candidates',{})
    if is_comp:
        if d.get('atomicity')!='COMPOSITE_CANDIDATE': errors.append(f'{rid}:composite flag missing')
        if d.get('composite_components') != contract['composite_candidates'][rid]: errors.append(f'{rid}:composite components drift')
        if not d.get('composite_components'): errors.append(f'{rid}:composite has no components')
    else:
        if d.get('atomicity')!='ATOMIC_AT_APPROVED_SOURCE_SCOPE': errors.append(f'{rid}:unexpected composite flag')
    if not d.get('primary_sequence_roles'):
        errors.append(f'{rid}:no primary Sequence role')
    form=d.get('runtime_form')
    own=d.get('mechanism_ownership','')
    if form in {'CONTROL','META_CONTROL'} and own.startswith('AI_PRIMARY'):
        errors.append(f'{rid}:control illegally classified AI_PRIMARY authority')
    if form=='STATE' and 'state itself does not close a Sequence' not in d.get('closure_contract',''):
        errors.append(f'{rid}:state closure law lost')
    if form=='EVIDENCE_CONTROL' and 'evidence' not in d.get('closure_contract','').lower():
        errors.append(f'{rid}:evidence-control closure contract missing evidence semantics')
    engine_ids=d.get('direct_engine_ids',[])
    engine_evidence=d.get('direct_engine_evidence',[])
    if engine_ids and not engine_evidence:
        errors.append(f'{rid}:direct Engine IDs lack source evidence')
    if not engine_ids and d.get('engine_binding_status')!='ENGINE_BINDING_OPEN_NO_EXACT_SOURCE_RELATION':
        errors.append(f'{rid}:engine gap status inconsistent')
    if engine_ids and d.get('engine_binding_status')!='SOURCE_DERIVED_DIRECT_BINDING':
        errors.append(f'{rid}:source-derived Engine binding status inconsistent')
    for eng in engine_ids:
        if not re.fullmatch(r'ENG-[A-Z0-9]+-\d{3}',eng): errors.append(f'{rid}:malformed Engine ID {eng}')
    if d.get('source_binding_status')=='GAP_REVIEW_REQUIRED':
        findings.append(f'{rid}:prior source binding remains GAP_REVIEW_REQUIRED')

source_level_counts=Counter(r[2] for r in src.get('records',[]))
expected_source_level_counts={
    'Operational parameter':19,
    'Control parameter':14,
    'Universal filter':19,
    'Evidence-control parameter':7,
    'Master control parameter':3,
    'Operating state':1,
    'Operating state or parameter':1,
}
if dict(source_level_counts) != expected_source_level_counts:
    errors.append(f'source-level distribution drift:{dict(source_level_counts)}')
if len(contract.get('composite_candidates',{})) != 11:
    errors.append('composite candidate count drift')

engine_open=sum(1 for r in dec.get('records',[]) if r.get('engine_binding_status')=='ENGINE_BINDING_OPEN_NO_EXACT_SOURCE_RELATION')
engine_bound=64-engine_open
if engine_open:
    findings.append(f'{engine_open} AI-NEW records have no exact direct Engine relation; gaps preserved rather than guessed')

invariants={
    'SOURCE_IDENTITY_PRESERVED': not any('source name drift' in e or 'source level drift' in e or 'source record hash drift' in e for e in errors),
    'ALL_64_STRUCTURALLY_CLASSIFIED': len(dec_by)==64 and not any('runtime form mismatch' in e for e in errors),
    'COMPOSITES_NOT_SILENTLY_SPLIT_OR_FLATTENED': not any('composite' in e for e in errors),
    'AI_CONTROL_HAS_NO_IMPLICIT_PERMISSION_AUTHORITY': not any('illegally classified AI_PRIMARY authority' in e for e in errors),
    'STATE_IS_NOT_SEQUENCE_CLOSURE': not any('state closure law lost' in e for e in errors),
    'DIRECT_ENGINE_BINDING_REQUIRES_SOURCE_EVIDENCE': not any('Engine' in e and 'source evidence' in e for e in errors),
    'ENGINE_GAPS_PRESERVED': all((r.get('direct_engine_ids') or r.get('engine_binding_status')=='ENGINE_BINDING_OPEN_NO_EXACT_SOURCE_RELATION') for r in dec.get('records',[])),
    'PRIMARY_SEQUENCE_ROLE_PRESENT': not any('no primary Sequence role' in e for e in errors),
}

report={
    'report_id':'P2-AI-NEW-64-STRUCTURAL-RFR-V1',
    'status':'FAIL' if errors else ('PASS_WITH_SOURCE_GAPS' if findings else 'PASS'),
    'scope_note':'Structural/runtime decomposition of approved AI-NEW-001..064. PASS does not promote Phase-2 crosswalks to source fact and does not invent direct Engine relations.',
    'pass0':{
        'declared_end':'All 64 approved AI-only records have source-preserving runtime-form, atomicity, ownership, Sequence/memory and Engine-binding status.',
        'closure_scope':'AI-NEW structural decomposition only; not final AI/ASI ontology closure'
    },
    'pass1':{
        'source_record_count':len(src_by),
        'source_level_counts':dict(source_level_counts),
        'runtime_form_counts':dec.get('summary',{}).get('runtime_form_counts',{}),
        'composite_candidate_count':len(contract.get('composite_candidates',{}))
    },
    'pass2':{
        'ownership_counts':dec.get('summary',{}).get('ownership_counts',{}),
        'engine_binding_counts':{'source_derived_direct':engine_bound,'open_no_exact_source_relation':engine_open},
        'governance_patch_count':dec.get('summary',{}).get('governance_patch_count')
    },
    'pass3':{
        'invariant_checks':invariants,
        'source_records_rewritten':False,
        'guessed_engine_bindings_allowed':False,
        'closed_sequence_reopen_used':False
    },
    'errors':errors,
    'findings':findings,
}
(OUT/'P2_AI_NEW_64_STRUCTURAL_RFR_V1.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(report['status'], 'errors',len(errors),'findings',len(findings))
sys.exit(1 if errors else 0)
