// pages/api/orchestrate.ts — Pages Router API
import type { NextApiRequest, NextApiResponse } from 'next'
import { evidenceEnvelope } from '../../lib/evidence'

const PSI = 1.4655712318767682
const PHI = (1 + Math.sqrt(5)) / 2
const PHI_STAR = PHI - 1
const FIB = [13, 21, 34, 55]

type TraceEntry = Record<string, unknown>

type ResponseBody = Record<string, unknown>

function snapToPhiLattice(confidence: number): number {
  const octave = 1 + confidence
  const lattice = [1, PHI_STAR + 1, PHI]
  let nearest = lattice[0]
  for (const point of lattice) {
    if (Math.abs(point - octave) < Math.abs(nearest - octave)) nearest = point
  }
  return nearest - 1
}

function reject(res: NextApiResponse<ResponseBody>, reason: string, evidenceStatus: 'PASS' | 'BLOCKED' = 'PASS') {
  return res.status(400).json({
    decision: 'REJECT',
    reason,
    evidence: evidenceEnvelope({
      mode: 'integration',
      status: evidenceStatus,
      claim_id: 'dgaf-runtime-governance',
    }),
  })
}

export default function handler(req: NextApiRequest, res: NextApiResponse<ResponseBody>) {
  if (req.method !== 'POST') {
    return res.status(405).json({
      error: 'Method not allowed',
      evidence: evidenceEnvelope({
        mode: 'integration',
        status: 'NOT_IMPLEMENTED',
        claim_id: 'dgaf-runtime-governance',
      }),
    })
  }

  const body = req.body
  if (body == null || typeof body !== 'object' || Array.isArray(body)) {
    return reject(res, 'request body must be a JSON object')
  }

  const payload = typeof body.payload === 'string' ? body.payload : ''
  const claim = typeof body.claim === 'string' ? body.claim : ''
  const turn = Number.isInteger(body.turn) ? Number(body.turn) : 1
  const confidence = typeof body.confidence === 'number' ? Number(body.confidence) : 0.5

  if (!Number.isFinite(confidence) || confidence < 0 || confidence > 1) {
    return reject(res, 'confidence must be a finite number in [0,1]')
  }

  if (!Number.isInteger(turn) || turn < 1) {
    return reject(res, 'turn must be a positive integer')
  }

  const trace: TraceEntry[] = []
  const normalizedPayload = payload.toLowerCase()

  for (const marker of ['ignore previous', 'disregard', 'jailbreak']) {
    if (normalizedPayload.includes(marker)) {
      trace.push({ gate: 'DemiJoule', decision: 'KILL', reason: `blocked: ${marker}` })
      return res.status(400).json({
        decision: 'KILL',
        reason: `blocked: ${marker}`,
        turn,
        trace,
        evidence: evidenceEnvelope({
          mode: 'integration',
          status: 'PASS',
          claim_id: 'dgaf-runtime-governance',
        }),
      })
    }
  }
  trace.push({ gate: 'DemiJoule', decision: 'PASS' })

  // Phi-Closure requires live audit state. Until that state is actually wired,
  // checkpoint execution must fail closed rather than manufacture a PASS.
  if (FIB.includes(turn)) {
    trace.push({
      gate: 'Phi-Closure',
      decision: 'BLOCKED',
      reason: 'live audit state is not wired into /api/orchestrate',
    })
    return res.status(503).json({
      decision: 'BLOCKED',
      reason: 'Phi-Closure checkpoint requires live audit state; execution is fail-closed until wired',
      turn,
      trace,
      evidence: evidenceEnvelope({
        mode: 'integration',
        status: 'BLOCKED',
        claim_id: 'dgaf-runtime-governance',
      }),
    })
  }

  const effectiveConfidence = snapToPhiLattice(confidence)
  const psiCubicCheck = Math.abs(PSI ** 3 - (PSI ** 2 + 1)) < 1e-10
  trace.push({ gate: 'Phi-Closure', decision: 'SKIP', reason: 'non-checkpoint turn' })
  trace.push({ gate: 'HPG', decision: 'PASS', effective_confidence: effectiveConfidence })
  trace.push({ gate: 'PSI-Identity', decision: psiCubicCheck ? 'PASS' : 'FAIL' })

  return res.status(200).json({
    decision: 'PASS',
    turn,
    raw_confidence: confidence,
    effective_confidence: Math.round(effectiveConfidence * 1e6) / 1e6,
    hpg_fired: true,
    phi_gate: 'SKIP',
    phi_delta: null,
    psi_cubic_check: psiCubicCheck,
    claim_received: claim,
    payload_len: payload.length,
    trace,
    evidence: evidenceEnvelope({
      mode: 'integration',
      status: 'PARTIAL',
      claim_id: 'dgaf-runtime-governance',
    }),
  })
}
