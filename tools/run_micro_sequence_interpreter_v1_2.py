#!/usr/bin/env python3
from pathlib import Path
import argparse, hashlib, json, re, subprocess, sys, tempfile

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / 'tools/run_micro_sequence_interpreter_v1_1.py'
CONFIG = ROOT / 'machine/runtime/INTENT_HYPOTHESIS_SYNTHESIS_RUNTIME_V1.json'
ROUTING = ROOT / 'machine/runtime/MICRO_SEQUENCE_ENGINE_ROUTING_V1.json'
RUBRICS = ROOT / 'machine/rubrics/RUBRIC_REGISTRY_R01_R52.json'
HUMAN_CONTAINERS = ROOT / 'registries/human/HUMAN_CONTAINER_INDEX_80_APPROVED_V1.json'
HFR = ROOT / 'generated/registry_views/human_functional_3204_registry_v1.json'
HUMAN_CANDIDATES = ROOT / 'registries/human/HUMAN_KING_PROFILE_PARAMETER_CANDIDATES_V0.json'


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def hid(*parts):
    return hashlib.sha256('\x1f'.join(str(x) for x in parts).encode()).hexdigest()[:16].upper()


def sid(prefix, *parts):
    return f"{prefix}-{hid(*parts)}"


def norm_atom(value):
    x = re.sub(r'[^A-Za-z0-9]+', '_', str(value).upper()).strip('_')
    return re.sub(r'_+', '_', x)


def read_history(path):
    if not path:
        return []
    d = load(path)
    if isinstance(d, list):
        return d
    for key in ('records', 'micro_sequences', 'items', 'history'):
        if isinstance(d.get(key), list):
            return d[key]
    return []


def prior_intents(records):
    by_sig = {}
    for record in records:
        seq = record.get('sequence_id') or record.get('intake', {}).get('sequence_id')
        for c in record.get('intent_hypotheses', []) or []:
            sig = c.get('signature')
            if sig:
                by_sig.setdefault(sig, []).append(seq)
    return by_sig


def human_container_index():
    out = {}
    for seg in load(HUMAN_CONTAINERS).get('segments', []):
        for row in seg.get('containers', []):
            out[row[0]] = {'name': row[1], 'segment_id': seg['segment_id']}
    return out


def human_parameter_indexes():
    approved = {}
    if HFR.exists():
        for p in load(HFR).get('parameters', []):
            approved[p.get('parameter_id')] = p
    candidates = {}
    if HUMAN_CANDIDATES.exists():
        for p in load(HUMAN_CANDIDATES).get('candidates', []):
            candidates[p.get('candidate_id')] = p
    return approved, candidates


def infer_role(name, role_keywords):
    n = str(name).lower()
    scores = []
    for role, words in role_keywords.items():
        score = sum(1 for w in words if w.lower() in n)
        if score:
            scores.append((score, role))
    return sorted(scores, reverse=True)[0][1] if scores else 'STATE'


def add_signal(signals, sequence_id, source_kind, source_ref, role, atom, source_status, evidence_refs):
    atom = norm_atom(atom)
    key = (source_kind, str(source_ref), role, atom)
    if any((s['source_kind'], str(s.get('source_ref')), s['role'], s['atom']) == key for s in signals):
        return
    signals.append({
        'signal_id': sid('INT-SIG', sequence_id, source_kind, source_ref, role, atom),
        'sequence_id': sequence_id,
        'source_kind': source_kind,
        'source_ref': source_ref,
        'role': role,
        'atom': atom,
        'source_status': source_status,
        'evidence_refs': list(evidence_refs),
    })


def load_parameter_signals(path, sequence_id, intake_id, config):
    if not path:
        return [], []
    raw = load(path)
    items = raw if isinstance(raw, list) else raw.get('signals', [])
    approved, candidates = human_parameter_indexes()
    signals = []
    refs = []
    for i, item in enumerate(items):
        pid = item.get('parameter_id')
        if not pid:
            raise SystemExit(f'parameter signal {i} missing parameter_id')
        if pid in approved:
            source = approved[pid]
            source_kind = 'HUMAN_PARAMETER'
            source_status = 'APPROVED_PARAMETER'
            canonical_name = source.get('name', '')
        elif pid in candidates:
            source = candidates[pid]
            source_kind = 'HUMAN_PARAMETER_CANDIDATE'
            source_status = 'REVIEW_REQUIRED_PARAMETER_CANDIDATE'
            canonical_name = source.get('name', '')
        else:
            raise SystemExit(f'unknown Human parameter signal: {pid}')
        supplied_name = item.get('name')
        if supplied_name and supplied_name != canonical_name:
            raise SystemExit(f'parameter signal name mismatch for {pid}: {supplied_name!r} != {canonical_name!r}')
        role = item.get('intent_role') or infer_role(canonical_name, config.get('parameter_role_keywords', {}))
        if role not in config.get('intent_roles', []):
            raise SystemExit(f'invalid intent_role {role} for {pid}')
        atom = item.get('atom') or canonical_name
        add_signal(signals, sequence_id, source_kind, pid, role, atom, source_status, [intake_id, pid])
        refs.append(pid)
    return signals, refs


def active_role_atoms(signals):
    out = {r: [] for r in ['GOAL','TARGET','METHOD','CONDITION','ORDER','MODIFIER','CONSTRAINT','STATE']}
    for s in signals:
        out.setdefault(s['role'], []).append(s['atom'])
    for role in out:
        out[role] = sorted(set(out[role]))
    return out


def describe_candidate(goal, atoms):
    pretty = lambda x: x.replace('_', ' ').lower()
    parts = [f"Possible relevant actor intent: {pretty(goal)}"]
    if atoms['TARGET']:
        parts.append('toward ' + ', '.join(pretty(x) for x in atoms['TARGET']))
    if atoms['METHOD']:
        parts.append('using/through ' + ', '.join(pretty(x) for x in atoms['METHOD']))
    conditions = atoms['CONDITION'] + atoms['CONSTRAINT']
    if conditions:
        parts.append('under ' + ', '.join(pretty(x) for x in conditions))
    if atoms['ORDER']:
        parts.append('with order ' + ', '.join(pretty(x) for x in atoms['ORDER']))
    if atoms['MODIFIER']:
        parts.append('and ' + ', '.join(pretty(x) for x in atoms['MODIFIER']))
    return '; '.join(parts) + '. This is a generated hypothesis from structure/parameters, not observed hidden intent.'


def candidate_signature(goal, selected):
    fields = [goal]
    for role in ['TARGET','METHOD','CONDITION','ORDER','MODIFIER','CONSTRAINT','STATE']:
        fields.append(role + '=' + ','.join(sorted(selected.get(role, []))))
    return '|'.join(fields)


def synthesize(sequence_id, signals, prior_by_sig, base_pattern_id, config):
    atoms = active_role_atoms(signals)
    goals = atoms['GOAL'][:]
    if not goals:
        return []
    max_candidates = int(config.get('composition_policy', {}).get('max_live_candidates', 12))
    candidates = []
    seen = set()

    def emit(goal, selected):
        nonlocal candidates
        role_count = sum(1 for role in ['GOAL','TARGET','METHOD','CONDITION','ORDER','MODIFIER','CONSTRAINT','STATE'] if (role == 'GOAL' or selected.get(role)))
        support = [s for s in signals if s['atom'] == goal or s['atom'] in {a for vals in selected.values() for a in vals}]
        support_ids = sorted({s['signal_id'] for s in support})
        if role_count < int(config.get('composition_policy', {}).get('minimum_distinct_roles', 2)):
            return
        if len(support_ids) < int(config.get('composition_policy', {}).get('minimum_supporting_signals', 2)):
            return
        sig = candidate_signature(goal, selected)
        if sig in seen or len(candidates) >= max_candidates:
            return
        seen.add(sig)
        prior_seqs = [x for x in prior_by_sig.get(sig, []) if x]
        novelty = 'MATCHES_PRIOR_INTENT_SIGNATURE' if prior_seqs else 'NEW_LIVE_INTENT_CANDIDATE'
        p_refs = sorted({s['source_ref'] for s in support if s['source_kind'] in {'HUMAN_PARAMETER','HUMAN_PARAMETER_CANDIDATE'} and s.get('source_ref')})
        review_param = any(s['source_kind'] == 'HUMAN_PARAMETER_CANDIDATE' for s in support)
        label_parts = [goal]
        if selected.get('TARGET'):
            label_parts += ['TARGET'] + selected['TARGET']
        if selected.get('METHOD'):
            label_parts += ['VIA'] + selected['METHOD']
        if selected.get('CONDITION') or selected.get('CONSTRAINT'):
            label_parts += ['UNDER'] + selected.get('CONDITION', []) + selected.get('CONSTRAINT', [])
        if selected.get('ORDER'):
            label_parts += ['ORDER'] + selected['ORDER']
        machine_label = '__'.join(label_parts)
        falsifiers = [
            'Comparable cases show the same observed structure with a different directly evidenced intent.',
            'The actor provides an alternative stated reason that better predicts the action sequence.',
            'Removing the hypothesized goal leaves the observed sequence equally or better explained.'
        ]
        if 'INCOMPLETE_CONTEXT' in selected.get('CONDITION', []):
            falsifiers.append('Comparable requests routinely contain incomplete context without strategic withholding or commitment-seeking.')
        if goal == 'TRANSFER_RESPONSIBILITY':
            falsifiers.append('The receiving actor explicitly accepted the responsibility with full context before the transfer.')
        candidates.append({
            'intent_candidate_id': sid('INT-CAND', sequence_id, sig),
            'sequence_id': sequence_id,
            'machine_label': machine_label,
            'machine_description': describe_candidate(goal, selected),
            'epistemic_status': 'HYPOTHESIZED',
            'novelty_status': novelty,
            'signature': sig,
            'goal_atoms': [goal],
            'target_atoms': selected.get('TARGET', []),
            'method_atoms': selected.get('METHOD', []),
            'condition_atoms': selected.get('CONDITION', []),
            'order_atoms': selected.get('ORDER', []),
            'modifier_atoms': selected.get('MODIFIER', []),
            'constraint_atoms': selected.get('CONSTRAINT', []),
            'state_atoms': selected.get('STATE', []),
            'supporting_signal_ids': support_ids,
            'supporting_parameter_refs': p_refs,
            'supporting_pattern_refs': [base_pattern_id] if base_pattern_id else [],
            'supporting_sequence_ids': prior_seqs + [sequence_id],
            'alternative_explanations': config.get('default_alternatives', []),
            'falsifiers': falsifiers,
            'proof_debt': config.get('default_proof_debt', []),
            'evidence_strength': {
                'supporting_signal_count': len(support_ids),
                'distinct_role_count': role_count,
                'prior_same_signature_count': len(prior_seqs)
            },
            'confidence': None,
            'depends_on_review_required_parameter_candidates': review_param,
            'review_status': 'NOT_REVIEWED',
            'approval_scope': None,
            'direct_action_authority': False
        })

    # Maximal candidate per goal: uses all relevant active atoms without Cartesian explosion.
    for goal in goals:
        selected = {role: atoms[role][:] for role in ['TARGET','METHOD','CONDITION','ORDER','MODIFIER','CONSTRAINT','STATE']}
        emit(goal, selected)

    # Target-specific variants make new target parameters capable of producing distinct live intent signatures.
    if len(candidates) < max_candidates and len(atoms['TARGET']) > 1:
        for goal in goals:
            for target in atoms['TARGET']:
                selected = {role: atoms[role][:] for role in ['METHOD','CONDITION','ORDER','MODIFIER','CONSTRAINT','STATE']}
                selected['TARGET'] = [target]
                emit(goal, selected)
                if len(candidates) >= max_candidates:
                    break
            if len(candidates) >= max_candidates:
                break

    return candidates


def ensure_rubric_activations(data, rids):
    registry = load(RUBRICS).get('rubrics', {})
    existing = {a.get('rubric_path', [None])[0] for a in data.get('rubric_activations', [])}
    mus = [m.get('micro_unit_id') for m in data.get('micro_units', [])]
    intake_id = data.get('intake', {}).get('intake_id')
    seq = data.get('sequence_id')
    for rid in rids:
        if rid in existing or rid not in registry:
            continue
        data.setdefault('rubric_activations', []).append({
            'activation_id': sid('ACT', seq, rid, 'LIVE-INTENT'),
            'sequence_id': seq,
            'micro_unit_ids': mus,
            'rubric_path': [rid],
            'rubric_name': registry[rid]['name'],
            'domain': 'UNIVERSAL_SEQUENCE',
            'activation_evidence_refs': [intake_id],
            'activation_status': 'CANDIDATE',
            'weight_or_relevance': None,
            'engine_candidate_ids': [],
            'asi_node_candidate_ids': []
        })


def ensure_human_containers(data, cids):
    idx = human_container_index()
    existing = {a.get('rubric_path', [])[-1] for a in data.get('human_container_activations', []) if a.get('rubric_path')}
    mus = [m.get('micro_unit_id') for m in data.get('micro_units', [])]
    intake_id = data.get('intake', {}).get('intake_id')
    seq = data.get('sequence_id')
    for cid in cids:
        if cid in existing or cid not in idx:
            continue
        data.setdefault('human_container_activations', []).append({
            'activation_id': sid('ACT-H', seq, cid, 'LIVE-INTENT'),
            'sequence_id': seq,
            'micro_unit_ids': mus,
            'rubric_path': [idx[cid]['segment_id'], cid],
            'native_name': idx[cid]['name'],
            'domain': 'HUMAN',
            'activation_status': 'CANDIDATE',
            'activation_note': 'Container candidate activated by live intent synthesis. Intent remains hypothesized; no atomic Human parameter is asserted unless explicitly supplied as a validated parameter signal.',
            'activation_evidence_refs': [intake_id]
        })


def ensure_engine_routes(data):
    features = set(data.get('features', []))
    existing = {r.get('route_id') for r in data.get('engine_routes', [])}
    for route in load(ROUTING).get('routes', []):
        if route.get('route_id') in existing:
            continue
        hit = sorted(set(route.get('activation_tags', [])) & features)
        if hit:
            data.setdefault('engine_routes', []).append({
                'route_id': route['route_id'],
                'matched_tags': hit,
                'engine_ids': route['engine_ids'],
                'purpose': route['purpose']
            })


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--text', required=True)
    ap.add_argument('--speaker', default='USER')
    ap.add_argument('--sequence-id')
    ap.add_argument('--history')
    ap.add_argument('--review-decision')
    ap.add_argument('--parameter-signals')
    ap.add_argument('--output')
    args = ap.parse_args()

    with tempfile.TemporaryDirectory() as td:
        base_out = Path(td) / 'base.json'
        cmd = [sys.executable, str(BASE), '--text', args.text, '--speaker', args.speaker, '--output', str(base_out)]
        if args.sequence_id:
            cmd += ['--sequence-id', args.sequence_id]
        if args.history:
            cmd += ['--history', args.history]
        if args.review_decision:
            cmd += ['--review-decision', args.review_decision]
        proc = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
        if proc.returncode != 0:
            sys.stderr.write(proc.stderr)
            raise SystemExit(proc.returncode)
        data = load(base_out)

    config = load(CONFIG)
    seq = data['sequence_id']
    intake_id = data.get('intake', {}).get('intake_id')
    features = set(data.get('features', []))
    signals = []

    for feature in sorted(features):
        for atom in config.get('feature_atoms', {}).get(feature, []):
            add_signal(signals, seq, 'FEATURE', feature, atom['role'], atom['atom'], 'OBSERVED_OR_REPORTED_STRUCTURE', [intake_id])

    for rule in config.get('derived_signal_rules', []):
        if not set(rule.get('requires_features', [])).issubset(features):
            continue
        if re.search(rule.get('text_pattern', ''), args.text, flags=re.I):
            for atom in rule.get('atoms', []):
                add_signal(signals, seq, 'DERIVED_STRUCTURE', rule['rule_id'], atom['role'], atom['atom'], 'INFERRED', [intake_id, rule['rule_id']])

    parameter_signals, parameter_refs = load_parameter_signals(args.parameter_signals, seq, intake_id, config)
    for s in parameter_signals:
        add_signal(signals, seq, s['source_kind'], s['source_ref'], s['role'], s['atom'], s['source_status'], s['evidence_refs'])

    history_records = read_history(args.history)
    prior_by_sig = prior_intents(history_records)
    base_pattern = data.get('pattern_candidate') or {}
    intents = synthesize(seq, signals, prior_by_sig, base_pattern.get('pattern_candidate_id'), config)

    if intents:
        features |= {'LIVE_INTENT_SYNTHESIS','INTENT_INFERENCE','UNCERTAINTY','PROOF_DEBT'}
        data['features'] = sorted(features)
        ensure_rubric_activations(data, ['R07','R10','R22','R50'])
        ensure_human_containers(data, ['CON-063','CON-064','CON-069','CON-075'])
        ensure_engine_routes(data)

    existing_interpretations = data.setdefault('interpretation_candidates', [])
    for c in intents:
        existing_interpretations.append({
            'interpretation_id': sid('INTP', seq, c['intent_candidate_id']),
            'sequence_id': seq,
            'claim': c['machine_description'],
            'claim_type': 'INTENT',
            'supporting_micro_unit_ids': [m.get('micro_unit_id') for m in data.get('micro_units', [])],
            'supporting_sequence_ids': c.get('supporting_sequence_ids', []),
            'contradicting_sequence_ids': [],
            'alternative_interpretation_ids': [],
            'epistemic_status': 'HYPOTHESIZED',
            'confidence': None,
            'direct_action_authority': False,
            'intent_candidate_ref': c['intent_candidate_id']
        })

    new_count = sum(1 for c in intents if c['novelty_status'] == 'NEW_LIVE_INTENT_CANDIDATE')
    prior_count = sum(1 for c in intents if c['novelty_status'] == 'MATCHES_PRIOR_INTENT_SIGNATURE')
    if new_count and prior_count:
        contribution_type = 'MIXED_NEW_AND_PRIOR'
    elif new_count:
        contribution_type = 'NEW_INTENT_CANDIDATE_SIGNAL'
    elif prior_count:
        contribution_type = 'SUPPORT_PRIOR_INTENT'
    else:
        contribution_type = 'NO_INTENT_CANDIDATE'
    intent_contribution = {
        'contribution_id': sid('INT-CONTRIB', seq, *[c['signature'] for c in intents]),
        'sequence_id': seq,
        'candidate_ids': [c['intent_candidate_id'] for c in intents],
        'contribution_type': contribution_type,
        'parameter_refs': sorted(set(parameter_refs)),
        'pattern_refs': [base_pattern['pattern_candidate_id']] if base_pattern.get('pattern_candidate_id') else [],
        'proof_debt_present': bool(intents)
    }

    data['intent_signals'] = signals
    data['intent_hypotheses'] = intents
    data['intent_contribution'] = intent_contribution
    data['intent_runtime_id'] = config['runtime_id']

    if base_pattern and intents and base_pattern.get('intent_status') == 'UNKNOWN':
        base_pattern['intent_status'] = 'INFERRED'
    if base_pattern and intents:
        base_pattern['candidate_intent_ids'] = [c['intent_candidate_id'] for c in intents]
        base_pattern['parameter_refs'] = sorted(set(base_pattern.get('parameter_refs', []) + parameter_refs))

    review = data.get('reviewable_rubric_view') or {}
    proposal = review.setdefault('machine_proposal', {})
    proposal['intent_hypotheses'] = intents
    proposal['intent_contribution'] = intent_contribution
    proposal['summary'] = 'V1.2 deterministic structural proposal with live intent synthesis. Generated intent is hypothesized unless directly user-attributed; ambiguity and proof debt remain reviewable.'
    unknowns = review.setdefault('unknowns', [])
    if intents:
        for x in ['which generated intent, if any, matches the actor\'s actual goal','whether incomplete context was deliberate strategy or non-strategic communication/planning failure']:
            if x not in unknowns:
                unknowns.append(x)

    data['interpreter_version'] = 'P2-MICRO-SEQUENCE-LIVE-INTERPRETER-001/V1.2'
    data['supersedes_interpreter'] = 'P2-MICRO-SEQUENCE-LIVE-INTERPRETER-001/V1.1'
    data['correction'] = 'Adds live compositional intent-hypothesis generation from relevant parameter/structure atoms even without explicit intent language. More relevant parameters can create new signatures; parameter count alone cannot.'
    data['epistemic_guard'] = 'Observed/reported action and structure may generate live intent hypotheses, but intent remains HYPOTHESIZED unless directly evidenced or USER_ATTRIBUTED. More parameters increase hypothesis resolution, not truth/confidence by themselves. No live intent candidate has direct action authority.'

    text = json.dumps(data, indent=2, ensure_ascii=False)
    if args.output:
        Path(args.output).write_text(text, encoding='utf-8')
    else:
        print(text)


if __name__ == '__main__':
    main()
