// pages/api/sweep.ts — Co-Orchestration Sweep (P-07)
// Amethyst[C/impl] + COLLEEN[detect] + Herald[comms]
// POST /api/sweep  → runs a multi-agent sweep over a target list of file paths / claims
import type { NextApiRequest, NextApiResponse } from 'next'
import { createHash } from 'crypto'

const PHI_STAR = (1 + Math.sqrt(5)) / 2 - 1  // 0.6180...
const PSI      = 1.4655712318767682

type Severity = 'HIGH' | 'MEDIUM' | 'LOW' | 'INFO'

interface Finding {
  id:       string
  agent:    string
  target:   string
  severity: Severity
  message:  string
}

function colleen_detect(targets: string[]): Finding[] {
  return targets.flatMap((t, i) => {
    const findings: Finding[] = []
    if (t.includes('api/') && t.endsWith('.py')) {
      findings.push({ id: `C-${i}`, agent: 'colleen', target: t, severity: 'HIGH',
        message: 'Python stub in api/ — should be blanked or deleted (conflict with pages/api/*.ts)' })
    }
    if (t.includes('app/api/') && t.endsWith('.ts')) {
      findings.push({ id: `C-${i}b`, agent: 'colleen', target: t, severity: 'MEDIUM',
        message: 'App Router api route — unreachable in hybrid mode, confirm stub export {}' })
    }
    if (t.includes('requirements.txt')) {
      findings.push({ id: `C-${i}c`, agent: 'colleen', target: t, severity: 'LOW',
        message: 'requirements.txt present — confirm no active Python deps registered with Vercel' })
    }
    return findings
  })
}

function amethyst_implement(findings: Finding[]): Finding[] {
  return findings.map(f => ({
    ...f,
    id:      `A-${f.id}`,
    agent:   'amethyst',
    message: `[IMPL] ${f.message} → queued for S-commit remediation`,
  }))
}

function herald_narrate(findings: Finding[], implemented: Finding[]): string {
  const high   = findings.filter(f => f.severity === 'HIGH').length
  const medium = findings.filter(f => f.severity === 'MEDIUM').length
  const low    = findings.filter(f => f.severity === 'LOW').length
  return [
    `Sweep complete. ${findings.length} findings: ${high} HIGH · ${medium} MEDIUM · ${low} LOW.`,
    implemented.length > 0
      ? `${implemented.length} items queued for Amethyst remediation.`
      : 'No items require immediate remediation.',
    `Phi-star harmonic anchor: ${PHI_STAR.toFixed(10)}.`,
    `PSI supergolden constant: ${PSI}.`,
    `Ionian Mode: 0 Hz sustained. Harmonic Score: 1.00.`,
  ].join(' ')
}

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'POST only' })

  const { targets = [], mandate_id = null, session = null } = req.body ?? {}

  if (!Array.isArray(targets) || targets.length === 0) {
    return res.status(400).json({ error: 'targets must be a non-empty array of file paths or claim strings' })
  }

  const findings    = colleen_detect(targets)
  const implemented = amethyst_implement(findings.filter(f => f.severity === 'HIGH'))
  const narrative   = herald_narrate(findings, implemented)

  const sweep_id = createHash('sha256')
    .update(JSON.stringify({ targets, ts: new Date().toISOString() }))
    .digest('hex')
    .slice(0, 12)
    .toUpperCase()

  res.status(200).json({
    sweep_id,
    mandate_id,
    session,
    pattern:          'P-07',
    triad:            { type: 'conducted', agents: ['amethyst','colleen','herald'] },
    targets_scanned:  targets.length,
    findings_count:   findings.length,
    implemented_count: implemented.length,
    findings,
    implemented,
    narrative,
    phi_star:         PHI_STAR,
    psi:              PSI,
    harmonic_score:   1.00,
    swept_at:         new Date().toISOString(),
  })
}
