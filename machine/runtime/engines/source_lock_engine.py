#!/usr/bin/env python3
"""Source custody and Point-Zero lock engine.

This is the mandatory first engine for a new external input.  It does not
interpret meaning.  It creates deterministic source references, records exact
content hashes, declares the Point Zero scope, and emits an Event-ready source
packet.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Mapping, Sequence
import mimetypes

from .runtime_core import (
    EngineResult,
    RuntimeContractError,
    TraceStep,
    canonicalize,
    digest_text,
    stable_id,
    utc_now,
)

ENGINE_ID = "SB-RT-ENG-SOURCE-LOCK-001"
RULES = [
    "SEQ-LOCK-POINT-ZERO-BEFORE-INTERPRETATION",
    "NO_INVENTION_BEFORE_SOURCE_LOCK",
    "RAW_SOURCE_NE_INTERPRETATION",
]

TEXT_SOURCE_TYPES = {"USER_INPUT", "FILE", "RAW_SOURCE", "GENERATED_TEST_FIXTURE"}


def _source_ref(
    *,
    source_type: str,
    content: str | bytes | None,
    locator: str | None,
    source_id: str | None = None,
    source_truth_status: str = "DIRECT_SOURCE_CONTENT",
    custody_status: str = "LOCKED",
    metadata: Mapping[str, Any] | None = None,
) -> dict[str, Any]:
    if content is None and not locator:
        raise RuntimeContractError("Source requires content or locator")
    if isinstance(content, bytes):
        digest = __import__("hashlib").sha256(content).hexdigest()
        size = len(content)
        content_kind = "BYTES"
    elif isinstance(content, str):
        digest = digest_text(content)
        size = len(content.encode("utf-8"))
        content_kind = "UTF8_TEXT"
    else:
        digest = None
        size = None
        content_kind = "REFERENCE_ONLY"
    sid = source_id or stable_id("SRC", source_type, locator, digest)
    return {
        "source_id": sid,
        "source_type": source_type,
        "locator": locator,
        "fingerprint_sha256": digest,
        "size_bytes": size,
        "content_kind": content_kind,
        "custody_status": custody_status,
        "source_truth_status": source_truth_status,
        "metadata": canonicalize(metadata or {}),
        "locked_at": utc_now(),
    }


def lock_text_source(
    text: str,
    *,
    source_type: str = "USER_INPUT",
    locator: str | None = None,
    source_id: str | None = None,
    scope: str | Mapping[str, Any] = "CURRENT_INPUT",
    parent_point_zero_id: str | None = None,
    metadata: Mapping[str, Any] | None = None,
) -> EngineResult:
    if not isinstance(text, str) or not text.strip():
        raise RuntimeContractError("Text source must be non-empty")
    source = _source_ref(
        source_type=source_type,
        content=text,
        locator=locator,
        source_id=source_id,
        metadata=metadata,
    )
    point_zero_id = stable_id("PZ", source["source_id"], scope, parent_point_zero_id)
    point_zero = {
        "point_zero_id": point_zero_id,
        "scope": canonicalize(scope),
        "status": "LOCAL" if parent_point_zero_id else "LOCKED",
        "source_refs": [source["source_id"]],
        "parent_point_zero_id": parent_point_zero_id,
        "origin_distance_base": 0,
        "notes": "Source custody locked before semantic interpretation.",
    }
    packet = {
        "source_lock_id": stable_id("SRCLOCK", source["source_id"], point_zero_id),
        "source_refs": [source],
        "point_zero": point_zero,
        "raw_content": text,
        "source_scope": canonicalize(scope),
        "interpretation_allowed": True,
        "epistemic_status": "DIRECT_SOURCE",
    }
    trace = TraceStep.create(
        ENGINE_ID,
        "LOCK_TEXT_SOURCE_AND_POINT_ZERO",
        input_refs=[source["source_id"]],
        output_refs=[point_zero_id, packet["source_lock_id"]],
        rule_refs=RULES,
    )
    return EngineResult(ENGINE_ID, "COMPLETE", packet, [trace])


def lock_file_source(
    path: str | Path,
    *,
    source_type: str = "FILE",
    scope: str | Mapping[str, Any] = "FILE_CONTENT",
    parent_point_zero_id: str | None = None,
    metadata: Mapping[str, Any] | None = None,
    include_text_content: bool = True,
) -> EngineResult:
    file_path = Path(path)
    if not file_path.exists() or not file_path.is_file():
        raise RuntimeContractError(f"Source file not found: {file_path}")
    raw = file_path.read_bytes()
    mime, _ = mimetypes.guess_type(file_path.name)
    meta = dict(metadata or {})
    meta.update({"filename": file_path.name, "mime_type": mime, "suffix": file_path.suffix.lower()})
    source = _source_ref(
        source_type=source_type,
        content=raw,
        locator=str(file_path),
        metadata=meta,
    )
    text: str | None = None
    if include_text_content:
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            text = None
    point_zero_id = stable_id("PZ", source["source_id"], scope, parent_point_zero_id)
    point_zero = {
        "point_zero_id": point_zero_id,
        "scope": canonicalize(scope),
        "status": "LOCAL" if parent_point_zero_id else "LOCKED",
        "source_refs": [source["source_id"]],
        "parent_point_zero_id": parent_point_zero_id,
        "origin_distance_base": 0,
        "notes": "File bytes hashed before interpretation; decoded text is derivative access only.",
    }
    packet = {
        "source_lock_id": stable_id("SRCLOCK", source["source_id"], point_zero_id),
        "source_refs": [source],
        "point_zero": point_zero,
        "raw_content": text,
        "binary_content_available": True,
        "source_scope": canonicalize(scope),
        "interpretation_allowed": True,
        "epistemic_status": "DIRECT_SOURCE",
    }
    trace = TraceStep.create(
        ENGINE_ID,
        "LOCK_FILE_SOURCE_AND_POINT_ZERO",
        input_refs=[source["source_id"]],
        output_refs=[point_zero_id, packet["source_lock_id"]],
        rule_refs=RULES,
    )
    return EngineResult(ENGINE_ID, "COMPLETE", packet, [trace])


def lock_multi_source(
    source_packets: Sequence[Mapping[str, Any]],
    *,
    scope: str | Mapping[str, Any],
    parent_point_zero_id: str | None = None,
) -> EngineResult:
    """Create a comparison Point Zero without merging source custody.

    Each source must already be separately locked.  This creates a new Point
    Zero whose source_refs point to those source identities; it never hashes a
    concatenated synthetic super-source and pretends that is original custody.
    """
    source_refs: list[dict[str, Any]] = []
    ids: list[str] = []
    for packet in source_packets:
        refs = packet.get("source_refs", [])
        if not refs:
            raise RuntimeContractError("All multi-source inputs must already be source-locked")
        for ref in refs:
            if isinstance(ref, Mapping):
                source_refs.append(dict(ref))
                ids.append(str(ref.get("source_id")))
    ids = sorted({i for i in ids if i and i != "None"})
    if not ids:
        raise RuntimeContractError("No source identities available for multi-source lock")
    point_zero_id = stable_id("PZ", ids, scope, parent_point_zero_id)
    point_zero = {
        "point_zero_id": point_zero_id,
        "scope": canonicalize(scope),
        "status": "LOCAL" if parent_point_zero_id else "LOCKED",
        "source_refs": ids,
        "parent_point_zero_id": parent_point_zero_id,
        "origin_distance_base": 0,
        "notes": "Comparison Point Zero over separately preserved source identities.",
    }
    payload = {
        "source_lock_id": stable_id("SRCLOCK", ids, point_zero_id),
        "source_refs": source_refs,
        "point_zero": point_zero,
        "raw_content": None,
        "source_scope": canonicalize(scope),
        "interpretation_allowed": True,
        "epistemic_status": "MULTI_SOURCE_COMPARISON",
    }
    trace = TraceStep.create(
        ENGINE_ID,
        "LOCK_MULTI_SOURCE_POINT_ZERO",
        input_refs=ids,
        output_refs=[point_zero_id, payload["source_lock_id"]],
        rule_refs=RULES,
    )
    return EngineResult(ENGINE_ID, "COMPLETE", payload, [trace])
