import assert from 'node:assert/strict'
import { readFileSync } from 'node:fs'
import test from 'node:test'

import { GOVERNANCE_MAP, GOVERNANCE_RELATIONSHIPS } from './governance-map.ts'
import { GOVERNANCE_STAGES } from './governance.ts'

test('governance map derives its vertical spine from canonical governance stages', () => {
  assert.deepEqual(
    GOVERNANCE_MAP.stages.map(stage => stage.id),
    GOVERNANCE_STAGES.map(stage => stage.id),
  )
  assert.equal(GOVERNANCE_MAP.blocking.id, 'locked-analysis')
  assert.equal(GOVERNANCE_MAP.blocking.state, 'open')
})

test('governance map relationships resolve only to canonical stage ids', () => {
  const stageIds = new Set(GOVERNANCE_STAGES.map(stage => stage.id))

  assert.equal(GOVERNANCE_RELATIONSHIPS.length, 4)
  for (const relationship of GOVERNANCE_RELATIONSHIPS) {
    assert.equal(stageIds.has(relationship.sourceId), true)
    assert.equal(stageIds.has(relationship.targetId), true)
    assert.ok(relationship.label.length > 0)
    assert.ok(relationship.provenance.length > 0)
    assert.ok(relationship.doesNotEstablish.length > 0)
  }
})

test('governance map preserves global field constraints without readiness scoring', () => {
  assert.equal(GOVERNANCE_MAP.constraints.programState, 'PRE-FREEZE')
  assert.equal(GOVERNANCE_MAP.constraints.failMode, 'FAIL-CLOSED')
  assert.equal(GOVERNANCE_MAP.constraints.authorization, 'NOT AUTHORIZED')
  assert.equal(GOVERNANCE_MAP.constraints.empiricalN, 0)
  assert.equal('readinessPercent' in GOVERNANCE_MAP, false)
  assert.equal('score' in GOVERNANCE_MAP, false)
})

test('governance map uses explicit non-color structural labels and keeps authorization distinct from authority', () => {
  const source = readFileSync('app/components/governance-map.tsx', 'utf8')

  assert.match(source, />AUTHORIZATION</)
  assert.doesNotMatch(source, />AUTHORITY</)
  assert.match(source, /GLOBAL FIELD CONDITIONS/)
  assert.match(source, /BLOCKING BOUNDARY/)
  assert.match(source, /LATERAL COUPLING/)
  assert.match(source, /DOES NOT ESTABLISH/)
})

test('governance view renders the structural map before the detailed lifecycle', () => {
  const source = readFileSync('app/components/governance-view.tsx', 'utf8')
  const mapIndex = source.indexOf('<GovernanceMap />')
  const lifecycleIndex = source.indexOf('className="lifecycle"')

  assert.ok(mapIndex >= 0)
  assert.ok(lifecycleIndex >= 0)
  assert.ok(mapIndex < lifecycleIndex)
  assert.doesNotMatch(source, /const\s+GOVERNANCE_STAGES\s*=/)
})
