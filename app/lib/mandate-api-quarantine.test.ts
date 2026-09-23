import assert from 'node:assert/strict'
import test from 'node:test'

import handler from '../../pages/api/mandate.ts'

type ResponseSnapshot = {
  statusCode?: number
  body?: unknown
}

function invoke(method: string, body?: unknown): ResponseSnapshot {
  const snapshot: ResponseSnapshot = {}
  const req = { method, body }
  const res = {
    status(code: number) {
      snapshot.statusCode = code
      return this
    },
    json(payload: unknown) {
      snapshot.body = payload
      return this
    },
  }

  handler(req as never, res as never)
  return snapshot
}

for (const [method, body] of [
  ['GET', undefined],
  ['POST', { issued_by: 'amethyst' }],
  ['PATCH', { status: 'signed_off' }],
  ['DELETE', undefined],
] as const) {
  test(`legacy mandate API fails closed for ${method}`, () => {
    const result = invoke(method, body)
    assert.equal(result.statusCode, 410)
    assert.deepEqual(result.body, {
      error: 'NON_AUTHORITATIVE_LEGACY_SURFACE',
      authority: 'NONE',
      state_change: 'DISABLED',
      guidance: 'Use reviewed PPTL governance paths; this endpoint cannot issue, mutate, or sign off mandates.',
    })
  })
}
