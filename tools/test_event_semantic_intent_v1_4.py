#!/usr/bin/env python3
from pathlib import Path
import argparse,json,subprocess,sys,tempfile
ROOT=Path(__file__).resolve().parents[1]; SCRIPT=ROOT/"tools/run_micro_sequence_interpreter_v1_4.py"; FIXTURE=ROOT/"phase2/tests/P2_EVENT_INTENT_GROWTH_EXAMPLES_V1.json"
def load(p): return json.loads(Path(p).read_text(encoding="utf-8"))
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--report"); a=ap.parse_args(); fx=load(FIXTURE); errors=[]; reports=[]
    with tempfile.TemporaryDirectory() as td:
        td=Path(td)
        for case in fx.get("cases",[]):
            out=td/(case["case_id"]+".json"); p=subprocess.run([sys.executable,str(SCRIPT),"--text",case["input_text"],"--speaker","USER","--sequence-id","SEQ-"+case["case_id"],"--output",str(out)],cwd=ROOT,text=True,capture_output=True)
            if p.returncode!=0: errors.append(case["case_id"]+": "+p.stderr.strip()); continue
            d=load(out); ledger=d.get("event_growth_ledger") or {}; counts=ledger.get("counts") or {}; intents=d.get("intent_hypotheses",[]); checks={"v1_4":d.get("interpreter_version")=="P2-MICRO-SEQUENCE-LIVE-INTERPRETER-001/V1.4","events_have_intent":bool(d.get("event_records")) and all(e.get("intent",{}).get("intent_type") for e in d.get("event_records",[])),"semantic_rule_hit":bool(d.get("semantic_intent_rule_hits")),"live_intent_generated":len(intents)>0,"canonical_parameter_zero":counts.get("canonical_parameter_additions")==0,"canonical_pattern_zero":counts.get("canonical_pattern_additions")==0,"validated_support_zero":counts.get("validated_support_delta")==0}
            for n,ok in checks.items():
                if not ok: errors.append(f"{case['case_id']}: failed {n}")
            reports.append({"case_id":case["case_id"],"label":case.get("label"),"checks":checks,"semantic_rules":[x.get("rule_id") for x in d.get("semantic_intent_rule_hits",[])],"container_ids":ledger.get("existing_id_activation_refs",{}).get("container_ids",[]),"rubric_ids":ledger.get("existing_id_activation_refs",{}).get("rubric_ids",[]),"counts":counts,"live_intents":[{"intent_candidate_id":x.get("intent_candidate_id"),"machine_label":x.get("machine_label"),"intent_scope_candidates":x.get("intent_scope_candidates",[]),"semantic_rule_refs":x.get("semantic_rule_refs",[]),"novelty_status":x.get("novelty_status")} for x in intents]})
    report={"report_id":"P2-EVENT-SEMANTIC-INTENT-V1-4","status":"PASS" if not errors else "FAIL","tested_interpreter":"P2-MICRO-SEQUENCE-LIVE-INTERPRETER-001/V1.4","case_count":len(fx.get("cases",[])),"cases":reports,"errors":errors,"known_limits":["Semantic Event rules are deterministic seed activators, not final intelligence or canonical truth.","Atomic 3,204 activation remains conservative; semantic container/rubric activation is broader than exact atomic parameter resolution.","Future growth should replace/augment lexical triggers with parameter/rubric/Node-Brain learned activation from reviewed examples."]}; text=json.dumps(report,indent=2,ensure_ascii=False); Path(a.report).write_text(text+"\n",encoding="utf-8") if a.report else print(text); raise SystemExit(1 if errors else 0)
if __name__=="__main__": main()
