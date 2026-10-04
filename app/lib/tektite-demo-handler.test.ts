import assert from 'node:assert/strict'
import test from 'node:test'

import handler from '../../pages/api/tektite-demo.ts'

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
