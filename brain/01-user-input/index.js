import { safeString, stageRecord } from '../shared.js';

export function userInputStage(input = {}) {
  const message = safeString(input.message);
  return stageRecord(1, 'user-input', 'sourceborn', {
    prompt: message,
    files: Array.isArray(input.files) ? input.files : [],
    images: Array.isArray(input.images) ? input.images : [],
    toolResults: Array.isArray(input.toolResults) ? input.toolResults : [],
    history: Array.isArray(input.history) ? input.history : [],
    mode: input.mode ?? 'standard',
  });
}
