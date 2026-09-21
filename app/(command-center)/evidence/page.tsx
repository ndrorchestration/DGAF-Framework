import type { Metadata } from 'next'
import { EvidenceView } from '../../components/evidence-view'

export const metadata: Metadata = {
  title: 'Evidence & Research — DGAF',
  description: 'DGAF claims, evidence, provenance, and research state.',
}

export default function EvidencePage() {
  return <EvidenceView />
}
