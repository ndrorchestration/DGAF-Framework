import type { UiState } from './types'

export const TRUTH_BOUNDARY = {
  programState: 'PRE-FREEZE',
  failMode: 'FAIL-CLOSED',
  authorization: 'NOT AUTHORIZED',
  empiricalN: 0,
  efficacy: 'NOT ESTABLISHED',
  sourceUpdated: '2026-09-11',
  sources: ['docs/PROJECT_STATUS.md', 'docs/CURRENT_STATE.md', 'docs/PUBLIC_TRANSLATION_LAYER.md'],
} as const

export interface GovernanceStage {
  id: string
  label: string
  shortLabel: string
  description: string
  predicateState: UiState
  toolingPrepared: boolean
  toolingNote?: string
}

export const CURRENT_FRONTIER_ID = 'immutable-freeze' as const

export const GOVERNANCE_STAGES: GovernanceStage[] = [
  {
    id: 'repository-custody',
    label: 'Repository custody acceptance',
    shortLabel: 'Custody',
    description: 'Validate and retain the exact public successor custody certificate and schema-v2 recovery receipt.',
    predicateState: 'pass',
    toolingPrepared: true,
    toolingNote:
      'The completion reconciler marks real_custody_v2 SATISFIED. Custody remains SAME_SYSTEM_NONINDEPENDENT; independent custody is false and this does not authorize collection.',
  },
  {
    id: 'precollection-preflight',
    label: 'Precollection preflight',
    shortLabel: 'Preflight',
    description: 'Retain the exact non-authorizing successor preflight record against the accepted custody evidence.',
    predicateState: 'pass',
    toolingPrepared: true,
    toolingNote:
      'The canonical Epoch 002 precollection preflight record is retained on accepted main. This satisfies preflight only and does not establish immutable freeze or collection authority.',
  },
  {
    id: 'immutable-freeze',
    label: 'Immutable freeze',
    shortLabel: 'Freeze',
    description: 'Bind the exact experimental candidate immutably after predecessor closure.',
    predicateState: 'open',
    toolingPrepared: true,
    toolingNote: 'Freeze tooling is prepared; no successor immutable freeze manifest is accepted yet.',
  },
  {
    id: 'final-closure',
    label: 'Final closure',
    shortLabel: 'Closure',
    description: 'Prove pre-authorization completeness for the exact frozen successor candidate.',
    predicateState: 'blocked',
    toolingPrepared: true,
    toolingNote: 'Closure tooling is prepared; successor closure is not established.',
  },
  {
    id: 'verification-classification',
    label: 'Verification classification',
    shortLabel: 'Verification',
    description: 'Classify the verification path and independence level without widening evidence scope.',
    predicateState: 'blocked',
    toolingPrepared: true,
    toolingNote: 'Classification tooling is prepared; predecessor acceptance is still required.',
  },
  {
    id: 'collection-authorization',
    label: 'Collection authorization',
    shortLabel: 'Authorize',
    description: 'A separate human-controlled decision permits the exact prospective collection.',
    predicateState: 'not_authorized',
    toolingPrepared: true,
    toolingNote: 'Authorization validation tooling exists; permission has not been granted.',
  },
  {
    id: 'empirical-collection',
    label: 'Empirical collection',
    shortLabel: 'Collect',
    description: 'Execute only the separately authorized successor collection.',
    predicateState: 'not_authorized',
    toolingPrepared: false,
  },
  {
    id: 'quality-control',
    label: 'Quality control',
    shortLabel: 'QC',
    description: 'Perform bounded post-collection quality checks before any dataset lock.',
    predicateState: 'blocked',
    toolingPrepared: false,
  },
  {
    id: 'dataset-lock',
    label: 'Dataset lock',
    shortLabel: 'Lock',
    description: 'Create an immutable content-addressed receipt for the collected successor dataset.',
    predicateState: 'not_established',
    toolingPrepared: true,
    toolingNote: 'Dataset-lock validation tooling is prepared; no successor dataset lock exists.',
  },
  {
    id: 'unblinding-decision',
    label: 'Separate unblinding decision',
    shortLabel: 'Unblind',
    description: 'A separate human-controlled decision governs bounded treatment-identity release.',
    predicateState: 'not_authorized',
    toolingPrepared: true,
    toolingNote: 'Unblinding-decision validation tooling exists; unblinding remains prohibited.',
  },
  {
    id: 'materialization',
    label: 'Controlled materialization + immutable receipt',
    shortLabel: 'Materialize',
    description: 'Deterministically construct analysis-ready unblinded input only after authorization.',
    predicateState: 'not_established',
    toolingPrepared: false,
  },
  {
    id: 'primary-analysis-authorization',
    label: 'Primary-analysis authorization',
    shortLabel: 'Analysis auth',
    description: 'A separate decision authorizes the locked confirmatory analysis and nothing broader.',
    predicateState: 'not_authorized',
    toolingPrepared: false,
  },
  {
    id: 'locked-analysis',
    label: 'Locked primary analysis',
    shortLabel: 'Analyze',
    description: 'Run the preregistered locked analysis only after every predecessor is satisfied.',
    predicateState: 'not_authorized',
    toolingPrepared: false,
  },
]

export const NEXT_TRANSITION = {
  title: 'Establish Epoch 002 immutable freeze',
  headingSummary:
    'Custody and precollection preflight are satisfied. Immutable freeze is now the next non-authorizing predecessor; prepared downstream tooling does not move the frontier.',
  evidenceTitle: 'Precollection preflight is accepted.',
  evidenceStatusLabel: 'PREFLIGHT ACCEPTED',
  evidence:
    'Repository custody-v2 remains SATISFIED / SAME_SYSTEM_NONINDEPENDENT, and the canonical Epoch 002 precollection preflight record is retained on accepted main. Independent custody remains false.',
  blockerTitle: 'The immutable freeze manifest does not yet exist.',
  blockerStatusLabel: 'ACTIONABLE / NOT ESTABLISHED',
  blocker:
    'The canonical Epoch 002 immutable freeze manifest is absent. Freeze tooling is prepared, but immutable freeze is not established until the exact one-file record is admitted and accepted.',
  actionTitle: 'Prepare only the non-authorizing immutable freeze manifest.',
  summary:
    'From a clean branch based on current accepted main containing the retained preflight record, run the immutable-freeze helper with --write. It writes only the canonical freeze manifest; review that one-file delta before validation and merge.',
  artifacts: ['docs/experiment/track_a_runs/TRACK_A_EPOCH_002_IMMUTABLE_FREEZE_MANIFEST.json'],
  operatorBranch: 'clean branch from current accepted main containing merged #651',
  operatorCommand: 'python scripts/prepare_track_a_epoch_002_immutable_freeze.py --write',
  operatorVerification: 'git diff --name-only',
  operatorSafety:
    'The freeze helper consumes only already-retained repository evidence and protected source identities. It does not create custody secrets, authorize empirical collection, unblind data, run empirical work, or increment scientific N.',
  warning:
    'Freeze preparation does not establish final closure, classify verification, authorize successor collection, increment scientific N, authorize unblinding or primary analysis, or establish efficacy.',
} as const

export interface EpochSummary {
  id: 'epoch-001' | 'epoch-002'
  eyebrow: string
  title: string
  state: UiState
  summary: string
  facts: string[]
}

export const EPOCH_SUMMARIES: EpochSummary[] = [
  {
    id: 'epoch-001',
    eyebrow: 'Historical prospective collection',
    title: 'Track A · Epoch 001',
    state: 'not_established',
    summary:
      'The blinded prospective collection and dataset lock completed, but the protected mapping is cryptographically unrecoverable, so the primary analysis is unanalyzable and was not run.',
    facts: [
      '50 paired inferential seed units',
      '2,250 blinded raw observations retained',
      'Dataset lock established',
      'Protected mapping cryptographically unrecoverable',
      'Primary analysis: UNANALYZABLE / NOT RUN',
    ],
  },
  {
    id: 'epoch-002',
    eyebrow: 'Successor prospective path',
    title: 'Track A · Epoch 002',
    state: 'not_authorized',
    summary:
      'Repository custody-v2 and the non-authorizing precollection preflight are now accepted. Immutable freeze is the next actionable gate; empirical collection remains unauthorized.',
    facts: [
      'Repository custody-v2: SATISFIED / SAME_SYSTEM_NONINDEPENDENT',
      'Independent custody: FALSE',
      'Precollection preflight: ACCEPTED / RETAINED',
      'Immutable freeze: ACTIONABLE / NOT ESTABLISHED',
      'Empirical collection: NOT AUTHORIZED / NOT EXECUTED',
      'Scientific N: 0',
    ],
  },
]

export const EVIDENCE_STATES: Array<{ state: UiState; term: string; meaning: string }> = [
  { state: 'info', term: 'PROPOSED', meaning: 'Designed but not demonstrated.' },
  { state: 'info', term: 'IMPLEMENTED', meaning: 'Exists in code or artifacts.' },
  { state: 'info', term: 'TESTED', meaning: 'Covered by stated tests in the stated environment.' },
  { state: 'pass', term: 'PASS', meaning: 'The exact predicate passed; scope does not widen automatically.' },
  { state: 'verified', term: 'VERIFIED', meaning: 'A defined verification predicate passed.' },
  {
    state: 'open',
    term: 'DEVELOPER SELF-ATTESTED / NONINDEPENDENT',
    meaning: 'Evidence comes from the same developer/system lineage and is not independent validation.',
  },
  {
    state: 'verified',
    term: 'INDEPENDENTLY VERIFIED',
    meaning: 'A separate accepted independence and evidence path was established.',
  },
  { state: 'not_authorized', term: 'NOT AUTHORIZED', meaning: 'The named execution remains prohibited.' },
  {
    state: 'not_established',
    term: 'NOT ESTABLISHED',
    meaning: 'Current evidence does not establish the claim; this is not equivalent to disproven.',
  },
  {
    state: 'pass',
    term: 'EMPIRICALLY DEMONSTRATED',
    meaning: 'Supported by an executed experiment in the exact stated scope.',
  },
]
