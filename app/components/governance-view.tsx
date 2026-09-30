import { GOVERNANCE_STAGES, NEXT_TRANSITION } from '../lib/governance'
import {
  hiddenMutationPolicyLaneCount,
  MUTATION_POLICY_DASHBOARD,
  visibleMutationPolicyLanes,
} from '../lib/mutation-policy-dashboard'
import { GovernanceMap } from './governance-map'
import { StatusChip } from './status-chip'

export function GovernanceView() {
  const visibleMutationLanes = visibleMutationPolicyLanes()
  const hiddenMutationLanes = hiddenMutationPolicyLaneCount()

  return <div className="view-stack">
    <section className="section-heading standalone"><div><span className="eyebrow">FAIL-CLOSED LIFECYCLE</span><h2>Progression is earned one predecessor at a time.</h2><p>Prepared tooling is shown separately from the state of the predicate it can eventually evaluate. Later readiness never backfills an earlier requirement.</p></div></section>
    <section className="panel governance-summary"><div><span className="eyebrow accent">CURRENT FRONTIER</span><h3>{NEXT_TRANSITION.title}</h3><p>{NEXT_TRANSITION.summary}</p><div className="artifact-row">{NEXT_TRANSITION.artifacts.map(item => <code key={item}>{item}</code>)}</div><p className="warning-copy">{NEXT_TRANSITION.warning}</p></div><StatusChip state="not_established" label="EVIDENCE ADMISSION PENDING"/></section>
    <section className="panel governance-summary" aria-labelledby="mutation-policy-title">
      <div>
        <span className="eyebrow accent">TEKTITE MUTATION POLICY</span>
        <h3 id="mutation-policy-title">Routine workflow mutation is blocked where history or source identity would be reinterpreted.</h3>
        <p>The dashboard now exposes the #939/#1135 policy projection directly: blocked workflow lanes stay visible as blocked, with the reconciliation action required before any ordinary immutable-action hardening can touch them.</p>
        <div className="truth-grid" aria-label="Workflow mutation-policy counts">
          <div><span>Blocked lanes</span><strong>{MUTATION_POLICY_DASHBOARD.counts.blocked}</strong></div>
          <div><span>Routine hardening allowed</span><strong>{MUTATION_POLICY_DASHBOARD.counts.routineAllowed}</strong></div>
          <div><span>Pending reconciliation</span><strong>{MUTATION_POLICY_DASHBOARD.counts.pendingReconciliation}</strong></div>
          <div><span>Projection updated</span><strong>{MUTATION_POLICY_DASHBOARD.sourceUpdated}</strong></div>
        </div>
      </div>
      <StatusChip state="blocked" label="FAIL-CLOSED"/>
    </section>
    <section className="card-grid two" aria-label="Blocked workflow mutation lanes">
      {visibleMutationLanes.map(lane => <article className="epoch-card panel" key={lane.path}>
        <div className="card-header"><div><span className="eyebrow">{lane.lifecycle}</span><h4>{lane.label}</h4></div><StatusChip state={lane.state} label="BLOCKED" compact /></div>
        <p>{lane.reason}</p>
        <div className="tooling-note"><span>PATH</span><code>{lane.path}</code></div>
        <div className="tooling-note"><span>NEXT ACTION</span>{lane.nextAction}</div>
        <ul className="fact-list">{lane.evidence.map(item => <li key={item}>{item}</li>)}</ul>
      </article>)}
    </section>
    {hiddenMutationLanes > 0 && <div className="alert info"><strong>Additional blocked lanes</strong><span>{hiddenMutationLanes} more workflow mutation lanes are encoded in the dashboard projection but collapsed here to keep the governance page readable. None grants authorization or widens the current claim ceiling.</span></div>}
    <GovernanceMap />
    <section className="lifecycle" aria-label="Ordered governance lifecycle">
      {GOVERNANCE_STAGES.map((stage, index) => <article className="lifecycle-stage panel" key={stage.id}>
        <div className="stage-index">{String(index + 1).padStart(2, '0')}</div>
        <div className="stage-body"><div className="stage-heading"><div><span className="eyebrow">{stage.shortLabel}</span><h3>{stage.label}</h3></div><StatusChip state={stage.predicateState}/></div><p>{stage.description}</p><div className="tooling-note"><span>EVIDENCE BOUNDARY</span>{stage.evidenceBoundary}</div><div className="tooling-note"><span>DOES NOT ESTABLISH</span>{stage.doesNotEstablish}</div>{stage.toolingPrepared && stage.toolingNote && <div className="tooling-note"><span>TOOLING</span>{stage.toolingNote}</div>}</div>
      </article>)}
    </section>
    <div className="alert info"><strong>Interpretation rule</strong><span>A prepared validator, workflow, or control surface is engineering evidence. It does not make the governed predicate true and does not grant authorization.</span></div>
  </div>
}
