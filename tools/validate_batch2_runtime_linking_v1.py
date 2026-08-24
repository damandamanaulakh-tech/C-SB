#!/usr/bin/env python3
"""R-F-R validator for Sourceborn Batch-2 runtime/schema linking.

Validates the structural links introduced after Batch-1:
- 22 runtime stages are valid and node-routed;
- all 22 ASI service Nodes have one Node-Brain binding;
- all 12 MemoryObject memory types have one channel definition;
- all Node/runtime memory reads+writes reference valid channels;
- 6 bounded combination modes align with CombinationRecord schema;
- auto-link direct relation encoding stays inside MemoryLink enum and richer
  runtime relations use the stable OTHER + extended_relation_type form;
- sourceborn.bundle exports the linked schemas after the linker runs;
- autonomy boundaries and loop counts remain explicit.
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "generated/tests/P2_BATCH2_RUNTIME_LINKING_RFR_V1.json"

PATHS = {
    "runtime": ROOT / "machine/runtime/SELF_SUSTAINING_RUNTIME_LINK_CONTRACT_V1.json",
    "nodes": ROOT / "registries/asi/asi_node_registry.json",
    "bindings": ROOT / "registries/sourceborn/NODE_BRAIN_RUNTIME_BINDINGS_V1.json",
    "memory_channels": ROOT / "registries/sourceborn/MEMORY_CHANNEL_REGISTRY_V1.json",
    "auto_links": ROOT / "registries/sourceborn/AUTO_LINK_RELATION_REGISTRY_V1.json",
    "combination_bindings": ROOT / "registries/sourceborn/COMBINATION_RUNTIME_BINDINGS_V1.json",
    "memory_schema": ROOT / "machine/schemas/memory_object.schema.json",
    "combination_schema": ROOT / "machine/schemas/combination_record.schema.json",
    "event_schema": ROOT / "machine/schemas/event_record.schema.json",
    "intent_schema": ROOT / "machine/schemas/event_intent.schema.json",
    "node_brain_schema": ROOT / "machine/schemas/node_brain.schema.json",
    "bundle": ROOT / "machine/schemas/sourceborn.bundle.schema.json",
    "invariants": ROOT / "machine/contracts/SOURCEBORN_SYSTEM_INVARIANTS.json",
}


def load(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def uniq(values):
    return len(values) == len(set(values))


def add(errors, cond, message):
    if not cond:
        errors.append(message)


def main() -> int:
    errors: list[str] = []
    findings: list[str] = []

    for name, path in PATHS.items():
        add(errors, path.exists(), f"missing required Batch-2 file: {name} -> {path.relative_to(ROOT)}")
    if errors:
        report = {"report_id":"P2-BATCH2-RUNTIME-LINKING-RFR-V1","status":"FAIL","errors":errors,"findings":findings}
        OUT.parent.mkdir(parents=True, exist_ok=True)
        OUT.write_text(json.dumps(report, indent=2)+"\n", encoding="utf-8")
        return 1

    docs = {name: load(path) for name, path in PATHS.items()}
    runtime = docs["runtime"]
    node_registry = docs["nodes"]
    bindings = docs["bindings"]
    memory_channels = docs["memory_channels"]
    auto_links = docs["auto_links"]
    combo_bindings = docs["combination_bindings"]
    memory_schema = docs["memory_schema"]
    combo_schema = docs["combination_schema"]
    bundle = docs["bundle"]
    invariants = docs["invariants"]

    # Identity / authority checks.
    add(errors, runtime.get("system_identity") == "REAL_TIME_GROWING_ASI_PROTOTYPE", "runtime identity drift")
    add(errors, invariants.get("system_identity") == "REAL_TIME_GROWING_ASI_PROTOTYPE", "invariant identity drift")
    autonomy = runtime.get("autonomy_boundary", {})
    add(errors, "unrestricted_tool_execution" in autonomy.get("never_implied", []), "autonomy boundary missing unrestricted-tool exclusion")
    add(errors, "authority_check" in autonomy.get("external_action_requires", []), "external action authority check missing")
    add(errors, "permission_check" in autonomy.get("external_action_requires", []), "external action permission check missing")
    add(errors, "barrier_clearance" in autonomy.get("external_action_requires", []), "external action barrier clearance missing")

    # Runtime stages.
    stages = runtime.get("stages", [])
    stage_ids = [x.get("stage_id") for x in stages]
    expected_stage_ids = [f"RT-{i:02d}" for i in range(1, 23)]
    add(errors, len(stages) == 22, f"runtime stage count must be 22, got {len(stages)}")
    add(errors, stage_ids == expected_stage_ids, f"runtime stage IDs/order mismatch: {stage_ids}")
    add(errors, uniq(stage_ids), "duplicate runtime stage IDs")

    # ASI service Nodes and one-to-one Node-Brain bindings.
    node_ids = [x.get("asi_node_id") for x in node_registry.get("nodes", [])]
    binding_ids = [x.get("asi_node_id") for x in bindings.get("bindings", [])]
    expected_node_ids = [f"ASI-NODE-{i:02d}" for i in range(22)]
    add(errors, node_registry.get("node_count") == 22, "ASI node registry count != 22")
    add(errors, node_ids == expected_node_ids, "ASI node ID set/order mismatch")
    add(errors, bindings.get("node_count") == 22, "Node-Brain binding count != 22")
    add(errors, sorted(binding_ids) == sorted(node_ids), "Node-Brain bindings must cover exactly all ASI service Nodes")
    add(errors, uniq(binding_ids), "duplicate Node-Brain binding IDs")

    valid_nodes = set(node_ids)
    valid_stages = set(stage_ids)
    for st in stages:
        sid = st.get("stage_id")
        pnodes = st.get("primary_nodes", [])
        add(errors, bool(pnodes), f"{sid} has no primary_nodes")
        unknown = sorted(set(pnodes) - valid_nodes)
        add(errors, not unknown, f"{sid} references unknown ASI Nodes: {unknown}")
        add(errors, bool(st.get("hard_guards")), f"{sid} has no hard_guards")

    for b in bindings.get("bindings", []):
        nid = b.get("asi_node_id")
        add(errors, bool(b.get("node_brain_type")), f"{nid} missing node_brain_type")
        unknown_stages = sorted(set(b.get("runtime_stages", [])) - valid_stages)
        add(errors, not unknown_stages, f"{nid} references unknown runtime stages: {unknown_stages}")
        add(errors, bool(b.get("must_not_do")), f"{nid} missing must_not_do guards")

    # Memory type source of truth comes from MemoryObject schema.
    try:
        valid_memory_types = set(memory_schema["$defs"]["MemoryObject"]["properties"]["memory_type"]["enum"])
    except Exception as exc:
        errors.append(f"cannot read MemoryObject.memory_type enum: {exc}")
        valid_memory_types = set()
    channel_types = [x.get("memory_type") for x in memory_channels.get("channels", [])]
    add(errors, memory_channels.get("channel_count") == 12, "memory channel registry count != 12")
    add(errors, len(channel_types) == 12 and uniq(channel_types), "memory channels must enumerate 12 unique types")
    add(errors, set(channel_types) == valid_memory_types, f"memory channel types differ from schema enum: registry={sorted(channel_types)}, schema={sorted(valid_memory_types)}")

    for st in stages:
        for field in ("reads", "writes"):
            unknown = sorted(set(st.get(field, [])) - valid_memory_types)
            add(errors, not unknown, f"{st.get('stage_id')} {field} unknown memory types: {unknown}")
    for b in bindings.get("bindings", []):
        for field in ("read_memory", "write_memory"):
            unknown = sorted(set(b.get(field, [])) - valid_memory_types)
            add(errors, not unknown, f"{b.get('asi_node_id')} {field} unknown memory types: {unknown}")

    # Combination schema/bindings.
    try:
        combo_types = set(combo_schema["$defs"]["CombinationRecord"]["properties"]["combination_type"]["enum"])
        output_types = set(combo_schema["$defs"]["CombinationOutput"]["properties"]["output_type"]["enum"])
        pass_types = set(combo_schema["$defs"]["CombinationPass"]["properties"]["pass_type"]["enum"])
    except Exception as exc:
        errors.append(f"cannot read Combination schema enums: {exc}")
        combo_types, output_types, pass_types = set(), set(), set()

    modes = combo_bindings.get("modes", [])
    mode_ids = [x.get("mode_id") for x in modes]
    mode_names = [x.get("name") for x in modes]
    add(errors, mode_ids == ["C1","C2","C3","C4","C5","C6"], f"combination mode IDs mismatch: {mode_ids}")
    add(errors, set(mode_names).issubset(combo_types), f"combination binding names not supported by CombinationRecord enum: {sorted(set(mode_names)-combo_types)}")
    expected_pass_names = {"ADJACENCY","PATTERN_SUPPORTED","CONTRADICTION","COUNTERFACTUAL","CROSS_DOMAIN","NOVELTY"}
    add(errors, expected_pass_names == pass_types, f"CombinationPass enum mismatch: {sorted(pass_types)}")
    for mode in modes:
        unknown_nodes = sorted(set(mode.get("primary_nodes", []) + mode.get("next_nodes", [])) - valid_nodes)
        add(errors, not unknown_nodes, f"{mode.get('mode_id')} unknown node refs: {unknown_nodes}")
        unknown_mem = sorted(set(mode.get("read_memory", [])) - valid_memory_types)
        add(errors, not unknown_mem, f"{mode.get('mode_id')} unknown memory refs: {unknown_mem}")
        unknown_out = sorted(set(mode.get("candidate_outputs", [])) - output_types)
        add(errors, not unknown_out, f"{mode.get('mode_id')} unknown output types: {unknown_out}")

    routing = combo_bindings.get("output_routing", [])
    routed_outputs = [x.get("output_type") for x in routing]
    add(errors, set(routed_outputs) == output_types, f"output routing must cover all CombinationOutput types; missing={sorted(output_types-set(routed_outputs))} extra={sorted(set(routed_outputs)-output_types)}")
    for route in routing:
        unknown = sorted(set(route.get("required_next_stages", [])) - valid_stages)
        add(errors, not unknown, f"output route {route.get('output_type')} has unknown stages: {unknown}")

    # Auto-link stable schema compatibility.
    try:
        memory_link_enum = set(memory_schema["$defs"]["MemoryLink"]["properties"]["relation_type"]["enum"])
    except Exception as exc:
        errors.append(f"cannot read MemoryLink relation enum: {exc}")
        memory_link_enum = set()
    enc = auto_links.get("memory_link_encoding", {})
    direct = set(enc.get("direct_memory_link_types", []))
    add(errors, direct.issubset(memory_link_enum), f"direct auto-link types exceed stable MemoryLink enum: {sorted(direct-memory_link_enum)}")
    extended_encoding = enc.get("extended_relation_encoding", {})
    add(errors, extended_encoding.get("relation_type") == "OTHER", "extended relation encoding must use MemoryLink OTHER")
    add(errors, "OTHER" in memory_link_enum, "MemoryLink schema lacks OTHER required for extended relation encoding")
    relation_names = [x.get("relation_type") for x in auto_links.get("relation_types", [])]
    add(errors, uniq(relation_names), "duplicate auto-link relation type")
    add(errors, "SAME_AS" in relation_names, "auto-link registry missing SAME_AS identity gate")
    same_as = next((x for x in auto_links.get("relation_types", []) if x.get("relation_type") == "SAME_AS"), {})
    add(errors, same_as.get("auto_candidate") is False, "SAME_AS must never be auto-candidate")

    # Loop counts.
    primary = runtime.get("primary_loops", [])
    maintenance = runtime.get("maintenance_loops", [])
    add(errors, len(primary) == 9 and [x.get("loop_id") for x in primary] == [f"L{i}" for i in range(1,10)], "primary loops must be L1..L9")
    add(errors, len(maintenance) == 4 and [x.get("loop_id") for x in maintenance] == [f"B{i}" for i in range(1,5)], "maintenance loops must be B1..B4")
    counts = runtime.get("loop_count", {})
    add(errors, counts == {"primary":9,"maintenance":4,"total_classes":13}, f"loop_count mismatch: {counts}")

    # Bundle must be linked after tools/link_batch2_runtime_schemas_v1.py runs.
    defs = bundle.get("$defs", {})
    expected_bundle_refs = {
        "EventRecord":"event_record.schema.json#/$defs/EventRecord",
        "LegacyEventRecordV1":"event_intent.schema.json#/$defs/EventRecord",
        "EventIntent":"event_intent.schema.json#/$defs/EventIntent",
        "PointZeroRef":"event_record.schema.json#/$defs/PointZeroRef",
        "ActorRoleAssignment":"event_record.schema.json#/$defs/ActorRoleAssignment",
        "NodeBrain":"node_brain.schema.json#/$defs/NodeBrain",
        "NodeLink":"node_brain.schema.json#/$defs/NodeLink",
        "MemoryObject":"memory_object.schema.json#/$defs/MemoryObject",
        "MemoryLink":"memory_object.schema.json#/$defs/MemoryLink",
        "RetrievalKey":"memory_object.schema.json#/$defs/RetrievalKey",
        "CombinationRecord":"combination_record.schema.json#/$defs/CombinationRecord",
        "CombinationComponent":"combination_record.schema.json#/$defs/ComponentRef",
        "CombinationOutput":"combination_record.schema.json#/$defs/CombinationOutput",
    }
    for name, ref in expected_bundle_refs.items():
        add(errors, defs.get(name, {}).get("$ref") == ref, f"bundle export {name} incorrect or missing")

    link_meta = bundle.get("x-sourceborn-runtime-linking", {})
    add(errors, link_meta.get("version") == "BATCH2_V1", "bundle Batch-2 runtime-link metadata missing")

    sequence_props = defs.get("Sequence", {}).get("properties", {})
    for prop in ["event_ids","node_brain_ids","memory_ids","combination_ids","intent_ids","pattern_contribution_ids","growth_batch_ids","runtime_link_contract_ref"]:
        add(errors, prop in sequence_props, f"Sequence missing additive runtime property {prop}")
    node_props = defs.get("Node", {}).get("properties", {})
    for prop in ["node_brain_ref","event_refs","intent_refs","memory_refs","combination_refs","pattern_refs","actor_view_refs","runtime_stage_refs"]:
        add(errors, prop in node_props, f"Node missing additive runtime property {prop}")

    # Cross-file semantic guards.
    add(errors, any("COMBINATION_NE_NEW_PRIMITIVE" in x.get("hard_guards", []) for x in stages), "runtime lacks combination/new-primitive separation")
    add(errors, any("NEW_WORDING_NE_NEW_INTENT" in x.get("hard_guards", []) for x in stages), "runtime lacks wording/intent novelty separation")
    add(errors, any("SELF_SUSTAINING_NE_UNRESTRICTED_EXTERNAL_AUTHORITY" in x.get("hard_guards", []) for x in stages), "runtime lacks self-sustain authority boundary")

    if not errors:
        findings.append("All 22 existing ASI service Nodes are linked one-to-one to persistent Node-Brain bindings.")
        findings.append("All 12 MemoryObject memory types have exactly one channel contract.")
        findings.append("All six bounded Combination modes and all CombinationOutput types are routed.")
        findings.append("Extended auto-link relations preserve the stable MemoryLink enum via OTHER + extended_relation_type.")
        findings.append("The schema bundle exports the Batch-2 Event/NodeBrain/Memory/Combination contracts additively.")

    report = {
        "report_id":"P2-BATCH2-RUNTIME-LINKING-RFR-V1",
        "status":"PASS" if not errors else "FAIL",
        "system_identity":"REAL_TIME_GROWING_ASI_PROTOTYPE",
        "counts":{
            "runtime_stages":len(stages),
            "asi_service_nodes":len(node_ids),
            "node_brain_bindings":len(binding_ids),
            "memory_channels":len(channel_types),
            "combination_modes":len(modes),
            "combination_output_types":len(output_types),
            "auto_link_relation_types":len(relation_names),
            "primary_loops":len(primary),
            "maintenance_loops":len(maintenance),
            "total_loop_classes":len(primary)+len(maintenance)
        },
        "findings":findings,
        "errors":errors,
        "next_sequence_after_pass":"BATCH3_RUNTIME_ENGINE_IMPLEMENTATION",
        "audit_law":"Runtime linking may add graph/schema bindings but may not change native domain definitions, fabricate provenance, inflate parameter counts, or grant unrestricted external authority."
    }
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2)+"\n", encoding="utf-8")
    print(report["status"], json.dumps(report["counts"], sort_keys=True), "errors", len(errors))
    for e in errors[:80]:
        print("ERROR", e)
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
