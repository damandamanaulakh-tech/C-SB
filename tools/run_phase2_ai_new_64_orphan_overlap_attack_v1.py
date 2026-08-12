#!/usr/bin/env python3
from pathlib import Path
import json, sys
from collections import Counter, defaultdict

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

dec=load('generated/registry_views/ai_new_64_structural_decomposition_v1.json')
ai_view=load('generated/registry_views/ai_native_runtime_view_v1.json')
asi_view=load('generated/registry_views/asi_governance_interface_view_from_ai_new_v1.json')
ov=load('machine/ai/AI_NEW_64_OVERLAP_CLUSTERS_V1.json')

records={r['ai_only_id']:r for r in dec.get('records',[])}
ai_records={r['ai_only_id']:r for r in ai_view.get('records',[])}
expected={f'AI-NEW-{i:03d}' for i in range(1,65)}
if set(records)!=expected: errors.append('decomposition does not contain exact 64 IDs')
if set(ai_records)!=expected: errors.append('AI runtime view does not contain exact 64 IDs')

hard_orphans=[]
governance_orphans=[]
node_orphans=[]
engine_gaps=[]
over_broad=[]
requires_gov={'CONTROL','FILTER','EVIDENCE_CONTROL','META_CONTROL','STATE'}
for rid in sorted(expected):
    r=records.get(rid,{})
    if not r.get('phase2_ai_segments') or not r.get('primary_sequence_roles'):
        hard_orphans.append(rid)
    if r.get('runtime_form') in requires_gov and not r.get('phase2_asi_segments'):
        governance_orphans.append(rid)
    if r.get('runtime_form') in requires_gov and not r.get('phase2_asi_nodes'):
        node_orphans.append(rid)
    if r.get('engine_binding_status')=='ENGINE_BINDING_OPEN_NO_EXACT_SOURCE_RELATION':
        engine_gaps.append(rid)
    breadth={
        'ai_segments':len(r.get('phase2_ai_segments',[])),
        'asi_segments':len(r.get('phase2_asi_segments',[])),
        'asi_nodes':len(r.get('phase2_asi_nodes',[])),
        'primary_sequence_roles':len(r.get('primary_sequence_roles',[])),
    }
    if breadth['ai_segments']>6 or breadth['asi_segments']>6 or breadth['asi_nodes']>10 or breadth['primary_sequence_roles']>12:
        over_broad.append({'ai_only_id':rid,'source_name':r.get('source_name'),'breadth':breadth,'status':'REVIEW_MAPPING_BREADTH_NOT_SOURCE_FAILURE'})

if hard_orphans: errors.append(f'hard orphans:{hard_orphans}')
if governance_orphans: errors.append(f'governance orphans:{governance_orphans}')
if node_orphans: errors.append(f'node orphans:{node_orphans}')

cluster_membership=defaultdict(list)
cluster_results=[]
for c in ov.get('clusters',[]):
    missing=[rid for rid in c['ids'] if rid not in expected]
    if missing: errors.append(f"{c['cluster_id']}:unknown IDs:{missing}")
    for rid in c['ids']: cluster_membership[rid].append(c['cluster_id'])
    cluster_results.append({
        'cluster_id':c['cluster_id'],
        'name':c['name'],
        'record_count':len(c['ids']),
        'expected_relation':c['expected_relation'],
        'duplicate_hypothesis':c['duplicate_hypothesis'],
        'auto_merge_allowed':False,
    })

unclustered=sorted(expected-set(cluster_membership))
if unclustered: findings.append(f'unclustered records:{unclustered}')

pair_results=[]
for p in ov.get('targeted_pairs',[]):
    a,b=p['ids']
    ra,rb=records[a],records[b]
    exact_runtime_equivalence=(
        ra['runtime_form']==rb['runtime_form'] and
        set(ra['phase2_ai_segments'])==set(rb['phase2_ai_segments']) and
        set(ra['phase2_asi_segments'])==set(rb['phase2_asi_segments']) and
        set(ra['primary_sequence_roles'])==set(rb['primary_sequence_roles']) and
        set(ra['state_ownership_candidates'])==set(rb['state_ownership_candidates']) and
        ra['activation_contract']==rb['activation_contract'] and
        ra['closure_contract']==rb['closure_contract']
    )
    pair_results.append({
        'ids':[a,b],
        'question':p['question'],
        'default':p['default'],
        'exact_runtime_equivalence':exact_runtime_equivalence,
        'merge_status':'REQUIRES_EXPLICIT_SOURCE_AND_TEST_DECISION' if exact_runtime_equivalence else 'KEEP_SEPARATE_RUNTIME_CONTRACTS_DIFFER',
    })
    if exact_runtime_equivalence:
        findings.append(f'{a}/{b}: runtime signatures equivalent; explicit duplicate review required')

asi_segment_counts={s['asi_segment_id']:s['ai_new_interface_count'] for s in asi_view.get('segments',[])}
unused_asi_segments=sorted([sid for sid,c in asi_segment_counts.items() if c==0])
if unused_asi_segments:
    findings.append(f'ASI segments with no AI-NEW interface in this bounded view:{unused_asi_segments}')
if engine_gaps:
    findings.append(f'{len(engine_gaps)} direct Engine source gaps preserved; not counted as AI orphans')
if over_broad:
    findings.append(f'{len(over_broad)} records exceed mapping-breadth review thresholds; source records remain valid')

invariants={
    'NO_HARD_AI_ORPHANS':not hard_orphans,
    'NO_GOVERNANCE_ORPHANS_FOR_CONTROL_LIKE_RECORDS':not governance_orphans,
    'NO_ASI_NODE_ORPHANS_FOR_CONTROL_LIKE_RECORDS':not node_orphans,
    'ENGINE_SOURCE_GAP_NOT_FORCE_FIT':len(engine_gaps)==sum(1 for r in records.values() if not r.get('direct_engine_ids')),
    'NO_AUTOMATIC_MERGE_FROM_OVERLAP':all(not c['auto_merge_allowed'] for c in cluster_results),
    'ALL_TARGETED_OVERLAPS_RETAIN_REVIEW_BOUNDARY':all(p['merge_status'] in {'REQUIRES_EXPLICIT_SOURCE_AND_TEST_DECISION','KEEP_SEPARATE_RUNTIME_CONTRACTS_DIFFER'} for p in pair_results),
    'AI_VIEW_PRESERVES_64_SOURCE_IDENTITIES':set(ai_records)==expected,
}
for k,v in invariants.items():
    if not v: errors.append(f'invariant failed:{k}')

report={
    'report_id':'P2-AI-NEW-64-ORPHAN-OVERLAP-ATTACK-V1',
    'status':'FAIL' if errors else ('PASS_WITH_REVIEW_FINDINGS' if findings else 'PASS'),
    'scope_note':'Orphan, governance-path, mapping-breadth and semantic-overlap attack for AI-NEW-001..064. Engine gaps are source gaps, not silently treated as runtime proof.',
    'pass0':{
        'declared_end':'No approved AI-NEW record is orphaned or silently merged; overlap and breadth risks remain machine-visible.',
        'scope':'AI-NEW-001..064 plus derived AI runtime and ASI governance interface views'
    },
    'pass1':{
        'records':len(records),
        'hard_orphans':hard_orphans,
        'governance_orphans':governance_orphans,
        'node_orphans':node_orphans,
        'engine_source_gaps':len(engine_gaps)
    },
    'pass2':{
        'overlap_clusters':cluster_results,
        'targeted_pairs':pair_results,
        'over_broad_mapping_review':over_broad,
        'unclustered_records':unclustered,
        'asi_segment_interface_counts':asi_segment_counts
    },
    'pass3':{
        'invariant_checks':invariants,
        'auto_merge_performed':False,
        'engine_force_fit_performed':False,
        'source_record_rewrite_performed':False
    },
    'errors':errors,
    'findings':findings,
}
(OUT/'P2_AI_NEW_64_ORPHAN_OVERLAP_ATTACK_V1.json').write_text(json.dumps(report,indent=2),encoding='utf-8')
print(report['status'],'errors',len(errors),'findings',len(findings),'over_broad',len(over_broad))
sys.exit(1 if errors else 0)
