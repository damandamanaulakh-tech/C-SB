export function stageRecord(id, slug, owner, data = {}) {
  return {
    id,
    slug,
    owner,
    status: 'complete',
    capturedAt: new Date().toISOString(),
    data,
  };
}

export function safeString(value) {
  return typeof value === 'string' ? value : String(value ?? '');
}
