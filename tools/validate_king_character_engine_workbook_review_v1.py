#!/usr/bin/env python3
from pathlib import Path
import json, sys

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "phase2/source_reviews/KING_CHARACTER_ENGINE_WORKBOOK_REVIEW_V1.json"
CANDIDATES = ROOT / "registries/sourceborn/DOMAIN_PACK_REASONING_CANDIDATES_V0.json"
OUT = ROOT / "generated/tests/P2_KING_CHARACTER_ENGINE_WORKBOOK_REVIEW_RFR_V1.json"

def load(p):
    return json.loads(p.read_text(encoding="utf-8"))

errors=[]
findings=[]

if not REVIEW.exists():
    errors.append("missing workbook review fixture")
if not CANDIDATES.exists():
    errors.append("missing domain-pack candidate registry")

if not errors:
    r=load(REVIEW)
    c=load(CANDIDATES)

    shape=r["shape"]
    checks = {
        "sheets": shape["sheets"] == 16,
        "segments": shape["segments"] == 10,
        "containers": shape["containers"] == 80,
        "instantiated_rows": shape["instantiated_parameter_rows"] == 2000,
        "unique_dimensions": shape["unique_interrogation_dimensions"] == 25,
        "factorization_exact": shape["containers"] * shape["unique_interrogation_dimensions"] == shape["instantiated_parameter_rows"],
        "loops": shape["ard_loops"] == 5,
        "nodes_total": shape["ard_loops"] * shape["nodes_per_loop"] == shape["ard_nodes_total"] == 60,
        "reverse_forward": shape["reverse_steps"] + shape["forward_steps"] == shape["reverse_forward_steps"] == 100,
        "characters": shape["character_families"] * shape["characters_per_family"] == shape["character_hypotheses"] == 100,
        "source_not_merged_to_3204": "Do not add 2000" in r["adoption_guards"][0],
        "candidate_count": len(c["candidates"]) == 4,
        "all_review_required": all(x["status"] == "REVIEW_REQUIRED" and x["canonical"] is False and x["direct_action_authority"] is False for x in c["candidates"]),
    }
    for k,v in checks.items():
        if not v:
            errors.append(f"failed check: {k}")

    f={x["finding_id"]:x for x in r["rfr_findings"]}
    expected={"KC-RFR-001","KC-RFR-002","KC-RFR-003","KC-RFR-004","KC-RFR-005","KC-RFR-006","KC-RFR-007"}
    if set(f) != expected:
        errors.append("R-F-R finding set mismatch")

    off=f.get("KC-RFR-002",{})
    if off.get("excluded_parameter_ids") != ["P1999","P2000"]:
        errors.append("off-by-two excluded parameter IDs not preserved")

    detail=f.get("KC-RFR-005",{}).get("detail","").lower()
    if "same 10-step reverse" not in detail or "same 10-step forward" not in detail:
        errors.append("loop route duplication finding missing")

    ids={x["candidate_id"] for x in c["candidates"]}
    expected_ids={
        "RC-DOMAIN-RUBRIC-INSTANTIATION-001",
        "RC-NO-EVIDENCE-NO-RANK-001",
        "RC-SCORE-CONFIDENCE-SEPARATION-001",
        "RC-INDEPENDENT-LOOP-001",
    }
    if ids != expected_ids:
        errors.append("candidate ID set mismatch")

    findings.append("Workbook declares 2,000 parameter rows, but review classifies them as 80×25 instantiated domain-rubric addresses; no 3,204 count change.")
    findings.append("Source formula defect preserved: P1999/P2000 excluded from PYRAMID_INDEX scoring.")
    findings.append("No-evidence ranking, score/confidence conflation, loop-route duplication, manual loop-score linkage, and weight-provenance gaps remain review findings.")

report={
    "report_id":"P2-KING-CHARACTER-ENGINE-WORKBOOK-REVIEW-RFR-V1",
    "status":"PASS" if not errors else "FAIL",
    "checks":{
        "source_sha256":"cb4f21211ec85762fe79e77f31637dbfaf27de3f178240a17b266f46d0ae43b5",
        "instantiated_rows":2000,
        "unique_interrogation_dimensions":25,
        "domain_containers":80,
        "candidate_count":4,
        "canonical_additions":0,
        "human_3204_count_effect":0
    },
    "errors":errors,
    "findings":findings
}
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(report,indent=2)+"\n",encoding="utf-8")
print(json.dumps(report,indent=2))
sys.exit(1 if errors else 0)
