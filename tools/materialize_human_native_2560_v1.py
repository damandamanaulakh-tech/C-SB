#!/usr/bin/env python3
from pathlib import Path
import base64, gzip, hashlib, json, csv, io, re, sys

ROOT=Path(__file__).resolve().parents[1]
PARTS=ROOT/'raw/human/task3_human_native_parts'
OUT=ROOT/'generated/registry_views'
OUT.mkdir(parents=True,exist_ok=True)
REPORT=ROOT/'generated/tests'
REPORT.mkdir(parents=True,exist_ok=True)

pid_rx=re.compile(r'^SB-ASI-P(\d{4})$')
con_rx=re.compile(r'^CON-(\d{3})$')
seg_rx=re.compile(r'^SEG-(\d{2})$')
part_paths=sorted(PARTS.glob('part-*.tsv.gz.b64'))
errors=[]
transport_findings=[]
if not part_paths:
    errors.append('no Human custody parts found')

def parse_param_rows(text):
    rows=list(csv.reader(io.StringIO(text),delimiter='\t')) if text else []
    param=[]
    for i,row in enumerate(rows):
        pids=[c for c in row if pid_rx.fullmatch(c)]
        if pids:
            param.append((i,row,pids[0]))
    return rows,param

# Probe every file independently first. Filenames end in .tsv.gz.b64, so this is the preferred legal transport form.
part_diagnostics=[]
independent_texts=[]
all_independent_valid=bool(part_paths)
for p in part_paths:
    encoded=''.join(p.read_text(encoding='utf-8').split())
    diag={
        'path':str(p.relative_to(ROOT)),
        'file_size':p.stat().st_size,
        'file_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),
        'encoded_chars':len(encoded),
        'encoded_length_mod4':len(encoded)%4,
        'base64_prefix':encoded[:8],
        'base64_suffix':encoded[-8:] if encoded else '',
        'padding_chars':len(encoded)-len(encoded.rstrip('=')),
        'base64_valid':False,
        'gzip_valid':False,
        'gzip_bytes':0,
        'utf8_bytes':0,
        'tsv_rows_total':0,
        'parameter_rows':0,
        'first_parameter_id':None,
        'last_parameter_id':None,
        'container_count':0,
        'segment_count':0,
        'parameter_column_counts':[],
        'error':None,
    }
    try:
        gz=base64.b64decode(encoded,validate=True)
        diag['base64_valid']=True
        diag['gzip_bytes']=len(gz)
        try:
            txt=gzip.decompress(gz).decode('utf-8')
            diag['gzip_valid']=True
            diag['utf8_bytes']=len(txt.encode('utf-8'))
            rows,param=parse_param_rows(txt)
            ids=[x[2] for x in param]
            diag['tsv_rows_total']=len(rows)
            diag['parameter_rows']=len(param)
            diag['first_parameter_id']=ids[0] if ids else None
            diag['last_parameter_id']=ids[-1] if ids else None
            diag['container_count']=len({c for _,row,_ in param for c in row if con_rx.fullmatch(c)})
            diag['segment_count']=len({c for _,row,_ in param for c in row if seg_rx.fullmatch(c)})
            diag['parameter_column_counts']=sorted({len(row) for _,row,_ in param})
            independent_texts.append(txt)
        except Exception as e:
            all_independent_valid=False
            diag['error']=f'gzip/utf8:{type(e).__name__}:{e}'
    except Exception as e:
        all_independent_valid=False
        diag['error']=f'base64:{type(e).__name__}:{e}'
    part_diagnostics.append(diag)

transport_mode=None
raw_gz=b''
text=''
if all_independent_valid and len(independent_texts)==len(part_paths):
    transport_mode='INDEPENDENT_GZIP_BASE64_PARTS'
    # Exact concatenation of decompressed chunk payloads. No newline or delimiter is invented.
    text=''.join(independent_texts)
    transport_findings.append('Each custody file independently decoded as base64(gzip(UTF-8)); decompressed payloads concatenated in filename order.')
else:
    # Fallback for a single base64 stream split over files. Whitespace is transport-only and removed.
    joined=''.join(''.join(p.read_text(encoding='utf-8').split()) for p in part_paths)
    try:
        raw_gz=base64.b64decode(joined,validate=True)
        try:
            text=gzip.decompress(raw_gz).decode('utf-8')
            transport_mode='CONCATENATED_BASE64_SINGLE_GZIP'
            transport_findings.append('Independent-part decoding failed; concatenated base64 stream decoded successfully.')
        except Exception as e:
            errors.append(f'concatenated gzip/utf8 decode failed:{type(e).__name__}:{e}')
    except Exception as e:
        errors.append(f'neither independent nor concatenated base64 transport decoded:{type(e).__name__}:{e}')

rows,param_rows=parse_param_rows(text)
ids=[x[2] for x in param_rows]
expected=[f'SB-ASI-P{i:04d}' for i in range(1,2561)]
containers=sorted({c for _,row,_ in param_rows for c in row if con_rx.fullmatch(c)})
segments=sorted({c for _,row,_ in param_rows for c in row if seg_rx.fullmatch(c)})
column_counts=sorted({len(row) for _,row,_ in param_rows})

if ids != expected:
    if ids:
        missing=[pid for pid in expected if pid not in set(ids)]
        errors.append(f'parameter ID coverage mismatch count={len(ids)} first={ids[0]} last={ids[-1]} missing_count={len(missing)} first_missing={missing[0] if missing else None}')
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

joined_encoded=''.join(''.join(p.read_text(encoding='utf-8').split()) for p in part_paths)
hashes={
    'ordered_part_file_sha256s':[d['file_sha256'] for d in part_diagnostics],
    'joined_transport_text_sha256':hashlib.sha256(joined_encoded.encode('ascii')).hexdigest() if joined_encoded else None,
    'single_gzip_payload_sha256':hashlib.sha256(raw_gz).hexdigest() if raw_gz else None,
    'reconstructed_tsv_sha256':hashlib.sha256(text.encode('utf-8')).hexdigest() if text else None,
}

report={
    'report_id':'P2-HUMAN-2560-CUSTODY-PROBE-V1',
    'status':'FAIL_INCOMPLETE_OR_INVALID' if errors else 'PASS_COMPLETE_CUSTODY',
    'transport_mode':transport_mode,
    'transport_findings':transport_findings,
    'part_count':len(part_paths),
    'part_diagnostics':part_diagnostics,
    'decoded':{
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
        'transport_mode':transport_mode,
        'source_custody_parts':[d['path'] for d in part_diagnostics],
        'source_hashes':hashes,
        'record_count':len(param_rows),
        'container_count':len(containers),
        'segment_count':len(segments),
        'header':rows[0] if rows and not any(pid_rx.fullmatch(c) for c in rows[0]) else None,
        'records':[row for _,row,_ in param_rows],
    }
    (OUT/'human_native_2560_registry_v1.json').write_text(json.dumps(registry,ensure_ascii=False,indent=2),encoding='utf-8')

compact_parts=[{k:d[k] for k in ['path','base64_valid','gzip_valid','parameter_rows','first_parameter_id','last_parameter_id','container_count','segment_count','parameter_column_counts','error']} for d in part_diagnostics]
print(report['status'],'transport',transport_mode,'decoded',json.dumps(report['decoded'],sort_keys=True),'parts',json.dumps(compact_parts,sort_keys=True),'errors',json.dumps(errors))
sys.exit(1 if errors else 0)
