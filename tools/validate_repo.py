#!/usr/bin/env python3
from pathlib import Path
import json, re, sys

ROOT = Path(__file__).resolve().parents[1]
errors = []
warnings = []

def load(path):
    p = ROOT / path
    if not p.exists():
        errors.append(f"Missing required file: {path}")
        return {}
    return json.loads(p.read_text(encoding="utf-8"))

canonical = load("CANONICALITY.json")
if canonical.get("phase2", {}).get("ai_capability_map_status") != "REVIEW_ONLY":
    errors.append("AI capability map must remain REVIEW_ONLY until user approval.")
if canonical.get("phase2", {}).get("status") != "ACTIVE":
    errors.append("Phase 2 is expected to be ACTIVE.")

for key in ["canonical_sequence_execution_manifest", "canonical_phase2_adoption_manifest"]:
    rel = canonical.get("phase1", {}).get(key)
    if not rel or not (ROOT / rel).exists():
        errors.append(f"Canonical manifest missing or invalid: {key}={rel}")

# Validate every ordered-parts manifest structurally.
for manifest_path in ROOT.rglob("*.manifest.json"):
    if "generated" in manifest_path.parts:
        continue
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    for rel in data.get("parts_in_order", []):
        p = manifest_path.parent / rel
        if not p.exists():
            errors.append(f"Manifest part missing: {p.relative_to(ROOT)}")

human = load("registries/human/HUMAN_REGISTRY_ADOPTION_CONTRACT.json")
if human.get("locked_shape") != {"segments": 10, "containers": 80, "active_parameters": 2560}:
    errors.append("Human native shape changed.")

vocab = load("machine/vocab/core_vocab.json")
for required in ["CLOSED_SUCCESS", "CLOSED_FAILURE", "CLOSED_NOT_APPLICABLE"]:
    if required not in vocab.get("terminal_sequence_statuses", []):
        errors.append(f"Missing terminal status: {required}")
if "META" not in vocab.get("controller_types", []):
    errors.append("META controller missing.")
if "WANT" not in vocab.get("driver_types", []):
    errors.append("WANT incorrectly removed from driver registry.")
if "ALWAYS" not in vocab.get("threshold_types", []):
    errors.append("Threshold vocabulary must include ALWAYS for edges with no special gate.")

asi = load("registries/asi/asi_node_registry.json")
asi_ids = [n.get("asi_node_id") for n in asi.get("nodes", [])]
if len(asi_ids) != 18 or len(set(asi_ids)) != 18:
    errors.append(f"ASI service registry must contain 18 unique nodes; found {len(asi_ids)} / {len(set(asi_ids))} unique.")

ai_path = ROOT / "raw/rubrics/AI_CAPABILITY_TO_SOURCEBORN_CONTAINERS_REVIEW.md"
if ai_path.exists():
    ids = re.findall(r"\bAI-CAP-\d{3}\b", ai_path.read_text(encoding="utf-8"))
    unique_ids = sorted(set(ids))
    if len(unique_ids) != 74:
        errors.append(f"AI review map expected 74 unique capability families; found {len(unique_ids)}.")
else:
    errors.append("AI capability review source missing.")

# Human native source is intentionally allowed to be absent, but must not be silently fabricated.
native_dir = ROOT / "registries/human/native"
if not native_dir.exists() or not any(p.is_file() for p in native_dir.rglob("*")):
    warnings.append("Approved Human 2,560-row native registry not present yet; full parameter relinking remains blocked by design.")

print("errors:", len(errors))
for e in errors:
    print("ERROR", e)
print("warnings:", len(warnings))
for w in warnings:
    print("WARN", w)
sys.exit(1 if errors else 0)
