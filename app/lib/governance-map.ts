import { GOVERNANCE_STAGES, TRUTH_BOUNDARY } from './governance.ts'
import type { UiState } from './types.ts'

export type GovernanceRelationKind = 'evidence' | 'authority' | 'dependency'

export interface GovernanceMapRelationship {
  id: string
  sourceId: string
  targetId: string
  kind: GovernanceRelationKind
  label: string
  provenance: string
  doesNotEstablish: string
}

export interface GovernanceMapStage {
  id: string
  label: string
  shortLabel: string
  state: UiState
  description: string
  evidenceBoundary: string
  doesNotEstablish: string
}

function projectStage(index: number): GovernanceMapStage {
  const stage = GOVERNANCE_STAGES[index]
  return {
    id: stage.id,
    label: stage.label,
    shortLabel: stage.shortLabel,
    state: stage.predicateState,
    description: stage.description,
    evidenceBoundary: stage.evidenceBoundary,
    doesNotEstablish: stage.doesNotEstablish,
  }
}

const blockingIndex = GOVERNANCE_STAGES.findIndex(stage => stage.predicateState !== 'pass')
const lifecycleComplete = blockingIndex === -1

export const GOVERNANCE_RELATIONSHIPS: GovernanceMapRelationship[] = [
  {
    id: 'custody-to-evidence-admission',
    sourceId: 'repository-custody',
    targetId: 'operator-evidence-admission',
    kind: 'evidence',
    label: 'Custody supports evidence admissibility',
    provenance:
      'The accepted repository custody and recovery evidence precede the retained operator-evidence admission path.',
    doesNotEstablish:
      'Independent custody, independent verification, materialization, analysis authority, or efficacy.',
  },
  {
    id: 'dataset-lock-to-unblinding',
    sourceId: 'dataset-lock',
    targetId: 'unblinding-decision',
    kind: 'authority',
    label: 'Dataset lock bounds unblinding',
    provenance:
      'The accepted dataset-lock receipt is a predecessor to the separately bounded mapping-release decision.',
    doesNotEstablish:
      'Materialization, primary-analysis authority, scientific-N promotion, independent validation, or efficacy.',
  },
  {
    id: 'materialization-to-analysis-authorization',
    sourceId: 'materialization',
    targetId: 'primary-analysis-authorization',
    kind: 'dependency',
    label: 'Materialization gates analysis authorization',
    provenance:
      'An accepted immutable materialization receipt is a real predecessor to any separate primary-analysis authorization event.',
    doesNotEstablish:
      'Primary-analysis authorization, execution, a scientific result, efficacy, or certification.',
  },
  {
    id: 'analysis-authorization-to-execution',
    sourceId: 'primary-analysis-authorization',
    targetId: 'locked-analysis',
    kind: 'authority',
    label: 'Analysis authorization gates execution',
    provenance:
      'The accepted bounded primary-analysis authorization is the exact authority predecessor to locked execution.',
    doesNotEstablish:
      'Analysis execution, a positive result, efficacy, independent validation, certification, or broader production authority.',
  },
  {
    id: 'locked-result-to-interpretation',
    sourceId: 'locked-analysis',
    targetId: 'interpretation-adjudication',
    kind: 'dependency',
    label: 'Accepted locked result gates interpretation',
    provenance:
      'The accepted creation-only LOCKED_ANALYSIS_RESULT_RECORD and its retained operator-local bytes are predecessors to bounded interpretation/adjudication.',
    doesNotEstablish:
      'A favorable interpretation, canonical DGAF efficacy, independent validation, scientific-N promotion, or High-Assurance authorization.',
  },
]

const stageIds = new Set(GOVERNANCE_STAGES.map(stage => stage.id))
for (const relationship of GOVERNANCE_RELATIONSHIPS) {
  if (!stageIds.has(relationship.sourceId) || !stageIds.has(relationship.targetId)) {
    throw new Error(`Governance Map relationship ${relationship.id} references a non-canonical stage`)
  }
}

export const GOVERNANCE_MAP = {
  lifecycleComplete,
  stages: GOVERNANCE_STAGES.map((_, index) => projectStage(index)),
  blocking: lifecycleComplete ? null : projectStage(blockingIndex),
  completed: lifecycleComplete
    ? GOVERNANCE_STAGES.map((_, index) => projectStage(index))
    : GOVERNANCE_STAGES.slice(0, blockingIndex).map((_, index) => projectStage(index)),
  downstream: lifecycleComplete
    ? []
    : GOVERNANCE_STAGES.slice(blockingIndex + 1).map((_, offset) =>
        projectStage(blockingIndex + 1 + offset),
      ),
  constraints: TRUTH_BOUNDARY,
  relationships: GOVERNANCE_RELATIONSHIPS,
} as const
