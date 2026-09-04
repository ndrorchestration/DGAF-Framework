# DGAF Documentation Architecture v1.0

**Status:** Audit/control integration map; non-authoritative until ratified
**Date:** 2026-09-04
**Purpose:** Define how existing DGAF documentation seeds fit together without creating parallel sources of truth.

## 1. Core rule

DGAF already contains substantial documentation for timeline/history, taxonomy, formations, agents, patterns, evidence, candidate identity, and transversal assurance. This document is an **integration map**, not a replacement specification.

Existing authoritative or seed artifacts remain authoritative within their declared scope. New documentation should normally extend, reconcile, or index an existing source rather than duplicate it.

## 2. Existing seed map

| Concern | Existing seed/source | Role of this document |
|---|---|---|
| Agent identity | `docs/agents/AGENT_ROSTER.md` | Map authority and unresolved conflicts |
| Agent architecture | `docs/AGENT_ARCHITECTURE_ASSESSMENT.md` | Map completeness, lineage, instantiation status |
| Formation/topology | `docs/agents/FORMATION_TOPOLOGY.md` | Bind formations, seats, states, and authority |
| Ecosystem taxonomy | `AGENT_ECOSYSTEM_REGISTRY.md` lineage | Reconcile taxonomy with sovereign identity |
| Pattern library | `docs/NDR_PATTERN_REGISTRY_UNIFIED.md` + `docs/ndr_patterns_unified.json` | Bind human/machine pattern surfaces and drift |
| Numerical instruments | `docs/qa/QA_RUBRIC.md`, AXIS, AHG and agent rubrics | Bind distinct instrument identities and dependencies |
| Evidence/provenance | `docs/qa/METRICS_PROVENANCE.md` + governance evidence records | Preserve evidence status and upstream dependencies |
| Candidate/runtime identity | candidate boundary, deployment, and assurance records | Keep source/app/deployment identity separate |
| Temporal/history | session logs, version histories, dated governance records, historical progress analysis | Preserve event/effective/discovery/resolution time distinctions |
| Transversal assurance | adversarial panel reviews, assurance matrices, transversal audits, reconciliation matrix | Provide cross-domain consistency checks |
| Operational control | Operational Control Center / expert-panel records | Coordinate current-state decisions without replacing GitHub source truth |

## 3. Documentation dimensions

DGAF documentation must be considered across seven dimensions:

**Temporal:** what changed, when, and from which prior state.

**Taxonomic:** what entities, categories, variants, patterns, instruments, states, and formations exist.

**Pattern:** what reusable control constructs exist and how they are versioned, triggered, implemented, and evidenced.

**Agentic:** which agents, variants, formations, authorities, seats, and system states exist.

**Layered:** at which control/architecture layer a statement operates.

**Evidence:** what observation, test, artifact, provenance, or explicit absence of evidence supports the statement.

**Transversal:** whether the same concept retains the same meaning as it crosses all affected documentation surfaces.

## 4. Temporal model

When a material event is documented, distinguish:

`EVENT_TIME` — underlying event occurred

`RECORD_TIME` — event/fact was documented

`EFFECTIVE_TIME` — resulting rule/configuration became operative

`DISCOVERY_TIME` — defect/fact was discovered

`RESOLUTION_TIME` — remediation became complete

A later summary cannot retroactively alter the epistemic meaning of an earlier artifact.

## 5. Taxonomy and agentic model

The documentation architecture explicitly separates:

`entity ≠ identifier ≠ seat ≠ directory ≠ formation member ≠ agent ≠ variant ≠ state ≠ rubric`

Agent records should therefore carry stable identity, display name, directory, seat status, formation membership, variant/historical lineage, activation status, authority, and rubric references.

The existing roster/topology conflict remains a reconciliation problem; this document does not select a winner.

## 6. Pattern-library model

The existing NDR registry is the seed pattern library. Pattern identity must remain independent of title and should bind, where applicable:

`pattern_id`, `version`, `layer`, `class`, `purpose`, `trigger`, `preconditions`, `postconditions`, `authority`, `implementation`, `dependencies`, `evidence`, `supersession`, `status`.

The Markdown and JSON NDR registries currently represent different releases and therefore require explicit reconciliation before one can silently replace the other.

## 7. Multi-layer model

The current assurance model separates:

### L0 — Identity & legitimacy

### L1 — Structural integrity

### L2 — Execution integrity

### L3 — Scientific integrity

### L4 — Governance integrity

A lower-layer pass does not erase a higher-layer failure. Documentation should label the layer a statement belongs to rather than implying that success transfers automatically between layers.

## 8. Transversal analysis as an operating method

For each high-impact concept, trace:

`identity → taxonomy → specification → implementation → test → execution → evidence → claim → governance → historical lineage`

A transversal defect includes identity drift, changed semantics under one label, unsupported promotion of evidence, missing dependency links, temporal ambiguity, or contradictory authority.

This is a standing assurance method, not merely a report category.

## 9. Documentation impact rule

A change touching an identifier, formula, threshold, authority, formation, pattern, state machine, dependency, deployment identity, or evidentiary claim must identify:

`affected concepts → affected documents → affected layers → affected tests → affected evidence → required re-verification`

The preferred implementation is to extend the existing document/registry responsible for that concern and add a reconciliation record when cross-domain impact exists.

## 10. Completion model

Documentation completeness has three distinct meanings:

1. **File completeness:** expected files exist.
2. **Semantic completeness:** required concepts and relationships are represented.
3. **Assurance completeness:** contradictions, historical boundaries, dependencies, and evidence status are explicitly handled.

File completeness alone is not certification.

## 11. Anti-duplication policy

Before creating a new DGAF documentation artifact:

1. search the repository and Notion for an existing source or seed;
2. determine whether the proposed artifact is canonical, derivative, index, reconciliation, or historical;
3. extend the existing artifact when it owns the concept;
4. create a separate artifact only when it has a genuinely distinct scope or lifecycle;
5. record lineage when a new artifact intentionally derives from an existing source.

Duplicate documents with overlapping authority are themselves documentation defects.

## 12. Current integration priorities

- Reconcile agent identity across roster, topology, and ecosystem records.
- Reconcile NDR Markdown/JSON release identity.
- Reconcile numerical instrument identities and dependencies.
- Backfill metrics provenance using the instrument dependency chain.
- Maintain the expert-panel and Operational Control Center as coordination surfaces, not alternate implementation truth.
- Preserve historical records while clearly labeling superseded/current/prospective states.

## 13. Scientific boundary

This integration map does not authorize freeze, pilot execution, unblinding, production certification, or empirical claims.

**DGAF:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N = 0.
