import Link from 'next/link'
import { EPOCH_SUMMARIES, NEXT_TRANSITION, TRUTH_BOUNDARY } from '../lib/governance'
import { ArrowIcon } from './icons'
import { StatusChip } from './status-chip'

const PUBLIC_SUMMARY = [
  ['Govern actions', 'Make admissible transitions explicit before agents or operators act.'],
  ['Bind evidence', 'Keep claims attached to provenance, verification scope, and immutable records.'],
  ['Expose limits', 'Show what is not authorized, not established, or not yet reachable.'],
]

const PILLARS = [
  ['Evidence', 'What was observed or produced, with exact scope and provenance.'],
  ['Verification', 'What review predicate passed, and whether it was independent.'],
  ['Authority', 'Which role or record can make a decision in the current state.'],
  ['Permission', 'Whether the exact next action is actually allowed to occur.'],
]

export function OverviewView() {
  return <div className="view-stack">
    <section className="hero panel-accent">
      <div className="hero-copy">
        <span className="eyebrow accent">GOVERNED MULTI-AGENT ORCHESTRATION & EVALUATION</span>
        <h2>Make the difference between <em>can act</em> and <em>may act</em> impossible to miss.</h2>
        <p>DGAF separates evidence, verification, authority, and permission so engineering capability cannot silently become authorization—or testing become proof.</p>
        <div className="hero-actions">
          <Link className="button primary" href="/evidence">Inspect evidence <ArrowIcon /></Link>
          <Link className="button ghost" href="/control">Open control room</Link>
        </div>
      </div>
      <div className="hero-field" role="img" aria-label={`Governed transition field. Current program state: ${TRUTH_BOUNDARY.programState}. Authorization: ${TRUTH_BOUNDARY.authorization}. Post-Epoch-002 boundary: ${NEXT_TRANSITION.title}.`}>
        <div className="hero-field-frame">
          <div className="hero-field-caption"><span className="eyebrow">SEMANTIC CONTROL FIELD</span><span>reachability preview</span></div>
          <div className="hero-state hero-state-current"><span>CURRENT STATE</span><strong>{TRUTH_BOUNDARY.programState}</strong><small>Established governance context</small></div>
          <div className="hero-filament hero-filament-established"><span>evidence + provenance</span></div>
          <div className="hero-boundary"><span>AUTHORIZATION BOUNDARY</span><strong>{TRUTH_BOUNDARY.authorization}</strong></div>
          <div className="hero-filament hero-filament-frontier"><span>separate-governance boundary</span></div>
          <div className="hero-state hero-state-frontier"><span>POST-EPOCH-002 BOUNDARY</span><strong>{NEXT_TRANSITION.title}</strong><small>No successor authority inferred</small></div>
        </div>
      </div>
    </section>

    <section className="public-summary panel" aria-labelledby="public-summary-title">
      <div className="public-summary-copy">
        <span className="eyebrow">EXTERNAL SUMMARY</span>
        <h3 id="public-summary-title">What DGAF is for</h3>
        <p>DGAF is a governance and evidence layer for agentic systems. It makes transition authority, provenance, and claim limits inspectable instead of leaving them implicit in orchestration code.</p>
      </div>
      <div className="public-summary-grid">
        {PUBLIC_SUMMARY.map(([title, body]) => <div key={title}><strong>{title}</strong><span>{body}</span></div>)}
      </div>
      <div className="public-claim-ceiling">
        <span>Current claim ceiling</span>
        <strong>{TRUTH_BOUNDARY.efficacy}</strong>
        <small>Engineering and governance maturity are not presented as established canonical efficacy.</small>
      </div>
    </section>

    <section className="aoss-readiness panel" aria-labelledby="aoss-readiness-title">
      <div className="section-heading">
        <div><span className="eyebrow">AOSS V0.6 / STAGE A</span><h3 id="aoss-readiness-title">Execution-readiness boundary</h3></div>
        <StatusChip state="open" label="NOT ESTABLISHED" />
      </div>
      <p>Stage A has advanced through the non-collecting foundation, PolicyInput mapping, exact CPython 3.12.3 runtime/dependency binding, synthetic environment-manifest contract, and environment observation. Observation remains explicitly unaccepted: it does not enable collection or create outcomes.</p>
      <div className="readiness-strip" aria-label="AOSS Stage A readiness progression">
        {[
          ['Foundation', 'ESTABLISHED'],
          ['Policy mapping', 'ESTABLISHED'],
          ['Runtime binding', 'ESTABLISHED'],
          ['Environment observed', 'OBSERVED · NOT ACCEPTED'],
          ['Source driver', 'NOT ESTABLISHED'],
          ['Collector + custody', 'NOT ESTABLISHED'],
        ].map(([label, state]) => <div key={label}><span>{label}</span><strong>{state}</strong></div>)}
      </div>
      <div className="aoss-readiness-footer">
        <span><strong>Outcome collection</strong> NOT EXECUTED</span>
        <span><strong>Scientific N increment</strong> 0</span>
        <span><strong>Next gate</strong> exact source-driver executable binding</span>
      </div>
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
      <p className="boundary-note">Substantial engineering and governance evidence exists. Epoch 002 materialization, bounded locked-primary-analysis authorization, local primary-analysis execution, the content-addressed locked-result receipt, bounded interpretation, and the creation-only post-interpretation disposition are established at their exact scopes; Epoch 002 is closed for this preregistered lane, while canonical DGAF efficacy and independent validation remain NOT ESTABLISHED and High-Assurance authority remains NOT AUTHORIZED.</p>
    </section>

    <section>
      <div className="section-heading"><div><span className="eyebrow">CONCEPTUAL MODEL</span><h3>Four controls that never collapse into one another</h3></div></div>
      <div className="card-grid four">{PILLARS.map(([title, body], index) => <article className="concept-card panel" key={title}><span className="concept-number">0{index + 1}</span><h4>{title}</h4><p>{body}</p></article>)}</div>
    </section>

    <section>
      <div className="section-heading"><div><span className="eyebrow">RESEARCH STATE</span><h3>Track A at a glance</h3></div><Link className="text-button" href="/evidence">Explore evidence <ArrowIcon /></Link></div>
      <div className="card-grid two">{EPOCH_SUMMARIES.map(epoch => <article className="epoch-card panel" key={epoch.id}><div className="card-header"><div><span className="eyebrow">{epoch.eyebrow}</span><h4>{epoch.title}</h4></div><StatusChip state={epoch.state}/></div><p>{epoch.summary}</p><ul className="fact-list">{epoch.facts.map(fact => <li key={fact}>{fact}</li>)}</ul></article>)}</div>
    </section>

    <section className="next-transition panel panel-accent">
      <div><span className="eyebrow accent">POST-EPOCH-002 BOUNDARY</span><h3>{NEXT_TRANSITION.title}</h3><p>{NEXT_TRANSITION.summary}</p><div className="artifact-row">{NEXT_TRANSITION.artifacts.map(item => <code key={item}>{item}</code>)}</div><p className="warning-copy">{NEXT_TRANSITION.warning}</p></div>
      <Link className="button ghost" href="/governance">View ordered chain <ArrowIcon /></Link>
    </section>
  </div>
}
