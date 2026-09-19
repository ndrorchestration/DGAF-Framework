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

test('lifecycle reflects accepted Epoch 002 closure without downstream promotion', () => {
  const custody = GOVERNANCE_STAGES.find(stage => stage.id === 'repository-custody')
  const freeze = GOVERNANCE_STAGES.find(stage => stage.id === 'immutable-freeze')
  const authorization = GOVERNANCE_STAGES.find(stage => stage.id === 'collection-authorization')
  const collection = GOVERNANCE_STAGES.find(stage => stage.id === 'empirical-collection')
  const admission = GOVERNANCE_STAGES.find(stage => stage.id === 'operator-evidence-admission')
  const qualityControl = GOVERNANCE_STAGES.find(stage => stage.id === 'quality-control')
  const datasetLock = GOVERNANCE_STAGES.find(stage => stage.id === 'dataset-lock')
  const unblinding = GOVERNANCE_STAGES.find(stage => stage.id === 'unblinding-decision')
  const materialization = GOVERNANCE_STAGES.find(stage => stage.id === 'materialization')
  const analysisAuthorization = GOVERNANCE_STAGES.find(stage => stage.id === 'primary-analysis-authorization')
  const lockedAnalysis = GOVERNANCE_STAGES.find(stage => stage.id === 'locked-analysis')
  const interpretation = GOVERNANCE_STAGES.find(stage => stage.id === 'interpretation-adjudication')
  const disposition = GOVERNANCE_STAGES.find(stage => stage.id === 'post-interpretation-disposition')

  assert.equal(custody?.predicateState, 'pass')
  assert.equal(freeze?.predicateState, 'pass')
  assert.equal(authorization?.predicateState, 'pass')
  assert.equal(collection?.predicateState, 'pass')
  assert.equal(admission?.predicateState, 'pass')
  assert.equal(qualityControl?.predicateState, 'pass')
  assert.equal(datasetLock?.predicateState, 'pass')
  assert.equal(unblinding?.predicateState, 'pass')
  assert.equal(materialization?.predicateState, 'pass')
  assert.equal(materialization?.toolingPrepared, true)
  assert.equal(analysisAuthorization?.predicateState, 'pass')
  assert.equal(lockedAnalysis?.predicateState, 'pass')
  assert.equal(lockedAnalysis?.toolingPrepared, true)
  assert.equal(interpretation?.predicateState, 'pass')
  assert.equal(interpretation?.toolingPrepared, true)
  assert.match(interpretation?.toolingNote ?? '', /#872/)
  assert.equal(disposition?.predicateState, 'pass')
  assert.equal(disposition?.toolingPrepared, true)
  assert.match(disposition?.toolingNote ?? '', /#881/)
})

test('every lifecycle stage carries an explicit claim boundary', () => {
  for (const stage of GOVERNANCE_STAGES) {
    assert.ok(stage.evidenceBoundary.length > 0)
    assert.ok(stage.doesNotEstablish.length > 0)
  }
})

test('runtime codenames are translated with public function first', () => {
  assert.equal(agentDisplayName('amethyst'), 'Governance Orchestrator (Amethyst)')
  assert.equal(agentDisplayName('colleen'), 'Continuity & Provenance Coordinator (COLLEEN)')
  assert.equal(agentDisplayName('apogee'), 'Evidence & Verification Reviewer (Apogee)')
  assert.equal(agentDisplayName('demijole'), 'Runtime Safety & Constraint Adviser (DemiJoule)')
})
