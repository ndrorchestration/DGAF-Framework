# DGAF Documentation Architecture v1.0

**Status:** Audit/control integration map; non-authoritative until ratified
**Date:** 2026-09-04

## Core rule

Existing DGAF documentation seeds remain authoritative within declared scope. New documentation should normally extend, reconcile, or index an existing source rather than duplicate it.

## Seed map

| Concern | Existing seed/source |
|---|---|
| Agent identity | `docs/agents/AGENT_ROSTER.md` |
| Agent architecture | `docs/AGENT_ARCHITECTURE_ASSESSMENT.md` |
| Formation/topology | `docs/agents/FORMATION_TOPOLOGY.md` |
| Ecosystem taxonomy | `AGENT_ECOSYSTEM_REGISTRY.md` lineage |
| Pattern library | `docs/NDR_PATTERN_REGISTRY_UNIFIED.md` + `docs/ndr_patterns_unified.json` |
| Numerical instruments | `docs/qa/QA_RUBRIC.md`, AXIS, AHG and agent rubrics |
| Evidence/provenance | `docs/qa/METRICS_PROVENANCE.md` + governance evidence records |
| Candidate/runtime identity | candidate, deployment, and assurance records |
| Temporal/history | session logs, version histories, dated governance records |
| Transversal assurance | expert-panel reviews, assurance matrices, transversal audits |

## Seven dimensions

**Temporal:** what changed, when, and from which prior state.  
**Taxonomic:** entities, variants, patterns, instruments, states, and formations.  
**Pattern:** reusable control constructs and their lifecycle.  
**Agentic:** agents, variants, formations, seats, authorities, and states.  
**Layered:** the assurance layer at which a statement operates.  
**Evidence:** observations, tests, artifacts, provenance, or explicit absence of evidence.  
**Transversal:** whether a concept retains the same meaning across affected surfaces.

## Temporal model

Use `EVENT_TIME`, `RECORD_TIME`, `EFFECTIVE_TIME`, `DISCOVERY_TIME`, and `RESOLUTION_TIME` where material. A later summary cannot retroactively alter the epistemic meaning of an earlier artifact.

## Identity model

Keep distinct:

`entity ≠ identifier ≠ seat ≠ directory ≠ formation member ≠ agent ≠ variant ≠ state ≠ rubric`

## Transversal operating method

For high-impact concepts trace:

`identity → taxonomy → specification → implementation → test → execution → evidence → claim → governance → historical lineage`

A transversal defect includes identity drift, changed semantics under one label, unsupported evidence promotion, missing dependencies, temporal ambiguity, or contradictory authority.

## Impact rule

A change touching an identifier, formula, threshold, authority, formation, pattern, state machine, dependency, deployment identity, or evidentiary claim must identify:

`affected concepts → affected documents → affected layers → affected tests → affected evidence → required re-verification`

## Anti-duplication

Before creating a new artifact: search existing repository/Notion sources; classify the proposed artifact as canonical, derivative, index, reconciliation, or historical; extend an existing owner where possible; create a separate artifact only for genuinely distinct scope; preserve lineage.

## Completion model

File completeness, semantic completeness, and assurance completeness are distinct. File existence alone is not certification.

## Scientific boundary

This integration map does not authorize freeze, pilot execution, unblinding, production certification, or empirical claims.

**DGAF:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N = 0.
