# Mahabharata Sequence — Phase-2 Test Contract v0

Status: `TEST CONTRACT ONLY — SOURCE INGESTION NOT YET PERFORMED`

This file converts the working discussion into testable Sequence contracts without treating discussion-level interpretations as source fact.

Mandatory separation:

```text
AUTHORITATIVE / SELECTED SOURCE TEXT
        ↓
EXTRACTED EVENT / RULE / PROMISE / RELATION
        ↓
ACTOR VIEW
        ↓
SEQUENCE GRAPH
        ↓
SOURCEBORN INTERPRETATION / PATTERN
```

Until source records are ingested, the patterns below remain `USER_SUPPLIED_INTERPRETATION` / `TEST HYPOTHESIS`.

---

## MHB-T01 — Karna → Arjuna final confrontation

### PASS 0

```text
DECLARED END
Karna–Arjuna confrontation reaches its terminal battlefield result.

SCOPE
Only events/conditions closure-critical to that declared confrontation.

CLOSURE CONDITION
Every required predecessor is sourced or explicitly unknown;
forward reconstruction reaches the declared result;
PASS 3 leaves no required unexplained causal/dependency edge.
```

### Reverse questions

```text
FINAL RESULT
↑
immediate battlefield state
↑
capability / vulnerability state of both actors
↑
weapon / knowledge / training state
↑
rule / promise / exception state
↑
alliance / role state
↑
identity and knowledge-distribution state
↑
earlier protection / armour-earring events
↑
Kunti/Karna birth and separation sequence
↑
earliest closure-critical seed within declared scope
```

### Required primitives to test

```text
SEED BEFORE CARRIER
ACTOR VIEW
KNOWLEDGE DISTRIBUTION
LATENT RESULT
DOWNSTREAM-CRITICAL EVENT
PROMISE AS FUTURE CODE
RULE / PRIORITY / EXCEPTION CONTRACT
CONTROLLER / PERFORMER / CARRIER
CONVERGENCE WINDOW
ENTITY OUTCOME
SEQUENCE CLOSURE
```

---

## MHB-T02 — Draupadi event → promise memory → later execution

Purpose: test whether an event can close locally while creating a future-action seed.

```text
EVENT S0
↓
RESULT / CONSEQUENCE
↓
PROMISE OR COMMITMENT CREATED
↓
S0 CLOSES
↓
PROMISE STORED AS SEED / MEMORY
↓
YEARS / EVENTS PASS
↓
ACTIVATION CONDITION MATCHES
↓
NEW SEQUENCE S1
↓
ACTION / FULFILMENT / FAILURE
↓
S1 CLOSES
```

This test specifically attacks the forbidden model:

```text
one promise Sequence stays open for years
```

Expected architecture:

```text
promise-creation Sequence closes;
future fulfilment is a new Sequence referencing the old closure.
```

---

## MHB-T03 — Rule conflict / exception contract

Purpose: test local rule, higher objective, promise, priority and exception handling without calling every rule violation a Sequence failure.

```text
RULE A
+
RULE B / PROMISE / OBJECTIVE
↓
CONFLICT
↓
PRIORITY / ARBITRATION
↓
EXCEPTION CONTRACT?
├── NO → rule remains binding
└── YES
      ↓
terms
controller authority
scope
cost/consequence
      ↓
action
      ↓
record:
FOLLOWED / BROKEN / OVERRIDDEN / NOT-APPLICABLE
```

PASS 3 must ask whether the exception was actually supported by source evidence or is only interpretation.

---

## MHB-T04 — Krishna line as Meta-Controller pattern

This is an architectural hypothesis, not a source claim.

Test whether one narrative line can function as:

```text
CROSS-SEQUENCE KNOWLEDGE HOLDER
+
TIMING / CONVERGENCE COORDINATOR
+
LOCAL-SEQUENCE INTERVENTION SOURCE
+
ERA-CLOSURE REFERENCE LINE
```

without incorrectly assuming:

```text
Krishna directly caused every event
or
every actor knew what the meta-controller knew.
```

Required representation:

```text
GLOBAL REALITY
        │
        ├── Krishna View
        ├── Arjuna View
        ├── Karna View
        ├── Kunti View
        └── other Actor Views
```

Each action must use the actor's View State, not Global Reality.

---

## MHB-T05 — War as convergence window, not origin

```text
SEQUENCE A ────────────┐
SEQUENCE B ────────────┤
SEQUENCE C ────────────┤
PROMISE D ─────────────┤
LINEAGE E ─────────────┤
ALLIANCE F ────────────┤
RULE CONFLICT G ───────┤
                       ↓
              CONVERGENCE WINDOW
                       ↓
                  WAR EXECUTION
```

The test asks:

```text
Which older Sequences had to reach terminal/ready states
before the shared execution window became possible?
```

This validates parallel Sequence development and synchronization barriers.

---

## MHB-T06 — Era closure vs war closure

Purpose: prevent scope collapse.

```text
BATTLE CLOSURE
≠
WAR CLOSURE
≠
DYNASTIC CLOSURE
≠
PERSON-LIFE CLOSURE
≠
ERA CLOSURE
```

Each closure requires its own scope and packet.

A lower closure may become an input to a higher closure but cannot silently terminate it.

---

## MHB-T07 — Observer / writer / guidance formation

Purpose: test the claim that a closed event history can later become compressed civilizational memory.

```text
EVENT / WAR SEQUENCES
↓
CLOSE
↓
TRACES / MEMORY / NARRATIVE MATERIAL
↓
NEW OBSERVER-WRITER SEQUENCE
↓
COLLECT
↓
ORDER
↓
COMPARE
↓
INTERPRET
↓
WRITE / TRANSMIT
↓
NARRATIVE MEMORY
↓
LATER READER SEQUENCE
↓
EXPAND / COMPARE / APPLY
```

Law/guidance formation is tested separately:

```text
MULTIPLE CLOSED CASES
↓
COMPARE CONSEQUENCES
↓
ABSTRACT PATTERN
↓
EXCEPTIONS
↓
RULE / RESTRICTION / GUIDANCE CANDIDATE
```

The resulting rule is not retroactively inserted into the earlier event as if it existed there first.

---

# Required source-ingestion fields

Before any test becomes a factual case graph, ingest records using:

`registries/holy_books/NARRATIVE_SOURCE_ADAPTER_SCHEMA.json`

Every extracted claim must include:

```text
source record id
location / citation
exact or faithful claim
actor(s)
actor view if supported
order type
causal/dependency status
rule/promise status
interpretation status
```

---

# Test order

```text
MHB-T01 Karna–Arjuna
        ↓
MHB-T02 Promise / latent seed
        ↓
MHB-T03 Rule conflict
        ↓
MHB-T05 Convergence window
        ↓
MHB-T04 Meta-controller hypothesis
        ↓
MHB-T06 Era closure
        ↓
MHB-T07 Observer/writer/law formation
```

The large global Mahabharata Sequence should be attempted only after the bounded tests close.
