#!/usr/bin/env python3
from pathlib import Path
import json, sys

ROOT = Path(__file__).resolve().parents[1]
IN_DIR = ROOT / "phase2" / "splits" / "observations"
OUT = ROOT / "generated" / "parameter_candidates"
OUT.mkdir(parents=True, exist_ok=True)

BEHAVIOR_KEYS = [
    "different_trigger",
    "different_threshold",
    "different_dependency",
    "different_evidence_requirement",
    "different_controller_or_authority",
    "different_identity_rule",
    "different_transition_mechanism",
    "different_result_interpretation",
    "different_closure_rule",
    "different_memory_rule",
    "different_verification_rule",
    "different_risk_or_priority_treatment",
    "different_provenance_requirement",
    "different_contradiction_handling",
    "different_downstream_behavior"
]

def as_list(v):
    return v if isinstance(v, list) else []

observations = []
if IN_DIR.exists():
    for p in sorted(IN_DIR.glob("*.json")):
        data = json.loads(p.read_text(encoding="utf-8"))
        if isinstance(data, list):
            observations.extend((p, x) for x in data)
        else:
            observations.append((p, data))

candidates = []
rejections = []
errors = []

for path, obs in observations:
    oid = obs.get("observation_id")
    parent = obs.get("parent_parameter_id")
    label = obs.get("candidate_label")
    source_claims = as_list(obs.get("source_claim_ids"))
    diffs = obs.get("behavior_differences", {}) or {}
    if not oid or not parent or not label:
        errors.append({"file": str(path.relative_to(ROOT)), "observation_id": oid, "reason": "missing observation_id/parent_parameter_id/candidate_label"})
        continue
    unknown_keys = sorted(set(diffs) - set(BEHAVIOR_KEYS))
    if unknown_keys:
        errors.append({"observation_id": oid, "reason": f"unknown behavior difference keys: {unknown_keys}"})
        continue
    positive = [k for k in BEHAVIOR_KEYS if diffs.get(k) is True]
    if not positive:
        rejections.append({"observation_id": oid, "parent_parameter_id": parent, "candidate_label": label, "status": "REJECTED_NO_MACHINE_BEHAVIOR_DIFFERENCE", "behavior_vector": {k: diffs.get(k, "UNDECLARED") for k in BEHAVIOR_KEYS}})
        continue
    if not source_claims:
        rejections.append({"observation_id": oid, "parent_parameter_id": parent, "candidate_label": label, "status": "UNDER_REVIEW_SOURCE_GAP", "reason": "behavior difference exists but no source_claim_ids supplied", "positive_behavior_differences": positive})
        continue
    candidates.append({
        "sub_parameter_id": f"CAND-{parent}-{len(candidates)+1:04d}",
        "parent_parameter_id": parent,
        "candidate_label": label,
        "differentiating_rubric_ids": as_list(obs.get("differentiating_rubric_ids")),
        "differentiating_value_set": obs.get("differentiating_value_set"),
        "reason_for_split": "At least one source-supported distinction changes machine behavior.",
        "machine_behavior_difference": positive,
        "behavior_vector": {k: diffs.get(k, "UNDECLARED") for k in BEHAVIOR_KEYS},
        "source_claim_ids": source_claims,
        "evidence_ids": as_list(obs.get("evidence_ids")),
        "source_sequence_ids": as_list(obs.get("sequence_example_ids")),
        "recurrence_count": obs.get("recurrence_count", "UNKNOWN"),
        "redundancy_with_ids": as_list(obs.get("redundancy_with_ids")),
        "unsupported_complexity_notes": as_list(obs.get("unsupported_complexity_notes")),
        "scope": obs.get("scope"),
        "conditions": as_list(obs.get("conditions")),
        "exceptions": as_list(obs.get("exceptions")),
        "epistemic_status": obs.get("epistemic_status", "UNDECLARED"),
        "status": "CANDIDATE_SPLIT",
        "version": "v0",
        "score_components_only": {
            "positive_behavior_difference_count": len(positive),
            "recurrence": obs.get("recurrence_count", "UNKNOWN"),
            "redundancy_count": len(as_list(obs.get("redundancy_with_ids"))),
            "unsupported_complexity_count": len(as_list(obs.get("unsupported_complexity_notes")))
        },
        "numeric_score": "UNDECLARED_NO_WEIGHTS"
    })

result = {
    "status": "GENERATED_REVIEW_ONLY",
    "rule": "Candidate generation is not approval or canonicalization.",
    "observation_count": len(observations),
    "candidate_count": len(candidates),
    "non_candidate_count": len(rejections),
    "error_count": len(errors),
    "candidates": candidates,
    "non_candidates": rejections,
    "errors": errors
}
(OUT / "subparameter_candidates.json").write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
print(f"observations={len(observations)} candidates={len(candidates)} non_candidates={len(rejections)} errors={len(errors)}")
sys.exit(1 if errors else 0)
