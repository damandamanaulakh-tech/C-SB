#!/usr/bin/env python3
"""Link Batch-2 self-sustaining runtime schemas into the Sourceborn schema bundle.

This is intentionally additive and idempotent. It does not rewrite the source
schemas and does not delete legacy definitions. It updates the bundle's public
refs and adds optional graph/runtime references to existing Sequence/Node defs.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
BUNDLE_PATH = ROOT / "machine/schemas/sourceborn.bundle.schema.json"

REQUIRED_SCHEMA_FILES = {
    "event_record.schema.json": ROOT / "machine/schemas/event_record.schema.json",
    "event_intent.schema.json": ROOT / "machine/schemas/event_intent.schema.json",
    "node_brain.schema.json": ROOT / "machine/schemas/node_brain.schema.json",
    "memory_object.schema.json": ROOT / "machine/schemas/memory_object.schema.json",
    "combination_record.schema.json": ROOT / "machine/schemas/combination_record.schema.json",
}


def load_json(path: Path) -> dict:
    with path.open("r", encoding="utf-8") as f:
        return json.load(f)


def save_json(path: Path, obj: dict) -> None:
    with path.open("w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, indent=2)
        f.write("\n")


def ensure_files() -> None:
    missing = [name for name, path in REQUIRED_SCHEMA_FILES.items() if not path.exists()]
    if missing:
        raise SystemExit(f"Batch-2 schema link missing required files: {missing}")
    for name, path in REQUIRED_SCHEMA_FILES.items():
        doc = load_json(path)
        if "$defs" not in doc:
            raise SystemExit(f"{name} has no $defs")


def array_of_strings() -> dict:
    return {"type": "array", "items": {"type": "string"}, "uniqueItems": True}


def main() -> None:
    ensure_files()
    bundle = load_json(BUNDLE_PATH)
    defs = bundle.setdefault("$defs", {})

    # Preserve the pre-Batch-2 EventRecord contract as an explicit legacy alias.
    # The active EventRecord now points at the dedicated richer schema.
    defs["LegacyEventRecordV1"] = {
        "$ref": "event_intent.schema.json#/$defs/EventRecord"
    }
    defs["EventIntent"] = {
        "$ref": "event_intent.schema.json#/$defs/EventIntent"
    }
    defs["EventRecord"] = {
        "$ref": "event_record.schema.json#/$defs/EventRecord"
    }
    defs["PointZeroRef"] = {
        "$ref": "event_record.schema.json#/$defs/PointZeroRef"
    }
    defs["ActorRoleSet"] = {
        "$ref": "event_record.schema.json#/$defs/ActorRoleSet"
    }
    defs["NodeBrain"] = {
        "$ref": "node_brain.schema.json#/$defs/NodeBrain"
    }
    defs["NodeLink"] = {
        "$ref": "node_brain.schema.json#/$defs/NodeLink"
    }
    defs["MemoryObject"] = {
        "$ref": "memory_object.schema.json#/$defs/MemoryObject"
    }
    defs["MemoryLink"] = {
        "$ref": "memory_object.schema.json#/$defs/MemoryLink"
    }
    defs["RetrievalKey"] = {
        "$ref": "memory_object.schema.json#/$defs/RetrievalKey"
    }
    defs["CombinationRecord"] = {
        "$ref": "combination_record.schema.json#/$defs/CombinationRecord"
    }
    defs["CombinationComponent"] = {
        "$ref": "combination_record.schema.json#/$defs/CombinationComponent"
    }
    defs["CombinationOutput"] = {
        "$ref": "combination_record.schema.json#/$defs/CombinationOutput"
    }

    # Add optional linking fields to the existing Sequence definition.
    # No prior required fields or meanings are removed.
    seq = defs.get("Sequence")
    if isinstance(seq, dict):
        props = seq.setdefault("properties", {})
        props.setdefault("event_ids", array_of_strings())
        props.setdefault("node_brain_ids", array_of_strings())
        props.setdefault("memory_ids", array_of_strings())
        props.setdefault("combination_ids", array_of_strings())
        props.setdefault("intent_ids", array_of_strings())
        props.setdefault("pattern_contribution_ids", array_of_strings())
        props.setdefault("growth_batch_ids", array_of_strings())
        props.setdefault("runtime_link_contract_ref", {"type": ["string", "null"]})

    # Add optional linking fields to the existing case-graph Node definition.
    node = defs.get("Node")
    if isinstance(node, dict):
        props = node.setdefault("properties", {})
        props.setdefault("node_brain_ref", {"type": ["string", "null"]})
        props.setdefault("event_refs", array_of_strings())
        props.setdefault("intent_refs", array_of_strings())
        props.setdefault("memory_refs", array_of_strings())
        props.setdefault("combination_refs", array_of_strings())
        props.setdefault("pattern_refs", array_of_strings())
        props.setdefault("actor_view_refs", array_of_strings())
        props.setdefault("runtime_stage_refs", array_of_strings())

    bundle["x-sourceborn-runtime-linking"] = {
        "version": "BATCH2_V1",
        "system_identity": "REAL_TIME_GROWING_ASI_PROTOTYPE",
        "runtime_contract": "../runtime/SELF_SUSTAINING_RUNTIME_LINK_CONTRACT_V1.json",
        "node_brain_bindings": "../../registries/sourceborn/NODE_BRAIN_RUNTIME_BINDINGS_V1.json",
        "memory_channels": "../../registries/sourceborn/MEMORY_CHANNEL_REGISTRY_V1.json",
        "auto_link_relations": "../../registries/sourceborn/AUTO_LINK_RELATION_REGISTRY_V1.json",
        "combination_bindings": "../../registries/sourceborn/COMBINATION_RUNTIME_BINDINGS_V1.json",
        "linking_law": "Schema exports are additive. Runtime bindings do not overwrite native Human/AI/Wisdom/ASI definitions or Sequence truth."
    }

    save_json(BUNDLE_PATH, bundle)
    print(
        "Batch-2 schema linking complete:",
        "defs=", len(defs),
        "EventRecord=standalone",
        "NodeBrain=linked",
        "MemoryObject=linked",
        "CombinationRecord=linked",
    )


if __name__ == "__main__":
    main()
