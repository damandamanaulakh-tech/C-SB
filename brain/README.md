# Sourceborn LLM Brain Walkthrough

This directory is the canonical runtime shape for the recovered Sourceborn orchestrator. It mirrors the attached 14-stage LLM walkthrough while keeping a hard distinction between Sourceborn-owned processing and opaque model internals.

## End-to-end flow

```text
WHAT GOES IN
  prompt | files/docs | images | tool results | history
      |
01 user-input
02 preprocessing
03 tokenization
04 embeddings-position
05 context-window
06 llm-brain
07 attention-flow
08 next-token-prediction
09 decoding
10 loop
11 output
   \-> 12 optional-tool-rag -> context/loop
   \-> 13 memory-session-update
   \-> 14 feedback-training
      |
WHAT COMES OUT
  answers | plans/ideas | code | charts/tables | tool actions | audio/image
```

## Truth boundary

Stages 06-09 describe the model-compute boundary. This repository does **not** fabricate hidden chain-of-thought, attention matrices, embeddings, logits, or token probabilities. Those fields remain opaque/adapter-owned unless a real model provider supplies public API data for them.

## Existing C-SB data

The existing canonical repository is not duplicated. `data-map.json` maps existing `CANONICALITY.json`, `phase2/`, `registries/`, `machine/`, `raw/`, `tools/`, and `generated/` assets into the brain stages. `Grok-ASS` is outside this architecture and is not read or changed.

## Code

`pipeline.js` executes all fourteen stage contracts and returns a trace. Each numbered directory contains the stage implementation. The recovered `src/orchestrator.js` attaches this walkthrough trace to every orchestration result.
