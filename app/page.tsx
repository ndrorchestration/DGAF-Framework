// app/page.tsx  —  DGAF-Framework Ensemble Dashboard v2
'use client'
import { useEffect, useState, useCallback } from 'react'

// ── Types ────────────────────────────────────────────────────────────────────
interface HealthData {
  status: string; psi_cubic: boolean; version: string
  phi_star: number; psi: number; runtime: string
  scpe_threshold: number; phi_checkpoints: number[]; adapters: string[]
}
interface AuditData {
  status: string; version: string; turn_count: number; stable_turns: number
  prune_events: number; axiom_count: number; consec_phi_fail: number
  cold_start: boolean; cold_start_at: string; _warning: string | null
}
interface Agent {
  id: string; tier: string; role: string; status: string; triad_roles: string[]
}
interface Triad {
  id: string; type: string; agents: string[]; use_case: string
}
interface RosterData {
  version: string; agent_count: number; triad_count: number
  ndr_patterns: number; agents: Agent[]; triads: Triad[]
  phi_star: number; psi: number
}
interface SweepResult {
  sweep_id: string; targets_scanned: number; findings_count: number
  findings: { id: string; agent: string; target: string; severity: string; message: string }[]
  narrative: string; harmonic_score: number; swept_at: string
}

// ── Constants ─────────────────────────────────────────────────────────────────
const REFRESH_MS  = 10_000
const TIER_COLOR: Record<string, string> = {
  L5: '#a78bfa', L4: '#38bdf8', L3: '#34d399', S1: '#fb923c', S2: '#fb923c', S3: '#fb923c',
}
const STATUS_COLOR: Record<string, string> = {
  active: '#16a34a', partial: '#ca8a04', foundational: '#475569',
}
const SEV_COLOR: Record<string, string> = {
  HIGH: '#dc2626', MEDIUM: '#ca8a04', LOW: '#2563eb', INFO: '#475569',
}
const TRIAD_TYPE_COLOR: Record<string, string> = {
  triumvirate: '#a78bfa', conducted: '#38bdf8', consensus: '#34d399',
}

// ── Sub-components ────────────────────────────────────────────────────────────
function Badge({ ok, label }: { ok: boolean; label: string }) {
  return (
    <span style={{
      display: 'inline-block', padding: '2px 10px', borderRadius: 4,
      fontSize: 13, fontWeight: 700,
      background: ok ? '#16a34a' : '#dc2626', color: '#fff', marginRight: 8,
    }}>{label}</span>
  )
}

function SectionHead({ title }: { title: string }) {
  return <h2 style={{ fontSize: 13, color: '#64748b', letterSpacing: '0.12em',
    textTransform: 'uppercase', marginBottom: 10, marginTop: 0 }}>{title}</h2>
}

function Pill({ label, color }: { label: string; color: string }) {
  return (
    <span style={{
      background: color + '22', border: `1px solid ${color}`,
      color, borderRadius: 4, padding: '1px 7px', fontSize: 11, fontWeight: 700,
      display: 'inline-block',
    }}>{label}</span>
  )
}

function AgentRow({ a }: { a: Agent }) {
  const tc = TIER_COLOR[a.tier] ?? '#94a3b8'
  const sc = STATUS_COLOR[a.status] ?? '#94a3b8'
  return (
    <tr style={{ borderBottom: '1px solid #1e293b' }}>
      <td style={{ padding: '7px 12px 7px 0', fontWeight: 700, color: '#f1f5f9', minWidth: 120 }}>
        {a.id}
      </td>
      <td style={{ padding: '7px 8px' }}>
        <Pill label={a.tier} color={tc} />
      </td>
      <td style={{ padding: '7px 8px', color: '#cbd5e1', fontSize: 12, maxWidth: 260 }}>
        {a.role}
      </td>
      <td style={{ padding: '7px 8px' }}>
        <Pill label={a.status} color={sc} />
      </td>
      <td style={{ padding: '7px 0', fontSize: 11, color: '#64748b' }}>
        {a.triad_roles.join(' · ')}
      </td>
    </tr>
  )
}

function TriadCard({ t }: { t: Triad }) {
  const tc = TRIAD_TYPE_COLOR[t.type] ?? '#94a3b8'
  return (
    <div style={{
      background: '#1e293b', borderRadius: 8, padding: '12px 14px',
      border: `1px solid ${tc}44`,
    }}>
      <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 6 }}>
        <span style={{ fontWeight: 700, color: '#f1f5f9', fontSize: 13 }}>{t.id}</span>
        <Pill label={t.type} color={tc} />
      </div>
      <div style={{ display: 'flex', flexWrap: 'wrap', gap: 4, marginBottom: 6 }}>
        {t.agents.map(a => (
          <span key={a} style={{
            background: '#0f172a', border: '1px solid #334155',
            borderRadius: 3, padding: '1px 6px', fontSize: 11, color: '#94a3b8',
          }}>{a}</span>
        ))}
      </div>
      <div style={{ fontSize: 11, color: '#64748b', lineHeight: 1.5 }}>{t.use_case}</div>
    </div>
  )
}

// ── Main Dashboard ────────────────────────────────────────────────────────────
export default function Dashboard() {
  const [health,      setHealth]      = useState<HealthData | null>(null)
  const [audit,       setAudit]       = useState<AuditData  | null>(null)
  const [roster,      setRoster]      = useState<RosterData | null>(null)
  const [lastPoll,    setLastPoll]    = useState('')
  const [err,         setErr]         = useState<string | null>(null)
  const [sweepInput,  setSweepInput]  = useState('api/health.py\napp/api/health/route.ts\nrequirements.txt')
  const [sweepResult, setSweepResult] = useState<SweepResult | null>(null)
  const [sweeping,    setSweeping]    = useState(false)
  const [activeTab,   setActiveTab]   = useState<'health'|'roster'|'triads'|'sweep'>('health')

  const poll = useCallback(async () => {
    try {
      const [h, a, r] = await Promise.all([
        fetch('/api/health').then(x => x.json()),
        fetch('/api/audit').then(x => x.json()),
        fetch('/api/roster').then(x => x.json()),
      ])
      setHealth(h); setAudit(a); setRoster(r)
      setLastPoll(new Date().toLocaleTimeString())
      setErr(null)
    } catch (e: unknown) { setErr(String(e)) }
  }, [])

  useEffect(() => {
    poll()
    const id = setInterval(poll, REFRESH_MS)
    return () => clearInterval(id)
  }, [poll])

  const runSweep = async () => {
    setSweeping(true)
    try {
      const targets = sweepInput.split('\n').map(s => s.trim()).filter(Boolean)
      const r = await fetch('/api/sweep', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ targets }),
      })
      setSweepResult(await r.json())
    } catch (e: unknown) { setErr(String(e)) }
    finally { setSweeping(false) }
  }

  const tabs: { id: typeof activeTab; label: string }[] = [
    { id: 'health',  label: '🔷 Health & Audit' },
    { id: 'roster',  label: '🤖 Agent Roster' },
    { id: 'triads',  label: '🔺 Triads' },
    { id: 'sweep',   label: '🔍 P-07 Sweep' },
  ]

  return (
    <main style={{
      fontFamily: 'monospace', padding: '28px 32px', maxWidth: 960,
      margin: '0 auto', background: '#0f172a', minHeight: '100vh', color: '#e2e8f0',
    }}>

      {/* Header */}
      <div style={{ display: 'flex', alignItems: 'baseline', gap: 16, marginBottom: 4 }}>
        <h1 style={{ fontSize: 20, fontWeight: 700, margin: 0 }}>DGAF-Framework Ensemble</h1>
        <span style={{ fontSize: 12, color: '#475569' }}>
          v{health?.version ?? '…'} · {roster?.agent_count ?? '…'} agents · NDR P-{roster?.ndr_patterns ?? '…'}
        </span>
      </div>
      <p style={{ fontSize: 11, color: '#475569', marginBottom: 20 }}>
        last poll: {lastPoll || '…'} · auto-refresh {REFRESH_MS / 1000}s · runtime: {health?.runtime ?? '…'}
      </p>

      {err && (
        <div style={{ background: '#7f1d1d', padding: 10, borderRadius: 6, marginBottom: 12, fontSize: 12 }}>
          ⚠️ {err}
        </div>
      )}
      {audit?.cold_start && (
        <div style={{
          background: '#78350f', border: '1px solid #d97706',
          padding: '8px 12px', borderRadius: 6, marginBottom: 12, fontSize: 11, color: '#fef3c7',
        }}>
          ⚠️ <strong>Cold start</strong> at {audit.cold_start_at} — counters reset.
          Wire Vercel KV for persistence.
        </div>
      )}

      {/* Tab bar */}
      <div style={{ display: 'flex', gap: 4, marginBottom: 24, borderBottom: '1px solid #1e293b' }}>
        {tabs.map(tab => (
          <button key={tab.id} onClick={() => setActiveTab(tab.id)} style={{
            background: activeTab === tab.id ? '#1e293b' : 'transparent',
            border: 'none',
            borderBottom: activeTab === tab.id ? '2px solid #38bdf8' : '2px solid transparent',
            color: activeTab === tab.id ? '#f1f5f9' : '#64748b',
            padding: '6px 14px', fontSize: 12, fontWeight: 700, cursor: 'pointer',
            fontFamily: 'monospace', borderRadius: '4px 4px 0 0',
          }}>{tab.label}</button>
        ))}
      </div>

      {/* TAB: Health & Audit */}
      {activeTab === 'health' && (
        <div>
          <section style={{ marginBottom: 24 }}>
            <SectionHead title="Health" />
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
              <Badge ok={health?.status === 'ok'}  label="status=ok" />
              <Badge ok={!!health?.psi_cubic}       label="psi_cubic" />
              <Badge ok={!!health?.psi_cubic}       label={`φ⋆=${health?.phi_star ?? '…'}`} />
              <Badge ok={true}                      label={health?.runtime ?? '…'} />
            </div>
          </section>
          <section style={{ marginBottom: 24 }}>
            <SectionHead title="Constants" />
            <table style={{ borderCollapse: 'collapse', width: '100%' }}>
              <tbody>
                {([
                  ['PSI (supergolden)', health?.psi],
                  ['PHI⋆ (conjugate)', health?.phi_star],
                  ['SCPE threshold',   health?.scpe_threshold],
                  ['Phi checkpoints',  health?.phi_checkpoints?.join(', ')],
                ] as [string, unknown][]).map(([k, v]) => (
                  <tr key={k}>
                    <td style={{ color: '#64748b', paddingRight: 24, paddingBottom: 4, width: 200, fontSize: 12 }}>{k}</td>
                    <td style={{ color: '#f8fafc', fontWeight: 600, fontSize: 13 }}>{String(v ?? '…')}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </section>
          <section style={{ marginBottom: 24 }}>
            <SectionHead title="Session Audit" />
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3,1fr)', gap: 10 }}>
              {([
                ['Turns',        audit?.turn_count],
                ['Stable',       audit?.stable_turns],
                ['Prune events', audit?.prune_events],
                ['Axioms',       audit?.axiom_count],
                ['φ fails',      audit?.consec_phi_fail],
              ] as [string, number | undefined][]).map(([label, val]) => (
                <div key={label} style={{ background: '#1e293b', borderRadius: 6, padding: '8px 12px' }}>
                  <div style={{ fontSize: 10, color: '#475569', textTransform: 'uppercase', letterSpacing: '0.1em' }}>{label}</div>
                  <div style={{ fontSize: 22, fontWeight: 700, color: audit?.cold_start ? '#334155' : '#38bdf8' }}>
                    {val ?? '…'}
                  </div>
                </div>
              ))}
            </div>
            {audit?.cold_start && (
              <p style={{ fontSize: 11, color: '#64748b', marginTop: 8 }}>
                Counters greyed — cold start, no session data yet.
              </p>
            )}
          </section>
          <section style={{ marginBottom: 24 }}>
            <SectionHead title="Adapters" />
            <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
              {(health?.adapters ?? []).map(a => (
                <span key={a} style={{
                  background: '#1e3a5f', border: '1px solid #38bdf8',
                  borderRadius: 4, padding: '2px 8px', fontSize: 12, color: '#93c5fd',
                }}>{a}</span>
              ))}
            </div>
          </section>
          <section>
            <SectionHead title="9-Gate Order" />
            <ol style={{ paddingLeft: 20, lineHeight: 2, fontSize: 12, color: '#94a3b8', margin: 0 }}>
              {[
                'SCPE.prune() — resonant decay, T0 immune',
                'COLLEEN schema diff check',
                'RECIPROCITY.arbitrate() — PDMAL reweight',
                'DemiJoule safety gate (syntactic + DGAF 6-axis)',
                'Phi-Closure Gate — Fib[13,21,34,55]',
                'HPG Ionian gate — snap confidence to φ-lattice',
                'PRODIGY.verify(claim, confidence)',
                'APOGEE.review_artifact_seal()',
                'AMETHYST.seal() — TurnAuditRecord',
              ].map((g, i) => <li key={i}>{g}</li>)}
            </ol>
          </section>
        </div>
      )}

      {/* TAB: Agent Roster */}
      {activeTab === 'roster' && (
        <div>
          <div style={{ display: 'flex', gap: 20, marginBottom: 14, fontSize: 12 }}>
            <span style={{ color: '#64748b' }}>
              {roster?.agent_count ?? '…'} agents · {roster?.triad_count ?? '…'} triads ·
              NDR P-{roster?.ndr_patterns ?? '…'}
            </span>
            <span style={{ color: '#64748b' }}>
              φ⋆ = {roster?.phi_star?.toFixed(10) ?? '…'} · ψ = {roster?.psi ?? '…'}
            </span>
          </div>
          <div style={{ overflowX: 'auto' }}>
            <table style={{ borderCollapse: 'collapse', width: '100%', fontSize: 13 }}>
              <thead>
                <tr style={{ borderBottom: '2px solid #334155' }}>
                  {['Agent', 'Tier', 'Role', 'Status', 'Triad Roles'].map(h => (
                    <th key={h} style={{
                      textAlign: 'left', padding: '4px 8px 8px',
                      color: '#475569', fontSize: 11,
                      textTransform: 'uppercase', letterSpacing: '0.1em',
                    }}>{h}</th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {(roster?.agents ?? []).map(a => <AgentRow key={a.id} a={a} />)}
              </tbody>
            </table>
          </div>
        </div>
      )}

      {/* TAB: Triads */}
      {activeTab === 'triads' && (
        <div>
          <div style={{ marginBottom: 14, fontSize: 12, color: '#64748b', display: 'flex', gap: 8, flexWrap: 'wrap' }}>
            <span>{roster?.triad_count ?? '…'} canonical formations · types:</span>
            {['triumvirate','conducted','consensus'].map(t => (
              <Pill key={t} label={t} color={TRIAD_TYPE_COLOR[t]} />
            ))}
          </div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(280px,1fr))', gap: 12 }}>
            {(roster?.triads ?? []).map(t => <TriadCard key={t.id} t={t} />)}
          </div>
        </div>
      )}

      {/* TAB: P-07 Sweep */}
      {activeTab === 'sweep' && (
        <div>
          <p style={{ fontSize: 12, color: '#64748b', marginBottom: 14 }}>
            P-07 Co-Orchestration Sweep · Amethyst[C] + COLLEEN[detect] + Herald[comms]
          </p>
          <SectionHead title="Target Paths (one per line)" />
          <textarea
            value={sweepInput}
            onChange={e => setSweepInput(e.target.value)}
            rows={5}
            style={{
              width: '100%', background: '#1e293b', border: '1px solid #334155',
              borderRadius: 6, color: '#f1f5f9', fontFamily: 'monospace',
              fontSize: 12, padding: 10, resize: 'vertical', boxSizing: 'border-box',
              marginBottom: 10,
            }}
          />
          <button
            onClick={runSweep}
            disabled={sweeping}
            style={{
              background: sweeping ? '#334155' : '#2563eb',
              color: '#fff', border: 'none', borderRadius: 6,
              padding: '8px 20px', fontFamily: 'monospace', fontSize: 13,
              fontWeight: 700, cursor: sweeping ? 'not-allowed' : 'pointer',
              marginBottom: 20,
            }}
          >
            {sweeping ? '⏳ Sweeping…' : '▶ Run Sweep'}
          </button>

          {sweepResult && (
            <div>
              <div style={{
                background: '#1e293b', borderRadius: 8, padding: '12px 16px', marginBottom: 16,
                border: '1px solid #334155',
              }}>
                <div style={{ fontSize: 11, color: '#64748b', marginBottom: 6 }}>
                  sweep_id: <span style={{ color: '#38bdf8' }}>{sweepResult.sweep_id}</span>
                  &nbsp;·&nbsp;{sweepResult.targets_scanned} targets
                  &nbsp;·&nbsp;{sweepResult.findings_count} findings
                  &nbsp;·&nbsp;harmonic score: {sweepResult.harmonic_score}
                </div>
                <p style={{ fontSize: 12, color: '#cbd5e1', margin: 0, lineHeight: 1.6 }}>
                  {sweepResult.narrative}
                </p>
              </div>
              {sweepResult.findings.length > 0 && (
                <div>
                  <SectionHead title="Findings" />
                  {sweepResult.findings.map(f => (
                    <div key={f.id} style={{
                      display: 'flex', gap: 10, alignItems: 'flex-start',
                      padding: '8px 0', borderBottom: '1px solid #1e293b', fontSize: 12,
                    }}>
                      <span style={{ minWidth: 64 }}>
                        <Pill label={f.severity} color={SEV_COLOR[f.severity] ?? '#64748b'} />
                      </span>
                      <span style={{ color: '#94a3b8', minWidth: 72 }}>[{f.agent}]</span>
                      <span style={{ color: '#64748b', minWidth: 200 }}>{f.target}</span>
                      <span style={{ color: '#cbd5e1', flex: 1 }}>{f.message}</span>
                    </div>
                  ))}
                </div>
              )}
            </div>
          )}
        </div>
      )}
    </main>
  )
}
