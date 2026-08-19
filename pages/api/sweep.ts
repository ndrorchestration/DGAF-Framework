// pages/api/sweep.ts — Co-Orchestration Sweep (P-07)
// Amethyst[C/impl] + COLLEEN[detect] + Herald[comms]
// POST /api/sweep → analyzes a supplied target list; it does not mutate repository state.
import type { NextApiRequest, NextApiResponse } from 'next'
import { createHash } from 'crypto'
import { evidenceEnvelope } from '../../lib/evidence'

const PHI_STAR = (1 + Math.sqrt(5)) / 2 - 1
const PSI      = 1.4655712318767682

type Severity = 'HIGH' | 'MEDIUM' | 'LOW' | 'INFO'

interface Finding {
  id: string
  agent: string
  target: string
  severity: Severity
  message: string
}

function colleen_detect(targets: string[]): Finding[] {
  return targets.flatMap((t, i) => {
    const findings: Finding[] = []
    if (t.includes('api/') && t.endsWith('.py')) {
      findings.push({
        id: `C-${i}`,
        agent: 'colleen',
        target: t,
        severity: 'HIGH',
        message: 'Python API stub candidate; confirm whether it conflicts with pages/api/*.ts.',
      })
    }
    if (t.includes('app/api/') && t.endsWith('.ts')) {
      findings.push({
        id: `C-${i}b`,
        agent: 'colleen',
        target: t,
        severity: 'MEDIUM',
        message: 'App Router API path candidate; confirm reachability in the current hybrid routing model.',
      })
    }
    if (t.includes('requirements.txt')) {
      findings.push({
        id: `C-${i}c`,
        agent: 'colleen',
        target: t,
        severity: 'LOW',
        message: 'requirements.txt present; confirm whether the file is operationally relevant to the deployment path.',
      })
    }
    return findings
  })
}

function planned_remediations(findings: Finding[]): Finding[] {
  return findings
    .filter(f => f.severity === 'HIGH')
    .map(f => ({
      ...f,
      id: `A-${f.id}`,
      agent: 'amethyst',
      message: `[PLAN ONLY] ${f.message}`,
    }))
}

function herald_narrate(findings: Finding[], planned: Finding[]): string {
  const high = findings.filter(f => f.severity === 'HIGH').length
  const medium = findings.filter(f => f.severity === 'MEDIUM').length
  const low = findings.filter(f => f.severity === 'LOW').length
  return [
    `Sweep complete. ${findings.length} findings: ${high} HIGH · ${medium} MEDIUM · ${low} LOW.`,
    planned.length > 0
      ? `${planned.length} remediation candidates identified; no repository mutation was performed by this endpoint.`
      : 'No high-severity remediation candidates identified.',
    `Phi-star harmonic anchor: ${PHI_STAR.toFixed(10)}.`,
    `PSI supergolden constant: ${PSI}.`,
  ].join(' ')
}

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  if (req.method !== 'POST') {
    return res.status(405).json({
      error: 'POST only',
      evidence: evidenceEnvelope({ mode: 'integration', status: 'NOT_IMPLEMENTED', claim_id: 'dgaf-sweep' }),
    })
  }

  const body = req.body ?? {}
  const { targets = [], mandate_id = null, session = null } = body

  if (!Array.isArray(targets) || targets.length === 0 || !targets.every(t => typeof t === 'string')) {
    return res.status(400).json({
      error: 'targets must be a non-empty array of strings',
      evidence: evidenceEnvelope({ mode: 'integration', status: 'PASS', claim_id: 'dgaf-sweep-input-validation' }),
    })
  }

  const findings = colleen_detect(targets)
  const planned = planned_remediations(findings)
  const narrative = herald_narrate(findings, planned)
  const sweep_id = createHash('sha256')
    .update(JSON.stringify({ targets, mandate_id, session, ts: new Date().toISOString() }))
    .digest('hex')
    .slice(0, 12)
    .toUpperCase()

  return res.status(200).json({
    sweep_id,
    mandate_id,
    session,
    pattern: 'P-07',
    triad: { type: 'conducted', agents: ['amethyst', 'colleen', 'herald'] },
    targets_scanned: targets.length,
    findings_count: findings.length,
    planned_remediation_count: planned.length,
    mutation_performed: false,
    findings,
    planned_remediations: planned,
    narrative,
    phi_star: PHI_STAR,
    psi: PSI,
    harmonic_score: null,
    harmonic_score_status: 'NOT_COMPUTED',
    swept_at: new Date().toISOString(),
    evidence: evidenceEnvelope({
      mode: 'integration',
      status: 'PARTIAL',
      claim_id: 'dgaf-sweep',
    }),
  })
}
