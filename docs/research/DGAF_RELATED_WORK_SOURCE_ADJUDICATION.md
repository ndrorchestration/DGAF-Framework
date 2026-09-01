# DGAF Related-Work Source Adjudication

**Status:** Current source-level adjudication; not an absolute novelty determination  
**Updated:** 2026-09-01  
**Purpose:** Compare concrete prior work against DGAF mechanisms and architectural compositions, explicitly separating primitive prior art from architecture-level hypotheses.

## Method

This document applies the mechanism-level comparison rule in the publication and provenance spine. A source is not treated as equivalent merely because it uses terms such as *governance*, *orchestration*, *formation*, or *provenance*.

Comparison dimensions now include:

1. governed object;
2. formation and membership state;
3. topology and organization;
4. authority and delegation;
5. transition lifecycle;
6. veto/conflict/escalation;
7. idempotency at the relevant state boundary;
8. runtime control/enforcement;
9. provenance and evidence custody;
10. candidate identity and immutability;
11. verification/authorization;
12. reproducibility and experimental governance.

Classifications are **external prior**, **near-composition prior**, **candidate distinction**, or **unresolved**. A candidate distinction is a hypothesis for review, not a novelty verdict.

## Source adjudications

### A. Dynamic Reorganization of Agent Societies (Dignum, Sonenberg, Dignum, 2004)

**Established overlap:** The paper explicitly studies dynamic organizational reorganization, how and why organizations change, authority to modify organizational structure, and how reorganization decisions are made.

**DGAF implication:** Dynamic formation/reorganization and authority over organizational structure are longstanding multi-agent-systems prior art.

**Status:** **External prior.**

Primary source: https://www.researchgate.net/publication/27694396_Dynamic_Reorganization_of_Agent_Societies

### B. Organizational multi-agent system frameworks (AGR / OMACS and related work)

**Established overlap:** Organizational MAS work models agents, roles, groups, capabilities, assignments, policies, and adaptive organizational state. These frameworks treat organizational structure as more than an incidental collection of actions.

**DGAF implication:** “Formation as a governed organizational object” is not a sufficient DGAF novelty claim without substantially narrower semantics.

**Status:** **External prior.**

### C. TB-CSPN / organizational theory for multi-agent interaction (2025)

**Established overlap:** TB-CSPN provides dynamic group formation, threshold-driven membership changes, hierarchical Supervisor/Consultant/Worker roles, supervisor authorization, multi-stage validation before structural integration, and traceability-oriented coordination. It therefore overlaps substantially with dynamic formation plus supervisory governance.

**DGAF implication:** The broad proposition that formation, role hierarchy, adaptive membership, authorization, and auditable coordination can be one architecture is prior to DGAF.

**Candidate distinction:** The inspected public material does not establish the complete DGAF candidate composition of sovereign authority conflict resolution + veto + explicit formation idempotency + exact software-candidate experimental authorization.

**Status:** **Near-composition prior.**

Primary sources:

- https://link.springer.com/article/10.1007/s10791-025-09667-2
- https://www.mdpi.com/1999-5903/17/8/363

### D. Microsoft Agent Governance Toolkit (AGT), March-April 2026

**Established overlap:** AGT public repository history predates DGAF's first located named formulation. March 7 records a production Agent Control Plane with constraint graphs, flight recorder, supervisor agents, shadow mode, and time-travel replay. A separate March 7 commit records MerkleAuditChain with SHA-256 and Ed25519 delegation verification. March 16 adds AuthorityResolver and multi-state authority decisions. An April 18 ADR describes a critic-with-veto layer, decision-boundary checks, and blast-radius escalation integrated with GovernanceGate.

**DGAF implication:** Runtime governance, supervisory structures, authority resolution, cryptographic audit/delegation, veto, escalation, and topology-sensitive risk escalation cannot be presented as DGAF inventions.

**Candidate distinction:** In the inspected AGT material, governance is organized primarily around agents/actions/decisions and governance gates. Whether AGT also makes a dynamically changing formation the persistent primary governed object, with the exact DGAF lifecycle semantics, remains unresolved.

**Status:** **Strong external prior / near-composition comparator.**

Primary sources:

- https://github.com/microsoft/agent-governance-toolkit/commit/f8113811c33f2ff7c54465c71bb503c5dbdd5f21
- https://github.com/microsoft/agent-governance-toolkit/commit/b9d1a5aae203d65e4cb3dabe23755360b0035abc
- https://github.com/microsoft/agent-governance-toolkit/commit/3155b34371ac0521a31987b5583a21c49f8bc46e
- https://github.com/microsoft/agent-governance-toolkit/blob/359a2332f57d9000924baba269ed24e4e15ad8b0/docs/adr/0006-constitutional-constraint-layer-as-community-extension.md

### E. SLSA

**Established overlap:** SLSA verification binds evidence to the artifact or source revision actually under verification. Source verification explicitly asks whether an attestation applies to the fetched revision; source attestations carry immutable revision identifiers/digests and can include tree digests.

**DGAF implication:** Exact source/artifact identity, immutable revision binding, evidence applicability, and verification against the actual object are established external principles.

**Status:** **Strong external prior.**

Primary sources:

- https://slsa.dev/spec/v1.0/verifying-artifacts
- https://slsa.dev/spec/v1.2/verifying-source
- https://slsa.dev/spec/v1.2/source-requirements

### F. in-toto attestation validation

**Established overlap:** The validation model hashes the artifact and matches it against attested subjects; if no acceptable subject digest matches, validation rejects the attestation.

**DGAF implication:** Subject/digest binding and independent verification of artifact-scoped evidence are external prior art.

**Status:** **Strong external prior.**

Primary source: https://github.com/in-toto/attestation/blob/main/docs/validation.md

### G. Runtime action-boundary governance and related agent-assurance work

**Established overlap:** Pre-execution policy mediation, fail-closed control, provenance, authorization, runtime assurance, deterministic replay, and trace evidence are all established research/engineering directions.

**DGAF implication:** Individual runtime governance mechanisms are not sufficient grounds for a DGAF novelty claim.

**Status:** **External prior / broad overlap.**

## DGAF source adjudication

### H. DGAF named formulation — 2026-04-29

Commit `bb5c8f19d393cf04eacac66ba3a58df97671bfdb` changes the public expansion to **Dynamic Governance Agentic Formation**. The repository issue created that day records the framework as identified during Session 004.

**What this establishes:** Earliest currently located public repository evidence for the named DGAF formulation.

**What it does not establish:** Firstness of agent governance, dynamic formation, organizational authority, veto, provenance, or any other primitive.

Primary sources:

- https://github.com/ndrorchestration/DGAF-Framework/commit/bb5c8f19d393cf04eacac66ba3a58df97671bfdb
- https://github.com/ndrorchestration/DGAF-Framework/issues/1

**Status:** **Historical provenance fact; not a novelty verdict.**

### I. DGAF formation semantics — 2026-05-01

Commit `edc9f93da03747cfab3a6610d3349a122ba5f128` adds to the Harmonic Quintet specification:

- explicit authority conflict resolution;
- sovereign veto semantics;
- a sole resolver;
- timeout escalation and blocking;
- idempotency guarantee for rerunning the same formation wave state;
- avoidance of duplicate sovereign audit-log entries.

**What this establishes:** Concrete DGAF implementation/specification evidence for formation-level authority conflict, veto, escalation, and idempotent replay.

**Temporal limitation:** Because this is dated May 1, it cannot establish that the complete composition existed before the April 29 named formulation unless earlier evidence is found.

Primary source: https://github.com/ndrorchestration/DGAF-Framework/commit/edc9f93da03747cfab3a6610d3349a122ba5f128

**Status:** **DGAF implementation evidence; historical priority unresolved.**

### J. DGAF development/candidate separation — 2026-08-21

The candidate-separation document explicitly distinguishes moving development state from an identified candidate and states that allowing development to collapse into the candidate would make subsequent evidence ambiguous. It proposes a candidate manifest/reference and exact SHA attribution before freeze/authorization.

**Established external baseline:** release engineering and provenance systems already use immutable/revision-scoped candidate identity and stale-evidence rejection.

**Potential DGAF distinction:** Using that separation explicitly as an **experimental evidentiary control** in the authorization lifecycle.

Primary source: `docs/experiment/DEVELOPMENT_CANDIDATE_SEPARATION_2026-08-21.md`

**Status:** **Potentially distinctive application; not a novel provenance primitive.**

## Current contribution hypothesis

The strongest remaining DGAF contribution hypothesis is not a novel mechanism. It is a cross-domain integration:

> DGAF may have independently coupled organizational formation governance with software/experimental identity governance, so that formation state, authority transitions, evidence provenance, exact candidate identity, verification, and authorization participate in one continuously constrained lifecycle.

This hypothesis is conditional. A prior system can defeat it only if it materially matches the same governed object and lifecycle, not merely because it contains similar components.

## Explicit non-claims

This review does not establish that DGAF is:

- the first governance framework for agentic AI;
- the first multi-agent orchestration framework;
- the first system to treat organizational formation dynamically;
- the first system to assign authority to organizational structure;
- the first system to use veto or escalation;
- the first system to use idempotency in distributed agent systems;
- the first system to bind evidence to exact artifacts or revisions;
- the first system to distinguish candidates from moving development;
- empirically better than alternative approaches;
- novel in an absolute sense.

## Current research questions

1. Did any public pre-2026-04-29 system implement the full formation-level composition `formation + authority + veto/conflict + idempotent transition + evidence` as one explicit architecture?
2. Did any public system before the relevant DGAF milestone connect formation-governance state directly to exact experimental candidate identity and authorization?
3. Does any predecessor preserve governed-object identity continuously across formation transitions, execution evidence, candidate verification, and promotion/authorization?
4. Are any claimed DGAF distinctions merely established release/provenance patterns reapplied to a new domain?

## Adjudication standard

A strong historical predecessor must be:

1. publicly accessible before the comparison cutoff;
2. reliably dated through a primary source;
3. concrete enough to demonstrate implementation or a specific formal architecture;
4. materially equivalent in governed object and transition semantics;
5. accompanied by enough evidence to distinguish mechanism-level overlap from architectural equivalence.

“No match located” means only that the bounded search has not located an equivalent. It is not evidence of global absence.

## Next actions

1. Preserve the 2026-09-01 historical-priority adjudication as the current baseline.
2. Expand primary-source searches across organizational MAS, agent governance, distributed reconfiguration, software supply-chain security, and research workflow provenance.
3. Inspect implementation-level evidence for the closest near-composition candidates.
4. Keep historical-priority claims independent from current PDMAL empirical status.
5. Update the contribution statement only when new primary evidence changes the adjudication.

## Cross-references

- [`DGAF_HISTORICAL_PRIORITY_ADJUDICATION_2026-09-01.md`](DGAF_HISTORICAL_PRIORITY_ADJUDICATION_2026-09-01.md)
- [`DGAF_RELATED_WORK_MATRIX.md`](../DGAF_RELATED_WORK_MATRIX.md)
- [`../PRIOR_ART_AND_RELATED_WORK_SCOPE.md`](../PRIOR_ART_AND_RELATED_WORK_SCOPE.md)
- [`../PUBLICATION_AND_PROVENANCE_SPINE.md`](../PUBLICATION_AND_PROVENANCE_SPINE.md)
- [`../CLAIM_EVIDENCE_INDEX.md`](../CLAIM_EVIDENCE_INDEX.md)
- [`../EPISTEMIC_EVIDENCE_STANDARD.md`](../EPISTEMIC_EVIDENCE_STANDARD.md)
