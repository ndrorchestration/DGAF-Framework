import assert from 'node:assert/strict'
import test from 'node:test'

import { createPostgresReplayAuthority, effectIdentityKey } from './replay-authority.ts'

const EFFECT = {
  version: 'AAR_V1',
  action_class: 'AUDIT_COUNTER_UPDATE_V1',
  target: '/api/audit',
  policy_id: 'AAR_AUDIT_POLICY_V1',
  authorization_id: 'auth-replay-pg-1',
  action_digest: 'b'.repeat(64),
} as const

test('PostgreSQL-shaped adapter uses one primary-writer insert-on-conflict consume operation', async () => {
  const calls: Array<{ sql: string; params: readonly unknown[] }> = []
  const authority = createPostgresReplayAuthority({
    execute: async (sql, params) => {
      calls.push({ sql, params })
      return { rowCount: 1, rows: [{ effect_key: effectIdentityKey(EFFECT) }] }
    },
  })

  assert.equal(await authority.consumeOnce(EFFECT), 'CONSUMED')
  assert.equal(calls.length, 1)
  assert.match(calls[0].sql, /INSERT\s+INTO/i)
  assert.match(calls[0].sql, /ON\s+CONFLICT\s*\([^)]*effect_key[^)]*\)\s+DO\s+NOTHING/i)
  assert.match(calls[0].sql, /RETURNING\s+effect_key/i)
  assert.deepEqual(calls[0].params, [effectIdentityKey(EFFECT)])
  assert.doesNotMatch(calls[0].sql, /SELECT/i)
})

test('PostgreSQL unique-conflict outcome maps to REPLAY', async () => {
  const authority = createPostgresReplayAuthority({
    execute: async () => ({ rowCount: 0, rows: [] }),
  })

  assert.equal(await authority.consumeOnce(EFFECT), 'REPLAY')
})

test('PostgreSQL connection failure maps to UNAVAILABLE', async () => {
  const authority = createPostgresReplayAuthority({
    execute: async () => {
      throw Object.assign(new Error('connection unavailable'), { code: '08006' })
    },
  })

  assert.equal(await authority.consumeOnce(EFFECT), 'UNAVAILABLE')
})

test('PostgreSQL ambiguous commit outcome maps to CONFLICTED', async () => {
  const authority = createPostgresReplayAuthority({
    execute: async () => {
      throw Object.assign(new Error('connection lost after write may have committed'), {
        code: 'DGAF_AMBIGUOUS_COMMIT',
      })
    },
  })

  assert.equal(await authority.consumeOnce(EFFECT), 'CONFLICTED')
})

test('PostgreSQL unexpected result shape fails closed as CONFLICTED', async () => {
  const authority = createPostgresReplayAuthority({
    execute: async () => ({ rowCount: 2, rows: [{ effect_key: 'x' }, { effect_key: 'y' }] }),
  })

  assert.equal(await authority.consumeOnce(EFFECT), 'CONFLICTED')
})
