import assert from 'node:assert/strict'
import test from 'node:test'

import {
  hiddenMutationPolicyLaneCount,
  MUTATION_POLICY_DASHBOARD,
  MUTATION_POLICY_DISPLAY_LIMIT,
  visibleMutationPolicyLanes,
} from './mutation-policy-dashboard.ts'

test('mutation-policy dashboard projection preserves claim boundaries', () => {
  assert.deepEqual(MUTATION_POLICY_DASHBOARD.claimBoundary, [
    'SCIENTIFIC_N_INCREMENT=0',
    'INDEPENDENT_VALIDATION=NOT_ESTABLISHED',
    'CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED',
    'HIGH_ASSURANCE=NOT_AUTHORIZED',
  ])
})

test('mutation-policy dashboard projection is blocked-only until reconciliation exists', () => {
  assert.equal(MUTATION_POLICY_DASHBOARD.counts.routineAllowed, 0)
  assert.equal(MUTATION_POLICY_DASHBOARD.counts.blocked, MUTATION_POLICY_DASHBOARD.lanes.length)
  assert.equal(MUTATION_POLICY_DASHBOARD.counts.pendingReconciliation, MUTATION_POLICY_DASHBOARD.lanes.length)
  assert.ok(MUTATION_POLICY_DASHBOARD.lanes.every(lane => lane.state === 'blocked'))
  assert.ok(MUTATION_POLICY_DASHBOARD.lanes.every(lane => lane.nextAction.length > 0))
})

test('mutation-policy dashboard projection includes the latest successor supplement lanes', () => {
  const paths = new Set(MUTATION_POLICY_DASHBOARD.lanes.map(lane => lane.path))
  assert.ok(paths.has('.github/workflows/track-a-epoch-001-unblinding-materialization.yml'))
  assert.ok(paths.has('.github/workflows/track-a-epoch-001-primary-analysis-authorization.yml'))
  assert.ok(paths.has('.github/workflows/track-a-successor-solo-custody.yml'))
})

test('mutation-policy dashboard display limit leaves an explicit remainder', () => {
  assert.equal(visibleMutationPolicyLanes().length, MUTATION_POLICY_DISPLAY_LIMIT)
  assert.equal(
    hiddenMutationPolicyLaneCount(),
    MUTATION_POLICY_DASHBOARD.lanes.length - MUTATION_POLICY_DISPLAY_LIMIT,
  )
})
