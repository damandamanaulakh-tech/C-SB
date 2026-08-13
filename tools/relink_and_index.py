#!/usr/bin/env python3
from pathlib import Path
import re, json, hashlib

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "generated"
OUT.mkdir(exist_ok=True)

PATTERNS = {
    "segments": re.compile(r"\bSEG-\d{2}\b"),
    "containers": re.compile(r"\bCON-\d{3}\b"),
    "sourceborn_parameters": re.compile(r"\bSB-ASI-P\d{4}\b"),
    "human_functional_v1_parameters": re.compile(r"\bSB-HFR-P\d{4}\b"),
    "human_functional_parameter_candidates": re.compile(r"\bHFP-KP-\d{3}\b"),
    "king_profile_reasoning_candidates": re.compile(r"\bRC-KP-\d{3}\b"),
    "egypt_domain_parameter_candidates": re.compile(r"\bEG-KP-\d{3}\b"),
    "human_combinations": re.compile(r"\bH-COMB-\d{2}\b"),
    "legacy_ai_capabilities": re.compile(r"\bAI-CAP-\d{3}\b"),
    "approved_ai_only_records": re.compile(r"\bAI-NEW-\d{3}\b"),
    "ai_rubric_segments": re.compile(r"\bAI-\d{2}\b"),
    "ai_container_candidates": re.compile(r"\bAI-CON-CAND-\d{3}\b"),
    "wisdom_lanes": re.compile(r"\bW-\d{2}\b"),
    "wisdom_source_batches": re.compile(r"\bWIS-SRC-BATCH-\d{3}\b"),
    "wisdom_source_text_ids": re.compile(r"\bWST-\d{3}\b"),
    "wisdom_source_claim_ids": re.compile(r"\bWSC-\d{3}\b"),
    "wisdom_interpretation_ids": re.compile(r"\bWINT-\d{3}\b"),
    "wisdom_sequence_ids": re.compile(r"\bWSEQ-\d{3}\b"),
    "wisdom_candidate_ids": re.compile(r"\bWIS-CAND-\d{3}\b"),
    "asi_rubric_segments": re.compile(r"\bASI-\d{2}\b"),
    "asi_container_candidates": re.compile(r"\bASI-CON-CAND-\d{3}\b"),
    "asi_nodes": re.compile(r"\bASI-NODE-\d{2}\b"),
    "node_brains": re.compile(r"\bNB-\d{2}\b"),
    "engine_ids": re.compile(r"\bENG-[A-Z0-9]+-\d{3}\b"),
    "activation_rule_ids": re.compile(r"\bACT-\d{3}\b"),
    "operational_element_codes": re.compile(r"\bE0[1-8]\b"),
    "governance_control_ids": re.compile(r"\bGOV-\d{3}\b"),
    "rubric_registry_ids": re.compile(r"\b(?:AI-RUBRIC-V\d+|ASI-RUBRIC-V\d+|WISDOM-REGISTRY-V\d+)\b"),
    "micro_sequence_runtime_stages": re.compile(r"\bMS-\d{2}\b"),
    "rubric_microscope_panels": re.compile(r"\bRM-\d{2}\b"),
    "micro_pattern_test_sequences": re.compile(r"\bSYN-MICRO-S\d+\b"),
    "pattern_candidate_ids": re.compile(r"\b(?:PATTERN-CANDIDATE|PAT-CAND|P-CAND)-[A-Z0-9-]+\b"),
    "intent_signal_ids": re.compile(r"\bINT-SIG-[A-Z0-9]+\b"),
    "intent_candidate_ids": re.compile(r"\bINT-CAND-[A-Z0-9]+\b"),
    "intent_contribution_ids": re.compile(r"\bINT-CONTRIB-[A-Z0-9]+\b"),
    "rubric_review_ids": re.compile(r"\b(?:REVIEW|RUBRIC-REVIEW)-[A-Z0-9-]+\b"),
    "learning_writeback_ids": re.compile(r"\b(?:WRITEBACK|LEARN-WB)-[A-Z0-9-]+\b"),
    "semantic_clarification_ids": re.compile(r"\bSC-[A-Z0-9-]+\b"),
    "dimensional_return_ids": re.compile(r"\bDR-[A-Z0-9-]+\b"),
    "human_rubric_change_candidate_ids": re.compile(r"\bHRC-[A-Z0-9-]+\b"),
    "semantic_correction_test_sequences": re.compile(r"\bSEQ-SEM-[A-Z0-9-]+\b"),
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

hfr_generated = ROOT / "generated/registry_views/human_functional_3204_registry_v1.json"
if hfr_generated.exists():
    text = hfr_generated.read_text(encoding="utf-8")
    rel = str(hfr_generated.relative_to(ROOT))
    kind = "human_functional_v1_parameters"
    for ident in sorted(set(PATTERNS[kind].findall(text))):
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
