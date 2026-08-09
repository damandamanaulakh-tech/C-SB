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

## P2-002 — AI capability family review

Status: `READY_FOR_REVIEW`

Source: `raw/rubrics/AI_CAPABILITY_TO_SOURCEBORN_CONTAINERS_REVIEW.md`

Current candidates: `AI-CAP-001..074`.

Allowed user outcomes per family:

```text
ACCEPT
RENAME
SPLIT
MERGE
MOVE
OMIT
HOLD
```

Until review, every item remains `REVIEW_ONLY`.

## P2-003 — ASI Node Brain instantiation

Status: `SEEDED`

Source registry: `registries/asi/asi_node_registry.json`

Template: `registries/asi/node_brain_template.json`

Next: instantiate `NB-00..NB-17` with exact inputs, outputs, memory, permissions, threshold evaluators, tools and closure responsibilities.

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

## P2-005 — Cross-reference/document generator

Status: `BOOTSTRAPPED`

- `tools/assemble_sources.py`
- `tools/generate_registry_views.py`
- `tools/relink_and_index.py`
- `tools/validate_repo.py`
- `.github/workflows/relink-validate.yml`

The workflow rebuilds `generated/` whenever source/registry/machine files change.
