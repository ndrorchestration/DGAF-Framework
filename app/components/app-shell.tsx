'use client'

import { useState } from 'react'
import type { DashboardPhase } from '../hooks/use-dashboard-data'
import { TRUTH_BOUNDARY } from '../lib/governance'
import { ActivityIcon, EvidenceIcon, MenuIcon, NodesIcon, OverviewIcon, ShieldIcon, ToolsIcon } from './icons'
import { StatusChip } from './status-chip'

export type ViewId = 'overview' | 'control' | 'governance' | 'agents' | 'evidence' | 'tools'

const NAV_GROUPS = [
  {
    label: 'UNDERSTAND',
    items: [
      { id: 'overview' as const, label: 'Overview', sub: 'What DGAF is', Icon: OverviewIcon },
    ],
  },
  {
    label: 'VERIFY',
    items: [
      { id: 'evidence' as const, label: 'Evidence & Research', sub: 'Claims, provenance & experiment', Icon: EvidenceIcon },
      { id: 'governance' as const, label: 'Governance', sub: 'Lifecycle & authority', Icon: ShieldIcon },
    ],
  },
  {
    label: 'INSPECT',
    items: [
      { id: 'agents' as const, label: 'Agents & Formations', sub: 'Roles & topology', Icon: NodesIcon },
      { id: 'tools' as const, label: 'Tools', sub: 'P-07 sweep workspace', Icon: ToolsIcon },
    ],
  },
  {
    label: 'OPERATE',
    items: [
      { id: 'control' as const, label: 'Control Room', sub: 'Operator actions & runtime', Icon: ActivityIcon },
    ],
  },
]

const NAV = NAV_GROUPS.flatMap(group => group.items)

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
      <aside id="primary-navigation" className={`sidebar ${mobileOpen ? 'mobile-open' : ''}`} aria-label="Primary navigation">
        <div className="brand-block">
          <div className="brand-mark" aria-hidden="true"><span /><span /><span /></div>
          <div><div className="brand-name">DGAF</div><div className="brand-subtitle">Governance Command Center</div></div>
        </div>
        <nav className="nav-list" aria-label="DGAF audience journey">
          {NAV_GROUPS.map(group => (
            <div className="nav-group" key={group.label}>
              <span className="nav-stage">{group.label}</span>
              {group.items.map(({ id, label, sub, Icon }) => (
                <button key={id} className="nav-item" data-active={activeView === id ? 'true' : 'false'} onClick={() => navigate(id)} aria-current={activeView === id ? 'page' : undefined}>
                  <Icon /><span><strong>{label}</strong><small>{sub}</small></span>
                </button>
              ))}
            </div>
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
            <button
              className="icon-button mobile-menu"
              onClick={() => setMobileOpen(open => !open)}
              aria-label={mobileOpen ? 'Close navigation' : 'Open navigation'}
              aria-controls="primary-navigation"
              aria-expanded={mobileOpen}
            ><MenuIcon /></button>
            <div><span className="eyebrow">DGAF / {active.id.toUpperCase()}</span><h1>{active.label}</h1></div>
          </div>
          <div className="runtime-pill"><StatusChip state={phaseState(phase)} label={phase === 'fresh' ? 'Runtime live' : phase === 'stale' ? 'Runtime stale' : phase === 'error' ? 'Runtime unavailable' : 'Connecting'} compact /><span>{lastSuccessAt ? `Updated ${lastSuccessAt.toLocaleTimeString()}` : 'Awaiting first valid snapshot'}</span></div>
        </header>
        <details className="truth-beacon">
          <summary aria-label="Canonical repository truth boundary">
            <span className="truth-beacon-label">Repository truth</span>
            <strong>{TRUTH_BOUNDARY.programState}</strong>
            <StatusChip state="not_authorized" label={TRUTH_BOUNDARY.authorization} compact />
            <code>N={TRUTH_BOUNDARY.empiricalN}</code>
            <span className="truth-beacon-expand">Details</span>
          </summary>
          <div className="truth-beacon-details">
            <div><span>Fail mode</span><strong>{TRUTH_BOUNDARY.failMode}</strong></div>
            <div><span>Canonical efficacy</span><StatusChip state="not_established" label={TRUTH_BOUNDARY.efficacy} compact /></div>
            <div><span>Presentation authority</span><strong>Repository SSoT · reconciled {TRUTH_BOUNDARY.sourceUpdated}</strong></div>
          </div>
        </details>
        <main id="main-content" className="page-content">{children}</main>
      </div>
    </div>
  )
}
