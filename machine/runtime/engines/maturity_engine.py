#!/usr/bin/env python3
"""Evidence-driven maturity evaluator for Sourceborn hypotheses.

Maturity is not confidence prose and not a reward score.  It is a structural
classification of how well a candidate is connected to source, evidence,
independent corroboration, counter-cases, falsifiers and R-F-R.

M0 synthetic seed
M1 structurally grounded synthetic
M2 domain-plausible / source-linked hypothesis
M3 object/event-linked evidence hypothesis
M4 textually/operationally anchored and R-F-R-supported
M5 mature interpretation: M4 plus strong provenance, independent support,
   counter-case survival and low remaining proof debt.
"""
from __future__ import annotations

from typing import Any, Mapping, Sequence

from .runtime_core import EngineResult, RuntimeContractError, TraceStep, evidence_strength, stable_id

ENGINE_ID = "SB-RT-ENG-MATURITY-001"
RULES = [
    "MATURITY_NE_TRUTH_PROBABILITY",
    "M4_REQUIRES_ANCHORED_TESTING",
    "M5_REQUIRES_INDEPENDENT_SUPPORT_AND_COUNTERCASE_SURVIVAL",
    "FALSIFIED_CANDIDATE_CANNOT_MATURE",
]


def evaluate_maturity(
    hypothesis: Mapping[str, Any],
    *,
    rfr_assessment: Mapping[str, Any] | None = None,
    falsifier_assessment: Mapping[str, Any] | None = None,
    evidence_records: Sequence[Mapping[str, Any]] = (),
    provenance_complete: bool = False,
    counter_case_tested: bool = False,
    domain_anchor_present: bool = False,
    textual_or_operational_anchor_present: bool = False,
) -> EngineResult:
    hypothesis_ref = str(
        hypothesis.get("intent_id")
        or hypothesis.get("future_state_id")
        or hypothesis.get("combination_id")
        or hypothesis.get("output_id")
        or hypothesis.get("id")
        or ""
    )
    if not hypothesis_ref:
        raise RuntimeContractError("Maturity engine requires hypothesis identity")

    falsifier_status = str((falsifier_assessment or {}).get("overall_status", "NO_FALSIFIER_DECLARED"))
    rfr_status = str((rfr_assessment or {}).get("overall_status", "OPEN"))
    proof_debt = list(hypothesis.get("proof_debt", []))
    strength = evidence_strength(evidence_records)
    supporting_groups = {
        str(r.get("source_independence_group") or r.get("source_independence_group_ref"))
        for r in evidence_records
        if (r.get("source_independence_group") or r.get("source_independence_group_ref"))
        and str(r.get("result", r.get("status", ""))).upper() in {"PASS", "SUPPORTS", "SUPPORTED", "CONFIRMED"}
    }
    contradiction_count = sum(
        1 for r in evidence_records
        if str(r.get("result", r.get("status", ""))).upper() in {"FAIL", "CONTRADICTS", "FALSIFIED", "REFUTED"}
    )

    reasons: list[str] = []
    blockers: list[str] = []

    if falsifier_status == "FALSIFIED":
        maturity = "M0"
        blockers.append("DECLARED_FALSIFIER_MET")
    else:
        maturity = "M0"
        if hypothesis.get("source_refs") or hypothesis.get("point_zero_ref") or hypothesis.get("point_zero_refs"):
            maturity = "M1"
            reasons.append("SOURCE_OR_POINT_ZERO_TRACE_PRESENT")
        if domain_anchor_present and maturity in {"M0", "M1"}:
            maturity = "M2"
            reasons.append("DOMAIN_ANCHOR_PRESENT")
        if provenance_complete and strength >= 0.30 and contradiction_count == 0:
            maturity = "M3"
            reasons.append("PROVENANCE_AND_EVENT_LINKED_EVIDENCE")
        if textual_or_operational_anchor_present and provenance_complete and rfr_status == "PASS" and strength >= 0.45 and contradiction_count == 0:
            maturity = "M4"
            reasons.append("ANCHORED_RFR_SUPPORTED")
        if (
            maturity == "M4"
            and counter_case_tested
            and len(supporting_groups) >= 2
            and strength >= 0.62
            and not proof_debt
            and falsifier_status in {"SURVIVED_CURRENT_FALSIFIERS", "NO_FALSIFIER_DECLARED"}
        ):
            maturity = "M5"
            reasons.append("INDEPENDENT_SUPPORT_COUNTERCASE_AND_LOW_PROOF_DEBT")

    if contradiction_count:
        blockers.append("CONTRADICTING_EVIDENCE_PRESENT")
        if maturity in {"M4", "M5"}:
            maturity = "M3"
    if rfr_status in {"FAIL", "WEAKEN_OR_REJECT"}:
        blockers.append(f"RFR_{rfr_status}")
        if maturity in {"M3", "M4", "M5"}:
            maturity = "M2"
    if proof_debt and maturity == "M5":
        maturity = "M4"
        blockers.append("PROOF_DEBT_REMAINS")

    assessment_id = stable_id("MAT", hypothesis_ref, maturity, reasons, blockers, rfr_status, falsifier_status, round(strength, 6))
    payload = {
        "maturity_assessment_id": assessment_id,
        "hypothesis_ref": hypothesis_ref,
        "maturity": maturity,
        "maturity_is_truth_probability": False,
        "evidence_strength": round(strength, 6),
        "independent_support_group_count": len(supporting_groups),
        "contradiction_count": contradiction_count,
        "provenance_complete": provenance_complete,
        "domain_anchor_present": domain_anchor_present,
        "textual_or_operational_anchor_present": textual_or_operational_anchor_present,
        "counter_case_tested": counter_case_tested,
        "rfr_status": rfr_status,
        "falsifier_status": falsifier_status,
        "proof_debt": proof_debt,
        "maturity_reasons": reasons,
        "maturity_blockers": blockers,
        "eligible_for_canonical_promotion": maturity == "M5" and not blockers and not proof_debt,
        "direct_action_authority": False,
    }
    trace = TraceStep.create(
        ENGINE_ID,
        "EVALUATE_HYPOTHESIS_MATURITY",
        input_refs=[hypothesis_ref],
        output_refs=[assessment_id],
        rule_refs=RULES,
        notes=[f"maturity={maturity}", f"evidence_strength={strength:.3f}"],
    )
    return EngineResult(ENGINE_ID, "COMPLETE", payload, [trace])
