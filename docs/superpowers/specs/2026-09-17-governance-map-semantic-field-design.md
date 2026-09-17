# Governance Map Semantic Field Design

## Purpose

Introduce the next Semantic Control Field tranche by evolving the existing Governance view into a structural Governance Map that explains vertical escalation, lateral coupling, global constraints, and provenance without creating a second governance model.

## Authority boundary

This is presentation-only work. Canonical lifecycle truth remains in `GOVERNANCE_STAGES`, `NEXT_TRANSITION`, and `TRUTH_BOUNDARY`. The map may derive visual relationships from those structures but may not infer authorization, scientific state, readiness percentages, efficacy, or continuous state-space semantics.

Global control posture remains **PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0**.

## Architecture

### Vertical escalation

`GOVERNANCE_STAGES` is the only lifecycle spine. The map presents stages in order and visually separates satisfied predecessors, the current blocking boundary, and downstream unreachable transitions.

### Lateral coupling

A presentation-only `GOVERNANCE_RELATIONSHIPS` projection identifies a small number of explicit cross-stage dependencies. Each relationship must reference existing stage IDs and contain:

- a stable relationship ID;
- source stage ID;
- target stage ID;
- relation kind;
- plain-language label;
- evidence/provenance explanation;
- explicit `doesNotEstablish` boundary.

Initial relation kinds are `evidence`, `authority`, and `dependency`. These are visual semantics only and do not mutate stage state.

### Global field constraints

`TRUTH_BOUNDARY` is rendered as the enclosing condition of the map rather than another lifecycle node. PRE-FREEZE, FAIL-CLOSED, NOT AUTHORIZED, empirical N=0, and efficacy NOT ESTABLISHED remain visibly global.

### Provenance

Relationship edges are inspectable statements, not decorative geometry. A user must be able to understand why a coupling exists and what it does not establish without relying on color.

## Component boundaries

- `app/lib/governance-map.ts` derives map sections and validates relationship endpoints against `GOVERNANCE_STAGES`.
- `app/components/governance-map.tsx` renders the structural map.
- `app/components/governance-view.tsx` composes the current frontier summary, Governance Map, detailed lifecycle, and interpretation rule.
- `app/lib/governance-map.test.ts` proves semantic derivation, relationship validity, field constraints, visual truth labels, and absence of synthetic readiness scoring.
- `app/styles/governance-map.css` owns map-specific visual grammar and responsive/reduced-motion rules.
- `app/layout.tsx` loads the Governance Map stylesheet alongside the existing global and Decision Frontier styles.

## Initial relationships

1. **Custody supports evidence admissibility** — repository custody is a provenance predecessor to retained evidence admission, without implying independence.
2. **Dataset lock bounds unblinding** — dataset lock is a predecessor to bounded unblinding, without authorizing materialization or analysis.
3. **Materialization gates analysis authorization** — an accepted materialization receipt is a predecessor to primary-analysis authorization, without itself authorizing analysis.
4. **Analysis authorization gates execution** — primary-analysis authorization is a predecessor to locked primary analysis, without implying a result or efficacy.

## Visual grammar

- Vertical stage rail = escalation/order.
- Horizontal/diagonal filaments = explicit lateral coupling.
- Boundary band = current blocking frontier.
- Enclosing constraint frame = global field conditions.
- Relationship cards/labels = provenance and consequence explanation.
- Geometry, labels, pattern, and typography redundantly carry state; color is supplemental.
- The global `authorization` field is labelled **AUTHORIZATION**, not authority; authority and authorization remain distinct concepts.

## Responsive behavior

Desktop may use a two-column map + relationship inspector. Tablet and mobile collapse into a linear semantic sequence where every relationship remains adjacent to its named source/target labels. No relationship may disappear solely because screen width shrinks.

## Motion

Motion is optional and limited to focus/inspection transitions. Reduced-motion mode must preserve all information with no dependence on animation.

## Acceptance criteria

- One canonical lifecycle source: `GOVERNANCE_STAGES`.
- One global constraint source: `TRUTH_BOUNDARY`.
- Every relationship endpoint resolves to a canonical stage ID.
- Current blocker remains controlled materialization; downstream primary analysis remains unauthorized.
- No `readinessPercent`, progress percentage, inferred authority, or efficacy score exists.
- Global constraints are visually separate from lifecycle stages.
- Lateral relationships expose provenance and `doesNotEstablish` text.
- Governance Map is present in Governance view before the detailed lifecycle list.
- Authority and authorization remain visually and semantically distinct.
- UI semantic tests and production build pass.
- Scientific/control effect: NONE.
