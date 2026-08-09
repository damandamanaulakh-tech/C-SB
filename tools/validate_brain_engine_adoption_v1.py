#!/usr/bin/env python3
from pathlib import Path
import json, sys

ROOT = Path(__file__).resolve().parents[1]
errors = []

def load(rel):
    p = ROOT / rel
    if not p.exists():
        errors.append(f"Missing {rel}")
        return {}
    return json.loads(p.read_text(encoding="utf-8"))

adopt = load("phase2/sources/BRAIN_ENGINE_LIBRARY_ADOPTION_V1.json")
ai64 = load("registries/ai/AI_ONLY_RECORDS_64_APPROVED_V1.json")
eng = load("registries/asi/ENGINE_LIBRARY_75_APPROVED_V1.json")
containers = load("registries/asi/OPERATIONAL_CONTAINERS_161_240_APPROVED_V1.json")
spine = load("machine/wiring/BRAIN_ENGINE_OPERATIONAL_SPINE_V1.json")
generated = load("generated/registry_views/operational_subparameters_2593_3072_v1.json")

if adopt.get("primary_operational_artifact", {}).get("declared_architecture", {}).get("master_containers") != 240:
    errors.append("Primary corpus must declare 240 master containers.")
if adopt.get("primary_operational_artifact", {}).get("declared_architecture", {}).get("operational_parameters") != 3072:
    errors.append("Primary corpus must declare 3072 operational parameters.")
if adopt.get("primary_operational_artifact", {}).get("declared_architecture", {}).get("canonical_engines") != 75:
    errors.append("Primary corpus must declare 75 canonical engines.")

ai_rows = ai64.get("records", [])
ai_ids = [r[0] for r in ai_rows]
expected_ai = [f"AI-NEW-{i:03d}" for i in range(1, 65)]
if ai_ids != expected_ai:
    errors.append("AI-only registry must contain AI-NEW-001..AI-NEW-064 exactly in order.")

eng_rows = eng.get("records", [])
eng_ids = [r[0] for r in eng_rows]
if len(eng_ids) != 75 or len(set(eng_ids)) != 75:
    errors.append(f"Engine registry must contain 75 unique engines; found {len(eng_ids)} / {len(set(eng_ids))} unique.")

crows = containers.get("records", [])
cids = [r[0] for r in crows]
expected_cids = [f"CON-{i:03d}" for i in range(161, 241)]
if cids != expected_cids:
    errors.append("Operational container registry must contain CON-161..CON-240 exactly in order.")
if any(r[2] not in {f"E0{i}" for i in range(1,9)} for r in crows):
    errors.append("Operational containers must use only E01..E08.")

els = spine.get("elements", [])
if len(els) != 8:
    errors.append("Operational spine must contain exactly 8 elements.")
covered = []
for e in els:
    covered.extend(e.get("container_ids", []))
if len(covered) != 80 or set(covered) != set(expected_cids):
    errors.append("Operational spine must cover CON-161..CON-240 exactly once.")

prows = generated.get("records", [])
pids = [r.get("parameter_id") for r in prows]
expected_pids = [f"SB-ASI-P{i:04d}" for i in range(2593, 3073)]
if pids != expected_pids:
    errors.append("Generated operational sub-parameters must contain SB-ASI-P2593..SB-ASI-P3072 exactly in order.")
for r in prows:
    cnum = int(r["container_id"].split("-")[-1])
    expected_start = 2593 + (cnum - 161) * 6
    expected_pid = f"SB-ASI-P{expected_start + int(r['local_number']) - 1:04d}"
    if r["parameter_id"] != expected_pid:
        errors.append(f"Parameter/container formula mismatch: {r['parameter_id']} -> {r['container_id']} local {r['local_number']}")
        break

print("errors:", len(errors))
for e in errors:
    print("ERROR", e)
sys.exit(1 if errors else 0)
