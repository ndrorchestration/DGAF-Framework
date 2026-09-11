import { EPOCH_SUMMARIES, NEXT_TRANSITION, TRUTH_BOUNDARY } from '../lib/governance'
import type { ViewId } from './app-shell'
import { ArrowIcon, ShieldIcon } from './icons'
import { StatusChip } from './status-chip'

const PILLARS = [
  ['Evidence', 'What was observed or produced, with exact scope and provenance.'],
  ['Verification', 'What review predicate passed, and whether it was independent.'],
  ['Authority', 'Which role or record can make a decision in the current state.'],
  ['Permission', 'Whether the exact next action is actually allowed to occur.'],
]

export function OverviewView({ onNavigate }: { onNavigate: (view: ViewId) => void }) {
  return <div className="view-stack">
    <section className="hero panel-accent">
      <div className="hero-copy">
        <span className="eyebrow accent">GOVERNED MULTI-AGENT ORCHESTRATION & EVALUATION</span>
        <h2>Make the difference between <em>can act</em> and <em>may act</em> impossible to miss.</h2>
        <p>DGAF separates evidence, verification, authority, and permission so engineering capability cannot silently become authorization—or testing become proof.</p>
        <div className="hero-actions">
          <button className="button primary" onClick={() => onNavigate('governance')}>Inspect governance <ArrowIcon /></button>
          <button className="button ghost" onClick={() => onNavigate('control')}>Open control room</button>
        </div>
      </div>
      <div className="hero-orbit" aria-hidden="true"><div className="orbit orbit-a"/><div className="orbit orbit-b"/><div className="orbit-core"><ShieldIcon /></div><span className="orbit-node n1"/><span className="orbit-node n2"/><span className="orbit-node n3"/><span className="orbit-node n4"/></div>
    </section>

    <section className="truth-boundary panel">
      <div className="section-heading"><div><span className="eyebrow">CANONICAL HIGH-ASSURANCE BOUNDARY</span><h3>Truth boundary</h3></div><span className="source-stamp">SSoT reconciled {TRUTH_BOUNDARY.sourceUpdated}</span></div>
      <div className="truth-grid">
        <div><span>Program state</span><strong>{TRUTH_BOUNDARY.programState}</strong></div>
        <div><span>Fail mode</span><strong>{TRUTH_BOUNDARY.failMode}</strong></div>
        <div><span>Authorization</span><StatusChip state="not_authorized" label={TRUTH_BOUNDARY.authorization}/></div>
        <div><span>Empirical N</span><strong>{TRUTH_BOUNDARY.empiricalN}</strong></div>
        <div><span>Canonical efficacy</span><StatusChip state="not_established" label={TRUTH_BOUNDARY.efficacy}/></div>
      </div>
      <p className="boundary-note">Substantial engineering and governance evidence exists. That does not establish canonical DGAF efficacy or authorize successor empirical collection.</p>
    </section>

    <section>
      <div className="section-heading"><div><span className="eyebrow">CONCEPTUAL MODEL</span><h3>Four controls that never collapse into one another</h3></div></div>
      <div className="card-grid four">{PILLARS.map(([title, body], index) => <article className="concept-card panel" key={title}><span className="concept-number">0{index + 1}</span><h4>{title}</h4><p>{body}</p></article>)}</div>
    </section>

    <section>
      <div className="section-heading"><div><span className="eyebrow">RESEARCH STATE</span><h3>Track A at a glance</h3></div><button className="text-button" onClick={() => onNavigate('evidence')}>Explore evidence <ArrowIcon /></button></div>
      <div className="card-grid two">{EPOCH_SUMMARIES.map(epoch => <article className="epoch-card panel" key={epoch.id}><div className="card-header"><div><span className="eyebrow">{epoch.eyebrow}</span><h4>{epoch.title}</h4></div><StatusChip state={epoch.state}/></div><p>{epoch.summary}</p><ul className="fact-list">{epoch.facts.map(fact => <li key={fact}>{fact}</li>)}</ul></article>)}</div>
    </section>

    <section className="next-transition panel panel-accent">
      <div><span className="eyebrow accent">NEXT ADMISSIBLE TRANSITION</span><h3>{NEXT_TRANSITION.title}</h3><p>{NEXT_TRANSITION.summary}</p><div className="artifact-row">{NEXT_TRANSITION.artifacts.map(item => <code key={item}>{item}</code>)}</div><p className="warning-copy">{NEXT_TRANSITION.warning}</p></div>
      <button className="button ghost" onClick={() => onNavigate('governance')}>View ordered chain <ArrowIcon /></button>
    </section>
  </div>
}
