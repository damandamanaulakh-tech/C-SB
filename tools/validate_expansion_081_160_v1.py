#!/usr/bin/env python3
from pathlib import Path
import json, sys, re

ROOT=Path(__file__).resolve().parents[1]
errors=[]
def load(rel):
    p=ROOT/rel
    if not p.exists():
        errors.append(f'Missing {rel}')
        return {}
    return json.loads(p.read_text(encoding='utf-8'))

idx=load('registries/expansion/EXPANSION_CONTAINERS_081_160_INDEX_V1.json')
params=load('registries/expansion/EXPANSION_PARAMETERS_2561_2592_APPROVED_V1.json')
cls=load('registries/expansion/EXPANSION_103_120_AI_ASI_CLASSIFICATION_V1.json')

rows=idx.get('records',[])
ids=[r[0] for r in rows]
expected=[f'CON-{i:03d}' for i in range(81,161)]
if ids != expected:
    errors.append('Expansion index must contain CON-081..CON-160 exactly in order.')
if len(rows)!=80:
    errors.append('Expansion index must contain exactly 80 source rows.')
for n in range(121,161):
    r=rows[n-81] if len(rows)>=80 else None
    if not r or r[2] != f'Extended Capability Node {n}':
        errors.append(f'CON-{n:03d} must retain source placeholder name Extended Capability Node {n}.')
        break

prows=params.get('records',[])
pids=[r[0] for r in prows]
expected_p=[f'SB-ASI-P{i:04d}' for i in range(2561,2593)]
if pids != expected_p:
    errors.append('Expansion parameter registry must contain SB-ASI-P2561..SB-ASI-P2592 exactly in order.')
for r in prows:
    if r[1] not in set(expected):
        errors.append(f'{r[0]} references non-expansion container {r[1]}.')
        break

crows=cls.get('records',[])
cids=[r.get('container_id') for r in crows]
expected_cross=[f'CON-{i:03d}' for i in range(103,121)]
if cids != expected_cross:
    errors.append('Named cross-domain classification must cover CON-103..CON-120 exactly and only.')
source_names={r[0]:r[2] for r in rows}
for r in crows:
    if source_names.get(r.get('container_id')) != r.get('name'):
        errors.append(f"Classification renamed source container {r.get('container_id')}.")
        break
    if not r.get('domain_role') or not r.get('asi_nodes'):
        errors.append(f"Classification {r.get('container_id')} lacks domain role or ASI Node mapping.")
        break
if any(int(cid.split('-')[-1]) >=121 for cid in cids):
    errors.append('CON-121..160 placeholders must not be semantically classified before source/test evidence resolves them.')

print('errors:',len(errors))
for e in errors: print('ERROR',e)
sys.exit(1 if errors else 0)
