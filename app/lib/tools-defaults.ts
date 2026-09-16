export const SWEEP_DEFAULT_TARGETS = [
  'pages/api/health.ts',
  'pages/api/sweep.ts',
  'requirements.txt',
] as const

export const SWEEP_DEFAULT_INPUT = SWEEP_DEFAULT_TARGETS.join('\n')
