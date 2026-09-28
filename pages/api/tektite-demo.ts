import type { NextApiRequest, NextApiResponse } from 'next'

import { isTektiteDemoScenario, createTektiteDemoRequest } from '../../app/lib/tektite-demo'

type DemoAttempt = {
  attempt: number
  http_status: number
  result: unknown
}

function requestOrigin(req: NextApiRequest): string {
  const protocol = String(req.headers['x-forwarded-proto'] ?? 'http').split(',')[0].trim()
  const host = String(req.headers['x-forwarded-host'] ?? req.headers.host ?? '').split(',')[0].trim()
  if (!host) throw new Error('TEKTITE_DEMO_HOST_UNAVAILABLE')
  return `${protocol}://${host}`
}

export default async function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    res.setHeader('Allow', 'POST')
    return res.status(405).json({ status: 'method_not_allowed' })
  }

  if (process.env.TEKTITE_DEMO_ENABLED !== 'true') {
    return res.status(503).json({
      status: 'blocked',
      reason: 'TEKTITE_DEMO_NOT_ENABLED',
      boundary: 'FAIL_CLOSED_DEMO_DISABLED',
    })
  }

  const internalToken = process.env.TEKTITE_DEMO_INTERNAL_TOKEN
  if (!internalToken) {
    return res.status(503).json({
      status: 'blocked',
      reason: 'TEKTITE_DEMO_INTERNAL_TOKEN_UNAVAILABLE',
      boundary: 'FAIL_CLOSED_NO_DEMO_ISSUANCE',
    })
  }

  const scenario = req.body?.scenario
  if (!isTektiteDemoScenario(scenario)) {
    return res.status(400).json({
      status: 'invalid_scenario',
      allowed: ['authorized', 'revoked', 'missing_scope', 'tampered_action', 'replay'],
    })
  }

  let demo
  try {
    demo = createTektiteDemoRequest(scenario)
  } catch (error) {
    return res.status(503).json({
      status: 'blocked',
      reason: error instanceof Error ? error.message : 'TEKTITE_DEMO_SETUP_FAILED',
      boundary: 'FAIL_CLOSED_NO_DEMO_ISSUANCE',
    })
  }

  const origin = requestOrigin(req)
  const attempts: DemoAttempt[] = []
  const count = scenario === 'replay' ? 2 : 1

  for (let attempt = 1; attempt <= count; attempt += 1) {
    const response = await fetch(`${origin}/api/audit`, {
      method: 'POST',
      headers: {
        'content-type': 'application/json',
        'x-tektite-demo-token': internalToken,
        ...(typeof req.headers['x-vercel-protection-bypass'] === 'string'
          ? { 'x-vercel-protection-bypass': req.headers['x-vercel-protection-bypass'] }
          : {}),
      },
      body: JSON.stringify(demo.requestBody),
    })
    let result: unknown
    try {
      result = await response.json()
    } catch {
      result = { status: 'invalid_json_response' }
    }
    attempts.push({ attempt, http_status: response.status, result })
  }

  return res.status(200).json({
    version: 'TEKTITE_DGAF_PROOF_V1',
    scenario,
    action: {
      action_class: demo.safeRecord.action_class,
      target: demo.safeRecord.target,
      policy_id: demo.safeRecord.policy_id,
      parameters: Object.fromEntries(Object.entries(demo.requestBody).filter(([key]) => key !== 'aar')),
    },
    authority: {
      authorization_id: demo.safeRecord.authorization.authorization_id,
      parent_scope: demo.safeRecord.authorization.parent_scope,
      delegated_scope: demo.safeRecord.authorization.delegated_scope,
      expires_at: demo.safeRecord.authorization.expires_at,
      revoked: demo.safeRecord.authorization.revoked,
      verifier_status: demo.safeRecord.predicates.verifier_status,
      attestation_fingerprint: demo.safeRecord.attestation_fingerprint,
      issuer_class: 'SAME_SYSTEM_DEMONSTRATION_FIXTURE',
    },
    attempts,
    claim_boundary: {
      scientific_n_increment: 0,
      independent_validation: 'NOT_ESTABLISHED',
      canonical_dgaf_efficacy: 'NOT_ESTABLISHED',
      high_assurance: 'NOT_AUTHORIZED',
      demo_effect: 'NON_SCIENTIFIC_EPHEMERAL_AUDIT_COUNTER_UPDATE_ONLY',
    },
  })
}