import crypto from 'node:crypto';
import http from 'node:http';
import path from 'node:path';
import { fileURLToPath } from 'node:url';
import { BRAIN_ARCHITECTURE } from '../brain/pipeline.js';
import { orchestrate } from './orchestrator.js';
import { getRepositoryContext } from './repository-context.js';

const port = Number(process.env.PORT || 3000);
const DEFAULT_MAX_BODY_BYTES = 1_000_000;
const RUNTIME_VERSION = '1.2.0';

class HttpError extends Error {
  constructor(statusCode, code, message) {
    super(message);
    this.statusCode = statusCode;
    this.code = code;
  }
}

function sendJson(res, statusCode, payload, extraHeaders = {}) {
  const body = JSON.stringify(payload);
  res.writeHead(statusCode, {
    'Content-Type': 'application/json; charset=utf-8',
    'Content-Length': Buffer.byteLength(body),
    'Cache-Control': 'no-store',
    'X-Content-Type-Options': 'nosniff',
    ...extraHeaders,
  });
  res.end(body);
}

function readBody(req, maxBytes) {
  return new Promise((resolve, reject) => {
    let body = '';
    let total = 0;
    let settled = false;

    req.on('data', (chunk) => {
      if (settled) return;
      total += chunk.length;
      if (total > maxBytes) {
        settled = true;
        reject(new HttpError(413, 'payload_too_large', 'Request body is too large.'));
        return;
      }
      body += chunk.toString('utf8');
    });
    req.on('end', () => {
      if (!settled) {
        settled = true;
        resolve(body);
      }
    });
    req.on('error', (error) => {
      if (!settled) {
        settled = true;
        reject(error);
      }
    });
  });
}

function safeTokenEqual(left, right) {
  const a = Buffer.from(String(left));
  const b = Buffer.from(String(right));
  return a.length === b.length && crypto.timingSafeEqual(a, b);
}

function requestToken(req) {
  const bearer = req.headers.authorization;
  if (typeof bearer === 'string' && bearer.startsWith('Bearer ')) return bearer.slice(7);
  const apiKey = req.headers['x-api-key'];
  return typeof apiKey === 'string' ? apiKey : '';
}

function clientKey(req, trustProxy) {
  if (trustProxy) {
    const forwarded = req.headers['x-forwarded-for'];
    if (typeof forwarded === 'string' && forwarded.trim()) return forwarded.split(',')[0].trim();
  }
  return req.socket.remoteAddress || 'unknown';
}

function createRateLimiter(maxRequests, windowMs) {
  const buckets = new Map();
  return (key) => {
    const now = Date.now();
    const current = buckets.get(key);
    if (!current || current.resetAt <= now) {
      buckets.set(key, { count: 1, resetAt: now + windowMs });
      return { allowed: true, retryAfterSeconds: 0 };
    }
    current.count += 1;
    if (current.count <= maxRequests) return { allowed: true, retryAfterSeconds: 0 };
    return { allowed: false, retryAfterSeconds: Math.max(1, Math.ceil((current.resetAt - now) / 1000)) };
  };
}

function validateArrayField(parsed, field) {
  if (parsed[field] != null && !Array.isArray(parsed[field])) {
    throw new HttpError(400, `invalid_${field}`, `${field} must be an array.`);
  }
}

export function createServer(options = {}) {
  const apiKey = options.apiKey ?? process.env.SOURCEBORN_API_KEY ?? '';
  const requireApiKey = options.requireApiKey ?? process.env.NODE_ENV === 'production';
  const trustProxy = options.trustProxy ?? process.env.TRUST_PROXY === '1';
  const maxBodyBytes = options.maxBodyBytes ?? DEFAULT_MAX_BODY_BYTES;
  const rateLimitMax = options.rateLimitMax ?? Number(process.env.RATE_LIMIT_MAX || 60);
  const rateLimitWindowMs = options.rateLimitWindowMs ?? Number(process.env.RATE_LIMIT_WINDOW_MS || 60_000);
  const checkRateLimit = createRateLimiter(rateLimitMax, rateLimitWindowMs);

  return http.createServer(async (req, res) => {
    const url = new URL(req.url ?? '/', 'http://localhost');

    if (req.method === 'GET' && url.pathname === '/api/health') {
      sendJson(res, 200, {
        ok: true,
        engine: 'Sourceborn URR Orchestrator',
        version: RUNTIME_VERSION,
        architecture: BRAIN_ARCHITECTURE.id,
        repository: getRepositoryContext(),
        security: {
          apiKeyRequired: requireApiKey,
          apiKeyConfigured: Boolean(apiKey),
        },
      });
      return;
    }

    if (req.method === 'GET' && url.pathname === '/api/brain') {
      sendJson(res, 200, {
        ok: true,
        engine: 'Sourceborn URR Orchestrator',
        version: RUNTIME_VERSION,
        architecture: BRAIN_ARCHITECTURE,
        truthBoundary: {
          hiddenChainOfThoughtExposed: false,
          syntheticEmbeddingsCreated: false,
          syntheticAttentionCreated: false,
          syntheticLogitsCreated: false,
          grokAssRead: false,
        },
      });
      return;
    }

    if (url.pathname === '/api/ask' && req.method !== 'POST') {
      sendJson(res, 405, { ok: false, error: 'method_not_allowed' }, { Allow: 'POST' });
      return;
    }

    if (req.method === 'POST' && url.pathname === '/api/ask') {
      try {
        if (requireApiKey && !apiKey) {
          throw new HttpError(503, 'service_not_configured', 'API authentication is required but no key is configured.');
        }
        if (apiKey && !safeTokenEqual(requestToken(req), apiKey)) {
          throw new HttpError(401, 'unauthorized', 'A valid API key is required.');
        }

        const rate = checkRateLimit(clientKey(req, trustProxy));
        if (!rate.allowed) {
          sendJson(res, 429, { ok: false, error: 'rate_limited' }, { 'Retry-After': String(rate.retryAfterSeconds) });
          return;
        }

        const contentType = String(req.headers['content-type'] || '').toLowerCase();
        if (!contentType.startsWith('application/json')) {
          throw new HttpError(415, 'unsupported_media_type', 'Content-Type must be application/json.');
        }

        const body = await readBody(req, maxBodyBytes);
        let parsed;
        try {
          parsed = body ? JSON.parse(body) : {};
        } catch {
          throw new HttpError(400, 'invalid_json', 'Request body must contain valid JSON.');
        }

        if (parsed.message != null && typeof parsed.message !== 'string') {
          throw new HttpError(400, 'invalid_message', 'message must be a string.');
        }
        if (parsed.mode != null && typeof parsed.mode !== 'string') {
          throw new HttpError(400, 'invalid_mode', 'mode must be a string.');
        }
        for (const field of ['files', 'images', 'toolResults', 'history']) validateArrayField(parsed, field);

        const repositoryContext = getRepositoryContext();
        sendJson(res, 200, orchestrate({
          message: parsed.message,
          mode: parsed.mode,
          repositoryContext,
          files: parsed.files ?? [],
          images: parsed.images ?? [],
          toolResults: parsed.toolResults ?? [],
          history: parsed.history ?? [],
          feedback: parsed.feedback ?? null,
        }));
      } catch (error) {
        if (error instanceof HttpError) {
          const headers = error.statusCode === 401 ? { 'WWW-Authenticate': 'Bearer realm="sourceborn"' } : {};
          sendJson(res, error.statusCode, { ok: false, error: error.code }, headers);
          return;
        }
        console.error('Sourceborn request failed:', error);
        sendJson(res, 500, { ok: false, error: 'internal_error' });
      }
      return;
    }

    sendJson(res, 404, { ok: false, error: 'not_found' });
  });
}

const isMainModule = process.argv[1] && path.resolve(process.argv[1]) === fileURLToPath(import.meta.url);

if (isMainModule) {
  createServer().listen(port, () => {
    console.log(`Sourceborn URR orchestrator listening on port ${port}`);
  });
}
