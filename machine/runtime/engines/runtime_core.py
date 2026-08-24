#!/usr/bin/env python3
"""Shared deterministic primitives for Sourceborn Batch-3 runtime engines.

Design goals
============
* stdlib only; no model/provider dependency;
* deterministic IDs for the same canonical payload;
* source/provenance preservation before interpretation;
* registry lookup without assuming one fixed JSON shape;
* explicit trace records for every engine transition;
* no automatic promotion of synthetic material to fact;
* no file-system write side effects unless a caller explicitly requests them.

This module is deliberately larger than a convenience helper because the
runtime needs one consistent implementation of hashing, canonicalization,
registry matching, maturity ordering and evidence bookkeeping.  Engines must
not quietly invent their own incompatible variants.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from hashlib import sha256
from pathlib import Path
from typing import Any, Iterable, Iterator, Mapping, MutableMapping, Sequence
import json
import math
import re

SYSTEM_IDENTITY = "REAL_TIME_GROWING_ASI_PROTOTYPE"
RUNTIME_VERSION = "BATCH3_V1"

Maturity = str
MATURITY_ORDER: tuple[Maturity, ...] = ("M0", "M1", "M2", "M3", "M4", "M5")

ID_KEYS = (
    "id",
    "event_id",
    "intent_id",
    "memory_id",
    "combination_id",
    "node_id",
    "asi_node_id",
    "parameter_id",
    "container_id",
    "segment_id",
    "pattern_id",
    "relation_id",
    "path_id",
    "engine_id",
    "binding_id",
    "wisdom_id",
    "seed_id",
    "sequence_id",
)
NAME_KEYS = (
    "name",
    "exact_name",
    "container_name",
    "segment_name",
    "parameter_name",
    "service_role",
    "title",
    "principle",
    "label",
)
TEXT_KEYS = NAME_KEYS + (
    "definition",
    "native_definition",
    "full_scope_wording",
    "scope",
    "functional_interpretation",
    "purpose",
    "description",
    "reason",
    "interpretation",
    "notes",
)

TOKEN_RE = re.compile(r"[A-Za-z0-9][A-Za-z0-9_\-]{1,}")
STOP_TOKENS = {
    "the", "and", "for", "with", "from", "that", "this", "into", "when",
    "where", "what", "which", "while", "have", "has", "had", "are", "was",
    "were", "will", "would", "could", "should", "their", "there", "then",
    "than", "not", "only", "also", "each", "some", "such", "one", "two",
    "new", "sourceborn", "sequence", "event", "object", "record", "system",
}


class RuntimeContractError(ValueError):
    """Raised when a runtime input violates a locked structural contract."""


class SourceBoundaryError(RuntimeContractError):
    """Raised when interpretation is attempted before source/Point-Zero lock."""


class RegistryResolutionError(RuntimeContractError):
    """Raised when a required registry identity cannot be resolved legally."""


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def canonicalize(value: Any) -> Any:
    """Return a JSON-compatible value with deterministic map ordering semantics."""
    if isinstance(value, Mapping):
        return {str(k): canonicalize(value[k]) for k in sorted(value, key=lambda x: str(x))}
    if isinstance(value, (list, tuple)):
        return [canonicalize(v) for v in value]
    if isinstance(value, set):
        return [canonicalize(v) for v in sorted(value, key=lambda x: str(x))]
    if isinstance(value, Path):
        return str(value)
    if hasattr(value, "__dataclass_fields__"):
        return canonicalize(asdict(value))
    return value


def canonical_json(value: Any) -> str:
    return json.dumps(canonicalize(value), ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest_text(text: str) -> str:
    return sha256(text.encode("utf-8")).hexdigest()


def digest_payload(value: Any) -> str:
    return digest_text(canonical_json(value))


def stable_id(prefix: str, *parts: Any, length: int = 16) -> str:
    payload = canonical_json(parts)
    return f"{prefix}-{digest_text(payload)[:length].upper()}"


def clamp(value: float, low: float = 0.0, high: float = 1.0) -> float:
    return max(low, min(high, value))


def maturity_index(maturity: str) -> int:
    try:
        return MATURITY_ORDER.index(maturity)
    except ValueError as exc:
        raise RuntimeContractError(f"Unknown maturity: {maturity}") from exc


def min_maturity(a: str, b: str) -> str:
    return MATURITY_ORDER[min(maturity_index(a), maturity_index(b))]


def max_maturity(a: str, b: str) -> str:
    return MATURITY_ORDER[max(maturity_index(a), maturity_index(b))]


def tokenize(value: Any) -> set[str]:
    """Extract conservative lexical tokens from arbitrary structured content."""
    if value is None:
        return set()
    if isinstance(value, Mapping):
        text = " ".join(str(v) for v in flatten_scalars(value))
    elif isinstance(value, (list, tuple, set)):
        text = " ".join(str(v) for v in flatten_scalars(value))
    else:
        text = str(value)
    result: set[str] = set()
    for match in TOKEN_RE.finditer(text.lower()):
        token = match.group(0).strip("_-")
        if len(token) < 3 or token in STOP_TOKENS:
            continue
        result.add(token)
    return result


def flatten_scalars(value: Any) -> Iterator[Any]:
    if isinstance(value, Mapping):
        for child in value.values():
            yield from flatten_scalars(child)
    elif isinstance(value, (list, tuple, set)):
        for child in value:
            yield from flatten_scalars(child)
    elif value is not None:
        yield value


def jaccard(a: Iterable[str], b: Iterable[str]) -> float:
    sa, sb = set(a), set(b)
    if not sa and not sb:
        return 1.0
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


def weighted_overlap(query: set[str], candidate: set[str]) -> float:
    if not query or not candidate:
        return 0.0
    intersection = query & candidate
    recall = len(intersection) / len(query)
    precision = len(intersection) / len(candidate)
    if recall + precision == 0:
        return 0.0
    f1 = 2 * recall * precision / (recall + precision)
    return clamp(0.65 * recall + 0.35 * f1)


def deep_get_ids(value: Any) -> set[str]:
    ids: set[str] = set()
    if isinstance(value, Mapping):
        for key, child in value.items():
            if key in ID_KEYS and isinstance(child, str) and child:
                ids.add(child)
            ids.update(deep_get_ids(child))
    elif isinstance(value, (list, tuple)):
        for child in value:
            ids.update(deep_get_ids(child))
    return ids


def first_identity(record: Mapping[str, Any]) -> str | None:
    for key in ID_KEYS:
        value = record.get(key)
        if isinstance(value, str) and value:
            return value
    return None


def record_text(record: Mapping[str, Any]) -> str:
    chunks: list[str] = []
    for key in TEXT_KEYS:
        value = record.get(key)
        if isinstance(value, str):
            chunks.append(value)
        elif isinstance(value, (dict, list)):
            chunks.extend(str(v) for v in flatten_scalars(value))
    return " ".join(chunks)


def walk_records(value: Any, path: tuple[Any, ...] = ()) -> Iterator[tuple[tuple[Any, ...], dict[str, Any]]]:
    """Yield dict records from arbitrary nested JSON without assuming layout."""
    if isinstance(value, dict):
        yield path, value
        for key, child in value.items():
            yield from walk_records(child, path + (key,))
    elif isinstance(value, list):
        for idx, child in enumerate(value):
            yield from walk_records(child, path + (idx,))


@dataclass(frozen=True)
class RegistryHit:
    object_id: str
    source_file: str
    json_path: tuple[Any, ...]
    score: float
    matched_tokens: tuple[str, ...]
    object_type: str
    record: dict[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class RegistryIndex:
    """Generic read-only index over Sourceborn JSON registries.

    The index intentionally does not infer canonicality from filename alone.  It
    stores the original source path and record, then callers decide whether a
    match is activation, evidence, provenance, or merely context.
    """

    def __init__(self) -> None:
        self._records: dict[str, tuple[str, tuple[Any, ...], dict[str, Any], set[str], str]] = {}

    @staticmethod
    def classify_id(object_id: str) -> str:
        prefix = object_id.upper()
        if prefix.startswith(("SB-ASI-P", "SB-HFR-P")):
            return "HUMAN_PARAMETER"
        if prefix.startswith("CON-"):
            return "HUMAN_CONTAINER"
        if prefix.startswith("SEG-"):
            return "HUMAN_SEGMENT"
        if prefix.startswith(("AI-NEW-", "AI-CAP-", "AI-CON-", "AI-")):
            return "AI_FUNCTION"
        if prefix.startswith(("WIS-", "W-BG-", "W-")):
            return "WISDOM_OBJECT"
        if prefix.startswith("ASI-NODE-"):
            return "ASI_NODE"
        if prefix.startswith("ASI-"):
            return "ASI_GOVERNANCE"
        if prefix.startswith("ENG-"):
            return "ENGINE"
        if prefix.startswith("R") and prefix[1:].isdigit():
            return "UNIVERSAL_RUBRIC"
        if prefix.startswith("PC-"):
            return "PATTERN"
        if prefix.startswith("INT-"):
            return "INTENT"
        if prefix.startswith("REL-"):
            return "RELATION"
        if prefix.startswith("PATH-"):
            return "PATH"
        return "OTHER"

    def add_document(self, source_file: str, document: Any) -> int:
        count = 0
        for path, record in walk_records(document):
            object_id = first_identity(record)
            if not object_id or object_id in self._records:
                continue
            tokens = tokenize(record_text(record)) | tokenize(object_id)
            self._records[object_id] = (
                source_file,
                path,
                record,
                tokens,
                self.classify_id(object_id),
            )
            count += 1
        return count

    def add_file(self, path: Path, *, root: Path | None = None) -> int:
        document = read_json(path)
        source = str(path.relative_to(root)) if root else str(path)
        return self.add_document(source, document)

    def get(self, object_id: str) -> RegistryHit | None:
        item = self._records.get(object_id)
        if item is None:
            return None
        source_file, path, record, _, object_type = item
        return RegistryHit(object_id, source_file, path, 1.0, tuple(), object_type, record)

    def search(
        self,
        query: Any,
        *,
        object_types: set[str] | None = None,
        min_score: float = 0.08,
        limit: int = 20,
    ) -> list[RegistryHit]:
        qtokens = tokenize(query)
        if not qtokens:
            return []
        hits: list[RegistryHit] = []
        for object_id, (source_file, path, record, tokens, object_type) in self._records.items():
            if object_types and object_type not in object_types:
                continue
            score = weighted_overlap(qtokens, tokens)
            if score < min_score:
                continue
            matched = tuple(sorted(qtokens & tokens))
            hits.append(RegistryHit(object_id, source_file, path, score, matched, object_type, record))
        hits.sort(key=lambda h: (-h.score, h.object_type, h.object_id))
        return hits[:limit]

    def ids(self) -> set[str]:
        return set(self._records)

    def __len__(self) -> int:
        return len(self._records)


def build_registry_index(root: Path, relative_paths: Sequence[str]) -> RegistryIndex:
    index = RegistryIndex()
    for relative in relative_paths:
        path = root / relative
        if path.exists() and path.suffix.lower() == ".json":
            index.add_file(path, root=root)
    return index


@dataclass
class TraceStep:
    trace_id: str
    engine_id: str
    operation: str
    input_refs: list[str] = field(default_factory=list)
    output_refs: list[str] = field(default_factory=list)
    rule_refs: list[str] = field(default_factory=list)
    status: str = "COMPLETE"
    epistemic_status: str = "STRUCTURAL_RUNTIME_TRACE"
    notes: list[str] = field(default_factory=list)
    created_at: str = field(default_factory=utc_now)

    @classmethod
    def create(
        cls,
        engine_id: str,
        operation: str,
        *,
        input_refs: Iterable[str] = (),
        output_refs: Iterable[str] = (),
        rule_refs: Iterable[str] = (),
        status: str = "COMPLETE",
        notes: Iterable[str] = (),
    ) -> "TraceStep":
        payload = {
            "engine_id": engine_id,
            "operation": operation,
            "input_refs": sorted(set(input_refs)),
            "output_refs": sorted(set(output_refs)),
            "rule_refs": sorted(set(rule_refs)),
            "status": status,
            "notes": list(notes),
        }
        return cls(
            trace_id=stable_id("TRACE", payload),
            engine_id=engine_id,
            operation=operation,
            input_refs=payload["input_refs"],
            output_refs=payload["output_refs"],
            rule_refs=payload["rule_refs"],
            status=status,
            notes=payload["notes"],
        )

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


@dataclass
class EngineResult:
    engine_id: str
    status: str
    payload: dict[str, Any]
    traces: list[TraceStep] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    errors: list[str] = field(default_factory=list)

    @property
    def ok(self) -> bool:
        return self.status in {"PASS", "COMPLETE", "PARTIAL"} and not self.errors

    def to_dict(self) -> dict[str, Any]:
        return {
            "engine_id": self.engine_id,
            "status": self.status,
            "payload": canonicalize(self.payload),
            "traces": [t.to_dict() for t in self.traces],
            "warnings": list(self.warnings),
            "errors": list(self.errors),
        }


def require_fields(record: Mapping[str, Any], fields: Iterable[str], label: str) -> None:
    missing = [field for field in fields if field not in record or record[field] in (None, "")]
    if missing:
        raise RuntimeContractError(f"{label} missing required fields: {missing}")


def ensure_point_zero_locked(event: Mapping[str, Any]) -> None:
    point_zero = event.get("point_zero")
    if not isinstance(point_zero, Mapping):
        raise SourceBoundaryError("Event has no Point Zero object")
    if point_zero.get("status") not in {"LOCKED", "DECLARED", "LOCAL"}:
        raise SourceBoundaryError(f"Point Zero is not usable: {point_zero.get('status')}")
    source_refs = event.get("source_refs")
    if not isinstance(source_refs, list) or not source_refs:
        raise SourceBoundaryError("Event has no source references")


def source_independence_groups(evidence_records: Iterable[Mapping[str, Any]]) -> set[str]:
    groups: set[str] = set()
    for evidence in evidence_records:
        group = evidence.get("source_independence_group") or evidence.get("source_independence_group_ref")
        if isinstance(group, str) and group:
            groups.add(group)
    return groups


def evidence_strength(evidence_records: Iterable[Mapping[str, Any]]) -> float:
    """Conservative evidence score based on independent groups, not repetitions."""
    records = list(evidence_records)
    if not records:
        return 0.0
    groups = source_independence_groups(records)
    supported = sum(1 for r in records if str(r.get("result", r.get("status", ""))).upper() in {"PASS", "SUPPORTS", "SUPPORTED", "CONFIRMED"})
    direct = sum(1 for r in records if str(r.get("epistemic_status", "")).upper() in {"OBSERVED", "DIRECT_SOURCE", "SOURCE_STATED"})
    group_factor = 1.0 - math.exp(-0.55 * max(1, len(groups)))
    direct_factor = clamp(direct / max(1, len(records)))
    support_factor = clamp(supported / max(1, len(records)))
    return clamp(0.45 * group_factor + 0.30 * direct_factor + 0.25 * support_factor)


def read_json(path: Path) -> Any:
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8") as handle:
        json.dump(canonicalize(value), handle, ensure_ascii=False, indent=2)
        handle.write("\n")


def load_json_if_exists(path: Path, default: Any = None) -> Any:
    if not path.exists():
        return default
    return read_json(path)


def merge_unique(existing: Iterable[str], additions: Iterable[str]) -> list[str]:
    return sorted(set(existing) | set(additions))


def copy_record(value: Mapping[str, Any]) -> dict[str, Any]:
    """Deep copy through canonical JSON, ensuring JSON-only runtime state."""
    return json.loads(json.dumps(value, ensure_ascii=False))
