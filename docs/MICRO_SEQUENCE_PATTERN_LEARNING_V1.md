# Sourceborn Micro-Sequence Pattern Learning V1

Status: Phase-2 active controlled testing.

## Core rule

Every input sentence, question, observation, action description, response, or correction creates at least one local Micro-Sequence.

The runtime does not treat a sentence as one opaque text blob. It progressively decomposes the sentence into bounded objects and addresses them through the existing Sourceborn Pyramid, rubrics, ASI Nodes, and Engine library.

```text
RAW INPUT
  ↓
LOCAL SEQUENCE / POINT ZERO
  ↓
clause / phrase / entity / action / state
  ↓
relation / order / expectation / difference / Actor View
  ↓
Segment → Container → Parameter → Sub-Parameter → Element
  ↓
Sequence roles
  ↓
bounded ASI Nodes + Engines
  ↓
local returns
  ↓
assembled interpretation
  ↓
prior Sequence comparison
  ↓
Pattern Contribution
  ↓
Pattern Candidate when justified
  ↓
Rubric Microscope review
  ↓
user edit / approve / reject / request evidence
  ↓
versioned write-back Sequence
  ↓
future scoped reuse
```

## The pattern rule

Every Micro-Sequence produces a Pattern Contribution. It may activate, support, contradict, weaken, or fail to match an existing pattern. A single sentence does not automatically become a reusable pattern, and repetition count is not a universal fixed threshold.

A Pattern Candidate must keep supporting Sequences, contradicting Sequences, alternative interpretations, context boundaries, intent epistemic status, confidence, and review status.

Observation is not interpretation. Interpretation is not intent fact. Pattern Candidate is not approved rubric.

## Small brains

Existing ASI Nodes remain the service network. The micro runtime adds bounded responsibilities to Nodes 02, 06, 08, 12, 15, 16, 17, 20, and 21.

Each Node Brain receives only the packet fields required by its contract. It returns a bounded result. Whole-case understanding is assembled from typed return packets. Local brains do not gain global authority merely because they participated in the sentence.

## Engine selection

The structured problem selects Engines. The Engine library is not a free-running authority layer.

Examples:

- Point Zero Source Lock → `ENG-CORE-001`
- Signal and clause split → `ENG-CORE-002`
- Real question/scope extraction → `ENG-CORE-003`
- Pyramid routing → `ENG-SB-002..005`
- bounded analytical relation reasoning → `ENG-ARD-001`
- example/pattern comparison → `ENG-CORE-004`, `ENG-PAT-001`, `ENG-CORE-009`, `ENG-SEQ-001`
- recursive deepening → `ENG-RGL-001/002`
- merge/orchestration → `ENG-CORE-010`, `ENG-ORC-001`
- verification/reverse attack → `ENG-URR-002`, `ENG-VER-001`, `ENG-REV-001`
- meta-governance/conflict → `ENG-META-001/002`
- versioned learning write-back → `ENG-CORE-012`, `ENG-EVO-001`

Engine output is evidence/output, not execution authority.

## Rubric Microscope

The intended application UI exposes the structured representation behind an answer without exposing private hidden chain-of-thought. It shows explicit Sourceborn records:

1. source + local Sequence,
2. micro split,
3. Pyramid rubric path and IDs,
4. small-brain/Engine trace,
5. Human interpretation candidates,
6. prior Sequences/repetition,
7. Pattern Candidate,
8. user decision,
9. write-back/version.

The authorized editor can change interpretation, feeling, emotion, intent attribution, motive attribution, meaning, boundary, rule/principle, pattern name, applicability, and approval scope.

The original machine proposal remains immutable as provenance. The edit creates a new review decision and, when accepted, a new learning/write-back Sequence.

## Pattern namespaces

```text
Occurrence Memory
→ Pattern Candidates
→ Personal Patterns
→ Relationship-specific Patterns
→ Domain Patterns
→ General Pattern Candidates
→ Rubric Change Candidates
```

These are different authority scopes. A personal or relationship interpretation does not silently become universal Human truth.

## Learning

Sourceborn learning here means structured write-back:

```text
new event
→ new evidence
→ new relation/difference
→ pattern contribution
→ review
→ approved versioned object
→ changed future activation
```

It does not imply model-weight self-update.

## Primary machine artifacts

- `machine/runtime/SENTENCE_MICRO_SEQUENCE_RUNTIME_V1.json`
- `machine/runtime/MICRO_SEQUENCE_ENGINE_ROUTING_V1.json`
- `machine/schemas/micro_sequence_learning.schema.json`
- `machine/schemas/sourceborn.bundle.schema.json`
- `registries/sourceborn/PATTERN_REGISTRY_CONTROL_V1.json`
- `registries/asi/node_brains/MICRO_SEQUENCE_PATTERN_RESPONSIBILITY_OVERLAY_V1.json`
- `machine/ui/RUBRIC_MICROSCOPE_CONTRACT_V1.json`
- `phase2/tests/MICRO_SEQUENCE_PATTERN_FIXTURE_001.json`
- `tools/validate_micro_sequence_pattern_runtime_v1.py`

The synthetic fixture tests repeated partial disclosure/resource commitment without storing any real person's identity or treating inferred intent as fact.
