#!/usr/bin/env python3
from pathlib import Path
import json, sys

ROOT = Path(__file__).resolve().parents[1]
errors=[]

def load(rel):
    p=ROOT/rel
    if not p.exists():
        errors.append(f"missing:{rel}")
        return {}
    return json.loads(p.read_text(encoding="utf-8"))

src=load("registries/sourceborn/EXPANSION_PARAMETERS_2561_2592_APPROVED_V1.json")
bind=load("machine/parameters/EXPANSION_2561_2592_DOMAIN_BINDINGS_V1.json")

srows=src.get("records",[])
brows=bind.get("records",[])
expected=[f"SB-ASI-P{i:04d}" for i in range(2561,2593)]
if [r[0] for r in srows] != expected:
    errors.append("source registry must contain P2561..P2592 exactly in order")
if [r.get("parameter_id") for r in brows] != expected:
    errors.append("domain binding must cover P2561..P2592 exactly in order")
if len({r.get("parameter_id") for r in brows}) != 32:
    errors.append("domain binding IDs must be unique")

source_ids={r[0] for r in srows}
for r in brows:
    if r.get("parameter_id") not in source_ids:
        errors.append(f"binding references non-source parameter:{r.get('parameter_id')}")
    if not r.get("primary_domain_role"):
        errors.append(f"missing primary domain role:{r.get('parameter_id')}")
    if r.get("human_owner") and not (r.get("human_owner").startswith("CON-") or r.get("human_owner") == "SOCIAL_COLLECTIVE_STATE"):
        errors.append(f"invalid Human owner:{r.get('parameter_id')}")

# Exact Human ownership boundary from source wording/parents.
for n in range(2561,2572):
    r=next(x for x in brows if x["parameter_id"]==f"SB-ASI-P{n:04d}")
    if r.get("primary_domain_role") != "HUMAN_PRIMARY" or not r.get("human_owner"):
        errors.append(f"Human source parameter mis-owned:P{n}")
    if r.get("ai_segments") or r.get("asi_segments"):
        errors.append(f"Human-primary parameter illegally transferred to AI/ASI:P{n}")

# Human-AI coupling retains Human owner and has AI mechanism bindings but no ASI authority by default.
for n in range(2572,2575):
    r=next(x for x in brows if x["parameter_id"]==f"SB-ASI-P{n:04d}")
    if r.get("primary_domain_role") != "HUMAN_AI_INTERFACE" or r.get("human_owner") != "CON-090":
        errors.append(f"Human-AI interface ownership mismatch:P{n}")
    if not r.get("ai_segments"):
        errors.append(f"Human-AI interface lacks AI mechanism binding:P{n}")
    if r.get("asi_segments"):
        errors.append(f"Human-AI interface gained unsupported ASI authority:P{n}")

# Evidence/proof debt controls must include ASI governance.
for n in range(2578,2581):
    r=next(x for x in brows if x["parameter_id"]==f"SB-ASI-P{n:04d}")
    if not r.get("primary_domain_role","").startswith("ASI_") or not r.get("asi_segments"):
        errors.append(f"proof/evidence governance missing ASI ownership:P{n}")

# Simulation parameters must preserve AI mechanism and ASI epistemic governance.
for n in range(2581,2584):
    r=next(x for x in brows if x["parameter_id"]==f"SB-ASI-P{n:04d}")
    if not r.get("ai_segments") or not r.get("asi_segments"):
        errors.append(f"simulation/reality binding incomplete:P{n}")

# Claim-evidence parameters need both AI verification and ASI provenance governance.
for n in range(2590,2593):
    r=next(x for x in brows if x["parameter_id"]==f"SB-ASI-P{n:04d}")
    if not r.get("ai_segments") or not r.get("asi_segments"):
        errors.append(f"claim-evidence binding incomplete:P{n}")

# No new source identities permitted in mapping.
if any(not pid.startswith("SB-ASI-P") for pid in [r.get("parameter_id","") for r in brows]):
    errors.append("mapping rebranded source IDs")

print("errors:",len(errors))
for e in errors:
    print("ERROR",e)
sys.exit(1 if errors else 0)
