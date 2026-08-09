#!/usr/bin/env python3
from pathlib import Path
import json

ROOT=Path(__file__).resolve().parents[1]
SRC=ROOT/'generated/tests/P2_AI_ASI_STRUCTURAL_RFR_V1.json'
OUT=ROOT/'generated/tests/P2_AI_ASI_STRUCTURAL_RFR_FINDINGS_V1.json'
report=json.loads(SRC.read_text(encoding='utf-8'))

def nonclean(rows):
    return [
        {
            'id':r.get('id'),
            'status':r.get('status'),
            'findings':r.get('findings',[]),
            'hard_failures':r.get('hard_failures',[]),
            'pass1':r.get('pass1',{}),
            'pass2':r.get('pass2',{}),
            'pass3':r.get('pass3',{})
        }
        for r in rows if r.get('status') not in {'PASS'}
    ]

payload={
    'report_id':'P2-AI-ASI-STRUCTURAL-RFR-FINDINGS-V1',
    'source_report':'generated/tests/P2_AI_ASI_STRUCTURAL_RFR_V1.json',
    'source_status':report.get('status'),
    'summary':report.get('summary'),
    'ai_only_nonclean':nonclean(report.get('ai_only_tests',[])),
    'engine_nonclean':nonclean(report.get('engine_tests',[])),
    'cross_expansion_nonclean':nonclean(report.get('cross_expansion_tests',[])),
    'hard_failure_count':sum(len(r.get('hard_failures',[])) for k in ['ai_only_tests','engine_tests','cross_expansion_tests'] for r in report.get(k,[])),
    'rule':'This is a compact index only. The full R-F-R report remains authoritative for Pass0/1/2/3 detail.'
}
OUT.write_text(json.dumps(payload,indent=2),encoding='utf-8')
print(json.dumps({
    'source_status':payload['source_status'],
    'ai_nonclean':len(payload['ai_only_nonclean']),
    'engine_nonclean':len(payload['engine_nonclean']),
    'cross_nonclean':len(payload['cross_expansion_nonclean']),
    'hard_failures':payload['hard_failure_count']
}))
