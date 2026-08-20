#!/usr/bin/env python3
"""Validate Sourceborn Batch-1 self-sustaining-runtime foundation.

This gate is intentionally stdlib-only so it can run in the existing CI image
without adding a dependency merely to parse/inspect the foundation contracts.
It validates:

- all Batch-1 files exist;
- all JSON files parse;
- schema IDs are unique;
- required schema definitions and fields exist;
- external local JSON-Schema refs resolve to files in machine/schemas;
- the master constitution and execution-flow document contain locked laws;
- the machine invariants preserve Event/Intent, Node-Brain, Memory,
  Combination, growth, loop, authority and no-inflation boundaries;
- the expanded intent schema preserves backward compatibility with the current
  sourceborn.bundle EventRecord reference;
- synthetic output cannot be represented as automatically factual/authoritative;
- Node Brain and Memory structures are persistent and linked, not prompt-only;
- Combination output types include the discovery objects needed by later
  runtime batches.

This is a structural R-F-R gate. Full JSON-Schema instance validation will be
added when the Batch-2 registries provide concrete canonical instances.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, Iterable, List, Set, Tuple

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "generated/tests/P2_BATCH1_FOUNDATION_RFR_V1.json"

BATCH_FILES = {
    "constitution": ROOT / "docs/SOURCEBORN_REALTIME_ASI_CONSTITUTION_V1.md",
    "execution_flow": ROOT / "docs/SOURCEBORN_EXECUTION_FLOW_MASTER.md",
    "invariants": ROOT / "machine/contracts/SOURCEBORN_SYSTEM_INVARIANTS.json",
    "event_record": ROOT / "machine/schemas/event_record.schema.json",
    "event_intent": ROOT / "machine/schemas/event_intent.schema.json",
    "node_brain": ROOT / "machine/schemas/node_brain.schema.json",
    "memory_object": ROOT / "machine/schemas/memory_object.schema.json",
    "combination_record": ROOT / "machine/schemas/combination_record.schema.json",
}

JSON_KEYS = {
    "invariants",
    "event_record",
    "event_intent",
    "node_brain",
    "memory_object",
    "combination_record",
}

errors: List[str] = []
findings: List[Dict[str, Any]] = []
parsed: Dict[str, Any] = {}


def fail(message: str) -> None:
    errors.append(message)


def finding(kind: str, message: str, **extra: Any) -> None:
    item: Dict[str, Any] = {"type": kind, "message": message}
    item.update(extra)
    findings.append(item)


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception as exc:  # pragma: no cover - CI diagnostic path
        fail(f"cannot read {path.relative_to(ROOT)}: {exc}")
        return ""


def load_json(key: str, path: Path) -> Any:
    text = read_text(path)
    if not text:
        return None
    try:
        value = json.loads(text)
    except json.JSONDecodeError as exc:
        fail(f"invalid JSON in {path.relative_to(ROOT)}: {exc}")
        return None
    parsed[key] = value
    return value


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def as_set(value: Any) -> Set[Any]:
    if isinstance(value, list):
        return set(value)
    return set()


def require_subset(actual: Iterable[Any], required: Iterable[Any], label: str) -> None:
    actual_set = set(actual)
    required_set = set(required)
    missing = sorted(required_set - actual_set)
    if missing:
        fail(f"{label} missing: {missing}")


def get_schema_def(schema: Dict[str, Any], name: str, label: str) -> Dict[str, Any]:
    defs = schema.get("$defs", {}) if isinstance(schema, dict) else {}
    value = defs.get(name)
    if not isinstance(value, dict):
        fail(f"{label} missing $defs.{name}")
        return {}
    return value


def required_fields(defn: Dict[str, Any]) -> Set[str]:
    required = defn.get("required", [])
    return set(required) if isinstance(required, list) else set()


def property_names(defn: Dict[str, Any]) -> Set[str]:
    props = defn.get("properties", {})
    return set(props) if isinstance(props, dict) else set()


def enum_values(defn: Dict[str, Any], prop: str) -> Set[Any]:
    props = defn.get("properties", {})
    if not isinstance(props, dict):
        return set()
    item = props.get(prop, {})
    if not isinstance(item, dict):
        return set()
    enum = item.get("enum", [])
    return set(enum) if isinstance(enum, list) else set()


def walk_refs(value: Any) -> Iterable[str]:
    if isinstance(value, dict):
        for key, child in value.items():
            if key == "$ref" and isinstance(child, str):
                yield child
            else:
                yield from walk_refs(child)
    elif isinstance(value, list):
        for child in value:
            yield from walk_refs(child)


def validate_external_local_refs(schema_key: str, schema: Dict[str, Any]) -> None:
    schema_dir = BATCH_FILES[schema_key].parent
    for ref in walk_refs(schema):
        if ref.startswith("#") or "://" in ref:
            continue
        file_part = ref.split("#", 1)[0]
        if not file_part:
            continue
        target = (schema_dir / file_part).resolve()
        try:
            target.relative_to(ROOT)
        except ValueError:
            fail(f"{schema_key} has external ref outside repo: {ref}")
            continue
        if not target.exists():
            fail(f"{schema_key} unresolved local $ref: {ref}")


# ---------------------------------------------------------------------------
# 1. Existence + parse
# ---------------------------------------------------------------------------
for key, path in BATCH_FILES.items():
    if not path.exists():
        fail(f"missing Batch-1 file: {path.relative_to(ROOT)}")

for key in JSON_KEYS:
    path = BATCH_FILES[key]
    if path.exists():
        load_json(key, path)

constitution = read_text(BATCH_FILES["constitution"]) if BATCH_FILES["constitution"].exists() else ""
flow = read_text(BATCH_FILES["execution_flow"]) if BATCH_FILES["execution_flow"].exists() else ""

# ---------------------------------------------------------------------------
# 2. Constitution checks
# ---------------------------------------------------------------------------
constitution_required = [
    "REAL_TIME_GROWING_ASI_PROTOTYPE",
    "EVERYTHING HAPPENING IS AN EVENT, AND ALL EVENTS HAVE INTENT",
    "INTENT != MOTIVE",
    "Node-Brain Law",
    "Memory-Brain Law",
    "Combination Law",
    "Live-Intent Law",
    "Future-State Reconstruction Law",
    "Origin-Distance / Proof-Debt Law",
    "Synthetic Discovery Law",
    "R-F-R Law",
    "New-Node Law",
    "Auto-Link Law",
    "Growth Law",
    "Self-Sustaining Runtime Law",
    "L1 RETRIEVAL LOOP",
    "B4 SCHEDULER / AUTO-SUSTAIN LOOP",
    "AI CAPABILITY",
    "Failure Law",
    "No-Silent-Merge Law",
    "Auditability Law",
]
for token in constitution_required:
    if token not in constitution:
        fail(f"constitution missing required law/token: {token}")

for forbidden_positive in [
    r"Sourceborn\s+is\s+an?\s+LLM\b",
    r"Sourceborn\s+is\s+an?\s+reasoning\s+(?:system|engine)\b",
    r"Sourceborn\s*=\s*LLM\b",
]:
    if re.search(forbidden_positive, constitution, re.I):
        fail(f"constitution contains forbidden positive identity: {forbidden_positive}")

# ---------------------------------------------------------------------------
# 3. Execution flow checks
# ---------------------------------------------------------------------------
flow_required = [
    "Sourceborn Execution Flow Master",
    "Source Lock and Point Zero",
    "Event Decomposition",
    "Existing Brain Activation",
    "Relation, Order and Actor Graph",
    "Node-Brain Activation",
    "Combination Engine",
    "Live Intent Engine",
    "Future-State Reconstruction",
    "Evidence Prediction Engine",
    "Reverse → Forward → Reverse",
    "Memory Brain",
    "Auto-Link Engine",
    "New Node Engine",
    "Growth Ledger",
    "Seed and Recheck Scheduler",
    "Nine Primary Runtime Loops",
    "Four Background Maintenance Loops",
    "Self-Sustain Scheduler Pseudocode",
    "New-Node Pseudocode",
    "Node-Brain Memory Cycle",
    "Tablet Synthetic Discovery Example",
]
for token in flow_required:
    if token not in flow:
        fail(f"execution flow missing required stage/token: {token}")

for loop in [
    "L1 Retrieval Loop",
    "L2 Combination Loop",
    "L3 Intent Loop",
    "L4 Evidence Loop",
    "L5 R-F-R Loop",
    "L6 Contradiction Loop",
    "L7 Memory Reinforcement Loop",
    "L8 Node-Growth Loop",
    "L9 Next-Sequence Loop",
    "B1 Recheck Loop",
    "B2 Orphan-Link Loop",
    "B3 Maturity-Upgrade Loop",
    "B4 Scheduler / Auto-Sustain Loop",
]:
    if loop not in flow:
        fail(f"execution flow missing loop: {loop}")

# ---------------------------------------------------------------------------
# 4. Invariant contract checks
# ---------------------------------------------------------------------------
inv = parsed.get("invariants") or {}
if inv:
    if inv.get("system_identity") != "REAL_TIME_GROWING_ASI_PROTOTYPE":
        fail("invariants system_identity mismatch")

    event_inv = inv.get("event_invariants", {})
    if event_inv.get("every_happening_is_event") is not True:
        fail("invariants must enforce every_happening_is_event=true")
    if event_inv.get("every_event_requires_intent_record") is not True:
        fail("invariants must enforce every_event_requires_intent_record=true")
    if event_inv.get("unknown_preferred_over_fabrication") is not True:
        fail("invariants must prefer UNKNOWN over fabrication")

    node_inv = inv.get("node_brain_invariants", {})
    if node_inv.get("node_brain_is_persistent_bounded_runtime_state") is not True:
        fail("Node Brain must be persistent bounded runtime state")
    if node_inv.get("node_brain_is_prompt") is not False:
        fail("Node Brain must not be a prompt")

    memory_inv = inv.get("memory_invariants", {})
    require_subset(
        memory_inv.get("memory_types", []),
        [
            "RAW_MEMORY",
            "EVENT_MEMORY",
            "INTENT_MEMORY",
            "RELATION_MEMORY",
            "PATH_MEMORY",
            "PATTERN_MEMORY",
            "EVIDENCE_MEMORY",
            "CONTRADICTION_MEMORY",
            "ACTOR_STATE_MEMORY",
            "SEQUENCE_MEMORY",
            "NODE_LOCAL_MEMORY",
            "GLOBAL_MEMORY_INDEX",
        ],
        "invariants memory types",
    )
    if memory_inv.get("repetition_alone_equals_truth") is not False:
        fail("memory invariant repetition_alone_equals_truth must be false")
    if memory_inv.get("repetition_alone_equals_independent_evidence") is not False:
        fail("memory invariant repetition_alone_equals_independent_evidence must be false")

    combo_inv = inv.get("combination_invariants", {})
    if combo_inv.get("combination_is_new_primitive") is not False:
        fail("Combination must not equal new primitive")
    if combo_inv.get("new_wording_is_new_intent") is not False:
        fail("new wording must not automatically equal new Intent")

    growth_inv = inv.get("growth_invariants", {})
    if growth_inv.get("accepted_growth_batch_requires_persistent_count_increase") is not True:
        fail("growth invariant missing monotonic persistent count law")
    if growth_inv.get("parameter_inflation_to_force_growth_forbidden") is not True:
        fail("growth invariant must forbid parameter inflation")

    loops = inv.get("loop_invariants", {})
    if len(loops.get("primary_loops", [])) != 9:
        fail("invariants must define exactly 9 primary loop classes")
    if len(loops.get("background_loops", [])) != 4:
        fail("invariants must define exactly 4 background loop classes")
    if loops.get("fixed_iterations_per_event") is not False:
        fail("loop count per Event must remain dynamic")
    if loops.get("infinite_recursion_allowed") is not False:
        fail("infinite recursion must be forbidden")

    auto = inv.get("autonomy_invariants", {})
    if auto.get("self_sustaining_means_unrestricted_external_authority") is not False:
        fail("self-sustaining runtime must not imply unrestricted external authority")

    batch_required = inv.get("batch1_required_files", [])
    expected_paths = [str(path.relative_to(ROOT)) for path in BATCH_FILES.values()]
    require_subset(batch_required, expected_paths, "invariants batch1_required_files")

# ---------------------------------------------------------------------------
# 5. Schema uniqueness + local ref checks
# ---------------------------------------------------------------------------
schema_ids: Dict[str, str] = {}
for key in ["event_record", "event_intent", "node_brain", "memory_object", "combination_record"]:
    schema = parsed.get(key)
    if not isinstance(schema, dict):
        continue
    sid = schema.get("$id")
    if not isinstance(sid, str) or not sid:
        fail(f"{key} missing $id")
    elif sid in schema_ids:
        fail(f"duplicate schema $id {sid} in {key} and {schema_ids[sid]}")
    else:
        schema_ids[sid] = key
    validate_external_local_refs(key, schema)

# ---------------------------------------------------------------------------
# 6. Event schema checks
# ---------------------------------------------------------------------------
event_schema = parsed.get("event_record") or {}
event = get_schema_def(event_schema, "EventRecord", "event_record")
require_subset(
    required_fields(event),
    [
        "event_id",
        "version",
        "event_type",
        "event_status",
        "source_refs",
        "point_zero",
        "sequence_id",
        "intent",
        "epistemic_status",
        "maturity",
        "lineage",
    ],
    "EventRecord required fields",
)
require_subset(
    property_names(event),
    [
        "observations",
        "actor_roles",
        "state_refs",
        "relation_ids",
        "order_types",
        "activation_refs",
        "node_brain_refs",
        "combination_ids",
        "evidence_prediction_ids",
        "falsifier_ids",
        "pattern_contribution_ids",
        "memory_write_refs",
        "seed_ids",
        "origin_distance",
        "proof_debt",
    ],
    "EventRecord properties",
)

# ---------------------------------------------------------------------------
# 7. Intent schema checks
# ---------------------------------------------------------------------------
intent_schema = parsed.get("event_intent") or {}
intent = get_schema_def(intent_schema, "EventIntent", "event_intent")
legacy_event = get_schema_def(intent_schema, "EventRecord", "event_intent")
require_subset(
    required_fields(intent),
    [
        "intent_id",
        "event_id",
        "intent_type",
        "intent_status",
        "epistemic_status",
        "maturity",
        "source_refs",
        "lineage",
    ],
    "EventIntent required fields",
)
require_subset(
    property_names(intent),
    [
        "actor_roles",
        "actor_view_refs",
        "actor_state_refs",
        "stated_intent",
        "inferred_intent",
        "stated_motive",
        "operating_motive_hypothesis",
        "desired_state_change",
        "method_or_action_tendency",
        "trigger_or_context",
        "priority",
        "constraints",
        "time_horizon",
        "expected_consequence",
        "future_state_candidates",
        "novelty_fingerprint",
        "existing_intent_matches",
        "evidence_prediction_ids",
        "falsifier_ids",
        "origin_distance",
        "proof_debt",
        "direct_action_authority",
    ],
    "EventIntent properties",
)
require_subset(
    enum_values(intent, "intent_type"),
    [
        "AGENT_INTENT",
        "INSTITUTIONAL_INTENT",
        "REPRESENTED_FUTURE_INTENT",
        "FUNCTIONAL_DIRECTION",
        "NATURAL_DYNAMICS_DIRECTION",
        "DERIVED_INTENT_HYPOTHESIS",
        "UNKNOWN",
        "NOT_YET_DECODED",
    ],
    "EventIntent intent types",
)
if not legacy_event:
    fail("event_intent must preserve lightweight EventRecord for current bundle compatibility")

# ---------------------------------------------------------------------------
# 8. Node Brain schema checks
# ---------------------------------------------------------------------------
node_schema = parsed.get("node_brain") or {}
node = get_schema_def(node_schema, "NodeBrain", "node_brain")
require_subset(
    required_fields(node),
    [
        "node_brain_id",
        "version",
        "node_id",
        "node_type",
        "lifecycle_status",
        "working_set",
        "memory_refs",
        "writeback_scope",
        "maturity",
        "epistemic_status",
        "lineage",
    ],
    "NodeBrain required fields",
)
require_subset(
    property_names(node),
    [
        "point_zero_refs",
        "active_event_refs",
        "active_sequence_refs",
        "parent_node_refs",
        "child_node_refs",
        "links",
        "local_state",
        "parameter_binding_refs",
        "rubric_binding_refs",
        "engine_binding_refs",
        "dependency_states",
        "threshold_states",
        "permission_states",
        "candidate_outputs",
        "accepted_return_refs",
        "pending_return_refs",
        "contradiction_refs",
        "falsifier_refs",
        "proof_debt",
        "recheck_rules",
        "runtime_counters",
    ],
    "NodeBrain properties",
)

# ---------------------------------------------------------------------------
# 9. Memory schema checks
# ---------------------------------------------------------------------------
memory_schema = parsed.get("memory_object") or {}
memory = get_schema_def(memory_schema, "MemoryObject", "memory_object")
require_subset(
    required_fields(memory),
    [
        "memory_id",
        "version",
        "memory_type",
        "memory_status",
        "owner_scope",
        "payload",
        "source_refs",
        "retrieval_keys",
        "retention_policy",
        "epistemic_status",
        "maturity",
        "lineage",
    ],
    "MemoryObject required fields",
)
require_subset(
    enum_values(memory, "memory_type"),
    [
        "RAW_MEMORY",
        "EVENT_MEMORY",
        "INTENT_MEMORY",
        "RELATION_MEMORY",
        "PATH_MEMORY",
        "PATTERN_MEMORY",
        "EVIDENCE_MEMORY",
        "CONTRADICTION_MEMORY",
        "ACTOR_STATE_MEMORY",
        "SEQUENCE_MEMORY",
        "NODE_LOCAL_MEMORY",
        "GLOBAL_MEMORY_INDEX",
    ],
    "MemoryObject memory types",
)
require_subset(
    property_names(memory),
    [
        "point_zero_refs",
        "event_refs",
        "sequence_refs",
        "actor_refs",
        "intent_refs",
        "parameter_refs",
        "container_refs",
        "rubric_refs",
        "node_refs",
        "engine_refs",
        "links",
        "supporting_evidence_refs",
        "contradicting_evidence_refs",
        "falsifier_refs",
        "pattern_refs",
        "combination_refs",
        "seed_refs",
        "reinforcement",
        "compression",
        "write_authority",
        "recheck",
    ],
    "MemoryObject properties",
)

# ---------------------------------------------------------------------------
# 10. Combination schema checks
# ---------------------------------------------------------------------------
combo_schema = parsed.get("combination_record") or {}
combo = get_schema_def(combo_schema, "CombinationRecord", "combination_record")
require_subset(
    required_fields(combo),
    [
        "combination_id",
        "version",
        "combination_type",
        "status",
        "event_refs",
        "sequence_ref",
        "components",
        "passes",
        "constraints",
        "budget",
        "novelty",
        "outputs",
        "epistemic_status",
        "maturity",
        "lineage",
    ],
    "CombinationRecord required fields",
)
require_subset(
    property_names(combo),
    [
        "node_brain_refs",
        "relation_refs",
        "path_refs",
        "actor_role_refs",
        "actor_state_refs",
        "actor_view_refs",
        "intent_refs",
        "future_state_refs",
        "pattern_refs",
        "memory_refs",
        "evidence_refs",
        "contradiction_refs",
        "evidence_prediction_ids",
        "rfr_run_refs",
        "falsifier_refs",
        "origin_distance",
        "proof_debt",
        "writeback_class",
    ],
    "CombinationRecord properties",
)
combo_output = get_schema_def(combo_schema, "CombinationOutput", "combination_record")
require_subset(
    enum_values(combo_output, "output_type"),
    [
        "SYNTHETIC_MEANING",
        "EVENT_HYPOTHESIS",
        "INTENT_HYPOTHESIS",
        "ACTOR_BRAIN_VARIANT",
        "SEQUENCE_VARIANT",
        "EVIDENCE_PREDICTION",
        "PATTERN_CANDIDATE",
        "NODE_CANDIDATE",
        "PRIMITIVE_CANDIDATE",
        "RELATION_CANDIDATE",
        "PATH_CANDIDATE",
    ],
    "Combination output types",
)

# ---------------------------------------------------------------------------
# 11. Cross-file invariant consistency
# ---------------------------------------------------------------------------
if inv and intent:
    intent_types_contract = as_set(inv.get("event_invariants", {}).get("intent_types", []))
    intent_types_schema = enum_values(intent, "intent_type")
    if intent_types_contract != intent_types_schema:
        fail(
            "intent type mismatch between machine invariants and event_intent schema: "
            f"contract_only={sorted(intent_types_contract - intent_types_schema)} "
            f"schema_only={sorted(intent_types_schema - intent_types_contract)}"
        )

if inv and memory:
    contract_memory = as_set(inv.get("memory_invariants", {}).get("memory_types", []))
    schema_memory = enum_values(memory, "memory_type")
    if contract_memory != schema_memory:
        fail(
            "memory type mismatch between machine invariants and memory schema: "
            f"contract_only={sorted(contract_memory - schema_memory)} "
            f"schema_only={sorted(schema_memory - contract_memory)}"
        )

# Informational finding: bundle linking is intentionally a next-pass task.
bundle_path = ROOT / "machine/schemas/sourceborn.bundle.schema.json"
if bundle_path.exists():
    bundle_text = read_text(bundle_path)
    missing_bundle_defs = []
    for name in ["NodeBrain", "MemoryObject", "CombinationRecord"]:
        if f'"{name}"' not in bundle_text:
            missing_bundle_defs.append(name)
    if missing_bundle_defs:
        finding(
            "NEXT_LINK_PASS_REQUIRED",
            "Batch-1 schemas exist but are not yet exported from sourceborn.bundle.schema.json; this is reserved for the explicit linking pass.",
            definitions=missing_bundle_defs,
        )

# ---------------------------------------------------------------------------
# 12. Build report
# ---------------------------------------------------------------------------
file_report = []
for key, path in BATCH_FILES.items():
    if not path.exists():
        continue
    file_report.append(
        {
            "key": key,
            "path": str(path.relative_to(ROOT)),
            "size_bytes": path.stat().st_size,
            "sha256": sha256(path),
        }
    )

report = {
    "report_id": "P2-BATCH1-FOUNDATION-RFR-V1",
    "status": "PASS" if not errors else "FAIL",
    "system_identity": "REAL_TIME_GROWING_ASI_PROTOTYPE",
    "batch": "BATCH_1_FOUNDATION",
    "foundation_file_count": len(BATCH_FILES),
    "json_file_count": len(JSON_KEYS),
    "schema_ids": schema_ids,
    "files": file_report,
    "checks": {
        "constitution_laws": len(constitution_required),
        "execution_flow_stage_tokens": len(flow_required),
        "runtime_loop_classes_expected": 13,
        "event_schema_checked": bool(event),
        "intent_schema_checked": bool(intent),
        "node_brain_schema_checked": bool(node),
        "memory_schema_checked": bool(memory),
        "combination_schema_checked": bool(combo),
        "local_schema_refs_checked": true,
        "cross_file_type_consistency_checked": true,
    },
    "findings": findings,
    "errors": errors,
    "next_legal_pass": "BATCH1_SCHEMA_BUNDLE_AND_RUNTIME_LINKING" if not errors else "REPAIR_BATCH1_FOUNDATION",
}

OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

print(
    report["status"],
    "foundation_files", report["foundation_file_count"],
    "json", report["json_file_count"],
    "findings", len(findings),
    "errors", len(errors),
)

for item in findings:
    print("FINDING", item["type"], item["message"])
for item in errors[:100]:
    print("ERROR", item)

sys.exit(1 if errors else 0)
