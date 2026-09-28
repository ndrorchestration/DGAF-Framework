import type { Metadata } from 'next'
import { TektiteDemoView } from '../../components/tektite-demo-view'

export const metadata: Metadata = {
  title: 'Tektite Demo — DGAF',
  description: 'Interactive bounded proof-of-operation for DGAF action governance.',
}

export default function DemoPage() {
  return <TektiteDemoView />
}
