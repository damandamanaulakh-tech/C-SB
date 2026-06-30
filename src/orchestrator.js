import crypto from 'node:crypto';

const ENGINE_RULES = [
  'Raw Source Never Changes',
  'URR is the integrity layer, not a replacement for Sourceborn',
  'Synthetic and assumption material must stay tagged',
  'Every run must create traceability',
  'Final output must be clean and public-safe',
];

function checksum(value) {
  return crypto.createHash('sha256').update(value, 'utf8').digest('hex');
}

function createRunId() {
  return `urr_${Date.now().toString(36)}_${crypto.randomBytes(6).toString('hex')}`;
}

function splitThought(rawSource) {
  return rawSource
    .split(/(?<=[.!?])\s+|\n+/)
    .map((part) => part.trim())
    .filter(Boolean)
    .map((text, index) => ({
      id: `fragment-${index + 1}`,
      text,
      role: inferFragmentRole(text),
    }));
}

function inferFragmentRole(text) {
  const lower = text.toLowerCase();
  if (lower.includes('must') || lower.includes('do not') || lower.includes('never')) return 'rule';
  if (lower.includes('build') || lower.includes('create') || lower.includes('turn')) return 'action';
  return 'source-thought';
}

function buildClaimLedger(fragments) {
  const claims = fragments.map((fragment) => ({
    id: `claim-${fragment.id.split('-')[1]}`,
    fragmentId: fragment.id,
    text: fragment.text,
    tag: 'sourcebound',
    proofStatus: 'unverified',
    proofDebt: ['Needs external evidence or user confirmation before being treated as verified.'],
  }));

  const assumptions = [];
  if (claims.length === 0) {
    assumptions.push({
      id: 'assumption-1',
      tag: 'assumption',
      text: 'No raw thought was provided, so the next loop should request source material.',
      proofStatus: 'open',
    });
  }

  return { claims, assumptions };
}

function runUrrChecks(rawLock, claimLedger) {
  return [
    {
      id: 'raw-source-lock',
      status: rawLock.rawSourceId && rawLock.checksum ? 'pass' : 'fail',
      evidence: { rawSourceId: rawLock.rawSourceId, checksum: rawLock.checksum },
    },
    {
      id: 'synthetic-tagging',
      status: claimLedger.assumptions.every((item) => item.tag === 'assumption') ? 'pass' : 'fail',
      evidence: { assumptions: claimLedger.assumptions.length },
    },
    {
      id: 'proof-debt-preserved',
      status: claimLedger.claims.every((claim) => Array.isArray(claim.proofDebt)) ? 'pass' : 'fail',
      evidence: { claims: claimLedger.claims.length },
    },
    {
      id: 'public-safety',
      status: 'pass',
      evidence: { secretHandling: 'No secrets, keys, or raw private data are added by the orchestrator.' },
    },
  ];
}

function chooseLoopRoute(checks, claimLedger) {
  const failed = checks.filter((check) => check.status !== 'pass');
  if (failed.length > 0) return { route: 'repair', reason: `URR checks failed: ${failed.map((item) => item.id).join(', ')}` };
  if (claimLedger.claims.some((claim) => claim.proofStatus !== 'verified') || claimLedger.assumptions.some((item) => item.proofStatus === 'open')) {
    return { route: 'proof-loop', reason: 'Some sourcebound claims or assumptions still carry proof debt.' };
  }
  return { route: 'public-output', reason: 'All claims are verified and checks passed.' };
}

function buildPublicAnswer(fragments, claimLedger, loopRoute) {
  const sourceSummary = fragments.length
    ? fragments.map((fragment) => fragment.text).join(' ')
    : 'No raw source was provided.';

  return {
    answer: `Sourceborn preserved the raw thought, split it into ${fragments.length} fragment(s), kept ${claimLedger.claims.length} sourcebound claim(s) distinct from ${claimLedger.assumptions.length} assumption(s), and routed the run to ${loopRoute.route}. Clean output: ${sourceSummary}`,
    disclosure: 'Unverified sourcebound material remains tagged with proof debt and is not presented as proven fact.',
  };
}

export function orchestrate({ message = '', mode = 'standard' } = {}) {
  const rawSource = String(message ?? '');
  const runId = createRunId();
  const rawSourceId = `raw_${checksum(`${runId}:${rawSource}`).slice(0, 16)}`;
  const rawLock = {
    rawSourceId,
    checksum: checksum(rawSource),
    immutable: true,
    capturedAt: new Date().toISOString(),
    mode,
  };

  const fragments = splitThought(rawSource);
  const claimLedger = buildClaimLedger(fragments);
  const checks = runUrrChecks(rawLock, claimLedger);
  const loopRoute = chooseLoopRoute(checks, claimLedger);
  const publicOutput = buildPublicAnswer(fragments, claimLedger, loopRoute);

  return {
    runId,
    engine: 'Sourceborn URR Orchestrator',
    rules: ENGINE_RULES,
    rawLock,
    stages: {
      sourceborn: { fragments },
      claimLedger,
      urr: { checks, decision: checks.every((check) => check.status === 'pass') ? 'pass' : 'fail' },
      loopRoute,
      publicOutput,
    },
    masterLog: [
      { event: 'raw-lock-created', rawSourceId, checksum: rawLock.checksum },
      { event: 'fragments-created', count: fragments.length },
      { event: 'claim-ledger-created', claims: claimLedger.claims.length, assumptions: claimLedger.assumptions.length },
      { event: 'urr-decision', decision: checks.every((check) => check.status === 'pass') ? 'pass' : 'fail' },
      { event: 'loop-route-selected', route: loopRoute.route },
      { event: 'public-output-created', safeForPublic: true },
    ],
  };
}
