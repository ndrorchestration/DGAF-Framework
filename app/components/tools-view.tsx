'use client'

import { useMemo, useState } from 'react'
import { runSweep } from '../lib/api'
import { SWEEP_DEFAULT_INPUT } from '../lib/tools-defaults'
import type { SweepResult } from '../lib/types'
import { StatusChip } from './status-chip'

const SEVERITIES = ['ALL', 'HIGH', 'MEDIUM', 'LOW', 'INFO'] as const

export function ToolsView() {
  const [input, setInput] = useState(SWEEP_DEFAULT_INPUT)
  const [result, setResult] = useState<SweepResult | null>(null)
  const [busy, setBusy] = useState(false)
  const [error, setError] = useState<string | null>(null)
  const [severity, setSeverity] = useState<(typeof SEVERITIES)[number]>('ALL')
  const [copyState, setCopyState] = useState('')
  const findings = useMemo(() => (result?.findings ?? []).filter(item => severity === 'ALL' || item.severity === severity), [result, severity])

  async function execute() {
    const targets = Array.from(new Set(input.split('\n').map(value => value.trim()).filter(Boolean)))
    if (!targets.length) { setError('Enter at least one repository target before running the sweep.'); return }
    setBusy(true); setError(null); setCopyState('')
    try { setResult(await runSweep(targets)) } catch (caught) { setError(caught instanceof Error ? caught.message : String(caught)) } finally { setBusy(false) }
  }

  async function copyResult() {
    if (!result) return
    if (!navigator.clipboard) { setCopyState('Clipboard access is unavailable in this browser.'); return }
    try { await navigator.clipboard.writeText(JSON.stringify(result, null, 2)); setCopyState('Result JSON copied.') } catch { setCopyState('Clipboard write failed.') }
  }

  return <div className="view-stack">
    <section className="section-heading standalone"><div><span className="eyebrow">WORKING SURFACE</span><h2>P-07 Co-Orchestration Sweep</h2><p>Analyze supplied repository paths for known integration concerns. This endpoint plans findings only and does not mutate repository state.</p></div></section>
    <section className="tool-workspace panel">
      <div className="tool-input"><label htmlFor="sweep-targets"><span className="eyebrow">TARGETS · ONE PATH PER LINE</span></label><textarea id="sweep-targets" value={input} onChange={event => setInput(event.target.value)} aria-describedby={error ? 'sweep-error' : 'sweep-guidance'} /><p id="sweep-guidance" className="field-help">Use repository-relative paths. No keys, passphrases, blinding secrets, or other recoverable secret material.</p>{error && <p id="sweep-error" className="field-error" role="alert">{error}</p>}<button className="button primary" disabled={busy} onClick={() => void execute()}>{busy ? 'Running bounded sweep…' : 'Run P-07 sweep'}</button></div>
      <aside className="tool-contract"><span className="eyebrow">OPERATION CONTRACT</span><div><span>Mutation</span><strong>NONE</strong></div><div><span>Input</span><strong>PATHS ONLY</strong></div><div><span>Harmonic score</span><strong>NOT ASSUMED</strong></div><div><span>Authority effect</span><strong>NONE</strong></div></aside>
    </section>
    {busy && !result && <div className="empty-state panel"><StatusChip state="loading"/><h3>Analyzing supplied targets</h3><p>No success state is shown until the response passes the frontend contract validator.</p></div>}
    {result && <section className="view-stack">
      <div className="sweep-summary metric-grid"><article className="metric-card panel"><span>Sweep ID</span><strong className="mono">{result.sweep_id}</strong><small>{result.swept_at}</small></article><article className="metric-card panel"><span>Targets scanned</span><strong>{result.targets_scanned}</strong><small>Bounded input set</small></article><article className="metric-card panel"><span>Findings</span><strong>{result.findings_count}</strong><small>Filtered view below</small></article><article className="metric-card panel"><span>Harmonic score</span><strong>{result.harmonic_score === null ? 'NOT COMPUTED' : result.harmonic_score}</strong><small>{result.harmonic_score_status ?? 'No status supplied'}</small></article></div>
      <section className="panel"><div className="section-heading"><div><span className="eyebrow">RESULT NARRATIVE</span><h3>Bounded analysis</h3></div><StatusChip state={result.mutation_performed === false ? 'pass' : 'unknown'} label={result.mutation_performed === false ? 'NO MUTATION' : 'MUTATION STATE UNKNOWN'}/></div><p>{result.narrative}</p><div className="result-actions"><button className="button ghost" onClick={() => void copyResult()}>Copy result JSON</button>{copyState && <span className="copy-state" role="status">{copyState}</span>}</div></section>
      <section><div className="section-heading"><div><span className="eyebrow">FINDINGS</span><h3>{findings.length} visible</h3></div><div className="severity-filter">{SEVERITIES.map(item => <button key={item} data-active={severity === item ? 'true' : 'false'} onClick={() => setSeverity(item)}>{item}</button>)}</div></div>{findings.length ? <div className="findings-list">{findings.map(finding => <article className="finding-card panel" key={finding.id}><div className="finding-meta"><span className={`severity severity-${finding.severity.toLowerCase()}`}>{finding.severity}</span><code>{finding.target}</code><span>{finding.agent}</span></div><p>{finding.message}</p></article>)}</div> : <div className="empty-state panel"><StatusChip state="pass" label="NO MATCHING FINDINGS"/><h3>No findings in this filter</h3><p>The sweep response remains available; change severity to inspect other classes.</p></div>}</section>
    </section>}
  </div>
}
