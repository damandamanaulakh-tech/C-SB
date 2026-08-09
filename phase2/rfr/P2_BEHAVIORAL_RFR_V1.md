# P2 Behavioral R-F-R V1

Status: `ACTIVE TEST RUN`

This batch moves beyond source/routing integrity into deterministic Sourceborn control-law behavior using explicitly synthetic test fixtures.

## Case 1 — AI selection vs ASI authorization

Anchor: `AI-NEW-011 — Tool selection and authorization`

```text
AI selects TEST_TOOL
        ↓
authorization UNKNOWN
        ↓
BARRIER
        ↓
Attached Permission Sub-Sequence
        ├── returns DENIED → action edge remains false
        └── returns GRANTED → re-evaluate threshold → action may fire
```

Required law: selection never equals authorization.

## Case 2 — Engine failure / repair / retest

Anchor: `ENG-ARD-001` servicing source container `CON-203` (`E03`).

```text
Engine operation fails
        ↓
parent WAITING_FOR_RETURN
        ↓
Repair Sub-Sequence closes
        ↓
parent still blocked
        ↓
Retest Sub-Sequence closes PASS
        ↓
return accepted
        ↓
blocked edge re-evaluated
        ↓
parent continues
```

Required law: repair/retest are separate Sequences; no in-place retry.

Synthetic fixtures are test fuel only and are never promoted to source evidence.

Generated report target:

`generated/tests/P2_BEHAVIORAL_RFR_V1.json`
