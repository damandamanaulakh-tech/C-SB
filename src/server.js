import http from 'node:http';
import { orchestrate } from './orchestrator.js';

const port = process.env.PORT || 3000;

function sendJson(res, statusCode, payload) {
  const body = JSON.stringify(payload);
  res.writeHead(statusCode, {
    'Content-Type': 'application/json; charset=utf-8',
    'Content-Length': Buffer.byteLength(body),
  });
  res.end(body);
}

function readBody(req) {
  return new Promise((resolve, reject) => {
    let body = '';
    req.on('data', (chunk) => {
      body += chunk;
      if (body.length > 1_000_000) {
        reject(new Error('Request body is too large.'));
        req.destroy();
      }
    });
    req.on('end', () => resolve(body));
    req.on('error', reject);
  });
}

export function createServer() {
  return http.createServer(async (req, res) => {
    const url = new URL(req.url ?? '/', `http://${req.headers.host ?? 'localhost'}`);

    if (req.method === 'GET' && url.pathname === '/api/health') {
      sendJson(res, 200, { ok: true });
      return;
    }

    if (req.method === 'POST' && url.pathname === '/api/ask') {
      try {
        const body = await readBody(req);
        const parsed = body ? JSON.parse(body) : {};
        sendJson(res, 200, orchestrate({ message: parsed.message, mode: parsed.mode }));
      } catch (error) {
        sendJson(res, 400, { ok: false, error: error.message });
      }
      return;
    }

    sendJson(res, 404, { ok: false, error: 'Not found' });
  });
}

if (process.env.NODE_ENV !== 'test') {
  createServer().listen(port, () => {
    console.log(`Sourceborn URR orchestrator listening on port ${port}`);
  });
}
