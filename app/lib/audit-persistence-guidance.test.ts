import assert from 'node:assert/strict'
import test from 'node:test'

import { COLD_START_WARNING } from '../../pages/api/audit.ts'

test('audit persistence guidance requires an admitted durable store without preselecting a provider', () => {
  assert.equal(COLD_START_WARNING.includes('Vercel KV'), false)
  assert.equal(COLD_START_WARNING.includes('admitted durable store'), true)
})
