import assert from 'node:assert/strict'
import { existsSync } from 'node:fs'
import { resolve } from 'node:path'
import test from 'node:test'

import { SWEEP_DEFAULT_TARGETS } from './tools-defaults.ts'

test('P-07 default targets resolve to existing repository paths', () => {
  assert.deepEqual(SWEEP_DEFAULT_TARGETS, [
    'pages/api/health.ts',
    'pages/api/sweep.ts',
    'requirements.txt',
  ])

  for (const target of SWEEP_DEFAULT_TARGETS) {
    assert.equal(existsSync(resolve(process.cwd(), target)), true, `missing default sweep target: ${target}`)
  }
})

test('P-07 defaults do not restore retired API locations', () => {
  assert.equal(SWEEP_DEFAULT_TARGETS.includes('api/health.py'), false)
  assert.equal(SWEEP_DEFAULT_TARGETS.includes('app/api/health/route.ts'), false)
})
