import type { UiState } from './types'

export const TRUTH_BOUNDARY = {
  programState: 'PRE-FREEZE',
  failMode: 'FAIL-CLOSED',
  authorization: 'NOT AUTHORIZED',
  empiricalN: 0,
  efficacy: 'NOT ESTABLISHED',
  sourceUpdated: '2026-09-19',
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
  evidenceBoundary: string
  doesNotEstablish: string
}

export const GOVERNANCE_STAGES: GovernanceStage[] = [
  {
    id: 'repository-custody',
    label: 'Repository custody acceptance',
    shortLabel: 'Custody',
    description: 'The exact successor custody certificate and recovery receipt were admitted and accepted.',
    predicateState: 'pass',
    toolingPrepared: true,
    toolingNote: 'Custody-v2 admission and validation are accepted predecessors.',
    evidenceBoundary: 'Recoverability is established at SAME_SYSTEM_NONINDEPENDENT scope.',
    doesNotEstablish: 'Independent custody, independent verification, efficacy, or downstream authority.',
  },
  {
    id: 'precollection-preflight',
    label: 'Precollection preflight',
    shortLabel: 'Preflight',
    description: 'The successor collection prerequisites were accepted against exact predecessor evidence.',
    predicateState: 'pass',
    toolingPrepared: true,
    evidenceBoundary: 'The defined precollection checks passed at their accepted identity.',
    doesNotEstablish: 'Freeze, authorization, execution, dataset lock, or efficacy.',
  },
  {
    id: 'immutable-freeze',
    label: 'Epoch 002 immutable freeze',
    shortLabel: 'Freeze',
    description: 'The exact Epoch 002 candidate and prospective inputs are immutably bound.',
    predicateState: 'pass',
    toolingPrepared: true,
    evidenceBoundary: 'The successor Epoch 002 freeze is established.',
    doesNotEstablish: 'The separate canonical High-Assurance freeze, collection permission, or efficacy.',
  },
  {
    id: 'final-closure',
    label: 'Final closure',
    shortLabel: 'Closure',
    description: 'The predecessor checklist is accepted as closed for authorization review.',
    predicateState: 'pass',
    toolingPrepared: true,
    evidenceBoundary: 'CLOSED_VERIFIED_FOR_AUTHORIZATION_REVIEW at the accepted scope.',
    doesNotEstablish: 'Authorization, execution, unblinding, analysis, or a scientific result.',
  },
  {
    id: 'verification-classification',
    label: 'Verification classification',
    shortLabel: 'Verification',
    description: 'The accepted verification path is explicitly developer self-attested and non-independent.',
    predicateState: 'pass',
    toolingPrepared: true,
    evidenceBoundary: 'The evidence class and its limitations are explicit and machine-checkable.',
    doesNotEstablish: 'Independent verification or a broader claim than the classified evidence supports.',
  },
  {
    id: 'collection-authorization',
    label: 'Collection authorization',
    shortLabel: 'Authorize',
    description: 'A separate human-controlled event authorized the exact bounded Epoch 002 collection.',
    predicateState: 'pass',
    toolingPrepared: true,
    evidenceBoundary: 'Accepted authorization commit 563152fdb254b8ee948a693c287126a8bf8314b8.',
    doesNotEstablish: 'Dataset lock, unblinding, materialization, primary-analysis authority, or efficacy.',
  },
  {
    id: 'empirical-collection',
    label: 'Blinded empirical collection',
    shortLabel: 'Collect',
    description: 'The operator-executed Codespace collection completed at 50 paired seed units / 2,250 blinded observations.',
    predicateState: 'pass',
    toolingPrepared: true,
    evidenceBoundary: 'Collection completion is accepted for the authorized Epoch 002 execution.',
    doesNotEstablish: 'Dataset lock, materialization, canonical N promotion, or efficacy by itself.',
  },
  {
    id: 'operator-evidence-admission',
    label: 'Operator evidence admission',
    shortLabel: 'Admit evidence',
    description: 'The bounded operator-retained evidence chain was admitted as the predecessor to dataset lock.',
    predicateState: 'pass',
    toolingPrepared: true,
    toolingNote: 'The accepted OPERATOR_CODESPACE/content-addressed predecessor chain now supports the dataset-lock receipt.',
    evidenceBoundary: 'Acceptance is bounded to the admitted retained evidence and its exact identities.',
    doesNotEstablish: 'Unblinding, materialization, primary-analysis authority, independent validation, or efficacy.',
  },
  {
    id: 'quality-control',
    label: 'Pre-lock structural quality control',
    shortLabel: 'QC',
    description: 'The bounded blinded pre-lock QC/ledger predecessor chain is accepted.',
    predicateState: 'pass',
    toolingPrepared: true,
    evidenceBoundary: 'Structural QC is a predecessor to dataset lock and does not inspect treatment identity for analysis.',
    doesNotEstablish: 'Treatment effect, efficacy, materialization, or analysis authority.',
  },
  {
    id: 'dataset-lock',
    label: 'Dataset-lock receipt',
    shortLabel: 'Lock',
    description: 'A separate accepted PASS receipt establishes the content-addressed Epoch 002 dataset lock.',
    predicateState: 'pass',
    toolingPrepared: true,
    toolingNote: 'The accepted receipt preserves separate unblinding and analysis authorization requirements.',
    evidenceBoundary: 'TRACK_A_EPOCH_002_DATASET_LOCK = ESTABLISHED at the accepted receipt identity.',
    doesNotEstablish: 'Unblinding, materialization, primary analysis, efficacy, or scientific-N promotion.',
  },
  {
    id: 'unblinding-decision',
    label: 'Separate unblinding decision',
    shortLabel: 'Unblind',
    description: 'A separate accepted human-controlled record authorizes bounded mapping release/decryption only.',
    predicateState: 'pass',
    toolingPrepared: true,
    toolingNote: 'Scope is CONTROLLED_MAPPING_RELEASE_OR_DECRYPTION_ONLY.',
    evidenceBoundary: 'Bounded unblinding is authorized; later materialization and analysis authorization remain separate accepted events.',
    doesNotEstablish: 'Materialization, primary-analysis authority, scientific-N promotion, independent validation, or a positive result by itself.',
  },
  {
    id: 'materialization',
    label: 'Controlled materialization + immutable receipt',
    shortLabel: 'Materialize',
    description: 'The real analysis-ready unblinded input was materialized under operator control, non-secret evidence was admitted, and a separate immutable receipt was accepted.',
    predicateState: 'pass',
    toolingPrepared: true,
    toolingNote: 'PR #824 admitted the non-secret materialization evidence; PR #826 established the creation-only MATERIALIZATION_RECEIPT.',
    evidenceBoundary: 'Epoch 002 materialization and its immutable repository receipt are ESTABLISHED at their accepted identities.',
    doesNotEstablish: 'Primary-analysis execution, efficacy, independent validation, or High-Assurance authorization.',
  },
  {
    id: 'primary-analysis-authorization',
    label: 'Primary-analysis authorization',
    shortLabel: 'Analysis auth',
    description: 'A separate human-controlled event authorizes exactly the locked confirmatory analysis and nothing broader.',
    predicateState: 'pass',
    toolingPrepared: true,
    toolingNote: 'PR #828 accepted the creation-only PRIMARY_ANALYSIS_AUTHORIZATION_RECORD with scope LOCKED_PRIMARY_ANALYSIS_ONLY.',
    evidenceBoundary: 'Bounded locked-primary-analysis authorization is ESTABLISHED; execution and result admission remain separate.',
    doesNotEstablish: 'Analysis execution, a positive result, efficacy, certification, or production readiness.',
  },
  {
    id: 'locked-analysis',
    label: 'Locked primary analysis + result receipt',
    shortLabel: 'Analyze',
    description: 'The preregistered Epoch 002 primary analysis executed locally under bounded authorization, and its content-addressed result receipt was accepted separately.',
    predicateState: 'pass',
    toolingPrepared: true,
    toolingNote: 'PR #851 established the creation-only LOCKED_ANALYSIS_RESULT_RECORD after local execution; the numerical output remains operator-local.',
    evidenceBoundary: 'Primary analysis is EXECUTED_LOCAL and LOCKED_ANALYSIS_RESULT_RECORD is ESTABLISHED at the accepted content address.',
    doesNotEstablish: 'Canonical DGAF efficacy, independent validation, or High-Assurance authorization; interpretation remains a separate stage.',
  },
  {
    id: 'interpretation-adjudication',
    label: 'Interpretation / adjudication',
    shortLabel: 'Interpret',
    description: 'Revalidate the retained operator-local locked-analysis output and derive only the frozen preregistered interpretation under the accepted claim ceiling.',
    predicateState: 'open',
    toolingPrepared: true,
    toolingNote: 'PR #855 accepted fail-closed interpretation tooling. No INTERPRETATION_NOTE has been admitted.',
    evidenceBoundary: 'INTERPRETATION_TOOLING = ACCEPTED; INTERPRETATION_EXECUTION = NOT RUN; INTERPRETATION_NOTE = NOT ESTABLISHED.',
    doesNotEstablish: 'Canonical DGAF efficacy, independent validation, production readiness, certification, High-Assurance authorization, or a scientific-N increment.',
  },
]

export const NEXT_TRANSITION = {
  title: 'Prepare and admit the bounded Epoch 002 interpretation',
  summary:
    'Use the accepted fail-closed interpretation preparer against the exact retained locked-analysis output outside the repository. It must revalidate the accepted result digest and frozen preregistration, write the numerical interpretation artifact externally, and prepare only a content-addressed INTERPRETATION_NOTE candidate for separate admission.',
  artifacts: [
    'Track A Epoch 002 local interpretation artifact (operator-controlled, external)',
    'local interpretation artifact SHA-256',
    'TRACK_A_EPOCH_002_INTERPRETATION_NOTE.json (separate creation-only repository event)',
  ],
  warning:
    'Do not copy the numerical estimate, interval, or classification into general repository projections. Do not pool historical epochs, relabel exploratory results, or treat the interpretation note as canonical DGAF efficacy, independent validation, or High-Assurance authorization.',
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
    state: 'open',
    summary:
      'Collection, dataset lock, bounded unblinding, materialization, primary-analysis authorization, local primary-analysis execution, and the content-addressed locked-result receipt are accepted; interpretation tooling is accepted but interpretation has not yet run.',
    facts: [
      'Collection: COMPLETE · 50 paired seed units / 2,250 blinded observations',
      'Custody: SAME_SYSTEM_NONINDEPENDENT',
      'Dataset lock: ESTABLISHED',
      'Bounded unblinding: AUTHORIZED',
      'Materialization + receipt: ESTABLISHED',
      'Primary-analysis authorization: ACCEPTED · LOCKED_PRIMARY_ANALYSIS_ONLY',
      'Primary analysis: EXECUTED_LOCAL',
      'Locked analysis result receipt: ESTABLISHED · PR #851',
      'Interpretation tooling: ACCEPTED · PR #855',
      'Interpretation note: NOT ESTABLISHED',
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
