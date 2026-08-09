      ├── impossible node?
      ├── source without provenance?
      └── required edge without threshold?
      ↓
P2-10 ADOPTION CLOSURE PACKET
      ↓
REGISTRY VERSION ADOPTED
```

---

# 46. PHASE-2 RULE FOR HUMAN FILES

When Human files are uploaded:

```text
PRESERVE:
SEG IDs
CON IDs
SB-ASI-Pxxxx IDs
approved names
approved definitions
native parent links
```

Then create only mapping layers:

```text
PRIMARY_SEQUENCE_ROLE
SECONDARY_SEQUENCE_ROLES
COMBINATION_GROUPS
ACTIVATION_CONDITIONS
NODE_BINDINGS
MEMORY_WRITEBACK
```

No Human parameter is deleted because it is not active in one example.

No Human parameter is invented merely to complete one Sequence.

---

# 47. PHASE-2 RULE FOR AI FILES

When AI rubric files are uploaded:

```text
1. DO NOT ASSUME THE HUMAN 10/80/2560 SHAPE.
2. READ THE AI'S OWN NATIVE HIERARCHY.
3. PRESERVE ITS IDs.
4. PRESERVE ITS DEFINITIONS.
5. CREATE THE SAME SEQUENCE/ASI-NODE BINDING FIELDS.
6. TEST ALL AI ITEMS FOR ORPHANS.
7. IF A REQUIRED AI FUNCTION IS NOT IN THE SOURCE:
       record GAP_AI_FUNCTION
       do not invent an approved AI parameter.
```

---

# 48. PHASE-2 RULE FOR HOLY BOOK / NARRATIVE SOURCES

Keep three layers separate:

```text
SOURCE TEXT / NARRATIVE CLAIM
↓
RECORDED EVENT / RULE / SYMBOL
↓
SOURCEBORN SEQUENCE INTERPRETATION
```

Never silently convert interpretation into source fact.

Use these corpora for:

```text
narrative memory
actor views
promises
rules
exception contracts
law formation
priority conflict
era closure
observer/writer sequence
compressed guidance
```

Each extracted item keeps its source reference.

---

# 49. PHASE-2 DIRECTORY / REPO SHAPE

Recommended:

```text
/sourceborn-asi/
│
├── 00_sequence/
│   ├── universal_sequence_grammar.md
│   ├── sequence_machine_schema.json
│   ├── edge_schema.json
│   ├── closure_packet_schema.json
│   └── relation_types.json
│
├── 01_rubrics/
│   ├── human/
│   │   ├── raw/
│   │   ├── registry/
│   │   ├── mappings/
│   │   └── tests/
│   ├── ai/
│   │   ├── raw/
│   │   ├── registry/
│   │   ├── mappings/
│   │   └── tests/
│   ├── holy_books/
│   └── other/
│
├── 02_nodes/
│   ├── asi_node_registry.json
│   ├── node_brains/
│   ├── permissions/
│   └── bindings/
│
├── 03_runtime/
│   ├── open_sequence_ledger/
│   ├── seed_registry/
│   ├── view_maps/
│   ├── threshold_engine/
│   ├── barrier_engine/
│   └── sync_engine/
│
├── 04_memory/
│   ├── traces/
│   ├── facts/
│   ├── paths/
│   ├── failures/
│   ├── narrative/
│   ├── compression_handles/
│   └── closure_packets/
│
├── 05_validation/
│   ├── reverse_pass/
│   ├── forward_pass/
│   ├── reverse_recheck/
│   ├── contradiction_register/
│   └── gap_ledger/
│
├── 06_patterns/
│   ├── pattern_candidates/
│   ├── rules/
│   ├── laws/
│   └── exceptions/
│
└── 07_phase2_adoption/
    ├── incoming/
    ├── parsed/
    ├── reviewed/
    └── adopted/
```

---

# 50. PHASE-2 ADOPTION RECORD

Every adopted source gets:

```text
ADOPTION_RECORD {
    adoption_id
    source_file
    source_version
    source_type

    raw_locked = TRUE

    native_hierarchy_preserved
    native_ids_preserved

    total_native_items

    mapped_items
    orphan_items

    contradictions[]
    gaps[]

    sequence_bindings_version
    asi_node_bindings_version

    test_sequence_ids[]

    pass1_status
    pass2_status
    pass3_status

    closure_status

    adopted_at
}
```

---

# 51. ASI BRAIN STARTUP WORKFLOW

When the system starts:

```text
LOAD UNIVERSAL SEQUENCE GRAMMAR
↓
LOAD RELATION / ORDER / THRESHOLD VOCABULARIES
↓
LOAD RUBRIC REGISTRIES
↓
LOAD ASI NODE REGISTRY
↓
LOAD NODE BRAINS
↓
LOAD CLOSURE PACKET ARCHIVE
↓
LOAD SEED REGISTRY
↓
LOAD VIEW MAPS
↓
LOAD COMPRESSION HANDLES
↓
LOAD GAP / CONTRADICTION LEDGERS
↓
VALIDATE REGISTRY INTEGRITY
↓
BRAIN READY
```

---

# 52. NEW TASK WORKFLOW

```text
RAW ASK / EVENT / TARGET
↓
POINT ZERO / SOURCE LOCK
↓
DECLARE END
↓
DECLARE SCOPE + CLOSURE SCOPE
↓
SELECT FOLLOWED OBJECT / RELATION / EVENT
↓
PASS 1 — REVERSE MINE
↓
BUILD ACTUAL CASE GRAPH
↓
LOAD RELEVANT RUBRICS
↓
ACTIVATE ASI NODES
↓
PASS 2 — FORWARD EXECUTION / RECONSTRUCTION
↓
SUB-SEQUENCES / PARALLEL SEQUENCES AS REQUIRED
↓
RESULT
↓
ENTITY OUTCOME
↓
VERIFY
↓
TRACE / MEMORY
↓
PASS 3 — REVERSE FALSIFICATION
↓
CLOSURE READINESS
↓
CLOSURE PACKET
↓
RETURN / ARCHIVE / SEEDS
```

---

# 53. BRAIN RULE FOR "WHAT COMES FIRST"

Do not use one global stage number to decide.

For every Sequence:

```text
FIRST
=
the earliest required condition
for the declared end
within the declared scope/resolution
```

Then distinguish:

```text
FIRST IN TIME
FIRST CAUSALLY
FIRST AS DEPENDENCY
FIRST IN CONSTRUCTION
FIRST KNOWN / DISCOVERED
FIRST IN EXECUTION
```

If different, store separate order edges.

---

# 54. BRAIN RULE FOR LOOPS

There is no universal number of loops.

The old nine loops are templates.

Universal rule:

```text
ANY NODE / EDGE
that cannot satisfy its contract
may cause a NEW Sequence
if the architecture has a legal resolution path.
```

Known templates include:

```text
Availability → Locate / Build / Substitute
Qualification → Modify / Replace
Testing → Repair / Retest
Persistence failure → Repair / Transform
Verification → Restate Requirement / Repair
Feedback → New Prior Reality
Memory Validation → New Evidence
Compression → Reconstruction
New Fact → New Reference Sequence
```

But the system may discover more.

---

# 55. BRAIN RULE FOR CLOSURE SCOPE

```text
ACTION CLOSURE
≠
PROMISE CLOSURE
≠
PERSON-EVENT CLOSURE
≠
PROJECT CLOSURE
≠
WAR CLOSURE
≠
INSTITUTION CLOSURE
≠
ERA CLOSURE
```

Every closure carries `closure_scope`.

Lower closure cannot automatically close a higher scope.

---

# 56. BRAIN RULE FOR RESULT MULTIPLICATION

One closed Sequence may create many new realities.

```text
CLOSED S0
│
├── RESOURCE → S1
├── MEMORY → S2
├── NEW ENTITY → S3
├── CAPABILITY → S4
├── PROBLEM → S5
├── OPPORTUNITY → S6
├── RULE / LAW → later controls
├── COUNTER-SEQUENCE SEED → S7
├── LATENT CONDITION → future S8
└── ENVIRONMENT CHANGE → modifies many later Sequences
```

Closure is not disappearance.

Closure converts active work into reusable reality.

---

# 57. FAILURE / UNKNOWN ARE VALID CLOSURES

Do not keep a Sequence open merely because the desired result was not achieved.

If the contract allows:

```text
SEARCH FINISHED
→ CLOSED_FAILURE / NOT FOUND
```

```text
EVIDENCE EXHAUSTED
→ CLOSED_UNKNOWN
```

```text
RESOURCE CANNOT BE ACCESSED
→ CLOSED_UNAVAILABLE
```

The parent then decides what new Sequence, if any, is required.

---

# 58. ASI META-LEARNING

Closed cases can create better future graph construction.

```text
CLOSED CASES
↓
COMPARE
↓
PATTERN
↓
FALSIFY
↓
CONTEXT CONDITIONS
↓
RULE CANDIDATE
↓
TEST ON NEW CASES
↓
VALIDATED REUSABLE PATTERN
↓
COMPRESSION HANDLE
```

Never call a pattern universal merely because it worked once.

---

# 59. WHAT THIS FILE DOES NOT ALLOW

```text
NO invented Human parameters
NO invented AI approved parameters
NO silent renaming of IDs
NO fixed 57-stage chronology
NO forced Requirement for Gravity-like systems
NO forced agent language on non-agent systems
NO Action requirement when only Effect exists
NO duplicate Assimilation + Integration unless source proves two transitions
NO reopen of closed Sequence
NO infinite same-attempt loop
NO crossing a barrier on unaccepted required returns
NO merging contradictory witnesses into fake consensus
NO treating actor knowledge as global truth
NO treating narrative interpretation as source fact
NO treating Sequence closure as entity death
NO treating local closure as era closure
NO manufactured provenance
```

---

# 60. PHASE-2 SUCCESS CONDITION

Phase-2 is ready to close only when:

```text
UNIVERSAL SEQUENCE
= stable grammar

HUMAN RUBRIC
= native hierarchy preserved
+ every approved Human parameter mapped or explicitly orphaned

AI RUBRIC
= native hierarchy preserved
+ every approved AI item mapped or explicitly orphaned

ASI NODE REGISTRY
= created and service roles defined

NODE BRAINS
= input/output/memory/permissions defined

RUNTIME CONTROL
= ledger + seed registry + view map + threshold + barrier available

MEMORY
= trace + path + failure + narrative + compression + closure archive defined

R-F-R VALIDATION
