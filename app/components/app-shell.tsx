'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { useEffect, useRef, useState } from 'react'
import type { DashboardPhase } from '../hooks/use-dashboard-data'
import { NAV_ITEMS, navigationForPath, type ViewId } from '../lib/navigation'
import { useDashboardRuntime } from './dashboard-runtime-provider'
import { ActivityIcon, EvidenceIcon, MenuIcon, NodesIcon, OverviewIcon, ShieldIcon, ToolsIcon } from './icons'
import { StatusChip } from './status-chip'

function iconForView(view: ViewId) {
  if (view === 'overview') return OverviewIcon
  if (view === 'control') return ActivityIcon
  if (view === 'evidence') return EvidenceIcon
  if (view === 'governance') return ShieldIcon
  if (view === 'tools') return ToolsIcon
  return NodesIcon
}

function phaseState(phase: DashboardPhase) {
  if (phase === 'fresh') return 'pass' as const
  if (phase === 'stale') return 'stale' as const
  if (phase === 'error') return 'unavailable' as const
  return 'loading' as const
}

export function AppShell({ children }: { children: React.ReactNode }) {
  const [mobileOpen, setMobileOpen] = useState(false)
  const menuButtonRef = useRef<HTMLButtonElement>(null)
  const navigationRef = useRef<HTMLElement>(null)
  const pathname = usePathname()
  const active = navigationForPath(pathname)
  const activeView = active.id
  const { phase, lastSuccessAt } = useDashboardRuntime()

  useEffect(() => {
    if (!mobileOpen) return
    navigationRef.current?.querySelector<HTMLAnchorElement>('a.nav-item')?.focus()
    const handleKeyDown = (event: KeyboardEvent) => {
      if (event.key !== 'Escape') return
      setMobileOpen(false)
      requestAnimationFrame(() => menuButtonRef.current?.focus())
    }
    window.addEventListener('keydown', handleKeyDown)
    return () => window.removeEventListener('keydown', handleKeyDown)
  }, [mobileOpen])

  return (
    <div className="command-center">
      <a className="skip-link" href="#main-content">Skip to main content</a>
      <aside id="primary-navigation" ref={navigationRef} className={`sidebar ${mobileOpen ? 'mobile-open' : ''}`} aria-label="Primary navigation">
        <div className="brand-block">
          <div className="brand-mark" aria-hidden="true"><span /><span /><span /></div>
          <div><div className="brand-name">DGAF</div><div className="brand-subtitle">Governance Command Center</div></div>
        </div>
        <nav className="nav-list">
          {NAV_ITEMS.map(({ id, href, label, sub }) => {
            const Icon = iconForView(id)
            return (
              <Link key={id} href={href} className="nav-item" data-active={activeView === id ? 'true' : 'false'} onClick={() => setMobileOpen(false)} aria-current={activeView === id ? 'page' : undefined}>
                <Icon /><span><strong>{label}</strong><small>{sub}</small></span>
              </Link>
            )
          })}
        </nav>
        <div className="sidebar-boundary">
          <span className="eyebrow">CONTROL BOUNDARY</span>
          <StatusChip state="not_authorized" label="NOT AUTHORIZED" compact />
          <p>Capability never becomes permission by implication.</p>
        </div>
      </aside>
      {mobileOpen && <button className="nav-scrim" aria-label="Close navigation" onClick={() => { setMobileOpen(false); requestAnimationFrame(() => menuButtonRef.current?.focus()) }} />}
      <div className="workspace">
        <header className="topbar">
          <div className="topbar-title">
            <button ref={menuButtonRef} className="icon-button mobile-menu" onClick={() => setMobileOpen(true)} aria-label="Open navigation" aria-expanded={mobileOpen} aria-controls="primary-navigation"><MenuIcon /></button>
            <div><span className="eyebrow">DGAF / {active.id.toUpperCase()}</span><h1>{active.label}</h1></div>
          </div>
          <div className="runtime-pill"><StatusChip state={phaseState(phase)} label={phase === 'fresh' ? 'Runtime live' : phase === 'stale' ? 'Runtime stale' : phase === 'error' ? 'Runtime unavailable' : 'Connecting'} compact /><span>{lastSuccessAt ? `Updated ${lastSuccessAt.toLocaleTimeString()}` : 'Awaiting first valid snapshot'}</span></div>
        </header>
        <main id="main-content" className="page-content" tabIndex={-1}>{children}</main>
      </div>
    </div>
  )
}
