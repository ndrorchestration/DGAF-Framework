import { EPOCH_SUMMARIES } from '../lib/governance'
import type { ViewId } from './app-shell'
import { DecisionFrontier } from './decision-frontier'
import { ArrowIcon } from './icons'
import { StatusChip } from './status-chip'

const CONTROL_MODEL = [
  ['Evidence', 'What exists'],
  ['Verification', 'What passed'],
  ['Authority', 'Who may decide'],
  ['Permission', 'What may happen'],
]

export function OverviewView({ onNavigate }: { onNavigate: (view: ViewId) => void }) {
  return <div className="view-stack">
    <section className="hero panel-accent hero-governance">
      <div className="hero-copy">
        <span className="eyebrow accent">GOVERNED MULTI-AGENT ORCHESTRATION & EVALUATION</span>
        <h2>Capability does not become permission.</h2>
        <p>DGAF binds agentic work to evidence, verification, explicit authority, and admissible transitions so implementation readiness cannot silently become authorization—or testing become proof.</p>
        <div className="hero-actions">
          <button className="button primary" onClick={() => onNavigate('governance')}>Inspect governance <ArrowIcon /></button>
          <button className="button ghost" onClick={() => onNavigate('evidence')}>Inspect evidence</button>
        </div>
      </div>
      <div className="hero-control-model" aria-label="DGAF control model">
        <div className="control-model-header"><span className="eyebrow">CONTROL MODEL</span><span>Scope narrows before action</span></div>
        <div className="control-chain">
          {CONTROL_MODEL.map(([title, sub], index) => <div className="control-step" key={title} data-step={index + 1}>
            <span>{String(index + 1).padStart(2, '0')}</span>
            <strong>{title}</strong>
            <small>{sub}</small>
          </div>)}
        </div>
        <div className="control-model-boundary"><span>FAIL-CLOSED BOUNDARY</span><strong>No implication across stages.</strong></div>
      </div>
    </section>

    <DecisionFrontier />

    <section>
      <div className="section-heading"><div><span className="eyebrow">RESEARCH STATE</span><h3>Track A at a glance</h3><p>Historical evidence and the successor path remain separate. Neither is promoted beyond its exact evidence ceiling.</p></div><button className="text-button" onClick={() => onNavigate('evidence')}>Explore evidence <ArrowIcon /></button></div>
      <div className="card-grid two">{EPOCH_SUMMARIES.map(epoch => <article className="epoch-card panel" key={epoch.id}><div className="card-header"><div><span className="eyebrow">{epoch.eyebrow}</span><h4>{epoch.title}</h4></div><StatusChip state={epoch.state}/></div><p>{epoch.summary}</p><ul className="fact-list">{epoch.facts.map(fact => <li key={fact}>{fact}</li>)}</ul></article>)}</div>
    </section>

    <section className="overview-principle panel">
      <div><span className="eyebrow">INTERPRETATION RULE</span><h3>Engineering readiness and governance authority remain different objects.</h3></div>
      <p>Prepared workflows, validators, adapters, or downstream analysis tooling are useful engineering evidence. They do not satisfy an unmet predecessor, authorize empirical collection, establish efficacy, or change scientific N.</p>
      <button className="button ghost" onClick={() => onNavigate('control')}>Open runtime control room <ArrowIcon /></button>
    </section>
  </div>
}
