import assert from 'node:assert/strict'
import test from 'node:test'

import {
  createUpstashReplayAuthority,
  effectIdentityKey,
  type ReplayAuthority,
  type ReplayAuthorityResult,
} from './replay-authority.ts'

const EFFECT = {
  version: 'AAR_V1',
  action_class: 'AUDIT_COUNTER_UPDATE_V1',
  target: '/api/audit',
  policy_id: 'AAR_AUDIT_POLICY_V1',
  authorization_id: 'auth-replay-1',
  action_digest: 'a'.repeat(64),
} as const

test('effect identity is deterministic and excludes caller-variable record id', () => {
  const first = effectIdentityKey({ ...EFFECT, record_id: 'record-a' })
  const second = effectIdentityKey({ ...EFFECT, record_id: 'record-b' })

  assert.equal(first, second)
  assert.match(first, /^aar:effect:[a-f0-9]{64}$/)
})

test('provider-neutral authority exposes only bounded consume outcomes', async () => {
  const outcomes: ReplayAuthorityResult[] = ['CONSUMED', 'REPLAY', 'UNAVAILABLE', 'CONFLICTED']
  const authority: ReplayAuthority = {
    consumeOnce: async () => outcomes.shift() ?? 'CONFLICTED',
  }

  assert.equal(await authority.consumeOnce(EFFECT), 'CONSUMED')
  assert.equal(await authority.consumeOnce(EFFECT), 'REPLAY')
  assert.equal(await authority.consumeOnce(EFFECT), 'UNAVAILABLE')
  assert.equal(await authority.consumeOnce(EFFECT), 'CONFLICTED')
})

test('Upstash-shaped adapter uses one conditional SET NX operation on effect identity', async () => {
  const calls: Array<{ key: string; value: string; nx: boolean }> = []
  const authority = createUpstashReplayAuthority({
    set: async (key, value, options) => {
      calls.push({ key, value, nx: options.nx })
      return 'OK'
    },
  })

  assert.equal(await authority.consumeOnce(EFFECT), 'CONSUMED')
  assert.deepEqual(calls, [
    {
      key: effectIdentityKey(EFFECT),
      value: 'CONSUMED',
      nx: true,
    },
  ])
})

test('conditional-set miss maps to REPLAY without a check-then-set read', async () => {
  let setCalls = 0
  const authority = createUpstashReplayAuthority({
    set: async () => {
      setCalls += 1
      return null
    },
  })

  assert.equal(await authority.consumeOnce(EFFECT), 'REPLAY')
  assert.equal(setCalls, 1)
})

test('provider error fails closed as UNAVAILABLE', async () => {
  const authority = createUpstashReplayAuthority({
    set: async () => {
      throw new Error('provider unavailable')
    },
  })

  assert.equal(await authority.consumeOnce(EFFECT), 'UNAVAILABLE')
})

test('ambiguous provider response fails closed as CONFLICTED', async () => {
  const authority = createUpstashReplayAuthority({
    set: async () => 'unexpected' as never,
  })

  assert.equal(await authority.consumeOnce(EFFECT), 'CONFLICTED')
})
