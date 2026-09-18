import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import path from 'node:path'
import test from 'node:test'
import { fileURLToPath } from 'node:url'

import { GOVERNANCE_STAGES, TRUTH_BOUNDARY } from './governance.ts'

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..')
const OVERVIEW_SOURCE = readFileSync(path.join(ROOT, 'app/components/overview-view.tsx'), 'utf8')

test('public governance projection reflects the accepted 2026-09-18 documentation frontier', () => {
  assert.equal(TRUTH_BOUNDARY.sourceUpdated, '2026-09-18')

  const analysisAuthorization = GOVERNANCE_STAGES.find(
    stage => stage.id === 'primary-analysis-authorization',
  )
  assert.equal(analysisAuthorization?.predicateState, 'not_authorized')
  assert.equal(analysisAuthorization?.toolingPrepared, true)
  assert.match(analysisAuthorization?.toolingNote ?? '', /#728/)
})

test('overview truth-boundary copy preserves established dataset-lock state', () => {
  assert.doesNotMatch(
    OVERVIEW_SOURCE,
    /completed successor collection does not establish dataset lock/,
  )
  assert.match(OVERVIEW_SOURCE, /dataset lock is established/)
})
