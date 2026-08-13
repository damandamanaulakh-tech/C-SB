#!/usr/bin/env python3
from pathlib import Path
import json, re

ROOT = Path(__file__).resolve().parents[1]
CONSTITUTION = "docs/SOURCEBORN_REALTIME_ASI_GROWING_PHASE_V1.md"
CONTRACT = "machine/runtime/EVENT_INTENT_GROWTH_CONTRACT_V1.json"

START = "<!-- SOURCEBORN-REALTIME-ASI-V1:START -->"
END = "<!-- SOURCEBORN-REALTIME-ASI-V1:END -->"

IDENTITY_BLOCK = f"""{START}

> **Sourceborn identity:** real-time growing Artificial Super Intelligence prototype. Reasoning, planning, prediction, retrieval, simulation, verification and communication are internal capabilities; none defines the whole system. Phase-2 is the **Growing Phase**: every example/event activates the existing Brain, tests relations + typed intent + combinations, and may create reviewed/versioned new memory, patterns, combinations or IDs only when a genuinely new reusable construct survives its gate. Canonical direction: `{CONSTITUTION}`. Runtime law: `{CONTRACT}`.

> **Universal event law:** **EVERYTHING HAPPENING IS AN EVENT, AND ALL EVENTS HAVE INTENT.** Intent is typed; `AGENT_INTENT != MOTIVE`, and `NATURAL_DYNAMICS_DIRECTION` does not imply conscious agency. `UNKNOWN` is preferred over fabricated intent.

{END}"""

EXAMPLE_BLOCK = f"""{START}

> **Growing-Phase example semantics:** this file is a **Brain-growth event fixture**, not an answer template and not a demonstration that Sourceborn is a reasoning/prompt engine. The event activates existing IDs and may produce relation, intent, interpretation, pattern, memory, combination or new-ID candidates. A new parameter/ID is created only after the required source boundary, review and R-F-R gate. Older filenames containing `REASONING` are retained as provenance labels only. See `{CONSTITUTION}`.

{END}"""

KING_BLOCK = f"""{START}

> **Tablet-event target:** King/queen/priest/workshop profiles are parallel, testable **candidate actor-Brain states** used to reconstruct the event that produced the surviving artifact. They are not the target answer and their count is not a count of historical kings. The target remains: who/when/why/how, who ordered, who performed, for whom, under what conditions, and what future state was intended. Evidence may retain, weaken, reject or leave each profile unknown. See `{CONSTITUTION}`.

{END}"""

MICRO_BLOCK = f"""{START}

> This runtime is one growth mechanism inside the **real-time growing Sourceborn ASI prototype**, not the definition of Sourceborn as a reasoning system. Every local Micro-Sequence is an Event contribution to the persistent Brain. Its most important durable output may be a new relation, typed intent hypothesis, combination, contradiction, memory or pattern contribution rather than a prose answer. See `{CONSTITUTION}` and `{CONTRACT}`.

{END}"""

TASK_BLOCK = f"""{START}

## P2-RT-ASI — Growing Phase direction

Status: `ACTIVE / HIGHEST SEMANTIC PRECEDENCE`.

```text
REAL EVENT / EXAMPLE
→ existing Brain activation
→ typed intent + motive separation
→ relation / order / Actor View reconstruction
→ parallel Brain-state combinations when useful
→ reverse ↔ forward ↔ reverse
→ evidence / contradiction / unknown
→ pattern contribution
→ reviewed versioned write-back
→ stronger Brain for the next Event
```

Phase-2 task workstreams below build the substrate for this growth loop. They are not separate product goals and do not redefine Sourceborn as a reasoning or decision engine. Direct-Engine gaps, parameter gaps and contradictory source records remain visible rather than being filled to make the prototype look complete.

{END}"""

LOCK_BLOCK = f"""{START}

## Real-time ASI / Growing-Phase locks

- **SEQ-LOCK-021 — SYSTEM IDENTITY:** Sourceborn is a real-time growing Artificial Super Intelligence prototype. It is not defined as a reasoning system, prompt generator, answer generator, mail-writing engine, LLM wrapper or static decision engine.
- **SEQ-LOCK-022 — UNIVERSAL EVENT LAW:** Everything happening is an Event; every Event carries a typed Intent record or explicit `UNKNOWN / NOT_YET_DECODED`.
- **SEQ-LOCK-023 — INTENT TYPING:** Agent intent, institutional intent, represented-future intent, functional direction, natural-dynamics direction and derived intent hypothesis are distinct. `INTENT != MOTIVE`. Natural dynamics never implies fabricated consciousness.
- **SEQ-LOCK-024 — EXAMPLE SEMANTICS:** Examples are Brain-growth Events. They activate existing IDs and build/test relations, intent signatures, combinations, patterns and memory. They are not output templates.
- **SEQ-LOCK-025 — GROWTH COUNT LAW:** Example count, activation count, relation count, combination count, pattern count and parameter/ID count are separate. No new ID is created merely because a new example exists.
- **SEQ-LOCK-026 — NEW-ID GATE:** A new parameter/rubric/operation/domain ID requires a residual not representable by existing IDs/combinations without distortion, provenance, boundaries/falsifier, review and target-scope R-F-R.
- **SEQ-LOCK-027 — TABLET/KING LAW:** Candidate Kings/actors are parallel testable Brain-state hypotheses for reconstructing the artifact-producing Event; profile count is not historical-entity count.
- **SEQ-LOCK-028 — NODE-BRAIN LAW:** A Node Brain is a persistent bounded intelligence/service state with local state/memory/contracts. It is not a prompt or an answer-generation step.
- **SEQ-LOCK-029 — NEW-THOUGHT LAW:** Mature growth is demonstrated when a new Event activates old primitives/relations in a useful combination not explicitly supplied in a prior example; evidence/R-F-R govern write-back.
- **SEQ-LOCK-030 — HISTORICAL SOURCE PRESERVATION:** Raw, historical and generated source copies are not rewritten to erase older terminology or failed hypotheses. Active architecture interprets them through the current constitution.

Canonical direction: `{CONSTITUTION}`. Machine contract: `{CONTRACT}`.

{END}"""


def upsert_marked_block(path: str, block: str, after_title=True):
    p = ROOT / path
    if not p.exists():
        return
    text = p.read_text(encoding="utf-8")
    pat = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
    if pat.search(text):
        text = pat.sub(block.strip(), text)
    else:
        if after_title and text.startswith("#"):
            first_nl = text.find("\n")
            text = text[:first_nl+1] + "\n" + block.strip() + "\n" + text[first_nl+1:]
        else:
            text = block.strip() + "\n\n" + text
    p.write_text(text, encoding="utf-8")


def load_json(path):
    p = ROOT / path
    return p, json.loads(p.read_text(encoding="utf-8"))


def save_json(p, obj):
    p.write_text(json.dumps(obj, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

# Core explanatory documents.
upsert_marked_block("README.md", IDENTITY_BLOCK)
upsert_marked_block("phase2/README.md", IDENTITY_BLOCK)
upsert_marked_block("phase2/TASK_QUEUE.md", TASK_BLOCK)
upsert_marked_block("docs/MICRO_SEQUENCE_PATTERN_LEARNING_V1.md", MICRO_BLOCK)
upsert_marked_block("docs/KING_CHARACTER_ENGINE_WORKBOOK_REVIEW_V1.md", KING_BLOCK)

# Every active example gets the same non-output-template semantics.
for p in sorted((ROOT / "phase2/examples").glob("*.md")):
    rel = str(p.relative_to(ROOT))
    if p.name == "README.md":
        upsert_marked_block(rel, EXAMPLE_BLOCK)
    else:
        upsert_marked_block(rel, EXAMPLE_BLOCK)

# Locked decisions: insert the lock block before precedence when possible.
p = ROOT / "docs/LOCKED_DECISIONS.md"
if p.exists():
    text = p.read_text(encoding="utf-8")
    pat = re.compile(re.escape(START) + r".*?" + re.escape(END), re.S)
    if pat.search(text):
        text = pat.sub(LOCK_BLOCK.strip(), text)
    else:
        marker = "## Precedence"
        if marker in text:
            text = text.replace(marker, LOCK_BLOCK.strip() + "\n\n" + marker, 1)
        else:
            text += "\n\n" + LOCK_BLOCK.strip() + "\n"
    p.write_text(text, encoding="utf-8")

# Remove stale README claims while preserving legacy source facts.
p = ROOT / "README.md"
if p.exists():
    text = p.read_text(encoding="utf-8")
    text = text.replace(
        "- Approved architecture: `10 Segments → 80 Containers → 2,560 parameters`.\n- Native IDs/names/definitions must be preserved.\n- Full native 2,560-row payload is still a required dependency if not present under `registries/human/native/`.",
        "- Immutable legacy Human provenance: `10 Segments → 80 Containers → SB-ASI-P0001..P2560`.\n- Active Human-derived functional successor: `SB-HFR-P0001..P3204` = 3,204 source parameters; source location does not determine runtime ownership.\n- Legacy IDs remain preserved; growth is versioned and never retroactively rewrites the closed 2,560 source."
    )
    text = text.replace(
        "- Existing 74-family AI capability crosswalk remains **REVIEW ONLY**.",
        "- The 74 AI-CAP families remain preserved source/evidence; approved AI-only records and Sourceborn-native decompositions are additive runtime material, never a definition of Sourceborn as an LLM/reasoning engine."
    )
    p.write_text(text, encoding="utf-8")

# Phase-2 Human and current-work-order sections are stale; replace only those sections.
p = ROOT / "phase2/README.md"
if p.exists():
    text = p.read_text(encoding="utf-8")
    human = """## P2-H — Human

```text
immutable Human legacy source
SB-ASI-P0001..P2560
        +
active Human-derived functional successor
SB-HFR-P0001..P3204
        ↓
exact source activation
        ↓
runtime-owner routing
        ↓
relations / combinations / learning write-back
```

Rules:
- preserve every legacy/source ID and source version;
- `SOURCE LOCATION != RUNTIME OWNERSHIP`;
- examples first activate existing IDs; they do not automatically add parameters;
- new Human-derived IDs arise only through a versioned growth source/review process;
- Human state may change node-to-node through explicit write-back and Actor View remains separate from global reality.
"""
    text = re.sub(r"## P2-H — Human\n.*?(?=\n## P2-A — AI)", human.rstrip(), text, flags=re.S)
    work = """## Current Growing-Phase work order

1. Treat every incoming source/example as an Event and open a typed Intent record (`UNKNOWN` is legal).
2. Activate the exact existing Human/AI/Wisdom/ASI/Sequence IDs before proposing new primitives.
3. Build/test relations, typed order, Actor Views, motives/intents, candidate Brain states and combinations.
4. Use the King/tablet domain as an artifact-event reconstruction test: profiles are candidate Brain states, not the target identity.
5. Persist Pattern Contributions, contradictions, evidence and reviewed write-backs so the next Event starts from a stronger Brain.
6. Promote a new ID only when the residual cannot be represented by existing IDs/combinations without distortion and the target-scope review/R-F-R passes.
7. Continue AI/ASI mechanism, Engine and Node-Brain binding as substrate for the real-time prototype; do not make any LLM or reasoning subsystem the system identity.
8. Close each bounded Sequence without closing the overall Growing Phase.
"""
    text = re.sub(r"## Current work order\n.*?(?=\n## Adoption invariant)", work.rstrip(), text, flags=re.S)
    p.write_text(text, encoding="utf-8")

# Father/Door remains a provenance filename but its visible semantics are corrected.
p = ROOT / "phase2/examples/FATHER_DOOR_3204_REASONING_EXAMPLE_V1.md"
if p.exists():
    text = p.read_text(encoding="utf-8")
    text = text.replace("# Example: Father / Door Reasoning Over Active 3,204 Registry V1", "# Example: Father / Door Brain-Growth Event Over Active 3,204 Registry V1")
    text = text.replace("This is a fictional reasoning fixture.", "This is a fictional Brain-growth Event fixture. The legacy filename is retained for provenance.")
    text = text.replace("║ GENERATED DURING REASONING                   ║", "║ GENERATED DURING EVENT RECONSTRUCTION        ║")
    p.write_text(text, encoding="utf-8")

# Canonicality gets an additive identity/growth layer; no existing source facts are deleted.
p, c = load_json("CANONICALITY.json")
c["system_identity"] = {
    "canonical_name": "Sourceborn ASI",
    "prototype_class": "REAL_TIME_GROWING_ASI_PROTOTYPE",
    "phase_mode": "GROWING_PHASE",
    "constitution_ref": CONSTITUTION,
    "runtime_contract_ref": CONTRACT,
    "reasoning_is_internal_capability_not_system_identity": True,
    "not_identity": ["LLM_WRAPPER", "PROMPT_GENERATOR", "ANSWER_GENERATOR", "MAIL_WRITING_ENGINE", "STATIC_DECISION_ENGINE", "REASONING_SYSTEM_AS_WHOLE_IDENTITY"]
}
c["universal_event_law"] = {
    "motto": "EVERYTHING HAPPENING IS AN EVENT, AND ALL EVENTS HAVE INTENT",
    "every_event_requires_typed_intent_record": True,
    "unknown_allowed": True,
    "natural_dynamics_does_not_imply_conscious_agency": True,
    "intent_not_motive": True
}
c["growing_phase"] = {
    "examples_are_brain_growth_events": True,
    "existing_ids_activate_before_new_id_proposal": True,
    "growth_channels": ["relations", "paths", "combinations", "intent_signatures", "actor_views", "memories", "pattern_contributions", "pattern_candidates", "domain_brain_state_hypotheses", "reviewed_new_ids"],
    "example_count_is_not_parameter_count": True,
    "new_id_gate_ref": CONTRACT,
    "maturation_target": "NOVEL_COMBINATION_FROM_PRIOR_PRIMITIVES_ON_A_NEW_EVENT"
}
save_json(p, c)

# Phase status gets the same identity and a first-class growing workstream.
p, s = load_json("phase2/PHASE_STATUS.json")
s["system_identity"] = {
    "prototype_class": "REAL_TIME_GROWING_ASI_PROTOTYPE",
    "mode": "GROWING_PHASE",
    "constitution_ref": CONSTITUTION,
    "runtime_contract_ref": CONTRACT
}
ph = s.setdefault("phase2", {})
ph["mode"] = "GROWING_PHASE"
ph["objective"] = "Grow the persistent Sourceborn ASI Brain through real Events/examples: activate existing IDs, reconstruct typed intent/motive/relations/order/Actor Views, test parallel combinations and candidate Brain states, preserve evidence/contradictions, and perform reviewed versioned write-back so future Events can activate new combinations."
ph["universal_event_law"] = "EVERYTHING HAPPENING IS AN EVENT, AND ALL EVENTS HAVE INTENT"
ph["growth_invariants"] = [
    "EXAMPLE != OUTPUT_TEMPLATE",
    "PARAMETER_ACTIVATION != NEW_PARAMETER",
    "COMBINATION != NEW_PRIMITIVE",
    "INTENT_HYPOTHESIS != INTENT_FACT",
    "KING_PROFILE_COUNT != HISTORICAL_KING_COUNT",
    "NODE_BRAIN != PROMPT",
    "UNKNOWN > FABRICATED_COMPLETENESS"
]
ws = ph.setdefault("workstreams", [])
ws = [w for w in ws if w.get("id") != "P2-REALTIME-ASI-GROWTH"]
ws.insert(0, {
    "id": "P2-REALTIME-ASI-GROWTH",
    "status": "ACTIVE_HIGHEST_SEMANTIC_PRECEDENCE",
    "outputs": [CONSTITUTION, CONTRACT, "machine/schemas/event_intent.schema.json"],
    "next": "Run every bounded example/source as a Brain-growth Event and measure durable growth in relations, combinations, intent signatures, patterns, memory and validated new IDs rather than prose-output quality."
})
ph["workstreams"] = ws
save_json(p, s)

# Example registry semantics.
p, e = load_json("phase2/examples/EXAMPLE_REGISTRY_V1.json")
e["system_identity_guard"] = "Examples are Brain-growth Events inside the real-time Sourceborn ASI prototype; they are not output templates and do not define Sourceborn as a reasoning engine."
e["example_semantics"] = {
    "default_role": "BRAIN_GROWTH_EVENT_FIXTURE",
    "activate_existing_ids_first": True,
    "possible_growth_outputs": ["RELATION", "PATH", "COMBINATION", "INTENT_HYPOTHESIS", "ACTOR_VIEW", "MEMORY", "PATTERN_CONTRIBUTION", "PATTERN_CANDIDATE", "NEW_ID_CANDIDATE"],
    "new_id_requires_gate": True,
    "contract_ref": CONTRACT
}
for law in ["Every fixture represents at least one Event with a typed Intent record or UNKNOWN", "Example count != parameter count", "Example output prose != primary growth metric"]:
    if law not in e.setdefault("laws", []):
        e["laws"].append(law)
for ex in e.get("examples", []):
    ex["growth_role"] = "BRAIN_GROWTH_EVENT_FIXTURE"
    if ex.get("example_id") == "EX-FATHER-DOOR-3204-001":
        ex["type"] = "MULTI_DOMAIN_BRAIN_GROWTH_EVENT_FIXTURE"
    if ex.get("example_id") == "EX-RAIN-TARGET-LAYER-ACTION-001":
        ex["type"] = "ACTION_TARGET_LAYER_AND_END_MEANS_BRAIN_GROWTH_FIXTURE"
save_json(p, e)

# Intent synthesis remains an internal capability, now explicitly attached to Event Intent.
p, i = load_json("machine/runtime/INTENT_HYPOTHESIS_SYNTHESIS_RUNTIME_V1.json")
i["system_identity_guard"] = "INTERNAL_SOURCEBORN_CAPABILITY_NOT_WHOLE_SYSTEM_IDENTITY"
i["event_intent_contract_ref"] = CONTRACT
i["universal_event_law"] = "EVERYTHING HAPPENING IS AN EVENT, AND ALL EVENTS HAVE INTENT"
i["intent_type_bridge"] = {
    "human_or_agent": "DERIVED_INTENT_HYPOTHESIS until evidence/review promotes it",
    "natural_event": "NATURAL_DYNAMICS_DIRECTION; never infer conscious agency without an agent source",
    "unknown": "UNKNOWN / NOT_YET_DECODED"
}
save_json(p, i)

# Bundle exposes Event + EventIntent as first-class records.
p, b = load_json("machine/schemas/sourceborn.bundle.schema.json")
defs = b.setdefault("$defs", {})
defs["EventIntent"] = {"$ref": "event_intent.schema.json#/$defs/EventIntent"}
defs["EventRecord"] = {"$ref": "event_intent.schema.json#/$defs/EventRecord"}
save_json(p, b)

# Any active Sourceborn registry with legacy REASONING in its registry id gets an explicit identity guard.
for p in sorted((ROOT / "registries/sourceborn").glob("*.json")):
    try:
        obj = json.loads(p.read_text(encoding="utf-8"))
    except Exception:
        continue
    rid = str(obj.get("registry_id", ""))
    if "REASONING" in rid.upper() or "reasoning" in p.name.lower():
        obj["system_identity_guard"] = "LEGACY_REASONING_LABEL_DESCRIBES_AN_INTERNAL_OPERATION_CANDIDATE_NAMESPACE; SOURCEBORN_AS_A_WHOLE_IS_A_REAL_TIME_GROWING_ASI_PROTOTYPE"
        obj["constitution_ref"] = CONSTITUTION
        if p.name == "KING_PROFILE_REASONING_PARAMETER_CANDIDATES_V0.json":
            obj["artifact_event_target"] = "Reconstruct the event/intent that produced the artifact; King profiles are parallel actor-Brain-state hypotheses, not historical identity assertions."
        if "promotion_rule" in obj and isinstance(obj["promotion_rule"], str):
            obj["promotion_rule"] = obj["promotion_rule"].replace("canonical reasoning registry", "canonical Sourceborn reusable-operation/parameter registry")
        save_json(p, obj)

print("Applied Sourceborn real-time ASI Growing-Phase semantic migration V1")
