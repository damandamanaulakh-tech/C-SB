# C-SB / Sourceborn — CODEX START HERE

## Repository

- Repository: `damandamanaulakh-tech/C-SB`
- Default branch: `main`
- System identity: `REAL_TIME_GROWING_ASI_PROTOTYPE`
- Current build phase: Growing Phase / self-sustaining runtime construction

This file is the handoff entry point for continuing the Sourceborn work in Codex. Do not reinterpret Sourceborn as an LLM wrapper, prompt generator, reasoning-only system, mail-writing engine, or static decision engine.

---

# 1. Core identity

Sourceborn is a **real-time growing Artificial Super Intelligence prototype**.

Reasoning, planning, retrieval, prediction, simulation, communication, verification and tool-use are internal capabilities. They are not the identity of the system.

Primary motto / invariant:

```text
EVERYTHING HAPPENING IS AN EVENT,
AND ALL EVENTS HAVE INTENT.
```

Intent is typed. Do not assign human consciousness to natural dynamics.

```text
EVENT_INTENT
├─ AGENT_INTENT
├─ INSTITUTIONAL_INTENT
├─ REPRESENTED_FUTURE_INTENT
├─ FUNCTIONAL_DIRECTION
├─ NATURAL_DYNAMICS_DIRECTION
├─ DERIVED_INTENT_HYPOTHESIS
├─ UNKNOWN
└─ NOT_YET_DECODED
```

For humans:

```text
INTENT ≠ MOTIVE
```

Intent = what the actor intends/plans to do or cause.
Motive = why the actor wants it.

---

# 2. Growing-Phase learning law

Examples are not demonstrations of answer generation. They are Brain-growth inputs.

```text
REAL EVENT / EXAMPLE
        ↓
POINT ZERO / SOURCE LOCK
        ↓
EXISTING BRAIN ACTIVATION
        ↓
parameters / containers / rubrics / Node Brains / memory
        ↓
typed Intent + motive + actor view
        ↓
relations + order + dependencies
        ↓
parallel combinations / actor-state branches
        ↓
Reverse → Forward → Reverse
        ↓
evidence / contradiction / falsifier / unknown
        ↓
Pattern Contribution / Memory / Candidate
        ↓
versioned writeback when justified
        ↓
stronger Brain for the next Event
```

Growth does **not** mean automatic parameter inflation.

```text
NEW EXAMPLE ≠ NEW PARAMETER
NEW WORDING ≠ NEW INTENT
NEW COMBINATION ≠ NEW PRIMITIVE
```

An accepted learning batch must increase at least one persistent Brain-object class, such as Event Memory, relation, path, Intent signature, combination signature, Pattern Contribution, Pattern Candidate, Node candidate, primitive candidate, or approved new primitive.

---

# 3. Universal Sequence foundation

Deep primitive:

```text
SEQUENCE = DIFFERENCE + RELATIONSHIP + ORDER
```

Every Sequence is a complete scoped causal/execution history from prior reality to new reality, including conditions, dependencies, alternatives, blocked paths, Sub-Sequences, results, effects, memory and closure.

Never reopen a closed Sequence. New evidence creates a new Sequence referencing the closed one.

Sub-Sequence close condition and return acceptance condition are separate.

---

# 4. Current architecture stack

```text
SOURCEBORN
│
├─ HUMAN
│  ├─ legacy approved source: 10 segments → 80 containers → 2,560 parameters
│  └─ active Human-derived functional successor: 3,204 functional objects
│
├─ AI
│  ├─ source-derived AI capabilities / AI-NEW records
│  ├─ native functional mechanisms
│  └─ AI side of shared operational parameters
│
├─ WISDOM
│  ├─ Source Text
│  ├─ Source Claim
│  ├─ Interpretation
│  ├─ Counter-case / applicability
│  └─ contextual Wisdom Object
│
├─ ASI
│  ├─ 20 semantic meta-governance segments
│  └─ 22 ASI service Nodes / Node Brains
│
├─ UNIVERSAL SEQUENCE RUBRICS
│  └─ 52 rubrics / 987 dimensions
│
├─ BRAIN + ENGINE
│  ├─ 240 master containers
│  ├─ 3,072 operational parameters
│  ├─ 75 engines
│  ├─ 400 Engine→Container relations
│  └─ 1,440 Parameter→Engine/Source relations
│
└─ GROWING MEMORY / COMBINATION / PATTERN GRAPH
```

---

# 5. Batch-1 — foundation contracts

Primary files:

```text
docs/SOURCEBORN_REALTIME_ASI_CONSTITUTION_V1.md
docs/SOURCEBORN_EXECUTION_FLOW_MASTER.md
machine/contracts/SOURCEBORN_SYSTEM_INVARIANTS.json
machine/schemas/event_record.schema.json
machine/schemas/event_intent.schema.json
machine/schemas/node_brain.schema.json
machine/schemas/memory_object.schema.json
machine/schemas/combination_record.schema.json
tools/validate_batch1_foundation_v1.py
phase2/checkpoints/P2_BATCH1_FOUNDATION_CHECKPOINT_V1.json
```

These files define Event, Intent, Node Brain, Memory, Combination, growth and runtime laws.

---

# 6. Batch-2 — runtime/schema linking

Primary files:

```text
machine/runtime/SELF_SUSTAINING_RUNTIME_LINK_CONTRACT_V1.json
registries/sourceborn/NODE_BRAIN_RUNTIME_BINDINGS_V1.json
registries/sourceborn/MEMORY_CHANNEL_REGISTRY_V1.json
registries/sourceborn/AUTO_LINK_RELATION_REGISTRY_V1.json
registries/sourceborn/COMBINATION_RUNTIME_BINDINGS_V1.json
tools/link_batch2_runtime_schemas_v1.py
tools/validate_batch2_runtime_linking_v1.py
phase2/checkpoints/P2_BATCH2_RUNTIME_LINKING_CHECKPOINT_V1.json
```

Runtime stages connect:

```text
source lock
→ Event
→ activation
→ relation graph
→ Node Brain routing
→ memory retrieval
→ combinations
→ live Intent
→ future state
→ evidence
→ R-F-R
→ maturity
→ writeback gate
→ auto-link
→ growth
→ seed / recheck
```

Node service registry remains:

```text
registries/asi/asi_node_registry.json
```

22 ASI service Nodes are bound additively to persistent Node-Brain roles; original Node definitions remain preserved.

---

# 7. Batch-3 — executable native runtime

Executable package:

```text
machine/runtime/engines/
├─ runtime_core.py
├─ source_lock_engine.py
├─ event_decomposition_engine.py
├─ parameter_activation_engine.py
├─ relation_graph_engine.py
├─ actor_role_engine.py
├─ actor_state_engine.py
├─ combination_engine.py
├─ live_intent_engine.py
├─ future_state_reconstruction_engine.py
├─ evidence_prediction_engine.py
├─ rfr_engine.py
├─ falsifier_engine.py
├─ maturity_engine.py
└─ native_runtime_pipeline.py
```

Test / checkpoint:

```text
tools/test_batch3_native_runtime_v1_1.py
phase2/checkpoints/P2_BATCH3_NATIVE_RUNTIME_CHECKPOINT_V1.json
```

Batch-3 is deliberately bounded at zero persistent writeback.

```text
automatic_persistent_writes_performed = 0
```

Persistent learning is Batch-4.

---

# 8. Batch-4 — NEXT BUILD

Exact next Sequence:

```text
P2-SELF-SUSTAINING-RUNTIME-BATCH4-MEMORY-AUTOLINK-NODE-GROWTH-01
```

Build these in order, without shortcuts:

```text
machine/runtime/engines/memory_writeback_engine.py
machine/runtime/engines/auto_link_engine.py
machine/runtime/engines/node_growth_engine.py
machine/runtime/engines/primitive_candidate_engine.py
machine/runtime/engines/growth_ledger_engine.py
machine/runtime/engines/seed_engine.py
machine/runtime/engines/recheck_engine.py
machine/runtime/engines/orphan_link_engine.py
```

Batch-4 goal:

```text
Event N
→ analyze
→ test
→ accepted writeback
→ persistent memory objects
→ relation/path auto-linking
→ strengthen existing Nodes
→ create Node candidates when representation is insufficient
→ promote only after evidence/R-F-R/governance
→ update global index
→ seed future recheck/Sequence
→ Event N+1 starts from changed Brain
```

Do not implement unrestricted external action. Self-sustaining internal learning and external action authority are different layers.

---

# 9. Memory Brain rules

Persistent memory classes:

```text
RAW_MEMORY
EVENT_MEMORY
INTENT_MEMORY
RELATION_MEMORY
PATH_MEMORY
PATTERN_MEMORY
EVIDENCE_MEMORY
CONTRADICTION_MEMORY
ACTOR_STATE_MEMORY
SEQUENCE_MEMORY
NODE_LOCAL_MEMORY
GLOBAL_MEMORY_INDEX
```

Key law:

```text
retrieval frequency ≠ truth
repetition ≠ independent corroboration
memory ≠ source replacement
```

Always preserve source lineage and source-independence groups.

---

# 10. Combination engine rules

Approved bounded combination modes:

```text
C1 ADJACENCY
C2 PATTERN_SUPPORTED
C3 CONTRADICTION
C4 COUNTERFACTUAL
C5 CROSS_DOMAIN
C6 NOVELTY
```

Never perform an unrestricted Cartesian product over the full Brain.

Combination outputs may include:

```text
SYNTHETIC_MEANING
EVENT_HYPOTHESIS
INTENT_HYPOTHESIS
ACTOR_BRAIN_VARIANT
SEQUENCE_VARIANT
EVIDENCE_PREDICTION
PATTERN_CANDIDATE
NODE_CANDIDATE
PRIMITIVE_CANDIDATE
RELATION_CANDIDATE
PATH_CANDIDATE
```

Every synthetic output must remain labeled synthetic until evidence maturity changes it.

---

# 11. R-F-R and maturity

R-F-R stores structured audit checks, not private chain-of-thought.

```text
PASS 1: REVERSE
trace to source / Point Zero / dependencies

PASS 2: FORWARD
predict observable consequences / evidence

PASS 3: REVERSE AUDIT
check assumptions, contradictions, proof debt and origin drift
```

Maturity ladder:

```text
M0 synthetic seed
M1 structurally/source grounded
M2 domain-plausible anchored hypothesis
M3 object/Event-linked evidence
M4 text/source/evidence anchored and R-F-R supported
M5 mature: independent support + counter-case + falsifier + provenance + low proof debt
```

Maturity is not probability.

---

# 12. Tablet / historical artifact work

Codex should read:

```text
docs/TABLET_SYNTHETIC_COMBINATION_NODE_SEQUENCE_MAP_V1.md
docs/TABLET_SYNTHETIC_MEANING_MATURITY_REVIEW_V1.md
docs/GPT_BLACK_ALGORITHM_ADOPTION_NOTES_V1.md
```

The tablet is an Event-reconstruction test, not a translation shortcut.

```text
SURVIVING ARTIFACT
→ what Event caused it to exist?
→ who requested / controlled / authored / performed?
→ what future state was intended?
→ generate parallel actor-state / meaning / Intent hypotheses
→ predict evidence
→ R-F-R
→ retain / weaken / reject / unknown
```

A King profile is a candidate actor-Brain state, not proof of a historical king.

---

# 13. GPT Black material

Use `GPT Black.txt` as historical/source research. Do not copy its LLM-oriented architecture as Sourceborn's identity.

Useful mechanisms to adopt are documented in:

```text
docs/GPT_BLACK_ALGORITHM_ADOPTION_NOTES_V1.md
```

Priority mechanisms:

```text
live Intent generation
same-actor multi-state branching
new-wording ≠ new-Intent test
future-state reconstruction
actor-role separation
damage-aware branching
origin-distance / proof-debt
synthetic-combination lifecycle
```

---

# 14. CI status warning

Do not assume a generated CI report has passed simply because source files exist.

At the time of this handoff, Batch-1/2/3 code/contracts are committed to `main`, but generated validation-report commits have shown infrastructure/trigger lag. Preserve `VALIDATION_PENDING` where the checkpoint says so, inspect workflow state in Codex, and repair actual failures rather than weakening validators.

---

# 15. Codex working rule

When continuing:

1. Read this file.
2. Read `docs/SOURCEBORN_REALTIME_ASI_CONSTITUTION_V1.md`.
3. Read `docs/SOURCEBORN_EXECUTION_FLOW_MASTER.md`.
4. Read `machine/contracts/SOURCEBORN_SYSTEM_INVARIANTS.json`.
5. Read Batch-2 runtime-link registries.
6. Read `phase2/checkpoints/P2_BATCH3_NATIVE_RUNTIME_CHECKPOINT_V1.json`.
7. Inspect current CI/workflow state.
8. Continue Batch-4 in the exact sequence listed above.
9. Do not rename or rewrite native Human/AI/Wisdom/ASI source identities just to fit runtime code.
10. Preserve GAP/UNKNOWN rather than inventing missing structure.

---

# 16. One-screen architecture

```text
REALITY
  ↓
EVENT
  ↓
POINT ZERO
  ↓
SOURCE LOCK
  ↓
EXISTING BRAIN ACTIVATION
  ↓
NODE BRAINS + MEMORY
  ↓
RELATIONS + ACTOR ROLES + ACTOR STATES
  ↓
BOUNDED COMBINATIONS
  ↓
LIVE INTENT
  ↓
FUTURE STATE
  ↓
EVIDENCE PREDICTION
  ↓
REVERSE ↔ FORWARD ↔ REVERSE
  ↓
FALSIFIER / CONTRADICTION
  ↓
MATURITY
  ↓
WRITEBACK GATE
  ↓
MEMORY + AUTO-LINK + NODE GROWTH
  ↓
GLOBAL BRAIN INDEX
  ↓
SEEDS / RECHECKS
  ↓
NEXT EVENT STARTS FROM A STRONGER BRAIN
```
