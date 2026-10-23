import assert from 'node:assert/strict'
import test from 'node:test'

import handler from '../../pages/api/tektite-demo.ts'

type Denial = { status?: string; reason?: string; boundary?: string }

for (const scenario of [
  {
    name: 'disabled demo',
    enabled: undefined,
    token: 'synthetic-internal-token',
    reason: 'TEKTITE_DEMO_NOT_ENABLED',
    boundary: 'FAIL_CLOSED_DEMO_DISABLED',
  },
  {
    name: 'missing internal token',
    enabled: 'true',
    token: undefined,
    reason: 'TEKTITE_DEMO_INTERNAL_TOKEN_UNAVAILABLE',
    boundary: 'FAIL_CLOSED_NO_DEMO_ISSUANCE',
  },
] as const) {
  test(`Tektite ${scenario.name} denies before outbound fetch`, async () => {
    const originalEnabled = process.env.TEKTITE_DEMO_ENABLED
    const originalToken = process.env.TEKTITE_DEMO_INTERNAL_TOKEN
    const originalFetch = globalThis.fetch
    let fetchCalls = 0
    let statusCode = 0
    let responseBody: Denial = {}

    try {
      if (scenario.enabled === undefined) delete process.env.TEKTITE_DEMO_ENABLED
      else process.env.TEKTITE_DEMO_ENABLED = scenario.enabled
      if (scenario.token === undefined) delete process.env.TEKTITE_DEMO_INTERNAL_TOKEN
      else process.env.TEKTITE_DEMO_INTERNAL_TOKEN = scenario.token

      globalThis.fetch = (async () => {
        fetchCalls += 1
        throw new Error('unexpected outbound request')
      }) as typeof fetch

      const req = { method: 'POST', body: { scenario: 'authorized' } }
      const res = {
        status(code: number) {
          statusCode = code
          return this
        },
        json(value: Denial) {
          responseBody = value
          return this
        },
      }

      await handler(req as never, res as never)

      assert.equal(statusCode, 503)
      assert.equal(responseBody.status, 'blocked')
      assert.equal(responseBody.reason, scenario.reason)
      assert.equal(responseBody.boundary, scenario.boundary)
      assert.equal(fetchCalls, 0, 'denied requests must never invoke fetch')
    } finally {
      globalThis.fetch = originalFetch
      if (originalEnabled === undefined) delete process.env.TEKTITE_DEMO_ENABLED
      else process.env.TEKTITE_DEMO_ENABLED = originalEnabled
      if (originalToken === undefined) delete process.env.TEKTITE_DEMO_INTERNAL_TOKEN
      else process.env.TEKTITE_DEMO_INTERNAL_TOKEN = originalToken
    }
  })
}
