'use client'

import { useEffect, useState } from 'react'
import { StatusChip } from './status-chip'

type CepObservability = {
  schema_version: string
  evidence_class: string
  live_model_experiment: boolean
  automatic_tool_gating_enabled: boolean
  live_context_routing_enabled: boolean
  sources: {
    acp_repository: string
    acp_cep_merge_commit: string
    acp_pr: number
    catalog_snapshot_sha256: string
    catalog_snapshot_path: string
    preservation_result_path: string
  }
  task: {
    capability: string
    required_tool: string
  }
  observed_catalog_measurement: {
    control_descriptor_count: number
    treatment_descriptor_count: number
    control_serialized_bytes: number
    treatment_serialized_bytes: number
    bytes_removed: number
    byte_reduction_fraction: number
    tokenizer: string
    encoding: string
    control_tokens: number
    treatment_tokens: number
    tokens_removed: number
    token_reduction_fraction: number
    required_tool_preserved: boolean
  }
  unobserved_or_not_established: Record<string, string>
  comparison_boundary: {
    evaluation_scope: string
    authority_effect: string
    scientific_n_increment: number
    independent_validation_effect: string
    canonical_dgaf_efficacy: string
    high_assurance: string
  }
  projection_boundary: string
}

const CEP_URL = '/evidence/tektite-cep-observability-v0.json'

function percent(value: number) {
  return `${(value * 100).toFixed(2)}%`
}

export function TektiteCepObservability() {
  const [data, setData] = useState<CepObservability | null>(null)
  const [error, setError] = useState<string | null>(null)

  useEffect(() => {
    let active = true

    async function loadCepEvidence() {
      try {
        const response = await fetch(CEP_URL, { cache: 'no-store' })
        if (!response.ok) throw new Error(`HTTP ${response.status}`)
        const payload = (await response.json()) as CepObservability
        if (active) setData(payload)
      } catch (err) {
        if (active) {
          setError(err instanceof Error ? err.message : 'CEP evidence unavailable')
        }
      }
    }

    void loadCepEvidence()
    return () => {
      active = false
    }
  }, [])

  return <section className="view-stack" aria-labelledby="tektite-cep-title">
    <section className="panel panel-accent">
      <div className="section-heading">
        <div>
          <span className="eyebrow accent">TEKTITE / CONTEXT EFFICIENCY</span>
          <h2 id="tektite-cep-title">Measure context exposure without turning the dashboard into a router.</h2>
          <p>This projection shows accepted ACP characterization from a static local fixture. It does not gate tools, suppress context, invoke ACP, or claim a live-model efficiency result.</p>
        </div>
        <StatusChip state={data ? 'pass' : error ? 'failed' : 'open'} label={data ? 'CHARACTERIZED' : error ? 'UNAVAILABLE' : 'LOADING'} />
      </div>
      <div className="tektite-boundary">
        <span>SCOPE</span>
        <strong>READ ONLY · AUTOMATIC TOOL GATING NOT ENABLED</strong>
        <small>Catalog-context measurement only. Live prompt, latency, monetary cost, correctness, efficacy, independent validation, and High-Assurance are not established by this surface.</small>
      </div>
    </section>

    {error && <div className="alert danger"><strong>CEP evidence unavailable.</strong><span>{error}</span></div>}

    {data && <>
      <section className="tektite-pipeline" aria-label="Context efficiency characterization">
        <article className="panel tektite-stage">
          <span className="tektite-step">01</span>
          <div><span className="eyebrow">CONTROL CATALOG</span><h3>{data.observed_catalog_measurement.control_descriptor_count} descriptors</h3><p>{data.observed_catalog_measurement.control_tokens.toLocaleString()} serialized <code>{data.observed_catalog_measurement.encoding}</code> tokens.</p></div>
        </article>
        <article className="panel tektite-stage">
          <span className="tektite-step">02</span>
          <div><span className="eyebrow">EXACT CAPABILITY</span><h3>{data.observed_catalog_measurement.treatment_descriptor_count} descriptor</h3><p><code>{data.task.required_tool}</code> remains available for <code>{data.task.capability}</code>.</p></div>
        </article>
        <article className="panel tektite-stage">
          <span className="tektite-step">03</span>
          <div><span className="eyebrow">CATALOG CONTEXT</span><h3>{percent(data.observed_catalog_measurement.token_reduction_fraction)} smaller</h3><p>{data.observed_catalog_measurement.control_tokens.toLocaleString()} → {data.observed_catalog_measurement.treatment_tokens.toLocaleString()} tokens in the frozen metadata serialization.</p></div>
        </article>
        <article className="panel tektite-stage">
          <span className="tektite-step">04</span>
          <div><span className="eyebrow">PRESERVATION</span><h3>{data.observed_catalog_measurement.required_tool_preserved ? 'Required tool preserved' : 'Preservation not established'}</h3><p>Evaluation scope: <strong>{data.comparison_boundary.evaluation_scope}</strong>.</p></div>
        </article>
        <article className="panel tektite-stage tektite-claim-stage">
          <span className="tektite-step">05</span>
          <div><span className="eyebrow">CLAIM BOUNDARY</span><h3>Characterization is not efficacy</h3><p>Authority effect <strong>{data.comparison_boundary.authority_effect}</strong>. Scientific N +{data.comparison_boundary.scientific_n_increment}. Independent validation effect <strong>{data.comparison_boundary.independent_validation_effect}</strong>. High-Assurance <strong>{data.comparison_boundary.high_assurance}</strong>.</p></div>
        </article>
      </section>

      <section className="panel tektite-evidence">
        <div className="section-heading">
          <div><span className="eyebrow">OBSERVED VS UNMEASURED</span><h3>Missing measurements stay missing.</h3></div>
          <StatusChip state="pass" label={data.schema_version} />
        </div>
        <div className="tektite-evidence-grid">
          <div><span>ACP accepted source</span><code>{data.sources.acp_cep_merge_commit}</code></div>
          <div><span>Catalog snapshot</span><code>{data.sources.catalog_snapshot_sha256}</code></div>
          <div><span>Tokenizer</span><strong>{data.observed_catalog_measurement.tokenizer}</strong></div>
          <div><span>Evidence class</span><strong>{data.evidence_class}</strong></div>
        </div>
        <div className="tektite-evidence-grid">
          {Object.entries(data.unobserved_or_not_established).map(([name, value]) =>
            <div key={name}><span>{name.replaceAll('_', ' ')}</span><strong>{value}</strong></div>
          )}
        </div>
        <details>
          <summary>Show raw CEP projection fixture</summary>
          <pre>{JSON.stringify(data, null, 2)}</pre>
        </details>
      </section>
    </>}
  </section>
}
