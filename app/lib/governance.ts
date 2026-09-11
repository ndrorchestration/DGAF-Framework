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

export const GOVERNANCE_STAGES: GovernanceStage[] = [
  {
    id: 'repository-custody',
    label: 'Repository custody acceptance',
    shortLabel: 'Custody',
    description: 'Admit the exact existing non-secret successor custody certificate and recovery receipt.',
    predicateState: 'not_established',
    toolingPrepared: false,
  },
  {
    id: 'precollection-preflight',
    label: 'Precollection preflight',
    shortLabel: 'Preflight',
    description: 'Verify the successor collection prerequisites against accepted predecessor evidence.',
    predicateState: 'blocked',
    toolingPrepared: true,
    toolingNote: 'Prospective preflight tooling has been repository-validated; the predicate remains predecessor-blocked.',
  },
  {
    id: 'immutable-freeze',
    label: 'Immutable freeze',
    shortLabel: 'Freeze',
    description: 'Bind the exact experimental candidate immutably after predecessor closure.',
    predicateState: 'blocked',
    toolingPrepared: true,
    toolingNote: 'Freeze tooling is prepared; no successor freeze is established.',
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
  title: 'Stage exact successor custody evidence',
  evidence:
    'Operator-local custody-v2 recovery passed at PASS_CURRENT_V2 / STRUCTURAL_SELF_ATTESTED_ONLY / NONINDEPENDENT.',
  blocker: 'Repository custody acceptance is NOT ESTABLISHED.',
  summary:
    'On the clean dedicated evidence branch based exactly on current accepted main, run the fail-closed admission helper to stage only the exact existing public certificate and non-secret schema-v2 recovery receipt, then verify the staged path list before creating the evidence commit.',
  artifacts: [
    'docs/experiment/track_a_runs/TRACK_A_SUCCESSOR_CUSTODY_CERT.pem',
    'docs/experiment/track_a_runs/TRACK_A_SUCCESSOR_SOLO_CUSTODY_RECOVERY_RECEIPT.json',
  ],
  operatorBranch: 'track-a-successor-custody-evidence-v2',
  operatorCommand: 'py -3 scripts/prepare_track_a_successor_custody_admission.py',
  operatorVerification: 'git diff --cached --name-only',
  warning:
    'Do not regenerate, substitute, or reconstruct custody evidence. The helper stages only; it does not commit, push, freeze, authorize collection, or change scientific N.',
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
      'Operator-local custody-v2 recovery passed at a self-attested, non-independent level; repository custody is not established and empirical collection remains unauthorized.',
    facts: [
      'Local custody recovery: PASS_CURRENT_V2 / STRUCTURAL_SELF_ATTESTED_ONLY / NONINDEPENDENT',
      'Repository custody: NOT ESTABLISHED',
      'Empirical collection: NOT AUTHORIZED / NOT EXECUTED',
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
