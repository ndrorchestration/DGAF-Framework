import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import test from 'node:test'

import { DECISION_FRONTIER } from './decision-frontier.ts'

test('decision frontier derives the current boundary from canonical governance stages', () => {
  assert.equal(DECISION_FRONTIER.current.label, 'Primary-analysis authorization')
  assert.equal(DECISION_FRONTIER.current.state, 'pass')
  assert.equal(DECISION_FRONTIER.blocking.label, 'Locked primary analysis')
  assert.equal(DECISION_FRONTIER.blocking.state, 'open')
  assert.equal(DECISION_FRONTIER.nearest.label, 'Locked primary analysis')
  assert.equal(DECISION_FRONTIER.nearest.reachable, true)
})

test('decision frontier has no invented downstream stage after the current locked-analysis frontier', () => {
  assert.equal(DECISION_FRONTIER.downstream.length, 0)
})

test('decision frontier preserves evidence and consequence text without readiness scoring', () => {
  assert.match(DECISION_FRONTIER.why, /authorization is ESTABLISHED/)
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
