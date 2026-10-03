'use client'

import { useEffect, useState } from 'react'
import { StatusChip } from './status-chip'

type ReplayTrace = {
  schema_version: string
  evidence_class: string
  live_execution: boolean
  cross_system_live_integration: boolean
  sources: {
    dgaf_repository: string
    dgaf_authority_semantics_commit: string
    dgaf_tektite_projection_commit: string
    acp_repository: string
    acp_execution_semantics_commit: string
  }
  intent: {
    action_class: string
    target_class: string
    scenario: string
  }
  dgaf_admission: {
    state: string
    authority_effect: string
  }
  authorization: {
    state: string
    scope: string
    next_authorization_state: string
  }
  acp_execution_contract: {
    execution_profile: string
    state: string
    real_project_mutation_authorized: boolean
    rollback_execution_authorized: boolean
  }
  receipt: {
    postcondition_state: string
    authority_effect: string
    follow_on_authority: string
  }
  durable_lineage: {
    scope: string
    state: string
    distributed_global_lineage: boolean
  }
  follow_on: {
    fresh_dgaf_adjudication: string
    next_authorization_state: string
    next_effect_state: string
  }
  claim_boundary: {
    scientific_n_increment: number
    independent_validation: string
    canonical_dgaf_efficacy: string
    high_assurance: string
    production_execution: string
    generalized_usability: string
  }
}

const TRACE_URL = '/evidence/tektite-dgaf-acp-replay-trace-v0.json'

export function TektiteGovernedReplayTrace() {
  const [trace, setTrace] = useState<ReplayTrace | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let active = true

    async function loadTrace() {
      try {
        const response = await fetch(TRACE_URL, { cache: 'no-store' })
        if (!response.ok) throw new Error(`HTTP ${response.status}`)
        const payload = (await response.json()) as ReplayTrace
        if (active) setTrace(payload)
      } catch (err) {
        if (active) {
          setError(err instanceof Error ? err.message : 'Replay trace unavailable')
        }
      }
    }

    void loadTrace()
    return () => {
      active = false
    }
  }, [])

  return <section className="view-stack" aria-labelledby="tektite-cross-system-trace-title">
    <section className="panel panel-accent">
      <div className="section-heading">
        <div>
          <span className="eyebrow accent">TEKTITE / DGAF → ACP REPLAY</span>
          <h2 id="tektite-cross-system-trace-title">See the governed handoff without creating a live mutation path.</h2>
          <p>This section replays accepted DGAF and ACP semantics from exact source identities. It does not call ACP, mutate a repository, or claim that this cross-system chain executed live.</p>
        </div>
        <StatusChip state={trace ? 'pass' : error ? 'failed' : 'open'} label={trace ? 'REPLAY BOUND' : error ? 'UNAVAILABLE' : 'LOADING'} />
      </div>
      <div className="tektite-boundary">
        <span>SCOPE</span>
        <strong>STATIC REPLAY · NO LIVE ACP EXECUTION</strong>
        <small>Bounded disposable-repository semantics only. Real-project mutation, rollback, production execution, independent validation, and High-Assurance remain outside this trace.</small>
      </div>
    </section>

    {error && <div className="alert danger"><strong>Replay trace unavailable.</strong><span>{error}</span></div>}

    {trace && <>
      <section className="tektite-pipeline" aria-label="Replayed DGAF to ACP governed action trace">
        <article className="panel tektite-stage">
          <span className="tektite-step">01</span>
          <div><span className="eyebrow">INTENT</span><h3>Bounded action</h3><p><code>{trace.intent.action_class}</code> · target <strong>{trace.intent.target_class}</strong>.</p></div>
        </article>
        <article className="panel tektite-stage">
          <span className="tektite-step">02</span>
          <div><span className="eyebrow">DGAF ADMISSION</span><h3>{trace.dgaf_admission.state}</h3><p>The replayed admission carries authority effect <strong>{trace.dgaf_admission.authority_effect}</strong>.</p></div>
        </article>
        <article className="panel tektite-stage">
          <span className="tektite-step">03</span>
          <div><span className="eyebrow">BOUNDED AUTHORITY</span><h3>{trace.authorization.scope}</h3><p>{trace.authorization.state}. Next authorization: <strong>{trace.authorization.next_authorization_state}</strong>.</p></div>
        </article>
        <article className="panel tektite-stage">
          <span className="tektite-step">04</span>
          <div><span className="eyebrow">ACP CONTRACT</span><h3>{trace.acp_execution_contract.state}</h3><p>Profile <code>{trace.acp_execution_contract.execution_profile}</code>. Real-project mutation authorized: <strong>{String(trace.acp_execution_contract.real_project_mutation_authorized)}</strong>.</p></div>
        </article>
        <article className="panel tektite-stage">
          <span className="tektite-step">05</span>
          <div><span className="eyebrow">RECEIPT</span><h3>{trace.receipt.postcondition_state}</h3><p>Authority effect <strong>{trace.receipt.authority_effect}</strong> · follow-on <strong>{trace.receipt.follow_on_authority}</strong>.</p></div>
        </article>
        <article className="panel tektite-stage">
          <span className="tektite-step">06</span>
          <div><span className="eyebrow">DURABLE LINEAGE</span><h3>{trace.durable_lineage.state}</h3><p>{trace.durable_lineage.scope}. Distributed/global lineage: <strong>{String(trace.durable_lineage.distributed_global_lineage)}</strong>.</p></div>
        </article>
        <article className="panel tektite-stage">
          <span className="tektite-step">07</span>
          <div><span className="eyebrow">FRESH ADJUDICATION</span><h3>{trace.follow_on.fresh_dgaf_adjudication}</h3><p>Next effect: <strong>{trace.follow_on.next_effect_state}</strong>. Next authorization: <strong>{trace.follow_on.next_authorization_state}</strong>.</p></div>
        </article>
        <article className="panel tektite-stage tektite-claim-stage">
          <span className="tektite-step">08</span>
          <div><span className="eyebrow">CLAIM BOUNDARY</span><h3>Replay does not promote the system</h3><p>Scientific N +{trace.claim_boundary.scientific_n_increment}. Independent validation: <strong>{trace.claim_boundary.independent_validation}</strong>. Production execution: <strong>{trace.claim_boundary.production_execution}</strong>. High-Assurance: <strong>{trace.claim_boundary.high_assurance}</strong>.</p></div>
        </article>
      </section>

      <section className="panel tektite-evidence">
        <div className="section-heading">
          <div><span className="eyebrow">EXACT SOURCE BINDING</span><h3>The replay is pinned to accepted semantics.</h3></div>
          <StatusChip state="pass" label={trace.schema_version} />
        </div>
        <div className="tektite-evidence-grid">
          <div><span>DGAF authority</span><code>{trace.sources.dgaf_authority_semantics_commit}</code></div>
          <div><span>Tektite projection</span><code>{trace.sources.dgaf_tektite_projection_commit}</code></div>
          <div><span>ACP execution semantics</span><code>{trace.sources.acp_execution_semantics_commit}</code></div>
          <div><span>Evidence class</span><strong>{trace.evidence_class}</strong></div>
        </div>
        <details>
          <summary>Show raw replay fixture</summary>
          <pre>{JSON.stringify(trace, null, 2)}</pre>
        </details>
      </section>
    </>}
  </section>
}
