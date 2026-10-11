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
    <section className="panel">
      <span className="eyebrow">SYNTHETIC CONTAINMENT ASSESSMENT</span>
      <h2>Evidence, meaning, and authority</h2>
      <p>Explore five fixed-time synthetic cases. Live containment and producer authenticity remain unestablished; every assessment carries no execution authority.</p>
      <a href="/evidence/tektite-containment-v0.html">Open the bounded assessment replay</a>
    </section>
    <TektiteCepObservability />
  </>
}
