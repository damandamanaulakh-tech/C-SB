#!/usr/bin/env python3
from pathlib import Path
import json, re

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "generated" / "registry_views"
OUT.mkdir(parents=True, exist_ok=True)

# ------------------------------------------------------------------
# AI review map -> machine-readable JSON
# ------------------------------------------------------------------
ai_md = ROOT / "raw" / "rubrics" / "AI_CAPABILITY_TO_SOURCEBORN_CONTAINERS_REVIEW.md"
ai_rows = []
if ai_md.exists():
    for line in ai_md.read_text(encoding="utf-8").splitlines():
        if not line.startswith("| AI-CAP-"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) != 4:
            continue
        cap_id, family, primary, secondary = cells
        ai_rows.append({
            "capability_id": cap_id,
            "capability_family": family,
            "primary_mapping_text": primary,
            "secondary_mapping_text": secondary,
            "container_refs": sorted(set(re.findall(r"CON-\d{3}", primary + " " + secondary))),
            "approval_status": "REVIEW_ONLY",
            "source_file": str(ai_md.relative_to(ROOT))
        })

(OUT / "ai_capability_review_map.json").write_text(json.dumps({
    "status": "REVIEW_ONLY",
    "count": len(ai_rows),
    "items": ai_rows
}, indent=2, ensure_ascii=False), encoding="utf-8")

# ------------------------------------------------------------------
# ASI node registry -> service view
# ------------------------------------------------------------------
asi_path = ROOT / "registries" / "asi" / "asi_node_registry.json"
asi = json.loads(asi_path.read_text(encoding="utf-8")) if asi_path.exists() else {"nodes": []}

# Human adoption readiness
human_contract_path = ROOT / "registries" / "human" / "HUMAN_REGISTRY_ADOPTION_CONTRACT.json"
human_contract = json.loads(human_contract_path.read_text(encoding="utf-8")) if human_contract_path.exists() else {}
native_dir = ROOT / "registries" / "human" / "native"
human_native_files = sorted(str(p.relative_to(ROOT)) for p in native_dir.rglob("*") if p.is_file()) if native_dir.exists() else []

summary = {
    "ai": {
        "status": "REVIEW_ONLY",
        "capability_family_count": len(ai_rows),
        "machine_view": str((OUT / "ai_capability_review_map.json").relative_to(ROOT))
    },
    "human": {
        "locked_shape": human_contract.get("locked_shape"),
        "native_files_present": human_native_files,
        "ready_for_full_parameter_relink": bool(human_native_files)
    },
    "asi": {
        "service_node_count": len(asi.get("nodes", [])),
        "node_ids": [n.get("asi_node_id") for n in asi.get("nodes", [])]
    }
}
(OUT / "registry_readiness.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

md = ["# Generated Registry Readiness", "", f"- AI review families: **{len(ai_rows)}** (REVIEW ONLY)", f"- ASI service nodes: **{len(asi.get('nodes', []))}**", f"- Human locked shape: **{human_contract.get('locked_shape')}**", f"- Human native files present: **{len(human_native_files)}**", ""]
if not human_native_files:
    md += ["> Full Human parameter relinking is intentionally blocked until the approved native 2,560-row source is present. No rows are invented.", ""]
(OUT / "REGISTRY_READINESS.md").write_text("\n".join(md), encoding="utf-8")
print(f"AI review rows parsed: {len(ai_rows)}; ASI nodes: {len(asi.get('nodes', []))}; Human native files: {len(human_native_files)}")
