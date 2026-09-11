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
  const tiers = useMemo(() => Array.from(new Set((roster?.agents ?? []).map(agent => agent.tier))), [roster])
  const statuses = useMemo(() => Array.from(new Set((roster?.agents ?? []).map(agent => agent.status))), [roster])
  const agentById = useMemo(() => new Map((roster?.agents ?? []).map(agent => [agent.id, agent])), [roster])
  const agents = useMemo(() => (roster?.agents ?? []).filter(agent => {
    const haystack = `${agent.id} ${agentDisplayName(agent.id)} ${agent.role} ${agent.triad_roles.join(' ')}`.toLowerCase()
    return (!query || haystack.includes(query.toLowerCase())) && (tier === 'all' || agent.tier === tier) && (status === 'all' || agent.status === status)
  }), [roster, query, tier, status])

  return <div className="view-stack">
    <section className="section-heading standalone">
      <div>
        <span className="eyebrow">AGENTS & FORMATIONS</span>
        <h2>Understand the formation before the codename.</h2>
        <p>DGAF presents runtime roles, formation membership, and topology before project-local identities. The roster is observability data, not evidence of authority or efficacy.</p>
      </div>
    </section>

    {!roster ? <div className="empty-state panel"><StatusChip state="loading"/><h3>Waiting for a validated roster snapshot</h3><p>The public translation layer remains available, but runtime roster facts will not be invented.</p></div> : <>
      <section className="roster-snapshot panel panel-accent" aria-labelledby="roster-snapshot-title">
        <div>
          <span className="eyebrow accent">VALIDATED RUNTIME SNAPSHOT</span>
          <h3 id="roster-snapshot-title">Current formation inventory</h3>
          <p>This surface describes the runtime roster returned by the application. It does not grant authority, establish scientific state, or widen any agent role.</p>
        </div>
        <div className="roster-metrics" aria-label="Roster summary">
          <div><span>Agents</span><strong>{roster.agent_count}</strong></div>
          <div><span>Formations</span><strong>{roster.triad_count}</strong></div>
          <div><span>NDR patterns</span><strong>{roster.ndr_patterns}</strong></div>
          <div><span>Version</span><strong className="mono">{roster.version}</strong></div>
        </div>
        <div className="roster-provenance"><span>Source</span><strong>{roster.rosterSource ?? 'Runtime roster endpoint'}</strong><span>Format</span><strong>{roster.rosterFormat ?? 'Validated response shape'}</strong></div>
      </section>

      <section aria-labelledby="formation-system-title">
        <div className="section-heading">
          <div><span className="eyebrow">FORMATION TOPOLOGY</span><h3 id="formation-system-title">Runtime coordination groups</h3><p>Each formation is shown as a bounded coordination context. Membership does not imply broader authority.</p></div>
        </div>
        <div className="formation-system">
          {roster.triads.length ? roster.triads.map(triad => <article className="formation-row panel" key={triad.id}>
            <div className="formation-summary">
              <div><span className="eyebrow">{triad.type}</span><h4>{triad.id.replaceAll('_', ' ')}</h4></div>
              <p>{triad.use_case}</p>
            </div>
            <div className="formation-rail" aria-label={`${triad.id} members`}>
              {triad.agents.map((id, index) => {
                const agent = agentById.get(id)
                return <div className="formation-member-wrap" key={id}>
                  {index > 0 && <span className="formation-link" aria-hidden="true" />}
                  <div className="formation-member">
                    <div className="formation-member-top"><span className="tier-mark">{agent?.tier ?? 'UNMAPPED'}</span><StatusChip state={agent ? normalizeRuntimeStatus(agent.status) : 'unknown'} label={agent?.status?.toUpperCase() ?? 'UNKNOWN'} compact /></div>
                    <strong>{agentDisplayName(id)}</strong>
                    <p>{agent?.role ?? 'Runtime role unavailable in current snapshot.'}</p>
                  </div>
                </div>
              })}
            </div>
          </article>) : <div className="empty-state panel"><StatusChip state="unknown"/><h3>No validated formations in this snapshot</h3><p>The interface will not infer topology from agent names or roles.</p></div>}
        </div>
      </section>

      <section aria-labelledby="roster-directory-title">
        <div className="section-heading"><div><span className="eyebrow">ROSTER DIRECTORY</span><h3 id="roster-directory-title">Inspect runtime roles</h3><p>Search and filter the validated snapshot without changing the source data.</p></div></div>
        <div className="panel filter-bar" aria-label="Agent filters">
          <label><span>Search</span><input value={query} onChange={event => setQuery(event.target.value)} placeholder="Role, codename, formation…" /></label>
          <label><span>Tier</span><select value={tier} onChange={event => setTier(event.target.value)}><option value="all">All tiers</option>{tiers.map(value => <option key={value}>{value}</option>)}</select></label>
          <label><span>Status</span><select value={status} onChange={event => setStatus(event.target.value)}><option value="all">All statuses</option>{statuses.map(value => <option key={value}>{value}</option>)}</select></label>
          <div className="filter-count"><strong>{agents.length}</strong><span>of {roster.agent_count} agents</span></div>
        </div>
        <div className="roster-directory panel" role="table" aria-label="Validated runtime agent roster">
          <div className="roster-directory-head" role="row">
            <span role="columnheader">Function / identity</span><span role="columnheader">Runtime role</span><span role="columnheader">Tier / status</span><span role="columnheader">Formation roles</span>
          </div>
          {agents.length ? agents.map(agent => <article className="roster-row" role="row" key={agent.id}>
            <div role="cell"><strong>{agentDisplayName(agent.id)}</strong><code>{agent.id}</code></div>
            <p role="cell">{agent.role}</p>
            <div className="roster-state" role="cell"><span className="tier-mark">{agent.tier}</span><StatusChip state={normalizeRuntimeStatus(agent.status)} label={agent.status.toUpperCase()} compact /></div>
            <div className="tag-cloud" role="cell">{agent.triad_roles.map(role => <span className="tag" key={role}>{role}</span>)}</div>
          </article>) : <div className="roster-no-results"><StatusChip state="unknown" label="NO MATCHES" compact/><span>No validated agent matches the current filters.</span></div>}
        </div>
      </section>
    </>}

    <div className="alert info"><strong>Ontology boundary</strong><span>{ONTOLOGY_NOTE}</span></div>
  </div>
}
