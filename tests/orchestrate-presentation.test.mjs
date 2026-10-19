import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import { normalizeOrchestrateResponse, decisionColor } from '../dashboard/lib/orchestrate-presentation.mjs';

const root = join(dirname(fileURLToPath(import.meta.url)), '..');

test('real PASS with PARTIAL evidence stays visibly qualified, not green', () => {
  const row = normalizeOrchestrateResponse({
    decision: 'PASS', evidence: { status: 'PARTIAL' }, turn: 2,
    effective_confidence: 0.618034, phi_gate: 'SKIP', hpg_fired: true
  });
  assert.equal(row.decision, 'PASS');
  assert.equal(row.evidence_status, 'PARTIAL');
  assert.equal(row.turn, 2);
  assert.equal(row.phi_gate, 'SKIP');
  assert.equal(row.effective_confidence, 0.618034);
  assert.equal(decisionColor(row), '#b45309');
  assert.equal(row.gold_star, undefined);
});

test('explicit gate PASS with PASS evidence is the only green case', () => {
  assert.equal(decisionColor({ decision: 'PASS', evidence: { status: 'PASS' } }), '#047857');
});

for (const decision of ['KILL', 'BLOCKED']) {
  test(`${decision} remains red with BLOCKED evidence or absent confidence`, () => {
    const row = normalizeOrchestrateResponse({ decision, reason: 'refused', evidence: { status: 'BLOCKED' } });
    assert.equal(row.decision, decision);
    assert.equal(row.reason, 'refused');
    assert.equal(row.effective_confidence, null);
    assert.equal(decisionColor(row), '#b91c1c');
  });
}

test('REJECT remains amber even if API evidence reports PASS', () => {
  const row = normalizeOrchestrateResponse({ decision: 'REJECT', evidence: { status: 'PASS' } });
  assert.equal(decisionColor(row), '#b45309');
});

for (const value of [null, {}, [], { decision: 'ESCALATE' }, { dgaf_decision: 'PASS' }, { decision: 'pass' }]) {
  test('unknown or legacy data is not inferred as green', () => {
    const row = normalizeOrchestrateResponse(value);
    assert.equal(row.decision, 'UNKNOWN');
    assert.equal(row.evidence_status, 'UNKNOWN');
    assert.equal(decisionColor(row), '#6b7280');
  });
}

test('invalid numeric values never become fake confidence or turn numbers', () => {
  const row = normalizeOrchestrateResponse({ decision: 'PASS', turn: -1, effective_confidence: NaN });
  assert.equal(row.turn, null);
  assert.equal(row.effective_confidence, null);
  assert.equal(decisionColor(row), '#b45309');
});

test('presentation input can be normalized twice without losing evidence status', () => {
  const x = normalizeOrchestrateResponse({ decision: 'KILL', evidence: { status: 'BLOCKED' }, turn: 13 });
  assert.deepEqual(normalizeOrchestrateResponse(x), x);
});

test('legacy JSX avoids fields absent in the current endpoint', () => {
  for (const name of ['OrchestratePanel.jsx', 'TurnTable.jsx', 'PhiTrajectory.jsx']) {
    const text = readFileSync(join(root, 'dashboard', 'components', name), 'utf8');
    assert.doesNotMatch(text, /dgaf_decision|kappa_category|apogee_grade|gold_star|seal_hash|phi_decision/);
    assert.match(text, /normalizeOrchestrateResponse/);
  }
});

test('HTTP error with contradictory PASS body never becomes a green acceptance', () => {
  const row = normalizeOrchestrateResponse(
    { decision: 'PASS', evidence: { status: 'PASS' } }, false
  );
  assert.equal(row.decision, 'UNKNOWN');
  assert.match(row.reason, /Conflicting PASS/);
  assert.equal(decisionColor(row), '#6b7280');
});

test('BLOCKED evidence prevents green even with PASS decision', () => {
  assert.equal(decisionColor({ decision: 'PASS', evidence: { status: 'BLOCKED' } }), '#b91c1c');
});
