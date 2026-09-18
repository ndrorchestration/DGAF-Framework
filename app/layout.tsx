import type { Metadata } from 'next'
import './styles/globals.css'
import './styles/decision-frontier.css'
import './styles/governance-map.css'
import './styles/state-space.css'
import './styles/typography-editorial.css'

export const metadata: Metadata = {
  title: 'DGAF — Governance Command Center',
  description: 'Governed multi-agent orchestration, evidence, verification, authority, and runtime observability.',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return <html lang="en"><body>{children}</body></html>
}
