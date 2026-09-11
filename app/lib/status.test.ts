import test from 'node:test'
import assert from 'node:assert/strict'
import { GOVERNANCE_STAGES, NEXT_TRANSITION, TRUTH_BOUNDARY } from './governance.ts'
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

test('not authorized is a governance lock, not a failure tone', () => {
  assert.equal(STATUS_META.not_authorized.label, 'Not authorized')
  assert.equal(STATUS_META.not_authorized.tone, 'authority')
  assert.notEqual(STATUS_META.not_authorized.tone, 'danger')
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

test('next custody action exposes the exact canonical repository destinations', () => {
  assert.deepEqual(NEXT_TRANSITION.artifacts, [
    'docs/experiment/track_a_runs/TRACK_A_SUCCESSOR_CUSTODY_CERT.pem',
    'docs/experiment/track_a_runs/TRACK_A_SUCCESSOR_SOLO_CUSTODY_RECOVERY_RECEIPT.json',
  ])
})

test('next custody action follows the current fail-closed admission helper contract', () => {
  assert.equal(NEXT_TRANSITION.operatorBranch, 'track-a-successor-custody-evidence-v2')
  assert.equal(NEXT_TRANSITION.operatorCommand, 'py -3 scripts/prepare_track_a_successor_custody_admission.py')
  assert.equal(NEXT_TRANSITION.operatorVerification, 'git diff --cached --name-only')
})

test('runtime codenames are translated with public function first', () => {
  assert.equal(agentDisplayName('amethyst'), 'Governance Orchestrator (Amethyst)')
  assert.equal(agentDisplayName('colleen'), 'Continuity & Provenance Coordinator (COLLEEN)')
  assert.equal(agentDisplayName('apogee'), 'Evidence & Verification Reviewer (Apogee)')
  assert.equal(agentDisplayName('demijole'), 'Runtime Safety & Constraint Adviser (DemiJoule)')
})
