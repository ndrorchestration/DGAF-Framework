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

  assert.equal(STATE_SPACE_PROJECTION.frontierId, null)

  for (const region of STATE_SPACE_PROJECTION.regions) {
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
  const interpretation = STATE_SPACE_PROJECTION.regions.find(
    region => region.id === 'interpretation-adjudication',
  )
  const disposition = STATE_SPACE_PROJECTION.regions.find(
    region => region.id === 'post-interpretation-disposition',
  )

  assert.ok(materialization)
  assert.ok(analysisAuthorization)
  assert.ok(lockedAnalysis)
  assert.ok(interpretation)
  assert.ok(disposition)

  assert.equal(materialization.reachability, 'established')
  assert.equal(materialization.nativeState, 'pass')

  assert.equal(analysisAuthorization.reachability, 'established')
  assert.equal(analysisAuthorization.nativeState, 'pass')

  assert.equal(lockedAnalysis.reachability, 'established')
  assert.equal(lockedAnalysis.nativeState, 'pass')

  assert.equal(interpretation.reachability, 'established')
  assert.equal(interpretation.nativeState, 'pass')

  assert.equal(disposition.reachability, 'established')
  assert.equal(disposition.nativeState, 'pass')
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

test('State Space is a separate expert route through the shared projection', () => {
  const navigation = readFileSync('app/lib/navigation.ts', 'utf8')
  const page = readFileSync('app/(command-center)/state-space/page.tsx', 'utf8')

  assert.match(navigation, /'state-space'/)
  assert.match(navigation, /State Space/)
  assert.match(navigation, /Reachability model/)
  assert.match(navigation, /href: '\/state-space'/)
  assert.match(page, /StateSpaceView/)
  assert.doesNotMatch(page, /const\\s+GOVERNANCE_STAGES\\s*=/)
})
