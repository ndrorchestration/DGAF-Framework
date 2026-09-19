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
    label: 'Interpretation note',
    state: lifecycleComplete ? ('pass' as UiState) : blocking!.state,
    summary: lifecycleComplete
      ? 'PR #872 established the creation-only content-addressed INTERPRETATION_NOTE. The numerical estimate, interval, and classification remain operator-local; the admitted note records only the bounded interpretation identity and non-effects.'
      : 'The Epoch 002 locked primary analysis executed locally and its content-addressed result receipt is accepted. Interpretation tooling is accepted, but no INTERPRETATION_NOTE exists; the numerical output remains operator-local and must be revalidated before any separate interpretation admission.',
  },
  transitionTitle: NEXT_TRANSITION.title,
  transitionSummary: NEXT_TRANSITION.summary,
  warning: NEXT_TRANSITION.warning,
} as const
