import type { DashboardPhase } from '../hooks/use-dashboard-data'
import { normalizeRuntimeStatus } from '../lib/status'
import type { DashboardSnapshot } from '../lib/types'
import { DecisionFrontier } from './decision-frontier'
import { RefreshIcon } from './icons'
import { StatusChip } from './status-chip'

export function ControlRoomView({ snapshot, phase, error, lastSuccessAt, onRefresh }: {
  snapshot: DashboardSnapshot | null
  phase: DashboardPhase
  error: string | null
  lastSuccessAt: Date | null
  onRefresh: () => void
}) {
  const health = snapshot?.health
  const audit = snapshot?.audit
  const loading = phase === 'loading' && !snapshot
  return <div className="view-stack">
    <section className="section-heading standalone"><div><span className="eyebrow">OPERATIONS</span><h2>Runtime observability without authority inflation</h2><p>Live application health is shown separately from repository governance and scientific state.</p></div><button className="button ghost" onClick={onRefresh}><RefreshIcon /> Refresh</button></section>
    {(phase === 'stale' || phase === 'error') && <div className={`alert ${phase === 'stale' ? 'warning' : 'danger'}`} role="status"><strong>{phase === 'stale' ? 'Showing last valid snapshot.' : 'Runtime data unavailable.'}</strong><span>{error ?? 'A refresh did not complete successfully.'}</span></div>}
    <div className="metric-grid">
      <article className="metric-card panel"><span>Runtime health</span>{loading ? <StatusChip state="loading"/> : <StatusChip state={health ? normalizeRuntimeStatus(health.status) : 'unavailable'} label={health?.status?.toUpperCase() ?? 'UNAVAILABLE'}/>}<small>{health?.runtime ?? 'No validated runtime snapshot'}</small></article>
      <article className="metric-card panel"><span>Version</span><strong className="mono">{health?.version ?? '—'}</strong><small>Runtime-reported ensemble version</small></article>
      <article className="metric-card panel"><span>PSI cubic check</span>{loading ? <StatusChip state="loading"/> : <StatusChip state={health ? (health.psi_cubic ? 'pass' : 'failed') : 'unknown'} label={health ? (health.psi_cubic ? 'PASS' : 'FAIL') : 'UNKNOWN'}/>}<small>Technical runtime predicate only</small></article>
      <article className="metric-card panel"><span>Last valid poll</span><strong>{lastSuccessAt ? lastSuccessAt.toLocaleTimeString() : '—'}</strong><small>Refresh cadence: 10 seconds</small></article>
    </div>
    <div className="split-grid">
      <section className="panel"><div className="section-heading"><div><span className="eyebrow">SESSION AUDIT</span><h3>Ephemeral counters</h3></div>{audit?.cold_start && <StatusChip state="open" label="COLD START"/>}</div>
        <div className="audit-grid">{[
          ['Turns', audit?.turn_count], ['Stable turns', audit?.stable_turns], ['Prune events', audit?.prune_events], ['Axioms', audit?.axiom_count], ['Consecutive φ fails', audit?.consec_phi_fail],
        ].map(([label, value]) => <div key={String(label)}><span>{label}</span><strong>{value ?? '—'}</strong></div>)}</div>
        <p className="telemetry-note">These counters are serverless in-memory telemetry and can reset on cold start. They are not durable governance evidence.</p>
        {audit?._warning && <div className="inline-warning">{audit._warning}</div>}
      </section>
      <section className="panel"><span className="eyebrow">ADAPTER SURFACE</span><h3>Connected runtime adapters</h3><div className="tag-cloud">{(health?.adapters ?? []).map(adapter => <span className="tag" key={adapter}>{adapter}</span>)}{!health?.adapters?.length && <span className="muted">No validated adapter list available.</span>}</div><div className="constants-table"><div><span>PSI</span><code>{health?.psi ?? '—'}</code></div><div><span>PHI⋆</span><code>{health?.phi_star ?? '—'}</code></div><div><span>SCPE threshold</span><code>{health?.scpe_threshold ?? '—'}</code></div><div><span>Phi checkpoints</span><code>{health?.phi_checkpoints?.join(' · ') ?? '—'}</code></div></div></section>
    </div>
    <DecisionFrontier showOperatorHandoff />
  </div>
}
