```text
LARGE CLOSED PATH
↓
SELECT PRESERVED INVARIANTS
↓
COMPRESSED HANDLE
```

Mandatory handle fields:

```text
source_sequence_ids
preserved_invariants
discarded_or_unavailable_detail
valid_scope
assumptions
known_exceptions
epistemic_status
recoverability_grade
```

Recoverability:

```text
LOSSLESS
PARTIAL
LOSSY
IRREVERSIBLE
CURRENTLY_UNRECOVERABLE
CONTEXT_DEPENDENT
```

Expansion:

```text
HANDLE
+
CURRENT CONTEXT
+
EVIDENCE
↓
RECONSTRUCT AVAILABLE PATH
```

Never invent missing detail.

---

# 36. OBSERVER / WRITER / LAW FORMATION

Event Sequence and recording Sequence are separate.

```text
EVENT SEQUENCE
↓
CLOSE
↓
TRACES / MEMORIES
↓
NEW OBSERVER / WRITER SEQUENCE
↓
COLLECT
↓
SELECT
↓
ORDER
↓
COMPARE
↓
INTERPRET
↓
RECORD
↓
NARRATIVE MEMORY
```

Therefore:

```text
EVENT REALITY
≠
RECORDED REALITY
≠
LATER INTERPRETATION
```

Law/guidance formation:

```text
MULTIPLE CLOSED CASES
↓
COMPARISON
↓
REPEATING RELATIONS
↓
EXCEPTIONS
↓
GENERALIZATION
↓
RULE CANDIDATE
↓
COMPROMISE / AGREEMENT /
RESTRICTION / PERMISSION /
FUTURE-ACTION CONDITION
↓
LAW / GUIDANCE / PROCEDURE
↓
PRIOR REALITY FOR LATER SEQUENCES
```

---

# 37. CLOSURE READINESS

Before Sequence Closure:

```text
CHECK:
1. contract terminal condition reached
2. closure scope explicit
3. result set recorded
4. entity outcomes recorded
5. required verification status recorded
6. all required Sub-Sequences terminal
7. all required returns accepted or terminally rejected
8. trace written
9. memory written as required
10. unknowns explicitly recorded
11. epistemic statuses attached
12. next-sequence seeds identified
13. PASS 3 completed
```

If any required item is missing:

```text
NOT READY
↓
DO NOT CLOSE
↓
IDENTIFY EXACT BLOCK
↓
OPEN REQUIRED SEQUENCE
OR
CLOSE FAILURE/UNKNOWN IF CONTRACT ALLOWS
```

---

# 38. CLOSURE PACKET

```text
CLOSURE_PACKET {
    sequence_id
    sequence_name

    closure_scope
    closure_status

    declared_end
    starting_reality
    final_reality

    result_set[]
    entity_outcomes[]

    effect_records[]
    event_weight_records[]

    related_sequence_ids[]
    sub_sequence_terminal_statuses[]

    verification_status

    trace_ids[]
    memory_ids[]
    narrative_memory_ids[]

    compression_handle_ids[]

    unresolved_conditions[]
    epistemic_summary

    inherited_outputs[]
    next_sequence_seeds[]

    prior_sequence_references[]

    driver
    controller
    performer
    carrier

    pass3_status
}
```

This is the permanent return object.

---

# 39. COMPLETE NODE EXECUTION LOOP

```text
ENTER SEQUENCE NODE
        ↓
LOAD:
current state
prior reality
node contract
actor views
rubric bindings
        ↓
IDENTIFY DRIVER
        ↓
IDENTIFY CONTROLLER / PERFORMER / CARRIER
        ↓
CHECK TRIGGER
   ├── absent
   │     ↓
   │  WAIT FOR DECLARED EVENT
   │
   └── occurred
          ↓
      EVALUATE THRESHOLD
          ├── FALSE
          │      ↓
          │  WAIT FOR DECLARED RECHECK
          │
          └── TRUE
                 ↓
             CHECK DEPENDENCIES
                 ├── missing / unaccepted
                 │      ↓
                 │  OPEN SUB-SEQUENCE(S)
                 │      ↓
                 │  REGISTER LEDGER
                 │      ↓
                 │  EXECUTE
                 │      ↓
                 │  CLOSE
                 │      ↓
                 │  RETURN PACKET
                 │      ↓
                 │  RE-EVALUATE NODE
                 │
                 └── READY
                        ↓
                  ACTIVATE RUBRIC SETS
                        ↓
                  BUILD TEMPORARY STATE
                        ↓
                  EXECUTE TRANSITION
                        ↓
                  RECORD STATE CHANGE
                        ↓
                  RECORD ENTITY OUTCOME
                        ↓
                  RECORD EFFECT / RESULT
                        ↓
                  RECORD EVENT WEIGHT
                        ↓
                  WRITE TRACE / LEARNING
                        ↓
                  NODE CONTRACT COMPLETE?
                       ├── NO
                       │    ↓
                       │ OPEN REQUIRED SEQUENCE
                       │    ↓
                       │ CLOSE / RETURN
                       │    ↓
                       │ RE-EVALUATE
                       │
                       └── YES
                              ↓
                         MARK NODE COMPLETE
                              ↓
                         FIRE NEXT LEGAL EDGE
```

---

# 40. PARALLEL / CONVERGENCE LOOP

```text
MAIN SEQUENCE
    │
    ├── RIDER A ───────────────┐
    ├── RIDER B ───────────────┤
    ├── ATTACHED C ────────────┤
    └── COUNTER D ─────────────┤
                               ↓
                       CONVERGENCE WINDOW
                               ↓
                     SYNCHRONIZATION GATE
                               ↓
              REQUIRED STATES / RETURNS READY?
                    ├── NO → block joint edge
                    └── YES
                           ↓
                       JOINT EVENT
                           ↓
                        RESULT
```

---

# 41. REPAIR / RETEST LOOP

```text
PARENT S0
↓
TEST ATTEMPT S1
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
S0 CONTINUES
```

No Sequence is rewritten.

---

# 42. MEMORY VALIDATION LOOP

```text
MEMORY M
↓
TRUST SUFFICIENT?
├── YES → USE UNDER DECLARED SCOPE
└── NO
      ↓
   VALIDATION SEQUENCE
      ↓
   second source / evidence /
   reconstruction / comparison
      ↓
   CLOSE
      ↓
   RETURN
      ↓
   UPDATE TRUST STATE
```

If sources disagree:

```text
HALT AUTOMATIC MERGE
↓
CONTRADICTION REGISTER
```

---

# 43. HUMAN LEARNING LOOP

```text
HUMAN H_t
↓
PERCEIVE / DECIDE / ACT
↓
RESULT
↓
ERROR / REWARD / CONSEQUENCE
↓
MEMORY ENCODING
↓
CONSOLIDATION
↓
MODEL / VALUE / SKILL UPDATE
↓
SEQUENCE CLOSES
↓
NEW HUMAN BASELINE H_t+1
↓
NEW SEQUENCE
```

---

# 44. AI LEARNING / MEMORY LOOP

```text
AI RUNTIME STATE A_t
↓
OBSERVE / REASON / ACT
↓
RESULT
↓
VERIFY
↓
WRITE-BACK POLICY?
├── TRACE_ONLY
│     ↓
│  no durable change
└── ALLOWED
      ↓
   memory / rule / artifact /
   evaluation set / training candidate
      ↓
   CLOSE
      ↓
NEW RUNTIME PRIOR REALITY A_t+1
```

Training model weights is a separate Sequence.

---

# 45. PHASE-2 SOURCE ADOPTION WORKFLOW

Every new Phase-2 file is adopted through this pipeline.

```text
NEW FILE / CORPUS
      ↓
P2-00 RAW SOURCE LOCK
      │
      ├── preserve original
      ├── file identity
      ├── version
      └── no rewriting
      ↓
P2-01 SOURCE CLASSIFICATION
      │
      ├── HUMAN RUBRIC
      ├── AI RUBRIC
      ├── HOLY BOOK / NARRATIVE
      ├── ASI SPEC
      ├── SCIENCE / FACT
      ├── RULE / LAW
      ├── EXAMPLE / TEST
      └── OTHER
      ↓
P2-02 NATIVE HIERARCHY EXTRACTION
      │
      ├── levels
      ├── IDs
      ├── names
      ├── definitions
      └── relations
      ↓
P2-03 SOURCE INTEGRITY CHECK
      │
      ├── duplicates
      ├── missing IDs
      ├── contradictions
      ├── undefined words
      └── source gaps
      ↓
P2-04 REGISTRY CREATION
      │
      ├── native registry unchanged
      └── versioned
      ↓
P2-05 UNIVERSAL SEQUENCE BINDING
      │
      ├── primary roles
      ├── secondary roles
      ├── order types
      ├── drivers
      ├── controllers
      ├── performers
      ├── carriers
      └── memory/write-back
      ↓
P2-06 ASI-NODE BINDING
      │
      ├── which Node Brains can activate it
      ├── allowed reads
      ├── allowed writes
      └── contracts
      ↓
P2-07 GAP / CONTRADICTION REGISTER
      ↓
P2-08 SAMPLE SEQUENCE TESTS
      │
      ├── reverse
      ├── forward
      ├── reverse
      ├── node truth
      └── path truth
      ↓
P2-09 ORPHAN TEST
      │
      ├── unmapped registry IDs?
