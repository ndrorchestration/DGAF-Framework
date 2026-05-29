// app/api/orchestrate/route.ts — Next.js App Router API route
import { NextResponse } from 'next/server'

const PSI      = 1.4655712318767682
const PHI      = (1 + Math.sqrt(5)) / 2
const PHI_STAR = PHI - 1
const FIB_CHECKPOINTS = [13, 21, 34, 55]
const PHI_TOLERANCE   = 0.05

interface OrchRequest {
  payload:    string
  confidence: number
  claim?:     string
  turn?:      number
}

function snapToPhiLattice(conf: number): number {
  // Octave map [0,1] → [1,2], snap to nearest phi-lattice point
  const octave = 1 + conf
  const lattice = [1, PHI_STAR + 1, PHI]
  let nearest = lattice[0]
  for (const pt of lattice) {
    if (Math.abs(pt - octave) < Math.abs(nearest - octave)) nearest = pt
  }
  return nearest - 1  // back to [0,1]
}

export async function POST(req: Request) {
  const body: OrchRequest = await req.json().catch(() => ({} as OrchRequest))
  const { payload = '', confidence = 0.5, claim = '', turn = 1 } = body

  // Gate 4: DemiJoule syntactic check (stub)
  const blocked_patterns = ['ignore previous', 'disregard', 'jailbreak']
  for (const p of blocked_patterns) {
    if (payload.toLowerCase().includes(p)) {
      return NextResponse.json(
        { decision: 'KILL', reason: `blocked_pattern: ${p}`, turn },
        { status: 400 }
      )
    }
  }

  // Gate 5: Phi-Closure check at Fibonacci checkpoints
  let phi_gate = 'SKIP'
  let phi_delta = null
  if (FIB_CHECKPOINTS.includes(turn)) {
    // Stub: assume stable ratio = 0.618 at checkpoint (production reads audit state)
    const R = PHI_STAR
    phi_delta = Math.abs(R - PHI_STAR)
    phi_gate  = phi_delta < PHI_TOLERANCE ? 'PASS' : 'REPROMPT'
  }

  // Gate 6: HPG — only if phi gate passed or skipped
  let effective_confidence = confidence
  let hpg_fired = false
  if (phi_gate !== 'REPROMPT') {
    effective_confidence = snapToPhiLattice(confidence)
    hpg_fired = true
  }

  const psi_cubic = Math.abs(PSI ** 3 - (PSI ** 2 + 1)) < 1e-10

  return NextResponse.json({
    decision:             'PASS',
    turn,
    raw_confidence:       confidence,
    effective_confidence: Math.round(effective_confidence * 1e6) / 1e6,
    hpg_fired,
    phi_gate,
    phi_delta,
    psi_cubic_check:      psi_cubic,
    claim_received:       claim,
    payload_len:          payload.length,
  })
}
