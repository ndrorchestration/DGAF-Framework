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
  assert.equal(analysisAuthorization?.predicateState, 'pass')
  assert.equal(analysisAuthorization?.toolingPrepared, true)
  assert.match(analysisAuthorization?.toolingNote ?? '', /#828/)

  const lockedAnalysis = GOVERNANCE_STAGES.find(stage => stage.id === 'locked-analysis')
  assert.equal(lockedAnalysis?.predicateState, 'open')
  assert.equal(lockedAnalysis?.toolingPrepared, true)
})

test('overview truth-boundary copy reflects the accepted locked-analysis frontier', () => {
  assert.match(OVERVIEW_SOURCE, /materialization and its immutable receipt are established/)
  assert.match(OVERVIEW_SOURCE, /bounded locked-primary-analysis authorization is accepted/)
  assert.match(OVERVIEW_SOURCE, /the analysis has not run/)
  assert.match(OVERVIEW_SOURCE, /no locked result is established/)
})
