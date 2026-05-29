// pages/api/audit.ts — Pages Router API
import type { NextApiRequest, NextApiResponse } from 'next'

// In-memory state — resets per cold start
// Production: replace with Vercel KV
const state = {
  turn_count:      0,
  stable_turns:    0,
  prune_events:    0,
  axiom_count:     1,
  consec_phi_fail: 0,
}

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === 'POST') {
    const b = req.body ?? {}
    if (b.turn_count      !== undefined) state.turn_count      = b.turn_count
    if (b.stable_turns    !== undefined) state.stable_turns    = b.stable_turns
    if (b.prune_events    !== undefined) state.prune_events    = b.prune_events
    if (b.axiom_count     !== undefined) state.axiom_count     = b.axiom_count
    if (b.consec_phi_fail !== undefined) state.consec_phi_fail = b.consec_phi_fail
    return res.status(200).json({ status: 'updated', ...state })
  }
  res.status(200).json({
    status:  'ok',
    version: process.env.ENSEMBLE_VERSION ?? '1.7.0',
    ...state,
  })
}
