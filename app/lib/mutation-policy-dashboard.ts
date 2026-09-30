import type { UiState } from './types'

export interface MutationPolicyDashboardLane {
  path: string
  label: string
  state: UiState
  policyId: string
  lifecycle: string
  reason: string
  nextAction: string
  evidence: string[]
}

export interface MutationPolicyDashboardSummary {
  sourceUpdated: string
  claimBoundary: readonly string[]
  counts: {
    blocked: number
    routineAllowed: number
    pendingReconciliation: number
  }
  lanes: readonly MutationPolicyDashboardLane[]
}

const CLAIM_BOUNDARY = [
  'SCIENTIFIC_N_INCREMENT=0',
  'INDEPENDENT_VALIDATION=NOT_ESTABLISHED',
  'CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED',
  'HIGH_ASSURANCE=NOT_AUTHORIZED',
] as const

export const MUTATION_POLICY_DASHBOARD: MutationPolicyDashboardSummary = {
  sourceUpdated: '2026-09-30',
  claimBoundary: CLAIM_BOUNDARY,
  counts: {
    blocked: 11,
    routineAllowed: 0,
    pendingReconciliation: 11,
  },
  lanes: [
    {
      path: '.github/workflows/pdmal-solo-final-experiment.yml',
      label: 'Retired Solo final experiment',
      state: 'blocked',
      policyId: 'MUTATION_BLOCKED_PENDING_RETIREMENT_CONTRACT_CLEANUP',
      lifecycle: 'HISTORICAL_EXACT_SCOPE',
      reason: 'Retired workflow retains historical authority-token text; retirement-contract cleanup must prove no live execution path before #939 pinning.',
      nextAction: 'Resolve #1138 before touching this workflow.',
      evidence: ['#1134 exact-head retirement guard failed after checkout succeeded', '#369 remains blocking for any fresh Solo empirical epoch'],
    },
    {
      path: '.github/workflows/b1-semantic-routing-safety-profile.yml',
      label: 'B1 semantic-routing profile',
      state: 'blocked',
      policyId: 'MUTATION_BLOCKED_SOURCE_BOUND_RECONCILIATION_REQUIRED',
      lifecycle: 'SOURCE_BOUND_EVIDENCE',
      reason: 'Profile validators source-bind the workflow by expected hash, so routine YAML mutation would create source-binding drift.',
      nextAction: 'Perform explicit source-binding reconciliation before ordinary #939 hardening.',
      evidence: ['audit_catalog.v1.json classifies this as source-bound non-empirical profile evidence'],
    },
    {
      path: '.github/workflows/b2-stateful-context-closure-profile.yml',
      label: 'B2 stateful-context profile',
      state: 'blocked',
      policyId: 'MUTATION_BLOCKED_SOURCE_BOUND_RECONCILIATION_REQUIRED',
      lifecycle: 'SOURCE_BOUND_EVIDENCE',
      reason: 'Profile validators source-bind the workflow by expected hash, so routine YAML mutation would create source-binding drift.',
      nextAction: 'Perform explicit source-binding reconciliation before ordinary #939 hardening.',
      evidence: ['audit_catalog.v1.json classifies this as source-bound non-empirical profile evidence'],
    },
    {
      path: '.github/workflows/b3-p33-convergence-profile.yml',
      label: 'B3 P-33 convergence profile',
      state: 'blocked',
      policyId: 'MUTATION_BLOCKED_SOURCE_BOUND_RECONCILIATION_REQUIRED',
      lifecycle: 'SOURCE_BOUND_EVIDENCE',
      reason: 'Exact-head CI already exposed adjacent validator source-blob drift for this lane.',
      nextAction: 'Perform dedicated source-binding reconciliation before ordinary #939 hardening.',
      evidence: ['#1127 exact-head CI exposed source-blob drift', 'workflow is implementation evidence for B3 profile/adjudication lanes'],
    },
    {
      path: '.github/workflows/track-a-epoch-002-preregistration.yml',
      label: 'Track A Epoch 002 preregistration',
      state: 'blocked',
      policyId: 'MUTATION_BLOCKED_STALE_SUCCESSOR_STATE_RECONCILIATION_REQUIRED',
      lifecycle: 'CLOSED_BOUNDED_EXACT_SCOPE',
      reason: 'The retained preregistration workflow still encodes successor-custody absence while successor custody evidence now exists.',
      nextAction: 'Reconcile historical-at-preregistration state from current successor-custody state.',
      evidence: ['successor custody recovery evidence now exists on protected main', '#1133 documented the stale absence failure'],
    },
    {
      path: '.github/workflows/track-a-epoch-002-analysis-lock.yml',
      label: 'Track A Epoch 002 analysis lock',
      state: 'blocked',
      policyId: 'MUTATION_BLOCKED_STALE_SUCCESSOR_STATE_RECONCILIATION_REQUIRED',
      lifecycle: 'CLOSED_BOUNDED_EXACT_SCOPE',
      reason: 'The lock-time boundary asserts successor custody is not established, which is no longer true on protected main.',
      nextAction: 'Reconcile historical lock-time boundary fields without changing scientific authority.',
      evidence: ['workflow and validator repeat successor_custody_recovery_receipt_established is false'],
    },
    {
      path: '.github/workflows/track-a-epoch-002-primary-analysis-autopilot.yml',
      label: 'Track A Epoch 002 primary-analysis autopilot',
      state: 'blocked',
      policyId: 'MUTATION_BLOCKED_POST_RESULT_LIFECYCLE_RECONCILIATION_REQUIRED',
      lifecycle: 'CLOSED_BOUNDED_EXACT_SCOPE',
      reason: 'Post-result state now intentionally refuses preflight execution once the locked result record exists.',
      nextAction: 'Define explicit post-result verification mode before maintaining this historical autopilot workflow.',
      evidence: ['#1149 passed immutable-action setup then failed because locked result record already exists'],
    },
    {
      path: '.github/workflows/track-a-epoch-001-runner.yml',
      label: 'Track A Epoch 001 runner',
      state: 'blocked',
      policyId: 'MUTATION_BLOCKED_STALE_DOWNSTREAM_STATE_RECONCILIATION_REQUIRED',
      lifecycle: 'HISTORICAL_EXACT_SCOPE',
      reason: 'Runner-time absence assertions now conflict with downstream Epoch 001 artifacts on protected main.',
      nextAction: 'Separate runner-time absence assertions from current repository state.',
      evidence: ['#1157 encoded five confirmed Epoch 001 stale-state blocks'],
    },
    {
      path: '.github/workflows/track-a-epoch-001-unblinding-materialization.yml',
      label: 'Track A Epoch 001 unblinding materialization',
      state: 'blocked',
      policyId: 'MUTATION_BLOCKED_STATE_AWARE_RECONCILIATION_REQUIRED',
      lifecycle: 'HISTORICAL_EXACT_SCOPE',
      reason: 'Validation asserts no unblinding and no analysis side effects; routine mutation requires state-aware reconciliation.',
      nextAction: 'Preserve validation-time no-unblinding semantics before any #939 mutation.',
      evidence: ['#1159 supplement records this as a blocked successor-adjacent lane'],
    },
    {
      path: '.github/workflows/track-a-epoch-001-primary-analysis-authorization.yml',
      label: 'Track A Epoch 001 primary-analysis authorization',
      state: 'blocked',
      policyId: 'MUTATION_BLOCKED_EXACT_SCOPE_RECONCILIATION_REQUIRED',
      lifecycle: 'HISTORICAL_EXACT_SCOPE',
      reason: 'The workflow contains exact authorization/tooling branch logic and primary-result absence checks.',
      nextAction: 'Reconcile exact-scope branch semantics before routine hardening.',
      evidence: ['#1159 supplement records this exact-scope lane as blocked'],
    },
    {
      path: '.github/workflows/track-a-successor-solo-custody.yml',
      label: 'Track A successor solo-custody',
      state: 'blocked',
      policyId: 'MUTATION_BLOCKED_SIDE_EFFECT_BOUNDARY_RECONCILIATION_REQUIRED',
      lifecycle: 'SYNTHETIC_ONLY_CUSTODY_VALIDATION',
      reason: 'The workflow asserts no recovery receipt or private key side effects while successor evidence exists elsewhere.',
      nextAction: 'Reconcile synthetic-only side-effect boundaries before any routine mutation.',
      evidence: ['#1159 supplement records this side-effect boundary as blocked'],
    },
  ],
}

export const MUTATION_POLICY_DISPLAY_LIMIT = 6

export function visibleMutationPolicyLanes(limit = MUTATION_POLICY_DISPLAY_LIMIT) {
  return MUTATION_POLICY_DASHBOARD.lanes.slice(0, limit)
}

export function hiddenMutationPolicyLaneCount(limit = MUTATION_POLICY_DISPLAY_LIMIT) {
  return Math.max(0, MUTATION_POLICY_DASHBOARD.lanes.length - limit)
}
