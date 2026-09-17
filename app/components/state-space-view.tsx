import { STATE_SPACE_DIMENSIONS, STATE_SPACE_PROJECTION, type ReachabilityRegion } from '../lib/state-space-projection.ts'
import { StatusChip } from './status-chip'

function reachabilityLabel(region: ReachabilityRegion) {
  if (region === 'established') return 'ESTABLISHED REGION'
  if (region === 'frontier') return 'CURRENT FRONTIER'
  return 'BLOCKED BY PREDECESSOR'
}

function dimensionLabel(representation: 'projectable' | 'bounded' | 'not_modeled') {
  if (representation === 'projectable') return 'PROJECTABLE'
  if (representation === 'bounded') return 'BOUNDED'
  return 'NOT MODELED — DO NOT INFER'
}

export function StateSpaceView() {
  return (
    <div className="state-space-view">
      <section className="state-space-contract panel" aria-labelledby="state-space-title">
        <div>
          <span className="eyebrow accent">EXPERT MODELING PROJECTION</span>
          <h2 id="state-space-title">State-Space Explorer V0</h2>
          <p>
            A categorical projection of current governed reachability. Native governance predicates remain authoritative;
            spatial grouping here is presentation only.
          </p>
        </div>
        <div className="state-space-contract-tags" aria-label="Representation contract">
          <strong>DISCRETE REACHABILITY</strong>
          <strong>NO CONTINUOUS INTERPOLATION</strong>
        </div>
        <div className="state-space-global-field" aria-label="Global field conditions">
          <div><span>PROGRAM</span><strong>{STATE_SPACE_PROJECTION.constraints.programState}</strong></div>
          <div><span>FAIL MODE</span><strong>{STATE_SPACE_PROJECTION.constraints.failMode}</strong></div>
          <div><span>AUTHORIZATION</span><strong>{STATE_SPACE_PROJECTION.constraints.authorization}</strong></div>
          <div><span>EMPIRICAL N</span><strong>{STATE_SPACE_PROJECTION.constraints.empiricalN}</strong></div>
          <div><span>EFFICACY</span><strong>{STATE_SPACE_PROJECTION.constraints.efficacy}</strong></div>
        </div>
      </section>

      <section className="state-space-field panel" aria-labelledby="reachability-heading">
        <div className="section-heading">
          <span className="eyebrow">REACHABILITY FIELD</span>
          <h3 id="reachability-heading">Canonical stages projected into discrete regions</h3>
          <p>Reachability and native predicate state are shown separately. A downstream block never rewrites a stage&apos;s own state.</p>
        </div>
        <ol className="state-space-corridor">
          {STATE_SPACE_PROJECTION.regions.map(region => (
            <li key={region.id} className="state-space-region" data-reachability={region.reachability}>
              <div className="state-space-region-axis" aria-hidden="true"><span /></div>
              <article>
                <div className="state-space-region-heading">
                  <div>
                    <span className="state-space-region-class">{reachabilityLabel(region.reachability)}</span>
                    <h4>{region.shortLabel}</h4>
                  </div>
                  <StatusChip state={region.nativeState} label={region.nativeState.replaceAll('_', ' ').toUpperCase()} compact />
                </div>
                <p className="state-space-region-title">{region.label}</p>
                <dl>
                  <div><dt>EVIDENCE BOUNDARY</dt><dd>{region.evidenceBoundary}</dd></div>
                  <div><dt>DOES NOT ESTABLISH</dt><dd>{region.doesNotEstablish}</dd></div>
                </dl>
              </article>
            </li>
          ))}
        </ol>
      </section>

      <section className="state-space-dimensions panel" aria-labelledby="dimensions-heading">
        <div className="section-heading">
          <span className="eyebrow">INDEPENDENT DIMENSIONS</span>
          <h3 id="dimensions-heading">What V0 can represent without inventing state</h3>
          <p>Representation classes describe the available model, not maturity, quality, or permission.</p>
        </div>
        <div className="state-space-dimension-grid">
          {STATE_SPACE_DIMENSIONS.map(dimension => (
            <article key={dimension.id} className="state-space-dimension" data-representation={dimension.representation}>
              <div className="state-space-dimension-heading">
                <h4>{dimension.label}</h4>
                <span>{dimensionLabel(dimension.representation)}</span>
              </div>
              <p>{dimension.description}</p>
            </article>
          ))}
        </div>
      </section>
    </div>
  )
}
