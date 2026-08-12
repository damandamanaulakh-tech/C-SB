import { stageRecord } from '../shared.js';

export function decodingStage({ modelOutput = null, decodingMetadata = null } = {}) {
  return stageRecord(9, 'decoding', 'model-adapter', {
    outputAvailable: typeof modelOutput === 'string' && modelOutput.length > 0,
    modelOutput,
    decodingMetadata,
    inventedSamplingSettings: false,
  });
}
