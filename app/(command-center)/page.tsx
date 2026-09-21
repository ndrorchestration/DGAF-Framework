import type { Metadata } from 'next'
import { OverviewView } from '../components/overview-view'

export const metadata: Metadata = {
  title: 'DGAF — Governance Command Center',
  description: 'Governed multi-agent orchestration, evidence, verification, authority, and runtime observability.',
}

export default function OverviewPage() {
  return <OverviewView />
}
