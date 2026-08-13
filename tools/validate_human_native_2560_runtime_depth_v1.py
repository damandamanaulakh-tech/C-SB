#!/usr/bin/env python3
from pathlib import Path
import json, re, sys

ROOT=Path(__file__).resolve().parents[1]
MAP=ROOT/'machine/parameters/HUMAN_NATIVE_2560_RUNTIME_PLACEMENT_V1.json'
SRC=ROOT/'registries/human/HUMAN_CONTAINER_INDEX_80_APPROVED_V1.json'
GENERATED=ROOT/'generated/registry_views/human_native_2560_registry_v1.json'
REPORT=ROOT/'generated/tests/P2_HUMAN_2560_RUNTIME_DEPTH_RFR_V1.json'
REPORT.parent.mkdir(parents=True,exist_ok=True)

errors=[]
findings=[]

def load(p):
    try:
        return json.loads(p.read_text(encoding='utf-8'))
    except Exception as e:
        errors.append(f'cannot load {p.relative_to(ROOT)}: {type(e).__name__}: {e}')
        return {}

def pnum(pid):
    m=re.fullmatch(r'SB-ASI-P(\d{4})',pid or '')
    return int(m.group(1)) if m else None

m=load(MAP)
s=load(SRC)

bank=m.get('native_parameter_bank',{})
if bank.get('first_id')!='SB-ASI-P0001': errors.append('bank first ID != SB-ASI-P0001')
if bank.get('last_id')!='SB-ASI-P2560': errors.append('bank last ID != SB-ASI-P2560')
if bank.get('count')!=2560: errors.append('bank count != 2560')
if bank.get('container_count')!=80: errors.append('bank container_count != 80')
if bank.get('segment_count')!=10: errors.append('bank segment_count != 10')
if bank.get('canonical_layer')!='PARAMETER': errors.append('native Human bank must live at PARAMETER layer')

required_laws={
    'NATIVE_HUMAN_PARAMETER != RUBRIC',
    'NATIVE_HUMAN_PARAMETER != ASI_NODE',
    'NATIVE_HUMAN_PARAMETER != ENGINE',
    'NATIVE_HUMAN_PARAMETER != ELEMENT',
    'NATIVE_HUMAN_PARAMETER != SUB_PARAMETER',
    'NATIVE_HUMAN_PARAMETER != PATTERN',
    'RUBRIC_INTERROGATES_OR_CLASSIFIES_ACTIVATED_PARAMETERS',
    'PATTERN_EMERGES_FROM_COMPARISON_ACROSS_SEQUENCE_EVIDENCE'
}
missing=sorted(required_laws-set(m.get('layer_laws',[])))
if missing: errors.append('missing layer laws: '+','.join(missing))

# Source container truth: ID, segment ownership, count.
source_containers={}
for seg in s.get('segments',[]):
    sid=seg.get('segment_id')
    for row in seg.get('containers',[]):
        if not isinstance(row,list) or len(row)<3: continue
        source_containers[row[0]]={'segment_id':sid,'name':row[1],'count':row[2]}
if len(source_containers)!=80: errors.append(f'approved source container count !=80 actual={len(source_containers)}')

ranges=m.get('container_ranges',[])
if len(ranges)!=80: errors.append(f'mapped container range count !=80 actual={len(ranges)}')
prev=0
mapped_total=0
mapped_ids=[]
for i,row in enumerate(ranges,1):
    if not isinstance(row,list) or len(row)!=5:
        errors.append(f'container range row {i} malformed')
        continue
    cid,sid,start_id,end_id,count=row
    mapped_ids.append(cid)
    a,b=pnum(start_id),pnum(end_id)
    if a is None or b is None:
        errors.append(f'{cid} invalid parameter ID format')
        continue
    if a!=prev+1: errors.append(f'{cid} non-contiguous start expected={prev+1} actual={a}')
    if b<a: errors.append(f'{cid} end before start')
    actual=b-a+1
    if actual!=count: errors.append(f'{cid} range size {actual} != declared {count}')
    src=source_containers.get(cid)
    if not src:
        errors.append(f'{cid} absent from approved Human container index')
    else:
        if src['segment_id']!=sid: errors.append(f'{cid} segment mismatch map={sid} source={src["segment_id"]}')
        if src['count']!=count: errors.append(f'{cid} parameter count mismatch map={count} source={src["count"]}')
    mapped_total+=count
    prev=b

if mapped_ids != [f'CON-{i:03d}' for i in range(1,81)]: errors.append('container IDs are not exact CON-001..CON-080 order')
if mapped_total!=2560: errors.append(f'mapped total !=2560 actual={mapped_total}')
if prev!=2560: errors.append(f'final mapped parameter !=2560 actual={prev}')

# Segment ranges must be contiguous and equal the sum/envelope of their eight source containers.
segments=m.get('segments',[])
if len(segments)!=10: errors.append(f'segment mapping count !=10 actual={len(segments)}')
prev_seg=0
segment_counts={}
for row in ranges:
    if isinstance(row,list) and len(row)==5:
        segment_counts[row[1]]=segment_counts.get(row[1],0)+row[4]
for i,row in enumerate(segments,1):
    if not isinstance(row,list) or len(row)!=5:
        errors.append(f'segment row {i} malformed')
        continue
    sid,start_id,end_id,count,roles=row
    if sid!=f'SEG-{i:02d}': errors.append(f'segment order mismatch at {i}: {sid}')
    a,b=pnum(start_id),pnum(end_id)
    if a!=prev_seg+1: errors.append(f'{sid} non-contiguous segment start')
    if b-a+1!=count: errors.append(f'{sid} segment range size mismatch')
    if segment_counts.get(sid)!=count: errors.append(f'{sid} container sum {segment_counts.get(sid)} != segment count {count}')
    if not roles: errors.append(f'{sid} runtime roles missing')
    prev_seg=b
if prev_seg!=2560: errors.append(f'last segment does not end at P2560 actual={prev_seg}')

# The illustrative bundle is allowed only as non-universal candidate activation.
example=m.get('illustrative_social_pattern_bundle',{})
if example.get('status')!='ILLUSTRATIVE_NOT_UNIVERSAL_ACTIVATION': errors.append('illustrative social bundle lost non-universal guard')
for cid in example.get('container_ids',[]):
    if cid not in source_containers: errors.append(f'illustrative bundle references unknown container {cid}')
if 'candidate' not in example.get('epistemic_guard','').lower(): errors.append('illustrative bundle missing candidate epistemic guard')

# When the generated exact 2,560 registry exists, independently verify complete ID coverage.
generated_ids=[]
if GENERATED.exists():
    g=load(GENERATED)
    generated_ids=sorted(set(re.findall(r'SB-ASI-P\d{4}',json.dumps(g))))
    expected=[f'SB-ASI-P{i:04d}' for i in range(1,2561)]
    if generated_ids!=expected: errors.append(f'generated Human registry ID coverage mismatch actual={len(generated_ids)}')
else:
    findings.append('generated exact Human registry not present at validation time; source index/range validation still executed')

report={
    'report_id':'P2-HUMAN-2560-RUNTIME-DEPTH-RFR-V1',
    'status':'PASS' if not errors else 'FAIL',
    'mapping_id':m.get('mapping_id'),
    'checks':{
        'canonical_layer_parameter':bank.get('canonical_layer')=='PARAMETER',
        'container_ranges':len(ranges),
        'segment_ranges':len(segments),
        'mapped_parameter_total':mapped_total,
        'final_parameter_number':prev,
        'approved_source_container_count':len(source_containers),
        'generated_exact_parameter_ids_checked':len(generated_ids),
        'required_layer_laws_present':not missing,
        'illustrative_bundle_non_universal':example.get('status')=='ILLUSTRATIVE_NOT_UNIVERSAL_ACTIVATION'
    },
    'errors':errors,
    'findings':findings
}
REPORT.write_text(json.dumps(report,indent=2),encoding='utf-8')
print(json.dumps(report,indent=2))
sys.exit(1 if errors else 0)
