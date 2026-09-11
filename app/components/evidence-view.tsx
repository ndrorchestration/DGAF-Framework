import { EPOCH_SUMMARIES, EVIDENCE_STATES, TRUTH_BOUNDARY } from '../lib/governance'
import { StatusChip } from './status-chip'

const REPOSITORY_URL = 'https://github.com/ndrorchestration/DGAF-Framework/blob/main/'

export function EvidenceView() {
  return <div className="view-stack">
    <section className="section-heading standalone"><div><span className="eyebrow">EVIDENCE & RESEARCH</span><h2>Claims carry their scope with them.</h2><p>Engineering completion, verification, authorization, empirical observation, and efficacy are separate evidence classes in this interface.</p></div></section>
    <section className="claim-ceiling panel panel-accent"><div><span className="eyebrow accent">CURRENT CLAIM CEILING</span><h3>Canonical DGAF efficacy is {TRUTH_BOUNDARY.efficacy}.</h3><p>Epoch 001 cannot support the planned primary inference because the protected mapping is unrecoverable. The successor path has not been authorized for empirical collection.</p></div><StatusChip state="not_established" label="EFFICACY NOT ESTABLISHED"/></section>
    <section className="source-authority panel" aria-labelledby="source-authority-title">
      <div className="source-authority-copy">
        <div><span className="eyebrow">PRESENTATION AUTHORITY</span><h3 id="source-authority-title">Current state is rendered from named repository truth sources.</h3></div>
        <p>These links expose the documents this interface uses as presentation authority. They are references to existing governance records, not new evidence and not a substitute for the underlying artifacts.</p>
      </div>
      <div className="source-links">{TRUTH_BOUNDARY.sources.map(source => <a className="source-link" key={source} href={`${REPOSITORY_URL}${source}`} target="_blank" rel="noreferrer">{source}</a>)}</div>
    </section>
    <div className="card-grid two">{EPOCH_SUMMARIES.map(epoch => <article className="epoch-card panel" key={epoch.id}><div className="card-header"><div><span className="eyebrow">{epoch.eyebrow}</span><h3>{epoch.title}</h3></div><StatusChip state={epoch.state}/></div><p>{epoch.summary}</p><ul className="fact-list">{epoch.facts.map(fact => <li key={fact}>{fact}</li>)}</ul></article>)}</div>
    <section><div className="section-heading"><div><span className="eyebrow">EPISTEMIC LEGEND</span><h3>How to read DGAF evidence states</h3></div></div><div className="evidence-list">{EVIDENCE_STATES.map(item => <article className="evidence-row panel" key={item.term}><StatusChip state={item.state} label={item.term}/><p>{item.meaning}</p></article>)}</div></section>
  </div>
}
