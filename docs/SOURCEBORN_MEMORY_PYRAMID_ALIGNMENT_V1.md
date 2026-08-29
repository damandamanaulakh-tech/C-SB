# SOURCEBORN MEMORY PYRAMID ALIGNMENT V1

## Status

`PHASE2_ACTIVE_ALIGNMENT_SPECIFICATION`

## Source

Preserved user source:

`raw/sourceborn/MEMORY_PYRAMID_USER_SOURCE_V1.txt`

The source proposes four layers:

1. System
2. Process: Encoding → Storage → Retrieval
3. Temporal stages: Sensory/Input Buffer → Working/RAM-Cache → Long-Term/Persistent Storage
4. Long-Term subsystems: Declarative/Explicit vs Non-Declarative/Implicit, with a computer analogy of user data vs system files/protocols.

This document aligns Sourceborn with that workflow without replacing existing Sourceborn memory types, Node-Brain contracts, Sequence laws, Event laws, source provenance, epistemic controls or growth rules.

---

# 1. Alignment decision

The Memory Pyramid becomes a **cross-cutting memory lifecycle model**, not a replacement memory taxonomy.

Sourceborn already has 12 typed persistent memory channels:

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

These answer:

> WHAT KIND OF MEMORY IS THIS?

The Memory Pyramid adds three additional questions:

```text
PROCESS PHASE
ENCODING / STORAGE / RETRIEVAL

TEMPORAL STAGE
TRANSIENT_INPUT / ACTIVE_WORKING / PERSISTENT_LONG_TERM

MEMORY MODE
EXPLICIT_KNOWLEDGE / PROCEDURAL_RUNTIME / MIXED
```

Therefore one memory object may be described on four orthogonal axes:

```text
MEMORY OBJECT
    │
    ├─ MEMORY TYPE
    │  EVENT_MEMORY / PATTERN_MEMORY / ...
    │
    ├─ PROCESS PHASE
    │  ENCODING / STORAGE / RETRIEVAL
    │
    ├─ TEMPORAL STAGE
    │  TRANSIENT_INPUT / ACTIVE_WORKING / PERSISTENT_LONG_TERM
    │
    └─ MEMORY MODE
       EXPLICIT_KNOWLEDGE / PROCEDURAL_RUNTIME / MIXED
```

This prevents conceptual collapse.

---

# 2. Layer 1 — The System

The source distinguishes Human Memory as a master concept from Computer Memory as a hardware system.

Sourceborn alignment:

```text
[ HUMAN MEMORY SOURCE MODEL ]
              │
              ├──────── reference / evidence ────────┐
              │                                      │
              ▼                                      ▼
      HUMAN SEG / CON / PARAMETERS           SOURCEBORN MEMORY BRAIN
                                                     │
                                                     ├─ Node-Brain local state
                                                     ├─ typed persistent memory
                                                     ├─ Sequence memory
                                                     ├─ global retrieval index
                                                     └─ growth / learning writeback

[ COMPUTER MEMORY SOURCE MODEL ]
              │
              └──────── implementation analogy ──────┘
```

Sourceborn is not defined as either human memory or ordinary computer memory.

It uses both as reference structures while maintaining its own runtime contracts.

Sourceborn system-level memory is:

```text
SOURCEBORN MEMORY BRAIN
=
TRANSIENT EVENT INPUT
+
ACTIVE NODE-BRAIN WORKING STATE
+
TYPED PERSISTENT MEMORY
+
GLOBAL MEMORY INDEX
+
RETRIEVAL / REACTIVATION
+
WRITEBACK / GROWTH
```

---

# 3. Layer 2 — Encoding → Storage → Retrieval

This becomes the primary memory lifecycle.

## 3.1 Encoding

Sourceborn encoding is not merely converting text to tokens or placing bytes at an address.

Sourceborn encoding means:

```text
RAW SOURCE / WORLD EVENT
        ↓
SOURCE LOCK
        ↓
POINT ZERO
        ↓
EVENT DECOMPOSITION
        ↓
OBSERVATIONS / FEATURES
        ↓
SEGMENT / CONTAINER / PARAMETER ACTIVATION
        ↓
RELATION GRAPH
        ↓
ACTOR ROLE / ACTOR STATE
        ↓
INTENT / FUTURE STATE CANDIDATES
        ↓
MEMORY ENCODING PACKET
```

Encoding creates structured meaning while retaining exact source lineage.

Required encoding outputs should include:

```text
source_ref
Point Zero
Event ID
Sequence ID
observation refs
Segment refs
Container refs
Parameter refs
actor refs
Intent refs
Relation refs
Node-Brain routes
epistemic status
origin distance
proof debt
```

Encoding law:

```text
ENCODING
!=
TRUTH PROMOTION
```

A structure may be encoded while still being:

```text
OBSERVED
SOURCE_STATED
INFERRED
NEW_SYNTHETIC
UNKNOWN
REJECTED
```

---

## 3.2 Storage

Storage is the writeback phase.

Sourceborn storage means assigning a durable typed object only after the appropriate write gate.

```text
ENCODED OBJECT
      ↓
WRITE AUTHORITY CHECK
      ↓
SOURCE / LINEAGE CHECK
      ↓
MEMORY TYPE
      ↓
OWNER SCOPE
      ↓
RETENTION POLICY
      ↓
MEMORY ID + VERSION
      ↓
PERSISTENT WRITE
      ↓
AUTO-LINK
      ↓
GLOBAL INDEX
      ↓
GROWTH LEDGER
```

Storage targets are the existing memory channels.

Examples:

```text
Event            → EVENT_MEMORY
Intent           → INTENT_MEMORY
Relation         → RELATION_MEMORY
Path             → PATH_MEMORY
Pattern          → PATTERN_MEMORY
Evidence         → EVIDENCE_MEMORY
Contradiction    → CONTRADICTION_MEMORY
Actor State      → ACTOR_STATE_MEMORY
Sequence         → SEQUENCE_MEMORY
Node working set → NODE_LOCAL_MEMORY
raw provenance   → RAW_MEMORY
retrieval keys   → GLOBAL_MEMORY_INDEX
```

Storage law:

```text
PERSISTENCE
!=
CANONICAL TRUTH
```

Rejected and contradictory hypotheses may remain stored because future Events can use them as negative memory or falsifiers.

---

## 3.3 Retrieval

Retrieval becomes an active reactivation process.

```text
NEW EVENT
   ↓
CURRENT EVENT / SEQUENCE / ACTOR STATE QUERY
   ↓
GLOBAL MEMORY INDEX
   ↓
SOURCE-LINEAGE DEDUPLICATION
   ↓
SCOPE / PERMISSION FILTER
   ↓
RELEVANCE RANKING
   ↓
TYPED MEMORY REFERENCES
   ↓
NODE-BRAIN REACTIVATION
   ↓
ACTIVE WORKING SET
   ↓
NEW COMBINATIONS / TESTS
```

Retrieval must remain reconstructive in the Sourceborn sense: memories are brought back into the **current Event/Sequence context**, not blindly replayed as final answers.

Sourceborn retrieval law:

```text
RETRIEVAL COUNT
!=
TRUTH STRENGTH

REPETITION
!=
INDEPENDENT EVIDENCE
```

The existing `ReinforcementState` already separates retrieval/reuse counts from independent epistemic support.

---

# 4. Layer 3 — Temporal Memory Stages

The source proposes:

```text
Human:
Sensory → Short-Term / Working → Long-Term

Computer:
Input Buffers → RAM / Cache → Hard Drive / SSD
```

Sourceborn alignment:

```text
STAGE T0 — TRANSIENT INPUT
        ↓
STAGE T1 — ACTIVE WORKING MEMORY
        ↓
STAGE T2 — PERSISTENT LONG-TERM MEMORY
```

These are temporal stages, not new memory types.

---

## 4.1 T0 — Transient Input

Equivalent role:

```text
Sensory Memory / Input Buffer
```

Sourceborn implementation concept:

```text
incoming source bytes/text/image/tool result
        ↓
raw Event intake buffer
        ↓
source fingerprint
        ↓
source lock
        ↓
Point Zero declaration
```

T0 objects should normally be temporary until source lock establishes durable provenance.

Possible T0 fields:

```text
input_id
input_type
received_at
raw_payload_ref
source_fingerprint
source_lock_status
preliminary_scope
```

T0 is not yet a durable learned memory.

---

## 4.2 T1 — Active Working Memory

Equivalent role:

```text
Human working memory / Computer RAM-cache
```

Sourceborn implementation:

```text
EVENT WORKING SET
+
NODE-BRAIN LOCAL WORKING SETS
+
ACTIVE SEQUENCE STATE
```

T1 contains active runtime objects such as:

```text
current Event
current Point Zero
active Parameters
active Containers / Segments
active Actor Views
active Actor States
active Intents
active Relations
active Paths
retrieved memories
combination candidates
evidence predictions
contradictions
R-F-R state
pending Sub-Sequence returns
```

Important:

```text
WORKING MEMORY
!=
PERSISTENT MEMORY
```

A candidate may exist in T1 and disappear at Sequence closure unless it passes a writeback rule.

Node-local working memory therefore has two sub-states:

```text
NODE_WORKING_TRANSIENT
NODE_LOCAL_PERSISTENT
```

The first is current execution state.
The second is durable Node-Brain learning/state retained across Events.

---

## 4.3 T2 — Persistent Long-Term Memory

Equivalent role:

```text
Human long-term memory / persistent computer storage
```

Sourceborn implementation:

```text
12 typed MemoryObject classes
+
versioned graph links
+
Global Memory Index
+
growth ledger
```

Persistent memory survives Event/Sequence completion unless its retention policy says otherwise.

Every T2 object must retain:

```text
memory_id
version
memory_type
owner scope
source refs
Point-Zero refs
Event / Sequence refs
retrieval keys
links
epistemic status
maturity
lineage
retention policy
write authority
```

---

# 5. Layer 4 — Long-Term Memory Modes

The source divides human LTM into:

```text
DECLARATIVE / EXPLICIT
NON-DECLARATIVE / IMPLICIT
```

and proposes a computer analogy:

```text
USER DATA
SYSTEM FILES / FIRMWARE
```

Sourceborn should not copy these analogies literally.

Instead it uses two operational persistence modes:

```text
EXPLICIT_KNOWLEDGE_MEMORY
PROCEDURAL_RUNTIME_MEMORY
```

plus:

```text
MIXED_MEMORY
```

This is a classification overlay.

---

## 5.1 Explicit Knowledge Memory

This stores inspectable claims/records about the world, source, Event, actor, evidence or system history.

Typical mapping:

```text
RAW_MEMORY            → EXPLICIT_KNOWLEDGE
EVENT_MEMORY          → EXPLICIT_KNOWLEDGE
INTENT_MEMORY         → EXPLICIT_KNOWLEDGE
RELATION_MEMORY       → EXPLICIT_KNOWLEDGE
EVIDENCE_MEMORY       → EXPLICIT_KNOWLEDGE
CONTRADICTION_MEMORY  → EXPLICIT_KNOWLEDGE
ACTOR_STATE_MEMORY    → EXPLICIT_KNOWLEDGE
SEQUENCE_MEMORY       → EXPLICIT_KNOWLEDGE / MIXED
```

Explicit memory answers questions such as:

```text
What happened?
What source says this?
What actor state was modeled?
What Intent was inferred?
What evidence supported it?
What contradicted it?
What Sequence produced this result?
```

---

## 5.2 Procedural Runtime Memory

This stores reusable operating structures that influence future execution without being treated as factual claims about the world.

Typical mapping:

```text
PATH_MEMORY        → PROCEDURAL_RUNTIME / MIXED
PATTERN_MEMORY     → PROCEDURAL_RUNTIME / MIXED
NODE_LOCAL_MEMORY  → PROCEDURAL_RUNTIME / MIXED
SEQUENCE_MEMORY    → PROCEDURAL_RUNTIME / MIXED
```

Procedural runtime memory can include:

```text
successful routing patterns
known failure routes
reusable dependency paths
Node-Brain local adaptation
retrieval strategies
combination structures
repair/retest paths
Sequence execution patterns
pattern applicability boundaries
```

Important law:

```text
PROCEDURAL MEMORY
!=
UNREVIEWED SELF-MODIFYING CODE
```

Persistent runtime learning may modify data-driven routing, priorities, links, patterns, memories and candidate structures only within governance contracts.

Executable code mutation remains a separate engineering/change-control process.

---

## 5.3 Mixed Memory

Some objects contain both explicit history and reusable runtime structure.

Examples:

```text
PATH_MEMORY
PATTERN_MEMORY
SEQUENCE_MEMORY
NODE_LOCAL_MEMORY
```

These should be marked `MIXED` when both roles materially apply.

---

# 6. Alignment with Segment → Container → Parameter graph

The Memory Pyramid must appear as a runtime layer around the new Human source graph.

```text
                    HUMAN SOURCE TAXONOMY

HUMAN
  ↓
SEGMENT
  ↓
CONTAINER
  ↓
PARAMETER
  │
  │  ENCODING
  ▼
PARAMETER ACTIVATION RECORD
  ↓
ACTIVE PARAMETER CONSTELLATION
  ↓
NODE-BRAIN WORKING MEMORY (T1)
  ↓
COMBINATION / INTENT / EVIDENCE / R-F-R
  │
  │  STORAGE
  ▼
TYPED PERSISTENT MEMORY (T2)
  ↓
GLOBAL MEMORY INDEX
  │
  │  RETRIEVAL
  ▼
NEXT EVENT / NEXT NODE-BRAIN ACTIVATION
```

This makes the relationship explicit:

```text
SEG / CON / PARAMETER
=
what cognitive/function structures exist

MEMORY PYRAMID
=
how Event information moves through runtime time and persistence
```

They are complementary, not competing hierarchies.

---

# 7. Parameter-memory links

Every persistent memory object may link back to source hierarchy.

```text
MemoryObject
  ├─ parameter_refs
  ├─ container_refs
  ├─ node_refs
  ├─ event_refs
  ├─ sequence_refs
  ├─ actor_refs
  ├─ intent_refs
  ├─ pattern_refs
  └─ combination_refs
```

Future graph render should support:

```text
SEGMENT
→ CONTAINER
→ PARAMETER
→ ACTIVATED_BY_EVENT
→ ROUTED_TO_NODE_BRAIN
→ WRITES_MEMORY
→ MEMORY_OBJECT
→ INDEXED_BY
→ GLOBAL_MEMORY_INDEX
→ RETRIEVED_FOR_EVENT
→ REACTIVATES_PARAMETER / NODE_BRAIN
```

---

# 8. Encoding-to-memory writeback flow

Full Sourceborn alignment:

```text
WORLD / USER / TOOL / FILE / SENSOR
        ↓
T0 TRANSIENT INPUT
        ↓
SOURCE LOCK
        ↓
POINT ZERO
        ↓
EVENT DECOMPOSITION
        ↓
ENCODING
        │
        ├─ observations
        ├─ Segments
        ├─ Containers
        ├─ Parameters
        ├─ actors
        ├─ relations
        └─ initial Intent state
        ↓
T1 ACTIVE WORKING MEMORY
        │
        ├─ Node-Brain working sets
        ├─ retrieved prior memory
        ├─ active constellations
        ├─ combinations
        ├─ live Intents
        ├─ future states
        ├─ evidence predictions
        ├─ contradictions
        └─ R-F-R
        ↓
WRITEBACK GATE
        ↓
STORAGE
        ↓
T2 PERSISTENT LONG-TERM MEMORY
        │
        ├─ explicit knowledge memory
        ├─ procedural runtime memory
        └─ mixed memory
        ↓
AUTO-LINK
        ↓
GLOBAL MEMORY INDEX
        ↓
GROWTH LEDGER
        ↓
RETRIEVAL
        ↓
NEXT EVENT
```

---

# 9. Retrieval loop alignment

The Memory Pyramid suggests a left-to-right memory process. Sourceborn adds a controlled return path because retrieval re-enters current working memory.

```text
ENCODING
   ↓
STORAGE
   ↓
RETRIEVAL
   ↓
CURRENT WORKING MEMORY
   ↓
NEW EVENT INTERPRETATION
```

This is not an in-place Sequence loop.

Each new Event or recheck creates a new legal Sequence/Sub-Sequence context.

Therefore:

```text
MEMORY REACTIVATION
!=
REOPEN CLOSED SEQUENCE
```

Closed Sequences stay immutable.

---

# 10. Node-Brain memory alignment

Each Node Brain should have three memory horizons.

```text
NODE BRAIN
  │
  ├─ T0 NODE INPUT VIEW
  │    current inbound Event/return packet
  │
  ├─ T1 NODE WORKING MEMORY
  │    active local processing state
  │
  └─ T2 NODE LOCAL PERSISTENT MEMORY
       reusable state across future Events
```

Node Brain reads from global T2 memory into local T1 working memory.

```text
GLOBAL MEMORY INDEX
       ↓ retrieval
NODE T1 WORKING SET
       ↓ processing
candidate result
       ↓ writeback gate
NODE_LOCAL_MEMORY / other typed T2 memory
```

This is the required mechanism for a Node Brain to become more useful over time without treating every temporary thought as permanent learning.

---

# 11. Memory promotion gate

Not everything in T1 becomes T2.

```text
WORKING OBJECT
    ↓
Is persistence useful?
    ↓
Does object have source lineage?
    ↓
Does correct writer have authority?
    ↓
Does memory type permit automatic candidate write?
    ↓
Are epistemic status and maturity explicit?
    ↓
Does it duplicate an existing object?
    ↓
WRITE / VERSION / LINK / DISCARD FROM PERSISTENT STORE
```

Possible outcomes:

```text
NO_WRITE_TRANSIENT_ONLY
CREATE_MEMORY
VERSION_EXISTING_MEMORY
LINK_TO_EXISTING_MEMORY
WRITE_CONTRADICTION_MEMORY
WRITE_PATTERN_CONTRIBUTION
REVIEW_REQUIRED
```

---

# 12. Pattern and implicit/procedural learning

This is where the Memory Pyramid strongly improves the self-sustaining design.

Repeated successful runtime structures should not automatically create new primitive Parameters.

They should first become procedural memory:

```text
EVENT A
  ↓
path / combination succeeds
  ↓
Pattern Contribution

EVENT B
  ↓
similar structure succeeds
  ↓
Pattern Contribution

EVENT C
  ↓
independent context
  ↓
survives counter-case
  ↓
PATTERN CANDIDATE
  ↓
R-F-R / maturity / review
  ↓
APPROVED PROCEDURAL PATTERN
```

This is Sourceborn's closest functional equivalent to skill/habit learning.

It remains explicit and auditable as data.

---

# 13. Explicit/declarative learning

Explicit factual or event learning follows a different route.

```text
SOURCE
  ↓
Event / claim / observation
  ↓
provenance
  ↓
epistemic status
  ↓
evidence / contradiction
  ↓
EVENT / RELATION / EVIDENCE / INTENT MEMORY
```

This is Sourceborn's closest equivalent to declarative memory.

The two paths may interact:

```text
EXPLICIT EVENT MEMORY
        ↓
repeated event structure
        ↓
PATTERN CONTRIBUTION
        ↓
PROCEDURAL PATTERN MEMORY
```

and:

```text
PROCEDURAL PATTERN MEMORY
        ↓
retrieved during new Event
        ↓
new evidence prediction
        ↓
new explicit Event/Evidence Memory
```

---

# 14. Sourceborn Memory Pyramid full flow

```text
LAYER 1 — SYSTEM

SOURCEBORN MEMORY BRAIN
        │
        ├─ Event / Sequence runtime
        ├─ Node Brains
        ├─ typed memory channels
        ├─ Global Memory Index
        └─ growth / learning


LAYER 2 — PROCESS

ENCODING
   ↓
STORAGE
   ↓
RETRIEVAL
   ↓
REACTIVATION IN NEW EVENT


LAYER 3 — TEMPORAL STAGES

T0 TRANSIENT INPUT
   ↓
T1 ACTIVE WORKING MEMORY
   ↓
T2 PERSISTENT LONG-TERM MEMORY


LAYER 4 — LONG-TERM MODES

T2 MEMORY
   ├─ EXPLICIT_KNOWLEDGE
   ├─ PROCEDURAL_RUNTIME
   └─ MIXED
```

Orthogonal to this:

```text
MEMORY TYPE
=
RAW / EVENT / INTENT / RELATION / PATH / PATTERN /
EVIDENCE / CONTRADICTION / ACTOR_STATE / SEQUENCE /
NODE_LOCAL / GLOBAL_INDEX
```

---

# 15. Required additions to future MemoryObject implementation

Do not replace current `memory_type`.

Add optional lifecycle metadata:

```text
memory_lifecycle:
  process_phase:
    ENCODING
    STORAGE
    RETRIEVAL
    REACTIVATION

  temporal_stage:
    TRANSIENT_INPUT
    ACTIVE_WORKING
    PERSISTENT_LONG_TERM

  memory_mode:
    EXPLICIT_KNOWLEDGE
    PROCEDURAL_RUNTIME
    MIXED
    INDEX_ONLY

  persistence_transition:
    TRANSIENT_ONLY
    CANDIDATE_FOR_WRITE
    PERSISTED
    VERSIONED
    ARCHIVED

  working_owner_ref:
  persistent_owner_ref:
  promoted_from_ref:
  retrieved_from_refs:
```

Because the current MemoryObject schema is a stable contract, this alignment should first exist as an additive runtime contract. The schema can be extended in a later versioned migration after validator coverage is added.

---

# 16. Alignment with Batch-4

Batch-4 is where this becomes executable.

Required engines should now be divided by Memory Pyramid phase.

## Encoding side

```text
memory_encoding_engine.py
```

Responsibilities:

```text
create memory-ready structured packets
attach Event/Sequence/Parameter/Node refs
classify explicit/procedural/mixed mode
assign temporal-stage transition candidate
```

## Storage side

```text
memory_writeback_engine.py
```

Responsibilities:

```text
validate write authority
assign memory type
assign memory ID/version
persist object
auto-link
update Global Memory Index
increment growth ledger
```

## Retrieval side

```text
memory_retrieval_engine.py
```

Responsibilities:

```text
derive current Event query
search Global Memory Index
deduplicate source lineage
rank relevance separately from truth
return typed refs
load into Node-Brain working memory
```

Existing planned Batch-4 engines remain:

```text
auto_link_engine.py
node_growth_engine.py
primitive_candidate_engine.py
growth_ledger_engine.py
seed_engine.py
recheck_engine.py
orphan_link_engine.py
```

The aligned Batch-4 order should be:

```text
1 memory_encoding_engine.py
2 memory_retrieval_engine.py
3 memory_writeback_engine.py
4 auto_link_engine.py
5 growth_ledger_engine.py
6 node_growth_engine.py
7 primitive_candidate_engine.py
8 seed_engine.py
9 recheck_engine.py
10 orphan_link_engine.py
```

---

# 17. Alignment with Seg / Con / Parameter graph work

The new graph substrate should expose the lifecycle visually.

For each Event:

```text
Event
 ↓ ENCODING
Segment activation
 ↓
Container activation
 ↓
Parameter activation
 ↓
Node-Brain T1 Working Memory
 ↓
Combination / Intent / Evidence / R-F-R
 ↓ STORAGE
Typed T2 Memory
 ↓
Global Memory Index
 ↓ RETRIEVAL
future Event / Node Brain
```

The graph renderer should permit switching between:

```text
SOURCE VIEW
SEG → CON → PARAMETER

TEMPORAL MEMORY VIEW
T0 → T1 → T2

PROCESS VIEW
ENCODING → STORAGE → RETRIEVAL

MEMORY MODE VIEW
EXPLICIT → PROCEDURAL → MIXED

RUNTIME VIEW
Event → Parameters → Nodes → Memory → Growth
```

All are projections of one underlying graph.

---

# 18. New graph edge types required by alignment

Additive candidate edge vocabulary:

```text
ENCODED_FROM
ENTERED_WORKING_MEMORY
PROMOTED_TO_PERSISTENT_MEMORY
STORED_AS
RETRIEVED_FROM
REACTIVATED_IN
PROCEDURALIZED_FROM
EXPLICITLY_RECORDED_AS
INDEXED_BY
WORKING_COPY_OF
PERSISTENT_VERSION_OF
```

These do not replace existing relation types.

---

# 19. New graph node classes required by alignment

```text
TRANSIENT_INPUT_NODE
WORKING_MEMORY_VIEW_NODE
PERSISTENT_MEMORY_NODE
MEMORY_INDEX_NODE
```

These are runtime visualization classes.

They do not create new cognitive Parameters.

---

# 20. Validation requirements

Any implementation claiming Memory Pyramid alignment must verify:

```text
1 Existing 12 memory types are preserved.
2 Encoding/Storage/Retrieval are represented separately.
3 T0/T1/T2 are temporal stages, not duplicate memory types.
4 Explicit/Procedural/Mixed are overlays, not truth classes.
5 No working-memory candidate is automatically persistent.
6 No persistent object automatically becomes truth.
7 Retrieval frequency remains separate from evidence support.
8 Closed Sequences are not reopened by retrieval.
9 Node local memory does not become global truth automatically.
10 Source lineage survives all encoding/storage/retrieval transitions.
11 Procedure learning does not silently mutate executable code.
12 Pattern learning does not automatically create Parameters.
13 Persistent writeback creates/version-links a durable object.
14 Global Memory Index points to authoritative payloads rather than duplicating them as new evidence.
15 Next Event can retrieve prior persistent memory into a new working set.
```

---

# 21. Self-sustaining runtime after alignment

The intended automatic loop becomes:

```text
NEW EVENT
   ↓
T0 INPUT
   ↓
ENCODE
   ↓
T1 WORKING MEMORY
   ↓
RETRIEVE RELEVANT T2 MEMORY
   ↓
ACTIVATE PARAMETERS + NODE BRAINS
   ↓
COMBINE
   ↓
LIVE INTENT / FUTURE STATE
   ↓
EVIDENCE / R-F-R
   ↓
WRITEBACK DECISION
   ↓
STORE DURABLE T2 MEMORY
   ↓
AUTO-LINK / INDEX
   ↓
PATTERN / NODE / PRIMITIVE GATES
   ↓
GROWTH LEDGER
   ↓
SEED / RECHECK
   ↓
WAIT
   ↓
NEXT EVENT
```

This is the intended self-sustaining memory loop.

It is not an uncontrolled in-place loop because each new Event/recheck enters a new legal Sequence context.

---

# 22. Final alignment statement

The Memory Pyramid contributes a useful lifecycle distinction:

```text
WHAT MEMORY DOES
ENCODE → STORE → RETRIEVE

WHERE MEMORY IS TEMPORALLY
T0 → T1 → T2

HOW LONG-TERM MEMORY OPERATES
EXPLICIT / PROCEDURAL / MIXED
```

Sourceborn already contributes:

```text
WHAT MEMORY CONTAINS
12 typed memory classes

WHY IT EXISTS
Event / Intent / Relation / Pattern / Evidence / Sequence lineage

WHO MAY USE IT
Node-Brain read/write permissions

HOW IT IS TESTED
R-F-R / falsifiers / maturity

HOW IT GROWS
writeback / auto-link / pattern contribution / growth ledger
```

Combined architecture:

```text
MEMORY PYRAMID LIFECYCLE
            ×
SOURCEBORN TYPED MEMORY
            ×
SEG / CON / PARAMETER ACTIVATION
            ×
NODE-BRAIN RUNTIME
            ×
R-F-R GOVERNANCE
            =
SELF-SUSTAINING SOURCEBORN MEMORY BRAIN
```
