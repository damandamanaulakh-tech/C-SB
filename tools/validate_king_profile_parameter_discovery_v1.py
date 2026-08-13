#!/usr/bin/env python3
from pathlib import Path
from difflib import SequenceMatcher
import json, re, sys

ROOT = Path(__file__).resolve().parents[1]
REVIEW = ROOT / "phase2/source_reviews/KING_PROFILE_PARAMETER_DISCOVERY_V1.json"
HUMAN = ROOT / "registries/human/HUMAN_KING_PROFILE_PARAMETER_CANDIDATES_V0.json"
REASON = ROOT / "registries/sourceborn/KING_PROFILE_REASONING_PARAMETER_CANDIDATES_V0.json"
DOMAIN = ROOT / "registries/domain/egypt/KING_PROFILE_ARTIFACT_PARAMETER_CANDIDATES_V0.json"
HFR = ROOT / "generated/registry_views/human_functional_3204_registry_v1.json"
CONTAINERS = ROOT / "registries/human/HUMAN_CONTAINER_INDEX_80_APPROVED_V1.json"
OUT = ROOT / "generated/tests/P2_KING_PROFILE_PARAMETER_DISCOVERY_RFR_V1.json"
OUT.parent.mkdir(parents=True, exist_ok=True)

errors = []
findings = []

def load(path):
    if not path.exists():
        errors.append(f"missing required file: {path.relative_to(ROOT)}")
        return {}
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception as exc:
        errors.append(f"invalid json {path.relative_to(ROOT)}: {exc}")
        return {}

def norm(s):
    return " ".join(re.findall(r"[a-z0-9]+", str(s).lower()))

review = load(REVIEW)
human = load(HUMAN)
reason = load(REASON)
domain = load(DOMAIN)
hfr = load(HFR)
container_index = load(CONTAINERS)

human_candidates = human.get("candidates", [])
reason_candidates = reason.get("candidates", [])
domain_candidates = domain.get("candidates", [])

if review.get("observed_profile_count") != 18:
    errors.append("review must record exactly 18 observed King profiles")
expected_counts = review.get("candidate_counts", {})
actual_counts = {
    "human_functional": len(human_candidates),
    "asi_reasoning": len(reason_candidates),
    "domain_egypt": len(domain_candidates),
    "total": len(human_candidates) + len(reason_candidates) + len(domain_candidates),
}
if expected_counts != actual_counts:
    errors.append(f"candidate count mismatch expected={expected_counts} actual={actual_counts}")

seps = set(review.get("correction_to_prior_review", {}).get("new_separations", []))
required_seps = {
    "INSTANTIATED_EVALUATION_ADDRESS != NEW_PARAMETER_CANDIDATE",
    "NEW_PARAMETER_CANDIDATE != APPROVED_PARAMETER",
    "PROFILE_LABEL != PARAMETER",
    "COMBINATION_OF_EXISTING_PARAMETERS != NEW_ATOMIC_PARAMETER",
}
if not required_seps.issubset(seps):
    errors.append("prior-review correction separations incomplete")

if human.get("baseline_count_changes_now") is not False:
    errors.append("candidate discovery must not change the active Human baseline count")

all_ids = []
for group, prefix, candidates in [
    ("HUMAN", "HFP-KP-", human_candidates),
    ("REASON", "RC-KP-", reason_candidates),
    ("DOMAIN", "EG-KP-", domain_candidates),
]:
    for c in candidates:
        cid = c.get("candidate_id", "")
        all_ids.append(cid)
        if not cid.startswith(prefix):
            errors.append(f"{group} bad candidate id: {cid}")
        if not c.get("name") or not c.get("definition"):
            errors.append(f"{cid} missing name/definition")
if len(all_ids) != len(set(all_ids)):
    errors.append("candidate IDs are not unique")

common_h = human.get("common_candidate_state", {})
common_r = reason.get("common_candidate_state", {})
common_d = domain.get("common_candidate_state", {})
for label, state in [("HUMAN",common_h),("REASON",common_r),("DOMAIN",common_d)]:
    if state.get("status") != "REVIEW_REQUIRED" or state.get("canonical") is not False or state.get("direct_action_authority") is not False:
        errors.append(f"{label} common candidate state violates review-only/no-authority law")

known_containers = set()
for seg in container_index.get("segments", []):
    for row in seg.get("containers", []):
        if row:
            known_containers.add(row[0])
for c in human_candidates:
    cid = c.get("candidate_id", "")
    for key in ["activation_condition","measurable_dimensions","negative_boundary","falsifier","source_signals"]:
        if not c.get(key):
            errors.append(f"{cid} missing {key}")
    for con in c.get("nearest_existing_containers", []):
        if con not in known_containers:
            errors.append(f"{cid} unknown nearest container {con}")

params = hfr.get("parameters", [])
if len(params) != 3204:
    errors.append(f"materialized Human registry must contain 3204 parameters, found {len(params)}")

existing = [(p.get("parameter_id"), p.get("name", ""), norm(p.get("name", ""))) for p in params]
existing_norm = {}
for pid, name, n in existing:
    existing_norm.setdefault(n, []).append((pid, name))

probe = []
exact_collisions = 0
possible_overlap_count = 0
for c in human_candidates:
    cn = norm(c.get("name", ""))
    exact = existing_norm.get(cn, [])
    if exact:
        exact_collisions += 1
    scored = []
    for pid, name, en in existing:
        score = SequenceMatcher(None, cn, en).ratio() if cn and en else 0.0
        scored.append((score, pid, name))
    scored.sort(reverse=True)
    top = scored[:5]
    max_score = top[0][0] if top else 0.0
    possible = max_score >= 0.82 and not exact
    if possible:
        possible_overlap_count += 1
    probe.append({
        "candidate_id": c.get("candidate_id"),
        "candidate_name": c.get("name"),
        "exact_name_collision": bool(exact),
        "exact_matches": [{"parameter_id": pid, "name": name} for pid, name in exact],
        "nearest_by_name": [{"parameter_id": pid, "name": name, "similarity": round(score, 4)} for score, pid, name in top],
        "novelty_probe_status": "EXACT_NAME_COLLISION" if exact else ("POSSIBLE_SEMANTIC_OVERLAP_REVIEW_REQUIRED" if possible else "NO_EXACT_NAME_COLLISION_SEMANTIC_REVIEW_REQUIRED")
    })

if exact_collisions:
    errors.append(f"{exact_collisions} Human candidates exactly duplicate current 3204 parameter names")
if possible_overlap_count:
    findings.append(f"{possible_overlap_count} Human candidates have high name similarity (>=0.82) to an existing parameter and require semantic overlap review")

# Domain separation is mandatory: archaeology-specific parameters cannot silently enter Human source bank.
if "do not enter the Human 3204 bank" not in domain.get("scope", ""):
    errors.append("domain registry missing explicit Human-bank separation")

report = {
    "test_id": "P2-KING-PROFILE-PARAMETER-DISCOVERY-RFR-V1",
    "status": "PASS" if not errors else "FAIL",
    "errors": errors,
    "findings": findings,
    "checks": {
        "profile_count": review.get("observed_profile_count"),
        "candidate_counts": actual_counts,
        "human_baseline_count": len(params),
        "human_exact_name_collisions": exact_collisions,
        "human_possible_name_overlaps": possible_overlap_count,
        "registry_separation_enforced": True,
        "candidate_creation_changes_active_3204": False,
        "prior_review_corrected_without_erasing_structural_findings": True,
        "new_parameter_requires_review": True
    },
    "human_3204_novelty_probe": probe,
    "note": "This automated probe detects exact-name collisions and name-neighborhood similarity only. Semantic novelty remains a review/R-F-R question; PASS does not adopt any candidate."
}
OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps({"status": report["status"], "checks": report["checks"], "errors": errors, "findings": findings}, indent=2))
if errors:
    sys.exit(1)
