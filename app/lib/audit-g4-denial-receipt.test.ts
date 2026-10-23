import assert from 'node:assert/strict'
import test from 'node:test'

import auditHandler from '../../pages/api/audit.ts'

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
    assert.equal(Object.hasOwn(result.payload, 'execution_receipt'), false)
    assert.equal(getTurnCount(), before)
  }
})
