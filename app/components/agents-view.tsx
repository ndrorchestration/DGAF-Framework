'use client'

import { useMemo, useState } from 'react'
import { ONTOLOGY_NOTE, agentDisplayName } from '../lib/public-translation'
import { normalizeRuntimeStatus } from '../lib/status'
import type { RosterData } from '../lib/types'
import { StatusChip } from './status-chip'

export function AgentsView({ roster }: { roster: RosterData | null }) {
  const [query, setQuery] = useState('')
  const [tier, setTier] = useState('all')
  const [status, setStatus] = useState('all')
  const tiers = useMemo(() => Array.from(new Set((roster?.agents ?? []).map(a => a.tier))), [roster])
  const statuses = useMemo(() => Array.from(new Set((roster?.agents ?? []).map(a => a.status))), [roster])
  const agents = useMemo(() => (roster?.agents ?? []).filter(agent => {
    const haystack = `${agent.id} ${agentDisplayName(agent.id)} ${agent.role} ${agent.triad_roles.join(' ')}`.toLowerCase()
    return (!query || haystack.includes(query.toLowerCase())) && (tier === 'all' || agent.tier === tier) && (status === 'all' || agent.status === status)
  }), [roster, query, tier, status])

  return <div className="view-stack">
    <section className="section-heading standalone"><div><span className="eyebrow">AGENTS & FORMATIONS</span><h2>Function first. Codename second.</h2><p>Runtime roster facts remain visible without forcing external readers to decode project-local identities before understanding the role.</p></div></section>
    <section className="panel filter-bar" aria-label="Agent filters">
      <label><span>Search</span><input value={query} onChange={event => setQuery(event.target.value)} placeholder="Role, codename, formation…" /></label>
      <label><span>Tier</span><select value={tier} onChange={event => setTier(event.target.value)}><option value="all">All tiers</option>{tiers.map(value => <option key={value}>{value}</option>)}</select></label>
      <label><span>Status</span><select value={status} onChange={event => setStatus(event.target.value)}><option value="all">All statuses</option>{statuses.map(value => <option key={value}>{value}</option>)}</select></label>
      <div className="filter-count"><strong>{agents.length}</strong><span>of {roster?.agent_count ?? 0} agents</span></div>
    </section>
    {!roster ? <div className="empty-state panel"><StatusChip state="loading"/><h3>Waiting for a validated roster snapshot</h3><p>The public translation layer remains available, but runtime roster facts will not be invented.</p></div> : <div className="agent-grid">{agents.map(agent => <article className="agent-card panel" key={agent.id}><div className="agent-top"><span className="tier-mark">{agent.tier}</span><StatusChip state={normalizeRuntimeStatus(agent.status)} label={agent.status.toUpperCase()} compact/></div><h3>{agentDisplayName(agent.id)}</h3><p className="agent-role">{agent.role}</p><div className="tag-cloud">{agent.triad_roles.map(role => <span className="tag" key={role}>{role}</span>)}</div></article>)}</div>}
    <section><div className="section-heading"><div><span className="eyebrow">FORMATIONS</span><h3>Runtime triads</h3></div></div><div className="formation-grid">{(roster?.triads ?? []).map(triad => <article className="formation-card panel" key={triad.id}><div className="card-header"><h4>{triad.id.replaceAll('_', ' ')}</h4><span className="tag violet">{triad.type}</span></div><p>{triad.use_case}</p><div className="member-list">{triad.agents.map(id => <span key={id}>{agentDisplayName(id)}</span>)}</div></article>)}</div></section>
    <div className="alert info"><strong>Ontology boundary</strong><span>{ONTOLOGY_NOTE}</span></div>
  </div>
}
