#!/usr/bin/env python3
from pathlib import Path
import json
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "tools/run_micro_sequence_interpreter_v1_2.py"
GEN = ROOT / "generated/tests"
GEN.mkdir(parents=True, exist_ok=True)
errors = []
text = ("They asked me to drive them somewhere in my car and did not explain the full plan; " "after I had already committed, they left another person with me.")

def run(td, seq, history=None, parameter_signals=None):
    out = Path(td) / f"{seq}.json"
    cmd = [sys.executable, str(SCRIPT), "--text", text, "--speaker", "SYNTHETIC-USER", "--sequence-id", seq, "--output", str(out)]
    if history: cmd += ["--history", str(history)]
    if parameter_signals: cmd += ["--parameter-signals", str(parameter_signals)]
    p = subprocess.run(cmd, cwd=ROOT, text=True, capture_output=True)
    if p.returncode != 0:
        errors.append(f"{seq} interpreter failed: {p.stderr}"); return {}
    return json.loads(out.read_text(encoding="utf-8"))

with tempfile.TemporaryDirectory() as td:
    d1 = run(td, "SYN-LIVE-INTENT-001")
    if d1:
        if d1.get("interpreter_version") != "P2-MICRO-SEQUENCE-LIVE-INTERPRETER-001/V1.2": errors.append("direct V1.2 interpreter regression did not report V1.2")
        if "INTENT_LANGUAGE" in d1.get("features", []): errors.append("fixture accidentally contains explicit intent language")
        if "LIVE_INTENT_SYNTHESIS" not in d1.get("features", []): errors.append("live intent synthesis feature did not activate")
        intents = d1.get("intent_hypotheses", [])
        if not intents: errors.append("no live intent hypotheses generated without explicit intent words")
        else:
            if not any("COMMITMENT" in c.get("machine_label", "") for c in intents): errors.append("commitment-before-full-context intent was not generated")
            if not any("TRANSFER_RESPONSIBILITY" in c.get("machine_label", "") for c in intents): errors.append("responsibility-transfer intent was not generated")
            for c in intents:
                if c.get("epistemic_status") != "HYPOTHESIZED": errors.append("machine-generated intent promoted above HYPOTHESIZED")
                if c.get("direct_action_authority") is not False: errors.append("live intent candidate gained direct action authority")
                if c.get("review_status") != "NOT_REVIEWED": errors.append("live intent candidate auto-promoted before review")
                if not c.get("proof_debt") or not c.get("falsifiers") or not c.get("alternative_explanations"): errors.append("live intent candidate missing proof debt/falsifier/alternatives")
        if d1.get("intent_contribution", {}).get("contribution_type") != "NEW_INTENT_CANDIDATE_SIGNAL": errors.append("first V1.2 live run did not emit NEW_INTENT_CANDIDATE_SIGNAL")
        hist = Path(td) / "history.json"; hist.write_text(json.dumps({"records": [d1]}), encoding="utf-8")
        d2 = run(td, "SYN-LIVE-INTENT-002", history=hist)
        if d2:
            if not d2.get("intent_hypotheses"): errors.append("history run produced no intent hypotheses")
            elif not all(c.get("novelty_status") == "MATCHES_PRIOR_INTENT_SIGNATURE" for c in d2.get("intent_hypotheses", [])): errors.append("same-signature prior intent was not recognized")
            if d2.get("intent_contribution", {}).get("contribution_type") != "SUPPORT_PRIOR_INTENT": errors.append("same-signature history did not produce SUPPORT_PRIOR_INTENT")
        ps = Path(td) / "parameter_signals.json"; ps.write_text(json.dumps({"signals": [{"parameter_id": "SB-HFR-P3182", "name": "Delegation", "intent_role": "METHOD", "atom": "DELEGATE_EXECUTION"}]}), encoding="utf-8")
        d3 = run(td, "SYN-LIVE-INTENT-003", parameter_signals=ps)
        if d3:
            i3 = d3.get("intent_hypotheses", [])
            if not any("SB-HFR-P3182" in c.get("supporting_parameter_refs", []) for c in i3): errors.append("plugged Human parameter did not contribute to V1.2 live intent")
            if not any("DELEGATE_EXECUTION" in c.get("machine_label", "") for c in i3): errors.append("plugged parameter did not alter V1.2 generated intent signature")
            sig1 = {c.get("signature") for c in d1.get("intent_hypotheses", [])}; sig3 = {c.get("signature") for c in i3}
            if sig1 == sig3: errors.append("adding relevant parameter did not change V1.2 intent signature space")
    else: d2, d3 = {}, {}

report = {"report_id": "P2-MICRO-SEQUENCE-LIVE-INTENT-V1-2", "status": "PASS" if not errors else "FAIL", "tested_interpreter": "P2-MICRO-SEQUENCE-LIVE-INTERPRETER-001/V1.2", "fixture_has_explicit_intent_language": False, "checks": {"direct_v1_2_regression": d1.get("interpreter_version") == "P2-MICRO-SEQUENCE-LIVE-INTERPRETER-001/V1.2" if d1 else False, "new_intent_without_intent_words": bool(d1.get("intent_hypotheses")) if d1 else False, "new_intent_contribution": d1.get("intent_contribution", {}).get("contribution_type") if d1 else None, "prior_signature_reuse": d2.get("intent_contribution", {}).get("contribution_type") if d2 else None, "parameter_plug_changes_intent_space": bool(d3 and any("DELEGATE_EXECUTION" in c.get("machine_label", "") for c in d3.get("intent_hypotheses", []))), "no_action_authority": not any(c.get("direct_action_authority") is not False for c in (d1.get("intent_hypotheses", []) if d1 else []))}, "errors": errors}
(GEN / "P2_MICRO_SEQUENCE_LIVE_INTENT_V1_2.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print(json.dumps(report, indent=2))
sys.exit(1 if errors else 0)
