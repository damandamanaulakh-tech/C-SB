import assert from 'node:assert/strict';
import { test } from 'node:test';
import { runBrainWalkthrough } from '../brain/pipeline.js';

test('brain walkthrough mirrors all fourteen numbered stages', () => {
  const result = runBrainWalkthrough({
    message: 'Build the Sourceborn engine safely.',
    repositoryContext: { phase2Status: 'ACTIVE' },
    modelOutput: 'Example public output',
    urrRoute: 'proof-loop',
    proofDebtOpen: true,
    runId: 'test-run',
  });

  assert.equal(result.stageCount, 14);
  assert.deepEqual(result.stages.map((stage) => stage.id), [1,2,3,4,5,6,7,8,9,10,11,12,13,14]);
  assert.equal(result.stageMap['05'].data.repositoryContext.phase2Status, 'ACTIVE');
  assert.equal(result.stageMap['10'].data.route, 'proof-loop');
});

test('model-internal boundaries stay truthful instead of fabricating telemetry', () => {
  const result = runBrainWalkthrough({ message: 'Trace this.' });

  assert.equal(result.stageMap['03'].data.modelTokenizer, false);
  assert.equal(result.stageMap['04'].data.embeddings, null);
  assert.equal(result.stageMap['06'].data.hiddenChainOfThoughtExposed, false);
  assert.equal(result.stageMap['07'].data.attentionWeights, null);
  assert.equal(result.stageMap['08'].data.logits, null);
  assert.equal(result.stageMap['14'].data.modifiesModelWeights, false);
  assert.equal(result.truthBoundary.grokAssRead, false);
});

test('tool/RAG stage maps current C-SB data without including Grok-ASS', () => {
  const result = runBrainWalkthrough({ message: 'Use repository context.' });
  const rag = result.stageMap['12'].data;

  assert.equal(rag.repositorySources.registries, 'registries/');
  assert.equal(rag.repositorySources.generatedRegistryViews, 'generated/registry_views/');
  assert.deepEqual(rag.excludedPaths, ['Grok-ASS']);
});
