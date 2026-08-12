import { stageRecord } from '../shared.js';

export function embeddingsPositionStage(previous) {
  const tokens = previous?.data?.tokens ?? [];
  return stageRecord(4, 'embeddings-position', 'model-adapter', {
    positions: tokens.map((token) => ({ tokenIndex: token.index, position: token.index })),
    embeddings: null,
    embeddingStatus: 'adapter-required',
    note: 'No synthetic embedding vectors are generated. Real embeddings must come from a configured model/embedding provider.',
  });
}
