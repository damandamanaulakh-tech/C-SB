import { stageRecord } from '../shared.js';

export function outputStage({ modelOutput = null, loopRoute = null } = {}) {
  return stageRecord(11, 'output', 'sourceborn', {
    type: 'answer',
    content: modelOutput,
    publicSafeBoundary: true,
    route: loopRoute,
    supportedOutputKinds: ['answers', 'plans-ideas', 'code', 'charts-tables', 'tool-actions', 'audio-image'],
  });
}
