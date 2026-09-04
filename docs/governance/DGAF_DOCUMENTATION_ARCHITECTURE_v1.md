# DGAF Documentation Architecture v1.0

**Status:** Audit/control proposal; non-authoritative until ratified
**Date:** 2026-09-04
**Scope:** Documentation, taxonomy, pattern-library, agentic, temporal, multi-layer, and transversal coherence across DGAF

## 1. Purpose

DGAF documentation is a control surface, not merely descriptive material. It must preserve what the system is, when a statement was true, what artifact established it, which authority owns it, what it depends on, and how it relates to other layers.

The documentation system therefore treats **identity, time, taxonomy, patterns, agents, layers, evidence, and dependencies as first-class dimensions**.

## 2. Seven documentation dimensions

| Dimension | Question answered | Canonical artifact family |
|---|---|---|
| Temporal | What changed, when, and from what state? | timeline / changelog / session history |
| Taxonomic | What entities and categories exist? | registries / vocabularies / ontology maps |
| Pattern | What reusable control patterns exist? | pattern registry / pattern specs |
| Agentic | Which agents, variants, formations, and authorities exist? | identity manifest / formation topology |
| Layered | At which architectural/control layer does a fact operate? | layer map / control-plane model |
| Evidence | What supports the claim or state? | provenance / attestation / execution artifacts |
| Transversal | Does the same concept remain coherent across all affected artifacts? | cross-reference matrix / drift audit |

No single dimension is a substitute for another.

## 3. Temporal documentation model

Every material artifact should expose:

- creation/effective date;
- superseded date, when applicable;
- source commit or immutable artifact identity;
- session/event provenance;
- status at that point in time;
- whether the statement is current, historical, prospective, or superseded.

A timeline record must distinguish at least:

`EVENT_TIME` — when the underlying event occurred

`RECORD_TIME` — when it was documented

`EFFECTIVE_TIME` — when the resulting rule/configuration became operative

`DISCOVERY_TIME` — when a defect or fact was discovered

`RESOLUTION_TIME` — when the defect was actually resolved

These timestamps must not be conflated.

## 4. Taxonomy model

Maintain separate registries for:

1. entities;
2. identifiers;
3. variants and aliases;
4. formations/topologies;
5. instruments;
6. patterns;
7. states;
8. evidence artifacts;
9. historical/superseded material.

A taxonomy entry must never imply implementation merely because an entry exists.

## 5. Pattern-library model

Every reusable pattern should have a stable pattern identity independent of its prose title. Minimum fields:

`pattern_id`, `name`, `version`, `layer`, `class`, `purpose`, `trigger`, `preconditions`, `postconditions`, `authority`, `implementation_ref`, `dependencies`, `evidence_ref`, `supersedes`, `status`.

Pattern documentation should separate:

- constitutional/normative patterns;
- executable runtime patterns;
- advisory patterns;
- evidence/provenance patterns;
- historical patterns.

A pattern's existence in the library is not evidence that its implementation is correct.

## 6. Agentic documentation model

Agent records must distinguish:

- stable identity;
- display name;
- role/domain;
- formation membership;
- authority scope;
- seat status;
- variant lineage;
- historical lineage;
- activation state;
- implementation state;
- rubric identity;
- integration contracts;
- upstream/downstream dependencies.

**Agent ≠ seat ≠ directory ≠ formation member ≠ state ≠ rubric.**

These must remain separate dimensions even when they share names.

## 7. Multi-layer model

DGAF documentation should classify claims across at least five control layers:

**L0 — Identity & legitimacy:** candidate, artifact, agent, dependency, authority identity.

**L1 — Structural integrity:** topology, state schema, null semantics, invariants, contract structure.

**L2 — Execution integrity:** runtime behavior, deployment, blinding, custody, reproducibility.

**L3 — Scientific integrity:** hypotheses, measurements, statistical analysis, independent verification.

**L4 — Governance integrity:** freeze, authorization, promotion, exception handling, release authority.

A passing lower layer cannot override a failed higher layer.

## 8. Transversal analysis

Transversal analysis is a standing method for testing whether a concept remains consistent as it crosses documentation domains.

For every high-value concept, audit at minimum across:

`identity → taxonomy → specification → implementation → test → evidence → governance → historical lineage`

Examples include:

- P-11 / 11Q;
- P-15 / Reson;
- AXIS;
- P-42 / AHG;
- agent IDs;
- NDR registry watermark;
- candidate/deployment identity.

A transversal defect exists when an identifier, formula, threshold, authority, or status changes meaning without an explicit lineage or scope boundary.

## 9. Documentation dependency graph

Documentation should be treated as a directed graph:

`source specification → implementation → tests → execution → evidence → claim → governance decision`

References should be typed, not merely textual. Preferred relationship classes:

`IMPLEMENTS`, `EXTENDS`, `ADAPTS`, `DERIVES_FROM`, `EVIDENCES`, `DEPENDS_ON`, `SUPERSEDES`, `CONFLICTS_WITH`, `HISTORICAL_OF`.

## 10. Claim/documentation contract

Every material claim should expose:

- claim ID;
- claim type;
- exact source artifact;
- source commit/version;
- temporal scope;
- applicable layer;
- dependencies;
- epistemic status;
- verification method;
- known conflicts or limitations.

A documentation page may be readable without all fields, but the underlying registry must retain them.

## 11. Required documentation families

DGAF should maintain these first-class families:

### Canonical registries
Identity, agents, instruments, patterns, taxonomy, terminology, evidence.

### Architecture
Layer maps, formation topology, dependency graphs, authority maps, state machines.

### Temporal lineage
Project timeline, decision chronology, amendment log, supersession ledger, historical snapshots.

### Pattern library
One page/spec per reusable pattern plus a registry/index and dependency map.

### Agentic system
Agent dossiers, formation contracts, authority matrix, integration contracts, variant/historical lineage.

### Evaluation
Rubrics, metrics, gates, protocols, acceptance tests, provenance, reproducibility records.

### Assurance
Transversal audits, contradiction register, drift reports, exception register, promotion controls.

### Operational
Runbooks, checklists, deployment identity, custody, release controls, incident records.

## 12. Change-management rule

A change touching any high-impact identifier, formula, threshold, authority, formation, pattern, or state machine must produce a documentation impact set.

The impact set should identify:

`affected IDs → affected layers → affected artifacts → dependent tests → affected evidence → required re-verification`

Documentation-only changes must be explicitly marked as such and must not be interpreted as apparatus changes.

## 13. Minimum transversal matrix

Each high-impact concept should be traceable through these columns:

| Concept | Identity | Taxonomy | Spec | Implementation | Test | Evidence | Governance | Temporal status | Conflict |
|---|---|---|---|---|---|---|---|---|---|

Blank cells are gaps. Contradictory cells are defects. Historical cells must be date/version bound.

## 14. Recommended repository structure

```text
docs/
  architecture/
  governance/
  instruments/
  patterns/
  agents/
  evidence/
  operations/
  research/
  history/
  taxonomy/
  terminology/
```

Existing paths may remain for compatibility; registries should provide canonical mappings rather than forcing disruptive moves before authority is established.

## 15. Anti-patterns prohibited

- documentation drift hidden by duplicated prose;
- current and historical states sharing the same unlabeled identity;
- aliases treated as interchangeable without lineage;
- agent directories used as proof of canonical seat status;
- generic `score` fields used without instrument identity;
- pattern titles used as identity without stable IDs;
- successful downstream tests used to erase unresolved upstream defects;
- documentation changes silently treated as scientific or experimental evidence.

## 16. Current DGAF boundary

This architecture is a documentation/control improvement. It does not authorize freeze, pilot execution, unblinding, production certification, or empirical claims.

**DGAF:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N = 0.
