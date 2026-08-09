# Phase-2 Adoption and Construction Workflow

Universal Sequence remains the core execution grammar. Phase-2 now runs four explicit workstreams in parallel:

```text
P2-H  HUMAN
P2-A  AI
P2-W  WISDOM / HOLY BOOKS
P2-S  ASI
        │
        └──────────────→ MULTI-RUBRIC WIRING → R-F-R → PHASE-2 CLOSURE
```

## Common source/adoption pipeline

```text
NEW SOURCE / CORPUS / RUBRIC
        ↓
RAW SOURCE LOCK
        ↓
SOURCE TYPE CLASSIFICATION
        ↓
NATIVE HIERARCHY / IDS / DEFINITIONS EXTRACTED
        ↓
SOURCE INTEGRITY CHECK
        ├── duplicates
        ├── missing IDs
        ├── contradictions
        ├── undefined terms
        └── source gaps
        ↓
NATIVE REGISTRY CREATED WITHOUT SILENT REWRITE
        ↓
SEQUENCE BINDINGS ADDED
        ↓
ASI-NODE / NODE-BRAIN BINDINGS ADDED
        ↓
ORPHAN TEST
        ↓
R-F-R SAMPLE TESTS
        ↓
GAP / CONTRADICTION LEDGER
        ↓
ADOPTION CLOSURE PACKET
        ↓
VERSION ADOPTED
```

## P2-H — Human

```text
approved Human native registry
        ↓
10 Segments
        ↓
80 Containers
        ↓
2,560 approved parameters
        ↓
additive Sequence bindings
        ↓
ASI-Node bindings
        ↓
activation-combination + learning/write-back mappings
```

Rules:
- preserve every approved native Human ID/name/definition;
- do not force Human parameters into one chronological Sequence stage;
- Human state may change node-to-node through explicit write-back;
- if the full 2,560-row native source is absent, record the dependency instead of inventing rows.

## P2-A — AI

AI is a construction workstream, not an LLM-adoption workstream.

```text
existing AI / LLM / agent / search / database /
control / planning / symbolic systems
        ↓
REFERENCE EVIDENCE ONLY
        ↓
reverse engineer useful functions
        ↓
remove product-specific implementation assumptions
        ↓
split composites / merge duplicates
        ↓
SOURCEBORN-NATIVE AI RUBRIC
        ↓
AI containers
        ↓
implementable mechanisms / parameters
        ↓
Sequence + ASI-Node bindings
```

Current native draft: `registries/ai/AI_RUBRIC_V0.json`.

Hard rule: no LLM API, Transformer, next-token, or monolithic-model dependency is assumed by Sourceborn.

## P2-W — Wisdom / Holy Books

Holy Books are sources. Wisdom is derived and source-linked.

```text
RAW SOURCE
↓
SOURCE TEXT
↓
SOURCE CLAIM
↓
EVENT / RULE / PROMISE / SYMBOL
↓
SEQUENCE RECONSTRUCTION
↓
INTERPRETATION RECORD
↓
CASE COMPARISON + COUNTER-CASE
↓
APPLICABILITY BOUNDARY
↓
WISDOM OBJECT
↓
optional LAW / GUIDANCE formation
```

Current files:
- `registries/wisdom/WISDOM_REGISTRY_V0.json`
- `registries/wisdom/HOLY_BOOK_SOURCE_TO_WISDOM_CONTRACT.json`

Never collapse Source Text → Interpretation → Wisdom → Law into one object.

## P2-S — ASI

ASI is the meta-governance layer, distinct from AI cognition.

```text
Human state/capability
+
AI cognition mechanisms
+
Wisdom / source-linked principles
+
current reality / evidence
        ↓
ASI meta-rubric
        ↓
truth / provenance / permission /
priority / contradiction / long-horizon /
closure-scope governance
        ↓
ASI Node network
```

Current ASI meta-rubric: `registries/asi/ASI_RUBRIC_V0.json`.

The ASI service registry now contains `ASI-NODE-00..21`.

New nodes:
- `ASI-NODE-18` — Holy-Book / Wisdom Source Interpreter
- `ASI-NODE-19` — Wisdom / Principle Synthesis
- `ASI-NODE-20` — AI Rubric / Cognitive Mechanism Router
- `ASI-NODE-21` — ASI Rubric / Meta-Governor

Node Brain contracts: `registries/asi/node_brains/NODE_BRAINS_18_21.json`.

## Multi-rubric runtime

```text
SEQUENCE NODE / EDGE
        ↓
ASI-NODE-06
MULTI-RUBRIC ACTIVATION / COMBINATION
        │
        ├── HUMAN activation
        ├── AI cognition demand
        ├── WISDOM/source demand
        └── ASI governance demand
        │
        ↓
required specialist ASI Nodes
        ↓
conflict / arbitration if required
        ↓
trigger + threshold
        ↓
barrier / dependency check
        ↓
execution
        ↓
result / entity outcome / trace
        ↓
R-F-R
        ↓
closure
```

Machine-readable wiring: `machine/wiring/MULTI_RUBRIC_WIRING_V0.json`.

## Current work order

1. Preserve and map the complete approved Human 2,560-row native registry when available.
2. Decompose `AI_RUBRIC_V0` into AI containers and implementable mechanisms/parameters.
3. Compare AI-CAP-001..074 against the native AI rubric; the old 74-family map remains REVIEW ONLY.
4. Build first Holy-Book/Wisdom source ingestion batch using strict source → claim → interpretation separation.
5. Decompose `ASI_RUBRIC_V0` into meta-containers/parameters and bind them to ASI-NODE-00..21.
6. Complete Node Brain contracts for all ASI Nodes, not only 18..21.
7. Run Human + AI + Wisdom + ASI multi-rubric Sequence tests.
8. Run Reverse → Forward → Reverse audits and orphan checks.
9. Close each adoption/construction batch with an explicit Closure Packet.

## Adoption invariant

```text
RAW SOURCE
↓
NATIVE REGISTRY
↓
ADDITIVE MAPPING
↓
ASI NODE BINDING
↓
TEST
↓
CLOSURE PACKET
```

The mapping layer is never allowed to rewrite a native registry merely to make a Sequence fit.
