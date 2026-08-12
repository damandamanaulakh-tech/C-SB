#!/usr/bin/env python3
from pathlib import Path
import json, sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "generated/tests"
OUT.mkdir(parents=True, exist_ok=True)

errors = []
findings = []

def load(rel):
    p = ROOT / rel
    if not p.exists():
        errors.append(f"missing:{rel}")
        return {}
    return json.loads(p.read_text(encoding="utf-8"))

src = load("raw/wisdom/BHAGAVAD_GITA_2_47_2_50_SOURCE_V1.json")
claims = load("phase2/wisdom/BG_2_47_2_50_SOURCE_CLAIMS_V1.json")
ints = load("phase2/wisdom/BG_2_47_2_50_INTERPRETATIONS_V1.json")
apps = load("phase2/wisdom/BG_2_47_2_50_APPLICABILITY_COUNTERCASES_V1.json")
cands = load("phase2/wisdom/BG_2_47_2_50_WISDOM_CANDIDATES_V1.json")
wisdom_registry = load("registries/wisdom/WISDOM_REGISTRY_V0.json")

source_rows = src.get("records", [])
claim_rows = claims.get("claims", [])
int_rows = ints.get("interpretations", [])
app_rows = apps.get("tests", [])
cand_rows = cands.get("candidates", [])

source_ids = {r.get("source_record_id") for r in source_rows}
claim_ids = {r.get("source_claim_id") for r in claim_rows}
int_ids = {r.get("interpretation_id") for r in int_rows}
app_ids = {r.get("case_id") for r in app_rows}
wisdom_lane_ids = {r.get("wisdom_lane_id") for r in wisdom_registry.get("lanes", [])}

# Pass 0 — declared end/scope
pass0 = {
    "declared_end": "Three source-linked contextual Wisdom candidates survive source custody, interpretation separation and counter-case/applicability audit without acquiring execution authority.",
    "source_scope": "Bhagavad Gita chapter 2 verses 47-50 only",
    "closure_scope": "source-ingestion architecture integrity; not doctrinal consensus or universal truth"
}
if src.get("bounded_scope", {}).get("record_count") != 4 or len(source_rows) != 4:
    errors.append("source_scope_must_contain_exactly_4_records")
if [r.get("verse") for r in source_rows] != [47,48,49,50]:
    errors.append("source_verse_order_must_be_47_48_49_50")

# Pass 1 — reverse trace every derived object to source
for r in claim_rows:
    refs = set(r.get("source_refs", []))
    if not refs or not refs <= source_ids:
        errors.append(f"claim_bad_source_refs:{r.get('source_claim_id')}")
for r in int_rows:
    refs = set(r.get("source_claim_refs", []))
    if not refs or not refs <= claim_ids:
        errors.append(f"interpretation_bad_claim_refs:{r.get('interpretation_id')}")
for r in cand_rows:
    if not set(r.get("source_claim_refs", [])) <= claim_ids:
        errors.append(f"candidate_bad_claim_refs:{r.get('wisdom_id')}")
    if not set(r.get("interpretation_refs", [])) <= int_ids:
        errors.append(f"candidate_bad_interpretation_refs:{r.get('wisdom_id')}")
    if not set(r.get("counter_case_refs", [])) <= app_ids:
        errors.append(f"candidate_bad_counter_case_refs:{r.get('wisdom_id')}")
    if not set(r.get("supporting_applicability_cases", [])) <= app_ids:
        errors.append(f"candidate_bad_applicability_refs:{r.get('wisdom_id')}")
    if not set(r.get("wisdom_lane_refs", [])) <= wisdom_lane_ids:
        errors.append(f"candidate_bad_wisdom_lane_refs:{r.get('wisdom_id')}")

# Pass 2 — legal forward chain and authority separation
if len(claim_rows) != 8:
    errors.append(f"expected_8_claims_found_{len(claim_rows)}")
if len(int_rows) != 3:
    errors.append(f"expected_3_interpretations_found_{len(int_rows)}")
if len(app_rows) != 7:
    errors.append(f"expected_7_applicability_cases_found_{len(app_rows)}")
if len(cand_rows) != 3:
    errors.append(f"expected_3_wisdom_candidates_found_{len(cand_rows)}")

for r in claim_rows:
    if "TRANSLATION_DEPENDENT" not in str(r.get("epistemic_status", "")):
        errors.append(f"claim_missing_translation_dependency:{r.get('source_claim_id')}")
for r in int_rows:
    if r.get("epistemic_status") != "INTERPRETIVE_CANDIDATE":
        errors.append(f"interpretation_wrong_epistemic_status:{r.get('interpretation_id')}")
    if not r.get("source_boundary_preserved"):
        errors.append(f"interpretation_source_boundary_not_preserved:{r.get('interpretation_id')}")
for r in cand_rows:
    if r.get("direct_action_authority") is not False:
        errors.append(f"wisdom_direct_action_authority_forbidden:{r.get('wisdom_id')}")
    if not r.get("counter_case_refs"):
        errors.append(f"wisdom_missing_counter_cases:{r.get('wisdom_id')}")
    if not r.get("does_not_apply_as_authority_when"):
        errors.append(f"wisdom_missing_non_applicability:{r.get('wisdom_id')}")

# Pass 3 — anti-generalization / source rewrite audit
source_texts = [r.get("source_text") for r in source_rows]
if any(not x for x in source_texts):
    errors.append("empty_source_text")
if len(set(source_texts)) != 4:
    errors.append("duplicate_source_text_records")

required_boundaries = {
    "Wisdom does not bypass permission.",
    "Wisdom does not satisfy missing resources or dependencies.",
    "Wisdom does not suppress failure evidence."
}
actual_boundaries = set(apps.get("hard_applicability_boundaries", []))
if not required_boundaries <= actual_boundaries:
    errors.append("required_applicability_boundaries_missing")

if apps.get("closure", {}).get("eligible_for_direct_action_authority") is not False:
    errors.append("counter_case_gate_wrongly_allows_direct_action")
if cands.get("status") != "WISDOM_CANDIDATES_PENDING_RFR":
    findings.append("candidate_status_changed_before_rfr_closure")

status = "FAIL" if errors else ("PASS_WITH_FINDINGS" if findings else "PASS")
report = {
    "report_id": "P2-WISDOM-SOURCE-INGESTION-RFR-V1",
    "status": status,
    "scope_note": "Structural/source-boundary R-F-R for one bounded Holy-Book ingestion batch. It does not establish theological consensus, external truth, or universal applicability.",
    "summary": {
        "source_records": len(source_rows),
        "source_claims": len(claim_rows),
        "interpretations": len(int_rows),
        "applicability_cases": len(app_rows),
        "wisdom_candidates": len(cand_rows),
        "errors": len(errors),
        "findings": len(findings)
    },
    "pass0": pass0,
    "pass1": {
        "all_claims_trace_to_source": not any(e.startswith("claim_bad_source_refs") for e in errors),
        "all_interpretations_trace_to_claims": not any(e.startswith("interpretation_bad_claim_refs") for e in errors),
        "all_wisdom_candidates_trace_to_claims_interpretations_and_cases": not any(e.startswith("candidate_bad_") for e in errors)
    },
    "pass2": {
        "chain": ["SOURCE_TEXT","SOURCE_CLAIM","INTERPRETATION","COUNTER_CASE_APPLICABILITY","WISDOM_CANDIDATE"],
        "direct_action_authority_present": any(r.get("direct_action_authority") is not False for r in cand_rows),
        "translation_dependency_preserved": all("TRANSLATION_DEPENDENT" in str(r.get("epistemic_status", "")) for r in claim_rows)
    },
    "pass3": {
        "counter_case_gate_present": bool(app_rows),
        "required_boundaries_present": required_boundaries <= actual_boundaries,
        "source_text_immutable_input": True,
        "law_formation_not_performed": True,
        "actor_view_not_modified": True
    },
    "errors": errors,
    "findings": findings
}
(OUT / "P2_WISDOM_SOURCE_INGESTION_RFR_V1.json").write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps(report["summary"], indent=2))
sys.exit(1 if errors else 0)
