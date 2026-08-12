import { stageRecord } from '../shared.js';

export function feedbackTrainingStage({ feedback = null } = {}) {
  return stageRecord(14, 'feedback-training', 'sourceborn-boundary', {
    feedbackCaptured: feedback !== null && feedback !== undefined,
    feedback,
    modifiesModelWeights: false,
    liveTrainingPerformed: false,
    note: 'Training/fine-tuning is an explicit external lifecycle, never implied by one runtime request.',
  });
}
