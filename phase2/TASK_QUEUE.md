# Phase-2 Active Task Queue

Phase-1 Universal Sequence baseline is closed. Phase-2 is active.

## P2-001 — Human native registry ingestion

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

Current project materials expose Human container mappings and examples of native parameter IDs, but they do not provide the complete authoritative 2,560-row registry. This task therefore remains blocked by source custody, not by architecture.

## P2-002 — AI capability family review

Status: `STRUCTURAL_REVIEW_V0_COMPLETE — NATIVE ADOPTION STILL OPEN`

Source: `raw/rubrics/AI_CAPABILITY_TO_SOURCEBORN_CONTAINERS_REVIEW.md`

Completed:

- all `AI-CAP-001..074` classified into AI-native candidate layers;
- composite/outcome vs primitive distinction recorded;
- failure/recovery boundaries separated;
- safety/control roles separated by Sequence location;
- runtime vs training boundary preserved;
- anthropomorphic labels narrowed where needed;
- split proposals created for `AI-CAP-056` and `AI-CAP-067`;
- hold conditions recorded for `AI-CAP-013` and `AI-CAP-046`;
- machine rules added in `phase2/reviews/AI_CAPABILITY_DECISION_RULES_v0.json`;
- generator added at `tools/build_ai_candidate_registry.py`.

Still required before AI adoption closure:

```text
resolve HOLD/SPLIT cases
→ establish final AI-native IDs/names
→ declare state ownership + memory writeback
→ add detailed Sequence bindings
→ add ASI-Node bindings
→ run R-F-R sample tests
→ orphan test
→ AI Adoption Closure Packet
```

Source `AI-CAP` rows remain `REVIEW_ONLY` until that closure packet is issued.

## P2-003 — ASI Node Brain instantiation

Status: `V0 INSTANTIATED`

Source registry: `registries/asi/asi_node_registry.json`

Instantiated registry: `registries/asi/node_brains_v0.json`

Explanation: `phase2/asi/ASI_NODE_BRAINS_V0.md`

All `NB-00..NB-17` now have explicit:

```text
inputs
outputs
read stores
write stores
threshold evaluators
allowed tool classes
closure responsibilities
```

Next:

```text
Human bindings
+
AI bindings
+
sample Sequence execution
↓
find contract failures
↓
revise only falsified Node Brain contracts
```

## P2-004 — Holy Book / narrative source adapter

Status: `SCHEMA_READY`

Mandatory separation:

```text
SOURCE TEXT / NARRATIVE CLAIM
↓
EXTRACTED EVENT / RULE / SYMBOL
↓
SOURCEBORN INTERPRETATION
```

Next: ingest a bounded source set and run a complete Source → Event → Sequence → Narrative Memory audit.

## P2-005 — Cross-reference/document generator

Status: `ACTIVE_AUTOGENERATION`

- `tools/assemble_sources.py`
- `tools/generate_registry_views.py`
- `tools/build_ai_candidate_registry.py`
- `tools/relink_and_index.py`
- `tools/validate_repo.py`
- `.github/workflows/relink-validate.yml`

The workflow now:

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
P2-HUMAN waits for authoritative native source

P2-AI
review v0 complete
→ native decision closure required

P2-ASI
Node Brains v0 instantiated
→ bind Human/AI registries

P2-GENERATOR
active

THEN
cross-domain R-F-R tests
→ adoption closure packets
```
