// app/layout.tsx
import type { Metadata } from 'next'
export const metadata: Metadata = {
  title: 'DGAF-Framework — Ensemble Dashboard',
  description: 'Topological Resonant Decay · Phi-Closure Gate · 9-Gate Orchestration',
}
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en">
      <body style={{ margin: 0, background: '#0f172a' }}>{children}</body>
    </html>
  )
}
