import { userInputStage } from './01-user-input/index.js';
import { preprocessingStage } from './02-preprocessing/index.js';
import { tokenizationStage } from './03-tokenization/index.js';
import { embeddingsPositionStage } from './04-embeddings-position/index.js';
import { contextWindowStage } from './05-context-window/index.js';
import { llmBrainStage } from './06-llm-brain/index.js';
import { attentionFlowStage } from './07-attention-flow/index.js';
import { nextTokenPredictionStage } from './08-next-token-prediction/index.js';
import { decodingStage } from './09-decoding/index.js';
import { loopStage } from './10-loop/index.js';
import { outputStage } from './11-output/index.js';
import { optionalToolRagStage } from './12-optional-tool-rag/index.js';
import { memorySessionUpdateStage } from './13-memory-session-update/index.js';
import { feedbackTrainingStage } from './14-feedback-training/index.js';

export const BRAIN_ARCHITECTURE = Object.freeze({
  id: 'sourceborn-llm-brain-walkthrough-v1',
  stageCount: 14,
  stages: [
    { id: 1, slug: 'user-input', owner: 'sourceborn' },
    { id: 2, slug: 'preprocessing', owner: 'sourceborn' },
    { id: 3, slug: 'tokenization', owner: 'sourceborn-boundary' },
    { id: 4, slug: 'embeddings-position', owner: 'model-adapter' },
    { id: 5, slug: 'context-window', owner: 'sourceborn' },
    { id: 6, slug: 'llm-brain', owner: 'model-internal' },
    { id: 7, slug: 'attention-flow', owner: 'model-internal' },
    { id: 8, slug: 'next-token-prediction', owner: 'model-internal' },
    { id: 9, slug: 'decoding', owner: 'model-adapter' },
    { id: 10, slug: 'loop', owner: 'sourceborn' },
    { id: 11, slug: 'output', owner: 'sourceborn' },
    { id: 12, slug: 'optional-tool-rag', owner: 'sourceborn' },
    { id: 13, slug: 'memory-session-update', owner: 'sourceborn' },
    { id: 14, slug: 'feedback-training', owner: 'sourceborn-boundary' },
  ],
  inputs: ['prompt', 'files-docs', 'images', 'tool-results', 'history'],
  outputs: ['answers', 'plans-ideas', 'code', 'charts-tables', 'tool-actions', 'audio-image'],
});

export function runBrainWalkthrough({
  message = '',
  mode = 'standard',
  repositoryContext = null,
  modelOutput = null,
  decodingMetadata = null,
  urrRoute = null,
  proofDebtOpen = false,
  files = [],
  images = [],
  toolResults = [],
  history = [],
  feedback = null,
  runId = null,
} = {}) {
  const s01 = userInputStage({ message, mode, files, images, toolResults, history });
  const s02 = preprocessingStage(s01);
  const s03 = tokenizationStage(s02);
  const s04 = embeddingsPositionStage(s03);
  const s05 = contextWindowStage({ inputStage: s01, tokenStage: s03, repositoryContext });
  const s06 = llmBrainStage();
  const s07 = attentionFlowStage();
  const s08 = nextTokenPredictionStage();
  const s09 = decodingStage({ modelOutput, decodingMetadata });
  const s10 = loopStage({ proofDebtOpen, urrRoute, toolRequested: toolResults.length > 0 });
  const s11 = outputStage({ modelOutput, loopRoute: s10.data.route });
  const s12 = optionalToolRagStage({ repositoryContext, toolResults });
  const s13 = memorySessionUpdateStage({ history, runId });
  const s14 = feedbackTrainingStage({ feedback });
  const stages = [s01,s02,s03,s04,s05,s06,s07,s08,s09,s10,s11,s12,s13,s14];

  return {
    architecture: BRAIN_ARCHITECTURE.id,
    stageCount: stages.length,
    stages,
    stageMap: Object.fromEntries(stages.map((stage) => [String(stage.id).padStart(2, '0'), stage])),
    truthBoundary: {
      hiddenChainOfThoughtExposed: false,
      syntheticEmbeddingsCreated: false,
      syntheticAttentionCreated: false,
      syntheticLogitsCreated: false,
      grokAssRead: false,
    },
  };
}
