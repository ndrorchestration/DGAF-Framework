'use client'

import { useState } from 'react'
import { useDashboardData } from './hooks/use-dashboard-data'
import { AgentsView } from './components/agents-view'
import { AppShell, type ViewId } from './components/app-shell'
import { ControlRoomView } from './components/control-room-view'
import { EvidenceView } from './components/evidence-view'
import { GovernanceView } from './components/governance-view'
import { OverviewView } from './components/overview-view'
import { ToolsView } from './components/tools-view'

export default function Dashboard() {
  const [view, setView] = useState<ViewId>('overview')
  const dashboard = useDashboardData()

  let content: React.ReactNode
  switch (view) {
    case 'control':
      content = <ControlRoomView snapshot={dashboard.snapshot} phase={dashboard.phase} error={dashboard.error} lastSuccessAt={dashboard.lastSuccessAt} onRefresh={() => void dashboard.refresh()} />
      break
    case 'governance':
      content = <GovernanceView />
      break
    case 'agents':
      content = <AgentsView roster={dashboard.snapshot?.roster ?? null} />
      break
    case 'evidence':
      content = <EvidenceView />
      break
    case 'tools':
      content = <ToolsView />
      break
    default:
      content = <OverviewView onNavigate={setView} />
  }

  return <AppShell activeView={view} onNavigate={setView} phase={dashboard.phase} lastSuccessAt={dashboard.lastSuccessAt}>{content}</AppShell>
}
