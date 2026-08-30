---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-30
applies_to_sha: 05fa286614bd80576c1f7f4b01f1bdd7fe57ef37
pre_freeze_candidate_sha: 05fa286614bd80576c1f7f4b01f1bdd7fe57ef37
pre_freeze_candidate_ref: main / post-#151 apparatus boundary
candidate_status: DESIGNATED / NOT FROZEN / REQUIRES FRESH CANDIDATE-SCOPED VERIFICATION
---

# PDMAL Current Control State

This is the current pre-authorization control record. Historical evidence remains scoped to its exact tested SHA; implemented controls are not equivalent to executed experimental verification evidence.

## Current state

| Control | State | Evidence / blocker |
|---|---|---|
| Historical freeze | HISTORICAL / SUPERSEDED | `3510b868…` is provenance only |
| Prior engineering/production source | VERIFIED / HISTORICAL SCOPE | `303f4424…`; prior P2/P6a deployment and evidence |
| Prior pre-remediation candidate | SUPERSEDED / HISTORICAL | `c6157158…`; post-#151 evidence does not inherit this identity |
| **Current post-#151 apparatus candidate** | **DESIGNATED / NOT FROZEN** | `05fa286614bd80576c1f7f4b01f1bdd7fe57ef37` |
| Candidate designation/control commit | CONTROL RECORD | `02c146d1…`; not apparatus identity |
| Corrected runner | IMPLEMENTED / EVIDENCE GATED | Exact candidate execution evidence still required |
| TGL contract | VERIFIED ENGINEERING CONTROL | F1 fail-closed remediation and F2/F3 controls merged in #151 |
| P7 scientific specification | ADOPTED / BINDING PENDING | Must bind to eventual final freeze identity |
| P8 analysis lock | OPEN / FAIL-CLOSED | Final apparatus/candidate evidence incomplete |
| Artifact contract | IMPLEMENTED / OPEN | Fresh candidate-scoped execution evidence required |
| Blinding custody | OPEN | Operational custody/separation evidence required |
| Durable retention | OPEN | Archive/retrieval/hash proof required |
| P2 runtime | PRIOR VERIFIED / CURRENT CANDIDATE OPEN | Run `33300481208` remains exact for `303f4424…`; fresh current-candidate execution required |
| P6a CORS | PRIOR VERIFIED / CURRENT CANDIDATE OPEN | Run `33302495240` remains exact for `303f4424…`; fresh current-candidate execution required |
| P9 independent verification | NOT EXECUTED FOR CURRENT CANDIDATE | Independent audit/reproduction required |
| New freeze | NOT CREATED | Candidate is designated, not frozen |
| Pilot authorization | NOT GRANTED | Separate governance transition |
| Empirical data | N = 0 | No authorized pilot execution |

## Candidate identity boundary

PR #151 merged as apparatus-changing commit `05fa286…`. That merge establishes the new candidate-cycle boundary. The previous candidate `c6157158…` and all evidence bound to it are retained as historical provenance and do not transfer automatically.

The subsequent designation/control commit `02c146d1…` records candidate designation but is not itself the apparatus identity. Documentation commits after designation do not alter the designated apparatus unless executable apparatus changes occur.

## Historical runtime evidence

P2 run `33300481208` and P6a run `33302495240` remain valid, exact evidence for candidate `303f4424…` and deployment `dpl_FbPSc3K9VFWESXuUuWDepBKwKra8`. They are not evidence for `05fa286…`.

## Candidate deployment/runtime boundary

The post-#151 candidate must have an exact deployment identity verified before current-candidate P2/P6a can close. Deployment readiness alone does not establish runtime predicate completion.

## Required next evidence events

1. Verify exact candidate/deployment identity for `05fa286…`.
2. Execute fresh P2 runtime verification against that exact candidate/deployment.
3. Execute fresh P6a CORS verification against the same exact candidate/deployment.
4. Complete P3 candidate-scoped artifact-contract execution evidence.
5. Reconcile/reify historical P-31/P-27/P-29/P-32/P-30/P-33/DemiJoule contracts under Issue #152 before any gate is restored.
6. Complete P4 operational blinding/custody evidence.
7. Complete P5 environment/topology/RNG reproducibility evidence.
8. Complete P6 durable archive/retrieval/hash evidence.
9. Bind P7 to the exact final candidate/protocol/analysis/freeze identity.
10. Close P8 from current-candidate evidence.
11. Execute independent P9 verification.
12. Create and independently verify a new immutable freeze.
13. Obtain explicit pilot authorization.
14. Only then execute the blinded pilot.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
