# DGAF Historical-Priority Adjudication — 2026-09-01

**Status:** Current research adjudication; no absolute novelty or priority claim established  
**Date:** 2026-09-01  
**Scope:** Historical priority of DGAF architectural mechanisms and compositions, with emphasis on the pre-2026-04-29 record and the later candidate/evidence governance lineage.

## Executive conclusion

DGAF is **not established as first** in agent governance, dynamic multi-agent formation, organizational authority, topology-aware coordination, veto, escalation, idempotency, provenance, exact artifact identity, stale-evidence rejection, or independent verification. These mechanisms have substantial prior art across multi-agent systems, agent-governance systems, software supply-chain security, release engineering, and research provenance.

The defensible historical thesis is narrower:

> DGAF may represent an independently developed integration in which a changing multi-agent formation is treated as a persistent governed state, with formation membership/topology/authority participating in governed transitions, while experimental evidence is subsequently constrained by exact candidate identity and independently verifiable provenance/authorization.

This remains a **historical hypothesis**, not a priority verdict.

## 1. Evidence classes

Use the following distinctions:

- **External prior:** an earlier source clearly establishes the mechanism or architectural relationship.
- **Near-composition prior:** an earlier source combines major components but differs in governed object, transition semantics, or lifecycle boundary.
- **Potentially distinctive integration:** no equivalent predecessor has been located in the bounded search, but absence is not proof of global uniqueness.
- **Unresolved:** evidence is insufficient to classify the relationship.

Do not convert “no match located” into “first.”

## 2. Strong pre-DGAF external prior

### Microsoft Agent Governance Toolkit (AGT)

Public repository evidence predates the first located DGAF-named repository evidence on 2026-04-29.

- **2026-03-05:** commit `93ae721acd4b7bd276480490e7932d210c400508` records five governance packages and a coordinated release update.
- **2026-03-07:** commit `f8113811c33f2ff7c54465c71bb503c5dbdd5f21` ports a production Agent Control Plane including constraint graphs, flight recorder, supervisor agents, shadow mode, and time-travel replay.
- **2026-03-07:** commit `b9d1a5aae203d65e4cb3dabe23755360b0035abc` adds MerkleAuditChain with SHA-256 verification and Ed25519 delegation verification.
- **2026-03-16:** commit `3155b34371ac0521a31987b5583a21c49f8bc46e` adds `AuthorityResolver` and `AuthorityDecision` states (`allow`, `allow_narrowed`, `deny`, `audit`).
- **2026-04-18:** ADR 0006 describes a constitutional constraint layer with a critic agent having veto-only authority, decision-boundary checks, blast-radius escalation, and integration with a three-gate architecture. The ADR explicitly treats the constitutional layer as a governance extension rather than a general orchestration substrate.

Primary links:

- https://github.com/microsoft/agent-governance-toolkit/commit/93ae721acd4b7bd276480490e7932d210c400508
- https://github.com/microsoft/agent-governance-toolkit/commit/f8113811c33f2ff7c54465c71bb503c5dbdd5f21
- https://github.com/microsoft/agent-governance-toolkit/commit/b9d1a5aae203d65e4cb3dabe23755360b0035abc
- https://github.com/microsoft/agent-governance-toolkit/commit/3155b34371ac0521a31987b5583a21c49f8bc46e
- https://github.com/microsoft/agent-governance-toolkit/blob/359a2332f57d9000924baba269ed24e4e15ad8b0/docs/adr/0006-constitutional-constraint-layer-as-community-extension.md

**Adjudication:** AGT establishes strong external prior for runtime governance, supervision, constraint graphs, authority resolution, audit/replay, cryptographic audit/delegation, veto, and escalation.

### Dynamic organizational multi-agent systems

The multi-agent systems literature predates DGAF by many years in treating organizational structure as a dynamic object subject to reorganization and authority.

A 2004 paper, *Dynamic Reorganization of Agent Societies*, explicitly studies how organizations change dynamically and classifies reorganization using the focus of reorganization, authority to modify organization, and how decisions are taken.

Primary record:

- https://www.researchgate.net/publication/27694396_Dynamic_Reorganization_of_Agent_Societies

**Adjudication:** dynamic organizational change plus authority over organizational structure is established external prior.

### TB-CSPN / organizational agent architecture

The 2025 TB-CSPN work provides a close modern near-composition. It describes dynamic group formation, threshold-based membership changes, Supervisor/Consultant/Worker roles, hierarchical oversight, validation before structural integration, and traceability/provenance-oriented coordination.

Primary records:

- https://link.springer.com/article/10.1007/s10791-025-09667-2
- https://www.mdpi.com/1999-5903/17/8/363

**Adjudication:** dynamic formation, hierarchical oversight, authorization, and adaptive organization are established before DGAF. No exact match has been established for DGAF's later explicit combination of sovereign veto conflict resolution plus formation replay idempotency plus candidate-bound experimental authorization.

## 3. Provenance and candidate identity are established external prior

### SLSA

SLSA's verification model requires evidence to apply to the artifact or source revision actually being verified. The Source Track explicitly describes attestations scoped to source revisions and requires the verifier to check that the VSA applies to the revision fetched; the source attestation `subject.digest` identifies the immutable revision and may include `gitTree` or other content digests.

Primary records:

- https://slsa.dev/spec/v1.0/verifying-artifacts
- https://slsa.dev/spec/v1.2/verifying-source
- https://slsa.dev/spec/v1.2/source-requirements

**Adjudication:** exact artifact/revision binding, immutable source identity, and rejection of mismatched evidence are external prior. DGAF must not claim these as original primitives.

### in-toto

in-toto's validation model requires the verifier to hash the artifact and identify matching attestation subjects; if no acceptable subject digest matches, validation rejects the attestation. This establishes artifact-scoped evidence validation as prior art.

Primary record:

- https://github.com/in-toto/attestation/blob/main/docs/validation.md

**Adjudication:** exact subject-digest evidence binding and independent attestation validation are external prior.

## 4. DGAF historical record

### 2026-04-29 — named DGAF identity

Commit `bb5c8f19d393cf04eacac66ba3a58df97671bfdb` changes the framework expansion to **Dynamic Governance Agentic Formation**. The repository issue created the same day records the framework as identified during Session 004.

Primary records:

- https://github.com/ndrorchestration/DGAF-Framework/commit/bb5c8f19d393cf04eacac66ba3a58df97671bfdb
- https://github.com/ndrorchestration/DGAF-Framework/issues/1

**Adjudication:** 2026-04-29 is the earliest currently located public repository evidence identifying the named DGAF formulation. It is **not** the earliest known public occurrence of the underlying mechanisms.

### 2026-05-01 — explicit formation conflict/idempotency semantics

Commit `edc9f93da03747cfab3a6610d3349a122ba5f128` adds to the Harmonic Quintet specification:

- authority conflict resolution;
- sovereign veto semantics;
- a sole resolver;
- timeout escalation and commit blocking;
- an explicit idempotency guarantee for rerunning the same formation wave state;
- prevention of duplicate sovereign audit entries.

Primary record:

- https://github.com/ndrorchestration/DGAF-Framework/commit/edc9f93da03747cfab3a6610d3349a122ba5f128

**Adjudication:** this is concrete DGAF evidence for a formation object with authority conflict, veto, escalation, and idempotent replay. Because it is dated 2026-05-01, it cannot retroactively establish that the full composition existed before 2026-04-29.

### 2026-08-21 — development/candidate separation

The DGAF document `DEVELOPMENT_CANDIDATE_SEPARATION_2026-08-21.md` treats development and candidate as distinct identities and warns that allowing a moving `main` branch to stand in for the candidate would make the candidate ambiguous and the evidence chain untraceable. It proposes an immutable candidate reference and candidate manifest before continued development.

Primary record:

- `docs/experiment/DEVELOPMENT_CANDIDATE_SEPARATION_2026-08-21.md`
- `docs/experiment/PDMAL_EXECUTION_PATH_SPEC_2026-08-21.md`

**Adjudication:** exact-object identity and candidate immutability are established external principles. The potentially distinctive DGAF feature is the explicit use of development/candidate separation as an experimental evidentiary and authorization control.

## 5. Architecture-level historical test

A strong predecessor must be compared at the level of the governed object and lifecycle, not by counting similar nouns.

Define the candidate integrated architecture as:

`Q = <GF, AF, VF, IF, PC, XC, L>`

where:

- `GF`: formation is an explicit governed state;
- `AF`: authority is attached to formation state;
- `VF`: veto/conflict/escalation changes or constrains formation governance;
- `IF`: formation transitions are explicitly idempotent;
- `PC`: evidence is bound to an exact experimental candidate;
- `XC`: verification/authorization resolves against that candidate;
- `L`: these controls form one continuous lifecycle rather than disconnected features.

A source that has only some of these is a **near-composition prior**, not an exact predecessor.

## 6. Current feature adjudication

| Feature | Adjudication |
|---|---|
| Multi-agent orchestration | External prior |
| Dynamic formation | External prior |
| Dynamic organizational reconfiguration | External prior |
| Formation-level organizational authority | External prior |
| Graph/topology-aware coordination | External prior |
| Runtime governance | External prior |
| Supervisor governance | External prior |
| Veto | External prior |
| Escalation | External prior |
| Idempotency | External prior |
| Provenance | External prior |
| Exact artifact/source identity | External prior |
| Candidate immutability | External prior |
| Stale/mismatched evidence rejection | External prior |
| Independent verification | External prior |
| Formation + authority + veto/conflict + idempotent replay in one explicit formation spec | **Potentially distinctive composition; predecessor search incomplete** |
| Formation governance + candidate-scoped experimental evidence | **Potentially distinctive composition; predecessor search incomplete** |
| Continuous lifecycle coupling formation governance to candidate verification/authorization | **Strongest remaining historical question** |

## 7. Historical conclusion

The evidence does not support an absolute claim that DGAF was first.

It does support the following narrower statement:

> DGAF appears to have independently evolved an integrated governance architecture that connects formation state, authority, veto/escalation, evidence/provenance, exact implementation identity, verification, and authorization. The individual mechanisms are established prior art. The historical question is whether an earlier public system implemented essentially the same cross-domain lifecycle with the same governed object and transition semantics.

This conclusion should remain conditional until the bounded comparator search is expanded across organizational multi-agent systems, agent governance, distributed reconfiguration, software supply-chain security, and research workflow provenance.

## 8. Explicit non-claims

This document does **not** establish that DGAF:

- was the first agent-governance framework;
- invented dynamic multi-agent formation;
- invented formation-level authority;
- invented veto/escalation;
- invented idempotency;
- invented provenance or exact artifact binding;
- invented candidate/release separation;
- is empirically superior;
- is production-validated;
- has a globally unique architecture.

## 9. Research status

**Historical priority:** unresolved; narrowly bounded composition remains under investigation.  
**Independent architectural evolution:** supported by repository chronology.  
**Absolute novelty:** not established.  
**Empirical PDMAL efficacy:** not established; current empirical N remains 0.  
**Experimental authorization:** not granted by this historical review.

## Cross-references

- `DGAF_RELATED_WORK_MATRIX.md`
- `research/DGAF_RELATED_WORK_SOURCE_ADJUDICATION.md`
- `PRIOR_ART_AND_RELATED_WORK_SCOPE.md`
- `PUBLICATION_AND_PROVENANCE_SPINE.md`
- `CURRENT_STATE.md`
- `CLAIM_EVIDENCE_INDEX.md`
- `experiment/DEVELOPMENT_CANDIDATE_SEPARATION_2026-08-21.md`
- `experiment/PDMAL_EXECUTION_PATH_SPEC_2026-08-21.md`
