export type SweepSeverity = 'HIGH' | 'MEDIUM' | 'LOW' | 'INFO'

export interface SweepFinding {
  id: string
  agent: string
  target: string
  severity: SweepSeverity
  message: string
}

const INTENTIONAL_PYTHON_API_SURFACES = new Set(['api/ahg_herald.py'])

function pagesApiCounterpart(target: string): string | null {
  if (!target.startsWith('api/') || !target.endsWith('.py')) {
    return null
  }

  const endpointName = target.slice('api/'.length, -'.py'.length)
  return `pages/api/${endpointName}.ts`
}

export function detectSweepTargets(targets: string[]): SweepFinding[] {
  const targetSet = new Set(targets)

  return targets.flatMap((target, index) => {
    const findings: SweepFinding[] = []

    if (target.startsWith('api/') && target.endsWith('.py')) {
      const counterpart = pagesApiCounterpart(target)

      if (counterpart && targetSet.has(counterpart)) {
        findings.push({
          id: `C-${index}`,
          agent: 'colleen',
          target,
          severity: 'HIGH',
          message: `Python API surface has a same-purpose Pages API candidate (${counterpart}); reconcile repository evidence before production.`,
        })
      } else if (INTENTIONAL_PYTHON_API_SURFACES.has(target)) {
        findings.push({
          id: `C-${index}`,
          agent: 'colleen',
          target,
          severity: 'INFO',
          message: 'Known intentional Python API surface; keeping it visible does not establish deployment correctness or production validation.',
        })
      } else {
        findings.push({
          id: `C-${index}`,
          agent: 'colleen',
          target,
          severity: 'INFO',
          message: 'Python API surface requires evidence review; path and language alone do not establish that it is deprecated, stale, or conflicting.',
        })
      }
    }

    if (target.startsWith('app/api/') && target.endsWith('.ts')) {
      findings.push({
        id: `C-${index}b`,
        agent: 'colleen',
        target,
        severity: 'MEDIUM',
        message: 'App Router API path candidate; confirm reachability in the current hybrid routing model.',
      })
    }

    if (target === 'requirements.txt') {
      findings.push({
        id: `C-${index}c`,
        agent: 'colleen',
        target,
        severity: 'LOW',
        message: 'requirements.txt present; confirm whether the file is operationally relevant to the deployment path.',
      })
    }

    return findings
  })
}
