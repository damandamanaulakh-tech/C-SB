#!/usr/bin/env python3
from pathlib import Path
import re, json, hashlib

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "generated"
OUT.mkdir(exist_ok=True)

PATTERNS = {
    "segments": re.compile(r"\bSEG-\d{2}\b"),
    "containers": re.compile(r"\bCON-\d{3}\b"),
    "human_parameters": re.compile(r"\bSB-ASI-P\d{4}\b"),
    "ai_capabilities": re.compile(r"\bAI-CAP-\d{3}\b"),
    "asi_nodes": re.compile(r"\bASI-NODE-\d{2}\b"),
    "human_combinations": re.compile(r"\bH-COMB-\d{2}\b"),
}

TEXT_EXTS = {".md", ".txt", ".json", ".yaml", ".yml", ".svg", ".py"}

files = []
for p in ROOT.rglob("*"):
    if not p.is_file() or ".git" in p.parts or "generated" in p.parts:
        continue
    rel = str(p.relative_to(ROOT))
    sha = hashlib.sha256(p.read_bytes()).hexdigest()
    files.append({"path": rel, "sha256": sha, "size_bytes": p.stat().st_size})

refs = {k: {} for k in PATTERNS}
for p in ROOT.rglob("*"):
    if not p.is_file() or p.suffix.lower() not in TEXT_EXTS or "generated" in p.parts:
        continue
    try:
        text = p.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        continue
    rel = str(p.relative_to(ROOT))
    for kind, rx in PATTERNS.items():
        for ident in sorted(set(rx.findall(text))):
            refs[kind].setdefault(ident, []).append(rel)

for kind in refs:
    for ident in refs[kind]:
        refs[kind][ident] = sorted(set(refs[kind][ident]))

(OUT / "reference_index.json").write_text(json.dumps(refs, indent=2), encoding="utf-8")
(OUT / "file_manifest.json").write_text(json.dumps(files, indent=2), encoding="utf-8")

lines = ["# Generated Cross-Reference Index", ""]
for kind, items in refs.items():
    lines += [f"## {kind.replace('_',' ').title()}", ""]
    if not items:
        lines += ["_No IDs currently present._", ""]
        continue
    for ident, paths in sorted(items.items()):
        lines.append(f"- **{ident}** → " + ", ".join(f"`{x}`" for x in paths))
    lines.append("")
(OUT / "REFERENCE_INDEX.md").write_text("\n".join(lines), encoding="utf-8")
print("Generated:", OUT / "reference_index.json", OUT / "file_manifest.json", OUT / "REFERENCE_INDEX.md")
