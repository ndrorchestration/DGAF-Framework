// pages/api/roster.ts — returns canonical agent registry (ENSEMBLE_ROSTER.md derived)
import type { NextApiRequest, NextApiResponse } from 'next'

const AGENTS = [
  { id: 'amethyst',    tier: 'L5', role: 'Meta-Orchestrator / Triumvirate Prime',       status: 'active',    triad_roles: ['Prime','Conductor'] },
  { id: 'colleen',     tier: 'L5', role: 'Institutional Anchor / Triumvirate Prefect',   status: 'active',    triad_roles: ['Prefect','Detect'] },
  { id: 'apogee',      tier: 'L4', role: 'QA Orchestrator / Triumvirate Prefect',        status: 'active',    triad_roles: ['Prefect','Verify'] },
  { id: 'demijole',    tier: 'L4', role: 'DGAF Ethics & Cost Gate',                      status: 'active',    triad_roles: ['Instrument'] },
  { id: 'reciprocity', tier: 'L3', role: 'Portfolio & Rollback Manager',                 status: 'active',    triad_roles: ['Instrument'] },
  { id: 'prodigy',     tier: 'L3', role: 'Phi-Calculus Specialist',                      status: 'partial',   triad_roles: ['Instrument'] },
  { id: 'herald',      tier: 'L3', role: 'Comms Gateway',                                status: 'partial',   triad_roles: ['Comms'] },
  { id: 'sentinel',    tier: 'L3', role: 'Security & CI Integrity',                      status: 'partial',   triad_roles: ['Instrument'] },
  { id: 'reson',       tier: 'S1', role: 'Harmonic Logic Gatekeeper',                   status: 'foundational', triad_roles: ['Studio'] },
  { id: 'echolette',   tier: 'S2', role: 'Feedback Loop Architect',                     status: 'foundational', triad_roles: ['Studio'] },
  { id: 'lyra',        tier: 'S3', role: 'Harmonic Synthesizer',                        status: 'foundational', triad_roles: ['Studio'] },
]

const TRIADS = [
  { id: 'governance',     type: 'conducted',   agents: ['amethyst','apogee','sentinel'],     use_case: 'Compliance sweeps, security audits, CI enforcement' },
  { id: 'coherence',      type: 'conducted',   agents: ['amethyst','colleen','apogee'],      use_case: 'Ecosystem coherence, doc sweeps, identity alignment' },
  { id: 'pdmal',          type: 'triumvirate', agents: ['amethyst','colleen','apogee'],      use_case: 'Large choreographed ensembles, multi-repo campaigns, swarm ops' },
  { id: 'optimization',   type: 'conducted',   agents: ['amethyst','demijole','reciprocity'],use_case: 'Token budget, rollback planning, cost-quality tradeoffs' },
  { id: 'formalization',  type: 'consensus',   agents: ['amethyst','prodigy','reson'],       use_case: 'Mathematical proof review, phi-calculus derivations' },
  { id: 'studio',         type: 'consensus',   agents: ['reson','echolette','lyra'],         use_case: 'Signal chain QA, drift detection, harmonic synthesis' },
  { id: 'runtime_gate',   type: 'conducted',   agents: ['amethyst','demijole','sentinel'],   use_case: 'SCPE/Phi-Closure/PDMAL Monitor operational oversight' },
]

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  const { filter } = req.query
  const agents = filter
    ? AGENTS.filter(a => a.status === filter || a.tier === filter)
    : AGENTS
  res.status(200).json({
    version:      process.env.ENSEMBLE_VERSION ?? '1.7.0',
    agent_count:  agents.length,
    triad_count:  TRIADS.length,
    ndr_patterns: 33,
    agents,
    triads:       TRIADS,
    phi_star:     0.6180339887,
    psi:          1.4655712318767682,
  })
}
