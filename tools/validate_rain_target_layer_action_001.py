#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "phase2/tests/RAIN_TARGET_LAYER_ACTION_FIXTURE_001.json"
CANDIDATES = ROOT / "registries/sourceborn/REASONING_OPERATION_CANDIDATES_V0.json"
HUMAN_INDEX = ROOT / "registries/human/HUMAN_CONTAINER_INDEX_80_APPROVED_V1.json"
EXAMPLE_REGISTRY = ROOT / "phase2/examples/EXAMPLE_REGISTRY_V1.json"
OUT = ROOT / "generated/tests/P2_RAIN_TARGET_LAYER_ACTION_RFR_001.json"


def load(path):
    return json.loads(path.read_text(encoding="utf-8"))


def main():
    errors = []
    findings = []
    fx = load(FIXTURE)
    cr = load(CANDIDATES)
    hi = load(HUMAN_INDEX)
    er = load(EXAMPLE_REGISTRY)

    known = set()
    for seg in hi.get("segments", []):
        for row in seg.get("containers", []):
            known.add(row[0])

    refs = fx["enumerated_container_refs"]
    unique_refs = set(refs)

    if fx["active_source_registry"]["count"] != 3204:
        errors.append("active source count must be 3204")
    if not fx["source"].get("immutable"):
        errors.append("raw source must remain immutable")
    if len(refs) != len(unique_refs):
        errors.append("enumerated container refs contain duplicates")
    if len(unique_refs) != 28:
        errors.append(f"expected 28 explicitly enumerated unique container refs, got {len(unique_refs)}")
    unknown = sorted(unique_refs - known)
    if unknown:
        errors.append(f"unknown Human container refs: {unknown}")

    declared = fx["declared_container_hit_count_from_source_example"]
    enumerated = fx["enumerated_unique_container_hit_count"]
    rec = fx["container_count_reconciliation"]
    if declared != 30 or enumerated != 28 or rec.get("delta") != 2:
        errors.append("30-vs-28 source count finding was not preserved exactly")
    if rec.get("status") != "SOURCE_INTERNAL_COUNT_MISMATCH_OPEN":
        errors.append("container count mismatch must remain open")
    findings.append("Source example declares 30/80 strong container hits but explicitly names 28 unique CON-* refs; unresolved delta=2 preserved without invented IDs.")

    action_refs = fx["action_mode_additional_regions"]
    if len(action_refs) != 12 or len(set(action_refs)) != 12:
        errors.append("action-mode additional region set must contain 12 unique containers")
    if not set(action_refs).issubset(unique_refs):
        errors.append("action-mode additional regions must be a subset of enumerated source regions")

    expected_layers = ["WORLD_STATE", "SIGNAL_STATE", "PERCEPTION_STATE", "BELIEF_STATE", "BEHAVIOR_STATE"]
    if fx["target_layer_split"] != expected_layers:
        errors.append("target-layer split must preserve world/signal/perception/belief/behavior order")

    by_id = {c["candidate_id"]: c for c in cr.get("candidates", [])}
    expected_candidates = {"RC-TARGET-LAYER-001", "RC-INSTRUMENTAL-TRIGGER-END-001"}
    if set(by_id) != expected_candidates:
        errors.append("reasoning operation candidate registry must contain exactly the two reviewed candidates")
    for cid in expected_candidates:
        c = by_id.get(cid, {})
        if c.get("status") != "REVIEW_REQUIRED":
            errors.append(f"{cid} must remain REVIEW_REQUIRED")
        if c.get("canonical") is not False:
            errors.append(f"{cid} must not be canonical")
        if c.get("direct_action_authority") is not False:
            errors.append(f"{cid} must have no direct action authority")

    if fx.get("canonical_additions") != 0:
        errors.append("fixture must not add canonical parameters")
    if fx.get("exact_atomic_parameter_ids_asserted") is not False:
        errors.append("fixture must not invent exact SB-HFR atomic IDs")

    example_ids = {x.get("example_id") for x in er.get("examples", [])}
    if "EX-RAIN-TARGET-LAYER-ACTION-001" not in example_ids:
        errors.append("rain target-layer example is not registered")

    required_laws = {
        "WORLD_CHANGE != SIGNAL_CHANGE != PERCEPTION_CHANGE != BELIEF_CHANGE != BEHAVIOR_CHANGE",
        "TRIGGER != TERMINAL_GOAL",
        "CANDIDATE_OPERATION != CANONICAL_PARAMETER"
    }
    if not required_laws.issubset(set(fx.get("runtime_laws", []))):
        errors.append("required target-layer/trigger/canonical separation laws missing")

    report = {
        "report_id": "P2-RAIN-TARGET-LAYER-ACTION-RFR-001",
        "status": "PASS" if not errors else "FAIL",
        "checks": {
            "active_source_count": fx["active_source_registry"]["count"],
            "source_declared_container_hits": declared,
            "explicit_unique_container_refs": len(unique_refs),
            "source_internal_count_delta": declared - len(unique_refs),
            "count_mismatch_preserved_open": rec.get("status") == "SOURCE_INTERNAL_COUNT_MISMATCH_OPEN",
            "action_mode_additional_regions": len(action_refs),
            "target_layers": len(fx["target_layer_split"]),
            "reasoning_operation_candidates": len(by_id),
            "canonical_additions": fx.get("canonical_additions"),
            "atomic_ids_invented": fx.get("exact_atomic_parameter_ids_asserted")
        },
        "errors": errors,
        "findings": findings
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2))
    raise SystemExit(1 if errors else 0)


if __name__ == "__main__":
    main()
