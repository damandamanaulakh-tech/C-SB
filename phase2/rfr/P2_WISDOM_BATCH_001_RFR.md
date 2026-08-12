# P2 Wisdom Batch 001 R-F-R

Status: `ACTIVE TEST RUN`

Source batch: `raw/wisdom/MAHABHARATA_MODELLING_NARRATIVE_BATCH_01.json`

Derivation: `phase2/wisdom/WISDOM_BATCH_001_DERIVATION.json`

This is the first bounded Wisdom ingestion test. The source is explicitly a user-provided Mahabharata modelling / interpretive narrative, not primary scripture and not independently verified history or theology.

```text
SOURCE TEXT
↓
SOURCE CLAIM
↓
INTERPRETATION
↓
SUPPORTING SEQUENCE RECONSTRUCTION
↓
WISDOM CANDIDATE
↓
R-F-R
```

Pass criteria:

- all five candidates reverse-trace to bounded source excerpts;
- Source Claim does not become source fact outside the supplied modelling lens;
- Interpretation remains explicitly derived;
- Wisdom remains candidate, not law;
- applicability and non-applicability conditions are present;
- primary-scripture, counter-case and external-verification debt remain visible;
- no Wisdom candidate has direct action authority.

Generated report target:

`generated/tests/P2_WISDOM_BATCH_001_RFR.json`
