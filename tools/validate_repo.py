#!/usr/bin/env python3
from pathlib import Path
import json, sys

ROOT = Path(__file__).resolve().parents[1]
errors = []
warnings = []

def load(path):
    return json.loads((ROOT / path).read_text(encoding="utf-8"))

canonical = load("CANONICALITY.json")
if canonical["phase2"]["ai_capability_map_status"] != "REVIEW_ONLY":
    errors.append("AI capability map must remain REVIEW_ONLY until user approval.")

human = load("registries/human/HUMAN_REGISTRY_ADOPTION_CONTRACT.json")
if human["locked_shape"] != {"segments": 10, "containers": 80, "active_parameters": 2560}:
    errors.append("Human native shape changed.")

vocab = load("machine/vocab/core_vocab.json")
for required in ["CLOSED_SUCCESS", "CLOSED_FAILURE", "CLOSED_NOT_APPLICABLE"]:
    if required not in vocab["terminal_sequence_statuses"]:
        errors.append(f"Missing terminal status: {required}")

if "META" not in vocab["controller_types"]:
    errors.append("META controller missing.")

if "WANT" not in vocab["driver_types"]:
    errors.append("WANT incorrectly removed from driver registry.")

print("errors:", len(errors))
for e in errors:
    print("ERROR", e)
print("warnings:", len(warnings))
for w in warnings:
    print("WARN", w)
sys.exit(1 if errors else 0)
