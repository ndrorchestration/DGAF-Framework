import assert from 'node:assert/strict'
import { createHash } from 'node:crypto'
import test from 'node:test'

import auditHandler from '../../pages/api/audit.ts'

type MockRequest = {
  method: string
  body?: Record<string, unknown>
}

type MockResponse = {
  statusCode: number
  payload: Record<string, unknown> | null
  status: (code: number) => MockResponse
  json: (payload: Record<string, unknown>) => MockResponse
}

type AarOverrides = {
  record_id?: string
  parent_scope?: string[]
  delegated_scope?: string[]
  expires_at?: string
  revoked?: boolean
  action_digest?: string
  verifier_status?: 'PASS' | 'UNKNOWN' | 'FAIL'
}

let recordCounter = 0

function response(): MockResponse {
  return {
    statusCode: 200,
    payload: null,
    status(code: number) {
      this.statusCode = code
      return this
    },
    json(payload: Record<string, unknown>) {
      this.payload = payload
      return this
    },
  }
}

function invoke(method: string, body?: Record<string, unknown>): MockResponse {
  const res = response()
  auditHandler({ method, body } as never, res as never)
  return res
}

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

function actionDigest(parameters: Record<string, unknown>, authorizationId = 'auth-test-1'): string {
  const payload = canonicalize({
    action_class: 'AUDIT_COUNTER_UPDATE_V1',
    authorization_id: authorizationId,
    parameters,
    policy_id: 'AAR_AUDIT_POLICY_V1',
    target: '/api/audit',
  })
  return createHash('sha256').update(JSON.stringify(payload)).digest('hex')
}

function aar(parameters: Record<string, unknown>, overrides: AarOverrides = {}): Record<string, unknown> {
  recordCounter += 1
  return {
    version: 'AAR_V1',
    record_id: overrides.record_id ?? `aar-test-${recordCounter}`,
    action_class: 'AUDIT_COUNTER_UPDATE_V1',
    target: '/api/audit',
    policy_id: 'AAR_AUDIT_POLICY_V1',
    action_digest: overrides.action_digest ?? actionDigest(parameters),
    authorization: {
      authorization_id: 'auth-test-1',
      parent_scope: overrides.parent_scope ?? ['audit:counter:update'],
      delegated_scope: overrides.delegated_scope ?? ['audit:counter:update'],
      expires_at: overrides.expires_at ?? '2099-01-01T00:00:00.000Z',
      revoked: overrides.revoked ?? false,
    },
    predicates: {
      verifier_status: overrides.verifier_status ?? 'PASS',
    },
  }
}

function turnCount(): number {
  const current = invoke('GET')
  assert.equal(current.statusCode, 200)
  assert.ok(current.payload)
  assert.equal(typeof current.payload.turn_count, 'number')
  return current.payload.turn_count as number
}

function assertDeniedWithoutMutation(body: Record<string, unknown>): MockResponse {
  const before = turnCount()
  const denied = invoke('POST', body)
  assert.equal(denied.statusCode, 403)
  assert.equal(denied.payload?.status, 'denied')
  assert.equal(turnCount(), before)
  return denied
}

test('POST /api/audit fails closed without an Action Admission Record and does not mutate state', () => {
  const before = turnCount()
  assertDeniedWithoutMutation({ turn_count: before + 1 })
})

test('POST /api/audit rejects malformed Action Admission Records', () => {
  const before = turnCount()
  assertDeniedWithoutMutation({ turn_count: before + 1, aar: { version: 'AAR_V1' } })
})

test('POST /api/audit rejects widened delegated authority', () => {
  const before = turnCount()
  const parameters = { turn_count: before + 1 }
  assertDeniedWithoutMutation({
    ...parameters,
    aar: aar(parameters, { parent_scope: ['audit:read'], delegated_scope: ['audit:read', 'audit:counter:update'] }),
  })
})

test('POST /api/audit rejects revoked and expired authorization', () => {
  const before = turnCount()
  const parameters = { turn_count: before + 1 }
  assertDeniedWithoutMutation({ ...parameters, aar: aar(parameters, { revoked: true }) })
  assertDeniedWithoutMutation({ ...parameters, aar: aar(parameters, { expires_at: '2020-01-01T00:00:00.000Z' }) })
})

test('POST /api/audit rejects action-digest substitution and UNKNOWN verifier state', () => {
  const before = turnCount()
  const parameters = { turn_count: before + 1 }
  assertDeniedWithoutMutation({ ...parameters, aar: aar(parameters, { action_digest: '0'.repeat(64) }) })
  assertDeniedWithoutMutation({ ...parameters, aar: aar(parameters, { verifier_status: 'UNKNOWN' }) })
})

test('POST /api/audit rejects fields outside the registered action parameter set', () => {
  const before = turnCount()
  const parameters = { turn_count: before + 1, unregistered_field: 1 }
  assertDeniedWithoutMutation({ ...parameters, aar: aar(parameters) })
})

test('POST /api/audit accepts an exact bound AAR once, emits a receipt, and rejects replay', () => {
  const before = turnCount()
  const parameters = { turn_count: before + 1 }
  const record = aar(parameters, { record_id: `aar-success-${before + 1}` })

  const accepted = invoke('POST', { ...parameters, aar: record })
  assert.equal(accepted.statusCode, 200)
  assert.equal(accepted.payload?.status, 'updated')
  assert.equal(accepted.payload?.turn_count, before + 1)
  assert.equal(typeof accepted.payload?.execution_receipt, 'object')
  assert.equal((accepted.payload?.execution_receipt as Record<string, unknown>)?.record_id, record.record_id)
  assert.equal((accepted.payload?.execution_receipt as Record<string, unknown>)?.action_digest, record.action_digest)

  const replay = invoke('POST', { ...parameters, aar: record })
  assert.equal(replay.statusCode, 403)
  assert.equal(replay.payload?.status, 'denied')
  assert.equal(turnCount(), before + 1)
})
