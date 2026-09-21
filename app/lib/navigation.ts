export type ViewId = 'overview' | 'control' | 'governance' | 'state-space' | 'agents' | 'evidence' | 'tools'

export type NavigationItem = {
  id: ViewId
  href: string
  label: string
  sub: string
}

export const NAV_ITEMS: readonly NavigationItem[] = [
  { id: 'overview', href: '/', label: 'Overview', sub: 'What DGAF is' },
  { id: 'control', href: '/control', label: 'Control Room', sub: 'Runtime telemetry' },
  { id: 'evidence', href: '/evidence', label: 'Evidence & Research', sub: 'Claims & experiment state' },
  { id: 'governance', href: '/governance', label: 'Governance', sub: 'Lifecycle & authority' },
  { id: 'state-space', href: '/state-space', label: 'State Space', sub: 'Reachability model' },
  { id: 'agents', href: '/agents', label: 'Agents & Formations', sub: 'Roles & topology' },
  { id: 'tools', href: '/tools', label: 'Tools', sub: 'P-07 sweep workspace' },
]

export function navigationForPath(pathname: string): NavigationItem {
  return NAV_ITEMS.find(item => item.href === pathname) ?? NAV_ITEMS[0]
}
