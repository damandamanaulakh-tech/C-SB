#!/usr/bin/env python3
from pathlib import Path
import argparse, importlib.util, json, re, subprocess, sys, tempfile
ROOT=Path(__file__).resolve().parents[1]; BASE=ROOT/"tools/run_micro_sequence_interpreter_v1_3.py"; RULES=ROOT/"machine/runtime/EVENT_SEMANTIC_INTENT_RULES_V1.json"; V12_PATH=ROOT/"tools/run_micro_sequence_interpreter_v1_2.py"; V13_PATH=ROOT/"tools/run_micro_sequence_interpreter_v1_3.py"
def load(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def module_from(path,name):
    spec=importlib.util.spec_from_file_location(name,path); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
V12=module_from(V12_PATH,"sourceborn_v12_helpers"); V13=module_from(V13_PATH,"sourceborn_v13_helpers")
def semantic_signals(text,seq,intake_id):
    out=[]; matched=[]
    for rule in load(RULES).get("rules",[]):
        if not re.search(rule.get("pattern",""),text,flags=re.I|re.S): continue
        matched.append(rule)
        for atom in rule.get("atoms",[]):
            before=len(out); V12.add_signal(out,seq,"SEMANTIC_EVENT_RULE",rule["rule_id"],atom["role"],atom["atom"],"INFERRED_REVIEW_REQUIRED",[intake_id,rule["rule_id"]])
            if len(out)>before: out[-1]["semantic_rule_id"]=rule["rule_id"]; out[-1]["intent_scope"]=rule.get("intent_scope","ACTOR_HYPOTHESIS")
    return out,matched
def merge_signals(existing,new):
    out=list(existing); keys={(x.get("source_kind"),str(x.get("source_ref")),x.get("role"),x.get("atom")) for x in out}
    for s in new:
        k=(s.get("source_kind"),str(s.get("source_ref")),s.get("role"),s.get("atom"))
        if k not in keys: out.append(s); keys.add(k)
    return out
def annotate(c,signals,mode):
    idx={s.get("signal_id"):s for s in signals}; c["intent_scope_candidates"]=sorted({idx[x].get("intent_scope") for x in c.get("supporting_signal_ids",[]) if x in idx and idx[x].get("intent_scope")}); c["semantic_rule_refs"]=sorted({idx[x].get("semantic_rule_id") for x in c.get("supporting_signal_ids",[]) if x in idx and idx[x].get("semantic_rule_id")}); c["composition_mode"]=mode; return c
def merge_intents(existing,new,signals):
    ordered=[]; bysig={}
    for c in existing:
        c.setdefault("composition_mode","BASE_V1_2"); c.setdefault("intent_scope_candidates",[]); c.setdefault("semantic_rule_refs",[]); sig=c.get("signature")
        if sig and sig not in bysig: bysig[sig]=c; ordered.append(c)
    for c in new:
        sig=c.get("signature")
        if not sig: continue
        c=annotate(c,signals,"SEMANTIC_RULE_LOCAL")
        if sig not in bysig: bysig[sig]=c; ordered.append(c)
        else:
            old=bysig[sig]; old["intent_scope_candidates"]=sorted(set(old.get("intent_scope_candidates",[])+c.get("intent_scope_candidates",[]))); old["semantic_rule_refs"]=sorted(set(old.get("semantic_rule_refs",[])+c.get("semantic_rule_refs",[]))); old["supporting_signal_ids"]=sorted(set(old.get("supporting_signal_ids",[])+c.get("supporting_signal_ids",[])))
    return ordered[:12]
def rule_local_candidates(seq,sem,matched,prior,pattern_id,config):
    goals_by_rule={r["rule_id"]:any(a.get("role")=="GOAL" for a in r.get("atoms",[])) for r in matched}; context=[s for s in sem if not goals_by_rule.get(s.get("semantic_rule_id"),False)]; generated=[]
    for r in matched:
        if not goals_by_rule.get(r["rule_id"]): continue
        local=[s for s in sem if s.get("semantic_rule_id")==r["rule_id"]]+context
        for c in V12.synthesize(seq,local,prior,pattern_id,config):
            c["semantic_primary_rule_id"]=r["rule_id"]; generated.append(c)
    return generated
def refresh_interpretations(data,intents):
    keep=[x for x in data.get("interpretation_candidates",[]) if x.get("claim_type")!="INTENT"]
    for c in intents: keep.append({"interpretation_id":V12.sid("INTP",data["sequence_id"],c["intent_candidate_id"]),"sequence_id":data["sequence_id"],"claim":c["machine_description"],"claim_type":"INTENT","supporting_micro_unit_ids":[m.get("micro_unit_id") for m in data.get("micro_units",[])],"supporting_sequence_ids":c.get("supporting_sequence_ids",[]),"contradicting_sequence_ids":[],"alternative_interpretation_ids":[],"epistemic_status":"HYPOTHESIZED","confidence":None,"direct_action_authority":False,"intent_candidate_ref":c["intent_candidate_id"]})
    data["interpretation_candidates"]=keep
def refresh_contribution(data,intents,parameter_refs):
    new=sum(c.get("novelty_status")=="NEW_LIVE_INTENT_CANDIDATE" for c in intents); prior=sum(c.get("novelty_status")=="MATCHES_PRIOR_INTENT_SIGNATURE" for c in intents); kind="MIXED_NEW_AND_PRIOR" if new and prior else ("NEW_INTENT_CANDIDATE_SIGNAL" if new else ("SUPPORT_PRIOR_INTENT" if prior else "NO_INTENT_CANDIDATE")); pc=data.get("pattern_candidate") or {}; data["intent_contribution"]={"contribution_id":V12.sid("INT-CONTRIB",data["sequence_id"],*[c.get("signature") for c in intents]),"sequence_id":data["sequence_id"],"candidate_ids":[c["intent_candidate_id"] for c in intents],"contribution_type":kind,"parameter_refs":sorted(set(parameter_refs)),"pattern_refs":[pc["pattern_candidate_id"]] if pc.get("pattern_candidate_id") else [],"proof_debt_present":bool(intents)}
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--text",required=True); ap.add_argument("--speaker",default="USER"); ap.add_argument("--sequence-id"); ap.add_argument("--history"); ap.add_argument("--review-decision"); ap.add_argument("--parameter-signals"); ap.add_argument("--no-auto-parameters",action="store_true"); ap.add_argument("--auto-parameter-limit",type=int,default=24); ap.add_argument("--output"); args=ap.parse_args()
    with tempfile.TemporaryDirectory() as td:
        out=Path(td)/"v13.json"; cmd=[sys.executable,str(BASE),"--text",args.text,"--speaker",args.speaker,"--output",str(out),"--auto-parameter-limit",str(args.auto_parameter_limit)]
        if args.sequence_id: cmd += ["--sequence-id",args.sequence_id]
        if args.history: cmd += ["--history",args.history]
        if args.review_decision: cmd += ["--review-decision",args.review_decision]
        if args.parameter_signals: cmd += ["--parameter-signals",args.parameter_signals]
        if args.no_auto_parameters: cmd += ["--no-auto-parameters"]
        p=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True)
        if p.returncode!=0: sys.stderr.write(p.stderr); raise SystemExit(p.returncode)
        data=load(out)
    seq=data["sequence_id"]; intake=data.get("intake",{}).get("intake_id"); sem,matched=semantic_signals(args.text,seq,intake); signals=merge_signals(data.get("intent_signals",[]),sem)
    if matched:
        data["features"]=sorted(set(data.get("features",[]))|{"SEMANTIC_INTENT_ACTIVATION","LIVE_INTENT_SYNTHESIS","INTENT_INFERENCE","UNCERTAINTY","PROOF_DEBT"}); V12.ensure_rubric_activations(data,sorted({rid for r in matched for rid in r.get("rubrics",[])}|{"R07","R10","R22","R43"})); V12.ensure_human_containers(data,sorted({cid for r in matched for cid in r.get("containers",[])})); V12.ensure_engine_routes(data)
    config=load(ROOT/"machine/runtime/INTENT_HYPOTHESIS_SYNTHESIS_RUNTIME_V1.json"); prior=V12.prior_intents(V12.read_history(args.history)); pc=data.get("pattern_candidate") or {}; generated=rule_local_candidates(seq,sem,matched,prior,pc.get("pattern_candidate_id"),config); intents=merge_intents(data.get("intent_hypotheses",[]),generated,signals); data["intent_signals"]=signals; data["intent_hypotheses"]=intents; refresh_interpretations(data,intents); param_refs=sorted({p for c in intents for p in c.get("supporting_parameter_refs",[]) if p}); refresh_contribution(data,intents,param_refs)
    if pc and intents: pc["intent_status"]="INFERRED" if pc.get("intent_status")=="UNKNOWN" else pc.get("intent_status"); pc["candidate_intent_ids"]=[c["intent_candidate_id"] for c in intents]; pc["parameter_refs"]=sorted(set(pc.get("parameter_refs",[])+param_refs))
    explicit_ids=[x.get("parameter_id") for x in V13.explicit_parameter_items(args.parameter_signals) if x.get("parameter_id")]; auto=data.get("auto_parameter_activation_candidates") or {}; exact=auto.get("exact_name_matches_that_fed_live_intent",[]); fuzzy=auto.get("token_overlap_candidates_review_only",[]); events=V13.build_event_records(data,args.speaker); ledger=V13.growth_ledger(data,events,explicit_ids,exact,fuzzy); data["event_records"]=events; data["event_intent_records"]=[e["intent"] for e in events]; data["event_growth_ledger"]=ledger; data["semantic_intent_rule_hits"]=[{"rule_id":r["rule_id"],"name":r["name"],"intent_scope":r.get("intent_scope"),"containers":r.get("containers",[]),"rubrics":r.get("rubrics",[])} for r in matched]; data["semantic_intent_runtime_id"]="EVENT-SEMANTIC-INTENT-RULES-V1"; data["interpreter_version"]="P2-MICRO-SEQUENCE-LIVE-INTERPRETER-001/V1.4"; data["supersedes_interpreter"]="P2-MICRO-SEQUENCE-LIVE-INTERPRETER-001/V1.3"; data["correction"]="V1.4 adds reusable semantic Event rules and rule-local intent composition, avoiding broad cross-rule Cartesian mixing while generating live intent beyond request/resource language."; data["epistemic_guard"]="Semantic rule hits are review-required inference signals. They expand live intent search but do not prove actor intent or create canonical parameters. Event Intent may remain UNKNOWN. Natural/functional direction is not conscious agency."
    review=data.get("reviewable_rubric_view") or {}; prop=review.setdefault("machine_proposal",{}); prop["intent_hypotheses"]=intents; prop["intent_contribution"]=data["intent_contribution"]; prop["event_records"]=events; prop["event_growth_ledger"]=ledger; prop["semantic_intent_rule_hits"]=data["semantic_intent_rule_hits"]; prop["summary"]="V1.4 Event-semantic growth proposal: existing IDs and rule-local semantic activations form multiple live intent signatures; all generated intent remains reviewable and non-canonical."; data["reviewable_rubric_view"]=review; text=json.dumps(data,indent=2,ensure_ascii=False); Path(args.output).write_text(text,encoding="utf-8") if args.output else print(text)
if __name__=="__main__": main()
