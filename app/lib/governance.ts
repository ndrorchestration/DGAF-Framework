import type { UiState } from './types'

export const TRUTH_BOUNDARY = {
  programState: 'PRE-FREEZE',
  failMode: 'FAIL-CLOSED',
  authorization: 'NOT AUTHORIZED',
  empiricalN: 0,
  efficacy: 'NOT ESTABLISHED',
  sourceUpdated: '2026-09-18',
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
    label: 'Locked primary analysis',
    shortLabel: 'Analyze',
    description: 'Run the preregistered analysis locally against the retained content-addressed input under the accepted bounded authorization.',
    predicateState: 'open',
    toolingPrepared: true,
    toolingNote: 'PR #831 accepted the fail-closed local runner; PR #835 accepted content-addressed result-admission tooling. The real primary analysis has not yet run.',
    evidenceBoundary: 'Primary analysis is AUTHORIZED_BOUNDED / NOT RUN; no accepted LOCKED_ANALYSIS_RESULT_RECORD exists.',
    doesNotEstablish: 'Canonical DGAF efficacy, independent validation, or High-Assurance authorization without later result admission and interpretation.',
  },
]

export const NEXT_TRANSITION = {
  title: 'Execute the authorized locked Epoch 002 primary analysis',
  summary:
    'Use the accepted fail-closed local runner against the exact retained materialized input in the locked Python 3.12.0 / NumPy 2.5.1 environment, retain the output outside GitHub, then admit only its validated content address through the separate result-record event.',
  artifacts: [
    'track_a_epoch_002_locked_primary_analysis_output.json (operator-controlled)',
    'locked-analysis output SHA-256 sidecar',
    'TRACK_A_EPOCH_002_LOCKED_ANALYSIS_RESULT_RECORD.json (later separate repository event)',
  ],
  warning:
    'Authorization is bounded to the frozen confirmatory analysis. Do not substitute endpoints, pool historical epochs, expose protected material, or treat execution/result admission as canonical efficacy.',
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
      'Collection, dataset lock, bounded unblinding, real materialization, immutable materialization receipt, and bounded locked-analysis authorization are accepted; the primary analysis has not yet run.',
    facts: [
      'Collection: COMPLETE · 50 paired seed units / 2,250 blinded observations',
      'Custody: SAME_SYSTEM_NONINDEPENDENT',
      'Dataset lock: ESTABLISHED',
      'Bounded unblinding: AUTHORIZED',
      'Materialization + receipt: ESTABLISHED',
      'Primary-analysis authorization: ACCEPTED · LOCKED_PRIMARY_ANALYSIS_ONLY',
      'Primary analysis: AUTHORIZED_BOUNDED / NOT RUN',
      'Locked analysis result: NOT ESTABLISHED',
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
