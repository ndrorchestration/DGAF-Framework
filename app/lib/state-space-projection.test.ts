import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import test from 'node:test'

import { STATE_SPACE_DIMENSIONS, STATE_SPACE_PROJECTION } from './state-space-projection.ts'
import { GOVERNANCE_STAGES } from './governance.ts'

test('state-space projection derives its ordered regions from canonical governance stages', () => {
  assert.deepEqual(
    STATE_SPACE_PROJECTION.regions.map(region => region.id),
    GOVERNANCE_STAGES.map(stage => stage.id),
  )

  assert.equal(STATE_SPACE_PROJECTION.frontierId, 'locked-analysis')

  const frontierIndex = GOVERNANCE_STAGES.findIndex(stage => stage.id === 'locked-analysis')
  assert.ok(frontierIndex > 0)

  for (const region of STATE_SPACE_PROJECTION.regions.slice(0, frontierIndex)) {
    assert.equal(region.reachability, 'established')
    assert.equal(region.nativeState, 'pass')
  }
})

test('state-space projection keeps derived reachability separate from native predicate state', () => {
  const materialization = STATE_SPACE_PROJECTION.regions.find(region => region.id === 'materialization')
  const analysisAuthorization = STATE_SPACE_PROJECTION.regions.find(
    region => region.id === 'primary-analysis-authorization',
  )
  const lockedAnalysis = STATE_SPACE_PROJECTION.regions.find(region => region.id === 'locked-analysis')

  assert.ok(materialization)
  assert.ok(analysisAuthorization)
  assert.ok(lockedAnalysis)

  assert.equal(materialization.reachability, 'established')
  assert.equal(materialization.nativeState, 'pass')

  assert.equal(analysisAuthorization.reachability, 'established')
  assert.equal(analysisAuthorization.nativeState, 'pass')

  assert.equal(lockedAnalysis.reachability, 'frontier')
  assert.equal(lockedAnalysis.nativeState, 'open')
})

test('state-space projection preserves global fail-closed constraints without scalar readiness', () => {
  assert.equal(STATE_SPACE_PROJECTION.constraints.programState, 'PRE-FREEZE')
  assert.equal(STATE_SPACE_PROJECTION.constraints.failMode, 'FAIL-CLOSED')
  assert.equal(STATE_SPACE_PROJECTION.constraints.authorization, 'NOT AUTHORIZED')
  assert.equal(STATE_SPACE_PROJECTION.constraints.empiricalN, 0)

  const forbiddenFields = [
    'readinessPercent',
    'score',
    'probability',
    'distanceToAuthorization',
    'continuousCoordinate',
  ]

  for (const field of forbiddenFields) {
    assert.equal(field in STATE_SPACE_PROJECTION, false)
  }
})

test('state-space dimensions expose modeling limits rather than invented coordinates', () => {
  const byId = new Map(STATE_SPACE_DIMENSIONS.map(dimension => [dimension.id, dimension]))

  assert.equal(byId.get('reachability')?.representation, 'projectable')
  assert.equal(byId.get('native-state')?.representation, 'projectable')
  assert.equal(byId.get('evidence-boundary')?.representation, 'projectable')
  assert.equal(byId.get('provenance')?.representation, 'bounded')
  assert.equal(byId.get('verification')?.representation, 'bounded')
  assert.equal(byId.get('authorization')?.representation, 'bounded')
  assert.equal(byId.get('uncertainty')?.representation, 'bounded')
  assert.equal(byId.get('consequence')?.representation, 'not_modeled')
  assert.equal(byId.get('reversibility')?.representation, 'not_modeled')

  for (const dimension of STATE_SPACE_DIMENSIONS) {
    assert.equal('value' in dimension, false)
    assert.equal('coordinate' in dimension, false)
    assert.equal('score' in dimension, false)
  }
})

test('State Space view makes the discrete representation boundary explicit without color-only semantics', () => {
  const source = readFileSync('app/components/state-space-view.tsx', 'utf8')

  assert.match(source, /DISCRETE REACHABILITY/)
  assert.match(source, /NO CONTINUOUS INTERPOLATION/)
  assert.match(source, /CURRENT FRONTIER/)
  assert.match(source, /BLOCKED BY PREDECESSOR/)
  assert.match(source, /NOT MODELED — DO NOT INFER/)
  assert.doesNotMatch(source, /readinessPercent|distanceToAuthorization|probability|continuousCoordinate/)
  assert.doesNotMatch(source, /const\s+GOVERNANCE_STAGES\s*=/)
})

test('State Space stylesheet remains contained to the expert surface', () => {
  const css = readFileSync('app/styles/state-space.css', 'utf8')

  assert.doesNotMatch(css, /^\.section-heading\s*\{/m)
  assert.match(css, /\.state-space-view \.section-heading\s*\{/)
})

test('State Space is a separate expert view routed through the shared projection', () => {
  const shell = readFileSync('app/components/app-shell.tsx', 'utf8')
  const page = readFileSync('app/page.tsx', 'utf8')

  assert.match(shell, /'state-space'/)
  assert.match(shell, /State Space/)
  assert.match(shell, /Reachability model/)
  assert.match(page, /StateSpaceView/)
  assert.match(page, /case 'state-space'/)
  assert.doesNotMatch(page, /const\s+GOVERNANCE_STAGES\s*=/)
})
