import { createHash, createHmac, randomUUID } from 'node:crypto'

import {
  AUDIT_ACTION_CLASS,
  AUDIT_POLICY_ID,
  AUDIT_REQUIRED_SCOPE,
  AUDIT_TARGET,
  canonicalActionDigest,
  type ActionAdmissionRecord,
} from './action-admission.ts'

export const TEKTITE_DEMO_SCENARIOS = [
  'authorized',
  'revoked',
  'missing_scope',
  'tampered_action',
  'replay',
] as const

export type TektiteDemoScenario = (typeof TEKTITE_DEMO_SCENARIOS)[number]

export type TektiteDemoRequest = {
  scenario: TektiteDemoScenario
  requestBody: Record<string, unknown>
  safeRecord: Omit<ActionAdmissionRecord, 'attestation'> & { attestation_fingerprint: string }
}

function canonicalize(value: unknown): unknown {
  if (Array.isArray(value)) return value.map(canonicalize)
  if (value && typeof value === 'object') {
    return Object.fromEntries(
      Object.entries(value as Record<string, unknown>)
        .sort(([a], [b]) => a.localeCompare(b))
        .map(([key, item]) => [key, canonicalize(item)]),
    )
  }
  return value
}

export function isTektiteDemoScenario(value: unknown): value is TektiteDemoScenario {
  return typeof value === 'string' && TEKTITE_DEMO_SCENARIOS.includes(value as TektiteDemoScenario)
}

export function createTektiteDemoRequest(
  scenario: TektiteDemoScenario,
  options: { nowMs?: number; trustKey?: string; recordId?: string } = {},
): TektiteDemoRequest {
  const nowMs = options.nowMs ?? Date.now()
  const trustKey = options.trustKey ?? process.env.DGAF_AAR_HMAC_KEY
  if (!trustKey) throw new Error('TEKTITE_DEMO_TRUST_ANCHOR_UNAVAILABLE')

  const recordId = options.recordId ?? `tektite-demo-${randomUUID()}`
  const authorizationId = `tektite-demo-auth-${recordId}`
  const digestParameters = { turn_count: 1, stable_turns: 1 }
  const requestParameters =
    scenario === 'tampered_action'
      ? { turn_count: 2, stable_turns: 1 }
      : digestParameters

  const unsignedRecord: Omit<ActionAdmissionRecord, 'attestation'> = {
    version: 'AAR_V1',
    record_id: recordId,
    action_class: AUDIT_ACTION_CLASS,
    target: AUDIT_TARGET,
    policy_id: AUDIT_POLICY_ID,
    action_digest: canonicalActionDigest(digestParameters, authorizationId),
    authorization: {
      authorization_id: authorizationId,
      parent_scope: [AUDIT_REQUIRED_SCOPE],
      delegated_scope: scenario === 'missing_scope' ? [] : [AUDIT_REQUIRED_SCOPE],
      expires_at: new Date(nowMs + 5 * 60_000).toISOString(),
      revoked: scenario === 'revoked',
    },
    predicates: {
      verifier_status: 'PASS',
    },
  }

  const attestation = createHmac('sha256', trustKey)
    .update(JSON.stringify(canonicalize(unsignedRecord)))
    .digest('hex')

  const safeRecord = {
    ...unsignedRecord,
    attestation_fingerprint: createHash('sha256').update(attestation).digest('hex').slice(0, 16),
  }

  return {
    scenario,
    requestBody: {
      ...requestParameters,
      aar: {
        ...unsignedRecord,
        attestation,
      },
    },
    safeRecord,
  }
}