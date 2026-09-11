import type {
  Agent,
  AuditData,
  DashboardSnapshot,
  HealthData,
  RosterData,
  SweepFinding,
  SweepResult,
  Triad,
} from './types'

function isRecord(value: unknown): value is Record<string, unknown> {
  return typeof value === 'object' && value !== null && !Array.isArray(value)
}

function isStringArray(value: unknown): value is string[] {
  return Array.isArray(value) && value.every(item => typeof item === 'string')
}

function fail(contract: string): never {
  throw new Error(`Invalid ${contract} API response`)
}

function isAgent(value: unknown): value is Agent {
  if (!isRecord(value)) return false
  return (
    typeof value.id === 'string' &&
    typeof value.tier === 'string' &&
    typeof value.role === 'string' &&
    typeof value.status === 'string' &&
    isStringArray(value.triad_roles)
  )
}

function isTriad(value: unknown): value is Triad {
  if (!isRecord(value)) return false
  return (
    typeof value.id === 'string' &&
    typeof value.type === 'string' &&
    isStringArray(value.agents) &&
    typeof value.use_case === 'string'
  )
}

function isSweepFinding(value: unknown): value is SweepFinding {
  if (!isRecord(value)) return false
  return (
    typeof value.id === 'string' &&
    typeof value.agent === 'string' &&
    typeof value.target === 'string' &&
    typeof value.severity === 'string' &&
    typeof value.message === 'string'
  )
}

export function validateHealthData(value: unknown): HealthData {
  if (!isRecord(value)) fail('health')
  if (
    typeof value.status !== 'string' ||
    typeof value.version !== 'string' ||
    typeof value.psi_cubic !== 'boolean' ||
    typeof value.phi_star !== 'number' ||
    typeof value.psi !== 'number' ||
    typeof value.runtime !== 'string' ||
    typeof value.scpe_threshold !== 'number' ||
    !Array.isArray(value.phi_checkpoints) ||
    !value.phi_checkpoints.every(item => typeof item === 'number') ||
    !isStringArray(value.adapters)
  ) {
    fail('health')
  }
  return value as unknown as HealthData
}

export function validateAuditData(value: unknown): AuditData {
  if (!isRecord(value)) fail('audit')
  if (
    typeof value.status !== 'string' ||
    typeof value.version !== 'string' ||
    typeof value.turn_count !== 'number' ||
    typeof value.stable_turns !== 'number' ||
    typeof value.prune_events !== 'number' ||
    typeof value.axiom_count !== 'number' ||
    typeof value.consec_phi_fail !== 'number' ||
    typeof value.cold_start !== 'boolean' ||
    typeof value.cold_start_at !== 'string' ||
    !(typeof value._warning === 'string' || value._warning === null)
  ) {
    fail('audit')
  }
  return value as unknown as AuditData
}

export function validateRosterData(value: unknown): RosterData {
  if (!isRecord(value)) fail('roster')
  if (
    typeof value.version !== 'string' ||
    typeof value.agent_count !== 'number' ||
    typeof value.triad_count !== 'number' ||
    typeof value.ndr_patterns !== 'number' ||
    !Array.isArray(value.agents) ||
    !value.agents.every(isAgent) ||
    !Array.isArray(value.triads) ||
    !value.triads.every(isTriad) ||
    typeof value.phi_star !== 'number' ||
    typeof value.psi !== 'number'
  ) {
    fail('roster')
  }
  return value as unknown as RosterData
}

export function validateSweepResult(value: unknown): SweepResult {
  if (!isRecord(value)) fail('sweep')
  if (
    typeof value.sweep_id !== 'string' ||
    typeof value.targets_scanned !== 'number' ||
    typeof value.findings_count !== 'number' ||
    !Array.isArray(value.findings) ||
    !value.findings.every(isSweepFinding) ||
    typeof value.narrative !== 'string' ||
    !(typeof value.harmonic_score === 'number' || value.harmonic_score === null) ||
    typeof value.swept_at !== 'string'
  ) {
    fail('sweep')
  }
  if (
    value.harmonic_score === null &&
    value.harmonic_score_status !== undefined &&
    value.harmonic_score_status !== 'NOT_COMPUTED'
  ) {
    fail('sweep')
  }
  if (value.mutation_performed !== undefined && typeof value.mutation_performed !== 'boolean') {
    fail('sweep')
  }
  return value as unknown as SweepResult
}

async function readJson(response: Response, contract: string): Promise<unknown> {
  if (!response.ok) {
    throw new Error(`${contract} request failed with HTTP ${response.status}`)
  }
  try {
    return await response.json()
  } catch {
    throw new Error(`${contract} response was not valid JSON`)
  }
}

export async function fetchDashboardSnapshot(signal?: AbortSignal): Promise<DashboardSnapshot> {
  const options: RequestInit = { signal, cache: 'no-store' }
  const [healthResponse, auditResponse, rosterResponse] = await Promise.all([
    fetch('/api/health', options),
    fetch('/api/audit', options),
    fetch('/api/roster', options),
  ])

  const [healthRaw, auditRaw, rosterRaw] = await Promise.all([
    readJson(healthResponse, 'health'),
    readJson(auditResponse, 'audit'),
    readJson(rosterResponse, 'roster'),
  ])

  return {
    health: validateHealthData(healthRaw),
    audit: validateAuditData(auditRaw),
    roster: validateRosterData(rosterRaw),
  }
}

export async function runSweep(targets: string[], signal?: AbortSignal): Promise<SweepResult> {
  const response = await fetch('/api/sweep', {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ targets }),
    signal,
  })
  return validateSweepResult(await readJson(response, 'sweep'))
}
