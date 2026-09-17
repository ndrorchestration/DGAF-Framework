import { GOVERNANCE_STAGES, TRUTH_BOUNDARY } from './governance.ts'

export type ReachabilityRegion = 'established' | 'frontier' | 'blocked_by_predecessor'
export type DimensionRepresentation = 'projectable' | 'bounded' | 'not_modeled'

export interface StateSpaceRegion {
  id: string
  label: string
  shortLabel: string
  order: number
  nativeState: (typeof GOVERNANCE_STAGES)[number]['predicateState']
  reachability: ReachabilityRegion
  evidenceBoundary: string
  doesNotEstablish: string
}

export interface StateSpaceDimension {
  id: string
  label: string
  representation: DimensionRepresentation
  description: string
}

const frontierIndex = GOVERNANCE_STAGES.findIndex(stage => stage.predicateState !== 'pass')

function reachabilityFor(index: number): ReachabilityRegion {
  if (frontierIndex === -1) return 'established'
  if (index < frontierIndex) return 'established'
  if (index === frontierIndex) return 'frontier'
  return 'blocked_by_predecessor'
}

export const STATE_SPACE_PROJECTION = {
  frontierId: frontierIndex === -1 ? null : GOVERNANCE_STAGES[frontierIndex].id,
  constraints: TRUTH_BOUNDARY,
  regions: GOVERNANCE_STAGES.map((stage, index): StateSpaceRegion => ({
    id: stage.id,
    label: stage.label,
    shortLabel: stage.shortLabel,
    order: index,
    nativeState: stage.predicateState,
    reachability: reachabilityFor(index),
    evidenceBoundary: stage.evidenceBoundary,
    doesNotEstablish: stage.doesNotEstablish,
  })),
} as const

export const STATE_SPACE_DIMENSIONS: StateSpaceDimension[] = [
  {
    id: 'reachability',
    label: 'Lifecycle / reachability',
    representation: 'projectable',
    description: 'Derived categorically from canonical stage order and the first unsatisfied predicate.',
  },
  {
    id: 'native-state',
    label: 'Native predicate state',
    representation: 'projectable',
    description: 'Preserves each canonical stage predicate without replacing it with reachability.',
  },
  {
    id: 'evidence-boundary',
    label: 'Evidence boundary',
    representation: 'projectable',
    description: 'Preserves the exact bounded claim text attached to each canonical stage.',
  },
  {
    id: 'provenance',
    label: 'Provenance / source binding',
    representation: 'bounded',
    description: 'Explicit lineage may be inspected where recorded; independence is never inferred.',
  },
  {
    id: 'verification',
    label: 'Verification',
    representation: 'bounded',
    description: 'Only explicit verification semantics are shown; no universal scalar coordinate exists.',
  },
  {
    id: 'authorization',
    label: 'Authorization / authority',
    representation: 'bounded',
    description: 'Categorical authority and authorization facts remain distinct and scope-bound.',
  },
  {
    id: 'uncertainty',
    label: 'Uncertainty',
    representation: 'bounded',
    description: 'Unknown and not-established states remain categorical rather than becoming a confidence number.',
  },
  {
    id: 'consequence',
    label: 'Consequence',
    representation: 'not_modeled',
    description: 'No canonical per-stage consequence coordinate is established in the current UI truth model.',
  },
  {
    id: 'reversibility',
    label: 'Reversibility',
    representation: 'not_modeled',
    description: 'The generic formalism defines recovery classes, but current stages do not carry canonical per-stage values.',
  },
]
