import type { Metadata } from 'next'
import { TektiteCepObservability } from '../../components/tektite-cep-observability'
import { TektiteDemoView } from '../../components/tektite-demo-view'
import { TektiteGovernedReplayTrace } from '../../components/tektite-governed-replay-trace'

export const metadata: Metadata = {
  title: 'Tektite Demo — DGAF',
  description: 'Interactive DGAF proof-of-operation, replay-only DGAF to ACP governed-action trace, and read-only CEP observability.',
}

export default function DemoPage() {
  return <>
    <TektiteDemoView />
    <TektiteGovernedReplayTrace />
    <TektiteCepObservability />
  </>
}
