import type { Metadata } from 'next'
import { GovernanceView } from '../../components/governance-view'

export const metadata: Metadata = {
  title: 'Governance — DGAF',
  description: 'DGAF lifecycle, authority, and governance state.',
}

export default function GovernancePage() {
  return <GovernanceView />
}
