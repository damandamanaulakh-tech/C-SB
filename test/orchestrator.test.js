import assert from 'node:assert/strict';
import { test } from 'node:test';
import { orchestrate } from '../src/orchestrator.js';

test('orchestrate creates required traceability and public output', () => {
  const run = orchestrate({ message: 'URR must not skip steps. Build clean output.', mode: 'standard' });

  assert.match(run.runId, /^urr_/);
  assert.equal(run.rawLock.immutable, true);
  assert.equal(run.rawLock.checksum.length, 64);
  assert.ok(Array.isArray(run.stages.claimLedger.claims));
  assert.ok(run.stages.claimLedger.claims.length >= 1);
  assert.ok(Array.isArray(run.stages.urr.checks));
  assert.equal(run.stages.urr.decision, 'pass');
  assert.equal(typeof run.stages.publicOutput.answer, 'string');
  assert.ok(run.masterLog.some((entry) => entry.event === 'urr-decision'));
});

test('empty raw source stays honest with tagged assumption', () => {
  const run = orchestrate({ message: '', mode: 'standard' });

  assert.equal(run.stages.claimLedger.claims.length, 0);
  assert.equal(run.stages.claimLedger.assumptions[0].tag, 'assumption');
  assert.equal(run.stages.loopRoute.route, 'proof-loop');
});

test('repository context can be carried into a run without changing source semantics', () => {
  const repositoryContext = { phase2Status: 'ACTIVE' };
  const run = orchestrate({ message: 'Preserve this.', repositoryContext });

  assert.deepEqual(run.repositoryContext, repositoryContext);
  assert.equal(run.stages.claimLedger.claims[0].text, 'Preserve this.');
});
