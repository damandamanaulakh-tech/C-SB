import { stageRecord } from '../shared.js';

export function tokenizationStage(previous) {
  const text = previous?.data?.normalizedText ?? '';
  const tokens = text.match(/[\p{L}\p{N}_]+|[^\s\p{L}\p{N}_]/gu) ?? [];
  return stageRecord(3, 'tokenization', 'sourceborn-boundary', {
    tokenizer: 'sourceborn-lexical-trace-v1',
    modelTokenizer: false,
    tokenCount: tokens.length,
    tokens: tokens.map((value, index) => ({ index, value })),
    note: 'Trace tokens are for Sourceborn observability only; provider model tokenization can differ.',
  });
}
