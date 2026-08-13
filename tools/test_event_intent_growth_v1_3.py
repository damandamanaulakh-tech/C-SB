#!/usr/bin/env python3
from pathlib import Path
import argparse, json, subprocess, sys, tempfile
ROOT=Path(__file__).resolve().parents[1]; INTERPRETER=ROOT/"tools/run_micro_sequence_interpreter_v1_3.py"; FIXTURE=ROOT/"phase2/tests/P2_EVENT_INTENT_GROWTH_EXAMPLES_V1.json"
def load(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--report"); args=ap.parse_args(); fixture=load(FIXTURE); errors=[]; case_reports=[]
    with tempfile.TemporaryDirectory() as td:
        td=Path(td)
        for case in fixture.get("cases",[]):
            cid=case["case_id"]; out=td/f"{cid}.json"; cmd=[sys.executable,str(INTERPRETER),"--text",case["input_text"],"--speaker","USER","--sequence-id",f"SEQ-{cid}","--output",str(out)]; proc=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True)
            if proc.returncode!=0: errors.append(f"{cid}: interpreter failed: {proc.stderr.strip()}"); continue
            data=load(out); events=data.get("event_records",[]); ledger=data.get("event_growth_ledger") or {}; counts=ledger.get("counts") or {}
            checks={"v1_3":data.get("interpreter_version")=="P2-MICRO-SEQUENCE-LIVE-INTERPRETER-001/V1.3","has_source_and_represented_events":len(events)>=2,"every_event_has_intent":bool(events) and all(isinstance(e.get("intent"),dict) and e["intent"].get("event_id")==e.get("event_id") and e["intent"].get("intent_type") for e in events),"growth_ledger_present":bool(ledger.get("growth_contribution_id")),"source_occurrence_counted":counts.get("source_event_count",0)>=1,"canonical_parameter_additions_zero":counts.get("canonical_parameter_additions")==0,"canonical_pattern_additions_zero":counts.get("canonical_pattern_additions")==0,"review_required":ledger.get("approval_state")=="REVIEW_REQUIRED"}
            for name,ok in checks.items():
                if not ok: errors.append(f"{cid}: failed check {name}")
            refs=ledger.get("existing_id_activation_refs") or {}; case_reports.append({"case_id":cid,"label":case.get("label"),"checks":checks,"counts":counts,"container_ids":refs.get("container_ids",[]),"rubric_ids":refs.get("rubric_ids",[]),"auto_exact_parameter_candidates":refs.get("auto_exact_parameter_candidate_ids",[]),"auto_fuzzy_parameter_candidates":refs.get("auto_fuzzy_parameter_candidate_ids",[]),"live_intent_count":counts.get("live_intents_generated",0),"new_live_intent_count":counts.get("new_live_intent_signatures",0),"pattern_candidate_count":counts.get("pattern_candidates",0)})
    report={"report_id":"P2-EVENT-INTENT-GROWTH-V1-3","status":"PASS" if not errors else "FAIL","tested_interpreter":"P2-MICRO-SEQUENCE-LIVE-INTERPRETER-001/V1.3","fixture_id":fixture.get("fixture_id"),"case_count":len(fixture.get("cases",[])),"universal_motto":fixture.get("universal_motto"),"cases":case_reports,"errors":errors,"known_open_gap":"Atomic 3,204 semantic activation is still conservative: exact-name matches can feed live intent; fuzzy token-overlap matches remain review-only. Deeper semantic parameter-to-role activation remains a growing-phase task."}
    text=json.dumps(report,indent=2,ensure_ascii=False)
    if args.report: Path(args.report).write_text(text+"\n",encoding="utf-8")
    else: print(text)
    if errors: raise SystemExit(1)
if __name__=="__main__": main()
