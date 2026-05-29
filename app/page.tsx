// app/page.tsx  —  DGAF-Framework Dashboard
'use client'
import { useEffect, useState } from 'react'

interface HealthData {
  status: string
  psi_cubic: boolean
  version: string
  phi_star: number
  psi: number
  runtime: string
  scpe_threshold: number
  phi_checkpoints: number[]
  adapters: string[]
}

interface AuditData {
  status: string
  version: string
  turn_count: number
  stable_turns: number
  prune_events: number
  axiom_count: number
  consec_phi_fail: number
  cold_start: boolean
  cold_start_at: string
  _warning: string | null
}

const REFRESH_MS = 10_000

export default function Dashboard() {
  const [health, setHealth]     = useState<HealthData | null>(null)
  const [audit, setAudit]       = useState<AuditData | null>(null)
  const [lastPoll, setLastPoll] = useState<string>('')
  const [err, setErr]           = useState<string | null>(null)

  const poll = async () => {
    try {
      const [h, a] = await Promise.all([
        fetch('/api/health').then(r => r.json()),
        fetch('/api/audit').then(r => r.json()),
      ])
      setHealth(h)
      setAudit(a)
      setLastPoll(new Date().toLocaleTimeString())
      setErr(null)
    } catch (e: unknown) {
      setErr(String(e))
    }
  }

  useEffect(() => {
    poll()
    const id = setInterval(poll, REFRESH_MS)
    return () => clearInterval(id)
  }, [])

  const badge = (ok: boolean, label: string) => (
    <span style={{
      display: 'inline-block', padding: '2px 10px', borderRadius: 4,
      fontSize: 13, fontWeight: 700,
      background: ok ? '#16a34a' : '#dc2626', color: '#fff', marginRight: 8,
    }}>{label}</span>
  )

  return (
    <main style={{ fontFamily: 'monospace', padding: 32, maxWidth: 860,
                   margin: '0 auto', background: '#0f172a', minHeight: '100vh',
                   color: '#e2e8f0' }}>

      <h1 style={{ fontSize: 22, fontWeight: 700, marginBottom: 4 }}>
        🔷 DGAF-Framework Ensemble Dashboard
      </h1>
      <p style={{ fontSize: 12, color: '#94a3b8', marginBottom: 24 }}>
        v{health?.version ?? '…'}  ·  last poll: {lastPoll || '…'}
         ·  auto-refresh every {REFRESH_MS / 1000}s
      </p>

      {err && (
        <div style={{ background: '#7f1d1d', padding: 12, borderRadius: 6, marginBottom: 16 }}>
          ⚠️ {err}
        </div>
      )}

      {/* Cold-start warning banner */}
      {audit?.cold_start && (
        <div style={{
          background: '#78350f', border: '1px solid #d97706',
          padding: '10px 14px', borderRadius: 6, marginBottom: 16,
          fontSize: 12, color: '#fef3c7',
        }}>
          ⚠️ <strong>Cold start detected</strong> at {audit.cold_start_at} — 
          session counters reset. Upgrade to Vercel KV for persistence.
        </div>
      )}

      {/* Health row */}
      <section style={{ marginBottom: 24 }}>
        <h2 style={{ fontSize: 14, color: '#94a3b8', marginBottom: 8 }}>HEALTH</h2>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: 8 }}>
          {badge(health?.status === 'ok',    'status=ok')}
          {badge(!!health?.psi_cubic,        'psi_cubic')}
          {badge(health?.psi_cubic ?? false, `φ⋆=${health?.phi_star ?? ''}`)}
          {badge(true,                        health?.runtime ?? '...')}
        </div>
      </section>

      {/* Constants */}
      <section style={{ marginBottom: 24 }}>
        <h2 style={{ fontSize: 14, color: '#94a3b8', marginBottom: 8 }}>CONSTANTS</h2>
        <table style={{ borderCollapse: 'collapse', width: '100%' }}>
          <tbody>
            {([
              ['PSI (supergolden)',  health?.psi],
              ['PHI⋆ (conjugate)',  health?.phi_star],
              ['SCPE threshold',    health?.scpe_threshold],
              ['Phi checkpoints',   health?.phi_checkpoints?.join(', ')],
            ] as [string, unknown][]).map(([k, v]) => (
              <tr key={k}>
                <td style={{ color: '#94a3b8', paddingRight: 24, paddingBottom: 4, width: 200 }}>{k}</td>
                <td style={{ color: '#f8fafc', fontWeight: 600 }}>{String(v ?? '…')}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </section>

      {/* Session audit */}
      <section style={{ marginBottom: 24 }}>
        <h2 style={{ fontSize: 14, color: '#94a3b8', marginBottom: 8 }}>SESSION AUDIT</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3,1fr)', gap: 12 }}>
          {([
            ['Turns',              audit?.turn_count],
            ['Stable turns',       audit?.stable_turns],
            ['Prune events',       audit?.prune_events],
            ['Axiom count',        audit?.axiom_count],
            ['Phi fails (consec)', audit?.consec_phi_fail],
          ] as [string, number | undefined][]).map(([label, val]) => (
            <div key={label} style={{ background: '#1e293b', borderRadius: 6, padding: '10px 14px' }}>
              <div style={{ fontSize: 11, color: '#94a3b8' }}>{label}</div>
              <div style={{
                fontSize: 24, fontWeight: 700,
                color: audit?.cold_start ? '#64748b' : '#38bdf8',
              }}>{val ?? '…'}</div>
            </div>
          ))}
        </div>
        {audit?.cold_start && (
          <p style={{ fontSize: 11, color: '#64748b', marginTop: 8 }}>
            Counters greyed — cold start, no session data yet.
          </p>
        )}
      </section>

      {/* Adapters */}
      <section style={{ marginBottom: 24 }}>
        <h2 style={{ fontSize: 14, color: '#94a3b8', marginBottom: 8 }}>ADAPTERS</h2>
        <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6 }}>
          {(health?.adapters ?? []).map(a => (
            <span key={a} style={{
              background: '#1e3a5f', border: '1px solid #38bdf8',
              borderRadius: 4, padding: '2px 8px', fontSize: 12, color: '#93c5fd',
            }}>{a}</span>
          ))}
        </div>
      </section>

      {/* 9-Gate order */}
      <section>
        <h2 style={{ fontSize: 14, color: '#94a3b8', marginBottom: 8 }}>9-GATE ORDER</h2>
        <ol style={{ paddingLeft: 20, lineHeight: 2, fontSize: 13, color: '#cbd5e1' }}>
          {[
            'SCPE.prune() — resonant decay, T0 immune',
            'COLLEEN schema diff check',
            'RECIPROCITY.arbitrate() — PDMAL reweight',
            'DemiJoule safety gate (syntactic + DGAF 6-axis)',
            'Phi-Closure Gate — Fib checkpoints 13/21/34/55',
            'HPG Ionian gate — snap confidence to φ-lattice',
            'PRODIGY.verify(claim, confidence)',
            'APOGEE.review_artifact_seal()',
            'AMETHYST.seal() — SHA-256 TurnAuditRecord',
          ].map((g, i) => <li key={i}>{g}</li>)}
        </ol>
      </section>
    </main>
  )
}
