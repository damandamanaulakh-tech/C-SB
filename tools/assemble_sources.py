#!/usr/bin/env python3
from pathlib import Path
import json, hashlib

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "generated" / "assembled_sources"
OUT.mkdir(parents=True, exist_ok=True)

reports = []
for manifest_path in sorted(ROOT.rglob("*.manifest.json")):
    if "generated" in manifest_path.parts:
        continue
    data = json.loads(manifest_path.read_text(encoding="utf-8"))
    parts = data.get("parts_in_order")
    source_file = data.get("source_file")
    if not parts or not source_file:
        continue
    base = manifest_path.parent
    content = ""
    missing = []
    for rel in parts:
        p = base / rel
        if not p.exists():
            missing.append(str(p.relative_to(ROOT)))
            continue
        content += p.read_text(encoding="utf-8")
    out = OUT / Path(source_file).name
    out.write_text(content, encoding="utf-8")
    digest = hashlib.sha256(out.read_bytes()).hexdigest()
    expected = data.get("sha256")
    reports.append({
        "manifest": str(manifest_path.relative_to(ROOT)),
        "source_file": source_file,
        "assembled_path": str(out.relative_to(ROOT)),
        "missing_parts": missing,
        "sha256": digest,
        "expected_sha256": expected,
        "hash_match": None if not expected else digest == expected,
        "note": data.get("note")
    })

(ROOT / "generated").mkdir(exist_ok=True)
(ROOT / "generated" / "assembly_report.json").write_text(json.dumps(reports, indent=2), encoding="utf-8")

md = ["# Assembled Source Report", ""]
for r in reports:
    md += [f"## {r['source_file']}", "", f"- Manifest: `{r['manifest']}`", f"- Assembled: `{r['assembled_path']}`", f"- SHA-256: `{r['sha256']}`", f"- Expected: `{r['expected_sha256']}`", f"- Hash match: `{r['hash_match']}`", f"- Missing parts: `{r['missing_parts']}`", ""]
(ROOT / "generated" / "ASSEMBLY_REPORT.md").write_text("\n".join(md), encoding="utf-8")
print(f"assembled {len(reports)} manifest-backed sources")
