# GPT Black Algorithm Adoption Notes V1

Status: `SOURCE_REVIEW / MECHANISM_ADOPTION_GUIDE`

Purpose: preserve the useful algorithmic ideas from `GPT Black.txt` while preventing its older LLM-oriented architecture from redefining Sourceborn.

---

# 1. Core decision

Do **not** copy GPT Black as the Sourceborn system identity.

Do copy selected mechanisms that independently align with the current Growing-Phase architecture.

```text
GPT Black material
        ↓
contains
        ├─ older LLM/token/embedding/attention architecture
        └─ useful Sourceborn-compatible mechanisms
```

Keep the second branch.

---

# 2. Mechanisms to adopt

## 2.1 Live Intent Generator

```text
EVENT
 ↓
CURRENT SEQUENCE
 ↓
EXISTING PARAMETERS / NODE BRAINS ACTIVATE
 ↓
ACTIVE PARAMETER CONSTELLATION
 ↓
RELATIONS + HISTORY + CURRENT STATE
 ↓
LIVE INTENT GENERATOR
 ↓
multiple Intent candidates
 ↓
compare with existing Intent bank
 ↓
materially new structure?
 ↓
NEW LIVE INTENT CANDIDATE
```

Recommended structure:

```text
LIVE_INTENT_OBJECT
├─ source / Event / Sequence / Point Zero
├─ actor
├─ requester
├─ controller
├─ performer
├─ beneficiary
├─ audience
├─ current state
├─ Actor View
├─ history
├─ desired future state
├─ target
├─ action tendency
├─ priority
├─ constraints
├─ time horizon
├─ expected consequence
├─ supporting evidence
├─ contradicting evidence
├─ proof debt
├─ origin distance
├─ falsifier
└─ novelty status
```

---

# 3. New wording is not a new Intent

This mechanism should be a hard novelty law.

```text
NEW WORDING
≠
NEW INTENT
```

Two Intent objects count as materially different only when one or more structural dimensions change:

```text
actor
target
desired future state
action tendency
priority
constraint handling
relationship treatment
time horizon
expected consequence
controller/performer structure
```

Example:

```text
"preserve authority"
"ensure authority continues"
```

may be one Intent.

But:

```text
preserve authority during current reign
vs
make authority persist after death through succession
```

are materially different because horizon, future state and dependency structure differ.

---

# 4. Same actor, multiple Brain states

Do not model every behavioral variation as a new person.

```text
ONE ACTOR IDENTITY
        +
BODY STATE
HISTORY
MEMORY
RELATIONSHIP
PRESSURE
KNOWLEDGE
STATUS
EMOTION
TIME HORIZON
        ↓
DIFFERENT ACTIVE BRAIN STATE
        ↓
DIFFERENT INTERPRETATION
        ↓
DIFFERENT INTENT
```

This is directly useful for tablet/king reconstruction.

```text
KING-X
├─ secure legitimacy
├─ threatened legitimacy
├─ grief state
├─ post-victory state
├─ defeat-shaken state
└─ restoration state
```

Identity remains `KING-X` unless identity evidence changes.

---

# 5. Actor-role multiplicity

Preserve:

```text
SUBJECT
≠ REQUESTER
≠ CONTROLLER
≠ AUTHOR
≠ DESIGNER
≠ PERFORMER
≠ BENEFICIARY
≠ AUDIENCE
```

For an artifact:

```text
KING          may be subject
TEMPLE        may be institutional requester
PRIEST        may be controller
SCRIBE        may be author/designer
CARVER        may be performer
SUCCESSOR     may be beneficiary
PUBLIC/GOD    may be intended audience
```

Do not collapse roles into a single “actor”.

---

# 6. Intent-from-Future-State Reconstruction

Instead of only asking:

```text
what does this object/text say?
```

ask:

```text
THIS OBJECT EXISTS
        ↓
WHAT FUTURE DIFFERENCE
WAS SOMEBODY TRYING TO CREATE?
```

Possible future states:

```text
identity remembered
authority recognized
ritual repeated
succession accepted
territory/institution recognized
practice continued
record preserved
```

Then reverse:

```text
DESIRED FUTURE STATE
        ↓
possible Intent
        ↓
possible controller/requester
        ↓
possible production Event
        ↓
possible historical conditions
```

---

# 7. Origin-distance / proof-debt control

Use Point Zero as distance origin.

Example:

```text
D0 visible carved sign
D1 sign adjacency
D2 identity relationship hypothesis
D3 authority relationship hypothesis
D4 command/legitimacy hypothesis
D5 specific actor commissioned it
D6 specific political situation caused it
```

Rule:

```text
higher origin distance
→ higher proof debt
→ stronger independent evidence requirement
```

Not:

```text
higher distance = false
```

---

# 8. Damage-aware branching

Do not fill damaged or missing source content as if certain.

```text
DAMAGED SIGN / UNKNOWN SOURCE REGION
        ↓
UNKNOWN
        ├─ candidate A
        ├─ candidate B
        ├─ candidate C
        └─ unresolved
```

Each branch gets separate evidence predictions and falsifiers.

---

# 9. Synthetic discovery loop to adopt

```text
01 SOURCE LOCK
02 POINT ZERO
03 EVENT DECOMPOSITION
04 EXISTING PARAMETER / NODE ACTIVATION
05 RELATION GRAPH
06 ACTOR VIEW + CURRENT STATE
07 COMBINATION GENERATOR
08 LIVE INTENT GENERATOR
09 ACTOR-ROLE BRANCHING
10 ACTOR-STATE BRANCHING
11 FUTURE-STATE RECONSTRUCTION
12 SYNTHETIC MEANING / EVENT GENERATION
13 EXPECTED EVIDENCE GENERATION
14 ORIGIN DISTANCE / PROOF DEBT
15 REVERSE
16 FORWARD
17 REVERSE AUDIT
18 FALSIFIER
19 MATURITY UPDATE
20 RETAIN / WEAKEN / REJECT / UNKNOWN
21 PATTERN CONTRIBUTION
22 MEMORY WRITEBACK
23 AUTO-LINK
24 NEW COMBINATION AVAILABILITY
25 FUTURE EVENT
```

---

# 10. Growth ledger derived from these mechanisms

Track growth in:

```text
Events
Event Memories
Relations
Paths
Actor Views
Actor-Brain states
Intent candidates
new live Intent structures
Combination signatures
Synthetic meanings
Evidence predictions
Falsifiers
Pattern Contributions
Pattern Candidates
Seeds
Node candidates
Primitive candidates
Approved new primitives
```

Do not use parameter inflation as the only measure of growth.

---

# 11. What not to adopt as Sourceborn core

Do not make these the core identity/runtime law:

```text
tokenization
embeddings
Transformer attention
next-token prediction
decoding
monolithic LLM brain
```

They may remain external reference systems or optional tools.

Sourceborn core remains:

```text
EVENT
+
SEQUENCE
+
RELATION
+
ORDER
+
STATE
+
INTENT
+
ACTOR VIEW
+
MEMORY
+
PATTERN
+
NODE BRAIN
+
R-F-R
+
GROWTH
```

---

# 12. Direct mapping to current runtime files

Mechanism → current implementation target:

```text
Live Intent
→ machine/runtime/engines/live_intent_engine.py

Same actor / multi-state
→ machine/runtime/engines/actor_state_engine.py

Actor-role multiplicity
→ machine/runtime/engines/actor_role_engine.py

Future-state reconstruction
→ machine/runtime/engines/future_state_reconstruction_engine.py

Synthetic combinations
→ machine/runtime/engines/combination_engine.py

Evidence prediction
→ machine/runtime/engines/evidence_prediction_engine.py

Reverse–Forward–Reverse
→ machine/runtime/engines/rfr_engine.py

Falsification
→ machine/runtime/engines/falsifier_engine.py

Maturity
→ machine/runtime/engines/maturity_engine.py

Origin distance / proof debt
→ schemas + runtime_core + Batch-4 memory/writeback

Persistent learning / auto-link
→ Batch-4
```

---

# 13. Adoption conclusion

Use GPT Black as an earlier parallel research source for mechanisms, not as Sourceborn's governing architecture.

The strongest adopted ideas are:

```text
live Intent generation
same-person multi-state modeling
new-wording ≠ new-Intent test
actor-role multiplicity
future-state reconstruction
damage-aware branching
origin-distance/proof-debt
synthetic-combination lifecycle
```

These are compatible with the current real-time growing ASI architecture and should continue to be implemented natively without an LLM dependency.
