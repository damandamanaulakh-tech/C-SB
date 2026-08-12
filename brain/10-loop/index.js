import { stageRecord } from '../shared.js';

export function loopStage({ proofDebtOpen = false, urrRoute = null, toolRequested = false } = {}) {
  let route = urrRoute ?? 'public-output';
  if (toolRequested) route = 'tool-rag';
  else if (proofDebtOpen && !urrRoute) route = 'proof-loop';
  return stageRecord(10, 'loop', 'sourceborn', {
    route,
    proofDebtOpen: Boolean(proofDebtOpen),
    toolRequested: Boolean(toolRequested),
    stoppingCriteria: route === 'public-output' ? 'public-safe-output-ready' : 'continuation-required',
  });
}
