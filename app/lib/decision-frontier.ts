import { GOVERNANCE_STAGES, NEXT_TRANSITION } from './governance.ts'
import type { UiState } from './types.ts'

export interface DecisionFrontierTransition {
  id: string
  label: string
  state: UiState
  reachable: boolean
  description: string
  evidenceBoundary: string
  doesNotEstablish: string
}

function transitionAt(index: number, reachable: boolean): DecisionFrontierTransition {
  const stage = GOVERNANCE_STAGES[index]
  return {
    id: stage.id,
    label: stage.label,
    state: stage.predicateState,
    reachable,
    description: stage.description,
    evidenceBoundary: stage.evidenceBoundary,
    doesNotEstablish: stage.doesNotEstablish,
  }
}

const frontierIndex = GOVERNANCE_STAGES.findIndex(stage => stage.predicateState !== 'pass')

if (frontierIndex <= 0) {
  throw new Error('Decision Frontier requires an established predecessor and an open boundary')
}

const current = transitionAt(frontierIndex - 1, false)
const blocking = transitionAt(frontierIndex, false)
const nearest = transitionAt(frontierIndex, true)
const downstream = GOVERNANCE_STAGES.slice(frontierIndex + 1).map((_, offset) =>
  transitionAt(frontierIndex + 1 + offset, false),
)

export const DECISION_FRONTIER = {
  current,
  why: current.evidenceBoundary,
  blocking,
  nearest,
  downstream,
  consequence: blocking.doesNotEstablish,
  receipt: {
    label: 'Immutable materialization receipt',
    state: blocking.predicateState,
    summary:
      'No accepted Epoch 002 MATERIALIZATION_RECEIPT exists. Execution evidence must remain non-secret and content-addressed before a separate receipt can be established.',
  },
  transitionTitle: NEXT_TRANSITION.title,
  transitionSummary: NEXT_TRANSITION.summary,
  warning: NEXT_TRANSITION.warning,
} as const
