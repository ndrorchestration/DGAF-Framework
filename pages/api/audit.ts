// pages/api/audit.ts — Pages Router API
// ⚠️  STATE RESETS ON COLD START — in-memory only.
// Production upgrade path: replace `state` with Vercel KV reads/writes.
import type { NextApiRequest, NextApiResponse } from 'next'

export const COLD_START_WARNING =
  'Audit counters are in-memory and reset on each serverless cold start. ' +
  'Wire to Vercel KV for persistence.'

const state = {
  turn_count:      0,
  stable_turns:    0,
  prune_events:    0,
  axiom_count:     1,   // T0 axiom guard
  consec_phi_fail: 0,
  cold_start:      true,
  cold_start_at:   new Date().toISOString(),
}

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method === 'POST') {
    const b = req.body ?? {}
    if (b.turn_count      !== undefined) { state.turn_count      = b.turn_count;      state.cold_start = false }
    if (b.stable_turns    !== undefined) state.stable_turns    = b.stable_turns
    if (b.prune_events    !== undefined) state.prune_events    = b.prune_events
    if (b.axiom_count     !== undefined) state.axiom_count     = b.axiom_count
    if (b.consec_phi_fail !== undefined) state.consec_phi_fail = b.consec_phi_fail
    return res.status(200).json({ status: 'updated', ...state, _warning: COLD_START_WARNING })
  }
  res.status(200).json({
    status:   'ok',
    version:  process.env.ENSEMBLE_VERSION ?? '1.7.0',
    ...state,
    _warning: state.cold_start ? COLD_START_WARNING : null,
  })
}
