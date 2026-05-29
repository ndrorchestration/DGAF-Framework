// app/api/audit/route.ts — Next.js App Router API route
import { NextResponse } from 'next/server'

// In-memory audit state — resets per cold start (serverless)
// Production: replace with Vercel KV or Redis
let state = {
  turn_count:      0,
  stable_turns:    0,
  prune_events:    0,
  axiom_count:     1,   // T0 axiom guard always starts at 1
  consec_phi_fail: 0,
}

export async function GET() {
  return NextResponse.json({
    status:          'ok',
    version:         process.env.ENSEMBLE_VERSION ?? '1.7.0',
    ...state,
  })
}

export async function POST(req: Request) {
  const body = await req.json().catch(() => ({}))
  if (body.turn_count      !== undefined) state.turn_count      = body.turn_count
  if (body.stable_turns    !== undefined) state.stable_turns    = body.stable_turns
  if (body.prune_events    !== undefined) state.prune_events    = body.prune_events
  if (body.axiom_count     !== undefined) state.axiom_count     = body.axiom_count
  if (body.consec_phi_fail !== undefined) state.consec_phi_fail = body.consec_phi_fail
  return NextResponse.json({ status: 'updated', ...state })
}
