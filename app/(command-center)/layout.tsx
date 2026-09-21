import { AppShell } from '../components/app-shell'
import { DashboardRuntimeProvider } from '../components/dashboard-runtime-provider'

export default function CommandCenterLayout({ children }: { children: React.ReactNode }) {
  return (
    <DashboardRuntimeProvider>
      <AppShell>{children}</AppShell>
    </DashboardRuntimeProvider>
  )
}
