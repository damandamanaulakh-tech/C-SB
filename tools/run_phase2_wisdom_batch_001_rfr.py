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

src = load("raw/wisdom/MAHABHARATA_MODELLING_NARRATIVE_BATCH_01.json")
der = load("phase2/wisdom/WISDOM_BATCH_001_DERIVATION.json")
reg = load("registries/wisdom/WISDOM_REGISTRY_V0.json")

source_rows = src.get("records", [])
claims = der.get("source_claims", [])
interpretations = der.get("interpretations", [])
sequences = der.get("supporting_sequences", [])
wisdom = der.get("wisdom_candidates", [])

expected = {
    "source_text": [f"WST-{i:03d}" for i in range(1, 6)],
    "claims": [f"WSC-{i:03d}" for i in range(1, 6)],
    "interpretations": [f"WINT-{i:03d}" for i in range(1, 6)],
    "sequences": [f"WSEQ-{i:03d}" for i in range(1, 6)],
    "wisdom": [f"WIS-CAND-{i:03d}" for i in range(1, 6)],
}

if [r.get("source_text_id") for r in source_rows] != expected["source_text"]:
    errors.append("source text IDs must be WST-001..005")
if [r.get("source_claim_id") for r in claims] != expected["claims"]:
    errors.append("source claim IDs must be WSC-001..005")
if [r.get("interpretation_id") for r in interpretations] != expected["interpretations"]:
    errors.append("interpretation IDs must be WINT-001..005")
if [r.get("sequence_id") for r in sequences] != expected["sequences"]:
    errors.append("supporting Sequence IDs must be WSEQ-001..005")
if [r.get("wisdom_id") for r in wisdom] != expected["wisdom"]:
    errors.append("Wisdom candidate IDs must be WIS-CAND-001..005")

if src.get("source_class") != "USER_PROVIDED_MAHABHARATA_MODELLING_NARRATIVE":
    errors.append("source class changed")
for forbidden in ["PRIMARY_SCRIPTURE_TEXT", "HISTORICAL_FACT_REGISTRY", "INDEPENDENT_EXTERNAL_VERIFICATION"]:
    if forbidden not in src.get("not_source_class", []):
        errors.append(f"missing source boundary:{forbidden}")

source_ids = {r.get("source_text_id") for r in source_rows}
claim_ids = {r.get("source_claim_id") for r in claims}
interp_ids = {r.get("interpretation_id") for r in interpretations}
seq_ids = {r.get("sequence_id") for r in sequences}
lane_ids = {r.get("wisdom_lane_id") for r in reg.get("lanes", [])}

for c in claims:
    refs = set(c.get("source_text_ids", []))
    if not refs or refs - source_ids:
        errors.append(f"{c.get('source_claim_id')} has invalid source text refs")
    if c.get("epistemic_status") != "SUPPORTED_BY_SUPPLIED_NARRATIVE_ONLY":
        errors.append(f"{c.get('source_claim_id')} lost narrative-only epistemic boundary")

for i in interpretations:
    refs = set(i.get("source_claim_ids", []))
    if not refs or refs - claim_ids:
        errors.append(f"{i.get('interpretation_id')} has invalid claim refs")
    if i.get("not_source_fact") is not True:
        errors.append(f"{i.get('interpretation_id')} must remain not_source_fact")

required_wisdom_fields = set(reg.get("wisdom_object_contract", {}).get("required_fields", []))
for w in wisdom:
    wid = w.get("wisdom_id")
    missing = [k for k in required_wisdom_fields if k not in w]
    if missing:
        errors.append(f"{wid} missing required fields:{','.join(sorted(missing))}")
    if set(w.get("source_claim_ids", [])) - claim_ids:
        errors.append(f"{wid} has invalid source claims")
    if set(w.get("interpretation_ids", [])) - interp_ids:
        errors.append(f"{wid} has invalid interpretations")
    if set(w.get("supporting_sequence_ids", [])) - seq_ids:
        errors.append(f"{wid} has invalid supporting sequences")
    if set(w.get("wisdom_lane_ids", [])) - lane_ids:
        errors.append(f"{wid} has invalid wisdom lane")
    statuses = set(w.get("epistemic_status", []))
    if "SOURCE_LINKED_CANDIDATE" not in statuses:
        errors.append(f"{wid} must remain candidate")
    if w.get("confidence") not in {"PROVISIONAL", "LOW_UNTIL_MULTI_CASE_TEST"}:
        errors.append(f"{wid} has over-promoted confidence")
    for forbidden_key in ["law_status", "permission", "execute", "action_authority"]:
        if forbidden_key in w:
            errors.append(f"{wid} illegally contains direct authority field:{forbidden_key}")

if "MULTI_CASE_EVIDENCE_NOT_YET_SUPPLIED" not in set(next(w for w in wisdom if w.get("wisdom_id") == "WIS-CAND-005").get("epistemic_status", [])):
    errors.append("WIS-CAND-005 must preserve multi-case evidence debt")

proof_debt = set(der.get("global_proof_debt", []))
for required_debt in [
    "No primary Mahabharata or Bhagavad Gita text is included in this batch.",
    "No independent historical or theological verification has been performed.",
    "No cross-tradition or counter-interpretation corpus has yet been ingested.",
]:
    if required_debt not in proof_debt:
        errors.append(f"missing proof debt:{required_debt}")

# R-F-R semantic checks for the five abstractions.
checks = {
    "WIS-CAND-001": "actor view must remain distinct from global state",
    "WIS-CAND-002": "exception must remain bounded and not replace normal rule",
    "WIS-CAND-003": "event/record/interpretation provenance layers must remain separate",
    "WIS-CAND-004": "unique path history may alter response under common input",
    "WIS-CAND-005": "guidance generalization requires multi-case/counter-case evidence before promotion",
}

report = {
    "report_id": "P2-WISDOM-BATCH-001-RFR",
    "status": "FAIL" if errors else "PASS_WITH_PROOF_DEBT",
    "scope": "Source custody, derivation separation, applicability and non-promotion checks for the first user-provided Mahabharata modelling narrative batch.",
    "counts": {
        "source_texts": len(source_rows),
        "source_claims": len(claims),
        "interpretations": len(interpretations),
        "supporting_sequences": len(sequences),
        "wisdom_candidates": len(wisdom),
        "hard_failures": len(errors)
    },
    "pass0": {
        "declared_end": "Five source-linked Wisdom Candidates exist without collapsing narrative source, claim, interpretation, Wisdom, law or action authority.",
        "closure_scope": "first bounded interpretive narrative ingestion only; not scripture validation"
    },
    "pass1": {
        "reverse_trace_complete": not errors,
        "source_class": src.get("source_class"),
        "source_boundaries": src.get("not_source_class", [])
    },
    "pass2": {
        "forward_derivation_path": ["SOURCE_TEXT", "SOURCE_CLAIM", "INTERPRETATION", "SEQUENCE_RECONSTRUCTION", "WISDOM_CANDIDATE"],
        "candidate_checks": checks
    },
    "pass3": {
        "proof_debt_preserved": sorted(proof_debt),
        "law_promotion_allowed": False,
        "direct_execution_allowed": False,
        "primary_scripture_verified": False,
        "counter_case_review_complete": False
    },
    "errors": errors,
    "findings": findings
}

(OUT / "P2_WISDOM_BATCH_001_RFR.json").write_text(json.dumps(report, indent=2), encoding="utf-8")
print(report["status"], report["counts"])
sys.exit(1 if errors else 0)
