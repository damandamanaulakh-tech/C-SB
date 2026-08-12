import assert from 'node:assert/strict';
import { test } from 'node:test';
import { createServer } from '../src/server.js';

async function withServer(options, fn) {
  const server = createServer(options);
  await new Promise((resolve) => server.listen(0, '127.0.0.1', resolve));
  const address = server.address();
  try {
    await fn(`http://127.0.0.1:${address.port}`);
  } finally {
    await new Promise((resolve, reject) => server.close((error) => error ? reject(error) : resolve()));
  }
}

test('health endpoint reports runtime and repository context', async () => {
  await withServer({ requireApiKey: false }, async (baseUrl) => {
    const response = await fetch(`${baseUrl}/api/health`);
    const body = await response.json();
    assert.equal(response.status, 200);
    assert.equal(body.ok, true);
    assert.equal(body.version, '1.1.0');
    assert.equal(typeof body.repository, 'object');
  });
});

test('production-style protection fails closed when no API key is configured', async () => {
  await withServer({ requireApiKey: true, apiKey: '' }, async (baseUrl) => {
    const response = await fetch(`${baseUrl}/api/ask`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: 'test' }),
    });
    const body = await response.json();
    assert.equal(response.status, 503);
    assert.equal(body.error, 'service_not_configured');
  });
});

test('ask endpoint requires and accepts configured API key', async () => {
  await withServer({ requireApiKey: true, apiKey: 'test-secret' }, async (baseUrl) => {
    const unauthorized = await fetch(`${baseUrl}/api/ask`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: 'test' }),
    });
    assert.equal(unauthorized.status, 401);

    const authorized = await fetch(`${baseUrl}/api/ask`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        Authorization: 'Bearer test-secret',
      },
      body: JSON.stringify({ message: 'URR must preserve source.' }),
    });
    const body = await authorized.json();
    assert.equal(authorized.status, 200);
    assert.equal(body.stages.urr.decision, 'pass');
    assert.equal(body.repositoryContext !== null, true);
  });
});

test('ask endpoint enforces JSON content type and rate limit', async () => {
  await withServer({ requireApiKey: false, rateLimitMax: 1 }, async (baseUrl) => {
    const unsupported = await fetch(`${baseUrl}/api/ask`, {
      method: 'POST',
      body: 'not-json',
    });
    assert.equal(unsupported.status, 415);

    const first = await fetch(`${baseUrl}/api/ask`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: 'one' }),
    });
    assert.equal(first.status, 429);
  });
});
