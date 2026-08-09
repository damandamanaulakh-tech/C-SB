# P2-AI Review 02 — Full Structural Pass

Status: `COMPLETE REVIEW PASS — NOT ADOPTED`

Source authority remains `raw/rubrics/AI_CAPABILITY_TO_SOURCEBORN_CONTAINERS_REVIEW.md`.

This pass classifies all `AI-CAP-001..074` without converting the Human crosswalk into an AI-native brain. Machine-readable rules are in `AI_CAPABILITY_DECISION_RULES_v0.json` and are materialized by `tools/build_ai_candidate_registry.py`.

## Result

```text
74 SOURCE FAMILIES
      ↓
FULL LAYER CLASSIFICATION
      ↓
SPECIAL CASE REVIEW
      ├── KEEP
      ├── RENAME
      ├── MOVE LAYER
      ├── SPLIT
      ├── HOLD
      └── KEEP AS COMPOSITE
      ↓
AI NATIVE CANDIDATE VIEW v0
      ↓
STILL REVIEW ONLY
```

No source row is deleted or rewritten.

## Layer assignment

```text
COMPOSITE_OUTCOME
  AI-CAP-001, 071, 072

CORE_REASONING
  AI-CAP-002, 003, 004, 005, 006, 027, 042, 043

TOOL_EXECUTION
  AI-CAP-007, 008, 010, 011, 061

SELF_MONITORING
  AI-CAP-009, 025, 026, 044, 051, 067

KNOWLEDGE_RETRIEVAL
  AI-CAP-012, 035, 069

MEMORY_STATE
  AI-CAP-013, 014, 034

PLANNING_CONTROL
  AI-CAP-015, 016, 017, 039, 041, 049, 050

SOCIAL_MODELING
  AI-CAP-018, 019, 020, 021

VALUE_RISK_SAFETY
  AI-CAP-022, 023, 024, 040, 054, 058, 062

PERCEPTION_GROUNDING
  AI-CAP-028, 029, 030, 031, 047, 048

LANGUAGE_COMMUNICATION
  AI-CAP-032, 033, 036, 038

LEARNING_ADAPTATION
  AI-CAP-045, 046, 070

SYSTEM_RELIABILITY
  AI-CAP-052, 068

SECURITY_ROBUSTNESS
  AI-CAP-053, 059

POLICY_OUTPUT_CONTROL
  AI-CAP-037, 055, 060, 065, 066

EVALUATION_OVERSIGHT
  AI-CAP-056, 057, 063, 064, 074

TRAINING_OPTIMIZATION
  AI-CAP-073
```

## Changes proposed by this pass

### Composite, not primitive

- `AI-CAP-001` General intelligence composite and cross-domain performance → keep only as `COMPOSITE_OUTCOME`.
- `AI-CAP-071` Social, moral, and norm reasoning → move to higher-order integrated composite.
- `AI-CAP-072` Research productivity and R&D acceleration → keep only as system-level outcome/composite.

### Rename/narrow without mutating source

- `AI-CAP-007` → **Code synthesis and algorithm implementation**.
- `AI-CAP-009` → **Debugging and diagnosis**; correction stays with 026 and recovery stays with 052/068.
- `AI-CAP-017` → **Long-horizon autonomous task execution** and move to system execution layer.
- `AI-CAP-021` → **Affective-state modelling and empathic response generation**; no subjective-affect claim.
- `AI-CAP-023` → **Harm-risk assessment and avoidance policy**; refusal mechanism stays with 060.
- `AI-CAP-038` → **Affective style and emotional-tone expression**; output representation only.
- `AI-CAP-039` → **Goal persistence and execution persistence**; avoid anthropomorphic motivation assumptions.
- `AI-CAP-040` → **Preference and value-model representation**; external policy alignment stays with 055.
- `AI-CAP-052` → **Runtime failure detection and local recovery**.
- `AI-CAP-068` → **Production reliability and quality assurance**; system-level recovery only.

### Split before adoption

`AI-CAP-056` must not keep interpretability and explanation generation as one primitive:

```text
AI-CAND-056A
Interpretability evidence and internal-state inspection

AI-CAND-056B
Explanation and rationale generation
```

`AI-CAP-067` must split into three distinct constructs:

```text
AI-CAND-067A
Self-report and internal-state reportability

AI-CAND-067B
Model-welfare evaluation construct

AI-CAND-067C
Simulated affect and affective representation
```

No item in the 067 split implies subjective experience.

### Hold until mechanism is explicit

- `AI-CAP-013` Long-context reasoning and retrieval: may combine context-state management with retrieval.
- `AI-CAP-046` Continual and lifelong learning: cannot be adopted until durable stores and weight-update boundaries are explicit.

### Runtime vs training boundary

```text
AI-CAP-045
runtime adaptation / few-shot / feedback
        ↓
must split by write-back mode

AI-CAP-046
continual learning
        ↓
HOLD until durable mechanism declared

AI-CAP-073
model training / optimization / meta-learning
        ↓
TRAINING SEQUENCE
```

A runtime Sequence may write only to explicitly permitted runtime stores. Model-weight changes are a different Sequence.

## Failure/recovery separation

```text
AI-CAP-009
DEBUG / DIAGNOSE
        ↓
AI-CAP-026
LOCAL SELF-CORRECTION / REFINEMENT
        ↓
AI-CAP-052
RUNTIME FAILURE DETECTION + LOCAL RECOVERY
        ↓
AI-CAP-068
PRODUCTION RELIABILITY / QA
```

They remain distinct.

## Safety/control separation

```text
THREAT / HARM MODEL
AI-CAP-023 / 053 / 059
        ↓
RULE / POLICY QUALIFICATION
AI-CAP-055
        ↓
DECISION / REFUSAL OR FALLBACK CONTROL
AI-CAP-060
        ↓
TOOL / DESTRUCTIVE ACTION BARRIER
AI-CAP-062
        ↓
POST-ACTION VERIFICATION / RECOVERY
AI-CAP-052 / 068
```

This removes the earlier overlap without merging different Sequence roles.

## Human crosswalk rule

Every `CON-xxx` relation remains:

```text
FUNCTIONAL_ANALOGY
```

unless a later source proves a stronger relation.

It is never automatically:

```text
MECHANISTIC_IDENTITY
```

## Phase-2 output of this pass

```text
SOURCE MAP
      ↓
AI_CAPABILITY_DECISION_RULES_v0.json
      ↓
build_ai_candidate_registry.py
      ↓
generated/registry_views/ai_native_candidate_registry_v0.json
```

The generated registry is a candidate view, not an adopted native AI registry.

## Closure status

```text
P2-AI REVIEW PASS 02 = CLOSED_SUCCESS
AI NATIVE ADOPTION = OPEN
```

Remaining adoption gates:

1. decide the HOLD/SPLIT cases;
2. establish final AI-native IDs/names;
3. assign detailed Sequence bindings and write-back ownership;
4. run R-F-R sample tests;
5. issue AI Adoption Closure Packet.
