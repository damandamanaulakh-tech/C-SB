#!/usr/bin/env python3
from pathlib import Path
import json, re, sys

ROOT = Path(__file__).resolve().parents[1]
errors = []


def load(rel):
    p = ROOT / rel
    if not p.exists():
        errors.append(f"Missing required file: {rel}")
        return {}
    return json.loads(p.read_text(encoding="utf-8"))

ai = load("registries/ai/AI_CONTAINER_CANDIDATES_V0.json")
asi = load("registries/asi/ASI_CONTAINER_CANDIDATES_FROM_AI_SOURCES_V0.json")
extraction = load("phase2/extractions/AI_ASI_CONTAINER_EXTRACTION_FROM_AI_SOURCES_V0.json")

ai_rows = ai.get("containers", [])
asi_rows = asi.get("containers", [])

expected_ai_ids = [f"AI-CON-CAND-{i:03d}" for i in range(1, 41)]
expected_asi_ids = [f"ASI-CON-CAND-{i:03d}" for i in range(1, 21)]
actual_ai_ids = [r.get("container_id") for r in ai_rows]
actual_asi_ids = [r.get("container_id") for r in asi_rows]

if ai.get("container_count") != 40 or actual_ai_ids != expected_ai_ids:
    errors.append("AI container candidates must be exactly AI-CON-CAND-001..040 in order for V0.")
if asi.get("container_count") != 20 or actual_asi_ids != expected_asi_ids:
    errors.append("ASI container candidates must be exactly ASI-CON-CAND-001..020 in order for V0.")

valid_ai_segments = {f"AI-{i:02d}" for i in range(1, 26)}
valid_asi_segments = {f"ASI-{i:02d}" for i in range(1, 21)}
cap_rx = re.compile(r"^AI-CAP-\d{3}$")
cand_rx = re.compile(r"^AI-CAND-\d{3}[A-Z]$")

covered_caps = set()

for row in ai_rows:
    bad = set(row.get("parent_ai_segments", [])) - valid_ai_segments
    if bad:
        errors.append(f"{row.get('container_id')} references unknown AI segments: {sorted(bad)}")
    if not row.get("source_ids"):
        errors.append(f"{row.get('container_id')} has no source_ids")
    for sid in row.get("source_ids", []):
        if not (cap_rx.match(sid) or cand_rx.match(sid)):
            errors.append(f"{row.get('container_id')} has malformed source id {sid}")
        if cap_rx.match(sid):
            covered_caps.add(sid)
    for sid in row.get("source_parent_ids", []):
        if not cap_rx.match(sid):
            errors.append(f"{row.get('container_id')} has malformed source_parent_id {sid}")
        else:
            covered_caps.add(sid)

for row in asi_rows:
    bad = set(row.get("parent_asi_segments", [])) - valid_asi_segments
    if bad:
        errors.append(f"{row.get('container_id')} references unknown ASI segments: {sorted(bad)}")
    if not row.get("source_ids"):
        errors.append(f"{row.get('container_id')} has no source_ids")
    for sid in row.get("source_ids", []):
        if not (cap_rx.match(sid) or cand_rx.match(sid)):
            errors.append(f"{row.get('container_id')} has malformed source id {sid}")
        if cap_rx.match(sid):
            covered_caps.add(sid)
    for sid in row.get("source_parent_ids", []):
        if not cap_rx.match(sid):
            errors.append(f"{row.get('container_id')} has malformed source_parent_id {sid}")
        else:
            covered_caps.add(sid)

expected_caps = {f"AI-CAP-{i:03d}" for i in range(1, 75)}
if covered_caps != expected_caps:
    errors.append(
        "Combined AI+ASI candidate containers must preserve source coverage AI-CAP-001..074. "
        f"Missing={sorted(expected_caps-covered_caps)} Extra={sorted(covered_caps-expected_caps)}"
    )

# Composite source families must not be smuggled into AI-native atomic containers.
for forbidden in ["AI-CAP-001", "AI-CAP-071", "AI-CAP-072"]:
    for row in ai_rows:
        if forbidden in row.get("source_ids", []) or forbidden in row.get("source_parent_ids", []):
            errors.append(f"Composite {forbidden} must not become an AI-native atomic container ({row.get('container_id')}).")

# Known source holds must remain explicit at container layer.
if next((r for r in ai_rows if r.get("container_id") == "AI-CON-CAND-012"), {}).get("status") != "HOLD_SPLIT_REQUIRED":
    errors.append("AI-CAP-013 context/retrieval hold was lost at AI-CON-CAND-012.")
if next((r for r in ai_rows if r.get("container_id") == "AI-CON-CAND-036"), {}).get("status") != "HOLD_UNTIL_DURABLE_STORE_AND_UPDATE_MECHANISM_DEFINED":
    errors.append("AI-CAP-046 continual-learning hold was lost at AI-CON-CAND-036.")

if extraction.get("source_family_count") != 74 or extraction.get("source_layer_count") != 17:
    errors.append("Source extraction must preserve 74 source families and 17 source layers.")

print("errors:", len(errors))
for e in errors:
    print("ERROR", e)
sys.exit(1 if errors else 0)
