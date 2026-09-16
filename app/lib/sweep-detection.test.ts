import assert from 'node:assert/strict'
import test from 'node:test'

import { detectSweepTargets } from './sweep-detection.ts'

test('P-07 does not classify the intentional Herald Python endpoint HIGH solely because it is Python', () => {
  const findings = detectSweepTargets(['api/ahg_herald.py'])
  const herald = findings.find((finding) => finding.target === 'api/ahg_herald.py')

  assert.ok(herald, 'expected the intentional Python API surface to remain visible to the sweep')
  assert.notEqual(herald.severity, 'HIGH')
  assert.match(herald.message, /intentional Python API surface/i)
  assert.match(herald.message, /does not establish deployment correctness or production validation/i)
})

test('P-07 still flags a same-purpose Python and Pages API pair as HIGH', () => {
  const findings = detectSweepTargets(['api/health.py', 'pages/api/health.ts'])
  const pythonFinding = findings.find((finding) => finding.target === 'api/health.py')

  assert.ok(pythonFinding, 'expected the conflicting Python API target to produce a finding')
  assert.equal(pythonFinding.severity, 'HIGH')
  assert.match(pythonFinding.message, /same-purpose Pages API/i)
})
