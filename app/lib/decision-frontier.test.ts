import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import test from 'node:test'

import { DECISION_FRONTIER } from './decision-frontier.ts'

test('decision frontier represents accepted Epoch 002 closure without inventing a successor lane', () => {
  assert.equal(DECISION_FRONTIER.lifecycleComplete, true)
  assert.equal(DECISION_FRONTIER.current.label, 'Epoch 002 post-interpretation disposition')
  assert.equal(DECISION_FRONTIER.current.state, 'pass')
  assert.equal(DECISION_FRONTIER.blocking, null)
  assert.equal(DECISION_FRONTIER.nearest, null)
  assert.equal(DECISION_FRONTIER.receipt.state, 'pass')
  assert.match(DECISION_FRONTIER.receipt.summary, /PR #881/)
  assert.match(DECISION_FRONTIER.receipt.summary, /CLOSED_BOUNDED_SAME_SYSTEM_NONINDEPENDENT/)
})

test('decision frontier has no invented downstream stage after accepted Epoch 002 closure', () => {
  assert.equal(DECISION_FRONTIER.downstream.length, 0)
  assert.match(DECISION_FRONTIER.transitionTitle, /no successor empirical lane designated/i)
})

test('decision frontier preserves evidence and consequence text without readiness scoring', () => {
  assert.match(DECISION_FRONTIER.why, /POST_INTERPRETATION_DISPOSITION = CLOSED_BOUNDED_SAME_SYSTEM_NONINDEPENDENT/)
  assert.match(DECISION_FRONTIER.consequence, /Canonical DGAF efficacy/)
  assert.equal('readinessPercent' in DECISION_FRONTIER, false)
  assert.equal('score' in DECISION_FRONTIER, false)
})

test('control room exposes one Decision Frontier instead of a competing legacy handoff', () => {
  const source = readFileSync('app/components/control-room-view.tsx', 'utf8')

  assert.match(source, /<DecisionFrontier \/>/)
  assert.doesNotMatch(source, /NEXT_TRANSITION/)
  assert.doesNotMatch(source, /className="next-transition panel"/)
})
