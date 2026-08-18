---
status: TEMPLATE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-18
applies_to_sha: N/A until freeze
---

# PDMAL Freeze Manifest Template

Populate this document only when all required pre-freeze controls are independently verified. The completed manifest should be committed as `FREEZE_MANIFEST.md` in the freeze commit.

## 1. Protocol / Design

| Item | Value / SHA |
|---|---|
| Protocol document | `___` |
| Protocol commit SHA | `___` |
| Task specification | `v0.7.4` |
| Task specification commit SHA | `___` |
| Analysis plan commit SHA | `___` |
| Primary endpoint | FFCR |
| Secondary endpoint | `final_std` |
| Consensus threshold | `< 0.01` |

## 2. Implementation

| Item | Value / SHA |
|---|---|
| Freeze runner / implementation SHA | `___` |
| DGAF adapter SHA | `___` |
| Topology generation implementation SHA(s) | `___` |
| RNG implementation SHA | `___` |
| Artifact schema version | `1.0` |

## 3. Environment

| Item | Value / SHA |
|---|---|
| Python version | `___` |
| NumPy version | `___` |
| NetworkX version | `___` |
| Full lockfile SHA | `___` |
| CI runner/image identifier | `___` |
| Environment fingerprint | `___` |

## 4. Verification / Characterization

| Control | Evidence |
|---|---|
| Environment lock | `___` |
| Topology provenance | `___` |
| Artifact schema/integrity | `___` |
| ConsensusTask CI verification | `___` |
| Runtime characterization artifact | `___` |
| 300-second ceiling verdict | `PASS / FAIL` |
| Blinding operational test | `___` |
| Retention decision | `___` |

## 5. Governance / Authorization

| Item | Record |
|---|---|
| Expert-panel approval | `___` |
| Freeze timestamp | `___` |
| Freeze commit SHA | `___` |
| Freeze author | `___` |
| Protocol authorization record | `___` |
| Pilot authorization record | `___` |

## 6. Evidence Index

| Control | Evidence unit |
|---|---|
| Environment lock | `___` |
| Topology provenance | `___` |
| Artifact schema | `___` |
| ConsensusTask | `___` |
| Runtime characterization | `___` |
| Blinding | `___` |
| Retention | `___` |
| Final CI / freeze verification | `___` |

## 7. Freeze invariants

Before this manifest is accepted:

- every SHA refers to an immutable executed or committed source;
- no `PENDING`, `CANDIDATE`, or `REQUIRED` control language remains in the frozen protocol unless explicitly designated historical/contextual;
- runtime evidence is based on the real workload;
- blinding custody is operationally demonstrated;
- the retention policy is explicit;
- the environment is reproducible from the recorded lock;
- pilot authorization is separate from technical readiness;
- no empirical data is generated before the authorization record exists.
