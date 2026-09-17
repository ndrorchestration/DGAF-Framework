# State-Space Explorer V0 — Design Specification

> **Status:** PRESENTATION / MODELING PROJECTION ONLY
> **Scientific/control effect:** NONE
> **Authority:** consumes canonical repository UI truth; does not create governance state

## Purpose

State-Space Explorer V0 is the next Semantic Control Field tranche after the merged Decision Frontier and Governance Map. It exposes DGAF's current governed lifecycle as a **discrete reachability model** without implying continuous geometry, numeric distance to authorization, probability, confidence, readiness, efficacy, or authority.

The surface exists to help an expert inspect which canonical stages are established, which stage is the current frontier, which downstream states are unreachable because a predecessor is unsatisfied, and which candidate dimensions are currently projectable, only bounded, or not formally modeled.

## Panel-derived boundary

The UI/UX Expert Panel and Visual Design & Cohesion Expert Agents permit state-space/manifold metaphors only when discrete semantics remain inspectable and cannot be mistaken for invented continuity. The conceptual tensor/manifold record is research guidance, not canonical governance authority.

Therefore V0 MUST be categorical and reachability-based. A later V1+ may introduce richer spatial geometry only after upstream formalization defines the semantics of those coordinates and relations.

## Source-of-truth contract

V0 derives from the existing presentation truth model:

- `GOVERNANCE_STAGES` supplies canonical stage identity, order, native `predicateState`, evidence boundary, and non-transfer clause.
- `TRUTH_BOUNDARY` supplies global program/fail-mode/authorization/N/efficacy constraints.
- `NEXT_TRANSITION` may provide plain-language frontier context, but must not create a second frontier calculation.

The projection MUST NOT duplicate the canonical stage list.

## Discrete reachability model

Let canonical stages be ordered `G = [g_0 ... g_n]`.

Define the presentation frontier as the first stage whose canonical `predicateState` is not `pass`.

Each stage receives exactly one derived display region:

- `established`: canonical stage occurs before the frontier and has native state `pass`;
- `frontier`: first canonical stage whose native state is not `pass`;
- `blocked_by_predecessor`: canonical stages after the frontier.

The derived region does **not** replace the stage's native predicate state. For example, a downstream stage may be `blocked_by_predecessor` while its native state remains `not_authorized`.

If every stage is `pass`, the projection MUST represent no active frontier rather than inventing a next state.

## Dimension contract

V0 exposes candidate independent dimensions with an explicit representation class:

- `projectable`: directly derivable from canonical UI truth without additional semantic invention;
- `bounded`: meaningful information exists, but it is not a scalar coordinate or complete per-stage formal dimension;
- `not_modeled`: no canonical per-stage value exists and the interface must not infer one.

Initial V0 dimensions:

| Dimension | Representation | V0 treatment |
| --- | --- | --- |
| Lifecycle / reachability | `projectable` | Established, frontier, blocked-by-predecessor regions from canonical stage order/state |
| Native predicate state | `projectable` | Preserve canonical `predicateState` exactly |
| Evidence boundary | `projectable` | Preserve stage evidence-boundary text; no numeric strength score |
| Provenance / source binding | `bounded` | Expose source/relationship lineage where explicitly available; no inferred independence |
| Verification | `bounded` | Preserve explicit verification semantics only; no universal verification coordinate |
| Authorization / authority | `bounded` | Preserve categorical global and stage-native states; no authority magnitude |
| Uncertainty | `bounded` | Categorical unknown/not-established semantics only; no probability/confidence score |
| Consequence | `not_modeled` | Display as not modeled; do not infer blast radius or severity coordinate |
| Reversibility | `not_modeled` | Display as not modeled; generic formalism does not establish current per-stage values |

## Visual grammar

V0 should feel like a controlled field without pretending to be a continuous manifold.

Required structures:

1. **Representation contract band** — visibly states `DISCRETE REACHABILITY`, `NO CONTINUOUS INTERPOLATION`, and the canonical global constraints.
2. **Reachability corridor** — ordered canonical stages grouped visually into established region, current frontier, and blocked downstream region.
3. **Frontier boundary** — the first unsatisfied canonical predicate forms a visible boundary rather than a progress percentage.
4. **Dimension matrix/rail** — shows each candidate dimension and whether it is projectable, bounded, or not modeled.
5. **Inspection text** — every stage retains its native state, evidence boundary, and `doesNotEstablish` clause.

Color MUST NOT be the sole carrier of meaning. Region identity requires labels, geometry/borders/patterning, and accessible text.

## Explicit prohibitions

V0 MUST NOT contain or imply:

- readiness percentages;
- probability of authorization or success;
- numeric confidence;
- scalar evidence quality;
- distance-to-authorization;
- continuous coordinates or interpolation;
- efficacy gradients;
- inferred consequence or reversibility values;
- runtime health as governance permission;
- a second lifecycle or authorization engine.

## Responsive and accessibility behavior

- Narrow layouts may collapse the corridor into an ordered vertical sequence, but MUST preserve stage order and region labels.
- Native state and derived reachability region must remain independently readable.
- Reduced-motion mode must preserve all meaning without animation.
- Keyboard/focus behavior must match the existing command-center navigation model.
- `not_modeled` must be textually explicit; it must never appear as zero, neutral, low, or absent risk.

## V0 acceptance criteria

A candidate is acceptable only if:

1. projection stage IDs exactly equal canonical `GOVERNANCE_STAGES` IDs in order;
2. current frontier derives from the first non-`pass` native state;
3. downstream native states remain unchanged while reachability is separately classified;
4. global constraints derive from `TRUTH_BOUNDARY`;
5. consequence and reversibility are explicitly `not_modeled`;
6. no numeric readiness/probability/distance/continuous coordinate is introduced;
7. a separate State Space view consumes the shared projection rather than copying governance truth;
8. semantic tests and production build pass;
9. scientific/control state remains unchanged.

## Current expected projection

At the current canonical UI truth:

- stages through bounded unblinding are established in the presentation projection;
- `materialization` is the discrete frontier with native state `not_established`;
- `primary-analysis-authorization` and `locked-analysis` are downstream `blocked_by_predecessor`, while each retains native state `not_authorized`;
- global posture remains `PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0`;
- efficacy remains `NOT ESTABLISHED`.

This expected projection is a presentation consequence of current canonical inputs, not a new governance record.
