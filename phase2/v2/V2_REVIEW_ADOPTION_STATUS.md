# Universal Sequence V2 — Phase-2 Adoption Status

Status: `LOCK CANDIDATE — NOT YET PHASE-1 CANONICAL REPLACEMENT`

The uploaded `SOURCEBORN_UNIVERSAL_SEQUENCE_V2_FINAL_REVIEW.md` is a later review/consolidation of the two Phase-1 Sequence sources. Its source-level verdict is that V1 must not be locked as one numbered linear stage chain. It repairs the machine by separating mode, graph layers, cross-cutting services, first-class records, closure integrity, and the rubric splitter.

The exact raw attachment bytes are not currently mounted through the GitHub write connector. The repo therefore records source custody honestly in:

`raw/sequence/SOURCEBORN_UNIVERSAL_SEQUENCE_V2_FINAL_REVIEW.custody.json`

and stores machine materializations separately.

## Materialized V2 objects

```text
V2 SOURCE REVIEW
      ↓
CANONICAL GRAPH CANDIDATE
machine/v2/CANONICAL_GRAPH_V2_LOCK_CANDIDATE.json
      │
      ├── 4-mode router
      ├── Layers A–L
      └── F01–F28 repairs
      ↓
FIRST-CLASS RECORDS
machine/v2/FIRST_CLASS_RECORD_SCHEMAS.json
      │
      ├── Sequence template / instance
      ├── Node template / instance
      ├── Edge template / instance
      ├── Claim
      ├── Gap
      ├── Contradiction
      ├── Evidence
      ├── Proof Debt
      ├── Identity Decision
      ├── Compression Contract
      ├── Open Ledger
      ├── Seed
      ├── Actor View
      └── Closure Packet
      ↓
CROSS-CUTTING SERVICES
SVC-01 ... SVC-18
      ↓
TYPED NULL SEMANTICS
8 distinct missing/error states
      ↓
MAXIMUM RUBRIC REGISTRY
R01 ... R52
987 dimensions
      ↓
PARAMETER / SUB-PARAMETER ENGINE
behavior-changing split only
      ↓
RUBRIC PACK ↔ ASI NODE BINDINGS
Phase-2 mapping v0
```

## Important V2 changes to earlier assumptions

### 1. End-first is mode-specific

```text
RECONSTRUCTION
observed end → reverse → forward → reverse → closure

EXECUTION
current target/contract → forward → verify → audit if closing

DISCOVERY
event stream → candidate segmentation → authorized selection

AUDIT
closed reference → new Audit Sequence → old Sequence remains closed
```

### 2. Acceptance contract is universal; Requirement is not

Natural dynamics can have no need/want/goal/requirement while still being analyzed under a Sequence contract.

### 3. Natural dynamics is a mechanism, not a Controller

```text
driver_presence
controller_presence
transition_mechanism
```

remain separate.

### 4. Progression and terminal closure are different

An unaccepted required return blocks a dependent success path. It does not necessarily prevent the parent from terminally closing `FAILURE`, `UNKNOWN`, `UNAVAILABLE`, etc., if the parent contract permits that terminal state.

### 5. Pass-3 is before immutable closure

```text
Closure Candidate
↓
Pass-3 Integrity Audit
↓
Closure Readiness
↓
Immutable Closure
```

Any later attack is a new `REFERENCE/AUDIT` Sequence.

### 6. Claims and edges are first-class

A node may contain many claims with different sources and confidence, so provenance cannot remain only at node level.

Every executable edge must explicitly carry its trigger, threshold, evaluator, evaluation policy, recheck policy, timeout, uncertainty policy, dependencies and barrier.

### 7. Concurrency is a machine problem

Parallel Sequences need lock/wait/deadlock/starvation/race/timeout/transaction/merge/synchronization semantics, not merely drawing multiple arrows.

### 8. Trace and Memory are different

```text
TRACE
persistent consequence/path evidence

MEMORY
trace/record/state encoded or addressable for later retrieval/reuse
```

### 9. Rubrics are orthogonal split dimensions

A parameter does not split merely because two rubric values can be crossed.

A split becomes a candidate only when the distinction changes machine behavior such as threshold, dependency, evidence, controller, identity, transition, result, closure, memory, verification, risk/priority, provenance, contradiction handling or downstream behavior.

## Current V2 gate

V2 is ready for Phase-2 testing as a lock candidate.

It does **not** yet rewrite the Phase-1 canonical pointer because:

1. the raw V2 attachment has not yet been byte-preserved in the repo;
2. the V2 machine materializations still need R-F-R tests against bounded cases;
3. Human native 2,560 rows are still absent;
4. AI candidate-native adoption is still open.

Canonical replacement must happen through a dedicated `V2_ADOPTION_CLOSURE_PACKET`, never by editing historical Phase-1 execution records.
