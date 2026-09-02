# DGAF Related-Work Source Adjudication

**Status:** Current source-level adjudication; not an absolute novelty determination  
**Updated:** 2026-09-01  
**Purpose:** Compare concrete prior work against DGAF mechanisms and architectural compositions, explicitly separating primitive prior art from architecture-level hypotheses.

## Method

Comparison dimensions include governed object; formation and membership; topology; authority and delegation; transition lifecycle; veto/conflict/escalation; idempotency at the relevant boundary; runtime control; provenance/evidence custody; candidate identity/immutability; verification/authorization; and reproducibility/experimental governance.

Classifications are **external prior**, **near-composition prior**, **candidate distinction**, or **unresolved**. A candidate distinction is a hypothesis for review, not a novelty verdict.

## Source adjudications

### A. Dynamic Reorganization of Decision-Making Groups (Barber & Martin, 2001)

The ACM record describes organizational structures specifying decision-making frameworks and authority, with adaptive frameworks dynamically changing who decides and who carries out decisions; experiments evaluate the reorganized systems.

**DGAF implication:** Dynamic organizational reorganization + authority + experimental evaluation is longstanding prior art. The inspected record does not establish immutable candidate identity, candidate-scoped cryptographic evidence, independent candidate verification, or authorization of a frozen software/research candidate.

**Status:** **External prior / boundary-adjacent comparator.**

Primary source: https://doi.org/10.1145/375735.376432

### B. Dynamic Reorganization of Agent Societies (Dignum, Sonenberg, Dignum, 2004)

The work explicitly studies dynamic organizational reorganization, organizational structure, authority to modify that structure, and how reorganization decisions are made.

**Status:** **External prior.**

Primary source: https://www.researchgate.net/publication/27694396_Dynamic_Reorganization_of_Agent_Societies

### C. Negotiating team formation using deep reinforcement learning (2020)

Agents negotiate to form teams and the team-formation mechanisms are experimentally evaluated.

**DGAF implication:** Dynamic team formation + experimental evaluation predates DGAF. The inspected record does not establish a governed organizational state whose transition freezes an exact software/research candidate and gates authorization using independently verified candidate evidence.

**Status:** **Near/boundary-adjacent prior.**

Primary source: https://doi.org/10.1016/j.artint.2020.103356

### D. TB-CSPN / organizational theory for multi-agent interaction (2025)

TB-CSPN provides dynamic group formation, threshold-driven membership changes, hierarchical Supervisor/Consultant/Worker roles, authorization, multi-stage validation before structural integration, and traceability-oriented coordination.

**DGAF implication:** The broad proposition that formation, role hierarchy, adaptive membership, authorization, validation, and auditable coordination can coexist in one architecture is prior to DGAF. The inspected material does not establish the complete DGAF candidate lifecycle.

**Status:** **Near-composition prior.**

Primary sources:

- https://link.springer.com/article/10.1007/s10791-025-09667-2
- https://www.mdpi.com/1999-5903/17/8/363

### E. Microsoft Agent Governance Toolkit (AGT), March-April 2026

AGT history includes constraint graphs, supervisor agents, flight recorder/replay, MerkleAuditChain, SHA-256/Ed25519 delegation verification, AuthorityResolver, multi-state authority decisions, critic-with-veto, decision-boundary checks, and blast-radius escalation.

**DGAF implication:** Runtime governance, supervision, authority resolution, cryptographic audit/delegation, veto, escalation, and topology-sensitive risk escalation cannot be presented as DGAF inventions. Whether AGT makes dynamic formation the persistent primary governed object and connects it to the complete candidate lifecycle remains unresolved.

**Status:** **Strong external prior / near-composition comparator.**

### F. Authenticated Workflows (Rajagopalan & Rao), February 2026

The February 11, 2026 arXiv record describes cryptographically authenticated agent workflows, organizational-policy enforcement, deterministic integrity checks, dynamically changing constraints as agents evolve, hierarchical policy composition, and cryptographic attestations for workflow dependencies.

**DGAF implication:** Organizational policy + evolving agent workflows + cryptographic integrity/authentication predates DGAF. The inspected record does not establish formation-state governance crossing into an exact frozen software/research candidate and subsequent candidate-bound independent verification/authorization.

**Status:** **Strong boundary-adjacent external prior; not an exact Q predecessor.**

Primary source: https://arxiv.org/abs/2602.10465

### G. OrgForge, March 2026

OrgForge's March 11, 2026 whitepaper describes a machine-readable organizational constitution, deterministic policy evaluation, signed authorization artifacts, replay safety, and execution-side verification of authorization artifacts for human, software, and AI-agent actors.

**DGAF implication:** Organizational policy → signed authorization artifact → verified execution is external prior. The inspected material does not establish dynamic formation as the governed state or a formation transition producing an exact experimental/software candidate whose evidence is independently verified before authorization.

**Status:** **Strong boundary-adjacent external prior; not an exact Q predecessor.**

Primary source: https://orgforge.io/paper/

### H. Trusted-execution team formation / attested team membership, April 2, 2026

A public patent record dated April 2, 2026 includes a team-formation embodiment in which a team specification identifies a coordinator and members, member identity evidence includes unique identifiers and device attestations, member attributes are determined, and a team proposal is generated.

**DGAF implication:** Team formation + coordinator authority + identity/attestation evidence is pre-DGAF prior. The inspected claims do not establish the complete formation-to-software/research-candidate-freeze-to-independent-verification-to-authorization lifecycle.

**Status:** **Near/boundary-adjacent prior; not an exact Q predecessor.**

Primary source: https://patents.justia.com/patent/20260095308

### I. SLSA

SLSA verification binds evidence to the artifact or source revision actually under verification. Immutable revision identifiers/digests establish applicability of evidence to the exact object.

**Status:** **Strong external prior.**

Primary sources:

- https://slsa.dev/spec/v1.0/verifying-artifacts
- https://slsa.dev/spec/v1.2/verifying-source
- https://slsa.dev/spec/v1.2/source-requirements

### J. in-toto attestation validation

in-toto validates artifact identity by digest against attested subjects and rejects when an acceptable subject does not match.

**Status:** **Strong external prior.**

Primary source: https://github.com/in-toto/attestation/blob/main/docs/validation.md

### K. Clarus, June 29 2026

Clarus describes auditable multi-phase research collaboration involving teams, agents, artifacts/evidence, audit, attribution, and checkpoints.

**Status:** **Later convergence comparator; not prior art against April/May DGAF chronology.**

Primary source: https://arxiv.org/abs/2606.30246

### L. LOGOS, July 12 2026

LOGOS describes persistent agent teams evolving artifacts, versioned agent packs, auditable traces, fail-closed verification, untrusted release candidates, held-out evidence, human policy, and explicit authorization before promotion.

**DGAF implication:** Close later convergence on the candidate/evidence/authorization side. It cannot defeat the April/May chronology because it is later.

**Status:** **Later convergence comparator.**

Primary source: https://arxiv.org/abs/2607.10878

### M. Artifact-centered scientific-agent observability, August 18 2026

This work proposes first-class claim/evidence bindings, verification records, artifact lineage, run records, archives, and steering commands for autonomous scientific agents.

**Status:** **Later convergence comparator.**

Primary source: https://arxiv.org/abs/2608.18312

### N. Runtime action-boundary governance and related agent-assurance work

Pre-execution policy mediation, fail-closed control, provenance, authorization, runtime assurance, deterministic replay, and trace evidence are established directions.

**Status:** **External prior / broad overlap.**

## DGAF source adjudication

### O. DGAF named formulation — 2026-04-29

Commit `bb5c8f19d393cf04eacac66ba3a58df97671bfdb` changes the public expansion to **Dynamic Governance Agentic Formation**. The repository issue created that day records the framework as identified during Session 004.

**What this establishes:** Earliest currently located public repository evidence for the named DGAF formulation.

**What it does not establish:** Firstness of agent governance, dynamic formation, organizational authority, veto, provenance, or any primitive.

**Status:** **Historical provenance fact; not a novelty verdict.**

### P. DGAF formation semantics — 2026-05-01

Commit `edc9f93da03747cfab3a6610d3349a122ba5f128` adds explicit authority conflict resolution, sovereign veto, sole resolver semantics, timeout escalation/blocking, idempotent formation-wave replay, and duplicate-audit prevention.

**Temporal limitation:** This is May 1 evidence and cannot establish that the complete composition existed before April 29 unless earlier evidence is found.

**Status:** **DGAF implementation evidence; historical priority unresolved.**

### Q. DGAF development/candidate separation — 2026-08-21

The candidate-separation document distinguishes moving development state from an identified candidate and requires exact SHA attribution before freeze/authorization.

**Established external baseline:** release engineering and provenance systems already use immutable/revision-scoped candidate identity and stale-evidence rejection.

**Potential DGAF distinction:** Using that separation explicitly as an **experimental evidentiary control** in the authorization lifecycle.

**Status:** **Potentially distinctive application; not a novel provenance primitive.**

## Current contribution hypothesis

The strongest remaining DGAF contribution hypothesis is:

> DGAF may have independently coupled organizational formation governance with software/experimental identity governance, so that formation state and authority transitions are carried forward into an exact experimental candidate, whose evidence is independently verified and whose authorization resolves against that same identity.

This is narrower than “formation + provenance + authorization.” Pre-DGAF systems already demonstrate substantial combinations of those components.

## Explicit non-claims

This review does not establish that DGAF is the first governance framework for agentic AI, the first multi-agent orchestration framework, the first dynamic organizational formation system, the first authority/veto/escalation system, the first cryptographic authorization system, the first exact-artifact evidence-binding system, or empirically superior.

## Current research questions

1. Did any public pre-2026-04-29 system implement the complete formation-to-candidate lifecycle with the same governed-object continuity?
2. Did any public system before the relevant DGAF milestone connect formation-governance state directly to exact experimental candidate identity and authorization?
3. Does any predecessor preserve governed-object identity continuously across formation transitions, candidate creation, execution evidence, independent verification, and promotion/authorization?
4. Are remaining DGAF distinctions merely established release/provenance/authorization patterns reapplied to a new domain?

## Adjudication standard

A strong historical predecessor must be publicly accessible before the comparison cutoff, reliably dated through a primary source, concrete enough to demonstrate implementation or a specific formal architecture, materially equivalent in governed object and transition semantics, and supported sufficiently to distinguish mechanism-level overlap from architectural equivalence.

“No match located” means only that the bounded search has not located an equivalent. It is not evidence of global absence.

## Latest audit tranches

- `DGAF_HISTORICAL_PRIORITY_TRANCHE_2026-09-01_02.md`
- `DGAF_HISTORICAL_PRIORITY_TRANCHE_2026-09-01_03.md`

## Cross-references

- `DGAF_HISTORICAL_PRIORITY_ADJUDICATION_2026-09-01.md`
- `DGAF_HISTORICAL_PRIORITY_TRANCHE_2026-09-01_02.md`
- `DGAF_HISTORICAL_PRIORITY_TRANCHE_2026-09-01_03.md`
- `../DGAF_RELATED_WORK_MATRIX.md`
- `../PRIOR_ART_AND_RELATED_WORK_SCOPE.md`
- `../PUBLICATION_AND_PROVENANCE_SPINE.md`
- `../CLAIM_EVIDENCE_INDEX.md`
- `../EPISTEMIC_EVIDENCE_STANDARD.md`
