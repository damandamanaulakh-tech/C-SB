import { stageRecord } from '../shared.js';

export function contextWindowStage({ inputStage, tokenStage, repositoryContext }) {
  return stageRecord(5, 'context-window', 'sourceborn', {
    activePrompt: inputStage?.data?.prompt ?? '',
    sourcebornTraceTokenCount: tokenStage?.data?.tokenCount ?? 0,
    repositoryContext: repositoryContext ?? null,
    contextPolicy: 'bounded-explicit-context-only',
    hiddenGlobalMemoryAssumed: false,
  });
}
