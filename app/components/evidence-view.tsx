import { EPOCH_SUMMARIES, EVIDENCE_STATES, GOVERNANCE_STAGES, TRUTH_BOUNDARY } from '../lib/governance'
import type { ViewId } from './app-shell'
import { ArrowIcon } from './icons'
import { StatusChip } from './status-chip'

export function EvidenceView({ onNavigate }: { onNavigate: (view: ViewId) => void }) {
  return <div className="view-stack">
    <section className="section-heading standalone"><div><span className="eyebrow">EVIDENCE & RESEARCH</span><h2>Claims carry their scope with them.</h2><p>Engineering completion, verification, authorization, empirical observation, and efficacy are separate evidence classes in this interface.</p></div></section>
    <section className="claim-ceiling panel panel-accent"><div><span className="eyebrow accent">CURRENT CLAIM CEILING</span><h3>Canonical DGAF efficacy is {TRUTH_BOUNDARY.efficacy}.</h3><p>Epoch 001 cannot support its planned primary inference because the protected mapping is unrecoverable. Epoch 002 collection, dataset lock, bounded unblinding, materialization, immutable receipt, and bounded primary-analysis authorization are accepted; the locked primary analysis has not yet run.</p></div><StatusChip state="not_established" label="EFFICACY NOT ESTABLISHED"/></section>
    <div className="card-grid two">{EPOCH_SUMMARIES.map(epoch => <article className="epoch-card panel" key={epoch.id}><div className="card-header"><div><span className="eyebrow">{epoch.eyebrow}</span><h3>{epoch.title}</h3></div><StatusChip state={epoch.state}/></div><p>{epoch.summary}</p><ul className="fact-list">{epoch.facts.map(fact => <li key={fact}>{fact}</li>)}</ul></article>)}</div>

    <section aria-labelledby="evidence-spine-title">
      <div className="section-heading"><div><span className="eyebrow">EVIDENCE SPINE</span><h3 id="evidence-spine-title">Trace what each accepted state establishes—and what it does not.</h3><p>The evidence spine reuses the same governed stages as the lifecycle view. It exposes scope before interpretation so a passed predecessor cannot silently widen into authorization, efficacy, or independence.</p></div></div>
      <div className="evidence-spine">
        {GOVERNANCE_STAGES.map((stage, index) => <article className="evidence-spine-row panel" key={stage.id}>
          <div className="evidence-spine-index">{String(index + 1).padStart(2, '0')}</div>
          <div className="evidence-spine-main">
            <div className="evidence-spine-heading"><div><span className="eyebrow">{stage.shortLabel}</span><h4>{stage.label}</h4></div><StatusChip state={stage.predicateState}/></div>
            <div className="evidence-boundary-grid">
              <div><span>EVIDENCE BOUNDARY</span><p>{stage.evidenceBoundary}</p></div>
              <div><span>DOES NOT ESTABLISH</span><p>{stage.doesNotEstablish}</p></div>
            </div>
          </div>
        </article>)}
      </div>
    </section>

    <section className="evidence-handoff panel panel-accent">
      <div><span className="eyebrow accent">VERIFY → INSPECT</span><h3>Evidence first; governance interpretation second.</h3><p>These records establish scoped predicates and limitations. Governance uses the same stage model to show ordering, blocking relationships, authority boundaries, and the next admissible transition.</p></div>
      <button className="button ghost" onClick={() => onNavigate('governance')}>Inspect governance context <ArrowIcon /></button>
    </section>

    <section><div className="section-heading"><div><span className="eyebrow">EPISTEMIC LEGEND</span><h3>How to read DGAF evidence states</h3></div></div><div className="evidence-list">{EVIDENCE_STATES.map(item => <article className="evidence-row panel" key={item.term}><StatusChip state={item.state} label={item.term}/><p>{item.meaning}</p></article>)}</div></section>
  </div>
}
