import assert from 'node:assert/strict'
import test from 'node:test'
import { createHmac } from 'node:crypto'

import auditHandler from '../../pages/api/audit.ts'
import { canonicalActionDigest, validateAuditAdmission } from './action-admission.ts'

type AuditPayload = Record<string, unknown>

function invoke(body: unknown): { code: number; payload: AuditPayload } {
  let code = 0
  let payload: AuditPayload = {}
  const response = {
    status(statusCode: number) {
      code = statusCode
      return this
    },
    json(value: AuditPayload) {
      payload = value
      return this
    },
  }
  auditHandler({ method: 'POST', body, headers: {} } as never, response as never)
  return { code, payload }
}

function getTurnCount(): number {
  let payload: AuditPayload = {}
  const response = {
    status(_code: number) {
      return this
    },
    json(value: AuditPayload) {
      payload = value
      return this
    },
  }
  auditHandler({ method: 'GET', headers: {} } as never, response as never)
  const count = payload.turn_count
  assert.equal(typeof count, 'number')
  return count as number
}

test('G4 non-object POST requests deny without receipts or state mutation', () => {
  for (const body of [null, undefined, [], 'unexpected', 7, true]) {
    const before = getTurnCount()
    const result = invoke(body)
    assert.equal(result.code, 403)
    assert.equal(result.payload.status, 'denied')
    assert.equal(result.payload.reason, 'INVALID_REQUEST')
    assert.equal(Object.hasOwn(result.payload, 'execution_receipt'), false)
    assert.equal(getTurnCount(), before)
  }
})

test('G4 malformed and missing AAR deny without an execution receipt', () => {
  for (const body of [{ turn_count: 999 }, { turn_count: 999, aar: { version: 'AAR_V1' } }]) {
    const before = getTurnCount()
    const result = invoke(body)
    assert.equal(result.code, 403)
    assert.equal(result.payload.status, 'denied')
    assert.equal(result.payload.reason, 'AAR_REQUIRED_OR_MALFORMED')
    assert.equal(Object.hasOwn(result.payload, 'execution_receipt'), false)
    assert.equal(getTurnCount(), before)
  }
})

function canonicalize(value: unknown): unknown {
  if (Array.isArray(value)) return value.map(canonicalize)
  if (value !== null && typeof value === 'object') {
    return Object.fromEntries(
      Object.entries(value as Record<string, unknown>)
        .sort(([a], [b]) => a.localeCompare(b))
        .map(([key, entry]) => [key, canonicalize(entry)]),
    )
  }
  return value
}

test('G4 validator pins exact denial reasons for signed negative fixtures', () => {
  const key = 'g4-test-only-trust-key'
  const now = Date.parse('2026-10-23T12:00:00Z')
  const parameters = { turn_count: 42 }
  const digest = canonicalActionDigest(parameters, 'g4-test-auth')
  const cases = [
    { label: 'revoked', expected: 'AUTHORIZATION_REVOKED', change: { revoked: true } },
    { label: 'expired', expected: 'AUTHORIZATION_EXPIRED', change: { expires_at: '2020-01-01T00:00:00Z' } },
    { label: 'widened', expected: 'DELEGATION_WIDENED', change: { parent_scope: ['audit:read'] } },
    { label: 'missing scope', expected: 'REQUIRED_SCOPE_MISSING', change: { delegated_scope: ['audit:read'], parent_scope: ['audit:read'] } },
    { label: 'unknown verifier', expected: 'VERIFIER_NOT_PASS', change: { verifier_status: 'UNKNOWN' } },
    { label: 'mismatched digest', expected: 'ACTION_DIGEST_MISMATCH', change: { action_digest: '0'.repeat(64) } },
  ] as const

  for (const { label, expected, change } of cases) {
    const unsigned = {
      version: 'AAR_V1',
      record_id: `g4-denied-${label.replaceAll(' ', '-')}`,
      action_class: 'AUDIT_COUNTER_UPDATE_V1',
      target: '/api/audit',
      policy_id: 'AAR_AUDIT_POLICY_V1',
      action_digest: digest,
      authorization: {
        authorization_id: 'g4-test-auth',
        parent_scope: ['audit:counter:update'],
        delegated_scope: ['audit:counter:update'],
        expires_at: '2099-01-01T00:00:00Z',
        revoked: false,
      },
      predicates: { verifier_status: 'PASS' },
    }
    const changed = { ...unsigned, action_digest: 'action_digest' in change ? change.action_digest : digest,
      authorization: { ...unsigned.authorization, ...('revoked' in change ? { revoked: change.revoked } : {}),
        ...('expires_at' in change ? { expires_at: change.expires_at } : {}),
        ...('parent_scope' in change ? { parent_scope: change.parent_scope } : {}),
        ...('delegated_scope' in change ? { delegated_scope: change.delegated_scope } : {}) },
      predicates: { verifier_status: 'verifier_status' in change ? change.verifier_status : 'PASS' },
    }
    const attestation = createHmac('sha256', key)
      .update(JSON.stringify(canonicalize(changed)))
      .digest('hex')
    const result = validateAuditAdmission({ ...parameters, aar: { ...changed, attestation } }, now, key)
    assert.deepEqual(result, { ok: false, reason: expected }, label)
  }

  const unregistered = { ...parameters, unregistered_field: 1 }
  const unsigned = {
    version: 'AAR_V1',
    record_id: 'g4-denied-unregistered',
    action_class: 'AUDIT_COUNTER_UPDATE_V1',
    target: '/api/audit',
    policy_id: 'AAR_AUDIT_POLICY_V1',
    action_digest: canonicalActionDigest(unregistered, 'g4-test-auth'),
    authorization: {
      authorization_id: 'g4-test-auth',
      parent_scope: ['audit:counter:update'],
      delegated_scope: ['audit:counter:update'],
      expires_at: '2099-01-01T00:00:00Z',
      revoked: false,
    },
    predicates: { verifier_status: 'PASS' },
  }
  const attestation = createHmac('sha256', key)
    .update(JSON.stringify(canonicalize(unsigned)))
    .digest('hex')
  assert.deepEqual(validateAuditAdmission({ ...unregistered, aar: { ...unsigned, attestation } }, now, key),
    { ok: false, reason: 'ACTION_PARAMETERS_NOT_REGISTERED' })
})
