import assert from 'node:assert/strict'
import { createHmac } from 'node:crypto'
import test from 'node:test'

import { canonicalActionDigest, validateAuditAdmission } from './action-admission.ts'

const TEST_KEY = 'dgaf-aar-mutation-regression-key'
process.env.DGAF_AAR_HMAC_KEY = TEST_KEY

function canonicalize(value: unknown): unknown {
  if (Array.isArray(value)) return value.map(canonicalize)
  if (value && typeof value === 'object') {
    return Object.fromEntries(
      Object.entries(value as Record<string, unknown>)
        .sort(([a], [b]) => a.localeCompare(b))
        .map(([key, item]) => [key, canonicalize(item)]),
    )
  }
  return value
}

function attest(record: Record<string, unknown>): string {
  return createHmac('sha256', TEST_KEY).update(JSON.stringify(canonicalize(record))).digest('hex')
}

function validRecord(parameters: Record<string, unknown>, recordId: string): Record<string, unknown> {
  const unsigned = {
    version: 'AAR_V1',
    record_id: recordId,
    action_class: 'AUDIT_COUNTER_UPDATE_V1',
    target: '/api/audit',
    policy_id: 'AAR_AUDIT_POLICY_V1',
    action_digest: canonicalActionDigest(parameters, 'auth-mutation-1'),
    authorization: {
      authorization_id: 'auth-mutation-1',
      parent_scope: ['audit:counter:update'],
      delegated_scope: ['audit:counter:update'],
      expires_at: '2099-01-01T00:00:00.000Z',
      revoked: false,
    },
    predicates: { verifier_status: 'PASS' },
  }
  return { ...unsigned, attestation: attest(unsigned) }
}

function request(record: Record<string, unknown>, parameters = { turn_count: 1 }) {
  return { ...parameters, aar: record }
}

test('registered policy, target, and action-class substitutions are denied', () => {
  const parameters = { turn_count: 1 }

  for (const [field, value] of [
    ['policy_id', 'AAR_OTHER_POLICY_V1'],
    ['target', '/api/other'],
    ['action_class', 'OTHER_ACTION_V1'],
  ] as const) {
    const record = validRecord(parameters, `aar-identity-${field}`)
    record[field] = value
    const result = validateAuditAdmission(request(record, parameters))
    assert.equal(result.ok, false)
  }
})

test('post-attestation mutation of consequential authorization and verifier fields is denied', () => {
  const parameters = { turn_count: 1 }

  const mutations: Array<(record: Record<string, unknown>) => void> = [
    (record) => {
      ;(record.authorization as Record<string, unknown>).revoked = true
    },
    (record) => {
      ;(record.authorization as Record<string, unknown>).expires_at = '2000-01-01T00:00:00.000Z'
    },
    (record) => {
      ;(record.authorization as Record<string, unknown>).delegated_scope = []
    },
    (record) => {
      ;(record.predicates as Record<string, unknown>).verifier_status = 'UNKNOWN'
    },
  ]

  mutations.forEach((mutate, index) => {
    const record = validRecord(parameters, `aar-mutated-${index}`)
    mutate(record)
    const result = validateAuditAdmission(request(record, parameters))
    assert.deepEqual(result, { ok: false, reason: 'AAR_ATTESTATION_INVALID' })
  })
})

test('trusted authorization-id substitution with a stale action digest is denied', () => {
  const parameters = { turn_count: 1 }
  const record = validRecord(parameters, 'aar-auth-id-substitution')
  const unsigned = { ...record }
  delete unsigned.attestation
  ;(unsigned.authorization as Record<string, unknown>).authorization_id = 'auth-mutation-2'
  record.authorization = unsigned.authorization
  record.attestation = attest(unsigned)

  const result = validateAuditAdmission(request(record, parameters))
  assert.deepEqual(result, { ok: false, reason: 'ACTION_DIGEST_MISMATCH' })
})
