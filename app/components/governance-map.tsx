import { GOVERNANCE_MAP, GOVERNANCE_RELATIONSHIPS } from '../lib/governance-map'
import { StatusChip } from './status-chip'

function stageRole(index: number) {
  const blockingIndex = GOVERNANCE_MAP.stages.findIndex(stage => stage.id === GOVERNANCE_MAP.blocking.id)
  if (index < blockingIndex) return 'completed'
  if (index === blockingIndex) return 'blocking'
  return 'downstream'
}

export function GovernanceMap() {
  const constraints = GOVERNANCE_MAP.constraints

  return <section className="governance-map panel" aria-labelledby="governance-map-title">
    <header className="governance-map-header">
      <div>
        <span className="eyebrow accent">SEMANTIC CONTROL FIELD · GOVERNANCE MAP</span>
        <h3 id="governance-map-title">Reachability is constrained by evidence, authority, and explicit predecessors.</h3>
        <p>Vertical position shows ordered escalation. Lateral filaments show named cross-stage dependencies. The enclosing frame shows global conditions that apply to the whole field.</p>
      </div>
    </header>

    <div className="governance-field-frame" aria-label="Global governance field constraints">
      <div className="governance-field-label"><span>GLOBAL FIELD CONDITIONS</span><strong>These constraints are not lifecycle stages.</strong></div>
      <dl className="governance-constraints">
        <div><dt>PROGRAM</dt><dd>{constraints.programState}</dd></div>
        <div><dt>FAIL MODE</dt><dd>{constraints.failMode}</dd></div>
        <div><dt>AUTHORIZATION</dt><dd>{constraints.authorization}</dd></div>
        <div><dt>EMPIRICAL N</dt><dd>{constraints.empiricalN}</dd></div>
        <div><dt>EFFICACY</dt><dd>{constraints.efficacy}</dd></div>
      </dl>

      <div className="governance-map-grid">
        <div className="governance-spine" aria-label="Vertical governance escalation">
          {GOVERNANCE_MAP.stages.map((stage, index) => {
            const role = stageRole(index)
            return <article className="governance-node" data-role={role} key={stage.id}>
              <div className="governance-node-rail" aria-hidden="true"><span>{String(index + 1).padStart(2, '0')}</span></div>
              <div className="governance-node-body">
                <div className="governance-node-heading">
                  <div><span className="eyebrow">{stage.shortLabel}</span><h4>{stage.label}</h4></div>
                  <StatusChip state={stage.state}/>
                </div>
                {role === 'blocking' && <div className="governance-boundary-band"><strong>BLOCKING BOUNDARY</strong><span>{stage.evidenceBoundary}</span></div>}
                <p>{stage.description}</p>
                <details className="governance-node-details"><summary>Inspect claim boundary</summary><div><strong>EVIDENCE / PROVENANCE</strong><span>{stage.evidenceBoundary}</span><strong>DOES NOT ESTABLISH</strong><span>{stage.doesNotEstablish}</span></div></details>
              </div>
            </article>
          })}
        </div>

        <aside className="governance-relations" aria-label="Lateral governance relationships">
          <div className="governance-relations-heading"><span className="eyebrow">LATERAL COUPLING</span><h4>Named relationships only</h4><p>Each filament is an inspectable dependency statement, not inferred authority.</p></div>
          {GOVERNANCE_RELATIONSHIPS.map(relationship => {
            const source = GOVERNANCE_MAP.stages.find(stage => stage.id === relationship.sourceId)
            const target = GOVERNANCE_MAP.stages.find(stage => stage.id === relationship.targetId)
            return <article className="governance-relation" data-kind={relationship.kind} key={relationship.id}>
              <div className="governance-filament" aria-hidden="true" />
              <span className="governance-relation-kind">{relationship.kind.toUpperCase()}</span>
              <h4>{relationship.label}</h4>
              <div className="governance-relation-endpoints"><span>{source?.shortLabel}</span><span aria-hidden="true">→</span><span>{target?.shortLabel}</span></div>
              <p>{relationship.provenance}</p>
              <div className="governance-relation-boundary"><strong>DOES NOT ESTABLISH</strong><span>{relationship.doesNotEstablish}</span></div>
            </article>
          })}
        </aside>
      </div>
    </div>
  </section>
}
