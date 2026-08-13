#!/usr/bin/env python3
from pathlib import Path
import base64, csv, gzip, hashlib, io, json

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "registries/human/HUMAN_FUNCTIONAL_REGISTRY_3204_V1.json"
OUT_DIR = ROOT / "generated/registry_views"
OUT_DIR.mkdir(parents=True, exist_ok=True)

manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
payload_path = ROOT / manifest["source_payload"]["path"]
encoded = "".join(payload_path.read_text(encoding="utf-8").split())
gz_bytes = base64.b64decode(encoded)
if hashlib.sha256(gz_bytes).hexdigest() != manifest["source_payload"]["gzip_sha256"]:
    raise SystemExit("HFR3204 gzip SHA mismatch")
tsv_bytes = gzip.decompress(gz_bytes)
if hashlib.sha256(tsv_bytes).hexdigest() != manifest["source_payload"]["tsv_sha256"]:
    raise SystemExit("HFR3204 TSV SHA mismatch")

text = tsv_bytes.decode("utf-8")
rows = list(csv.DictReader(io.StringIO(text), delimiter="\t"))
expected_columns = [
    "parameter_id","segment_id","segment_name","container_id",
    "container_name","container_local_ordinal","name"
]
if not rows or list(rows[0].keys()) != expected_columns:
    raise SystemExit(f"HFR3204 columns mismatch: {list(rows[0].keys()) if rows else 'NO_ROWS'}")
if len(rows) != 3204:
    raise SystemExit(f"HFR3204 row count mismatch: {len(rows)}")

expected_ids = [f"SB-HFR-P{i:04d}" for i in range(1, 3205)]
actual_ids = [r["parameter_id"] for r in rows]
if actual_ids != expected_ids:
    raise SystemExit("HFR3204 parameter IDs are not exact contiguous SB-HFR-P0001..P3204")

segment_counts = {}
container_counts = {}
container_names = {}
for r in rows:
    segment_counts[r["segment_id"]] = segment_counts.get(r["segment_id"], 0) + 1
    container_counts[r["container_id"]] = container_counts.get(r["container_id"], 0) + 1
    container_names[r["container_id"]] = r["container_name"]

expected_segment_counts = {
    f"SEG-{i:02d}": n for i, n in enumerate(manifest["shape"]["segment_parameter_counts"], start=1)
}
if segment_counts != expected_segment_counts:
    raise SystemExit(f"HFR3204 segment counts mismatch: {segment_counts}")
if len(container_counts) != 80:
    raise SystemExit(f"HFR3204 container count mismatch: {len(container_counts)}")
if container_counts.get("CON-042") != 42 or container_counts.get("CON-057") != 42:
    raise SystemExit("HFR3204 42-item source containers do not match CON-042/CON-057")
for cid, count in container_counts.items():
    if cid not in {"CON-042", "CON-057"} and count != 40:
        raise SystemExit(f"HFR3204 unexpected container count {cid}={count}")

legacy_index = json.loads((ROOT / manifest["legacy_baseline"]["container_index"]).read_text(encoding="utf-8"))
legacy = {}
for seg in legacy_index["segments"]:
    for cid, name, count in seg["containers"]:
        legacy[cid] = {"name": name, "count": int(count), "segment_id": seg["segment_id"]}
if len(legacy) != 80 or sum(x["count"] for x in legacy.values()) != 2560:
    raise SystemExit("Legacy 2560 container index no longer matches locked baseline")

reconciliation = []
for cid in sorted(container_counts):
    old = legacy[cid]
    if old["name"] != container_names[cid]:
        raise SystemExit(f"Container name drift: {cid}: {old['name']} != {container_names[cid]}")
    delta = container_counts[cid] - old["count"]
    reconciliation.append({
        "container_id": cid,
        "container_name": container_names[cid],
        "segment_id": old["segment_id"],
        "legacy_count": old["count"],
        "v1_count": container_counts[cid],
        "delta": delta,
        "version_relation": "GROWN" if delta > 0 else "UNCHANGED" if delta == 0 else "CONTRACTED_SOURCE_VERSION"
    })

registry = {
    "registry_id": manifest["registry_id"],
    "status": manifest["status"],
    "shape": manifest["shape"],
    "legacy_baseline": manifest["legacy_baseline"],
    "identity_policy": manifest["identity_policy"],
    "runtime_owner_policy": manifest["runtime_owner_policy"],
    "source_documents": manifest["source_documents"],
    "parameters": [
        {
            **r,
            "container_local_ordinal": int(r["container_local_ordinal"]),
            "runtime_owner_status": "UNCLASSIFIED_PENDING_P2_HUMAN_3204_RUNTIME_OWNER_RECLASSIFICATION",
            "legacy_atomic_alias_status": "NOT_INFERRED"
        } for r in rows
    ]
}
summary = {
    "registry_id": manifest["registry_id"],
    "parameter_count": len(rows),
    "legacy_count": 2560,
    "net_count_change": len(rows) - 2560,
    "segments": segment_counts,
    "containers": reconciliation,
    "grown_containers": sum(1 for x in reconciliation if x["delta"] > 0),
    "unchanged_containers": sum(1 for x in reconciliation if x["delta"] == 0),
    "contracted_source_version_containers": [x for x in reconciliation if x["delta"] < 0],
    "scaffolds_counted_as_parameters": False
}

(OUT_DIR / "human_functional_3204_registry_v1.json").write_text(
    json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8"
)
(OUT_DIR / "human_functional_3204_summary_v1.json").write_text(
    json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8"
)
print("Materialized HFR v1:", len(rows), "parameters; net +", len(rows)-2560)
