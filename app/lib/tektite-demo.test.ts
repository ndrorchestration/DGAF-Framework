import assert from 'node:assert/strict'
import test from 'node:test'

import { validateAuditAdmission } from './action-admission.ts'
import { createTektiteDemoRequest, isTektiteDemoScenario } from './tektite-demo.ts'

const KEY = 'tektite-demo-test-key'

test('demo scenarios are explicitly bounded', () => {
  assert.equal(isTektiteDemoScenario('authorized'), true)
  assert.equal(isTektiteDemoScenario('replay'), true)
  assert.equal(isTektiteDemoScenario('delete_repository'), false)
})

test('authorized demo fixture is accepted by the real AAR validator', () => {
  const demo = createTektiteDemoRequest('authorized', {
    trustKey: KEY,
    nowMs: Date.parse('2026-09-28T16:00:00Z'),
    recordId: 'tektite-test-authorized',
  })
  const result = validateAuditAdmission(demo.requestBody, Date.parse('2026-09-28T16:01:00Z'), KEY)
  assert.equal(result.ok, true)
})

test('revoked demo fixture fails closed', () => {
  const demo = createTektiteDemoRequest('revoked', {
    trustKey: KEY,
    nowMs: Date.parse('2026-09-28T16:00:00Z'),
    recordId: 'tektite-test-revoked',
  })
  const result = validateAuditAdmission(demo.requestBody, Date.parse('2026-09-28T16:01:00Z'), KEY)
  assert.deepEqual(result, { ok: false, reason: 'AUTHORIZATION_REVOKED' })
})

test('missing-scope demo fixture fails closed', () => {
  const demo = createTektiteDemoRequest('missing_scope', {
    trustKey: KEY,
    nowMs: Date.parse('2026-09-28T16:00:00Z'),
    recordId: 'tektite-test-scope',
  })
  const result = validateAuditAdmission(demo.requestBody, Date.parse('2026-09-28T16:01:00Z'), KEY)
  assert.deepEqual(result, { ok: false, reason: 'REQUIRED_SCOPE_MISSING' })
})

test('tampered action is rejected by digest binding', () => {
  const demo = createTektiteDemoRequest('tampered_action', {
    trustKey: KEY,
    nowMs: Date.parse('2026-09-28T16:00:00Z'),
    recordId: 'tektite-test-tamper',
  })
  const result = validateAuditAdmission(demo.requestBody, Date.parse('2026-09-28T16:01:00Z'), KEY)
  assert.deepEqual(result, { ok: false, reason: 'ACTION_DIGEST_MISMATCH' })
})