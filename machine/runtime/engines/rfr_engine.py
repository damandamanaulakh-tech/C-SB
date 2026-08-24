#!/usr/bin/env python3
"""Reverse → Forward → Reverse (R-F-R) audit engine.

R-F-R is a structural falsification/audit loop, not hidden chain-of-thought.
The engine records observable checks:

1. Reverse: can the hypothesis trace back to locked source/Point Zero and its
   declared dependencies?
2. Forward: do its declared evidence predictions survive available tests?
3. Reverse audit: after seeing those results, which assumptions/proof debts are
   still necessary, contradictory, or unexplained?

The output is a machine-readable assessment; no private reasoning trace is
stored or required.
"""
from __future__ import annotations

from collections import defaultdict
from typing import Any, Iterable, Mapping, Sequence

from .runtime_core import EngineResult, RuntimeContractError, TraceStep, clamp, stable_id

ENGINE_ID = "SB-RT-ENG-RFR-001"
RULES = [
    "REVERSE_FORWARD_REVERSE_REQUIRED_FOR_SYNTHETIC_PROMOTION",
    "UNKNOWN_NE_PASS",
    "CONTRADICTION_MUST_SURVIVE_AUDIT",
    "SOURCE_LINEAGE_REQUIRED",
    "RFR_NE_PRIVATE_CHAIN_OF_THOUGHT",
]

SUPPORT_RESULTS = {"PASS", "SUPPORTS", "SUPPORTED", "CONFIRMED"}
CONTRADICT_RESULTS = {"FAIL", "CONTRADICTS", "FALSIFIED", "REFUTED"}
UNKNOWN_RESULTS = {"NOT_RUN", "UNKNOWN", "UNAVAILABLE", "INCONCLUSIVE", "OPEN"}


def _hypothesis_refs(
    intents: Sequence[Mapping[str, Any]],
    future_states: Sequence[Mapping[str, Any]],
    combinations: Sequence[Mapping[str, Any]],
) -> dict[str, Mapping[str, Any]]:
    result: dict[str, Mapping[str, Any]] = {}
    for collection, key in ((intents, "intent_id"), (future_states, "future_state_id"), (combinations, "combination_id")):
        for item in collection:
            if isinstance(item, Mapping) and item.get(key):
                result[str(item[key])] = item
    return result


def _prediction_results(
    predictions: Sequence[Mapping[str, Any]],
    evidence_results: Mapping[str, Mapping[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    grouped: dict[str, list[dict[str, Any]]] = defaultdict(list)
    for prediction in predictions:
        pid = str(prediction.get("evidence_prediction_id", ""))
        href = str(prediction.get("hypothesis_ref", ""))
        if not pid or not href:
            continue
        supplied = evidence_results.get(pid, {})
        result = str(supplied.get("result", supplied.get("status", prediction.get("test_result", "NOT_RUN")))).upper()
        grouped[href].append({
            "evidence_prediction_id": pid,
            "test_type": prediction.get("test_type"),
            "priority": prediction.get("priority", "NORMAL"),
            "result": result,
            "supporting_evidence_refs": list(supplied.get("supporting_evidence_refs", prediction.get("supporting_evidence_refs", []))),
            "contradicting_evidence_refs": list(supplied.get("contradicting_evidence_refs", prediction.get("contradicting_evidence_refs", []))),
            "source_independence_groups": list(supplied.get("source_independence_groups", [])),
            "notes": supplied.get("notes"),
        })
    return grouped


def _reverse_pass(event: Mapping[str, Any], hypothesis_ref: str, hypothesis: Mapping[str, Any]) -> dict[str, Any]:
    source_refs = hypothesis.get("source_refs", [])
    event_source_ids = {
        str(ref.get("source_id")) for ref in event.get("source_refs", [])
        if isinstance(ref, Mapping) and ref.get("source_id")
    }
    hypothesis_sources = {str(x) for x in source_refs if x}
    point_zero_ref = hypothesis.get("point_zero_ref") or (hypothesis.get("point_zero_refs", [None])[0] if hypothesis.get("point_zero_refs") else None)
    event_pz = event.get("point_zero", {}).get("point_zero_id")
    source_trace_ok = not hypothesis_sources or bool(hypothesis_sources & event_source_ids)
    point_zero_ok = point_zero_ref in {None, event_pz} or point_zero_ref in set(hypothesis.get("point_zero_refs", []))
    lineage = hypothesis.get("lineage", [])
    lineage_present = bool(lineage) or bool(source_refs) or hypothesis_ref == event.get("event_id")
    hard_failures = []
    if not source_trace_ok:
        hard_failures.append("SOURCE_TRACE_MISMATCH")
    if not point_zero_ok:
        hard_failures.append("POINT_ZERO_TRACE_MISMATCH")
    if not lineage_present:
        hard_failures.append("LINEAGE_MISSING")
    return {
        "pass": "REVERSE",
        "hypothesis_ref": hypothesis_ref,
        "source_trace_ok": source_trace_ok,
        "point_zero_trace_ok": point_zero_ok,
        "lineage_present": lineage_present,
        "hard_failures": hard_failures,
        "status": "PASS" if not hard_failures else "FAIL",
    }


def _forward_pass(hypothesis_ref: str, tests: Sequence[Mapping[str, Any]]) -> dict[str, Any]:
    support = [t for t in tests if t["result"] in SUPPORT_RESULTS]
    contradict = [t for t in tests if t["result"] in CONTRADICT_RESULTS]
    unknown = [t for t in tests if t["result"] in UNKNOWN_RESULTS or t["result"] not in SUPPORT_RESULTS | CONTRADICT_RESULTS]
    critical_contradictions = [t for t in contradict if t.get("priority") == "CRITICAL"]
    tested = len(support) + len(contradict)
    score = 0.0
    if tests:
        score = (len(support) - len(contradict)) / len(tests)
    score = clamp((score + 1.0) / 2.0)
    if critical_contradictions:
        status = "FAIL"
    elif contradict:
        status = "CONTRADICTED"
    elif tested == 0:
        status = "UNKNOWN"
    elif unknown:
        status = "PARTIAL"
    else:
        status = "PASS"
    return {
        "pass": "FORWARD",
        "hypothesis_ref": hypothesis_ref,
        "support_count": len(support),
        "contradiction_count": len(contradict),
        "unknown_count": len(unknown),
        "critical_contradiction_count": len(critical_contradictions),
        "evidence_score": round(score, 6),
        "tested_prediction_count": tested,
        "total_prediction_count": len(tests),
        "supporting_evidence_refs": sorted({e for t in support for e in t.get("supporting_evidence_refs", [])}),
        "contradicting_evidence_refs": sorted({e for t in contradict for e in t.get("contradicting_evidence_refs", [])}),
        "status": status,
    }


def _reverse_audit(hypothesis_ref: str, hypothesis: Mapping[str, Any], reverse: Mapping[str, Any], forward: Mapping[str, Any]) -> dict[str, Any]:
    original_debt = list(hypothesis.get("proof_debt", []))
    unresolved = list(original_debt)
    new_debt: list[str] = []
    if forward.get("unknown_count", 0):
        new_debt.append("UNTESTED_OR_INCONCLUSIVE_PREDICTIONS_REMAIN")
    if forward.get("contradiction_count", 0):
        new_debt.append("CONTRADICTING_EVIDENCE_REQUIRES_EXPLANATION_OR_REJECTION")
    if not reverse.get("source_trace_ok"):
        new_debt.append("SOURCE_TRACE_REPAIR_REQUIRED")
    if not reverse.get("point_zero_trace_ok"):
        new_debt.append("POINT_ZERO_TRACE_REPAIR_REQUIRED")
    unresolved = sorted(set(unresolved + new_debt))
    if reverse.get("status") == "FAIL" or forward.get("status") == "FAIL":
        status = "FAIL"
    elif forward.get("status") == "CONTRADICTED":
        status = "WEAKEN_OR_REJECT"
    elif unresolved:
        status = "OPEN_PROOF_DEBT"
    elif forward.get("status") == "PASS":
        status = "PASS"
    else:
        status = "UNKNOWN"
    return {
        "pass": "REVERSE_AUDIT",
        "hypothesis_ref": hypothesis_ref,
        "original_proof_debt": original_debt,
        "new_proof_debt": new_debt,
        "unresolved_proof_debt": unresolved,
        "status": status,
    }


def run_rfr(
    event: Mapping[str, Any],
    *,
    intent_candidates: Sequence[Mapping[str, Any]] = (),
    future_states: Sequence[Mapping[str, Any]] = (),
    combination_records: Sequence[Mapping[str, Any]] = (),
    evidence_predictions: Sequence[Mapping[str, Any]] = (),
    evidence_results: Mapping[str, Mapping[str, Any]] | None = None,
) -> EngineResult:
    event_id = str(event.get("event_id", ""))
    if not event_id:
        raise RuntimeContractError("R-F-R engine requires event_id")
    evidence_results = evidence_results or {}
    hypotheses = _hypothesis_refs(intent_candidates, future_states, combination_records)
    tests_by_hypothesis = _prediction_results(evidence_predictions, evidence_results)
    assessments: list[dict[str, Any]] = []

    for href, hypothesis in hypotheses.items():
        reverse = _reverse_pass(event, href, hypothesis)
        forward = _forward_pass(href, tests_by_hypothesis.get(href, []))
        audit = _reverse_audit(href, hypothesis, reverse, forward)
        if reverse["status"] == "FAIL" or forward["status"] == "FAIL":
            overall = "FAIL"
        elif forward["status"] == "CONTRADICTED":
            overall = "WEAKEN_OR_REJECT"
        elif audit["status"] == "PASS":
            overall = "PASS"
        else:
            overall = "OPEN"
        assessments.append({
            "rfr_assessment_id": stable_id("RFR", event_id, href, reverse, forward, audit),
            "event_id": event_id,
            "hypothesis_ref": href,
            "reverse": reverse,
            "forward": forward,
            "reverse_audit": audit,
            "overall_status": overall,
            "direct_action_authority": False,
        })

    trace = TraceStep.create(
        ENGINE_ID,
        "RUN_REVERSE_FORWARD_REVERSE",
        input_refs=[event_id] + sorted(hypotheses),
        output_refs=[a["rfr_assessment_id"] for a in assessments],
        rule_refs=RULES,
        notes=[
            f"hypothesis_count={len(hypotheses)}",
            f"pass={sum(1 for a in assessments if a['overall_status']=='PASS')}",
            f"open={sum(1 for a in assessments if a['overall_status']=='OPEN')}",
            f"weaken_or_reject={sum(1 for a in assessments if a['overall_status']=='WEAKEN_OR_REJECT')}",
            f"fail={sum(1 for a in assessments if a['overall_status']=='FAIL')}",
        ],
    )
    return EngineResult(
        ENGINE_ID,
        "COMPLETE",
        {
            "event_id": event_id,
            "assessments": assessments,
            "assessment_count": len(assessments),
            "pass_count": sum(1 for a in assessments if a["overall_status"] == "PASS"),
            "open_count": sum(1 for a in assessments if a["overall_status"] == "OPEN"),
            "weaken_or_reject_count": sum(1 for a in assessments if a["overall_status"] == "WEAKEN_OR_REJECT"),
            "fail_count": sum(1 for a in assessments if a["overall_status"] == "FAIL"),
        },
        [trace],
    )
