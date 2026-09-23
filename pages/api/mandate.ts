// pages/api/mandate.ts — quarantined legacy compatibility surface
//
// NON_AUTHORITATIVE_LEGACY_SURFACE
//
// This route previously exposed process-local mandate creation and sign-off
// without an authenticated principal or durable provenance. It is intentionally
// fail-closed. Authoritative Triumvirate lifecycle behavior lives in the PPTL
// governance implementation and must not be inferred from this HTTP endpoint.
import type { NextApiRequest, NextApiResponse } from 'next'

export default function handler(_req: NextApiRequest, res: NextApiResponse) {
  return res.status(410).json({
    error: 'NON_AUTHORITATIVE_LEGACY_SURFACE',
    authority: 'NONE',
    state_change: 'DISABLED',
    guidance: 'Use reviewed PPTL governance paths; this endpoint cannot issue, mutate, or sign off mandates.',
  })
}
