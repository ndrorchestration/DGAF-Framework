import { GOVERNANCE_STAGES, NEXT_TRANSITION } from '../lib/governance'
import { StatusChip } from './status-chip'

export function GovernanceView() {
  return <div className="view-stack">
    <section className="section-heading standalone"><div><span className="eyebrow">FAIL-CLOSED LIFECYCLE</span><h2>Progression is earned one predecessor at a time.</h2><p>Prepared tooling is shown separately from the state of the predicate it can eventually evaluate. Later readiness never backfills an earlier requirement.</p></div></section>
    <section className="panel governance-summary"><div><span className="eyebrow accent">CURRENT FRONTIER</span><h3>{NEXT_TRANSITION.title}</h3><p>{NEXT_TRANSITION.summary}</p><div className="artifact-row">{NEXT_TRANSITION.artifacts.map(item => <code key={item}>{item}</code>)}</div><p className="warning-copy">{NEXT_TRANSITION.warning}</p></div><StatusChip state="not_established" label="CUSTODY NOT ESTABLISHED"/></section>
    <section className="lifecycle" aria-label="Ordered governance lifecycle">
      {GOVERNANCE_STAGES.map((stage, index) => <article className="lifecycle-stage panel" key={stage.id}>
        <div className="stage-index">{String(index + 1).padStart(2, '0')}</div>
        <div className="stage-body"><div className="stage-heading"><div><span className="eyebrow">{stage.shortLabel}</span><h3>{stage.label}</h3></div><StatusChip state={stage.predicateState}/></div><p>{stage.description}</p>{stage.toolingPrepared && <div className="tooling-note"><span>TOOLING PREPARED</span>{stage.toolingNote}</div>}</div>
      </article>)}
    </section>
    <div className="alert info"><strong>Interpretation rule</strong><span>A prepared validator, workflow, or control surface is engineering evidence. It does not make the governed predicate true and does not grant authorization.</span></div>
  </div>
}
