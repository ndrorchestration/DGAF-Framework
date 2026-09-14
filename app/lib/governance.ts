import type { UiState } from './types'

export const TRUTH_BOUNDARY = {
  programState: 'PRE-FREEZE',
  failMode: 'FAIL-CLOSED',
  authorization: 'NOT AUTHORIZED',
  empiricalN: 0,
  efficacy: 'NOT ESTABLISHED',
  sourceUpdated: '2026-09-14',
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
    evidenceBoundary: 'Collection completion is reported for the authorized Epoch 002 execution.',
    doesNotEstablish: 'Repository admission of retained bytes, dataset lock, canonical N promotion, or efficacy.',
  },
  {
    id: 'operator-evidence-admission',
    label: 'Operator evidence admission',
    shortLabel: 'Admit evidence',
    description: 'Validate and admit the exact operator-retained public and encrypted-protected archive bytes.',
    predicateState: 'not_established',
    toolingPrepared: true,
    toolingNote: 'PRs #687–#689 provide the accepted dry-run-first OPERATOR_CODESPACE preparation path.',
    evidenceBoundary: 'The tooling is accepted; no retained-byte PASS or canonical evidence-admission event exists yet.',
    doesNotEstablish: 'That retained evidence passed, that dataset lock exists, or that any downstream action is authorized.',
  },
  {
    id: 'quality-control',
    label: 'Pre-lock structural quality control',
    shortLabel: 'QC',
    description: 'Produce and validate the bounded 53-record blinded pre-lock ledger.',
    predicateState: 'blocked',
    toolingPrepared: true,
    toolingNote: 'PR #688 provides the accepted non-authorizing ledger preparer.',
    evidenceBoundary: 'QC remains predecessor-blocked until operator retained-byte admission succeeds.',
    doesNotEstablish: 'Outcome comparison, treatment effect, efficacy, unblinding, or analysis authority.',
  },
  {
    id: 'dataset-lock',
    label: 'Dataset-lock receipt',
    shortLabel: 'Lock',
    description: 'Create a separate exact one-parent, one-file receipt after accepted evidence admission and PASS QC.',
    predicateState: 'not_established',
    toolingPrepared: true,
    toolingNote: 'PR #689 adds truthful OPERATOR_CODESPACE evidence support; the receipt remains a later event.',
    evidenceBoundary: 'No accepted Epoch 002 DATASET_LOCK_RECEIPT exists.',
    doesNotEstablish: 'Unblinding, materialization, primary analysis, efficacy, or scientific-N promotion.',
  },
  {
    id: 'unblinding-decision',
    label: 'Separate unblinding decision',
    shortLabel: 'Unblind',
    description: 'A separate human-controlled decision must govern any bounded treatment-identity release.',
    predicateState: 'not_authorized',
    toolingPrepared: true,
    toolingNote: 'Validation tooling exists; tooling readiness is not an authorization event.',
    evidenceBoundary: 'No accepted unblinding decision exists.',
    doesNotEstablish: 'Materialization, primary-analysis authority, or a positive result.',
  },
  {
    id: 'materialization',
    label: 'Controlled materialization + immutable receipt',
    shortLabel: 'Materialize',
    description: 'Construct analysis-ready unblinded input only after bounded unblinding authorization.',
    predicateState: 'not_established',
    toolingPrepared: false,
    evidenceBoundary: 'No accepted Epoch 002 materialization event exists.',
    doesNotEstablish: 'Primary-analysis authority, efficacy, or High-Assurance authorization.',
  },
  {
    id: 'primary-analysis-authorization',
    label: 'Primary-analysis authorization',
    shortLabel: 'Analysis auth',
    description: 'A separate decision must authorize the locked confirmatory analysis and nothing broader.',
    predicateState: 'not_authorized',
    toolingPrepared: false,
    evidenceBoundary: 'No accepted primary-analysis authorization exists.',
    doesNotEstablish: 'A positive result, efficacy, certification, or production readiness.',
  },
  {
    id: 'locked-analysis',
    label: 'Locked primary analysis',
    shortLabel: 'Analyze',
    description: 'Run the preregistered analysis only after every predecessor is accepted.',
    predicateState: 'not_authorized',
    toolingPrepared: false,
    evidenceBoundary: 'Primary analysis is NOT AUTHORIZED / NOT RUN.',
    doesNotEstablish: 'Canonical DGAF efficacy unless the exact analysis and later adjudication support that claim.',
  },
]

export const NEXT_TRANSITION = {
  title: 'Validate and admit the exact operator-retained evidence',
  summary:
    'Run the accepted #687–#689 preparers in the original operator-controlled Codespace against the exact retained public and encrypted-protected archives, then admit only the bounded non-secret outputs.',
  artifacts: [
    'track_a_epoch_002_operator_execution_receipt.json',
    'track_a_epoch_002_operator_collection_admission.json',
    'TRACK_A_EPOCH_002_PRE_LOCK_RESULT_LEDGER.json',
    'TRACK_A_EPOCH_002_DATASET_LOCK_EVIDENCE.json',
  ],
  warning:
    'Do not rerun collection, decrypt protected material, aggregate outcomes, or invent GitHub Actions identities.',
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
      'The separately authorized operator collection completed; exact retained-byte admission and the later dataset-lock receipt remain open.',
    facts: [
      'Collection: COMPLETE · 50 paired seed units / 2,250 blinded observations',
      'Custody: SAME_SYSTEM_NONINDEPENDENT',
      'Operator retained-byte admission: PENDING',
      'Dataset lock: NOT ESTABLISHED',
      'Unblinding and primary analysis: NOT AUTHORIZED',
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
