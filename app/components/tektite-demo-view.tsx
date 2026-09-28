'use client'

import { useMemo, useState } from 'react'
import { StatusChip } from './status-chip'

type Scenario = 'authorized' | 'revoked' | 'missing_scope' | 'tampered_action' | 'replay'

type DemoResponse = {
  version: string
  scenario: Scenario
  action: {
    action_class: string
    target: string
    policy_id: string
    parameters: Record<string, unknown>
  }
  authority: {
    authorization_id: string
    parent_scope: string[]
    delegated_scope: string[]
    expires_at: string
    revoked: boolean
    verifier_status: string
    attestation_fingerprint: string
    issuer_class: string
  }
  attempts: Array<{
    attempt: number
    http_status: number
    result: {
      status?: string
      reason?: string
      execution_receipt?: Record<string, unknown>
      [key: string]: unknown
    }
  }>
  claim_boundary: {
    scientific_n_increment: number
    independent_validation: string
    canonical_dgaf_efficacy: string
    high_assurance: string
    demo_effect: string
  }
}

const SCENARIOS: Array<{ id: Scenario; title: string; summary: string; expected: string }> = [
  { id: 'authorized', title: 'Authorized update', summary: 'Valid scope, live authorization, passing verifier, bound action digest.', expected: 'ALLOW → EXECUTE → RECEIPT' },
  { id: 'revoked', title: 'Revoked authority', summary: 'The record is correctly signed, but its authorization is revoked.', expected: 'DENY · AUTHORIZATION_REVOKED' },
  { id: 'missing_scope', title: 'Missing delegated scope', summary: 'The parent has scope, but the delegated authority does not include the required action.', expected: 'DENY · REQUIRED_SCOPE_MISSING' },
  { id: 'tampered_action', title: 'Tampered action', summary: 'The signed action digest binds one parameter set, while the submitted action is changed.', expected: 'DENY · ACTION_DIGEST_MISMATCH' },
  { id: 'replay', title: 'Replay same admission', summary: 'The first valid request executes; the exact same record is then submitted again.', expected: 'FIRST EXECUTES · SECOND DENIED' },
]

function resultLabel(result: DemoResponse | null): { state: 'pass' | 'failed' | 'open'; label: string } {
  if (!result) return { state: 'open', label: 'NOT RUN' }
  const first = result.attempts[0]
  if (result.scenario === 'authorized') {
    return first?.result?.status === 'updated'
      ? { state: 'pass', label: 'AUTHORIZED + EXECUTED' }
      : { state: 'failed', label: 'UNEXPECTED RESULT' }
  }
  if (result.scenario === 'replay') {
    const second = result.attempts[1]
    return first?.result?.status === 'updated' && second?.result?.reason === 'AAR_REPLAY'
      ? { state: 'pass', label: 'REPLAY BLOCKED' }
      : { state: 'failed', label: 'UNEXPECTED RESULT' }
  }
  return first?.result?.status === 'denied'
    ? { state: 'pass', label: 'FAIL-CLOSED DENIAL' }
    : { state: 'failed', label: 'UNEXPECTED RESULT' }
}

export function TektiteDemoView() {
  const [scenario, setScenario] = useState<Scenario>('authorized')
  const [phase, setPhase] = useState<'idle' | 'running' | 'complete' | 'error'>('idle')
  const [result, setResult] = useState<DemoResponse | null>(null)
  const [error, setError] = useState<string | null>(null)

  const selected = useMemo(() => SCENARIOS.find(item => item.id === scenario) ?? SCENARIOS[0], [scenario])
  const outcome = resultLabel(result)

  async function run(nextScenario: Scenario = scenario) {
    setScenario(nextScenario)
    setPhase('running')
    setError(null)
    setResult(null)
    try {
      const response = await fetch('/api/tektite-demo', {
        method: 'POST',
        headers: { 'content-type': 'application/json' },
        body: JSON.stringify({ scenario: nextScenario }),
      })
      const payload = await response.json()
      if (!response.ok) {
        throw new Error(payload?.reason ?? payload?.status ?? `HTTP ${response.status}`)
      }
      setResult(payload)
      setPhase('complete')
    } catch (err) {
      setError(err instanceof Error ? err.message : 'Demo execution failed')
      setPhase('error')
    }
  }

  const firstAttempt = result?.attempts?.[0]
  const finalAttempt = result?.attempts?.[result.attempts.length - 1]
  const executed = firstAttempt?.result?.status === 'updated'
  const receipt = firstAttempt?.result?.execution_receipt

  return <div className="view-stack tektite-demo">
    <section className="tektite-hero panel panel-accent">
      <div>
        <span className="eyebrow accent">TEKTITE / DGAF PROOF OF OPERATION</span>
        <h2>Watch one governed action move from intent to evidence.</h2>
        <p>This demonstrator uses DGAF's existing bounded <code>AAR_V1</code> admission validator and the real <code>/api/audit</code> effect path. Choose a valid or adversarial scenario and inspect what the system permits, blocks, executes, and records.</p>
      </div>
      <div className="tektite-boundary">
        <span>SCOPE</span>
        <strong>SAME-SYSTEM · BOUNDED DEMONSTRATION</strong>
        <small>The fixture issuer is not an accepted production issuer and does not establish independent validation, efficacy, or High-Assurance authority.</small>
      </div>
    </section>

    <section className="panel tektite-start-here" aria-labelledby="tektite-start-title">
      <div className="section-heading">
        <div>
          <span className="eyebrow accent">START HERE · 60 SECOND WALKTHROUGH</span>
          <h3 id="tektite-start-title">See the basic idea before learning the framework.</h3>
          <p>You do not need to understand DGAF's architecture first. Run these two cases and compare what changes.</p>
        </div>
      </div>
      <div className="tektite-starter-grid">
        <article className="tektite-starter-card">
          <span className="tektite-starter-number">A</span>
          <div>
            <strong>1. Let a valid action through</strong>
            <p>The request has live, scoped authority and an untampered action binding. DGAF should admit it, execute the bounded effect, and emit a receipt.</p>
            <button className="button primary" type="button" disabled={phase === 'running'} onClick={() => void run('authorized')}>Run allowed action</button>
          </div>
        </article>
        <article className="tektite-starter-card">
          <span className="tektite-starter-number">B</span>
          <div>
            <strong>2. Take the authority away</strong>
            <p>The same kind of request carries revoked authority. DGAF should deny it before execution and produce no execution receipt.</p>
            <button className="button ghost" type="button" disabled={phase === 'running'} onClick={() => void run('revoked')}>Run blocked action</button>
          </div>
        </article>
      </div>
      <div className="tektite-reading-key">
        <div><span>Watch</span><strong>REQUEST → AUTHORITY → ADMISSION → EFFECT → RECEIPT</strong></div>
        <div><span>Then check</span><strong>CLAIM BOUNDARY</strong></div>
        <p>The important behavior is not simply “allow” or “deny.” It is that execution and evidence remain downstream of explicit authority, and the resulting evidence cannot silently promote its own claims.</p>
      </div>
    </section>

    <section className="panel tektite-scenario-panel">
      <div className="section-heading">
        <div><span className="eyebrow">DEEPER TESTS · CHOOSE A SCENARIO</span><h3>Now try the failure modes individually.</h3></div>
        <StatusChip state={outcome.state} label={outcome.label} />
      </div>
      <div className="tektite-scenarios" role="radiogroup" aria-label="DGAF demonstration scenario">
        {SCENARIOS.map(item => <button key={item.id} type="button" className="tektite-scenario" data-active={scenario === item.id ? 'true' : 'false'} onClick={() => { setScenario(item.id); setResult(null); setPhase('idle'); setError(null) }} role="radio" aria-checked={scenario === item.id}>
          <strong>{item.title}</strong>
          <span>{item.summary}</span>
          <code>{item.expected}</code>
        </button>)}
      </div>
      <div className="tektite-run-row">
        <button className="button primary" type="button" disabled={phase === 'running'} onClick={() => void run()}>
          {phase === 'running' ? 'Running governed action…' : 'Run governed action'}
        </button>
        <span>{selected.expected}</span>
      </div>
      {error && <div className="alert danger"><strong>Demo failed closed.</strong><span>{error}</span></div>}
    </section>

    <section className="tektite-pipeline" aria-label="DGAF governed action pipeline">
      <article className="panel tektite-stage">
        <span className="tektite-step">01</span><div><span className="eyebrow">REQUEST</span><h3>Canonical action</h3><p>{result ? <><code>{result.action.action_class}</code> targeting <code>{result.action.target}</code>.</> : 'Run a scenario to bind an exact action class, target, policy, and parameters.'}</p></div>
      </article>
      <article className="panel tektite-stage">
        <span className="tektite-step">02</span><div><span className="eyebrow">AUTHORITY</span><h3>Delegation + status</h3><p>{result ? <>Authorization <code>{result.authority.authorization_id}</code> · revoked={String(result.authority.revoked)} · delegated scope {result.authority.delegated_scope.length ? result.authority.delegated_scope.join(', ') : '∅'}.</> : 'Authority must be explicit, scoped, live, and separately verified.'}</p></div>
      </article>
      <article className="panel tektite-stage">
        <span className="tektite-step">03</span><div><span className="eyebrow">ADMISSION</span><h3>Allow or deny</h3><p>{finalAttempt ? <><code>HTTP {finalAttempt.http_status}</code> · <strong>{finalAttempt.result.status ?? 'unknown'}</strong>{finalAttempt.result.reason ? <> · {finalAttempt.result.reason}</> : null}</> : 'The validator checks attestation, revocation, expiry, delegation, required scope, verifier state, and action digest.'}</p></div>
      </article>
      <article className="panel tektite-stage">
        <span className="tektite-step">04</span><div><span className="eyebrow">EFFECT</span><h3>{executed ? 'Executed' : 'Not executed'}</h3><p>{executed ? 'The bounded ephemeral audit-counter effect completed and its postcondition was checked.' : result ? 'No authorized effect was produced by the denied attempt.' : 'Execution occurs only after admission.'}</p></div>
      </article>
      <article className="panel tektite-stage">
        <span className="tektite-step">05</span><div><span className="eyebrow">RECEIPT</span><h3>{receipt ? 'Execution evidence emitted' : 'No execution receipt'}</h3><p>{receipt ? <>Receipt <code>{String(receipt.record_id ?? '—')}</code> · postcondition <strong>{String(receipt.postcondition ?? '—')}</strong>.</> : 'A denial does not masquerade as execution evidence.'}</p></div>
      </article>
      <article className="panel tektite-stage tektite-claim-stage">
        <span className="tektite-step">06</span><div><span className="eyebrow">CLAIM BOUNDARY</span><h3>What this result is allowed to mean</h3><p>{result ? <>Scientific N +{result.claim_boundary.scientific_n_increment}. Independent validation: <strong>{result.claim_boundary.independent_validation}</strong>. Canonical efficacy: <strong>{result.claim_boundary.canonical_dgaf_efficacy}</strong>. High-Assurance: <strong>{result.claim_boundary.high_assurance}</strong>.</> : 'A successful bounded engineering demonstration does not promote scientific, independent-validation, efficacy, or High-Assurance state.'}</p></div>
      </article>
    </section>

    {result && <section className="panel tektite-evidence">
      <div className="section-heading"><div><span className="eyebrow">INSPECT THE EVIDENCE</span><h3>Machine-readable demonstration record</h3></div><StatusChip state="pass" label={result.version} /></div>
      <div className="tektite-evidence-grid">
        <div><span>Policy</span><code>{result.action.policy_id}</code></div>
        <div><span>Attestation fingerprint</span><code>{result.authority.attestation_fingerprint}</code></div>
        <div><span>Issuer class</span><code>{result.authority.issuer_class}</code></div>
        <div><span>Attempts</span><strong>{result.attempts.length}</strong></div>
      </div>
      <details>
        <summary>Show raw bounded evidence</summary>
        <pre>{JSON.stringify(result, null, 2)}</pre>
      </details>
    </section>}

    <section className="alert info tektite-explainer">
      <strong>What you just saw</strong>
      <span>DGAF is not the button. DGAF is the control chain around the button: identify the exact action, bind authority, admit or deny, execute only when permitted, retain a receipt, and keep the resulting claim inside the evidence it actually supports. A successful demo is engineering evidence that this bounded path behaved as specified; it is not independent validation or proof of general efficacy.</span>
    </section>
  </div>
}
