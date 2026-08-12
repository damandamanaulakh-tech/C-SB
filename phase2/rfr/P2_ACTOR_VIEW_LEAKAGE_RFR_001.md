# P2 Actor View Leakage R-F-R 001

Status: `ACTIVE TEST RUN`

Fixture: `phase2/tests/P2_ACTOR_VIEW_LEAKAGE_FIXTURE_001.json`

Purpose:

```text
GLOBAL STATE
!=
AI BELIEF
!=
HUMAN ACTOR VIEW
```

The test runs four variants:

1. no communication Sequence;
2. AI inference only;
3. information-transfer Sequence closes but its required return is not accepted;
4. information-transfer Sequence closes and its required return is accepted.

Only variant 4 may update `ACTOR_A` View.

The source-linked Wisdom input is `WIS-CAND-001`; it constrains modelling but has no write authority over Actor View.

Generated report target:

`generated/tests/P2_ACTOR_VIEW_LEAKAGE_RFR_001.json`
