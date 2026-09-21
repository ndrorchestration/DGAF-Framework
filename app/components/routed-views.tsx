'use client'

import { AgentsView } from './agents-view'
import { ControlRoomView } from './control-room-view'
import { useDashboardRuntime } from './dashboard-runtime-provider'

export function ControlRouteView() {
  const dashboard = useDashboardRuntime()
  return (
    <ControlRoomView
      snapshot={dashboard.snapshot}
      phase={dashboard.phase}
      error={dashboard.error}
      lastSuccessAt={dashboard.lastSuccessAt}
      onRefresh={() => void dashboard.refresh()}
    />
  )
}

export function AgentsRouteView() {
  const dashboard = useDashboardRuntime()
  return <AgentsView roster={dashboard.snapshot?.roster ?? null} />
}
