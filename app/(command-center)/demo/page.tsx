import type { Metadata } from 'next'
import { TektiteDemoView } from '../../components/tektite-demo-view'
import { TektiteGovernedReplayTrace } from '../../components/tektite-governed-replay-trace'

export const metadata: Metadata = {
  title: 'Tektite Demo — DGAF',
  description: 'Interactive DGAF proof-of-operation plus a replay-only DGAF to ACP governed-action trace.',
}

export default function DemoPage() {
  return <>
    <TektiteDemoView />
    <TektiteGovernedReplayTrace />
  </>
}
