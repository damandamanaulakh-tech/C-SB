#!/usr/bin/env python3
from pathlib import Path
import json, hashlib, re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'generated/registry_views'
OUT.mkdir(parents=True, exist_ok=True)

def load(rel):
    return json.loads((ROOT / rel).read_text(encoding='utf-8'))

src = load('registries/ai/AI_ONLY_RECORDS_64_APPROVED_V1.json')
bind = load('generated/registry_views/ai_only_64_phase2_bindings_v1.json')
contract = load('machine/ai/AI_NEW_64_STRUCTURAL_DECOMPOSITION_CONTRACT_V1.json')

binding_by_id = {r['ai_only_id']: r for r in bind['records']}
form_map = contract['runtime_form_by_source_level']
composites = contract['composite_candidates']
seq_contracts = contract['sequence_contract_by_runtime_form']

# Only source-derived Engine relationship files are inspected for exact AI-NEW references.
engine_relation_files = [
    'generated/registry_views/brain_engine_relationships_compact_v1.json',
    'registries/asi/ENGINE_SEGMENT_BINDINGS_75_APPROVED_V1.json',
]
engine_relation_docs = []
for rel in engine_relation_files:
    p = ROOT / rel
    if p.exists():
        engine_relation_docs.append((rel, json.loads(p.read_text(encoding='utf-8'))))

def collect_engines_near_id(obj, rid):
    found = set()
    def walk(x):
        if isinstance(x, dict):
            blob = json.dumps(x, ensure_ascii=False)
            if rid in blob:
                for v in x.values():
                    if isinstance(v, str):
                        found.update(re.findall(r'ENG-[A-Z0-9]+-\d{3}', v))
                    elif isinstance(v, (dict, list)):
                        walk(v)
        elif isinstance(x, list):
            for v in x:
                walk(v)
    walk(obj)
    return sorted(found)

def ownership(runtime_form, asi_segments):
    has_asi = bool(asi_segments)
    if runtime_form == 'MECHANISM':
        return 'AI_PRIMARY_WITH_ASI_GOVERNANCE_INTERFACE' if has_asi else 'AI_PRIMARY'
    if runtime_form == 'CONTROL':
        return 'SHARED_AI_ASI_CONTROL' if has_asi else 'AI_LOCAL_CONTROL_WITHOUT_PERMISSION_AUTHORITY'
    if runtime_form == 'FILTER':
        return 'AI_FILTER_WITH_ASI_ACCEPTANCE_INTERFACE' if has_asi else 'AI_LOCAL_FILTER'
    if runtime_form == 'EVIDENCE_CONTROL':
        return 'AI_EVIDENCE_MECHANISM_WITH_ASI_PROVENANCE_GOVERNANCE'
    if runtime_form == 'META_CONTROL':
        return 'SHARED_AI_ASI_META_CONTROL'
    if runtime_form == 'STATE':
        return 'AI_RUNTIME_STATE_UNDER_ASI_POLICY' if has_asi else 'AI_RUNTIME_STATE'
    if runtime_form == 'STATE_OR_MECHANISM_MIXED':
        return 'AI_RUNTIME_STATE_OR_MECHANISM_UNDER_EXPLICIT_CALL_CONTRACT'
    raise ValueError(runtime_form)

records = []
for row in src['records']:
    rid, name, source_level, lineage = row
    b = binding_by_id[rid]
    if b['name'] != name or b['source_structural_level'] != source_level:
        raise ValueError(f'source/binding mismatch {rid}')
    runtime_form = form_map[source_level]
    engine_ids = set()
    engine_evidence = []
    for rel, doc in engine_relation_docs:
        ids = collect_engines_near_id(doc, rid)
        if ids:
            engine_ids.update(ids)
            engine_evidence.append({'source': rel, 'engine_ids': ids})
    is_composite = rid in composites
    source_payload = json.dumps(row, ensure_ascii=False, separators=(',', ':')).encode('utf-8')
    records.append({
        'ai_only_id': rid,
        'source_name': name,
        'source_structural_level': source_level,
        'source_ai_cap_lineage': b['source_ai_cap_ids'],
        'source_record_sha256': hashlib.sha256(source_payload).hexdigest(),
        'runtime_form': runtime_form,
        'atomicity': 'COMPOSITE_CANDIDATE' if is_composite else 'ATOMIC_AT_APPROVED_SOURCE_SCOPE',
        'composite_components': composites.get(rid, []),
        'composite_split_status': 'RUNTIME_SUBCONTRACTS_REQUIRED_IF_COMPONENT_CLOSURE_DIFFERS' if is_composite else 'NOT_REQUIRED_BY_CURRENT_SOURCE',
        'mechanism_ownership': ownership(runtime_form, b['phase2_asi_segments']),
        'phase2_ai_segments': b['phase2_ai_segments'],
        'phase2_asi_segments': b['phase2_asi_segments'],
        'phase2_asi_nodes': b['phase2_asi_nodes'],
        'primary_sequence_roles': b['primary_sequence_roles'],
        'secondary_sequence_roles': b['secondary_sequence_roles'],
        'state_ownership_candidates': b['state_ownership_candidates'],
        'memory_read_candidates': b['memory_read_candidates'],
        'memory_write_candidates': b['memory_write_candidates'],
        'activation_contract': seq_contracts[runtime_form]['activation'],
        'closure_contract': seq_contracts[runtime_form]['closure'],
        'direct_engine_ids': sorted(engine_ids),
        'direct_engine_evidence': engine_evidence,
        'engine_binding_status': 'SOURCE_DERIVED_DIRECT_BINDING' if engine_ids else 'ENGINE_BINDING_OPEN_NO_EXACT_SOURCE_RELATION',
        'authority_guards': contract['authority_guards'],
        'source_binding_status': b['binding_status'],
        'governance_patch_applied': b['governance_patch_applied'],
    })

assert len(records) == 64
assert [r['ai_only_id'] for r in records] == [f'AI-NEW-{i:03d}' for i in range(1,65)]

from collections import Counter
summary = {
    'runtime_form_counts': dict(Counter(r['runtime_form'] for r in records)),
    'atomicity_counts': dict(Counter(r['atomicity'] for r in records)),
    'ownership_counts': dict(Counter(r['mechanism_ownership'] for r in records)),
    'engine_binding_counts': dict(Counter(r['engine_binding_status'] for r in records)),
    'governance_patch_count': sum(1 for r in records if r['governance_patch_applied']),
}

payload = {
    'registry_id': 'AI-NEW-64-STRUCTURAL-DECOMPOSITION-V1',
    'phase': 'PHASE_2',
    'status': 'GENERATED_ADDITIVE_DECOMPOSITION_NOT_SOURCE_REWRITE',
    'source_registry': 'registries/ai/AI_ONLY_RECORDS_64_APPROVED_V1.json',
    'binding_registry': 'generated/registry_views/ai_only_64_phase2_bindings_v1.json',
    'contract': 'machine/ai/AI_NEW_64_STRUCTURAL_DECOMPOSITION_CONTRACT_V1.json',
    'record_count': 64,
    'summary': summary,
    'records': records,
}
(OUT/'ai_new_64_structural_decomposition_v1.json').write_text(json.dumps(payload, indent=2), encoding='utf-8')

md = ['# AI-NEW-001..064 Structural Decomposition V1', '', 'Source IDs/names/levels are preserved. Structural and ownership fields are additive.', '']
md.append(f"- Records: {len(records)}")
for k,v in summary.items():
    md.append(f"- {k}: `{json.dumps(v, sort_keys=True)}`")
md += ['', '## Composite candidates', '']
for r in records:
    if r['atomicity'] == 'COMPOSITE_CANDIDATE':
        md.append(f"- **{r['ai_only_id']} {r['source_name']}** → {', '.join(r['composite_components'])}")
md += ['', '## Engine binding', '', 'Direct Engine IDs are emitted only when an exact AI-NEW reference is found in a source-derived Engine relationship registry. Name similarity is not used.']
(OUT/'AI_NEW_64_STRUCTURAL_DECOMPOSITION_V1.md').write_text('\n'.join(md)+'\n', encoding='utf-8')
print(json.dumps(summary, sort_keys=True))
