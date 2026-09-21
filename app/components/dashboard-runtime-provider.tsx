'use client'

import { createContext, useContext } from 'react'
import { useDashboardData } from '../hooks/use-dashboard-data'

type DashboardRuntime = ReturnType<typeof useDashboardData>

const DashboardRuntimeContext = createContext<DashboardRuntime | null>(null)

export function DashboardRuntimeProvider({ children }: { children: React.ReactNode }) {
  const dashboard = useDashboardData()
  return <DashboardRuntimeContext.Provider value={dashboard}>{children}</DashboardRuntimeContext.Provider>
}

export function useDashboardRuntime(): DashboardRuntime {
  const dashboard = useContext(DashboardRuntimeContext)
  if (!dashboard) throw new Error('DashboardRuntimeProvider is required for command-center routes')
  return dashboard
}
