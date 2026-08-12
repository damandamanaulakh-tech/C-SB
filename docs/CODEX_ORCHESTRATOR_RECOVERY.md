# Codex Orchestrator Recovery

Recovered from the closed Codex PR (`codex/deploy-sourceborn-urr-orchestrator-to-render`, commit `c29c8b13c982bf876633315725f538612c2ed14f`). The original README content is preserved below while the runtime itself has been integrated and hardened against the current C-SB tree.

---

# Sourceborn URR Orchestrator

A minimal Node.js API that preserves Sourceborn / URR integrity rules while turning raw thought into traceable, public-safe output.

## Engine guarantees

- Raw source is locked with an immutable source ID and SHA-256 checksum.
- Sourcebound claims stay separate from assumptions and synthetic material.
- Proof debt is preserved instead of silently treating unfinished ideas as verified.
- Every run includes a master log, URR checks, loop routing, and public output.

## Local development

```bash
npm install
npm test
npm start
```

Health check:

```bash
curl http://localhost:3000/api/health
```

Ask endpoint:

```bash
curl -X POST http://localhost:3000/api/ask \
  -H "Content-Type: application/json" \
  -d '{"message":"URR must not skip steps. Build clean output.","mode":"standard"}'
```

## Render deployment

This repository includes `render.yaml` for Render Blueprint/Web Service deployment.

- Runtime: Node
- Build Command: `npm install`
- Start Command: `npm start`
- Health URL: `/api/health`
