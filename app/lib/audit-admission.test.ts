import assert from 'node:assert/strict'
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

test('POST /api/audit fails closed without an Action Admission Record and does not mutate state', () => {
  const before = invoke('GET')
  assert.equal(before.statusCode, 200)
  assert.ok(before.payload)

  const originalTurnCount = before.payload.turn_count
  assert.equal(typeof originalTurnCount, 'number')

  const attemptedTurnCount = (originalTurnCount as number) + 1
  const denied = invoke('POST', { turn_count: attemptedTurnCount })

  assert.equal(denied.statusCode, 403)
  assert.equal(denied.payload?.status, 'denied')

  const after = invoke('GET')
  assert.equal(after.payload?.turn_count, originalTurnCount)
})
