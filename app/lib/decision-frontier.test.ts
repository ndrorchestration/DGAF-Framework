import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import test from 'node:test'

import { DECISION_FRONTIER } from './decision-frontier.ts'

test('decision frontier derives the current boundary from canonical governance stages', () => {
  assert.equal(DECISION_FRONTIER.current.label, 'Separate unblinding decision')
  assert.equal(DECISION_FRONTIER.current.state, 'pass')
  assert.equal(DECISION_FRONTIER.blocking.label, 'Controlled materialization + immutable receipt')
  assert.equal(DECISION_FRONTIER.blocking.state, 'not_established')
  assert.equal(DECISION_FRONTIER.nearest.label, 'Controlled materialization + immutable receipt')
  assert.equal(DECISION_FRONTIER.nearest.reachable, true)
})

test('decision frontier keeps downstream unauthorized transitions unreachable', () => {
  const analysisAuthorization = DECISION_FRONTIER.downstream.find(
    transition => transition.id === 'primary-analysis-authorization',
  )
  const lockedAnalysis = DECISION_FRONTIER.downstream.find(
    transition => transition.id === 'locked-analysis',
  )

  assert.ok(analysisAuthorization)
  assert.equal(analysisAuthorization.state, 'not_authorized')
  assert.equal(analysisAuthorization.reachable, false)
  assert.ok(lockedAnalysis)
  assert.equal(lockedAnalysis.state, 'not_authorized')
  assert.equal(lockedAnalysis.reachable, false)
})

test('decision frontier preserves evidence and consequence text without readiness scoring', () => {
  assert.match(DECISION_FRONTIER.why, /Bounded unblinding is authorized/)
  assert.match(DECISION_FRONTIER.consequence, /Primary-analysis authority/)
  assert.equal('readinessPercent' in DECISION_FRONTIER, false)
  assert.equal('score' in DECISION_FRONTIER, false)
})

test('control room exposes one Decision Frontier instead of a competing legacy handoff', () => {
  const source = readFileSync('app/components/control-room-view.tsx', 'utf8')

  assert.match(source, /<DecisionFrontier \/>/)
  assert.doesNotMatch(source, /NEXT_TRANSITION/)
  assert.doesNotMatch(source, /className="next-transition panel"/)
})
