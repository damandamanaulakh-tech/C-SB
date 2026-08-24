#!/usr/bin/env python3
"""Declarative falsifier engine.

A falsifier is an explicit condition that can kill or materially weaken a
hypothesis.  Low confidence alone is not a falsifier.  The engine evaluates a
small safe operator language against structured runtime facts/evidence results.
"""
from __future__ import annotations

from typing import Any, Mapping, Sequence

from .runtime_core import EngineResult, RuntimeContractError, TraceStep, stable_id

ENGINE_ID = "SB-RT-ENG-FALSIFIER-001"
RULES = [
    "FALSIFIER_MUST_BE_DECLARED",
    "LOW_SCORE_NE_FALSIFICATION",
    "UNKNOWN_NE_FALSIFIED",
    "FALSIFICATION_SCOPE_MUST_BE_EXPLICIT",
]

SUPPORTED_OPERATORS = {
    "EXISTS",
    "NOT_EXISTS",
    "EQUALS",
    "NOT_EQUALS",
    "IN",
    "NOT_IN",
    "GT",
    "GTE",
    "LT",
    "LTE",
    "ANY_CONTRADICTION",
    "PREDICTION_RESULT_IS",
}


def _resolve_path(context: Mapping[str, Any], path: str) -> tuple[bool, Any]:
    current: Any = context
    if not path:
        return True, current
    for part in path.split("."):
        if isinstance(current, Mapping) and part in current:
            current = current[part]
        else:
            return False, None
    return True, current


def _evaluate(condition: Mapping[str, Any], context: Mapping[str, Any]) -> tuple[str, Any]:
    operator = str(condition.get("operator", ""))
    if operator not in SUPPORTED_OPERATORS:
        raise RuntimeContractError(f"Unsupported falsifier operator: {operator}")
    path = str(condition.get("path", ""))
    exists, actual = _resolve_path(context, path)
    expected = condition.get("value")

    if operator == "EXISTS":
        return ("MET" if exists and actual is not None else "NOT_MET"), actual
    if operator == "NOT_EXISTS":
        return ("MET" if not exists or actual is None else "NOT_MET"), actual
    if not exists:
        return "UNKNOWN", None
    if operator == "EQUALS":
        return ("MET" if actual == expected else "NOT_MET"), actual
    if operator == "NOT_EQUALS":
        return ("MET" if actual != expected else "NOT_MET"), actual
    if operator == "IN":
        try:
            return ("MET" if actual in expected else "NOT_MET"), actual
        except TypeError:
            return "UNKNOWN", actual
    if operator == "NOT_IN":
        try:
            return ("MET" if actual not in expected else "NOT_MET"), actual
        except TypeError:
            return "UNKNOWN", actual
    if operator in {"GT", "GTE", "LT", "LTE"}:
        try:
            comparisons = {
                "GT": actual > expected,
                "GTE": actual >= expected,
                "LT": actual < expected,
                "LTE": actual <= expected,
            }
            return ("MET" if comparisons[operator] else "NOT_MET"), actual
        except TypeError:
            return "UNKNOWN", actual
    if operator == "ANY_CONTRADICTION":
        values = actual if isinstance(actual, list) else []
        return ("MET" if bool(values) else "NOT_MET"), values
    if operator == "PREDICTION_RESULT_IS":
        return ("MET" if str(actual).upper() == str(expected).upper() else "NOT_MET"), actual
    return "UNKNOWN", actual


def evaluate_falsifiers(
    *,
    hypothesis_ref: str,
    falsifiers: Sequence[Mapping[str, Any]],
    context: Mapping[str, Any],
) -> EngineResult:
    if not hypothesis_ref:
        raise RuntimeContractError("Falsifier engine requires hypothesis_ref")
    results: list[dict[str, Any]] = []
    for index, falsifier in enumerate(falsifiers, start=1):
        condition = falsifier.get("condition") if isinstance(falsifier.get("condition"), Mapping) else falsifier
        scope = str(falsifier.get("scope", "HYPOTHESIS"))
        consequence = str(falsifier.get("consequence", "REJECT_HYPOTHESIS"))
        status, actual = _evaluate(condition, context)
        fid = str(falsifier.get("falsifier_id") or stable_id("FALS", hypothesis_ref, index, condition, scope))
        results.append({
            "falsifier_id": fid,
            "hypothesis_ref": hypothesis_ref,
            "scope": scope,
            "condition": dict(condition),
            "evaluation_status": status,
            "actual_value": actual,
            "consequence_if_met": consequence,
            "supporting_evidence_refs": list(falsifier.get("supporting_evidence_refs", [])),
            "notes": falsifier.get("notes"),
        })

    met = [r for r in results if r["evaluation_status"] == "MET"]
    unknown = [r for r in results if r["evaluation_status"] == "UNKNOWN"]
    rejection_met = [r for r in met if r["consequence_if_met"] in {"REJECT_HYPOTHESIS", "FALSIFY_HYPOTHESIS"}]
    if rejection_met:
        overall = "FALSIFIED"
    elif met:
        overall = "WEAKENED"
    elif unknown:
        overall = "OPEN"
    elif results:
        overall = "SURVIVED_CURRENT_FALSIFIERS"
    else:
        overall = "NO_FALSIFIER_DECLARED"

    trace = TraceStep.create(
        ENGINE_ID,
        "EVALUATE_DECLARED_FALSIFIERS",
        input_refs=[hypothesis_ref],
        output_refs=[r["falsifier_id"] for r in results],
        rule_refs=RULES,
        notes=[f"falsifier_count={len(results)}", f"met={len(met)}", f"unknown={len(unknown)}", f"overall={overall}"],
    )
    return EngineResult(
        ENGINE_ID,
        "COMPLETE",
        {
            "hypothesis_ref": hypothesis_ref,
            "falsifier_results": results,
            "overall_status": overall,
            "falsifier_count": len(results),
            "met_count": len(met),
            "unknown_count": len(unknown),
            "rejection_triggered": bool(rejection_met),
        },
        [trace],
    )
