# C-SB — Sourceborn ASI

Canonical Sourceborn repository for the **Universal Sequence grammar**, **Phase-2 Human/AI/Wisdom/ASI construction and adoption**, and the **ASI Node / Node-Brain runtime**.

## Current status

```text
PHASE 1 — UNIVERSAL SEQUENCE
CLOSED BASELINE
        ↓
PHASE 2 — ACTIVE
        │
        ├── P2-H  HUMAN
        ├── P2-A  AI
        ├── P2-W  WISDOM / HOLY BOOKS
        └── P2-S  ASI
                 ↓
         MULTI-RUBRIC WIRING
                 ↓
                R-F-R
                 ↓
         PHASE-2 CLOSURE
```

The key machine rule is:

> Universal Sequence is a grammar, not a fixed chronological timeline. Every real case declares an end/scope, is reverse-mined, forward reconstructed, reverse-audited, and closes only when its declared contract is terminal.

## Sourceborn is not an LLM wrapper

Current LLM/AI architectures may be studied as reverse-engineering evidence for useful functions, but Sourceborn does **not** assume an LLM API, Transformer runtime, next-token engine, or monolithic model as its Brain.

```text
CURRENT AI SYSTEM
      ↓
reverse-engineer useful function
      ↓
SOURCEBORN-NATIVE AI RUBRIC / MECHANISM
```

## Read first

1. `CANONICALITY.json`
2. `raw/sequence/Universal_Sequence_Machine_Architecture_v1.manifest.json`
3. `raw/phase2/SOURCEBORN_ASI_PHASE2_ADOPTION_CONFIG.manifest.json`
4. `phase2/README.md`
5. `machine/wiring/MULTI_RUBRIC_WIRING_V0.json`
6. `registries/asi/asi_node_registry.json`
7. `docs/LOCKED_DECISIONS.md`
8. `docs/SEQUENCE_RESEARCH_LEDGER.md`

## Phase-2 registries

### Human
- Approved architecture: `10 Segments → 80 Containers → 2,560 parameters`.
- Native IDs/names/definitions must be preserved.
- Full native 2,560-row payload is still a required dependency if not present under `registries/human/native/`.

### AI
- `registries/ai/AI_RUBRIC_V0.json`
- Native artificial-cognition functions, not an LLM capability wrapper.
- Existing 74-family AI capability crosswalk remains **REVIEW ONLY**.

### Wisdom / Holy Books
- `registries/wisdom/WISDOM_REGISTRY_V0.json`
- `registries/wisdom/HOLY_BOOK_SOURCE_TO_WISDOM_CONTRACT.json`
- Source Text, Source Claim, Interpretation, Wisdom and Law/Guidance remain distinct records.

### ASI
- `registries/asi/ASI_RUBRIC_V0.json`
- ASI is the meta-governance layer across Human, AI, Wisdom, Sequences, memories, priorities, permissions, contradictions and closure scopes.

## ASI Node network

`registries/asi/asi_node_registry.json` is a service registry, not a chronological Sequence.

Current service classes: `ASI-NODE-00..21`.

New Phase-2 service nodes:
- `ASI-NODE-18` — Holy-Book / Wisdom Source Interpreter
- `ASI-NODE-19` — Wisdom / Principle Synthesis
- `ASI-NODE-20` — AI Rubric / Cognitive Mechanism Router
- `ASI-NODE-21` — ASI Rubric / Meta-Governor

Node Brain contracts for the new nodes:
- `registries/asi/node_brains/NODE_BRAINS_18_21.json`

## Machine-readable layers

- `machine/schemas/` — Sequence, Node, Edge, Sub-Sequence Contract, Closure Packet, Seed, View and Rubric schemas.
- `machine/vocab/` — order types, drivers, thresholds, controller types, relation types and statuses.
- `machine/wiring/` — cross-domain/rubric wiring maps.
- `machine/rubrics/` — orthogonal machine rubric dimensions.
- `registries/human/` — Human native-registry adoption contract and data when supplied.
- `registries/ai/` — Sourceborn-native AI rubric construction.
- `registries/wisdom/` — Wisdom and source-custody architecture.
- `registries/asi/` — ASI meta-rubric, ASI Node registry and Node Brains.
- `tools/relink_and_index.py` — scans repository IDs and generates cross-reference documents.
- `tools/validate_repo.py` — checks locked invariants that can be checked statically.

## Runtime — recovered URR orchestrator

The Codex URR prototype has been recovered into the current repository and wired to read canonical Phase/registry status without mutating the canonical registries.

```bash
npm ci
npm run check
npm start
```

Runtime endpoints:

- `GET /api/health` — service health plus bounded repository/Phase status.
- `POST /api/ask` — raw-source lock, fragment/claim ledger, URR checks, proof-debt routing and public output.

Production mode fails closed unless `SOURCEBORN_API_KEY` is configured. Call `/api/ask` with `Authorization: Bearer <key>` (or `X-API-Key`). The server also applies a 1 MB body limit, JSON validation, safer error responses and an in-memory request rate limit. `render.yaml` keeps automatic deployment disabled until the service secret is configured.

The original Codex prototype README is preserved at `docs/CODEX_ORCHESTRATOR_RECOVERY.md`.

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
- Source Text != Source Claim != Interpretation != Wisdom != Law/Guidance.
- AI cognition != ASI governance.
