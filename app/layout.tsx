import type { Metadata } from 'next'
import './styles/globals.css'
import './styles/refinement.css'

export const metadata: Metadata = {
  title: 'DGAF — Governance Command Center',
  description: 'Governed multi-agent orchestration, evidence, verification, authority, and runtime observability.',
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return <html lang="en"><body>{children}</body></html>
}
