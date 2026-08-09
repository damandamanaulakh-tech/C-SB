# Phase-2 Active Task Queue

Phase-1 Universal Sequence baseline is closed. Phase-2 is active with four explicit workstreams.

```text
P2-H  HUMAN
P2-A  AI
P2-W  WISDOM / HOLY BOOKS
P2-S  ASI
        │
        ↓
MULTI-RUBRIC INTEGRATION
        ↓
R-F-R
        ↓
PHASE-2 CLOSURE
```

## P2-H — Human native registry ingestion

Status: `WAITING_SOURCE`

Required input: complete approved Human registry containing all `SEG-xx`, `CON-xxx`, and `SB-ASI-Pxxxx` records.

Execution:

```text
RAW LOCK
→ native hierarchy parse
→ ID integrity check
→ source/definition preservation
→ Sequence-role binding
→ ASI-Node binding
→ combination/writeback mapping
→ orphan test
→ R-F-R sample tests
→ Adoption Closure Packet
```

No Human parameter may be synthesized to fill a missing row.

Current project materials expose Human container mappings and examples of native parameter IDs, but they do not provide the complete authoritative 2,560-row registry. This task remains blocked by source custody, not by architecture.

## P2-A — Native AI rubric construction

Status: `NATIVE_RUBRIC_V0_CREATED — DECOMPOSITION OPEN`

Native draft: `registries/ai/AI_RUBRIC_V0.json`

Legacy evidence source: `raw/rubrics/AI_CAPABILITY_TO_SOURCEBORN_CONTAINERS_REVIEW.md`

The legacy `AI-CAP-001..074` map remains `REVIEW_ONLY`.

Current rule:

```text
EXISTING AI / LLM / AGENT / SEARCH / DATABASE /
CONTROL / PLANNING / SYMBOLIC SYSTEM
        ↓
REVERSE ENGINEERING EVIDENCE
        ↓
USEFUL FUNCTION
        ↓
REMOVE PRODUCT-SPECIFIC IMPLEMENTATION
        ↓
SOURCEBORN-NATIVE AI MECHANISM
```

No LLM API, Transformer, next-token or monolithic-model dependency is assumed.

Current native AI rubric contains `AI-01..AI-25` functional segments.

Next:

```text
AI-01..AI-25
→ containers
→ implementable mechanisms/parameters
→ compare AI-CAP-001..074
→ split/merge/omit/hold decisions
→ state ownership + memory writeback
→ Sequence bindings
→ ASI-Node bindings
→ R-F-R tests
→ orphan test
→ AI Adoption Closure Packet
```

## P2-W — Wisdom / Holy Books

Status: `WISDOM_REGISTRY_V0 + SOURCE_CONTRACT CREATED — SOURCE INGESTION OPEN`

Files:
- `registries/wisdom/WISDOM_REGISTRY_V0.json`
- `registries/wisdom/HOLY_BOOK_SOURCE_TO_WISDOM_CONTRACT.json`

Hard separation:

```text
SOURCE TEXT
!= SOURCE CLAIM
!= INTERPRETATION
!= WISDOM OBJECT
!= LAW / GUIDANCE
!= CURRENT APPLICATION
```

Current Wisdom registry contains `W-01..W-15` initial lanes.

Next:

```text
bounded Holy-Book/narrative source batch
→ raw lock
→ source claims
→ event/rule/promise/symbol extraction
→ Sequence reconstruction
→ interpretation records
→ counter-case comparison
→ applicability boundaries
→ Wisdom candidates
→ ASI-NODE-18 / 19 test
→ R-F-R
→ Wisdom batch Closure Packet
```

## P2-S — ASI rubric + Node Brain instantiation

Status: `ASI_RUBRIC_V0 CREATED — ASI-NODE-00..21 WIRED`

Files:
- `registries/asi/ASI_RUBRIC_V0.json`
- `registries/asi/asi_node_registry.json`
- `registries/asi/node_brains_v0.json`
- `registries/asi/node_brains/NODE_BRAINS_18_21.json`

Base Node Brains `NB-00..17` remain preserved.

New Node Brains:
- `NB-18` — Holy-Book / Wisdom Source Interpreter
- `NB-19` — Wisdom / Principle Synthesis
- `NB-20` — AI Rubric / Cognitive Mechanism Router
- `NB-21` — ASI Rubric / Meta-Governor

Current ASI rubric contains `ASI-01..ASI-20` meta-governance segments.

Next:

```text
ASI-01..ASI-20
→ meta-containers / parameters
→ bind to ASI-NODE-00..21
→ complete all Node Brain cross-domain bindings
→ execute sample conflict / priority / provenance / closure cases
→ falsify contracts
→ revise only falsified contracts
→ ASI Adoption Closure Packet
```

## P2-I — Multi-rubric wiring

Status: `WIRED_DRAFT_FOR_RFR`

Machine-readable file: `machine/wiring/MULTI_RUBRIC_WIRING_V0.json`

Runtime:

```text
SEQUENCE NODE / EDGE
        ↓
ASI-NODE-06 MULTI-RUBRIC ROUTER
        │
        ├── HUMAN activation/state
        ├── AI cognition demand
        ├── WISDOM/source demand
        └── ASI governance demand
        ↓
specialist ASI Nodes
        ↓
conflict / arbitration where required
        ↓
trigger + threshold
        ↓
barrier / dependency
        ↓
execution
        ↓
result / entity outcome / trace
        ↓
R-F-R
        ↓
closure
```

Next integration tests must include at least:

1. Human + AI without Wisdom.
2. Human + Wisdom without artificial action.
3. AI + ASI governance conflict.
4. Human + AI + Wisdom + ASI on the same Sequence node.
5. Contradictory Wisdom/source cases.
6. Actor View restricting global knowledge.
7. Local closure vs higher-scope closure.
8. Barrier blocked by an unaccepted required return.

## P2-G — Cross-reference/document generator

Status: `ACTIVE_AUTOGENERATION`

- `tools/assemble_sources.py`
- `tools/generate_registry_views.py`
- `tools/build_ai_candidate_registry.py`
- `tools/relink_and_index.py`
- `tools/validate_repo.py`
- `.github/workflows/relink-validate.yml`

The relinker now indexes:

```text
SEG-xx
CON-xxx
SB-ASI-Pxxxx
H-COMB-xx
AI-CAP-xxx legacy review IDs
AI-01..AI-25 native rubric IDs
W-01..W-15 Wisdom lanes
ASI-01..ASI-20 meta-rubric IDs
ASI-NODE-00..21 service nodes
NB-00..21 Node Brains
AI/ASI/Wisdom registry IDs
```

The workflow:

```text
ASSEMBLE CANONICAL SOURCES
↓
BUILD REGISTRY VIEWS
↓
BUILD AI NATIVE CANDIDATE VIEW
↓
RELINK KNOWN IDS
↓
VALIDATE LOCKED INVARIANTS
↓
COMMIT GENERATED OUTPUTS
```

## Current Phase-2 critical path

```text
P2-H
waits for authoritative 2,560-row Human source

P2-A
AI rubric v0 exists
→ mechanism/container decomposition now begins

P2-W
Wisdom/source contracts exist
→ first bounded source ingestion now begins

P2-S
ASI rubric v0 + 22 ASI Nodes exist
→ meta-parameter decomposition + integration tests now begin

P2-I
four-rubric wiring exists
→ R-F-R integration tests required

THEN
orphan tests
→ adoption closure packets
→ Phase-2 closure
```
