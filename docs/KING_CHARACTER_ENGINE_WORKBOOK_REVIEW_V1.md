# King Character Engine Workbook Review V1

<!-- SOURCEBORN-REALTIME-ASI-V1:START -->

> **Tablet-event target:** King/queen/priest/workshop profiles are parallel, testable **candidate actor-Brain states** used to reconstruct the event that produced the surviving artifact. They are not the target answer and their count is not a count of historical kings. The target remains: who/when/why/how, who ordered, who performed, for whom, under what conditions, and what future state was intended. Evidence may retain, weaken, reject or leave each profile unknown. See `docs/SOURCEBORN_REALTIME_ASI_GROWING_PHASE_V1.md`.

<!-- SOURCEBORN-REALTIME-ASI-V1:END -->

## Source

Uploaded workbook fingerprint:

- SHA-256: `cb4f21211ec85762fe79e77f31637dbfaf27de3f178240a17b266f46d0ae43b5`
- Size: 329,383 bytes
- 16 sheets

This review does not overwrite the workbook and does not add its declared 2,000 rows to the active 3,204 Human-derived functional source count.

## What the workbook actually is

The workbook presents `10 segments × 8 containers × 25 parameters = 2,000`.

Inspection shows a more precise structure:

```text
10 DOMAIN SEGMENTS
    ↓
80 DOMAIN CONTAINERS
    ↓
same 25 interrogation dimensions reused once per container
    ↓
2,000 instantiated evaluation addresses
```

The 25 repeated dimensions are:

`Presence, Strength, Frequency, Trigger Situation, Primary Actor, Primary Target, Sequence Position, Duration, Repetition Pattern, Geographic Scope, Social Scope, Material Evidence, Textual Evidence, Iconographic Evidence, Comparative Parallel, Chronological Fit, Workshop Fit, Family Linkage, War Linkage, Ritual Linkage, Economic Linkage, Contradiction Risk, Alternative Explanation, Falsifier, Confidence`.

Many are Sourceborn-style rubrics/evidence/relations rather than independent domain primitives. Therefore the workbook is best classified as a **domain-rubric instantiation matrix**, not as a new native 2,000-parameter Human registry.

Candidate law:

```text
DOMAIN CONTAINER
×
REUSABLE EVALUATION DIMENSION
=
RUNTIME INTERROGATION ADDRESS

RUNTIME ADDRESS != NATIVE PARAMETER
```

## Strong architecture matches

```text
Observation Lock / Source Lock
→ Point Zero / source sovereignty

Reverse Chain
→ END→START dependency reconstruction

Forward Chain
→ START→END legal path

Contradiction Test / Falsifier Test
→ R-F-R

Memory Write
→ append-only/versioned memory

King Character
→ candidate weighted brain-state, not fixed person identity
```

The `SOURCEBORN_INIT` sheet explicitly describes a King-character as a generated, testable brain-state rather than a final identity.

## Structural counts verified

```text
Sheets                     16
Domain Segments            10
Containers                 80
Instantiated rows        2000
Unique interrogation dims  25

ARD loops                   5
Nodes per loop             12
ARD nodes total            60

Reverse/forward steps     100
Reverse                    50
Forward                    50
Steps per loop             20

Evidence capacity         500
Memory capacity           500

Character hypotheses      100
Character families         10
Characters per family      10
```

All 100 character weight vectors sum to approximately 1.0.

## R-F-R findings

### KC-RFR-001 — 2,000 rows are not 2,000 independent primitives

Every one of the 80 containers receives exactly the same 25 interrogation dimensions. The workbook's source count remains 2,000, but the machine meaning should be `2,000 instantiated evaluation addresses`.

### KC-RFR-002 — scoring range excludes P1999 and P2000

Actual parameter rows occupy Excel rows `4:2003`.

`PYRAMID_INDEX` formulas use:

```text
PARAMETER_BANK!$B$2:$B$2001
PARAMETER_BANK!$O$2:$O$2001
PARAMETER_BANK!$I$2:$I$2001
```

Therefore the final two rows are excluded from S10 scoring:

```text
P1999 = Completeness & Authenticity — Falsifier
P2000 = Completeness & Authenticity — Confidence
```

The source defect is preserved as a finding rather than silently repaired.

### KC-RFR-003 — no evidence still creates ranks

With no parameter evidence and no loop adjustments, every Final Score is `0`. The Rank formula still assigns ranks `1..100` using row-order tie breaking, and the Dashboard shows an ordered top-ten list.

```text
NO VALIDATED EVIDENCE
→ UNRANKED
→ NO LEADING HYPOTHESIS
```

### KC-RFR-004 — score magnitude is labelled as confidence

The workbook's Confidence Band uses `ABS(Final Score)`.

```text
MATCH DIRECTION / MAGNITUDE
!=
EPISTEMIC CONFIDENCE
```

A strong negative mismatch is not automatically high epistemic confidence.

### KC-RFR-005 — five loops share one route skeleton

The `REVERSE_FORWARD` sheet uses the exact same ten reverse edges and exact same ten forward edges for L1 through L5.

```text
LOOP COUNT != EVIDENTIAL INDEPENDENCE
DIFFERENT QUESTION != DIFFERENT PATH
REPEATED ROUTE != CORROBORATION
```

### KC-RFR-006 — loop completion does not automatically feed scoring

`MATCH_ENGINE` columns `L1 Adj.` through `L5 Adj.` are manual cells and are not formula-linked to `ARD_5_LOOPS`. Therefore the declared no-skip contract is not machine-enforced by the score engine.

```text
LOOP RESULT
→ verified completion
→ accepted return
→ only then score contribution
```

### KC-RFR-007 — character-weight provenance is open

The 100 candidate characters have normalized ten-segment weight vectors, but the workbook provides no provenance/evidence field for how those weights were derived. They should remain synthetic hypothesis priors/scaffolds rather than learned facts.

## New review-required candidates

1. `RC-DOMAIN-RUBRIC-INSTANTIATION-001` — Domain Container × Evaluation Dimension = Runtime Address.
2. `RC-NO-EVIDENCE-NO-RANK-001` — No validated evidence means no leading rank.
3. `RC-SCORE-CONFIDENCE-SEPARATION-001` — Match direction/magnitude is separate from epistemic confidence.
4. `RC-INDEPENDENT-LOOP-001` — Multiple loops are not independent merely because their prompts differ.

None is canonical from this workbook alone.

## Fit into C-SB

```text
SOURCEBORN UNIVERSAL RUBRICS
          │
          ├──────────────┐
          │              │
          ▼              ▼
DOMAIN PACK          CASE / SOURCE
(King / artifact)        │
          │              │
          └──────┬───────┘
                 ▼
        MEANINGFUL INSTANTIATION
                 │
                 ▼
      RUNTIME EVALUATION ADDRESSES
                 │
                 ▼
          SEQUENCE / R-F-R
                 │
                 ▼
       HYPOTHESIS STATE CANDIDATES
                 │
                 ▼
        EVIDENCE / CONTRADICTIONS
                 │
                 ▼
              REVIEW
```

The workbook contributes more value as a **domain-pack generator and falsification specimen** than as a new parameter-count source.
