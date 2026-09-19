import { DECISION_FRONTIER } from '../lib/decision-frontier'
import type { UiState } from '../lib/types'
import { StatusChip } from './status-chip'

function FrontierNode({
  eyebrow,
  label,
  state,
  copy,
  relation,
}: {
  eyebrow: string
  label: string
  state: UiState
  copy: string
  relation: string
}) {
  return <article className="frontier-node" data-state={state}>
    <div className="frontier-node-topline">
      <span className="eyebrow">{eyebrow}</span>
      <StatusChip state={state} />
    </div>
    <h4>{label}</h4>
    <p>{copy}</p>
    <span className="frontier-relation">{relation}</span>
  </article>
}

export function DecisionFrontier() {
  const frontier = DECISION_FRONTIER
  return <section className="decision-frontier panel panel-accent" aria-labelledby="decision-frontier-title">
    <div className="section-heading frontier-heading">
      <div>
        <span className="eyebrow accent">SEMANTIC CONTROL FIELD · DECISION FRONTIER</span>
        <h3 id="decision-frontier-title">The nearest admissible change, without collapsing the truth boundary</h3>
        <p>Canonical governance stages are projected here as a field of established state, boundary, reachable work, and explicitly unreachable downstream transitions.</p>
      </div>
      <div className="frontier-legend" aria-label="Decision Frontier legend">
        <span><i className="frontier-key established" aria-hidden="true"/>Established</span>
        <span><i className="frontier-key boundary" aria-hidden="true"/>Boundary</span>
        <span><i className="frontier-key unreachable" aria-hidden="true"/>Unreachable</span>
      </div>
    </div>

    <div className="frontier-field">
      <div className="frontier-path" aria-hidden="true" />
      <FrontierNode
        eyebrow="CURRENT GOVERNED STATE"
        label={frontier.current.label}
        state={frontier.current.state}
        copy={frontier.why}
        relation="Established predecessor"
      />
      {frontier.blocking && frontier.nearest ? <>
        <FrontierNode
          eyebrow="BLOCKING BOUNDARY"
          label={frontier.blocking.label}
          state={frontier.blocking.state}
          copy={frontier.blocking.evidenceBoundary}
          relation="No admissible downstream transition yet"
        />
        <FrontierNode
          eyebrow="NEAREST ADMISSIBLE TRANSITION"
          label={frontier.nearest.label}
          state={frontier.nearest.state}
          copy={frontier.transitionSummary}
          relation="Reachable work · not an authorization grant"
        />
      </> : <FrontierNode
        eyebrow="POST-INTERPRETATION BOUNDARY"
        label="No downstream gate designated"
        state="info"
        copy={frontier.transitionSummary}
        relation="Requires a separate governed definition"
      />}
    </div>

    <div className="frontier-detail-grid">
      <div className="frontier-stratum">
        <span className="eyebrow">PROVENANCE FILAMENT</span>
        <strong>Why this state exists</strong>
        <p>{frontier.why}</p>
      </div>
      <div className="frontier-stratum consequence">
        <span className="eyebrow">CONSEQUENCE FIELD</span>
        <strong>What crossing this boundary still would not establish</strong>
        <p>{frontier.consequence}</p>
      </div>
      <div className="frontier-stratum receipt">
        <span className="eyebrow">EXECUTION RECEIPT</span>
        <div className="frontier-receipt-title"><strong>{frontier.receipt.label}</strong><StatusChip state={frontier.receipt.state}/></div>
        <p>{frontier.receipt.summary}</p>
      </div>
    </div>

    <div className="frontier-unreachable" aria-label="Currently unreachable downstream transitions">
      <div>
        <span className="eyebrow">UNREACHABLE TRANSITIONS</span>
        <strong>Downstream capability does not imply admissibility</strong>
      </div>
      <div className="frontier-unreachable-list">
        {frontier.downstream.length ? frontier.downstream.map(transition => <div className="frontier-unreachable-item" key={transition.id}>
          <span aria-hidden="true">×</span>
          <div><strong>{transition.label}</strong><small>{transition.evidenceBoundary}</small></div>
          <StatusChip state={transition.state} compact />
        </div>) : <div className="frontier-unreachable-item">
          <span aria-hidden="true">×</span>
          <div><strong>No downstream lifecycle stage is currently modeled</strong><small>Absence of a modeled stage does not create authority; any next gate requires a separate governed definition.</small></div>
          <StatusChip state="info" compact />
        </div>}
      </div>
    </div>

    <div className="frontier-warning" role="note">
      <span className="eyebrow">BOUNDARY CONDITION</span>
      <p>{frontier.warning}</p>
    </div>
  </section>
}
