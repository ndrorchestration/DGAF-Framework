# DGAF Related-Work Matrix

**Status:** Living prior-art map; current source-level adjudication, not a novelty verdict  
**Updated:** 2026-09-01  
**Scope:** Multi-agent orchestration, organizational formation, governance, runtime assurance, evaluation, provenance, reproducibility, candidate identity, and authorization.

## Purpose

DGAF should not claim novelty merely because its terminology differs from existing systems. The matrix compares mechanisms, governed objects, lifecycle semantics, and evidence boundaries so that overlap, synthesis, and candidate distinctions can be stated precisely.

A source's absence from this matrix is not evidence that it is irrelevant. This remains a bounded working map and must expand before any absolute novelty or firstness claim.

## Historical-priority rule

The relevant comparison target is **architecture-level composition**, not a count of shared features. A predecessor is strong only when it materially matches the governed object, transition model, evidence binding, and authorization lifecycle under examination.

## Comparison dimensions

| Dimension | Question |
|---|---|
| Governed object | Is control centered on an action, agent, workflow, organization/formation, artifact, or candidate? |
| Formation | Are agent groups/organizations explicit, persistent, and dynamically reconfigurable? |
| Membership/roles | Are membership and role changes represented as governed state? |
| Topology | Does graph/relationship structure affect coordination, authority, or policy? |
| Authority | Where are decision rights, delegation, and overrides represented? |
| Transitions | Are creation, reconfiguration, handoff, escalation, suspension, and dissolution explicit? |
| Veto/conflict | Can a distinct authority block, pause, or resolve another authority? |
| Idempotency | Is repeat behavior controlled at the relevant formation/state transition boundary? |
| Runtime enforcement | Can controls mediate actions during execution? |
| Evidence/provenance | What records support reconstruction, accountability, or verification? |
| Candidate identity | Is evidence bound to an exact software/source candidate or artifact? |
| Verification/authorization | Does promotion or authorization resolve against exact evidence and identity? |
| Epistemic status | Are implementation, verification, empirical, and historical claims explicitly separated? |

## Comparative map

| Work / family | Primary contribution | Material overlap with DGAF | Historical adjudication |
|---|---|---|---|
| Dynamic organization/reorganization MAS | Organizations as explicit structures; dynamic reorganization; authority over organizational change | Strong overlap with formation as an organizational object and authority over structural change | **External prior** |
| OMACS / organizational MAS | Roles, agents, capabilities, assignments, policies, adaptive organization state | Strong overlap with governed organizational state and role assignment | **External prior** |
| TB-CSPN / organizational agent architecture (2025) | Dynamic group formation, hierarchical supervisor oversight, threshold-driven membership, validation, traceability | Strong overlap with dynamic groups, roles, supervisory authority, transition validation | **Near-composition prior**; no exact match yet for the full DGAF cross-domain lifecycle |
| Microsoft Agent Governance Toolkit (AGT), March-April 2026 | Runtime governance, constraint graphs, supervisors, authority resolution, audit/replay, cryptographic audit/delegation, veto and escalation | Very strong overlap with governance, authority, supervision, veto, escalation, audit, and runtime enforcement | **Strong external prior**; formation itself as the persistent primary governed object remains unresolved in the inspected record |
| Runtime action-boundary governance | Pre-execution mediation, fail-closed control, provenance, non-unilateral authorization | Strong overlap in action gating and trust boundaries | **External prior** |
| SLSA | Revision/artifact provenance and verification bound to exact source/artifact identity | Strong overlap in exact candidate/artifact evidence binding | **Strong external prior** |
| in-toto | Attestation validation by exact subject digest and recognized attester | Strong overlap in candidate/artifact evidence binding and independent validation | **Strong external prior** |
| Research workflow provenance | Version-bound experiment provenance and traceability | Overlap with evidence scoped to a specific version/revision | **External prior** |
| Distributed reconfiguration/idempotency literature | Idempotent recovery/reconfiguration and state-transition safety | Partial overlap with formation-transition idempotency | **External prior at mechanism level; formation-governance composition remains open** |

## DGAF historical composition under review

The current candidate integration is represented as:

`Q = <GF, AF, VF, IF, PC, XC, L>`

where:

- `GF` = formation is an explicit governed state;
- `AF` = authority is attached to formation state;
- `VF` = veto/conflict/escalation constrains formation governance;
- `IF` = formation transitions are explicitly idempotent;
- `PC` = evidence is bound to an exact experimental candidate;
- `XC` = verification/authorization resolves against that candidate;
- `L` = these controls participate in one continuous lifecycle rather than independent subsystems.

A source with only some of these properties is a **near-composition prior**, not an exact predecessor.

## DGAF repository chronology relevant to the hypothesis

- **2026-04-29 04:04 UTC:** commit `bb5c8f19d393cf04eacac66ba3a58df97671bfdb` changes the framework expansion to **Dynamic Governance Agentic Formation**.
- **2026-05-01 09:28 UTC:** commit `edc9f93da03747cfab3a6610d3349a122ba5f128` explicitly adds authority conflict resolution, sovereign veto semantics, timeout escalation/blocking, and an idempotency guarantee to the Harmonic Quintet formation specification.
- **2026-08-21:** DGAF documents development/candidate separation and exact-candidate execution requirements.

These dates establish a development lineage but do not establish historical firstness.

## Candidate contribution statement — revised

> DGAF is an open research and implementation framework that integrates agent orchestration, formation governance, evaluation, provenance, and explicit claim/evidence management. Its potentially distinctive contribution is not any individual governance or provenance primitive, but a possible integration in which formation state and authority transitions are carried forward into candidate-bound experimental verification and authorization.

This is a **research hypothesis**, not an established novelty claim.

## Candidate/evidence distinction

The following are treated as established external principles rather than DGAF inventions:

- exact artifact/source identity;
- evidence subject/digest matching;
- immutable or revision-bound source identity;
- rejection of mismatched or stale evidence;
- independent attestation/verification;
- release-candidate separation.

DGAF's narrower candidate distinction is the possible use of those established principles as an explicit **experimental governance boundary**, so that a moving development branch cannot silently redefine the evaluated candidate and later authorization must resolve to the same candidate identity.

## What is currently defensible

- DGAF publicly documents an integrated implementation and governance approach for orchestration, formation, evaluation, provenance, and epistemic controls.
- The repository contains candidate-bound evidence controls and a documented development/candidate separation model.
- The repository contains explicit formation-level authority conflict, veto, escalation, and idempotency semantics by 2026-05-01.
- The current PDMAL efficacy claim remains unestablished: the experimental boundary is PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.

## What is not currently defensible

- That DGAF is the first framework to combine these concerns.
- That DGAF invented dynamic formation, formation authority, veto, escalation, idempotency, provenance, exact artifact identity, candidate immutability, or independent verification.
- That a shared set of features proves architectural equivalence.
- That repository-local verification establishes production readiness, general correctness, or empirical efficacy.
- That historical absence from this matrix proves nonexistence elsewhere.

## Required next comparison

The highest-value remaining research target is the exact cross-domain lifecycle:

`formation state → formation authority → governed transition → evidence → exact candidate identity → independent verification → authorization`

The search should test this composition against organizational MAS, agent-governance systems, distributed reconfiguration, software supply-chain security, and research workflow provenance. Results must be dated to primary sources.

## Publication rule

External-facing materials may describe DGAF as a **distinct formulation or implementation** when the statement is scoped to documented evidence. Novelty/priority language must use calibrated wording such as “potentially distinctive integration,” “independently developed formulation,” or “no equivalent predecessor located in the bounded review,” unless a substantially broader review supports stronger language.

## Cross-references

- `research/DGAF_HISTORICAL_PRIORITY_ADJUDICATION_2026-09-01.md`
- `research/DGAF_RELATED_WORK_SOURCE_ADJUDICATION.md`
- `PRIOR_ART_AND_RELATED_WORK_SCOPE.md`
- `PUBLICATION_AND_PROVENANCE_SPINE.md`
- `CLAIM_EVIDENCE_INDEX.md`
- `CURRENT_STATE.md`
- `experiment/DEVELOPMENT_CANDIDATE_SEPARATION_2026-08-21.md`
- `experiment/PDMAL_EXECUTION_PATH_SPEC_2026-08-21.md`
