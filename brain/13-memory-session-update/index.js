import { stageRecord } from '../shared.js';

export function memorySessionUpdateStage({ history = [], runId = null } = {}) {
  return stageRecord(13, 'memory-session-update', 'sourceborn', {
    runId,
    priorTurnCount: history.length,
    sessionStateUpdated: true,
    persistence: 'request/session-boundary-only',
    persistentMemoryByDefault: false,
  });
}
