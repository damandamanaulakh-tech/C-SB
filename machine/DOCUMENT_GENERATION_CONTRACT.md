# Document Generation Contract

Generated documents must:

1. Read `CANONICALITY.json` first.
2. Treat `raw/sequence/Universal_Sequence_Machine_Architecture_v1.md` as the canonical Phase-1 execution grammar once that source is present.
3. Preserve native rubric IDs exactly.
4. Rebuild a cross-reference index with `tools/relink_and_index.py` before generating link-heavy documents.
5. Distinguish source facts, approved registry definitions, mappings, interpretations, inferences and unknowns.
6. Never activate `REVIEW_ONLY` AI capability families without an explicit approval record.
7. Never fabricate absent Human parameter rows.
8. When a historical document conflicts with canonical rules, preserve the historical artifact but follow `CANONICALITY.json`.
9. Every generated mapping document must include source references and an orphan/gap section.
10. Every adopted batch must end in an Adoption Closure Packet.

## Self-relink rule

```text
NATIVE ID
↓
SCAN ALL SOURCE / REGISTRY / MAPPING FILES
↓
BUILD REFERENCE INDEX
↓
RESOLVE STRUCTURAL PARENT
↓
RESOLVE SEQUENCE BINDINGS
↓
RESOLVE ASI-NODE BINDINGS
↓
GENERATE LINK REPORT
```

A generated document may propose new mappings, but proposed mappings remain separate from approved native data until adopted through the Phase-2 workflow.
