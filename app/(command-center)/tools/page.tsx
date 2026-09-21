import type { Metadata } from 'next'
import { ToolsView } from '../../components/tools-view'

export const metadata: Metadata = {
  title: 'Tools — DGAF',
  description: 'DGAF bounded operator and sweep tooling.',
}

export default function ToolsPage() {
  return <ToolsView />
}
