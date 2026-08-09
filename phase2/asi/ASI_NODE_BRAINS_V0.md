# Phase-2 ASI Node Brains v0

Status: `INSTANTIATED V0 — ACTIVE REVIEW`

Machine registry: `registries/asi/node_brains_v0.json`

The 18 ASI Nodes are service classes. They are not a new chronological Sequence spine.

```text
REAL CASE GRAPH
      ↓
invokes only the ASI services it needs
      ↓
actual causal/dependency/control order decides invocation order
```

## Brain layout

```text
RAW ASK / DECLARED EVENT
          ↓
┌──────────────────────────────────────┐
│ NB-00 END / SCOPE LOCK               │
└──────────────────────────────────────┘
          ↓
┌──────────────────────────────────────┐
│ NB-01 REVERSE MINER / PROVENANCE     │
└──────────────────────────────────────┘
          ↓
     CASE GRAPH FORMS
          │
          ├──────────────→ NB-02 STATE / IDENTITY / RELATION
          ├──────────────→ NB-03 DRIVER / RULE / PRIORITY
          ├──────────────→ NB-04 TRIGGER / THRESHOLD
          ├──────────────→ NB-05 DEPENDENCY / BARRIER
          ├──────────────→ NB-06 RUBRIC ACTIVATION
          ├──────────────→ NB-07 EVIDENCE / TEST
          ├──────────────→ NB-08 ALTERNATIVE / ARBITRATION
          ├──────────────→ NB-09 COUPLING / DYNAMICS
          ├──────────────→ NB-10 RESULT / ENTITY OUTCOME
          ├──────────────→ NB-11 VERIFICATION / ACCEPTANCE
          ├──────────────→ NB-12 TRACE / MEMORY / LEARNING
          ├──────────────→ NB-13 COMPRESSION / INHERITANCE
          ├──────────────→ NB-14 CLOSURE / RETURN / SEED
          ├──────────────→ NB-15 PATTERN / LAW / WRITER
          ├──────────────→ NB-16 R-F-R FALSIFIER
          └──────────────→ NB-17 META-CONTROLLER
```

## Runtime contract

```text
NODE / EDGE WANTS TO FIRE
          ↓
NB-04
TRIGGER OCCURRED?
THRESHOLD TRUE?
          │
      ┌───┴───┐
      │       │
     NO      YES
      │       │
  wait for    ↓
 declared   NB-05
 recheck    dependencies ready?
              │
          ┌───┴────────┐
          │            │
         YES           NO
          │            │
          │       SUB-SEQUENCE CONTRACT
          │            ↓
          │       OPEN LEDGER ENTRY
          │            ↓
          │       SUB-SEQUENCE RUNS
          │            ↓
          │          CLOSES
          │            ↓
          │       RETURN PACKET
          │            ↓
          │       ACCEPTED?
          │       ┌────┴────┐
          │      YES        NO
          │       │          │
          └───────┘      new legal
              ↓          resolution Sequence
            NB-06
      activate Human/AI/
      domain rubric state
              ↓
            NB-09
      execute interaction /
      dynamics / tool path
              ↓
            NB-10
      result + entity outcome
              ↓
            NB-11
      verify + accept/reject
              ↓
            NB-12
      trace / memory / learning
              ↓
            NB-16
      R-F-R falsification
              ↓
            NB-14
      closure / return / seed
```

## Parallel execution and synchronization

```text
                MAIN S0
                  │
        ┌─────────┼─────────┐
        ↓         ↓         ↓
       S1        S2        S3
    REQUIRED   OPTIONAL   REQUIRED
        │         │         │
      CLOSE      ...      CLOSE
        │                   │
        └──────────┬────────┘
                   ↓
             NB-05 / NB-17
              SYNC BARRIER
                   ↓
     required terminal returns accepted?
             ┌─────┴─────┐
            NO          YES
             │            │
          BLOCK          JOINT
          EDGE           EVENT
```

## No in-place loop

```text
WRONG
TEST → FAIL → TEST → FAIL → TEST

CORRECT
TEST S1
  ↓
CLOSE FAILURE
  ↓
RETURN
  ↓
REPAIR S2
  ↓
CLOSE
  ↓
RETURN
  ↓
RETEST S3
  ↓
CLOSE SUCCESS
  ↓
RETURN
  ↓
PARENT CONTINUES
```

## Node Brain ownership

| Brain | Owns |
|---|---|
| NB-00 | End, scope, closure scope |
| NB-01 | Reverse mining, provenance, gaps |
| NB-02 | State, identity continuity, relations |
| NB-03 | Driver, rules, promises, priorities, exceptions |
| NB-04 | Trigger, threshold, WHY NOW |
| NB-05 | Dependencies, availability, barriers, sync |
| NB-06 | Human/AI/domain rubric activation |
| NB-07 | Evidence, testing, qualification, contradiction |
| NB-08 | Options, selection, arbitration, counter-sequences |
| NB-09 | Encounter, coupling, dynamics, tool execution |
| NB-10 | Result set, entity outcome, latent result, event weight |
| NB-11 | Verification and return acceptance |
| NB-12 | Trace, memory, learning/write-back |
| NB-13 | Compression, expansion, inheritance |
| NB-14 | Closure Packet, return, Seed Registry |
| NB-15 | Pattern, law, narrative/observer-writer sequences |
| NB-16 | Reverse → Forward → Reverse falsification |
| NB-17 | Cross-sequence coordination, convergence and meta-control |

## Locked separation

```text
DRIVER
≠ CONTROLLER
≠ PERFORMER
≠ CARRIER
```

```text
GLOBAL REALITY
≠ ACTOR VIEW
```

```text
SEQUENCE TERMINAL STATUS
≠ ENTITY OUTCOME
```

```text
SUB-SEQUENCE CLOSED
≠ RETURN ACCEPTED
```

## Closure

This instantiation closes the Phase-2 task of defining a usable v0 contract for every ASI service node.

It does not close ASI Node development itself. Phase-2 must still bind approved Human/AI registries, run sample Sequences, and revise any Node Brain contract that fails those cases.
