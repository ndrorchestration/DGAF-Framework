import assert from 'node:assert/strict'
import test from 'node:test'

import { trustedTektiteAuditOrigin } from './tektite-demo-origin.ts'

test('accepts a fixed HTTPS origin from trusted server configuration', () => {
  assert.equal(trustedTektiteAuditOrigin('https://example.test'), 'https://example.test')
})

test('fails closed when the trusted audit origin is absent', () => {
  assert.throws(() => trustedTektiteAuditOrigin(undefined), /TEKTITE_DEMO_AUDIT_ORIGIN_UNAVAILABLE/)
})

test('rejects non-HTTPS and credential-bearing origins', () => {
  assert.throws(() => trustedTektiteAuditOrigin('http://example.test'), /HTTPS_REQUIRED/)
  assert.throws(() => trustedTektiteAuditOrigin('https://user:pass@example.test'), /CREDENTIALS_FORBIDDEN/)
})

test('rejects path, query, fragment, and malformed origin values', () => {
  for (const value of [
    'https://example.test/api',
    'https://example.test/?target=attacker',
    'https://example.test/#fragment',
    'not-a-url',
  ]) {
    assert.throws(() => trustedTektiteAuditOrigin(value))
  }
})
