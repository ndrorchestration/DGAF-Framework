import { EPOCH_SUMMARIES, EVIDENCE_STATES, NEXT_TRANSITION, TRUTH_BOUNDARY } from '../lib/governance'
import { StatusChip } from './status-chip'

const REPOSITORY_URL = 'https://github.com/ndrorchestration/DGAF-Framework/blob/main/'

export function EvidenceView() {
  return <div className="view-stack">
    <section className="section-heading standalone"><div><span className="eyebrow">EVIDENCE & RESEARCH</span><h2>Claims carry their scope with them.</h2><p>This view separates observed evidence, repository predicates, permission, and efficacy so readers can see exactly where a claim stops.</p></div></section>

    <section className="claim-ceiling panel panel-accent evidence-ceiling"><div><span className="eyebrow accent">CURRENT CLAIM CEILING</span><h3>Canonical DGAF efficacy is {TRUTH_BOUNDARY.efficacy}.</h3><p>Epoch 001 cannot support the planned primary inference because the protected mapping is unrecoverable. Epoch 002 has not been authorized for empirical collection. Accepted preflight does not bridge either gap.</p></div><StatusChip state="not_established" label="EFFICACY NOT ESTABLISHED"/></section>

    <section className="evidence-lineage panel" aria-labelledby="evidence-lineage-title">
      <div className="evidence-lineage-heading"><div><span className="eyebrow">CURRENT EVIDENCE LINEAGE</span><h3 id="evidence-lineage-title">What is established, what is actionable, and what remains prohibited</h3></div><p>These are separate epistemic and governance objects. Movement at one layer does not silently promote the next.</p></div>
      <div className="evidence-lineage-rail">
        <article className="evidence-current-node" data-kind="evidence"><span className="evidence-current-index">01</span><span className="eyebrow">REPOSITORY EVIDENCE</span><h4>{NEXT_TRANSITION.evidenceTitle}</h4><p>{NEXT_TRANSITION.evidence}</p><StatusChip state="pass" label={NEXT_TRANSITION.evidenceStatusLabel} compact/></article>
        <div className="evidence-lineage-link" aria-hidden="true"><span /></div>
        <article className="evidence-current-node" data-kind="predicate"><span className="evidence-current-index">02</span><span className="eyebrow">NEXT PREDICATE</span><h4>{NEXT_TRANSITION.blockerTitle}</h4><p>{NEXT_TRANSITION.blocker}</p><StatusChip state="open" label={NEXT_TRANSITION.blockerStatusLabel} compact/></article>
        <div className="evidence-lineage-link" aria-hidden="true"><span /></div>
        <article className="evidence-current-node" data-kind="authority"><span className="evidence-current-index">03</span><span className="eyebrow">PERMISSION</span><h4>Successor collection remains prohibited.</h4><p>Final closure, verification classification, and a separate collection authorization remain downstream; prepared tooling grants no permission.</p><StatusChip state="not_authorized" label={TRUTH_BOUNDARY.authorization} compact/></article>
        <div className="evidence-lineage-link" aria-hidden="true"><span /></div>
        <article className="evidence-current-node" data-kind="claim"><span className="evidence-current-index">04</span><span className="eyebrow">CANONICAL CLAIM</span><h4>Efficacy remains outside the evidence ceiling.</h4><p>Empirical N remains {TRUTH_BOUNDARY.empiricalN}; no successor efficacy claim is established.</p><StatusChip state="not_established" label={TRUTH_BOUNDARY.efficacy} compact/></article>
      </div>
    </section>

    <section className="source-authority panel" aria-labelledby="source-authority-title">
      <div className="source-authority-copy">
        <div><span className="eyebrow">PROVENANCE ANCHORS</span><h3 id="source-authority-title">Named repository sources define the presentation boundary.</h3></div>
        <p>These documents are references to existing governance records. They are not new evidence and do not replace the exact artifacts or workflow evidence beneath them.</p>
      </div>
      <div className="source-links">{TRUTH_BOUNDARY.sources.map(source => <a className="source-link" key={source} href={`${REPOSITORY_URL}${source}`} target="_blank" rel="noreferrer">{source}</a>)}</div>
    </section>

    <section aria-labelledby="epoch-comparison-title">
      <div className="section-heading"><div><span className="eyebrow">RESEARCH STATE</span><h3 id="epoch-comparison-title">Track A epoch comparison</h3><p>Historical and successor evidence remain separate records with different failure and authorization boundaries.</p></div></div>
      <div className="epoch-comparison">{EPOCH_SUMMARIES.map(epoch => <article className="epoch-comparison-card panel" data-epoch={epoch.id} key={epoch.id}><div className="card-header"><div><span className="eyebrow">{epoch.eyebrow}</span><h3>{epoch.title}</h3></div><StatusChip state={epoch.state}/></div><p>{epoch.summary}</p><ul className="fact-list">{epoch.facts.map(fact => <li key={fact}>{fact}</li>)}</ul></article>)}</div>
    </section>

    <section className="evidence-glossary-section" aria-labelledby="evidence-glossary-title"><div className="section-heading"><div><span className="eyebrow">EPISTEMIC LEGEND</span><h3 id="evidence-glossary-title">How to read DGAF evidence states</h3><p>Status terms are claim-scoped. A stronger term is never implied by a weaker one.</p></div></div><div className="evidence-glossary panel">{EVIDENCE_STATES.map(item => <article className="evidence-glossary-row" key={item.term}><StatusChip state={item.state} label={item.term}/><p>{item.meaning}</p></article>)}</div></section>
  </div>
}
