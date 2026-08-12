import { stageRecord } from '../shared.js';

export function nextTokenPredictionStage() {
  return stageRecord(8, 'next-token-prediction', 'model-internal', {
    logits: null,
    probabilities: null,
    candidates: null,
    status: 'opaque-model-internal',
    note: 'No fake logits, probabilities, or top-token candidates are generated.',
  });
}
