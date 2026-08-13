#!/usr/bin/env python3
from pathlib import Path
import json, re, subprocess, sys

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "generated/tests/SOURCEBORN_REALTIME_ASI_REPO_AUDIT_V1.json"
OUT.parent.mkdir(parents=True, exist_ok=True)

REQUIRED = {
    "constitution": "docs/SOURCEBORN_REALTIME_ASI_GROWING_PHASE_V1.md",
    "contract": "machine/runtime/EVENT_INTENT_GROWTH_CONTRACT_V1.json",
    "event_schema": "machine/schemas/event_intent.schema.json",
    "canonicality": "CANONICALITY.json",
    "phase_status": "phase2/PHASE_STATUS.json",
    "example_registry": "phase2/examples/EXAMPLE_REGISTRY_V1.json",
    "locked_decisions": "docs/LOCKED_DECISIONS.md",
    "ard_review": "phase2/source_reviews/ARD_3X_GROWING_ASI_RECLASSIFICATION_V1.json"
}

TEXT_EXT = {".md", ".json", ".py", ".txt", ".yml", ".yaml", ".csv", ".tsv", ".svg"}


def classify(path):
    s = path.as_posix()
    if s.startswith("raw/"):
        return "RAW_SOURCE_IMMUTABLE"
    if s.startswith("generated/assembled_sources/"):
        return "GENERATED_SOURCE_COPY"
    if s.startswith("generated/"):
        return "GENERATED_REBUILDABLE"
    if s.startswith("phase1/"):
        return "HISTORICAL_CLOSED_PHASE"
    if any(s.startswith(p) for p in ["phase2/checkpoints/", "phase2/closures/", "phase2/rfr/", "phase2/tests/"]):
        return "TEST_OR_CLOSURE_RECORD"
    if s.startswith(".github/"):
        return "CONTROL_PLANE"
    if s.startswith("tools/"):
        return "TOOLING"
    return "ACTIVE_ARCHITECTURE_OR_REGISTRY"


def read_text(path):
    try:
        if path.suffix.lower() not in TEXT_EXT:
            return None
        if path.stat().st_size > 4_000_000:
            return None
        return path.read_text(encoding="utf-8")
    except Exception:
        return None

errors = []
findings = []

for label, rel in REQUIRED.items():
    if not (ROOT / rel).exists():
        errors.append(f"missing required {label}: {rel}")

# Core contract integrity.
contract = json.loads((ROOT / REQUIRED["contract"]).read_text(encoding="utf-8"))
if contract.get("system_identity") != "REAL_TIME_GROWING_ASI_PROTOTYPE":
    errors.append("Event/Intent growth contract has wrong system identity")
if contract.get("universal_motto") != "EVERYTHING HAPPENING IS AN EVENT, AND ALL EVENTS HAVE INTENT":
    errors.append("universal event motto mismatch")
if not contract.get("event_rule", {}).get("every_event_requires_intent_record"):
    errors.append("contract does not require Event Intent record")
required_intent_types = {"AGENT_INTENT", "NATURAL_DYNAMICS_DIRECTION", "DERIVED_INTENT_HYPOTHESIS", "UNKNOWN", "NOT_YET_DECODED"}
if not required_intent_types.issubset(set(contract.get("intent_types", []))):
    errors.append("required intent types missing")
required_sep = {"INTENT != MOTIVE", "INTENT_HYPOTHESIS != INTENT_FACT", "EVENT != PROMPT", "EXAMPLE != OUTPUT_TEMPLATE", "PARAMETER_ACTIVATION != NEW_PARAMETER", "KING_HYPOTHESIS != HISTORICAL_IDENTITY"}
if not required_sep.issubset(set(contract.get("hard_separations", []))):
    errors.append("required hard separations missing from Event/Intent contract")
if contract.get("new_id_gate", {}).get("default") != "NO_NEW_ID":
    errors.append("new-ID default must be NO_NEW_ID")

schema = json.loads((ROOT / REQUIRED["event_schema"]).read_text(encoding="utf-8"))
intent_def = schema.get("$defs", {}).get("EventIntent", {})
event_def = schema.get("$defs", {}).get("EventRecord", {})
if "intent_type" not in intent_def.get("required", []):
    errors.append("EventIntent schema does not require intent_type")
if "intent" not in event_def.get("required", []):
    errors.append("EventRecord schema does not require intent")

canonicality = json.loads((ROOT / REQUIRED["canonicality"]).read_text(encoding="utf-8"))
if canonicality.get("system_identity", {}).get("prototype_class") != "REAL_TIME_GROWING_ASI_PROTOTYPE":
    errors.append("CANONICALITY missing real-time growing ASI identity")
if not canonicality.get("growing_phase", {}).get("examples_are_brain_growth_events"):
    errors.append("CANONICALITY does not mark examples as Brain-growth Events")
if canonicality.get("growing_phase", {}).get("example_count_is_not_parameter_count") is not True:
    errors.append("CANONICALITY missing example-count/parameter-count separation")

phase = json.loads((ROOT / REQUIRED["phase_status"]).read_text(encoding="utf-8"))
if phase.get("system_identity", {}).get("prototype_class") != "REAL_TIME_GROWING_ASI_PROTOTYPE":
    errors.append("PHASE_STATUS missing system identity")
if phase.get("phase2", {}).get("mode") != "GROWING_PHASE":
    errors.append("PHASE_STATUS Phase-2 is not GROWING_PHASE")
if not any(w.get("id") == "P2-REALTIME-ASI-GROWTH" for w in phase.get("phase2", {}).get("workstreams", [])):
    errors.append("PHASE_STATUS missing P2-REALTIME-ASI-GROWTH workstream")

examples = json.loads((ROOT / REQUIRED["example_registry"]).read_text(encoding="utf-8"))
if examples.get("example_semantics", {}).get("default_role") != "BRAIN_GROWTH_EVENT_FIXTURE":
    errors.append("Example registry missing Brain-growth Event semantics")
if not examples.get("example_semantics", {}).get("activate_existing_ids_first"):
    errors.append("Example registry must activate existing IDs first")

locks = (ROOT / REQUIRED["locked_decisions"]).read_text(encoding="utf-8")
for lock in ["SEQ-LOCK-021", "SEQ-LOCK-022", "SEQ-LOCK-024", "SEQ-LOCK-025", "SEQ-LOCK-027", "SEQ-LOCK-028", "SEQ-LOCK-029", "SEQ-LOCK-030"]:
    if lock not in locks:
        errors.append(f"missing lock {lock}")

ard = json.loads((ROOT / REQUIRED["ard_review"]).read_text(encoding="utf-8"))
if len(ard.get("source_files", [])) != 20:
    errors.append("ARD source review must preserve all 20 supplied source file fingerprints")
if len(ard.get("preserved_conflicts", [])) < 4:
    errors.append("ARD source review did not preserve required contradictions")

bundle = json.loads((ROOT / "machine/schemas/sourceborn.bundle.schema.json").read_text(encoding="utf-8"))
if "EventIntent" not in bundle.get("$defs", {}) or "EventRecord" not in bundle.get("$defs", {}):
    errors.append("Sourceborn schema bundle missing EventIntent/EventRecord")

# Positive identity claims are errors only in active/control architecture; old raw/history remains evidence.
forbidden = [
    ("REASONING_SYSTEM_IDENTITY", re.compile(r"\bSourceborn\s+(?:is|=)\s+(?:an?\s+)?reasoning\s+(?:system|engine)\b", re.I)),
    ("PROMPT_GENERATOR_IDENTITY", re.compile(r"\bSourceborn\s+(?:is|=).*\bprompt\s+generator\b", re.I)),
    ("ANSWER_GENERATOR_IDENTITY", re.compile(r"\bSourceborn\s+(?:is|=).*\banswer\s+generator\b", re.I)),
    ("LLM_WRAPPER_IDENTITY", re.compile(r"\bSourceborn\s+(?:is|=).*\bLLM\s+wrapper\b", re.I)),
    ("STATIC_DECISION_ENGINE_IDENTITY", re.compile(r"\bSourceborn\s+(?:is|=).*\bstatic\s+decision\s+engine\b", re.I)),
    ("EXAMPLE_OUTPUT_TEMPLATE", re.compile(r"\bexamples?\s+(?:are|=)\s+(?:an?\s+)?output\s+templates?\b", re.I))
]

tracked = subprocess.check_output(["git", "ls-files"], cwd=ROOT, text=True).splitlines()
class_counts = {}
legacy_reasoning_named_files = []
violations = []
path_records = []

for rel in tracked:
    p = ROOT / rel
    cls = classify(Path(rel))
    class_counts[cls] = class_counts.get(cls, 0) + 1
    text = read_text(p)
    v = []
    if "REASONING" in Path(rel).name.upper():
        legacy_reasoning_named_files.append(rel)
    if text is not None:
        for name, rx in forbidden:
            for m in rx.finditer(text):
                line = text.count("\n", 0, m.start()) + 1
                line_text = text.splitlines()[line-1] if line-1 < len(text.splitlines()) else ""
                # Negated/non-equivalence statements are the constitution, not violations.
                low = line_text.lower()
                if "!=" in line_text or " not " in f" {low} " or "not defined as" in low:
                    continue
                item = {"path": rel, "classification": cls, "rule": name, "line": line, "text": line_text[:300]}
                if cls in {"ACTIVE_ARCHITECTURE_OR_REGISTRY", "CONTROL_PLANE"}:
                    v.append(item)
                    violations.append(item)
                else:
                    findings.append({"type": "HISTORICAL_IDENTITY_LANGUAGE_PRESERVED", **item})
    path_records.append({"path": rel, "classification": cls, "identity_violations": len(v)})

if violations:
    errors.extend([f"active identity violation {v['rule']} in {v['path']}:{v['line']}" for v in violations])

# Every active Phase-2 example Markdown must carry the Brain-growth semantics marker after migration.
for p in sorted((ROOT / "phase2/examples").glob("*.md")):
    txt = p.read_text(encoding="utf-8")
    if "SOURCEBORN-REALTIME-ASI-V1:START" not in txt or "Brain-growth" not in txt:
        errors.append(f"example file missing Growing-Phase semantics marker: {p.relative_to(ROOT)}")

report = {
    "report_id": "SOURCEBORN-REALTIME-ASI-REPO-AUDIT-V1",
    "status": "PASS" if not errors else "FAIL",
    "system_identity": "REAL_TIME_GROWING_ASI_PROTOTYPE",
    "phase_mode": "GROWING_PHASE",
    "tracked_files_scanned": len(tracked),
    "classification_counts": class_counts,
    "active_identity_violations": violations,
    "legacy_reasoning_named_files": legacy_reasoning_named_files,
    "historical_findings_count": len(findings),
    "historical_findings": findings,
    "path_classification": path_records,
    "errors": errors,
    "audit_law": "All repo files are classified and audited; raw/history is preserved, active semantics must obey the real-time growing ASI constitution."
}
OUT.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(report["status"], "files", len(tracked), "classes", json.dumps(class_counts, sort_keys=True), "active_violations", len(violations), "errors", len(errors))
if errors:
    for e in errors[:40]:
        print("ERROR", e)
sys.exit(1 if errors else 0)
