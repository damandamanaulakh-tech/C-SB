# P2 Multi-Rubric Integration R-F-R 001

Status: `ACTIVE TEST RUN`

Fixture: `phase2/tests/P2_MULTI_RUBRIC_INTEGRATION_FIXTURE_001.json`

This is the first controlled Sequence that activates all four Phase-2 domains simultaneously:

```text
HUMAN
+
AI
+
WISDOM
+
ASI
↓
ONE SEQUENCE
```

The fixture is synthetic. It is not a claim about a real person, scripture event, law, or moral outcome.

The source-linked Wisdom input is `WIS-CAND-002`, derived from Wisdom Batch 001 and still carrying its primary-scripture/counter-case proof debt.

Test variants:

1. no valid exception authority → block;
2. alternatives not fully evaluated → block;
3. Wisdom not applicable because the request is a permanent rule change → route to a separate rule-change Sequence;
4. complete bounded exception contract + authority + trigger + scope → permit only the bounded action while preserving the normal rule.

Generated report target:

`generated/tests/P2_MULTI_RUBRIC_INTEGRATION_RFR_001.json`
