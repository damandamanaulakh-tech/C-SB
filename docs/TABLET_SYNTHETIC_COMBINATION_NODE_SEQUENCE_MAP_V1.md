# Tablet Synthetic Combination → Node / Format / Pattern / Sequence Map V1

Status: `GROWING_PHASE_TEST_ARCHITECTURE`

Epistemic boundary:

> The visible tablet image is a source artifact for structural observation. The synthetic combinations below are **not verified hieroglyph translations**. They are Sourceborn hypothesis objects used to test Event/Intent reconstruction, Node-Brain routing, evidence prediction, falsification and memory growth.

---

# 1. Purpose

The tablet test exists to answer a deeper question than “what does this inscription say?”

```text
SURVIVING ARTIFACT
        ↓
WHAT EVENT CAUSED THIS OBJECT TO EXIST?
        ↓
WHO?
WHEN?
WHY?
HOW?
WHO REQUESTED IT?
WHO CONTROLLED IT?
WHO DESIGNED/AUTHORED IT?
WHO PERFORMED THE PHYSICAL WORK?
WHO BENEFITED?
WHO WAS THE INTENDED AUDIENCE?
WHAT FUTURE DIFFERENCE WAS EXPECTED AFTER THE OBJECT EXISTED?
```

The tablet is therefore an Event-reconstruction and Intent-discovery fixture.

---

# 2. Point Zero

Point Zero must contain only source-grounded observation.

```text
POINT ZERO
├─ source image / artifact reference
├─ visible sign positions
├─ visible enclosures / cartouche-like forms
├─ visible repetitions
├─ visible columns/rows
├─ visible orientation
├─ visible damage / uncertainty
└─ no assumed translation
```

Do not insert the following at Point Zero unless independently verified:

```text
specific king name
specific reign
specific date
specific translation
specific ritual meaning
specific political purpose
```

---

# 3. Visual sign-group abstraction

Until exact Egyptological sign identification is locked, Sourceborn may use visual observation groups.

```text
SG-A = enclosed identity/name-like group
SG-B = bird-like sign cluster
SG-C = water/wave-like sign cluster
SG-D = standing/seated figure-like sign cluster
SG-E = vertical/architectural sign cluster
SG-F = offering/object-like cluster
SG-G = repeated short cluster
SG-H = boundary/enclosure-like form
SG-I = damaged/uncertain sign region
SG-J = terminal/result-like cluster
```

These codes are visual grouping aids, not translations.

---

# 4. Base transformation pipeline

```text
VISIBLE GROUP
    ↓
POSITION / ORIENTATION / NEIGHBOR / REPETITION / ENCLOSURE
    ↓
SIGN-RELATION CANDIDATE
    ↓
SYNTHETIC COMBINATION
    ↓
SYNTHETIC MEANING
    ↓
EVENT HYPOTHESIS
    ↓
INTENT HYPOTHESIS
    ↓
ACTOR-ROLE BRANCHES
    ↓
ACTOR-STATE BRANCHES
    ↓
EXPECTED FUTURE STATE
    ↓
PREDICTED EVIDENCE
    ↓
R-F-R
    ↓
FALSIFIER / CONTRADICTION
    ↓
MATURITY
    ↓
RETAIN / WEAKEN / REJECT / UNKNOWN
```

---

# 5. Sourceborn record formats used

## 5.1 ArtifactObservationRecord

```text
artifact_id
source_ref
point_zero_ref
visual_group_id
location
orientation
neighbors
repetition_count
damage_state
epistemic_status
origin_distance
```

## 5.2 SyntheticCombinationRecord

```text
combination_id
component_group_ids
relation_ids
order_type
combination_mode
synthetic_meaning
source_refs
origin_distance
proof_debt
maturity
status
```

## 5.3 EventHypothesisRecord

```text
event_hypothesis_id
artifact_ref
combination_ref
possible_event_type
actor_role_refs
state_refs
sequence_ref
predicted_result
source_distance
status
```

## 5.4 EventIntent

```text
intent_id
event_ref
intent_type
actor
requester
controller
performer
beneficiary
audience
target
desired_future_state
motive_hypothesis
constraints
time_horizon
expected_consequence
proof_debt
maturity
falsifier_refs
```

## 5.5 ActorBrainHypothesis

```text
actor_brain_id
actor_identity_ref
actor_role
actor_view
actor_state
history_refs
active_human_parameters
active_ai_functions
active_wisdom_context
intent_ref
future_state_ref
status
```

## 5.6 EvidencePredictionRecord

```text
prediction_id
hypothesis_ref
expected_observation
expected_absence
source_independence_required
priority
failure_implication
```

## 5.7 FalsifierRecord

```text
falsifier_id
hypothesis_ref
condition
test_source_ref
result
status
```

---

# 6. Reusable Sequence formats

## SEQ-FMT-TAB-01 — Sign Group → Synthetic Meaning

```text
Point Zero
→ visual groups
→ typed relations
→ bounded combination
→ synthetic meaning
→ evidence debt
```

Primary Nodes:

```text
ASI-NODE-01  Reverse / Provenance
ASI-NODE-02  State / Identity / Relation
ASI-NODE-06  Multi-rubric Combination
ASI-NODE-07  Evidence / Qualification
ASI-NODE-16  R-F-R Falsifier
```

## SEQ-FMT-TAB-02 — Synthetic Meaning → Event + Intent

```text
synthetic meaning
→ possible Event type
→ actor-role separation
→ actor-state branches
→ desired future state
→ Intent hypotheses
```

Primary Nodes:

```text
ASI-NODE-02
ASI-NODE-03
ASI-NODE-06
ASI-NODE-08
ASI-NODE-10
ASI-NODE-20
ASI-NODE-21
```

## SEQ-FMT-TAB-03 — Actor-Brain Branching

```text
same candidate actor identity
        ↓
state A
state B
state C
...
        ↓
different active Human parameter constellations
        ↓
different Intent candidates
```

Primary Nodes:

```text
ASI-NODE-02
ASI-NODE-06
ASI-NODE-08
ASI-NODE-20
```

## SEQ-FMT-TAB-04 — Reverse → Forward → Reverse

```text
hypothesis
→ reverse to Point Zero / source
→ forward-predict evidence
→ compare actual evidence
→ reverse-audit assumptions
→ falsifier
→ maturity update
```

Primary Nodes:

```text
ASI-NODE-01
ASI-NODE-07
ASI-NODE-10
ASI-NODE-11
ASI-NODE-16
ASI-NODE-21
```

## SEQ-FMT-TAB-05 — Growth Writeback

```text
retained hypothesis / rejection / contradiction
→ Pattern Contribution
→ memory write
→ auto-link
→ Pattern Candidate / Node Candidate if reusable
→ future Seed
```

Primary Nodes:

```text
ASI-NODE-12
ASI-NODE-13
ASI-NODE-14
ASI-NODE-15
ASI-NODE-17
ASI-NODE-21
```

---

# 7. Synthetic meaning bank

All items below are `NEW_SYNTHETIC` until external/source evidence increases maturity.

## Family A — Identity / Title / Entity

### SYNTH-001 — Protected identity formula

Combination:

```text
SG-A + SG-H + adjacent title-like groups
```

Possible meaning:

```text
an enclosed identity/name presented under a protective or privileged formal structure
```

Possible Event:

```text
formal inscription of a protected identity
```

Possible Intents:

```text
identity preservation
royal/elite recognition
continuity
ritual protection
status display
```

Nodes:

```text
01 → 02 → 06 → 07 → 16 → 11 → 12
```

Falsifier examples:

```text
verified enclosure is not a name/title structure
verified signs form a different grammatical function
```

### SYNTH-002 — Office / role title

Combination:

```text
SG-A + recurring adjacent title-like cluster
```

Possible Intent:

```text
make an office/role recognizable independently of the individual
```

### SYNTH-003 — Lineage / succession marker

Combination:

```text
SG-A1 + SG-A2 + ordered relationship
```

Possible Event:

```text
association of one identity with another across succession/family/order
```

Guard:

```text
two enclosed names ≠ lineage automatically
```

### SYNTH-004 — Institutional identity

Combination:

```text
SG-A + SG-E + repeated institutional context
```

Possible Intent:

```text
identify office/temple/estate/institution rather than only a person
```

### SYNTH-005 — Protected title sequence

Combination:

```text
SG-A + SG-H + multiple title components
```

### SYNTH-006 — Dual-identity association

Combination:

```text
SG-A1 ↔ SG-A2
```

Possible relations:

```text
succession
co-rule
lineage
patron/deity relation
copy/restoration relation
```

---

## Family B — Authority / Command / Permission

### SYNTH-007 — Royal / central order

```text
identity/title group
+ action cluster
+ performer/reference cluster
```

Possible Event:

```text
an authority requests or commands production/action
```

Actor split:

```text
SUBJECT      may be king
REQUESTER    may be king/queen/institution
CONTROLLER   may be priest/administrator
AUTHOR       may be scribe
PERFORMER    may be carver/workshop
```

### SYNTH-008 — Priestly authorization

Possible Intent:

```text
ritual/institutional permission for an action or inscription
```

### SYNTH-009 — Delegated authority

```text
central identity
→ delegate/controller
→ performer
```

Important Sourceborn pattern:

```text
CONTROLLER ≠ PERFORMER
```

### SYNTH-010 — Administrative command

Possible Event:

```text
record/production/service initiated through an administrative chain
```

### SYNTH-011 — Ritual permission

Possible Event:

```text
formal action allowed under religious/institutional rule
```

### SYNTH-012 — Public authority display

Possible future state:

```text
audience recognizes authority/status after viewing the artifact
```

Guard:

```text
surviving object today ≠ proof of public original display
```

---

## Family C — Action / Work / Execution

### SYNTH-013 — Construction / workshop order

Possible actor chain:

```text
requester
→ designer/scribe
→ workshop controller
→ carver/performer
```

### SYNTH-014 — Offering preparation

Possible Event:

```text
ritual preparation directed toward a deity/temple/royal context
```

### SYNTH-015 — Ritual performance

Possible future state:

```text
ritual obligation considered performed / renewed / made visible
```

### SYNTH-016 — Record-making instruction

Possible Event:

```text
someone causes a statement/identity/event to be permanently recorded
```

### SYNTH-017 — Service / duty statement

Possible Intent:

```text
assign, acknowledge or preserve role/duty
```

### SYNTH-018 — Completion claim

Possible result:

```text
work/action reaches local closure
```

Guard:

```text
local completion claim ≠ global purpose fulfilled
```

---

## Family D — Place / Territory / Institution

### SYNTH-019 — Temple / estate marker

Possible Event:

```text
artifact associated with a named institution/location
```

### SYNTH-020 — Territorial designation

Guard:

```text
enclosure boundary ≠ territorial boundary automatically
```

### SYNTH-021 — Sacred-location marker

Possible Intent:

```text
bind identity/action to a sacred place
```

### SYNTH-022 — Workshop / production location

Possible evidence:

```text
material source
carving style
workshop parallels
known production debris
same hand/tool traces
```

### SYNTH-023 — Administrative district

High proof debt. Remains weak until geographic/administrative sign evidence exists.

### SYNTH-024 — Protected domain / bounded place

Possible relation:

```text
identity ↔ protected location / estate / institutional domain
```

---

## Family E — Purpose / Intent

### SYNTH-025 — Memorial intent

Future-state reconstruction:

```text
present Event
→ artifact created
→ identity/action remains remembered after participants are gone
```

Possible actors:

```text
king
queen
family
priesthood
institution
successor
```

### SYNTH-026 — Protection intent

Possible future state:

```text
identity/object/institution remains protected or ritually secured
```

### SYNTH-027 — Legitimacy / status intent

Actor-state branches:

```text
same ruler
├─ secure legitimacy
├─ threatened legitimacy
├─ newly succeeded
├─ post-conflict
└─ restoration context
```

Different states may produce different commissioning Intents.

### SYNTH-028 — Continuity / succession intent

Possible future state:

```text
authority / identity / ritual / institution persists beyond current actor
```

### SYNTH-029 — Public-display intent

Possible future state:

```text
audience changes belief/recognition after encountering artifact
```

### SYNTH-030 — Instruction / transmission intent

Possible Event:

```text
artifact exists so information/action/ritual can be transmitted or repeated
```

---

## Family F — Record / Time / Result / Future State

### SYNTH-031 — Record of action

Possible Event:

```text
an action is converted into durable recorded representation
```

### SYNTH-032 — Dedication record

Possible role chain:

```text
requester
→ dedicatee/beneficiary
→ scribe/designer
→ carver
→ future audience
```

### SYNTH-033 — Ownership / possession statement

Requires actual linguistic/relational support before maturity upgrade.

### SYNTH-034 — Temporal / reign-phase marker

High-risk synthetic. Repetition/order alone cannot establish chronology.

### SYNTH-035 — Future-preservation formula

Future-state reconstruction:

```text
current actor acts
→ inscription survives
→ identity/action remains available to future observers
```

### SYNTH-036 — Renewal / restoration record

Alternative Event branches:

```text
ORIGINAL PRODUCTION EVENT
LATER RESTORATION EVENT
REUSE / COPYING EVENT
```

This is a major Sourceborn guard:

```text
surviving inscription today
≠
original production Event automatically
```

---

# 8. Pattern Candidates generated by tablet work

## PC-TAB-SYN-001 — Repeated Enclosure Role Stability

Repeated enclosure structure may indicate stable function, but not automatically stable meaning.

## PC-TAB-SYN-002 — Position-Dependent Sign Function

Same visual sign may perform different roles depending on neighboring signs and position.

## PC-TAB-SYN-003 — Controller–Performer Separation

Artifact subject/controller/author/performer may be different actors.

## PC-TAB-SYN-004 — Intent-from-Future-State Reconstruction

Infer possible Intent by asking what future difference the artifact was meant to create.

## PC-TAB-SYN-005 — Same Actor / Different Brain State

One historical actor may produce different Intents under different internal/external states.

## PC-TAB-SYN-006 — Actor-Role Multiplicity

Subject, requester, controller, author, performer, beneficiary and audience are independent roles.

## PC-TAB-SYN-007 — Damage-Aware Meaning Branching

Damaged sign region produces bounded alternatives, not automatic completion.

## PC-TAB-SYN-008 — Actor-Role Multiplicity Under Institutional Production

Institutional artifacts may require multi-actor chains rather than a single author assumption.

## PC-TAB-SYN-009 — Origin-Distance Evidence Scaling

Each interpretive step away from Point Zero increases proof debt and evidence requirement.

## PC-TAB-SYN-010 — Restoration-vs-Original-Production Split

Surviving text may derive from restoration/copy/reuse rather than original creation.

## PC-TAB-SYN-011 — Synthetic Meaning Does Not Equal Translation

Sourceborn can preserve a useful synthetic Event hypothesis without treating it as philological fact.

## PC-TAB-SYN-012 — Synthetic-Meaning Evidence-Debt Scaling

Greater semantic specificity requires stronger independent evidence.

---

# 9. Actor-Brain search space

Do not create 100 historical kings as facts. Create candidate actor-Brain states.

```text
UNKNOWN ARTIFACT-PRODUCING EVENT
        ↓
ACTOR CANDIDATE A
  ├─ state 1
  ├─ state 2
  └─ state 3

ACTOR CANDIDATE B
  ├─ state 1
  └─ state 2

ACTOR CANDIDATE C
  └─ state 1
```

A candidate may represent:

```text
king
queen
priest
scribe
administrator
workshop controller
carver
family member
temple institution
later restorer
copyist
successor
unknown
```

For each actor-state branch, generate:

```text
possible Intent
possible motive
possible constraints
possible time horizon
expected future state
predicted evidence
counter-evidence
falsifier
```

---

# 10. Example deep branch — legitimacy hypothesis

```text
SYNTH-027
LEGITIMACY / STATUS INTENT
        ↓
ACTOR CANDIDATE
        ↓
STATE A: SECURE
STATE B: THREATENED
STATE C: NEWLY SUCCESSFUL
STATE D: RESTORER
        ↓
LIVE INTENT GENERATOR
        ↓
INT-A preserve existing authority
INT-B repair disputed authority
INT-C connect present ruler to older legitimacy
INT-D establish continuity after disruption
        ↓
PREDICTED EVIDENCE
        ├─ titulary parallels
        ├─ restoration traces
        ├─ predecessor references
        ├─ temple context
        ├─ repeated formulae
        └─ chronology constraints
        ↓
R-F-R
        ↓
FALSIFIER
```

---

# 11. Memory writeback classes for tablet test

Even rejected hypotheses may create valuable memory.

Examples:

```text
REJECTED SYNTH-034
because repeated structure was grammatical, not chronological
        ↓
CONTRADICTION_MEMORY
PATTERN_MEMORY
RULE MEMORY:
"repetition/order does not automatically imply chronology"
```

Retained structures may write:

```text
EVENT_MEMORY
INTENT_MEMORY
RELATION_MEMORY
PATH_MEMORY
ACTOR_STATE_MEMORY
EVIDENCE_MEMORY
CONTRADICTION_MEMORY
PATTERN_MEMORY
NODE_LOCAL_MEMORY
```

But Source Text / artifact source remains immutable.

---

# 12. Auto-link targets

New tablet objects should automatically search for legal links through:

```text
same source
same Point Zero
same visual group
same sign relation
same actor role
same actor identity
same actor state
same Intent structure
same future-state structure
same evidence class
same contradiction
same Pattern Candidate
same Sequence family
```

Never auto-merge:

```text
historical actor identity
king identity
source identity
Intent identity
synthetic meaning identity
contradictory hypotheses
```

---

# 13. Growth counting

The tablet test should increase persistent Brain objects by classes, not fake parameter count.

Possible count ledger:

```text
Artifact Observation IDs          +N
Sign/visual group relations        +N
Synthetic Combination IDs         +36 or more
Synthetic Meaning IDs             +36 or more
Event Hypothesis IDs              +N
Intent Hypothesis IDs             +N
Actor-Brain Variant IDs           +N
Evidence Prediction IDs           +N
Falsifier IDs                     +N
Pattern Contribution IDs          +N
Pattern Candidate IDs             +12 or more
Memory IDs                        +N
Seed IDs                          +N
Node Candidate IDs                +N when reusable residual appears
Primitive Candidate IDs           +N only when irreducible
```

---

# 14. Final tablet execution flow

```text
TABLET IMAGE / ARTIFACT
        ↓
POINT ZERO
        ↓
VISUAL SIGN GROUPS
        ↓
RELATION / ORDER / DAMAGE / ORIENTATION
        ↓
BOUNDED COMBINATION ENGINE
        ↓
36+ NEW SYNTHETIC MEANINGS
        ↓
EVENT HYPOTHESES
        ↓
ACTOR ROLE SPLIT
        ↓
ACTOR STATE BRANCHING
        ↓
LIVE INTENT
        ↓
FUTURE STATE
        ↓
EVIDENCE PREDICTION
        ↓
R-F-R
        ↓
FALSIFIER / CONTRADICTION
        ↓
MATURITY
        ↓
RETAIN / WEAKEN / REJECT / UNKNOWN
        ↓
MEMORY WRITEBACK
        ↓
AUTO-LINK
        ↓
PATTERN / NODE / PRIMITIVE CANDIDATE GATES
        ↓
NEXT ARTIFACT EVENT STARTS FROM A STRONGER BRAIN
```

This document is a runtime/architecture specification. It is not a historical translation claim.
