#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
reg_path = ROOT / "generated/registry_views/human_functional_3204_registry_v1.json"
sum_path = ROOT / "generated/registry_views/human_functional_3204_summary_v1.json"
manifest_path = ROOT / "registries/human/HUMAN_FUNCTIONAL_REGISTRY_3204_V1.json"

reg = json.loads(reg_path.read_text(encoding="utf-8"))
summary = json.loads(sum_path.read_text(encoding="utf-8"))
manifest = json.loads(manifest_path.read_text(encoding="utf-8"))

errors = []
params = reg.get("parameters", [])
ids = [p.get("parameter_id") for p in params]
expected = [f"SB-HFR-P{i:04d}" for i in range(1, 3205)]

if len(params) != 3204: errors.append(f"expected 3204 parameters, got {len(params)}")
if ids != expected: errors.append("SB-HFR-P0001..P3204 exact contiguous ID coverage failed")
if summary.get("legacy_count") != 2560: errors.append("legacy baseline count changed")
if summary.get("net_count_change") != 644: errors.append("net count change must be +644")
if summary.get("grown_containers") != 77: errors.append("expected 77 grown containers")
if summary.get("unchanged_containers") != 2: errors.append("expected 2 unchanged containers")
contracted = summary.get("contracted_source_version_containers", [])
if len(contracted) != 1 or contracted[0].get("container_id") != "CON-042" or contracted[0].get("legacy_count") != 48 or contracted[0].get("v1_count") != 42:
    errors.append("CON-042 source-version divergence must remain explicit as 48 -> 42")
if manifest["identity_policy"].get("legacy_rows_deleted") is not False:
    errors.append("legacy deletion must remain forbidden")
if manifest["identity_policy"].get("legacy_rows_renamed") is not False:
    errors.append("legacy renaming must remain forbidden")
scaffolds = manifest.get("scaffolds_not_counted_as_parameters", {})
if any(scaffolds.get(k, 0) <= 0 for k in ["universal_filters","operating_states","evidence_levels","failure_distortion_classes","operating_chain_steps"]):
    errors.append("scaffold separation metadata incomplete")
if manifest["runtime_owner_policy"].get("rule") != "SOURCE LOCATION != RUNTIME OWNERSHIP":
    errors.append("runtime ownership separation law missing")
if any(p.get("runtime_owner_status") != "UNCLASSIFIED_PENDING_P2_HUMAN_3204_RUNTIME_OWNER_RECLASSIFICATION" for p in params):
    errors.append("3204 source rows were prematurely assigned runtime ownership")
if any(p.get("legacy_atomic_alias_status") != "NOT_INFERRED" for p in params):
    errors.append("legacy atomic aliases were inferred without a source reconciliation pass")

report = {
    "report_id":"P2-HUMAN-FUNCTIONAL-3204-EXPANSION-RFR-V1",
    "status":"PASS" if not errors else "FAIL",
    "checks":{
        "expanded_parameter_count":len(params),
        "legacy_parameter_count":summary.get("legacy_count"),
        "net_count_change":summary.get("net_count_change"),
        "segments":len(summary.get("segments",{})),
        "containers":len(summary.get("containers",[])),
        "grown_containers":summary.get("grown_containers"),
        "unchanged_containers":summary.get("unchanged_containers"),
        "contracted_source_version_containers":len(contracted),
        "legacy_ids_preserved":manifest["identity_policy"].get("legacy_rows_deleted") is False and manifest["identity_policy"].get("legacy_rows_renamed") is False,
        "runtime_owner_not_forced":not any(p.get("runtime_owner_status") != "UNCLASSIFIED_PENDING_P2_HUMAN_3204_RUNTIME_OWNER_RECLASSIFICATION" for p in params),
        "scaffolds_excluded_from_parameter_count":True
    },
    "errors":errors,
    "findings":[
        "CON-042 Core Reasoning is 48 in the legacy 2,560 container index but 42 in the v1.0 3,204 source; no legacy row is deleted. Atomic reconciliation remains open."
    ]
}
out = ROOT / "generated/tests/P2_HUMAN_FUNCTIONAL_3204_EXPANSION_RFR_V1.json"
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text(json.dumps(report, indent=2), encoding="utf-8")
if errors:
    raise SystemExit("\n".join(errors))
print("PASS: Human-derived functional source count raised 2560 -> 3204; legacy identities preserved.")
