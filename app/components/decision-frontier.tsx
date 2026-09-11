import { NEXT_TRANSITION } from '../lib/governance'
import { StatusChip } from './status-chip'

export function DecisionFrontier({ showOperatorHandoff = false }: { showOperatorHandoff?: boolean }) {
  return (
    <section className="decision-frontier panel panel-accent" aria-labelledby="decision-frontier-title">
      <div className="decision-frontier-heading">
        <div>
          <span className="eyebrow accent">DECISION FRONTIER</span>
          <h3 id="decision-frontier-title">{NEXT_TRANSITION.title}</h3>
          <p>Custody is satisfied. One non-authorizing predecessor is now actionable; prepared downstream tooling does not move the frontier.</p>
        </div>
        <StatusChip state="open" label="PREFLIGHT ACTIONABLE" />
      </div>

      <div className="decision-flow" aria-label="Evidence, blocker, and next admissible action">
        <article className="decision-node" data-kind="evidence">
          <span className="decision-node-index">01</span>
          <span className="eyebrow">EVIDENCE</span>
          <h4>Repository custody-v2 evidence is satisfied.</h4>
          <p>{NEXT_TRANSITION.evidence}</p>
          <StatusChip state="pass" label="CUSTODY SATISFIED" compact />
        </article>
        <div className="decision-connector" aria-hidden="true"><span /></div>
        <article className="decision-node" data-kind="blocker">
          <span className="decision-node-index">02</span>
          <span className="eyebrow">BLOCKER</span>
          <h4>The retained preflight record does not yet exist.</h4>
          <p>{NEXT_TRANSITION.blocker}</p>
          <StatusChip state="open" label="ACTIONABLE / NOT RETAINED" compact />
        </article>
        <div className="decision-connector" aria-hidden="true"><span /></div>
        <article className="decision-node" data-kind="action">
          <span className="decision-node-index">03</span>
          <span className="eyebrow accent">ACTION PERMITTED NOW</span>
          <h4>Prepare only the non-authorizing preflight record.</h4>
          <p>{NEXT_TRANSITION.summary}</p>
          <div className="artifact-row">{NEXT_TRANSITION.artifacts.map(item => <code key={item}>{item}</code>)}</div>
        </article>
      </div>

      {showOperatorHandoff && <details className="operator-handoff">
        <summary><span>Operator handoff</span><strong>Show exact safe local step</strong></summary>
        <div className="operator-handoff-grid">
          <div><span>Starting point</span><code>{NEXT_TRANSITION.operatorBranch}</code></div>
          <div><span>Run</span><code>{NEXT_TRANSITION.operatorCommand}</code></div>
          <div><span>Verify one-file delta</span><code>{NEXT_TRANSITION.operatorVerification}</code></div>
        </div>
        <p>The preflight helper consumes only the already-admitted public certificate and non-secret custody receipt. It never creates, reads, requests, or accepts a private key or passphrase, and it cannot authorize empirical collection.</p>
      </details>}

      <div className="decision-lock">
        <StatusChip state="not_authorized" label="SUCCESSOR COLLECTION NOT AUTHORIZED" compact />
        <p>Downstream implementation readiness does not authorize collection or establish efficacy. {NEXT_TRANSITION.warning}</p>
      </div>
    </section>
  )
}
