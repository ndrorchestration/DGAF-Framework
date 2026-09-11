export type UiState =
  | 'loading'
  | 'unknown'
  | 'unavailable'
  | 'stale'
  | 'info'
  | 'open'
  | 'blocked'
  | 'pass'
  | 'verified'
  | 'not_authorized'
  | 'not_established'
  | 'failed'

export type StatusTone = 'neutral' | 'info' | 'positive' | 'warning' | 'danger' | 'violet'

export interface StatusMeta {
  label: string
  tone: StatusTone
  description: string
}

export interface HealthData {
  status: string
  version: string
  psi_cubic: boolean
  psi_cubic_error?: number
  phi_star: number
  psi: number
  runtime: string
  scpe_threshold: number
  phi_checkpoints: number[]
  adapters: string[]
}

export interface AuditData {
  status: string
  version: string
  turn_count: number
  stable_turns: number
  prune_events: number
  axiom_count: number
  consec_phi_fail: number
  cold_start: boolean
  cold_start_at: string
  _warning: string | null
  runtime?: string
}

export interface Agent {
  id: string
  tier: string
  role: string
  status: string
  triad_roles: string[]
}

export interface Triad {
  id: string
  type: string
  agents: string[]
  use_case: string
}

export interface RosterData {
  version: string
  agent_count: number
  triad_count: number
  ndr_patterns: number
  agents: Agent[]
  triads: Triad[]
  phi_star: number
  psi: number
  rosterSource?: string
  rosterFormat?: string
}

export interface SweepFinding {
  id: string
  agent: string
  target: string
  severity: string
  message: string
  patternId?: string
  scanner?: string
  kind?: string
  remediationCandidate?: string
}

export interface SweepResult {
  sweep_id: string
  targets_scanned: number
  findings_count: number
  findings: SweepFinding[]
  narrative: string
  harmonic_score: number | null
  harmonic_score_status?: string
  swept_at: string
  mutation_performed?: boolean
  remediation_candidates?: unknown[]
}

export interface DashboardSnapshot {
  health: HealthData
  audit: AuditData
  roster: RosterData
}
