// pages/api/health.ts — Pages Router API (takes precedence over app/api in hybrid mode)
import type { NextApiRequest, NextApiResponse } from 'next'

const PSI      = 1.4655712318767682
const PHI      = (1 + Math.sqrt(5)) / 2
const PHI_STAR = PHI - 1
const VERSION  = process.env.ENSEMBLE_VERSION ?? '1.7.0'
const PSI_ON   = (process.env.PSI_CHECK ?? 'enabled').toLowerCase() === 'enabled'

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  const psi_cubic = Math.abs(PSI ** 3 - (PSI ** 2 + 1)) < 1e-10
  res.status(200).json({
    status:          'ok',
    psi_cubic:       psi_cubic && PSI_ON,
    version:         VERSION,
    phi_star:        Math.round(PHI_STAR * 1e6) / 1e6,
    psi:             Math.round(PSI * 1e10) / 1e10,
    runtime:         `node-${process.version}`,
    scpe_threshold:  0.15,
    phi_checkpoints: [13, 21, 34, 55],
    phi_tolerance:   0.05,
    t0_axiom_guard:  true,
    adapters:        ['raw', 'langchain', 'langgraph', 'autogen', 'crewai'],
  })
}
