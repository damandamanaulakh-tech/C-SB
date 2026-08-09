↓
ACTION
↓
RESULT
↓
VERIFICATION
```

---

## H-COMB-02 — Perceive / Interpret / Decide

Primary containers:

```text
CON-009–016
CON-025
CON-028
CON-041–047
```

Typical route:

```text
ENVIRONMENT
↓
PERCEPTION
↓
SALIENCE
↓
ATTENTION
↓
WORKING STATE
↓
INTERPRETATION
↓
REASONING
↓
ALTERNATIVES
↓
SELECTION
↓
DECISION
```

---

## H-COMB-03 — Execute / Observe / Correct

Primary containers:

```text
CON-017–024
CON-031
CON-032
```

Typical route:

```text
DECISION
↓
ACTION READINESS
↓
MOTOR / EXECUTION PLAN
↓
EXECUTION
↓
OUTPUT / EFFECT
↓
SENSORIMOTOR FEEDBACK
↓
ERROR MONITORING
↓
CORRECTION SEQUENCE
```

---

## H-COMB-04 — Learn / Compress / Reuse

Primary containers:

```text
CON-033–040
CON-074
CON-075
CON-078
CON-079
CON-080
```

Typical route:

```text
RESULT
↓
ERROR / OUTCOME COMPARISON
↓
EPISODIC / SEMANTIC / PROCEDURAL MEMORY
↓
CONSOLIDATION
↓
RECONSOLIDATION
↓
METACOGNITION
↓
PLASTICITY / EXPERTISE
↓
COMPRESSION
↓
VALIDATED HANDLE
↓
FUTURE REFERENCE / RE-ENTRY BY NEW SEQUENCE
```

---

# 26. HUMAN DUAL-TRACK EXECUTION

A Human Sequence runs at least two paths simultaneously.

```text
                    HUMAN AT STATE H_t
                           │
              ┌────────────┴────────────┐
              ↓                         ↓
       WORLD EXECUTION            HUMAN WRITE-BACK
              │                         │
      what happens outside       what changes inside
              │                         │
              └────────────┬────────────┘
                           ↓
                    HUMAN STATE H_t+1
```

Learning is node-to-node.

It is not only an end-stage event.

Examples:

```text
PERCEPTION
→ perceptual learning

REQUIREMENT / DRIVER
→ value / priority update

TESTING
→ evidence learning

SELECTION
→ preference update

ACTION
→ procedural learning

RESULT
→ outcome learning

VERIFICATION
→ model correction

MEMORY
→ encoding / consolidation / integration

RETRIEVAL
→ reconsolidation / update
```

---

# 27. HUMAN TIMESCALE LOOPS

```text
EXECUTION LOOP
seconds → minutes

LEARNING LOOP
minutes → days

DEVELOPMENT LOOP
months → years

SOCIAL / CULTURAL TRANSMISSION
years → generations
```

These loops are not one endlessly open Sequence.

Each event/episode closes.

Their Closure Packets change the next baseline.

```text
H0
↓ experience S1 closes
H1
↓ experience S2 closes
H2
↓ ...
Hn
```

---

# 28. HUMAN MEMORY CYCLE

```text
EXPERIENCE
↓
ATTENTION
↓
ENCODING
↓
CONSOLIDATION
↓
INTEGRATION
↓
STORAGE
↓
RETRIEVAL
↓
RECONSOLIDATION
↓
UPDATED MEMORY
```

Compression must preserve:

```text
scope
conditions
confidence
recoverability
source
exceptions
```

---

# 29. AI RUBRIC — ADOPTION RULE

The exact native AI rubric is not defined in the currently loaded Sequence source.

Therefore this file must **not invent AI parameter counts, IDs or names**.

The AI adapter is ready to adopt any approved AI rubric when it is supplied.

```text
AI_RUBRIC_SOURCE
↓
RAW SOURCE LOCK
↓
NATIVE HIERARCHY DETECTION
↓
PRESERVE EVERY APPROVED ID
↓
PRESERVE EVERY APPROVED NAME
↓
PRESERVE EVERY APPROVED DEFINITION
↓
CREATE AI_SEQUENCE_BINDINGS
↓
CREATE AI_ASI_NODE_BINDINGS
↓
TEST FOR ORPHAN PARAMETERS
↓
ADOPT VERSION
```

Until the AI registry is loaded:

```text
AI_RUBRIC_STATUS = SCHEMA_READY_DATA_PENDING
```

This is not a gap to fill by invention.

---

# 30. AI RUBRIC ADAPTER SCHEMA

Regardless of its native hierarchy:

```text
AI_SEQUENCE_BINDING {
    native_ai_id
    native_parent_ids[]
    native_name
    native_definition

    primary_sequence_roles[]
    secondary_sequence_roles[]

    activation_conditions[]

    read_channels[]
    action_channels[]
    tool_channels[]

    writeback_channels[]

    memory_read_types[]
    memory_write_types[]

    combination_group_ids[]

    controller_roles[]
    performer_roles[]

    source_ref
    epistemic_status
}
```

Possible mapping-role classes may include:

```text
INPUT / OBSERVATION
RETRIEVAL
STATE ESTIMATION
RELATION MAPPING
REASONING
PLANNING
ALTERNATIVE GENERATION
ARBITRATION
TOOL EXECUTION
VERIFICATION
MEMORY
COMPRESSION
META-CONTROL
```

These are **adapter roles**, not replacements for the native AI rubric.

---

# 31. AI STATE AND LEARNING DISCIPLINE

Do not pretend that an AI model's internal trained weights change merely because one Sequence ran.

Separate:

```text
MODEL WEIGHTS
RUNTIME CONTEXT
WORKING MEMORY
EXTERNAL MEMORY
TOOL STATE
RULE / CONFIG STATE
RETRIEVAL STATE
LEARNED ARTIFACTS
```

Runtime learning may write only to explicitly permitted stores.

```text
AI EXPERIENCE
↓
RESULT / ERROR
↓
VERIFICATION
↓
ALLOWED WRITE-BACK?
   ├── NO → trace only
   └── YES
          ↓
      memory / rule / config / dataset /
      compressed handle / training candidate
```

Actual model training is a separate Sequence with its own contract.

---

# 32. HUMAN + AI RUBRIC FUSION AT A SEQUENCE NODE

A Sequence node may activate Human and AI registries at the same time.

```text
                      SEQUENCE NODE N
                            │
        ┌───────────────────┼────────────────────┐
        ↓                   ↓                    ↓
   HUMAN RUBRIC         AI RUBRIC          OTHER REGISTRY
        │                   │                    │
   H activation set     A activation set      tools / corpus /
        │                   │                 environment
        └───────────────────┼────────────────────┘
                            ↓
                  ACTIVATION COMBINATION
                            ↓
                    TEMPORARY NODE STATE
                            ↓
                   LEGAL EDGE EVALUATION
                            ↓
                     ACTION / EFFECT
                            ↓
                         RESULT
```

Keep ownership clear:

```text
which registry supplied the capability?
which actor owns the state?
who controls?
who performs?
who carries?
who is affected?
```

---

# 33. ASI RUBRIC — META LAYER

Sourceborn ASI does not replace Human or AI registries.

ASI is the meta-coordination layer that can:

```text
build Sequence graphs
reverse-mine declared ends
route to Human/AI/domain rubrics
activate ASI Nodes
evaluate thresholds
maintain Open-Sequence Ledger
maintain Seed Registry
maintain Actor View maps
detect unconnected dots
open Investigation Sequences
coordinate parallel Sequences
manage convergence/synchronization
run R-F-R verification
manage compression/expansion
assemble Closure Packets
compare closed cases
form candidate patterns/rules
```

ASI must still obey:

```text
source precedence
barrier law
no reopen
no manufactured source
actor-view separation
closure-scope separation
```

---

# 34. ASI MEMORY FABRIC

Memory is not one store.

```text
MEMORY FABRIC
│
├── WORKING NODE MEMORY
├── SEQUENCE TRACE
├── FACT / RESULT MEMORY
├── PATH MEMORY
├── FAILURE MEMORY
├── CONTEXT MEMORY
├── RULE MEMORY
├── PROCEDURAL / SKILL MEMORY
├── ACTOR VIEW MEMORY
├── SEED REGISTRY
├── NARRATIVE MEMORY
├── INSTITUTIONAL MEMORY
├── COMPRESSION HANDLE STORE
├── CLOSURE PACKET ARCHIVE
└── CONTRADICTION / GAP LEDGER
```

Every memory item carries:

```text
source
scope
time/version
context
confidence
epistemic status
contradictions
recoverability
exceptions
reference_sequence_ids
```

---

# 35. COMPRESSION ↔ EXPANSION

Compression:
