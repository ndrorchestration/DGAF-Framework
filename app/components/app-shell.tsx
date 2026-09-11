'use client'

import { useState } from 'react'
import type { DashboardPhase } from '../hooks/use-dashboard-data'
import { TRUTH_BOUNDARY } from '../lib/governance'
import { ActivityIcon, EvidenceIcon, MenuIcon, NodesIcon, OverviewIcon, ShieldIcon, ToolsIcon } from './icons'
import { StatusChip } from './status-chip'

export type ViewId = 'overview' | 'control' | 'governance' | 'agents' | 'evidence' | 'tools'

const NAV = [
  { id: 'overview' as const, label: 'Overview', sub: 'What DGAF is', Icon: OverviewIcon },
  { id: 'control' as const, label: 'Control Room', sub: 'Runtime telemetry', Icon: ActivityIcon },
  { id: 'governance' as const, label: 'Governance', sub: 'Lifecycle & authority', Icon: ShieldIcon },
  { id: 'agents' as const, label: 'Agents & Formations', sub: 'Roles & topology', Icon: NodesIcon },
  { id: 'evidence' as const, label: 'Evidence & Research', sub: 'Claims & experiment state', Icon: EvidenceIcon },
  { id: 'tools' as const, label: 'Tools', sub: 'P-07 sweep workspace', Icon: ToolsIcon },
]

function phaseState(phase: DashboardPhase) {
  if (phase === 'fresh') return 'pass' as const
  if (phase === 'stale') return 'stale' as const
  if (phase === 'error') return 'unavailable' as const
  return 'loading' as const
}

export function AppShell({ activeView, onNavigate, children, phase, lastSuccessAt }: {
  activeView: ViewId
  onNavigate: (view: ViewId) => void
  children: React.ReactNode
  phase: DashboardPhase
  lastSuccessAt: Date | null
}) {
  const [mobileOpen, setMobileOpen] = useState(false)
  const active = NAV.find(item => item.id === activeView) ?? NAV[0]
  const navigate = (view: ViewId) => { onNavigate(view); setMobileOpen(false) }
  return (
    <div className="command-center">
      <aside className={`sidebar ${mobileOpen ? 'mobile-open' : ''}`} aria-label="Primary navigation">
        <div className="brand-block">
          <div className="brand-mark" aria-hidden="true"><span /><span /><span /></div>
          <div><div className="brand-name">DGAF</div><div className="brand-subtitle">Governance Command Center</div></div>
        </div>
        <nav className="nav-list">
          {NAV.map(({ id, label, sub, Icon }) => (
            <button key={id} className="nav-item" data-active={activeView === id ? 'true' : 'false'} onClick={() => navigate(id)} aria-current={activeView === id ? 'page' : undefined}>
              <Icon /><span><strong>{label}</strong><small>{sub}</small></span>
            </button>
          ))}
        </nav>
        <div className="sidebar-boundary">
          <span className="eyebrow">CONTROL BOUNDARY</span>
          <StatusChip state="not_authorized" label="NOT AUTHORIZED" compact />
          <p>Capability never becomes permission by implication.</p>
        </div>
      </aside>
      {mobileOpen && <button className="nav-scrim" aria-label="Close navigation" onClick={() => setMobileOpen(false)} />}
      <div className="workspace">
        <header className="topbar">
          <div className="topbar-title">
            <button className="icon-button mobile-menu" onClick={() => setMobileOpen(true)} aria-label="Open navigation"><MenuIcon /></button>
            <div><span className="eyebrow">DGAF / {active.id.toUpperCase()}</span><h1>{active.label}</h1></div>
          </div>
          <div className="runtime-pill"><StatusChip state={phaseState(phase)} label={phase === 'fresh' ? 'Runtime live' : phase === 'stale' ? 'Runtime stale' : phase === 'error' ? 'Runtime unavailable' : 'Connecting'} compact /><span>{lastSuccessAt ? `Updated ${lastSuccessAt.toLocaleTimeString()}` : 'Awaiting first valid snapshot'}</span></div>
        </header>
        <section className="truth-ribbon" aria-label="Canonical repository truth boundary">
          <div className="truth-ribbon-label"><span>Repository truth</span><strong>Canonical state · reconciled {TRUTH_BOUNDARY.sourceUpdated}</strong></div>
          <div className="truth-ribbon-item"><span>Program</span><strong>{TRUTH_BOUNDARY.programState}</strong></div>
          <div className="truth-ribbon-item"><span>Fail mode</span><strong>{TRUTH_BOUNDARY.failMode}</strong></div>
          <div className="truth-ribbon-item"><span>Authorization</span><StatusChip state="not_authorized" label={TRUTH_BOUNDARY.authorization} compact /></div>
          <div className="truth-ribbon-item"><span>Empirical N</span><code>N={TRUTH_BOUNDARY.empiricalN}</code></div>
          <div className="truth-ribbon-item"><span>Efficacy</span><StatusChip state="not_established" label={TRUTH_BOUNDARY.efficacy} compact /></div>
        </section>
        <main id="main-content" className="page-content">{children}</main>
      </div>
    </div>
  )
}
