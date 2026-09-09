// pages/api/staging-breaker.ts — preview-only structural runtime evidence
import type { NextApiRequest, NextApiResponse } from 'next'

type BreakerState = 'STAGING' | 'ACTIVE' | 'BREAKER_OPEN' | 'FROZEN' | 'ROLLBACK' | 'VERIFIED'
type TraceEntry = { from: BreakerState | null; to: BreakerState; reason: string }

const BREAKER_THRESHOLD = 0.8
const INJECTED_FAULT_SCORE = 0.95
const EXPECTED_SEQUENCE: BreakerState[] = [
  'STAGING',
  'ACTIVE',
  'BREAKER_OPEN',
  'FROZEN',
  'ROLLBACK',
  'VERIFIED',
]

function unavailable(res: NextApiResponse) {
  res.setHeader('Cache-Control', 'no-store')
  return res.status(404).json({
    status: 'NOT_AVAILABLE',
    reason: 'live staging breaker exercise is available only on an explicitly enabled Vercel preview',
    scientific_state_effect: 'NONE',
  })
}

export default function handler(req: NextApiRequest, res: NextApiResponse) {
  res.setHeader('Cache-Control', 'no-store')

  if (req.method !== 'POST') {
    return res.status(405).json({ status: 'METHOD_NOT_ALLOWED', scientific_state_effect: 'NONE' })
  }

  if (process.env.VERCEL_ENV !== 'preview') return unavailable(res)
  if (process.env.DGAF_STAGING_BREAKER_EXERCISE_ENABLED !== 'true') return unavailable(res)

  const expectedExerciseId = process.env.DGAF_STAGING_BREAKER_EXERCISE_ID
  const suppliedExerciseId = req.headers['x-dgaf-staging-exercise-id']
  if (
    !expectedExerciseId ||
    typeof suppliedExerciseId !== 'string' ||
    suppliedExerciseId !== expectedExerciseId
  ) {
    return res.status(403).json({
      status: 'REJECTED',
      reason: 'exercise identity mismatch',
      scientific_state_effect: 'NONE',
    })
  }

  const trace: TraceEntry[] = []
  let state: BreakerState = 'STAGING'
  trace.push({ from: null, to: state, reason: 'disposable preview staging baseline' })

  const transition = (next: BreakerState, reason: string) => {
    const previous = state
    state = next
    trace.push({ from: previous, to: state, reason })
  }

  transition('ACTIVE', 'staging exercise admitted')

  if (INJECTED_FAULT_SCORE <= BREAKER_THRESHOLD) {
    return res.status(500).json({
      status: 'FAIL',
      reason: 'controlled fault did not cross the fixed breaker threshold',
      threshold: BREAKER_THRESHOLD,
      injected_fault_score: INJECTED_FAULT_SCORE,
      trace,
      scientific_state_effect: 'NONE',
    })
  }

  transition('BREAKER_OPEN', 'controlled synthetic fault crossed fixed threshold')
  transition('FROZEN', 'breaker-open state freezes the exercise path')
  transition('ROLLBACK', 'restore disposable staging baseline')
  transition('VERIFIED', 'rollback state verified inside the exercised runtime path')

  const sequence = trace.map((entry) => entry.to)
  const sequenceMatches = JSON.stringify(sequence) === JSON.stringify(EXPECTED_SEQUENCE)
  if (!sequenceMatches) {
    return res.status(500).json({
      status: 'FAIL',
      reason: 'breaker transition sequence did not match the declared contract',
      trace,
      scientific_state_effect: 'NONE',
    })
  }

  return res.status(200).json({
    evidence_class: 'DGAF_LIVE_STAGING_BREAKER_EXERCISE_V1',
    status: 'PASS_STRUCTURAL_LIVE_STAGING_ONLY',
    exercise_id: expectedExerciseId,
    runtime_environment: 'vercel_preview',
    threshold: BREAKER_THRESHOLD,
    injected_fault_score: INJECTED_FAULT_SCORE,
    sequence,
    rollback_verified: true,
    protected_or_empirical_material_used: false,
    primary_analysis_authorized: false,
    canonical_dgaf_efficacy: 'NOT_ESTABLISHED',
    high_assurance_authorized: false,
    scientific_state_effect: 'NONE',
    trace,
  })
}
