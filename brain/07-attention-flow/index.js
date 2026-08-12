import { stageRecord } from '../shared.js';

export function attentionFlowStage() {
  return stageRecord(7, 'attention-flow', 'model-internal', {
    attentionWeights: null,
    status: 'opaque-model-internal',
    causalMaskTelemetry: null,
    note: 'Attention data is populated only if a real provider exposes supported telemetry.',
  });
}
