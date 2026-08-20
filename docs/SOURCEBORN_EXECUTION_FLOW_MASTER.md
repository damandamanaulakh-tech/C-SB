# Sourceborn Execution Flow Master

Status: **PHASE-2 ACTIVE BUILD SPECIFICATION**  
Constitution: `docs/SOURCEBORN_REALTIME_ASI_CONSTITUTION_V1.md`

---

## 1. What this document defines

This document specifies how the real-time Sourceborn ASI prototype should operate when the user is no longer manually instructing every transition.

It defines:

1. the main Event→Sequence→Node-Brain execution route;
2. the data objects exchanged between stages;
3. how Node Brains retrieve and write memory;
4. how combinations and live intents are generated;
5. how new Nodes are proposed and promoted;
6. how new parameters/headers/rubrics are linked;
7. how persistent growth is counted;
8. how the runtime re-enters itself automatically;
9. the nine primary loops and four maintenance loops;
10. stop, halt, open and recheck conditions;
11. the boundary between automatic growth and authority-sensitive execution.

This is not an LLM prompt chain. It is the execution design for a persistent graph-and-memory runtime.

---

# 2. High-Level Arrow Graph

```text
┌──────────────────────────────────────────────────────────────────────────┐
│                           WORLD / INPUT                                 │
│ user text • image • artifact • file • event • tool result • memory     │
└──────────────────────────────────┬───────────────────────────────────────┘
                                   ↓
┌──────────────────────────────────────────────────────────────────────────┐
│ 01 SOURCE LOCK + POINT ZERO                                              │
│ preserve raw source • provenance • scope • origin • no fabrication       │
└──────────────────────────────────┬───────────────────────────────────────┘
                                   ↓
┌──────────────────────────────────────────────────────────────────────────┐
│ 02 EVENT INTAKE / DECOMPOSITION                                          │
│ one source may create 1..N Events • nested Events • local Point Zeros     │
└──────────────────────────────────┬───────────────────────────────────────┘
                                   ↓
┌──────────────────────────────────────────────────────────────────────────┐
│ 03 EXISTING BRAIN ACTIVATION                                             │
│ parameters • containers • rubrics • nodes • engines • memories • views   │
└──────────────────────────────────┬───────────────────────────────────────┘
                                   ↓
┌──────────────────────────────────────────────────────────────────────────┐
│ 04 RELATION / ORDER / ACTOR GRAPH                                        │
│ produced_by • depends_on • before_after • supports • contradicts • roles  │
└──────────────────────────────────┬───────────────────────────────────────┘
                                   ↓
┌──────────────────────────────────────────────────────────────────────────┐
│ 05 NODE-BRAIN ACTIVATION                                                 │
│ retrieve local memory • state • intents • evidence • patterns • limits    │
└──────────────────────────────────┬───────────────────────────────────────┘
                                   ↓
┌──────────────────────────────────────────────────────────────────────────┐
│ 06 COMBINATION ENGINE                                                    │
│ components + state + memory + patterns + relations → candidate structures │
└───────────────────────┬──────────────────────────────────────────────────┘
                        │
           ┌────────────┼─────────────┬────────────────┬────────────────┐
           ↓            ↓             ↓                ↓                ↓
     synthetic      event         actor-brain       sequence        pattern
      meaning      hypothesis       variant          variant        candidate
           └────────────┴─────────────┴────────────────┴────────────────┘
                                   ↓
┌──────────────────────────────────────────────────────────────────────────┐
│ 07 LIVE INTENT + FUTURE-STATE SYNTHESIS                                  │
│ actor • target • desired state • pressure • history • horizon • result    │
└──────────────────────────────────┬───────────────────────────────────────┘
                                   ↓
┌──────────────────────────────────────────────────────────────────────────┐
│ 08 EVIDENCE PREDICTION                                                    │
│ if hypothesis true → what should exist / happen / not exist?              │
└──────────────────────────────────┬───────────────────────────────────────┘
                                   ↓
┌──────────────────────────────────────────────────────────────────────────┐
│ 09 REVERSE → FORWARD → REVERSE                                           │
│ origin requirements → predicted consequences → evidence return test       │
└──────────────────────────────────┬───────────────────────────────────────┘
                                   ↓
┌──────────────────────────────────────────────────────────────────────────┐
│ 10 FALSIFIER / CONTRADICTION / MATURITY                                  │
│ retain • weaken • reject • unknown • upgrade maturity • preserve debt     │
└──────────────────────────────────┬───────────────────────────────────────┘
                                   ↓
┌──────────────────────────────────────────────────────────────────────────┐
│ 11 WRITE-BACK DECISION                                                    │
│ no write • memory only • relation • path • pattern • candidate Node / ID   │
└──────────────────────────────────┬───────────────────────────────────────┘
                                   ↓
┌──────────────────────────────────────────────────────────────────────────┐
│ 12 MEMORY BRAIN                                                           │
│ local Node memory + Sequence memory + global memory index                  │
└──────────────────────────────────┬───────────────────────────────────────┘
                                   ↓
┌──────────────────────────────────────────────────────────────────────────┐
│ 13 AUTO-LINK                                                              │
│ source • actor • relation • pattern • contradiction • future • similarity │
└──────────────────────────────────┬───────────────────────────────────────┘
                                   ↓
┌──────────────────────────────────────────────────────────────────────────┐
│ 14 NEW-NODE / NEW-PRIMITIVE GATE                                         │
│ representable already? → reinforce | irreducible? → candidate → R-F-R     │
└──────────────────────────────────┬───────────────────────────────────────┘
                                   ↓
┌──────────────────────────────────────────────────────────────────────────┐
│ 15 GROWTH LEDGER                                                         │
│ persistent object count increases without fake parameter inflation        │
└──────────────────────────────────┬───────────────────────────────────────┘
                                   ↓
┌──────────────────────────────────────────────────────────────────────────┐
│ 16 SEED + RECHECK SCHEDULER                                               │
│ future trigger • threshold • missing evidence • contradiction • maturity  │
└──────────────────────────────────┬───────────────────────────────────────┘
                                   ↓
                       NEXT EVENT / NEXT RUN
```

---

# 3. Execution Envelope

Every runtime invocation should create an `ExecutionEnvelope` even before that schema is formalized in a later batch.

Conceptual fields:

```yaml
execution_id:
mode: MANUAL | SEMI_AUTO | AUTO_GROW | SCHEDULED
started_at:
source_refs: []
point_zero_ref:
root_event_ids: []
root_sequence_id:
authorized_write_scope:
authorized_action_scope:
compute_budget:
loop_budget:
max_candidate_count:
max_origin_distance:
required_validators: []
open_subsequences: []
created_object_ids: []
updated_object_ids: []
rejected_candidate_ids: []
errors: []
status:
```

The envelope prevents autonomous loops from expanding indefinitely or writing outside their authority scope.

---

# 4. Stage 01 — Source Lock and Point Zero

## Input

Any authorized source:

```text
USER INPUT
FILE
IMAGE
ARTIFACT
DATABASE RECORD
TOOL RESULT
EXTERNAL EVENT
MEMORY RECHECK
SEED ACTIVATION
```

## Operations

1. Generate immutable source reference.
2. Compute source fingerprint where technically available.
3. Preserve exact raw form or stable connector reference.
4. Declare source class.
5. Declare scope.
6. Create Point Zero record/reference.
7. Separate source truth from objective truth.
8. Mark unreadable/damaged/unknown areas explicitly.
9. Block downstream promotion if provenance is missing beyond allowed scope.

## Output packet

```text
SOURCE_PACKET
├─ source_ref
├─ source_type
├─ source_fingerprint
├─ point_zero_ref
├─ scope
├─ raw_content_ref
├─ observation_constraints
├─ unreadable_regions
├─ source_claim_status
└─ provenance_status
```

## Hard rule

```text
NO INVENTION BEFORE SOURCE LOCK
```

---

# 5. Stage 02 — Event Decomposition

A source is not necessarily one Event.

Examples:

```text
one paragraph → several claims/events
one historical artifact → production event + restoration event + discovery event
one meeting → request event + decision event + execution event
one image → visual observations + artifact-existence event
```

## Event boundary tests

A new Event candidate may be created when one or more of these materially changes:

- actor;
- state;
- action;
- result;
- time;
- location/context;
- controller;
- target;
- intent;
- causal relation;
- evidence status;
- Sequence scope.

## Event output

Each Event receives:

```text
EVENT-ID
Point Zero
source refs
Sequence ref
actor refs
object refs
prior state
resulting state
relations
orders
intent record
candidate combinations
memory refs
```

## Nested Events

A parent Event may spawn a Sub-Sequence with its own local Point Zero.

```text
PARENT EVENT
   ↓
SUB-SEQUENCE REQUEST
   ↓
LOCAL POINT ZERO
   ↓
LOCAL EVENT GRAPH
   ↓
RETURN PACKET
   ↓
PARENT ACCEPTS / REJECTS RETURN
```

---

# 6. Stage 03 — Existing Brain Activation

The runtime must search existing structures before inventing anything new.

Activation sources:

```text
Human parameters / containers
AI functions / mechanisms
Wisdom objects / source claims
ASI governance segments
Universal Sequence rubrics
ASI service Nodes
Engine bindings
prior Node Brains
Event memory
Intent memory
relation/path memory
patterns
Actor Views
actor-state memory
contradictions
```

## Activation record

For every hit:

```yaml
activation_id:
source_event_id:
object_id:
object_type:
activation_reason:
matched_features: []
activation_strength:
source_distance:
primary_or_secondary:
read_only: true|false
```

Activation strength is retrieval/relevance, not truth confidence.

---

# 7. Stage 04 — Relation, Order and Actor Graph

The system turns activated objects into an explicit graph.

## Core relation vocabulary

```text
produced_by
depends_on
supports
contradicts
causes
enables
blocks
before
after
contains
part_of
similar_to
different_from
actor_of
acted_on
requested_by
controlled_by
performed_by
benefits
observed_by
future_of
result_of
references
repairs
retests
supersedes
```

Relations must have provenance and epistemic status.

## Actor-role projection

For each Event, the runtime tries to populate independently:

```text
SUBJECT
REQUESTER
CONTROLLER
AUTHOR / DESIGNER
PERFORMER
CARRIER
BENEFICIARY
AUDIENCE
OBSERVER
```

Unknown is valid for any role.

---

# 8. Stage 05 — Node-Brain Activation

## What a Node Brain is

A Node Brain is the persistent local operating state attached to a service Node or accepted domain Node.

It contains a compact working view of everything currently relevant to that Node.

## Node-Brain load process

```text
NODE ACTIVATED
   ↓
LOAD NODE IDENTITY / TYPE
   ↓
LOAD LOCAL MEMORY
   ↓
LOAD ACTIVE EVENT / SEQUENCE
   ↓
LOAD PARAMETER/RUBRIC BINDINGS
   ↓
LOAD ACTOR VIEWS / ACTIVE STATES
   ↓
LOAD EVIDENCE / CONTRADICTIONS
   ↓
LOAD RECENT PATTERNS / FAILED PATTERNS
   ↓
LOAD THRESHOLDS / PERMISSIONS / LIMITS
   ↓
BUILD WORKING SNAPSHOT
```

## Node-Brain local state

```text
NODE BRAIN
├─ identity
├─ local Point Zero refs
├─ active Events
├─ active Sequences
├─ working memory
├─ long-term memory refs
├─ parameter/rubric activations
├─ actor/state refs
├─ intent refs
├─ relation refs
├─ evidence refs
├─ contradiction refs
├─ pattern refs
├─ candidate outputs
├─ thresholds
├─ permissions
├─ proof debt
├─ maturity
├─ recheck triggers
└─ write-back queue
```

Node memory should be selective. The global archive remains outside the Node; the Node stores references and locally important summaries/indices.

---

# 9. Stage 06 — Combination Engine

The Combination Engine is where reusable pieces become candidate new structures.

## Combination input sets

```text
A = observed source features
B = activated parameters/containers/rubrics
C = relations/orders
D = actor roles
E = actor active states
F = existing intents
G = existing patterns
H = retrieved memories
I = evidence constraints
J = future-state targets
```

The engine does not blindly compute a Cartesian product across everything. That would explode combinatorially.

It uses bounded combination passes.

## Pass C1 — adjacency combinations

Combine objects already directly connected by source position, Event relation, dependency, same actor, or same Sequence.

## Pass C2 — pattern-supported combinations

Combine structures where a previous pattern says the relation is reusable.

## Pass C3 — contradiction combinations

Generate alternatives specifically around contradictions.

## Pass C4 — counterfactual combinations

Change one important state/role/assumption while holding the rest stable.

## Pass C5 — cross-domain combinations

Combine Human/AI/Wisdom/ASI views only through Node-06 / allowed multi-rubric bindings.

## Pass C6 — novelty combinations

Try combinations not previously instantiated but composed entirely of known primitives and legal relations.

## Candidate output types

```text
SYNTHETIC_MEANING
EVENT_HYPOTHESIS
INTENT_HYPOTHESIS
ACTOR_BRAIN_VARIANT
SEQUENCE_VARIANT
EVIDENCE_PREDICTION
PATTERN_CANDIDATE
PRIMITIVE_CANDIDATE
```

## Combination explosion controls

Each execution envelope defines:

```text
max_candidates_per_pass
max_depth
max_origin_distance
max_cross_domain_edges
max_counterfactuals
novelty_threshold
minimum_relevance
```

Candidate generation halts when budgets are exhausted and records `PARTIAL / BUDGET_LIMIT` instead of pretending completeness.

---

# 10. Stage 07 — Live Intent Engine

The live intent engine builds intent from current semantic conditions.

## Inputs

```text
actor
Actor View
active state
current Event
current Sequence
activated parameters
relations
history
pressure
constraints
priority
resources
time horizon
possible future state
```

## Intent assembly frame

```text
ACTOR
   ↓
CURRENT STATE
   ↓
PERCEIVED DIFFERENCE
   ↓
TARGET / DESIRED FUTURE STATE
   ↓
WHY IT MATTERS (MOTIVE HYPOTHESIS)
   ↓
AVAILABLE ACTION TENDENCY
   ↓
CONSTRAINTS / RISKS
   ↓
TIME HORIZON
   ↓
EXPECTED CONSEQUENCE
   ↓
LIVE INTENT CANDIDATE
```

## Novelty test

Compare generated intent against existing Intent Memory.

If only wording changes:

```text
MATCH EXISTING INTENT
→ reinforce / attach Event
```

If structural dimensions change:

```text
NEW LIVE INTENT CANDIDATE
```

Material dimensions include:

```text
target
desired state change
priority
action tendency
constraint handling
relationship treatment
time horizon
expected consequence
controller/performer structure
```

---

# 11. Stage 07B — Future-State Reconstruction

For an observed result/artifact:

```text
OBSERVED RESULT
  ↓
POSSIBLE FUTURE STATE THAT PRODUCER WANTED
  ↓
POSSIBLE INTENT
  ↓
POSSIBLE CONTROLLER / REQUESTER
  ↓
POSSIBLE PRODUCTION EVENT
  ↓
REQUIRED PRIOR CONDITIONS
```

Multiple future-state hypotheses are kept in parallel until evidence separates them.

For the tablet class of tests, this allows:

```text
identity remembered
royal authority recognized
ritual repeated
succession accepted
institutional procedure preserved
territorial relation recognized
```

without claiming any is the historical translation.

---

# 12. Stage 08 — Evidence Prediction Engine

Every non-trivial synthetic hypothesis should produce evidence expectations.

For each candidate ask:

```text
IF TRUE:
- what additional source feature should exist?
- what related artifact should exist?
- what actor role should be visible?
- what chronological relation should hold?
- what grammar/mechanism should support it?
- what downstream result should occur?
- what contradictory evidence should be absent?
```

Output:

```yaml
evidence_prediction_id:
hypothesis_id:
expected_positive_evidence: []
expected_negative_evidence: []
expected_context: []
required_independent_sources: []
missing_evidence: []
observation_deadline_or_recheck:
```

---

# 13. Stage 09 — Reverse → Forward → Reverse

## Pass R1 — Reverse

Start from candidate result/meaning and reconstruct required prior conditions.

```text
candidate meaning
← actor intent
← actor state
← controller/requester
← dependencies
← prior events
← Point Zero
```

## Pass F — Forward

Start from reconstructed prior state and simulate expected legal consequences.

```text
Point Zero
→ conditions
→ intent
→ action/production
→ intermediate traces
→ result
→ future traces
```

## Pass R2 — Reverse Audit

Compare predicted traces with observed/current evidence.

```text
observed result
← does evidence support required path?
← are missing dependencies explainable?
← did another path fit better?
```

Output status:

```text
RETAIN
WEAKEN
REJECT
UNKNOWN
NEEDS_EVIDENCE
NEEDS_SUBSEQUENCE
```

---

# 14. Stage 10 — Falsifier, Contradiction and Maturity

## Falsifier types

```text
DIRECT_SOURCE_CONTRADICTION
MISSING_REQUIRED_DEPENDENCY
WRONG_ORDER
WRONG_ACTOR_ROLE
WRONG_TIME
WRONG_STATE
COUNTEREXAMPLE
ALTERNATIVE_WITH_BETTER_EVIDENCE
PREDICTION_FAILURE
SOURCE_PROVENANCE_FAILURE
UNRESOLVED_DAMAGE
```

A rejected candidate is not deleted. It becomes contradiction/falsifier memory.

## Maturity changes

Maturity can move both directions.

```text
M0 → M1 → M2 → M3 → M4 → M5
```

But new contradiction may cause:

```text
M4 → M2
```

or rejection.

No maturity lock is permanent unless the object is immutable source truth within its declared source scope.

---

# 15. Stage 11 — Write-Back Decision

Not every runtime output becomes memory.

Write-back classes:

```text
WB0 NO_WRITE
WB1 TRACE_ONLY
WB2 EVENT_MEMORY
WB3 RELATION/PATH_MEMORY
WB4 INTENT/ACTOR_STATE_MEMORY
WB5 PATTERN_CONTRIBUTION
WB6 PATTERN_CANDIDATE
WB7 CANDIDATE_NODE
WB8 CANDIDATE_PRIMITIVE
WB9 APPROVED_ID / APPROVED_PATTERN
```

Approval authority increases as the class gets stronger.

Automatic runtime may freely create lower-authority trace/candidate objects within configured scope, but canonical native registry changes require their defined review/governance contract.

---

# 16. Stage 12 — Memory Brain

Memory is written at three levels.

## Level M1 — Node-local memory

Stores what this Node should retrieve quickly next time.

Examples:

- recent successful route;
- important contradiction;
- active actor-state pattern;
- local evidence rule;
- threshold history;
- rejected combination signature.

## Level M2 — Sequence memory

Stores what happened in this complete scoped Sequence.

Includes:

- Event graph;
- actor-role assignments;
- decisions;
- evidence;
- rejected alternatives;
- closure;
- future seeds.

## Level M3 — Global memory index

Indexes reusable objects across all Nodes/Sequences.

Search keys can include:

```text
source
Event type
Point Zero class
actor
actor role
state
intent
relation
path
pattern
contradiction
future state
parameter/container
Node service
maturity
```

Global memory index points to objects; it should not duplicate/flatten all source content.

---

# 17. Memory Read Conditions

A Node may retrieve memory when one or more triggers match:

```text
same Event type
same actor
same actor-state family
same intent structure
same source/artifact family
same parameter activation
same relation signature
same path signature
same contradiction
same future-state target
same pattern
same Point-Zero type
```

Retrieval must return:

```text
object ID
why retrieved
similarity/relevance
source independence information
maturity
epistemic status
contradictions
```

---

# 18. Memory Write Conditions

A memory write should require:

```text
source/provenance retained
Event/Sequence ref exists
object type known
status assigned
maturity assigned
origin distance assigned where relevant
parent links known
contradiction links retained
write authority permits class
```

For synthetic candidates:

```text
synthetic = true
historical_fact = false
```

until evidence and approval change status.

---

# 19. Stage 13 — Auto-Link Engine

The auto-link engine operates after each accepted persistent write.

## Link passes

### A1 Source linkage

```text
same source_ref
same source fragment
same Point Zero
```

### A2 Structural linkage

```text
same parent
same container
same parameter/rubric
same Node service
```

### A3 Event linkage

```text
same Event family
before/after
causal/dependency adjacency
same result
same actor
```

### A4 Intent linkage

```text
same target
different horizon
same desired future state
different actor
same motive family
contradictory intent
```

### A5 Pattern linkage

```text
supports pattern
counterexample to pattern
specialization of pattern
instance of pattern
```

### A6 Contradiction linkage

```text
contradicts
supersedes
repaired_by
retested_by
```

### A7 Future linkage

```text
future_of
seeded_by
expected_result_of
```

## Link rules

```text
LINK != MERGE
SIMILAR != SAME
REPEATED != INDEPENDENT EVIDENCE
```

Every auto-created link records generator, rule, source objects, timestamp/version and confidence/relevance.

---

# 20. Stage 14 — New Node Engine

## Why a new Node exists

A new Node is justified when a reusable object/state/service cannot be represented by existing Nodes without distortion or repeated ad-hoc exceptions.

## Candidate process

```text
UNEXPLAINED / UNREPRESENTABLE RESIDUAL
        ↓
SEARCH EXISTING NODE TYPES
        ↓
can represent cleanly?
   ├─ YES → attach relation/memory
   └─ NO
        ↓
CREATE CANDIDATE NODE
        ↓
assign temporary ID
        ↓
source/provenance packet
        ↓
parent / child / relation packet
        ↓
R-F-R
        ↓
falsifier / counter-case
        ↓
reusability test
        ↓
maturity threshold
        ↓
governance approval if required
        ↓
PERMANENT NODE ID
        ↓
auto-link + memory initialization
```

## Candidate Node state

```text
CANDIDATE_OPEN
CANDIDATE_TESTING
CANDIDATE_WEAKENED
CANDIDATE_REJECTED
CANDIDATE_RETAINED
APPROVED_NODE
```

Rejected Nodes remain retrievable as failed structure memory.

---

# 21. New Parameter / Header / Rubric Integration

When a new primitive or header is proposed, the runtime must not simply append a name.

Required integration sequence:

```text
NEW CANDIDATE
↓
source/provenance
↓
existing IDs insufficient?
↓
definition + boundary
↓
parent/header/container
↓
Sequence roles
↓
Node bindings
↓
read/write channels
↓
relations
↓
examples + counterexamples
↓
falsifier
↓
R-F-R
↓
approval
↓
permanent ID
↓
auto-index + auto-link
```

## Required header metadata

```yaml
id:
name:
type:
parent_ids: []
source_refs: []
definition:
boundary:
allowed_children: []
sequence_roles: []
node_bindings: []
read_channels: []
write_channels: []
memory_effects: []
maturity:
epistemic_status:
review_status:
version:
```

---

# 22. Stage 15 — Growth Ledger

The Growth Ledger must distinguish source registries from learned Brain objects.

## Source registry counts

Examples:

```text
Human functional source parameters = fixed/versioned native count
AI source functions = fixed/versioned source count
Wisdom source objects = source-bound count
ASI governance registry = approved count
```

These do not change merely because a new example appears.

## Persistent learned counts

```text
Event Memory IDs
Intent Memory IDs
Relation IDs
Path IDs
Actor View IDs
Actor-State IDs
Combination IDs
Evidence Prediction IDs
Falsifier IDs
Pattern Contribution IDs
Pattern Candidate IDs
Sequence Memory IDs
Node Brain IDs
Seed IDs
Primitive Candidate IDs
Approved Primitive IDs
```

## Acceptance rule

```text
accepted_growth_batch =
    persistent_count_after > persistent_count_before
```

If nothing durable was learned, the run may still be a valid analysis/test run, but it is not accepted as a growth batch.

---

# 23. Stage 16 — Seed and Recheck Scheduler

A closed run may create one or more Seeds.

Seed examples:

```text
WAIT_FOR_EXTERNAL_EVIDENCE
RECHECK_WHEN_NEW_SOURCE_ARRIVES
RETEST_AFTER_REPAIR
COMPARE_WITH_NEXT_SIMILAR_EVENT
MATURE_PATTERN_AFTER_N_INDEPENDENT_CASES
REVISIT_CONTRADICTION
CHECK_FUTURE_RESULT
```

A Seed is latent. It is **not** an open Sequence.

When trigger + threshold become true:

```text
SEED
  ↓
CREATE NEW SEQUENCE ID
  ↓
OPEN LEDGER
  ↓
RUN
```

---

# 24. Nine Primary Runtime Loops

## L1 Retrieval Loop

Purpose: retrieve relevant Brain state.

```text
Event
→ search Node/local/global memory
→ rank relevance
→ load evidence/contradictions
→ return working set
```

Stop when relevance floor or retrieval budget reached.

---

## L2 Combination Loop

Purpose: create legal new combinations.

```text
working set
→ adjacency combinations
→ pattern combinations
→ counterfactual combinations
→ cross-domain combinations
→ novelty combinations
```

Stop on candidate budget, diminishing novelty, barrier or contradiction requiring external evidence.

---

## L3 Intent Loop

Purpose: generate/match intent.

```text
actor/state/event/future difference
→ live intent candidates
→ compare with intent memory
→ merge paraphrase OR create candidate
```

Stop when candidate set stabilizes or evidence cannot distinguish alternatives.

---

## L4 Evidence Loop

Purpose: ask what reality should contain if each candidate is true.

```text
candidate
→ predicted evidence
→ retrieve/check evidence
→ update support/debt
```

Stop when evidence exhausted or new source retrieval required.

---

## L5 R-F-R Loop

Purpose: attack candidate causal structure.

```text
reverse
→ forward
→ reverse audit
```

Can iterate more than once only when a materially new dependency/evidence item enters. Repeating identical route is not independent confirmation.

---

## L6 Contradiction Loop

Purpose: preserve and classify conflicts.

```text
new object
→ compare with active claims/patterns
→ contradiction?
→ classify
→ generate alternatives/counter-sequence
```

Contradiction may block promotion without blocking memory write.

---

## L7 Memory Reinforcement Loop

Purpose: improve retrieval and pattern support.

```text
accepted result
→ update local memory
→ update Sequence memory
→ update global index
→ strengthen supported links
```

Frequency does not equal truth.

---

## L8 Node-Growth Loop

Purpose: turn repeated irreducible residuals into candidate Nodes/patterns/primitives.

```text
repeated residual
→ existing structure insufficient?
→ candidate Node/primitive
→ R-F-R
→ promotion or rejection
```

---

## L9 Next-Sequence Loop

Purpose: keep the system alive across time without reopening closed Sequences.

```text
closure
→ unresolved future condition
→ Seed
→ trigger watch
→ new Sequence when threshold true
```

---

# 25. Four Background Maintenance Loops

## B1 Recheck Loop

Periodic re-evaluation of open/weak hypotheses when new evidence appears.

## B2 Orphan-Link Loop

Find persistent objects with insufficient graph connectivity and attempt legal links.

An orphan is not automatically wrong. It may be a genuinely novel island.

## B3 Maturity-Upgrade Loop

Recompute maturity when independent evidence, falsifiers, counter-cases or repeated cross-domain instances change.

## B4 Scheduler / Auto-Sustain Loop

Controls when other loops run.

It enforces:

- execution budget;
- write authority;
- action authority;
- concurrency;
- backoff;
- retry policy;
- source availability;
- trigger/threshold conditions;
- human/authorized review gates.

---

# 26. How Many Loops Can One Event Create?

There is **no fixed number of iterations per Event**.

The system has 13 loop classes, but an Event activates only those needed.

Typical simple Event:

```text
L1 Retrieval
L3 Intent
L4 Evidence
L5 R-F-R
L7 Memory
L9 Seed
```

Complex tablet/historical Event:

```text
L1 Retrieval
L2 Combination
L3 Intent
L4 Evidence
L5 R-F-R
L6 Contradiction
L2 Combination again with counter-case
L5 R-F-R again if NEW evidence/dependency exists
L7 Memory
L8 Node Growth if irreducible residual repeats
L9 Next Sequence
```

Loop counters must record:

```yaml
loop_id:
loop_type:
iteration:
new_information_entered: true|false
objects_created: []
objects_changed: []
stop_reason:
```

A loop may not keep running merely because the previous output was unsatisfying.

---

# 27. Automatic Operation Proposal

## Manual mode — current/early phase

Human supplies input and often asks what to test next.

System performs bounded execution and writes reviewed growth.

## Semi-auto mode

System automatically performs:

```text
decomposition
activation
retrieval
combination
intent synthesis
evidence prediction
R-F-R
candidate write-back
```

Human/authorized controller reviews promotion of stronger objects.

## Auto-grow mode

System automatically creates and links candidate memory/relations/patterns, schedules rechecks, and runs allowed Seeds.

Human/authorized controller mainly handles:

- disputed authority;
- native-registry promotion;
- external actions;
- safety/permission exceptions;
- high-impact closure.

## Scheduled self-sustaining mode

The runtime watches authorized input/event channels and Seed triggers.

```text
EVENT ARRIVES
→ AUTO RUN
→ GROWTH / MEMORY
→ AUTO LINK
→ SEED
→ WAIT
→ FUTURE EVENT
```

The system remains bounded by permissions and resource policies.

---

# 28. Self-Sustain Scheduler Pseudocode

```python
while scheduler_enabled:
    triggers = collect_due_triggers()

    for trigger in triggers:
        if not trigger_is_authorized(trigger):
            record_block(trigger, "AUTHORITY")
            continue

        envelope = create_execution_envelope(trigger)
        source_packet = lock_source_and_point_zero(envelope)
        events = decompose_events(source_packet)

        for event in events:
            activation = activate_existing_brain(event)
            relations = build_relation_actor_graph(event, activation)
            node_brains = load_relevant_node_brains(event, relations)
            candidates = generate_bounded_combinations(event, node_brains)
            intents = generate_or_match_live_intents(event, candidates)
            predictions = predict_evidence(event, candidates, intents)
            rfr_results = run_rfr(event, candidates, predictions)
            reviewed = apply_falsifiers_contradictions_maturity(rfr_results)
            write_decisions = decide_writeback(reviewed, envelope.authority)
            persisted = write_memory(write_decisions)
            links = auto_link(persisted)
            growth = update_growth_ledger(persisted)
            seeds = create_next_sequence_seeds(reviewed, growth)
            schedule_legal_rechecks(seeds)

        close_execution_envelope(envelope)

    sleep_until_next_trigger_window()
```

This pseudocode is architectural only; implementation will be split into separate engines in later batches.

---

# 29. Auto-Link Pseudocode

```python
def auto_link(new_object):
    candidate_links = []

    candidate_links += by_same_source(new_object)
    candidate_links += by_same_point_zero(new_object)
    candidate_links += by_event_family(new_object)
    candidate_links += by_actor_and_role(new_object)
    candidate_links += by_parameter_activation(new_object)
    candidate_links += by_relation_signature(new_object)
    candidate_links += by_intent_structure(new_object)
    candidate_links += by_future_state(new_object)
    candidate_links += by_pattern_family(new_object)
    candidate_links += by_contradiction_family(new_object)
    candidate_links += by_sequence_family(new_object)

    candidate_links = dedupe_links(candidate_links)

    for link in candidate_links:
        if passes_link_threshold(link) and not violates_identity_boundary(link):
            persist_link(link)
        else:
            preserve_as_link_candidate(link)
```

---

# 30. New-Node Pseudocode

```python
def evaluate_new_node(residual, context):
    matches = search_existing_nodes(residual, context)

    if any(can_represent_without_distortion(m, residual) for m in matches):
        target = best_existing_node(matches)
        add_memory_and_relation(target, residual)
        return {"result": "REUSED_EXISTING_NODE", "node_id": target.id}

    candidate = create_candidate_node(residual, context)
    attach_provenance(candidate)
    attach_parent_child_links(candidate)
    attach_falsifier(candidate)

    rfr = run_node_candidate_rfr(candidate)
    maturity = assess_node_maturity(candidate, rfr)

    if rfr.failed:
        persist_rejected_candidate(candidate, rfr)
        return {"result": "REJECTED", "candidate_id": candidate.id}

    if maturity < required_node_maturity(candidate):
        persist_open_candidate(candidate)
        schedule_recheck(candidate)
        return {"result": "OPEN_CANDIDATE", "candidate_id": candidate.id}

    if requires_authorized_promotion(candidate):
        queue_promotion_review(candidate)
        return {"result": "REVIEW_REQUIRED", "candidate_id": candidate.id}

    node = promote_to_permanent_node(candidate)
    initialize_node_memory(node)
    auto_link(node)
    return {"result": "APPROVED_NODE", "node_id": node.id}
```

---

# 31. Node-Brain Memory Cycle

```text
NEW EVENT
  ↓
GLOBAL INDEX FINDS NODE-BRAIN
  ↓
NODE BRAIN READS:
  local memory
  linked evidence
  linked contradictions
  linked patterns
  actor-state history
  failed prior combinations
  ↓
NODE EXECUTES BOUNDED FUNCTION
  ↓
NEW RESULT
  ↓
NODE LOCAL WRITE
  ↓
SEQUENCE MEMORY WRITE
  ↓
GLOBAL INDEX LINK
  ↓
NODE IS STRONGER / MORE SPECIFIC FOR NEXT EVENT
```

Important:

```text
NODE MEMORY GROWTH
!= NODE BECOMES UNBOUNDED
```

Old low-value details may be compressed into references/patterns, but original source-linked records remain available in authoritative storage.

---

# 32. Combination-Memory Cycle

```text
Event A
→ Combination C1
→ retained
→ Memory

Event B
→ retrieves C1
→ combines C1 with new relation R7
→ Combination C2
→ survives R-F-R
→ Pattern Contribution P3

Event C
→ retrieves C1 + C2 + P3
→ creates Combination C9 never explicitly shown before
```

This is the core maturation target: **new combinations from accumulated reusable structures**.

---

# 33. Tablet Synthetic Discovery Example

```text
TABLET IMAGE
↓
Source Lock / Point Zero
↓
Visual classes SG-A..SG-J
↓
relations: position / neighbor / repetition / enclosure / damage
↓
Combination Engine
↓
SYNTH-001..036 + future synthetic combinations
↓
Event hypotheses
↓
Intent hypotheses
↓
Actor-role branches
↓
Same-actor different-state branches
↓
Future-state reconstruction
↓
Evidence predictions
↓
R-F-R
↓
M0..M5 maturity
↓
retain / weaken / reject / unknown
↓
Pattern Contributions + Memory
↓
new tablet/event run starts with larger Brain
```

No synthetic meaning is promoted to historical translation without source/philological evidence.

---

# 34. Stop Conditions

A run or loop stops when any relevant condition is met:

```text
DECLARED_END_REACHED
CLOSED_SUCCESS
CLOSED_FAILURE
CLOSED_PARTIAL
CLOSED_UNKNOWN
CLOSED_UNAVAILABLE
NOT_APPLICABLE
ABORTED
WAITING_FOR_TRIGGER
WAITING_FOR_THRESHOLD
WAITING_FOR_DEPENDENCY
WAITING_FOR_RETURN
INSUFFICIENT_EVIDENCE
CONTRADICTION_REQUIRES_EXTERNAL_SOURCE
COMPUTE_BUDGET_REACHED
CANDIDATE_BUDGET_REACHED
ORIGIN_DISTANCE_LIMIT_REACHED
AUTHORITY_BARRIER
HUMAN_OR_AUTHORIZED_REVIEW_REQUIRED
```

Open/unknown is valid. The runtime never forces an answer simply to terminate.

---

# 35. Auto-Sustain Safety Boundary

Self-sustaining memory/thought growth and external action authority are different.

The runtime may be allowed to autonomously:

- create candidate combinations;
- create candidate intents;
- create evidence predictions;
- write bounded memory;
- add relations;
- add Pattern Contributions;
- create Seeds;
- run rechecks;
- create review-gated candidate Nodes/primitives.

It may **not automatically acquire external authority** merely because its internal confidence/maturity increased.

External execution remains governed by controller, permission, threshold and ASI governance contracts.

---

# 36. Build Decomposition

This master flow is implemented in stages.

## Batch 1 — foundation

```text
Constitution
Execution Flow Master
System Invariants
Event schema
Intent schema
Node-Brain schema
Memory schema
Combination schema
```

## Batch 2 — persistent registries

```text
Event Registry
Intent Registry
Node-Brain Registry
Memory Registry
Combination Registry
Pattern Candidate Registry
Growth Batch Registry
Primitive Candidate Registry
```

## Batch 3 — intake/runtime core

```text
Source Lock Engine
Event Decomposition Engine
Parameter Activation Engine
Relation Graph Engine
Actor Role Engine
Actor State Engine
```

## Batch 4 — generative discovery core

```text
Combination Engine
Live Intent Engine
Future State Engine
Evidence Prediction Engine
R-F-R Engine
Falsifier Engine
Maturity Engine
```

## Batch 5 — persistent growth core

```text
New Node Engine
Memory Writeback Engine
Auto-Link Engine
Growth Batch Engine
Seed Engine
```

## Batch 6 — self-sustain core

```text
Scheduler
Recheck Engine
Orphan Link Engine
Self-Sustain Controller
Loop budgets / authority controls
```

## Batch 7 — render/link

```text
Graph Render Contract
Node Renderer
Memory Renderer
Sequence Renderer
Tablet Hypothesis Renderer
Dashboard Renderer
```

---

# 37. Final Runtime Contract

The system should eventually operate as:

```text
AUTHORIZED EVENT ARRIVES
        ↓
SOURCE + POINT ZERO LOCKED
        ↓
EVENTS CREATED
        ↓
EXISTING BRAIN ACTIVATED
        ↓
NODE BRAINS RETRIEVED
        ↓
RELATIONS + COMBINATIONS GENERATED
        ↓
LIVE INTENTS + FUTURE STATES GENERATED
        ↓
EVIDENCE PREDICTED
        ↓
R-F-R + FALSIFIERS
        ↓
MATURITY UPDATED
        ↓
MEMORY WRITTEN
        ↓
AUTO-LINKED
        ↓
NEW NODE / PATTERN / PRIMITIVE CANDIDATES WHEN NEEDED
        ↓
GROWTH LEDGER INCREASES
        ↓
SEEDS / RECHECKS SCHEDULED
        ↓
SYSTEM WAITS FOR NEXT LEGAL TRIGGER
```

The purpose of automation is not to remove governance. It is to remove the need for a human to manually tell Sourceborn every internal step of learning, linking, rechecking and memory growth.
