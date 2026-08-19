export type EvidenceMode = 'synthetic' | 'integration' | 'empirical' | 'production'

export interface EvidenceEnvelope {
  mode: EvidenceMode
  status: 'PASS' | 'PARTIAL' | 'BLOCKED' | 'NOT_IMPLEMENTED'
  claim_id?: string
  run_id?: string
  dataset?: string
}

export function evidenceEnvelope(input: EvidenceEnvelope): EvidenceEnvelope {
  return input
}
