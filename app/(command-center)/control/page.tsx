import type { Metadata } from 'next'
import { ControlRouteView } from '../../components/routed-views'

export const metadata: Metadata = {
  title: 'Control Room — DGAF',
  description: 'DGAF runtime telemetry and operator controls.',
}

export default function ControlPage() {
  return <ControlRouteView />
}
