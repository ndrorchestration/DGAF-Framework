import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import path from 'node:path'
import test from 'node:test'
import { fileURLToPath } from 'node:url'

import { GOVERNANCE_STAGES, TRUTH_BOUNDARY } from './governance.ts'

const ROOT = path.resolve(path.dirname(fileURLToPath(import.meta.url)), '../..')
const OVERVIEW_SOURCE = readFileSync(path.join(ROOT, 'app/components/overview-view.tsx'), 'utf8')

test('public governance projection reflects the accepted 2026-09-19 documentation frontier', () => {
  assert.equal(TRUTH_BOUNDARY.sourceUpdated, '2026-09-19')

  const analysisAuthorization = GOVERNANCE_STAGES.find(
    stage => stage.id === 'primary-analysis-authorization',
  )
  assert.equal(analysisAuthorization?.predicateState, 'pass')
  assert.equal(analysisAuthorization?.toolingPrepared, true)
  assert.match(analysisAuthorization?.toolingNote ?? '', /#828/)

  const lockedAnalysis = GOVERNANCE_STAGES.find(stage => stage.id === 'locked-analysis')
  const interpretation = GOVERNANCE_STAGES.find(stage => stage.id === 'interpretation-adjudication')
  assert.equal(lockedAnalysis?.predicateState, 'pass')
  assert.equal(lockedAnalysis?.toolingPrepared, true)
  assert.equal(interpretation?.predicateState, 'pass')
  assert.equal(interpretation?.toolingPrepared, true)
  assert.match(interpretation?.toolingNote ?? '', /#872/)
})

test('overview truth-boundary copy reflects the accepted interpretation state', () => {
  assert.match(OVERVIEW_SOURCE, /local primary-analysis execution/)
  assert.match(OVERVIEW_SOURCE, /content-addressed locked-result receipt/)
  assert.match(OVERVIEW_SOURCE, /bounded interpretation note are established/)
  assert.match(OVERVIEW_SOURCE, /canonical DGAF efficacy and independent validation remain NOT ESTABLISHED/)
  assert.match(OVERVIEW_SOURCE, /High-Assurance authority remains NOT AUTHORIZED/)
})
