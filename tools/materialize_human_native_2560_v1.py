#!/usr/bin/env python3
from pathlib import Path
import base64, gzip, hashlib, json, csv, io, re, sys

ROOT=Path(__file__).resolve().parents[1]
PARTS=ROOT/'raw/human/task3_human_native_parts'
OUT=ROOT/'generated/registry_views'
OUT.mkdir(parents=True,exist_ok=True)
REPORT=ROOT/'generated/tests'
REPORT.mkdir(parents=True,exist_ok=True)

part_paths=sorted(PARTS.glob('part-*.tsv.gz.b64'))
errors=[]
if not part_paths:
    errors.append('no Human custody parts found')

joined=''.join(p.read_text(encoding='utf-8').strip() for p in part_paths)
raw_gz=b''
text=''
try:
    raw_gz=base64.b64decode(joined, validate=True)
except Exception as e:
    errors.append(f'base64 decode failed:{type(e).__name__}:{e}')
if raw_gz:
    try:
        text=gzip.decompress(raw_gz).decode('utf-8')
    except Exception as e:
        errors.append(f'gzip/utf8 decode failed:{type(e).__name__}:{e}')

rows=[]
if text:
    rows=list(csv.reader(io.StringIO(text), delimiter='\t'))

pid_rx=re.compile(r'^SB-ASI-P(\d{4})$')
con_rx=re.compile(r'^CON-(\d{3})$')
seg_rx=re.compile(r'^SEG-(\d{2})$')
param_rows=[]
for i,row in enumerate(rows):
    pids=[c for c in row if pid_rx.fullmatch(c)]
    if pids:
        param_rows.append((i,row,pids[0]))

ids=[x[2] for x in param_rows]
expected=[f'SB-ASI-P{i:04d}' for i in range(1,2561)]
containers=sorted({c for _,row,_ in param_rows for c in row if con_rx.fullmatch(c)})
segments=sorted({c for _,row,_ in param_rows for c in row if seg_rx.fullmatch(c)})
column_counts=sorted({len(row) for _,row,_ in param_rows})

if ids != expected:
    if ids:
        errors.append(f'parameter ID coverage mismatch count={len(ids)} first={ids[0]} last={ids[-1]}')
    else:
        errors.append('no SB-ASI-Pxxxx parameter rows reconstructed')
if len(containers)!=80: errors.append(f'container coverage !=80 actual={len(containers)}')
if len(segments)!=10: errors.append(f'segment coverage !=10 actual={len(segments)}')
if column_counts != [13]: errors.append(f'parameter row column counts !=[13] actual={column_counts}')

approval_count=sum(1 for _,row,_ in param_rows if 'APPROVED BY USER' in row)
evidence_count=sum(1 for _,row,_ in param_rows if 'USER EVIDENT' in row)
brain_base_count=sum(1 for _,row,_ in param_rows if 'Canonical Brain Base' in row)
if param_rows and approval_count!=len(param_rows): errors.append(f'APPROVED BY USER coverage {approval_count}/{len(param_rows)}')
if param_rows and evidence_count!=len(param_rows): errors.append(f'USER EVIDENT coverage {evidence_count}/{len(param_rows)}')
if param_rows and brain_base_count!=len(param_rows): errors.append(f'Canonical Brain Base coverage {brain_base_count}/{len(param_rows)}')

hashes={
    'joined_base64_sha256':hashlib.sha256(joined.encode('ascii')).hexdigest() if joined else None,
    'gzip_payload_sha256':hashlib.sha256(raw_gz).hexdigest() if raw_gz else None,
    'decompressed_tsv_sha256':hashlib.sha256(text.encode('utf-8')).hexdigest() if text else None,
}
part_manifest=[{'path':str(p.relative_to(ROOT)),'size':p.stat().st_size,'sha256':hashlib.sha256(p.read_bytes()).hexdigest()} for p in part_paths]

report={
    'report_id':'P2-HUMAN-2560-CUSTODY-PROBE-V1',
    'status':'FAIL_INCOMPLETE_OR_INVALID' if errors else 'PASS_COMPLETE_CUSTODY',
    'part_count':len(part_paths),
    'parts':part_manifest,
    'decoded':{
        'gzip_bytes':len(raw_gz),
        'utf8_bytes':len(text.encode('utf-8')) if text else 0,
        'tsv_rows_total':len(rows),
        'parameter_rows':len(param_rows),
        'first_parameter_id':ids[0] if ids else None,
        'last_parameter_id':ids[-1] if ids else None,
        'container_count':len(containers),
        'segment_count':len(segments),
        'parameter_column_counts':column_counts,
        'approval_coverage':approval_count,
        'evidence_coverage':evidence_count,
        'canonical_brain_base_coverage':brain_base_count,
    },
    'hashes':hashes,
    'errors':errors,
}
(REPORT/'P2_HUMAN_2560_CUSTODY_PROBE_V1.json').write_text(json.dumps(report,indent=2),encoding='utf-8')

if not errors:
    (OUT/'human_native_2560_source_v1.tsv').write_text(text,encoding='utf-8')
    registry={
        'registry_id':'HUMAN-NATIVE-2560-SOURCE-V1',
        'status':'MATERIALIZED_EXACT_FROM_CUSTODY_PARTS',
        'source_custody_parts':[str(p.relative_to(ROOT)) for p in part_paths],
        'source_hashes':hashes,
        'record_count':len(param_rows),
        'container_count':len(containers),
        'segment_count':len(segments),
        'header':rows[0] if rows and not any(pid_rx.fullmatch(c) for c in rows[0]) else None,
        'records':[row for _,row,_ in param_rows],
    }
    (OUT/'human_native_2560_registry_v1.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2),encoding='utf-8')

print(report['status'],json.dumps(report['decoded'],sort_keys=True), 'errors',len(errors))
sys.exit(1 if errors else 0)
