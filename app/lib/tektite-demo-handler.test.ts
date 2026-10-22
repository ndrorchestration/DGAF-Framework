import assert from 'node:assert/strict'
import test from 'node:test'

import handler from '../../pages/api/tektite-demo.ts'

type MockResponse = {
  statusCode: number
  body: unknown
  setHeader: () => void
  status: (code: number) => MockResponse
  json: (value: unknown) => MockResponse
}

function response(): MockResponse {
  return {
    statusCode: 0,
    body: undefined,
    setHeader() {},
    status(code: number) {
      this.statusCode = code
      return this
    },
    json(value: unknown) {
      this.body = value
      return this
    },
  }
}

test('disabled Tektite demo fails closed without attempting a network request', async () => {
  const previousEnabled = process.env.TEKTITE_DEMO_ENABLED
  const previousFetch = globalThis.fetch
  delete process.env.TEKTITE_DEMO_ENABLED

  let fetchCalls = 0
  globalThis.fetch = (async () => {
    fetchCalls += 1
    throw new Error('fetch must not run while demo is disabled')
  }) as typeof fetch

  const res = response()
  try {
    await handler({ method: 'POST', headers: {}, body: { scenario: 'authorized' } } as never, res as never)
    assert.equal(res.statusCode, 503)
    assert.deepEqual(res.body, {
      status: 'blocked',
      reason: 'TEKTITE_DEMO_NOT_ENABLED',
      boundary: 'FAIL_CLOSED_DEMO_DISABLED',
    })
    assert.equal(fetchCalls, 0)
  } finally {
    globalThis.fetch = previousFetch
    if (previousEnabled === undefined) delete process.env.TEKTITE_DEMO_ENABLED
    else process.env.TEKTITE_DEMO_ENABLED = previousEnabled
  }
})

test('enabled Tektite demo without its internal token fails closed before network access', async () => {
  const previousEnabled = process.env.TEKTITE_DEMO_ENABLED
  const previousToken = process.env.TEKTITE_DEMO_INTERNAL_TOKEN
  const previousFetch = globalThis.fetch
  process.env.TEKTITE_DEMO_ENABLED = 'true'
  delete process.env.TEKTITE_DEMO_INTERNAL_TOKEN

  let fetchCalls = 0
  globalThis.fetch = (async () => {
    fetchCalls += 1
    throw new Error('fetch must not run without the internal token')
  }) as typeof fetch

  const res = response()
  try {
    await handler({ method: 'POST', headers: {}, body: { scenario: 'authorized' } } as never, res as never)
    assert.equal(res.statusCode, 503)
    assert.deepEqual(res.body, {
      status: 'blocked',
      reason: 'TEKTITE_DEMO_INTERNAL_TOKEN_UNAVAILABLE',
      boundary: 'FAIL_CLOSED_NO_DEMO_ISSUANCE',
    })
    assert.equal(fetchCalls, 0)
  } finally {
    globalThis.fetch = previousFetch
    if (previousEnabled === undefined) delete process.env.TEKTITE_DEMO_ENABLED
    else process.env.TEKTITE_DEMO_ENABLED = previousEnabled
    if (previousToken === undefined) delete process.env.TEKTITE_DEMO_INTERNAL_TOKEN
    else process.env.TEKTITE_DEMO_INTERNAL_TOKEN = previousToken
  }
})

test('hostile forwarded headers cannot redirect the credentialed audit request', async () => {
  const previous = {
    enabled: process.env.TEKTITE_DEMO_ENABLED,
    token: process.env.TEKTITE_DEMO_INTERNAL_TOKEN,
    key: process.env.TEKTITE_DEMO_AAR_HMAC_KEY,
    origin: process.env.TEKTITE_DEMO_AUDIT_ORIGIN,
    fetch: globalThis.fetch,
  }

  process.env.TEKTITE_DEMO_ENABLED = 'true'
  process.env.TEKTITE_DEMO_INTERNAL_TOKEN = 'test-internal-token'
  process.env.TEKTITE_DEMO_AAR_HMAC_KEY = 'test-aar-key'
  process.env.TEKTITE_DEMO_AUDIT_ORIGIN = 'https://trusted.example'

  let requestedUrl = ''
  let requestedRedirect: RequestRedirect | undefined
  let requestedHeaders: Record<string, string> = {}
  globalThis.fetch = (async (input, init) => {
    requestedUrl = String(input)
    requestedRedirect = init?.redirect
    requestedHeaders = Object.fromEntries(new Headers(init?.headers).entries())
    return new Response(JSON.stringify({ status: 'ok' }), {
      status: 200,
      headers: { 'content-type': 'application/json' },
    })
  }) as typeof fetch

  let statusCode = 0
  let body: unknown
  const req = {
    method: 'POST',
    headers: {
      host: 'attacker.example',
      'x-forwarded-host': 'attacker.example',
      'x-forwarded-proto': 'http',
      'x-vercel-protection-bypass': 'attacker-controlled-bypass',
    },
    body: { scenario: 'authorized' },
  }
  const res = {
    setHeader() {},
    status(code: number) {
      statusCode = code
      return this
    },
    json(value: unknown) {
      body = value
      return this
    },
  }

  try {
    await handler(req as never, res as never)
    assert.equal(statusCode, 200)
    assert.equal(requestedUrl, 'https://trusted.example/api/audit')
    assert.equal(requestedRedirect, 'error', 'credentialed callbacks must reject redirects')
    assert.equal(requestedHeaders['x-tektite-demo-token'], 'test-internal-token')
    assert.equal(requestedHeaders['x-vercel-protection-bypass'], undefined)
    assert.equal((body as { scenario?: string }).scenario, 'authorized')
  } finally {
    globalThis.fetch = previous.fetch
    for (const [key, value] of [
      ['TEKTITE_DEMO_ENABLED', previous.enabled],
      ['TEKTITE_DEMO_INTERNAL_TOKEN', previous.token],
      ['TEKTITE_DEMO_AAR_HMAC_KEY', previous.key],
      ['TEKTITE_DEMO_AUDIT_ORIGIN', previous.origin],
    ] as const) {
      if (value === undefined) delete process.env[key]
      else process.env[key] = value
    }
  }
})


test('production excludes the Tektite demo even when generic demo enablement is true', async () => {
  const previous = {
    vercelEnv: process.env.VERCEL_ENV,
    enabled: process.env.TEKTITE_DEMO_ENABLED,
    token: process.env.TEKTITE_DEMO_INTERNAL_TOKEN,
    key: process.env.TEKTITE_DEMO_AAR_HMAC_KEY,
    fetch: globalThis.fetch,
  }

  process.env.VERCEL_ENV = 'production'
  process.env.TEKTITE_DEMO_ENABLED = 'true'
  process.env.TEKTITE_DEMO_INTERNAL_TOKEN = 'must-not-be-consumed'
  process.env.TEKTITE_DEMO_AAR_HMAC_KEY = 'must-not-be-consumed'

  let fetchCalls = 0
  globalThis.fetch = (async () => {
    fetchCalls += 1
    throw new Error('fetch must not run for production-excluded demo')
  }) as typeof fetch

  const res = response()
  try {
    await handler({ method: 'POST', headers: {}, body: { scenario: 'authorized' } } as never, res as never)
    assert.equal(res.statusCode, 404)
    assert.deepEqual(res.body, {
      status: 'not_available',
      reason: 'TEKTITE_DEMO_PRODUCTION_DISABLED',
      boundary: 'EXCLUDED_FROM_PRODUCTION',
    })
    assert.equal(fetchCalls, 0)
  } finally {
    globalThis.fetch = previous.fetch
    for (const [key, value] of [
      ['VERCEL_ENV', previous.vercelEnv],
      ['TEKTITE_DEMO_ENABLED', previous.enabled],
      ['TEKTITE_DEMO_INTERNAL_TOKEN', previous.token],
      ['TEKTITE_DEMO_AAR_HMAC_KEY', previous.key],
    ] as const) {
      if (value === undefined) delete process.env[key]
      else process.env[key] = value
    }
  }
})
