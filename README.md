# C-SB — Sourceborn ASI

Canonical Sourceborn repository for the **Universal Sequence grammar**, **Phase-2 rubric adoption**, and the **ASI Node / Node-Brain runtime**.

## Current status

```text
PHASE 1 — UNIVERSAL SEQUENCE
CLOSED BASELINE
        ↓
PHASE 2 — HUMAN / AI / ASI / DOMAIN RUBRIC ADOPTION
ACTIVE
```

The key machine rule is:

> Universal Sequence is a grammar, not a fixed 57-step chronological timeline. Every real case declares an end/scope, is reverse-mined, forward reconstructed, reverse-audited, and closes only when its declared contract is terminal.

## Read first

1. `CANONICALITY.json`
2. `raw/sequence/Universal_Sequence_Machine_Architecture_v1.manifest.json`
3. `raw/phase2/SOURCEBORN_ASI_PHASE2_ADOPTION_CONFIG.manifest.json`
4. `phase2/README.md`
5. `docs/LOCKED_DECISIONS.md`
6. `docs/SEQUENCE_RESEARCH_LEDGER.md`

The two canonical long source documents are stored as exact ordered parts. Their manifests contain the source SHA-256 and reconstruction order.

## Machine-readable layers

- `machine/schemas/` — Sequence, Node, Edge, Sub-Sequence Contract, Closure Packet, Seed, View and Rubric schemas.
- `machine/vocab/` — order types, drivers, thresholds, controller types, relation types and statuses.
- `registries/asi/` — ASI Node service registry.
- `registries/human/` — Human native-registry adoption contract. The full 2,560-row native Human registry must be imported unchanged when supplied.
- `raw/rubrics/AI_CAPABILITY_TO_SOURCEBORN_CONTAINERS_REVIEW.md` — current 74-family AI review map; it is **REVIEW ONLY**.
- `tools/relink_and_index.py` — scans repository IDs and generates cross-reference documents.
- `tools/validate_repo.py` — checks locked invariants that can be checked statically.

## Source preservation

`raw/` preserves source text artifacts and research outputs. Historical files are not deleted when superseded; canonical precedence is recorded in `CANONICALITY.json`.

Binary visual artifacts from the working session are listed with SHA-256 hashes in `raw/visuals/BINARY_ARTIFACT_MANIFEST.json`. Text-native visual sources such as SVG are archived directly when available.

## Core invariants

- No in-place loop.
- No reopening a closed Sequence.
- Local Barrier Law on dependent edges.
- Trigger and threshold are separate.
- Sequence closure and entity outcome are separate.
- Close condition and acceptance condition are separate.
- Driver, Controller, Performer and Carrier are separate.
- Seeds and Actor Views are first-class.
- Unknown provenance remains unknown.
- Native rubric IDs are never silently rewritten.
