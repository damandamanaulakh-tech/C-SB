import { stageRecord } from '../shared.js';

export function preprocessingStage(previous) {
  const prompt = previous?.data?.prompt ?? '';
  const normalizedText = prompt.replace(/\r\n?/g, '\n').replace(/[ \t]+/g, ' ').trim();
  return stageRecord(2, 'preprocessing', 'sourceborn', {
    normalizedText,
    changed: normalizedText !== prompt,
    sourceLength: prompt.length,
    normalizedLength: normalizedText.length,
  });
}
