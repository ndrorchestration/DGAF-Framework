import test from 'node:test'
import assert from 'node:assert/strict'
import { GOVERNANCE_STAGES, TRUTH_BOUNDARY } from './governance.ts'
import { agentDisplayName } from './public-translation.ts'
import { STATUS_META, normalizeRuntimeStatus, statusMeta } from './status.ts'

test('loading is neutral rather than destructive', () => {
  const loading = statusMeta('loading')
  assert.equal(loading.tone, 'neutral')
  assert.notEqual(loading.label, 'Failed')
  assert.notEqual(loading.label, 'Denied')
})

test('pass and verified remain distinct evidence states', () => {
  assert.equal(STATUS_META.pass.label, 'Pass')
  assert.equal(STATUS_META.verified.label, 'Verified')
  assert.notEqual(STATUS_META.pass.label, STATUS_META.verified.label)
})

test('not authorized and not established remain distinct', () => {
  assert.equal(STATUS_META.not_authorized.label, 'Not authorized')
  assert.equal(STATUS_META.not_established.label, 'Not established')
  assert.notEqual(STATUS_META.not_authorized.description, STATUS_META.not_established.description)
})

test('unknown runtime input remains unknown', () => {
  assert.equal(normalizeRuntimeStatus('mystery'), 'unknown')
  assert.equal(normalizeRuntimeStatus(undefined), 'unknown')
})

test('runtime ok maps to pass, never verified', () => {
  assert.equal(normalizeRuntimeStatus('ok'), 'pass')
  assert.notEqual(normalizeRuntimeStatus('ok'), 'verified')
})

test('current truth boundary remains fail-closed and non-authorized', () => {
  assert.equal(TRUTH_BOUNDARY.programState, 'PRE-FREEZE')
  assert.equal(TRUTH_BOUNDARY.failMode, 'FAIL-CLOSED')
  assert.equal(TRUTH_BOUNDARY.authorization, 'NOT AUTHORIZED')
  assert.equal(TRUTH_BOUNDARY.empiricalN, 0)
  assert.equal(TRUTH_BOUNDARY.efficacy, 'NOT ESTABLISHED')
})

test('lifecycle predicates do not inherit readiness from prepared tooling', () => {
  const custody = GOVERNANCE_STAGES.find(stage => stage.id === 'repository-custody')
  const freeze = GOVERNANCE_STAGES.find(stage => stage.id === 'immutable-freeze')
  const collection = GOVERNANCE_STAGES.find(stage => stage.id === 'collection-authorization')
  assert.equal(custody?.predicateState, 'not_established')
  assert.equal(freeze?.toolingPrepared, true)
  assert.notEqual(freeze?.predicateState, 'pass')
  assert.equal(collection?.predicateState, 'not_authorized')
})

test('runtime codenames are translated with public function first', () => {
  assert.equal(agentDisplayName('amethyst'), 'Governance Orchestrator (Amethyst)')
  assert.equal(agentDisplayName('colleen'), 'Continuity & Provenance Coordinator (COLLEEN)')
  assert.equal(agentDisplayName('apogee'), 'Evidence & Verification Reviewer (Apogee)')
  assert.equal(agentDisplayName('demijole'), 'Runtime Safety & Constraint Adviser (DemiJoule)')
})
