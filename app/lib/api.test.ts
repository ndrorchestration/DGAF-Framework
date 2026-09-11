import test from 'node:test'
import assert from 'node:assert/strict'
import {
  validateAuditData,
  validateHealthData,
  validateRosterData,
  validateSweepResult,
} from './api.ts'

const validHealth = {
  status: 'ok',
  version: '1.8.0',
  psi_cubic: true,
  psi: 1.4655712318767682,
  phi_star: 0.6180339887498949,
  runtime: 'nodejs',
  scpe_threshold: 0.15,
  phi_checkpoints: [13, 21, 34, 55],
  adapters: ['openai'],
}

const validAudit = {
  status: 'ok',
  version: '1.8.0',
  turn_count: 0,
  stable_turns: 0,
  prune_events: 0,
  axiom_count: 0,
  consec_phi_fail: 0,
  cold_start: true,
  cold_start_at: '2026-09-11T06:00:00.000Z',
  _warning: 'In-memory counters reset on serverless cold starts.',
}

const validRoster = {
  version: '1.8.0',
  agent_count: 1,
  triad_count: 1,
  ndr_patterns: 7,
  agents: [{ id: 'amethyst', tier: 'L5', role: 'orchestrator', status: 'active', triad_roles: ['conductor'] }],
  triads: [{ id: 'T-01', type: 'conducted', agents: ['amethyst'], use_case: 'governance' }],
  phi_star: 0.6180339887498949,
  psi: 1.4655712318767682,
}

const validSweep = {
  sweep_id: 'ABC123',
  targets_scanned: 1,
  findings_count: 0,
  findings: [],
  narrative: 'Sweep complete.',
  harmonic_score: null,
  harmonic_score_status: 'NOT_COMPUTED',
  mutation_performed: false,
  swept_at: '2026-09-11T06:00:00.000Z',
}

test('accepts structurally valid dashboard payloads', () => {
  assert.equal(validateHealthData(validHealth).version, '1.8.0')
  assert.equal(validateAuditData(validAudit).cold_start, true)
  assert.equal(validateRosterData(validRoster).agents[0].id, 'amethyst')
})

test('rejects malformed health, audit, and roster payloads', () => {
  assert.throws(() => validateHealthData({ ...validHealth, adapters: 'openai' }), /health/i)
  assert.throws(() => validateAuditData({ ...validAudit, turn_count: '0' }), /audit/i)
  assert.throws(() => validateRosterData({ ...validRoster, agents: {} }), /roster/i)
})

test('accepts a non-computed harmonic score without inventing a number', () => {
  const sweep = validateSweepResult(validSweep)
  assert.equal(sweep.harmonic_score, null)
  assert.equal(sweep.harmonic_score_status, 'NOT_COMPUTED')
  assert.equal(sweep.mutation_performed, false)
})

test('rejects malformed sweep success payloads', () => {
  assert.throws(() => validateSweepResult({ ...validSweep, findings_count: '0' }), /sweep/i)
  assert.throws(() => validateSweepResult({ ...validSweep, harmonic_score: '0.9' }), /sweep/i)
})
