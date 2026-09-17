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

if (blockingIndex < 0) {
  throw new Error('Governance Map requires an unresolved canonical governance stage')
}

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
      'Locked primary analysis remains unreachable until the separate analysis-authorization predicate is accepted.',
    doesNotEstablish:
      'A positive result, efficacy, independent validation, certification, or broader production authority.',
  },
]

const stageIds = new Set(GOVERNANCE_STAGES.map(stage => stage.id))
for (const relationship of GOVERNANCE_RELATIONSHIPS) {
  if (!stageIds.has(relationship.sourceId) || !stageIds.has(relationship.targetId)) {
    throw new Error(`Governance Map relationship ${relationship.id} references a non-canonical stage`)
  }
}

export const GOVERNANCE_MAP = {
  stages: GOVERNANCE_STAGES.map((_, index) => projectStage(index)),
  blocking: projectStage(blockingIndex),
  completed: GOVERNANCE_STAGES.slice(0, blockingIndex).map((_, index) => projectStage(index)),
  downstream: GOVERNANCE_STAGES.slice(blockingIndex + 1).map((_, offset) =>
    projectStage(blockingIndex + 1 + offset),
  ),
  constraints: TRUTH_BOUNDARY,
  relationships: GOVERNANCE_RELATIONSHIPS,
} as const
