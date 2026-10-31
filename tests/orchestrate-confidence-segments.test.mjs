import test from 'node:test';
import assert from 'node:assert/strict';
import { readFileSync } from 'node:fs';
import { fileURLToPath } from 'node:url';
import { dirname, join } from 'node:path';
import { confidenceSegments, normalizeOrchestrateResponse } from '../dashboard/lib/orchestrate-presentation.mjs';

const row = effective_confidence => ({ decision: 'PASS', evidence_status: 'PARTIAL', effective_confidence });
const rendered = readFileSync(join(dirname(fileURLToPath(import.meta.url)), '..',
  'dashboard', 'components', 'PhiTrajectory.jsx'), 'utf8');

test('no confidence readings produce no connecting lines', () => {
  assert.deepEqual(confidenceSegments([]), []);
  assert.deepEqual(confidenceSegments(null), []);
  assert.deepEqual(confidenceSegments([row(null), row(undefined)]), []);
});

test('consecutive observed samples retain chronological index and valid zero', () => {
  assert.deepEqual(confidenceSegments([row(0), row(0.4), row(1)]), [[
    { index: 0, confidence: 0 },
    { index: 1, confidence: 0.4 },
    { index: 2, confidence: 1 },
  ]]);
});

test('missing middle observation splits line without invented intermediate point', () => {
  assert.deepEqual(confidenceSegments([row(0.1), row(null), row(0.9)]), [
    [{ index: 0, confidence: 0.1 }],
    [{ index: 2, confidence: 0.9 }],
  ]);
});

test('multiple missing readings keep separated contiguous spans and plot positions', () => {
  assert.deepEqual(confidenceSegments([
    row(null), row(0.2), row(0.3), row(undefined), row(0.7), row(0.8), row(null),
  ]), [
    [{ index: 1, confidence: 0.2 }, { index: 2, confidence: 0.3 }],
    [{ index: 4, confidence: 0.7 }, { index: 5, confidence: 0.8 }],
  ]);
});

test('invalid numeric readings break interpolation instead of being clamped or fabricated', () => {
  assert.deepEqual(confidenceSegments([
    row(0.1), row(Number.NaN), row(Infinity), row(-0.1), row(1.01), row('0.5'), row(0.4),
  ]), [
    [{ index: 0, confidence: 0.1 }],
    [{ index: 6, confidence: 0.4 }],
  ]);
});

test('unknown and blocked decisions do not synthesize confidence', () => {
  const values = [row(0.5), { decision: 'BLOCKED' }, { dgaf_decision: 'PASS' }, row(0.8)];
  assert.equal(normalizeOrchestrateResponse(values[2]).effective_confidence, null);
  assert.deepEqual(confidenceSegments(values), [
    [{ index: 0, confidence: 0.5 }],
    [{ index: 3, confidence: 0.8 }],
  ]);
});

test('presentation is wired to split polylines and keeps individual observed dots', () => {
  assert.match(rendered, /confidenceSegments\(data\)/);
  assert.match(rendered, /segments\.filter\(segment => segment\.length > 1\)\.map/);
  assert.match(rendered, /observed\.map\(\(\{ t, i \}\)/);
  assert.doesNotMatch(rendered, /<polyline points=\{points\}/);
});


test('confidence chart exposes accessible semantics and a responsive viewBox', () => {
  assert.match(rendered, /role="img"/);
  assert.match(rendered, /aria-label="Observed confidence across turns/);
  assert.match(rendered, /viewBox=\{\x60/);
  assert.match(rendered, /width="100%"/);
  assert.match(rendered, /<title>Observed effective confidence/);
});
