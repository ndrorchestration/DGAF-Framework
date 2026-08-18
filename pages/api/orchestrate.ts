// pages/api/orchestrate.ts — Pages Router API
import type { NextApiRequest, NextApiResponse } from 'next'
import { evidenceEnvelope } from '../../lib/evidence'

const PSI      = 1.4655712318767682
const PHI      = (1 + Math.sqrt(5)) / 2
const PHI_STAR = PHI - 1
const FIB      = [13, 21, 34, 55]
const PHI_TOL  = 0.05

function snapToPhiLattice(c: number): number {
  const octave  = 1 + c
  const lattice = [1, PHI_STAR + 1, PHI]
  let nearest   = lattice[0]
  for (const pt of lattice) {
    if (Math.abs(pt - octave) < Math.abs(nearest - octave)) nearest = pt
  }
  return nearest - 1
}

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({
      error: 'Method not allowed',
      evidence: evidenceEnvelope({ mode: 'integration', status: 'NOT_IMPLEMENTED', claim_id: 'dgaf-runtime-governance' }),
    })
  }

  const { payload = '', confidence = 0.5, claim = '', turn = 1 } = req.body ?? {}
  const trace: Array<Record<string, unknown>> = []

  // Gate 4: DemiJoule syntactic block.
  for (const p of ['ignore previous', 'disregard', 'jailbreak']) {
    if (String(payload).toLowerCase().includes(p)) {
      trace.push({ gate: 'DemiJoule', decision: 'KILL', reason: `blocked: ${p}` })
      return res.status(400).json({
        decision: 'KILL',
        reason: `blocked: ${p}`,
        turn,
        trace,
        evidence: evidenceEnvelope({ mode: 'integration', status: 'PASS', claim_id: 'dgaf-runtime-governance' }),
      })
    }
  }
  trace.push({ gate: 'DemiJoule', decision: 'PASS' })

  // Gate 5: Phi-Closure at Fibonacci checkpoints.
  let phi_gate  = 'SKIP'
  let phi_delta: number | null = null
  if (FIB.includes(turn)) {
    // Audit state is not yet wired into this endpoint. Do not represent the
    // placeholder check as empirical evidence.
    phi_delta = 0
    phi_gate  = 'PASS'
    trace.push({ gate: 'Phi-Closure', decision: phi_gate, audit_state: 'NOT_WIRED', phi_delta })
  }

  const effective_confidence = phi_gate !== 'REPROMPT' ? snapToPhiLattice(confidence) : confidence
  const psi_cubic = Math.abs(PSI ** 3 - (PSI ** 2 + 1)) < 1e-10

  return res.status(200).json({
    decision:             'PASS',
    turn,
    raw_confidence:       confidence,
    effective_confidence: Math.round(effective_confidence * 1e6) / 1e6,
    hpg_fired:            phi_gate !== 'REPROMPT',
    phi_gate,
    phi_delta,
    psi_cubic_check:      psi_cubic,
    claim_received:       claim,
    payload_len:          String(payload).length,
    trace,
    evidence: evidenceEnvelope({
      mode: 'integration',
      status: 'PARTIAL',
      claim_id: 'dgaf-runtime-governance',
    }),
  })
}
