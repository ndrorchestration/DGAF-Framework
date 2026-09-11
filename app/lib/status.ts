import type { StatusMeta, UiState } from './types'

export const STATUS_META: Record<UiState, StatusMeta> = {
  loading: {
    label: 'Loading',
    tone: 'neutral',
    description: 'Data is being requested. No positive or negative state is inferred yet.',
  },
  unknown: {
    label: 'Unknown',
    tone: 'neutral',
    description: 'The available evidence does not establish the state.',
  },
  unavailable: {
    label: 'Unavailable',
    tone: 'neutral',
    description: 'The requested data is not currently available.',
  },
  stale: {
    label: 'Stale',
    tone: 'warning',
    description: 'The last valid snapshot is retained, but a newer refresh did not succeed.',
  },
  info: {
    label: 'Information',
    tone: 'info',
    description: 'Informational state with no implied authorization or verification.',
  },
  open: {
    label: 'Open',
    tone: 'warning',
    description: 'The predicate or work item remains open.',
  },
  blocked: {
    label: 'Blocked',
    tone: 'warning',
    description: 'Progression is blocked by an unmet predecessor or prerequisite.',
  },
  pass: {
    label: 'Pass',
    tone: 'positive',
    description: 'The exact tested predicate passed in its stated scope.',
  },
  verified: {
    label: 'Verified',
    tone: 'violet',
    description: 'A defined verification predicate passed; scope does not widen automatically.',
  },
  not_authorized: {
    label: 'Not authorized',
    tone: 'danger',
    description: 'The named action remains prohibited even if tooling or capability exists.',
  },
  not_established: {
    label: 'Not established',
    tone: 'warning',
    description: 'Required evidence does not currently establish the predicate; this is not the same as disproven.',
  },
  failed: {
    label: 'Failed',
    tone: 'danger',
    description: 'The evaluated predicate or operation failed in its stated scope.',
  },
}

export function statusMeta(state: UiState): StatusMeta {
  return STATUS_META[state]
}

export function normalizeRuntimeStatus(value: unknown): UiState {
  if (typeof value !== 'string') return 'unknown'

  switch (value.trim().toLowerCase()) {
    case 'ok':
    case 'healthy':
    case 'active':
    case 'success':
    case 'pass':
      return 'pass'
    case 'verified':
      return 'verified'
    case 'partial':
    case 'open':
    case 'pending':
      return 'open'
    case 'foundational':
    case 'info':
      return 'info'
    case 'blocked':
      return 'blocked'
    case 'not authorized':
    case 'not_authorized':
      return 'not_authorized'
    case 'not established':
    case 'not_established':
      return 'not_established'
    case 'failed':
    case 'failure':
    case 'error':
      return 'failed'
    case 'unavailable':
      return 'unavailable'
    case 'stale':
      return 'stale'
    case 'loading':
      return 'loading'
    default:
      return 'unknown'
  }
}
