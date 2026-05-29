// pages/api/triad.ts — triad formation + 9-gate turn execution
// POST /api/triad/form   → validate and form a triad
// POST /api/triad/turn   → run orchestrate_turn() through all 9 gates
import type { NextApiRequest, NextApiResponse } from 'next'

const PHI      = (1 + Math.sqrt(5)) / 2
const PHI_STAR = PHI - 1                        // 0.6180339887...
const PSI      = 1.4655712318767682
const FIB      = new Set([13, 21, 34, 55])
const PHI_TOL  = 0.05
const SCPE_THR = 0.15

const VALID_TRIADS: Record<string, { type: string; agents: string[] }> = {
  governance:    { type: 'conducted',   agents: ['amethyst','apogee','sentinel'] },
  coherence:     { type: 'conducted',   agents: ['amethyst','colleen','apogee'] },
  pdmal:         { type: 'triumvirate', agents: ['amethyst','colleen','apogee'] },
  optimization:  { type: 'conducted',   agents: ['amethyst','demijole','reciprocity'] },
  formalization: { type: 'consensus',   agents: ['amethyst','prodigy','reson'] },
  studio:        { type: 'consensus',   agents: ['reson','echolette','lyra'] },
  runtime_gate:  { type: 'conducted',   agents: ['amethyst','demijole','sentinel'] },
}

function snapToPhiLattice(c: number): number {
  const lattice = [0, PHI_STAR, 1]          // Ionian octave anchors
  let nearest   = lattice[0]
  for (const pt of lattice) {
    if (Math.abs(pt - c) < Math.abs(nearest - c)) nearest = pt
  }
  return Math.round(nearest * 1e9) / 1e9
}

function runGates(payload: string, confidence: number, claim: string, turn: number) {
  const gates: Record<string, unknown> = {}

  // Gate 1 — SCPE: token decay proxy (payload length compression)
  const tokens_before = payload.length
  const scpe_ratio    = tokens_before > 0 ? Math.min(SCPE_THR, tokens_before / (tokens_before + 100)) : 0
  const scpe_pruned   = scpe_ratio > 0.02
  gates.g1_scpe = { fired: scpe_pruned, ratio: Math.round(scpe_ratio * 1e4) / 1e4, t0_immune: true }

  // Gate 2 — COLLEEN: schema diff stub
  gates.g2_colleen = { fired: true, schema_delta: 0, aligned: true }

  // Gate 3 — RECIPROCITY: PDMAL reweight stub
  const pdmal_drift   = Math.abs(PHI_STAR - (confidence > 0 ? confidence : PHI_STAR))
  const pdmal_status  = pdmal_drift > 0.08 ? 'ALERT' : pdmal_drift > 0.02 ? 'WATCH' : 'OK'
  gates.g3_reciprocity = { fired: true, pdmal_drift: Math.round(pdmal_drift * 1e6) / 1e6, pdmal_status }

  // Gate 4 — DemiJoule: syntactic safety block
  const blocked_phrases = ['ignore previous','disregard','jailbreak','bypass']
  const blocked = blocked_phrases.find(p => payload.toLowerCase().includes(p))
  if (blocked) {
    return { decision: 'KILL', reason: `DemiJoule blocked: "${blocked}"`, gate_reached: 4, gates }
  }
  gates.g4_demijole = { fired: true, blocked: false }

  // Gate 5 — Phi-Closure: Fibonacci checkpoint
  let phi_gate  = 'SKIP'
  let phi_delta = 0
  if (FIB.has(turn)) {
    phi_delta = Math.abs(PHI_STAR - confidence)
    phi_gate  = phi_delta < PHI_TOL ? 'PASS'
              : phi_delta < 0.15    ? 'REPROMPT'
              : turn >= 34          ? 'KILL_REC'
              :                       'WARN'
  }
  if (phi_gate === 'KILL_REC') {
    return { decision: 'KILL_REC', reason: 'Phi-Closure KILL_REC at Fib checkpoint', turn, gate_reached: 5, gates }
  }
  gates.g5_phi_closure = { fired: FIB.has(turn), phi_gate, phi_delta: Math.round(phi_delta * 1e6) / 1e6 }

  // Gate 6 — HPG: snap confidence to phi-lattice (only if phi_gate !== REPROMPT)
  const eff_confidence = phi_gate !== 'REPROMPT' ? snapToPhiLattice(confidence) : confidence
  gates.g6_hpg = { fired: phi_gate !== 'REPROMPT', raw: confidence, snapped: eff_confidence }

  // Gate 7 — PRODIGY: claim verification stub
  const claim_valid = claim.length > 3 && eff_confidence > 0.1
  gates.g7_prodigy  = { fired: true, claim_valid, claim_len: claim.length }

  // Gate 8 — APOGEE: artifact review stub
  const psi_cubic = Math.abs(PSI ** 3 - (PSI ** 2 + 1)) < 1e-9
  gates.g8_apogee = { fired: true, psi_cubic_valid: psi_cubic, phi_star_valid: Math.abs(PHI_STAR - 0.6180339887) < 1e-9 }

  // Gate 9 — AMETHYST seal
  const seal_hash = Buffer.from(`${turn}:${claim}:${eff_confidence}`).toString('base64').slice(0, 16)
  gates.g9_amethyst = { fired: true, seal: seal_hash }

  return {
    decision:             'PASS',
    turn,
    effective_confidence: eff_confidence,
    phi_gate,
    pdmal_status,
    seal:                 seal_hash,
    gate_reached:         9,
    gates,
  }
}

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'POST only' })

  const { action } = req.query

  // POST /api/triad?action=form
  if (action === 'form') {
    const { triad_id, agents } = req.body ?? {}
    const canonical = VALID_TRIADS[triad_id]
    if (!canonical) {
      return res.status(400).json({
        error:   'Unknown triad_id',
        valid:   Object.keys(VALID_TRIADS),
        received: triad_id,
      })
    }
    const provided = [...(agents ?? [])].sort().join(',')
    const expected = [...canonical.agents].sort().join(',')
    const match    = provided === expected
    return res.status(match ? 200 : 400).json({
      triad_id,
      type:    canonical.type,
      agents:  canonical.agents,
      formed:  match,
      mismatch: match ? null : { expected: canonical.agents, received: agents },
    })
  }

  // POST /api/triad?action=turn  (default)
  const { payload = '', confidence = PHI_STAR, claim = '', turn = 1 } = req.body ?? {}
  const result = runGates(String(payload), Number(confidence), String(claim), Number(turn))
  return res.status(result.decision === 'PASS' ? 200 : 400).json(result)
}
