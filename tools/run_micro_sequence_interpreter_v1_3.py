#!/usr/bin/env python3
from pathlib import Path
import argparse, hashlib, json, re, subprocess, sys, tempfile

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT / "tools/run_micro_sequence_interpreter_v1_2.py"
HFR = ROOT / "generated/registry_views/human_functional_3204_registry_v1.json"
KING_CANDIDATES = ROOT / "registries/human/HUMAN_KING_PROFILE_PARAMETER_CANDIDATES_V0.json"
LEDGER_CONFIG = ROOT / "machine/runtime/EVENT_GROWTH_LEDGER_RUNTIME_V1.json"
STOPWORDS = {"a","an","and","are","as","at","be","been","being","by","for","from","had","has","have","he","her","his","i","in","is","it","its","of","on","or","our","she","that","the","their","them","they","this","to","was","we","were","with","you","your","state","ability","capacity","process","system","general","overall","level","response","function","functional"}

def load(path): return json.loads(Path(path).read_text(encoding="utf-8"))
def hid(*parts): return hashlib.sha256("\x1f".join(str(x) for x in parts).encode()).hexdigest()[:16].upper()
def sid(prefix,*parts): return f"{prefix}-{hid(*parts)}"
def norm_text(value): return re.sub(r"\s+"," ",re.sub(r"[^a-z0-9]+"," ",str(value).lower())).strip()
def tokens(value): return [x for x in norm_text(value).split() if x and x not in STOPWORDS and len(x)>2]

def parameter_rows():
    if not HFR.exists(): return []
    raw=load(HFR); rows=raw if isinstance(raw,list) else raw.get("parameters",[]); out=[]
    for row in rows:
        pid=row.get("parameter_id") or row.get("id"); name=row.get("name") or row.get("exact_name") or row.get("parameter_name")
        if pid and name: out.append({"parameter_id":pid,"name":name})
    return out

def auto_parameter_candidates(text,limit):
    nt=norm_text(text); itoks=set(tokens(text)); exact=[]; fuzzy=[]
    for row in parameter_rows():
        name=row["name"]; nn=norm_text(name); sig=tokens(name)
        if not nn or not sig: continue
        if len(sig)==1:
            w=sig[0]; exact_hit=len(w)>=5 and re.search(rf"\b{re.escape(w)}\b",nt) is not None
        else: exact_hit=re.search(rf"\b{re.escape(nn)}\b",nt) is not None
        if exact_hit:
            exact.append({"parameter_id":row["parameter_id"],"name":name,"activation_mode":"AUTO_EXACT_NAME_MATCH","activation_status":"CANDIDATE_ACTIVATION","match_score":1.0}); continue
        overlap=len(set(sig)&itoks); coverage=overlap/max(len(set(sig)),1)
        if overlap>=2 and coverage>=0.75:
            fuzzy.append({"parameter_id":row["parameter_id"],"name":name,"activation_mode":"AUTO_TOKEN_OVERLAP","activation_status":"REVIEW_REQUIRED_CANDIDATE","match_score":round(coverage,3)})
    exact=sorted(exact,key=lambda x:(x["name"],x["parameter_id"]))[:limit]
    fuzzy=sorted(fuzzy,key=lambda x:(-x["match_score"],x["name"],x["parameter_id"]))[:limit]
    return exact,fuzzy

def explicit_parameter_items(path):
    if not path: return []
    raw=load(path); return raw if isinstance(raw,list) else raw.get("signals",[])

def candidate_parameter_ids():
    if not KING_CANDIDATES.exists(): return set()
    return {x.get("candidate_id") for x in load(KING_CANDIDATES).get("candidates",[]) if x.get("candidate_id")}

def event_type_for_facets(facets):
    f=set(facets or [])
    if "REQUEST" in f: return "REQUEST_EVENT"
    if "DECISION_LANGUAGE" in f: return "DECISION_EVENT"
    if "PERSON_TRANSFER_OR_PRESENCE" in f: return "TRANSFER_OR_PRESENCE_EVENT"
    if "EMOTION_LANGUAGE" in f: return "AFFECT_OR_STATE_EVENT"
    if "REPETITION" in f: return "REPEATED_DESCRIBED_EVENT"
    if "NEGATION" in f: return "NEGATED_OR_ABSENT_STATE_EVENT"
    return "DESCRIBED_EVENT"

def unknown_intent(event_id,source_refs):
    return {"intent_id":sid("INTENT",event_id,"UNKNOWN"),"event_id":event_id,"intent_type":"UNKNOWN","stated_intent":None,"inferred_intent":None,"stated_motive":None,"operating_motive_hypothesis":None,"goal":None,"target":None,"method":None,"conditions":[],"typed_order_refs":[],"actor_view_refs":[],"supporting_evidence_refs":list(source_refs),"contradicting_evidence_refs":[],"alternative_intent_ids":[],"falsifiers":[],"proof_debt":["Intent has not yet been decoded for this event."],"epistemic_status":"UNKNOWN","review_status":"NOT_REVIEWED","source_refs":list(source_refs)}

def case_intent(event_id,intents,signals,source_refs):
    if not intents: return unknown_intent(event_id,source_refs)
    goals=sorted({x for c in intents for x in c.get("goal_atoms",[])}); targets=sorted({x for c in intents for x in c.get("target_atoms",[])}); methods=sorted({x for c in intents for x in c.get("method_atoms",[])})
    conditions=sorted({x for c in intents for x in (c.get("condition_atoms",[])+c.get("constraint_atoms",[])+c.get("state_atoms",[]))}); candidate_ids=[c["intent_candidate_id"] for c in intents]
    return {"intent_id":sid("INTENT",event_id,*candidate_ids),"event_id":event_id,"intent_type":"DERIVED_INTENT_HYPOTHESIS","stated_intent":None,"inferred_intent":candidate_ids,"stated_motive":None,"operating_motive_hypothesis":None,"goal":goals,"target":targets,"method":methods,"conditions":conditions,"typed_order_refs":sorted({x for c in intents for x in c.get("order_atoms",[])}),"actor_view_refs":[],"supporting_evidence_refs":sorted({s.get("signal_id") for s in signals if s.get("signal_id")} | set(source_refs)),"contradicting_evidence_refs":[],"alternative_intent_ids":candidate_ids,"falsifiers":sorted({x for c in intents for x in c.get("falsifiers",[])}),"proof_debt":sorted({x for c in intents for x in c.get("proof_debt",[])}),"epistemic_status":"HYPOTHESIZED","review_status":"NOT_REVIEWED","source_refs":list(source_refs)}

def build_event_records(data,speaker):
    seq=data["sequence_id"]; intake=data.get("intake",{}); intake_id=intake.get("intake_id"); mus=data.get("micro_units",[]); intents=data.get("intent_hypotheses",[]); signals=data.get("intent_signals",[])
    rubric_refs=sorted({(a.get("rubric_path") or [None])[0] for a in data.get("rubric_activations",[]) if (a.get("rubric_path") or [None])[0]}); container_refs=sorted({(a.get("rubric_path") or [None])[-1] for a in data.get("human_container_activations",[]) if a.get("rubric_path")}); parameter_refs=sorted({p for c in intents for p in c.get("supporting_parameter_refs",[]) if p})
    pc=data.get("pattern_candidate") or {}; pattern_refs=[pc["pattern_candidate_id"]] if pc.get("pattern_candidate_id") else []; contrib=data.get("pattern_contribution") or {}; contribution_refs=[contrib["contribution_id"]] if contrib.get("contribution_id") else []
    source_id=sid("EVT-SOURCE",seq,intake_id); case_id=sid("EVT-CASE",seq,intake_id); clause_ids=[sid("EVT-DESC",seq,m.get("micro_unit_id")) for m in mus]
    source_event={"event_id":source_id,"event_type":"SOURCE_UTTERANCE_EVENT","sequence_id":seq,"parent_event_id":None,"child_event_ids":[case_id],"source_refs":[intake_id] if intake_id else [],"source_span_refs":[],"actor_ids":[speaker] if speaker else [],"object_ids":[],"prior_state_refs":[],"resulting_state_refs":[],"relation_ids":[],"order_types":[],"parameter_refs":[],"rubric_refs":rubric_refs,"container_refs":[],"intent_candidate_ids":[],"intent":unknown_intent(source_id,[intake_id] if intake_id else []),"candidate_brain_state_ids":[],"combination_ids":[],"pattern_contribution_ids":[],"memory_write_refs":[],"observer_or_view_refs":[],"epistemic_status":"OBSERVED_INPUT_OCCURRENCE","event_status":"OPEN_FOR_REPRESENTATION"}
    case_sources=([intake_id] if intake_id else [])+[m.get("micro_unit_id") for m in mus if m.get("micro_unit_id")]
    case_event={"event_id":case_id,"event_type":"REPRESENTED_CASE_EVENT","sequence_id":seq,"parent_event_id":source_id,"child_event_ids":clause_ids,"source_refs":case_sources,"source_span_refs":[m.get("micro_unit_id") for m in mus if m.get("micro_unit_id")],"actor_ids":[],"object_ids":[],"prior_state_refs":[],"resulting_state_refs":[],"relation_ids":sorted({r for m in mus for r in m.get("relation_ids",[])}),"order_types":sorted({o for m in mus for o in m.get("order_types",[])}),"parameter_refs":parameter_refs,"rubric_refs":rubric_refs,"container_refs":container_refs,"intent_candidate_ids":[c["intent_candidate_id"] for c in intents],"intent":case_intent(case_id,intents,signals,case_sources),"candidate_brain_state_ids":[],"combination_ids":[sid("COMB",seq,c["signature"]) for c in intents],"pattern_contribution_ids":contribution_refs,"memory_write_refs":[],"observer_or_view_refs":[],"epistemic_status":"REPRESENTED_FROM_SOURCE","event_status":"REVIEW_REQUIRED"}
    described=[]
    for event_id,m in zip(clause_ids,mus):
        refs=[x for x in [intake_id,m.get("micro_unit_id")] if x]
        described.append({"event_id":event_id,"event_type":event_type_for_facets(m.get("detected_facets",[])),"sequence_id":seq,"parent_event_id":case_id,"child_event_ids":[],"source_refs":refs,"source_span_refs":[m.get("micro_unit_id")] if m.get("micro_unit_id") else [],"actor_ids":[],"object_ids":list(m.get("linked_object_ids",[])),"prior_state_refs":[],"resulting_state_refs":[],"relation_ids":list(m.get("relation_ids",[])),"order_types":list(m.get("order_types",[])),"parameter_refs":[],"rubric_refs":rubric_refs,"container_refs":container_refs,"intent_candidate_ids":[],"intent":unknown_intent(event_id,refs),"candidate_brain_state_ids":[],"combination_ids":[],"pattern_contribution_ids":[],"memory_write_refs":[],"observer_or_view_refs":list(m.get("view_state_refs",[])),"epistemic_status":"REPORTED_OR_DESCRIBED","event_status":"OPEN_INTENT"})
    return [source_event,case_event]+described

def growth_ledger(data,events,explicit_ids,auto_exact,auto_fuzzy):
    seq=data["sequence_id"]; intents=data.get("intent_hypotheses",[]); intent_signatures=[c.get("signature") for c in intents if c.get("signature")]; prior=[c for c in intents if c.get("novelty_status")=="MATCHES_PRIOR_INTENT_SIGNATURE"]; new=[c for c in intents if c.get("novelty_status")=="NEW_LIVE_INTENT_CANDIDATE"]
    containers=sorted({(a.get("rubric_path") or [None])[-1] for a in data.get("human_container_activations",[]) if a.get("rubric_path")}); rubrics=sorted({(a.get("rubric_path") or [None])[0] for a in data.get("rubric_activations",[]) if (a.get("rubric_path") or [None])[0]}); review_candidates=candidate_parameter_ids(); explicit_review=sorted(set(explicit_ids)&review_candidates)
    pattern_refs=[]; contrib=data.get("pattern_contribution") or {}; pc=data.get("pattern_candidate") or {}
    if contrib.get("contribution_id"): pattern_refs.append(contrib["contribution_id"])
    if pc.get("pattern_candidate_id"): pattern_refs.append(pc["pattern_candidate_id"])
    event_ids=[e["event_id"] for e in events]; source_count=sum(1 for e in events if e["event_type"]=="SOURCE_UTTERANCE_EVENT")
    counts={"source_event_count":source_count,"represented_event_count":len(events)-source_count,"existing_container_ids_activated":len(containers),"existing_rubric_ids_activated":len(rubrics),"explicit_atomic_parameter_ids_activated":len(set(explicit_ids)),"auto_atomic_parameter_candidates":len(auto_exact)+len(auto_fuzzy),"intent_signals":len(data.get("intent_signals",[])),"live_intents_generated":len(intents),"prior_intent_signatures_matched":len(prior),"new_live_intent_signatures":len(new),"pattern_contributions":1 if contrib.get("contribution_id") else 0,"pattern_candidates":1 if pc.get("pattern_candidate_id") else 0,"review_required_parameter_candidates_activated":len(explicit_review),"validated_support_delta":0,"canonical_parameter_additions":0,"canonical_pattern_additions":0}
    return {"growth_contribution_id":sid("GROWTH",seq,*event_ids,*intent_signatures),"sequence_id":seq,"event_ids":event_ids,"count_layers":{"occurrence":"RECORDED","activation":"CANDIDATE_ACTIVATION_RECORDED","candidate_support":"RECORDED_IF_PRESENT","validated_support":"NO_DELTA_UNTIL_REVIEW","canonical":"NO_DELTA_UNTIL_EXPLICIT_PROMOTION"},"counts":counts,"existing_id_activation_refs":{"container_ids":containers,"rubric_ids":rubrics,"explicit_parameter_ids":sorted(set(explicit_ids)),"auto_exact_parameter_candidate_ids":[x["parameter_id"] for x in auto_exact],"auto_fuzzy_parameter_candidate_ids":[x["parameter_id"] for x in auto_fuzzy],"review_required_parameter_candidate_ids":explicit_review},"intent_signature_refs":intent_signatures,"pattern_refs":pattern_refs,"candidate_support_deltas":[{"signature":c.get("signature"),"candidate_id":c.get("intent_candidate_id"),"delta":1,"status":c.get("novelty_status")} for c in intents],"validated_support_deltas":[],"canonical_additions":[],"contradiction_refs":[],"proof_debt":sorted({x for c in intents for x in c.get("proof_debt",[])}),"approval_state":"REVIEW_REQUIRED","writeback_status":"OCCURRENCE_AND_CANDIDATE_TRACE_ONLY","provenance_refs":[data.get("intake",{}).get("intake_id")]}

def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--text",required=True); ap.add_argument("--speaker",default="USER"); ap.add_argument("--sequence-id"); ap.add_argument("--history"); ap.add_argument("--review-decision"); ap.add_argument("--parameter-signals"); ap.add_argument("--no-auto-parameters",action="store_true"); ap.add_argument("--auto-parameter-limit",type=int,default=24); ap.add_argument("--output"); args=ap.parse_args()
    explicit=explicit_parameter_items(args.parameter_signals); explicit_ids=[x.get("parameter_id") for x in explicit if x.get("parameter_id")]; auto_exact,auto_fuzzy=([],[])
    if not args.no_auto_parameters:
        try: auto_exact,auto_fuzzy=auto_parameter_candidates(args.text,max(0,args.auto_parameter_limit))
        except Exception: auto_exact,auto_fuzzy=[],[]
    combined=list(explicit); seen={x.get("parameter_id") for x in combined if x.get("parameter_id")}
    for row in auto_exact:
        if row["parameter_id"] not in seen: combined.append({"parameter_id":row["parameter_id"]}); seen.add(row["parameter_id"])
    with tempfile.TemporaryDirectory() as td:
        td=Path(td); base_out=td/"base.json"; param_path=None
        if combined:
            param_path=td/"parameter_signals.json"; param_path.write_text(json.dumps({"signals":combined},indent=2),encoding="utf-8")
        cmd=[sys.executable,str(BASE),"--text",args.text,"--speaker",args.speaker,"--output",str(base_out)]
        if args.sequence_id: cmd += ["--sequence-id",args.sequence_id]
        if args.history: cmd += ["--history",args.history]
        if args.review_decision: cmd += ["--review-decision",args.review_decision]
        if param_path: cmd += ["--parameter-signals",str(param_path)]
        proc=subprocess.run(cmd,cwd=ROOT,text=True,capture_output=True)
        if proc.returncode!=0: sys.stderr.write(proc.stderr); raise SystemExit(proc.returncode)
        data=load(base_out)
    events=build_event_records(data,args.speaker); ledger=growth_ledger(data,events,explicit_ids,auto_exact,auto_fuzzy)
    data["event_records"]=events; data["event_intent_records"]=[e["intent"] for e in events]; data["auto_parameter_activation_candidates"]={"exact_name_matches_that_fed_live_intent":auto_exact,"token_overlap_candidates_review_only":auto_fuzzy,"guard":"Only exact-name auto matches feed V1.3 live intent. Token-overlap candidates are review-only and do not alter intent synthesis."}; data["event_growth_ledger"]=ledger; data["event_growth_runtime_id"]=load(LEDGER_CONFIG).get("runtime_id") if LEDGER_CONFIG.exists() else "EVENT-GROWTH-LEDGER-RUNTIME-V1"; data["interpreter_version"]="P2-MICRO-SEQUENCE-LIVE-INTERPRETER-001/V1.3"; data["supersedes_interpreter"]="P2-MICRO-SEQUENCE-LIVE-INTERPRETER-001/V1.2"; data["correction"]="V1.3 makes Event/Intent output first-class, records separate occurrence/activation/candidate-support/validated/canonical growth counts, and adds conservative atomic Human parameter auto-activation candidates."; data["epistemic_guard"]="Every event receives an intent record, but UNKNOWN is valid. Natural or non-agentic events must not be given conscious intent without evidence. Auto parameter matching is candidate activation, not validated truth. Occurrence/candidate counts may grow automatically; validated and canonical counts remain zero until review/promotion."
    review=data.get("reviewable_rubric_view") or {}; proposal=review.setdefault("machine_proposal",{}); proposal["event_records"]=events; proposal["event_growth_ledger"]=ledger; proposal["auto_parameter_activation_candidates"]=data["auto_parameter_activation_candidates"]; proposal["summary"]="V1.3 real-time growing ASI proposal: Event → existing IDs → live intent → pattern contribution → tiered growth ledger. Example occurrence grows automatically; semantic/canonical promotion remains gated."; unknowns=review.setdefault("unknowns",[])
    for x in ["which auto atomic parameter candidates are semantically correct beyond lexical match","which Event intent hypotheses, if any, match the actor/system intent","whether candidate support should be promoted to validated support"]:
        if x not in unknowns: unknowns.append(x)
    data["reviewable_rubric_view"]=review; text=json.dumps(data,indent=2,ensure_ascii=False)
    if args.output: Path(args.output).write_text(text,encoding="utf-8")
    else: print(text)

if __name__=="__main__": main()
