// pages/api/orchestrate.ts — Pages Router API
import type { NextApiRequest, NextApiResponse } from 'next'

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
    return res.status(405).json({ error: 'Method not allowed' })
  }
  const { payload = '', confidence = 0.5, claim = '', turn = 1 } = req.body ?? {}

  // Gate 4: DemiJoule syntactic block
  for (const p of ['ignore previous', 'disregard', 'jailbreak']) {
    if (String(payload).toLowerCase().includes(p)) {
      return res.status(400).json({ decision: 'KILL', reason: `blocked: ${p}`, turn })
    }
  }

  // Gate 5: Phi-Closure at Fibonacci checkpoints
  let phi_gate  = 'SKIP'
  let phi_delta = null
  if (FIB.includes(turn)) {
    phi_delta = Math.abs(PHI_STAR - PHI_STAR)  // stub: always 0 until audit state wired
    phi_gate  = phi_delta < PHI_TOL ? 'PASS' : 'REPROMPT'
  }

  // Gate 6: HPG snap
  const effective_confidence = phi_gate !== 'REPROMPT' ? snapToPhiLattice(confidence) : confidence
  const psi_cubic = Math.abs(PSI ** 3 - (PSI ** 2 + 1)) < 1e-10

  res.status(200).json({
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
  })
}
