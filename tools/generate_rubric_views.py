#!/usr/bin/env python3
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "generated" / "rubrics"
OUT.mkdir(parents=True, exist_ok=True)

registry = json.loads((ROOT / "machine/rubrics/RUBRIC_REGISTRY_R01_R52.json").read_text(encoding="utf-8"))
bindings = json.loads((ROOT / "machine/rubrics/RUBRIC_PACK_ASI_NODE_BINDINGS_v0.json").read_text(encoding="utf-8"))["bindings"]

rubric_to_pack = {}
for pack, ids in registry["packs"].items():
    for rid in ids:
        rubric_to_pack[rid] = pack

pack_node_map = {}
for pack, b in bindings.items():
    pack_node_map[pack] = {
        "primary_asi_nodes": b["primary_asi_nodes"],
        "secondary_asi_nodes": b["secondary_asi_nodes"]
    }

rows = []
for rid in sorted(registry["rubrics"]):
    spec = registry["rubrics"][rid]
    pack = rubric_to_pack[rid]
    rows.append({
        "rubric_id": rid,
        "rubric_name": spec["name"],
        "dimension_count": len(spec["dimensions"]),
        "dimensions": spec["dimensions"],
        "pack": pack,
        **pack_node_map[pack]
    })

(OUT / "rubric_dimension_index.json").write_text(json.dumps({
    "rubric_count": len(rows),
    "dimension_count": sum(r["dimension_count"] for r in rows),
    "status": registry["status"],
    "items": rows
}, indent=2, ensure_ascii=False), encoding="utf-8")

node_to_packs = {}
for pack, b in bindings.items():
    for nid in b["primary_asi_nodes"]:
        node_to_packs.setdefault(nid, {"primary": [], "secondary": []})["primary"].append(pack)
    for nid in b["secondary_asi_nodes"]:
        node_to_packs.setdefault(nid, {"primary": [], "secondary": []})["secondary"].append(pack)
(OUT / "asi_node_rubric_pack_index.json").write_text(json.dumps(node_to_packs, indent=2), encoding="utf-8")

md = ["# Universal Sequence V2 — Rubric Index", "", f"- Rubric families: **{len(rows)}**", f"- Total splitter dimensions: **{sum(r['dimension_count'] for r in rows)}**", f"- Registry status: `{registry['status']}`", "", "| Rubric | Name | Dimensions | Pack | Primary ASI Nodes |", "|---|---|---:|---|---|"]
for r in rows:
    md.append(f"| {r['rubric_id']} | {r['rubric_name']} | {r['dimension_count']} | {r['pack']} | {', '.join(r['primary_asi_nodes'])} |")
md += ["", "> Rubric-to-ASI bindings are Phase-2 mapping proposals. They do not change source rubric definitions or impose a chronological node order.", ""]
(OUT / "RUBRIC_INDEX.md").write_text("\n".join(md), encoding="utf-8")

print(f"rubrics={len(rows)} dimensions={sum(r['dimension_count'] for r in rows)} packs={len(registry['packs'])}")
