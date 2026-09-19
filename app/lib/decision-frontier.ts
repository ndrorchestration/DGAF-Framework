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
const lifecycleComplete = frontierIndex === -1

if (frontierIndex === 0) {
  throw new Error('Decision Frontier requires an established predecessor before an open boundary')
}

const currentIndex = lifecycleComplete ? GOVERNANCE_STAGES.length - 1 : frontierIndex - 1
const current = transitionAt(currentIndex, false)
const blocking = lifecycleComplete ? null : transitionAt(frontierIndex, false)
const nearest = lifecycleComplete ? null : transitionAt(frontierIndex, true)
const downstream = lifecycleComplete
  ? []
  : GOVERNANCE_STAGES.slice(frontierIndex + 1).map((_, offset) =>
      transitionAt(frontierIndex + 1 + offset, false),
    )

export const DECISION_FRONTIER = {
  lifecycleComplete,
  current,
  why: current.evidenceBoundary,
  blocking,
  nearest,
  downstream,
  consequence: lifecycleComplete ? current.doesNotEstablish : blocking!.doesNotEstablish,
  receipt: {
    label: 'Epoch 002 disposition',
    state: lifecycleComplete ? ('pass' as UiState) : blocking!.state,
    summary: lifecycleComplete
      ? 'PR #881 established the creation-only CLOSED_BOUNDED_SAME_SYSTEM_NONINDEPENDENT disposition. Epoch 002 is closed for its exact preregistered scope; the private numerical interpretation remains operator-local and no successor empirical epoch is authorized.'
      : 'The current modeled lifecycle has an unresolved predecessor and remains fail-closed.',
  },
  transitionTitle: NEXT_TRANSITION.title,
  transitionSummary: NEXT_TRANSITION.summary,
  warning: NEXT_TRANSITION.warning,
} as const
