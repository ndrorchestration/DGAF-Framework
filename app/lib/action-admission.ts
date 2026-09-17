import { createHash, createHmac, timingSafeEqual } from 'node:crypto'

export const AUDIT_ACTION_CLASS = 'AUDIT_COUNTER_UPDATE_V1' as const
export const AUDIT_TARGET = '/api/audit' as const
export const AUDIT_POLICY_ID = 'AAR_AUDIT_POLICY_V1' as const
export const AUDIT_REQUIRED_SCOPE = 'audit:counter:update' as const
export const AUDIT_COUNTER_FIELDS = [
  'turn_count',
  'stable_turns',
  'prune_events',
  'axiom_count',
  'consec_phi_fail',
] as const

export type AuditCounterField = (typeof AUDIT_COUNTER_FIELDS)[number]

export type ActionAdmissionRecord = {
  version: 'AAR_V1'
  record_id: string
  action_class: typeof AUDIT_ACTION_CLASS
  target: typeof AUDIT_TARGET
  policy_id: typeof AUDIT_POLICY_ID
  action_digest: string
  authorization: {
    authorization_id: string
    parent_scope: string[]
    delegated_scope: string[]
    expires_at: string
    revoked: boolean
  }
  predicates: {
    verifier_status: 'PASS' | 'UNKNOWN' | 'FAIL'
  }
  attestation: string
}

export type AuditAdmissionSuccess = {
  ok: true
  record: ActionAdmissionRecord
  parameters: Partial<Record<AuditCounterField, number>>
}

export type AuditAdmissionFailure = {
  ok: false
  reason: string
}

export type AuditAdmissionResult = AuditAdmissionSuccess | AuditAdmissionFailure

const usedRecordIds = new Set<string>()

function isRecord(value: unknown): value is Record<string, unknown> {
  return Boolean(value) && typeof value === 'object' && !Array.isArray(value)
}

function canonicalize(value: unknown): unknown {
  if (Array.isArray(value)) return value.map(canonicalize)
  if (isRecord(value)) {
    return Object.fromEntries(
      Object.entries(value)
        .sort(([a], [b]) => a.localeCompare(b))
        .map(([key, item]) => [key, canonicalize(item)]),
    )
  }
  return value
}

export function canonicalActionDigest(
  parameters: Record<string, unknown>,
  authorizationId: string,
): string {
  const payload = canonicalize({
    action_class: AUDIT_ACTION_CLASS,
    authorization_id: authorizationId,
    parameters,
    policy_id: AUDIT_POLICY_ID,
    target: AUDIT_TARGET,
  })
  return createHash('sha256').update(JSON.stringify(payload)).digest('hex')
}

function secureDigestEqual(actual: string, expected: string): boolean {
  if (!/^[a-f0-9]{64}$/.test(actual) || !/^[a-f0-9]{64}$/.test(expected)) return false
  return timingSafeEqual(Buffer.from(actual, 'hex'), Buffer.from(expected, 'hex'))
}

function stringArray(value: unknown): value is string[] {
  return Array.isArray(value) && value.every((item) => typeof item === 'string')
}

function parseAar(value: unknown): ActionAdmissionRecord | null {
  if (!isRecord(value)) return null
  if (value.version !== 'AAR_V1') return null
  if (typeof value.record_id !== 'string' || value.record_id.length === 0) return null
  if (value.action_class !== AUDIT_ACTION_CLASS) return null
  if (value.target !== AUDIT_TARGET) return null
  if (value.policy_id !== AUDIT_POLICY_ID) return null
  if (typeof value.action_digest !== 'string') return null
  if (typeof value.attestation !== 'string') return null
  if (!isRecord(value.authorization) || !isRecord(value.predicates)) return null

  const authorization = value.authorization
  const predicates = value.predicates
  if (typeof authorization.authorization_id !== 'string' || authorization.authorization_id.length === 0) return null
  if (!stringArray(authorization.parent_scope) || !stringArray(authorization.delegated_scope)) return null
  if (typeof authorization.expires_at !== 'string') return null
  if (typeof authorization.revoked !== 'boolean') return null
  if (!['PASS', 'UNKNOWN', 'FAIL'].includes(String(predicates.verifier_status))) return null

  return value as ActionAdmissionRecord
}

function extractParameters(body: Record<string, unknown>): Record<string, unknown> | null {
  const parameters = Object.fromEntries(Object.entries(body).filter(([key]) => key !== 'aar'))
  const keys = Object.keys(parameters)
  if (keys.length === 0) return null
  if (keys.some((key) => !AUDIT_COUNTER_FIELDS.includes(key as AuditCounterField))) return null
  if (Object.values(parameters).some((value) => typeof value !== 'number' || !Number.isFinite(value))) return null
  return parameters
}

function verifyAttestation(record: ActionAdmissionRecord): AuditAdmissionFailure | null {
  const trustKey = process.env.DGAF_AAR_HMAC_KEY
  if (!trustKey) return { ok: false, reason: 'TRUST_ANCHOR_UNAVAILABLE' }

  const { attestation, ...unsignedRecord } = record
  const expected = createHmac('sha256', trustKey)
    .update(JSON.stringify(canonicalize(unsignedRecord)))
    .digest('hex')
  if (!secureDigestEqual(attestation, expected)) return { ok: false, reason: 'AAR_ATTESTATION_INVALID' }
  return null
}

export function validateAuditAdmission(body: unknown, nowMs = Date.now()): AuditAdmissionResult {
  if (!isRecord(body)) return { ok: false, reason: 'INVALID_REQUEST' }
  const record = parseAar(body.aar)
  if (!record) return { ok: false, reason: 'AAR_REQUIRED_OR_MALFORMED' }
  if (usedRecordIds.has(record.record_id)) return { ok: false, reason: 'AAR_REPLAY' }

  const attestationFailure = verifyAttestation(record)
  if (attestationFailure) return attestationFailure

  const parameters = extractParameters(body)
  if (!parameters) return { ok: false, reason: 'ACTION_PARAMETERS_NOT_REGISTERED' }

  const { authorization } = record
  if (authorization.revoked) return { ok: false, reason: 'AUTHORIZATION_REVOKED' }
  const expiresAt = Date.parse(authorization.expires_at)
  if (!Number.isFinite(expiresAt) || expiresAt <= nowMs) return { ok: false, reason: 'AUTHORIZATION_EXPIRED' }
  if (!authorization.delegated_scope.every((scope) => authorization.parent_scope.includes(scope))) {
    return { ok: false, reason: 'DELEGATION_WIDENED' }
  }
  if (!authorization.delegated_scope.includes(AUDIT_REQUIRED_SCOPE)) {
    return { ok: false, reason: 'REQUIRED_SCOPE_MISSING' }
  }
  if (record.predicates.verifier_status !== 'PASS') return { ok: false, reason: 'VERIFIER_NOT_PASS' }

  const expectedDigest = canonicalActionDigest(parameters, authorization.authorization_id)
  if (!secureDigestEqual(record.action_digest, expectedDigest)) return { ok: false, reason: 'ACTION_DIGEST_MISMATCH' }

  return {
    ok: true,
    record,
    parameters: parameters as Partial<Record<AuditCounterField, number>>,
  }
}

export function consumeAuditAdmission(recordId: string): boolean {
  if (usedRecordIds.has(recordId)) return false
  usedRecordIds.add(recordId)
  return true
}
