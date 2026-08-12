# P2 Human + Wisdom, No-AI R-F-R 001

Status: `ACTIVE TEST RUN`

Fixture: `phase2/tests/P2_HUMAN_WISDOM_NO_AI_FIXTURE_001.json`

Purpose:

```text
HUMAN STATE / HISTORY
+
SOURCE-LINKED WISDOM
+
ASI PROVENANCE / APPLICABILITY AUDIT

AI = NOT REQUIRED
```

The test uses `WIS-CAND-004` and the same synthetic `INPUT_X` across different Human history/current-state variants.

It checks that:

- Human state/history owns the response;
- Wisdom is contextual and conditional, not the response producer;
- Wisdom applicability can be false;
- AI segments, AI-only records and Engines remain inactive;
- ASI audits provenance/applicability without becoming the Human decision-maker.

Generated report target:

`generated/tests/P2_HUMAN_WISDOM_NO_AI_RFR_001.json`
