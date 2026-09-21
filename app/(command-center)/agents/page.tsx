import type { Metadata } from 'next'
import { AgentsRouteView } from '../../components/routed-views'

export const metadata: Metadata = {
  title: 'Agents & Formations — DGAF',
  description: 'DGAF agent roles, formations, and topology.',
}

export default function AgentsPage() {
  return <AgentsRouteView />
}
