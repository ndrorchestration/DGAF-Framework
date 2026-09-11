import { CURRENT_FRONTIER_ID, GOVERNANCE_STAGES } from '../lib/governance'
import { DecisionFrontier } from './decision-frontier'
import { StatusChip } from './status-chip'

const LIFECYCLE_LANES = [
  {
    label: 'Pre-authorization control',
    description: 'Custody, preflight, freeze, closure, verification, and the separate human authorization boundary.',
    stages: GOVERNANCE_STAGES.slice(0, 6),
  },
  {
    label: 'Empirical execution',
    description: 'Collection and post-collection control remain downstream of an explicit collection authorization.',
    stages: GOVERNANCE_STAGES.slice(6, 9),
  },
  {
    label: 'Controlled disclosure',
    description: 'Unblinding and materialization remain bounded, separately governed transitions.',
    stages: GOVERNANCE_STAGES.slice(9, 11),
  },
  {
    label: 'Primary analysis',
    description: 'The locked confirmatory analysis requires a separate analysis authorization after every predecessor.',
    stages: GOVERNANCE_STAGES.slice(11),
  },
]

export function GovernanceView() {
  return <div className="view-stack">
    <section className="section-heading standalone"><div><span className="eyebrow">FAIL-CLOSED LIFECYCLE</span><h2>Progression is earned one predecessor at a time.</h2><p>The interface separates predicate state, prepared tooling, and authorization. Later readiness never backfills an earlier requirement.</p></div></section>

    <DecisionFrontier />

    <section className="governance-map" aria-labelledby="governance-map-title">
      <div className="section-heading"><div><span className="eyebrow">ORDERED CONTROL MAP</span><h3 id="governance-map-title">Four lanes, one predecessor chain</h3><p>Stages remain strictly ordered even when later validators or workflows have already been implemented.</p></div></div>
      <div className="governance-lanes">
        {LIFECYCLE_LANES.map(lane => <section className="governance-lane panel" key={lane.label}>
          <div className="lane-copy"><span className="eyebrow">{lane.label}</span><p>{lane.description}</p></div>
          <div className="lane-rail">
            {lane.stages.map(stage => {
              const index = GOVERNANCE_STAGES.indexOf(stage) + 1
              const isFrontier = stage.id === CURRENT_FRONTIER_ID
              return <article className="lane-stage" data-frontier={isFrontier ? 'true' : 'false'} key={stage.id}>
                <div className="lane-stage-heading"><span className="lane-stage-number">{String(index).padStart(2, '0')}</span><StatusChip state={stage.predicateState} compact /></div>
                <h4>{stage.shortLabel}</h4>
                <p>{stage.description}</p>
                {stage.toolingPrepared && <div className="tooling-note"><span>TOOLING PREPARED</span>{stage.toolingNote}</div>}
              </article>
            })}
          </div>
        </section>)}
      </div>
    </section>

    <div className="alert info"><strong>Interpretation rule</strong><span>A prepared validator, workflow, or control surface is engineering evidence. It does not make the governed predicate true and does not grant authorization.</span></div>
  </div>
}
