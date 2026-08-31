---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-31
applies_to_sha: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
pre_freeze_candidate_sha: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
pre_freeze_candidate_ref: main / post-#174 provenance-corrected apparatus boundary
candidate_status: PROVISIONAL / NOT FROZEN / REQUIRES FRESH DEPLOYMENT + CANDIDATE-SCOPED VERIFICATION
---

# PDMAL Current Control State

This is the current pre-authorization control record. Historical evidence remains scoped to its exact tested SHA; implemented controls are not equivalent to executed experimental verification evidence.

## Current state

| Control | State | Evidence / blocker |
|---|---|---|
| Historical freeze | HISTORICAL / SUPERSEDED | `3510b868…` is provenance only |
| Prior engineering/production source | VERIFIED / HISTORICAL SCOPE | `303f4424…`; prior runtime boundary |
| Superseded post-#151 candidate | SUPERSEDED / HISTORICAL | `05fa286…`; evidence does not transfer |
| Pre-correction restored apparatus | INVALIDATED / HISTORICAL | `d56b5b3c…`; provenance identity omitted five restored gate-state blocks |
| **Current corrected apparatus / provisional candidate basis** | **IDENTIFIED / NOT FROZEN** | `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1` from merged #174 |
| Current apparatus tree | IDENTIFIED | `973c92335caf84f37fc2b3c4df6dd83b3b855087` |
| Current production deployment | NOT YET ESTABLISHED | No authoritative deployment for `2a54a67d…` captured yet |
| Provenance identity | COMPLETE / VALIDATED | All seven restored gate-state blocks included in canonical identity |
| Seven-gate constitutive restoration | IMPLEMENTED / PRE-FREEZE VALIDATED | Semantic restoration and provenance integrity validated; no current-candidate runtime evidence yet |
| P7 scientific specification | ADOPTED / BINDING PENDING | Must bind to eventual final freeze identity |
| P8 analysis lock | OPEN / FAIL-CLOSED | Final candidate evidence incomplete |
| Artifact contract | IMPLEMENTED / OPEN | Fresh candidate-scoped execution evidence required |
| Blinding custody | OPEN | Current-cycle operational custody/separation evidence required |
| Durable retention | OPEN | Archive/retrieval/hash proof required |
| R1–R4 semantic recovery | CLOSED / FAIL-CLOSED | Do not reopen absent genuinely new authoritative semantic evidence |
| P2 runtime | BLOCKED UNTIL DEPLOYMENT | Fresh run required for `2a54a67d…` + exact deployment |
| P6a CORS | BLOCKED UNTIL DEPLOYMENT | Fresh run required for same candidate/deployment + configured origin |
| P3 | IMPLEMENTED / OPEN | Current-candidate evidence required |
| P4 | OPEN | Current-cycle blinding/custody evidence required |
| P5 | OPEN | Current-cycle reproducibility evidence required |
| P6 | OPEN / FAIL-CLOSED | Current-cycle durable custody proof required |
| P9 independent verification | NOT EXECUTED FOR CURRENT CANDIDATE | Independent audit/reproduction required |
| New freeze | NOT CREATED | Candidate is provisional, not frozen |
| Pilot authorization | NOT GRANTED | Separate governance transition |
| Empirical data | N = 0 | No authorized pilot execution |

## Candidate identity boundary

PR #174 merged the provenance-integrity correction as apparatus-changing commit `2a54a67d…`. This is the current corrected apparatus/source boundary and the basis for the new candidate cycle.

The prior `d56b5b3c…` source is invalidated as an execution candidate because its canonical identity was incomplete. Its deployment `dpl_76UU8mCm…` and all evidence derived from that source are historical/non-closing.

The eventual frozen identity must additionally bind the exact candidate tree/protocol/dependencies/deployment and final P1-P9 state.

## Current deployment/runtime boundary

No current deployment identity is established yet for `2a54a67d…`. A deployment is usable for P2/P6a only after Vercel reports READY, production target as required, and exact Git source SHA equality with `2a54a67d…`.

## Historical runtime evidence

P2 run `33300481208` and P6a run `33302495240` remain exact historical evidence for earlier apparatus/deployment boundaries. They are not evidence for the post-#174 candidate.

## Required next evidence events

1. Establish and verify an exact deployment sourced from `2a54a67d…`.
2. Execute fresh P2 runtime verification against that exact deployment.
3. Execute fresh P6a CORS verification against the same deployment and configured origin.
4. Complete P3 current-candidate artifact-contract evidence.
5. Complete P4 operational blinding/custody evidence.
6. Complete P5 environment/topology/RNG reproducibility evidence.
7. Complete P6 durable archive/retrieval/hash evidence.
8. Bind P7 to the exact candidate/protocol/analysis/freeze identity.
9. Close P8 from current-candidate evidence.
10. Execute independent P9 verification.
11. Create and independently verify a new immutable freeze.
12. Obtain explicit pilot authorization.
13. Only then execute the blinded pilot.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**

## Anti-loop rule

A documentation-only commit, CI fan-out, deployment-health success, historical evidence artifact, or repeated semantic audit does not create a new apparatus candidate or reopen a completed recovery determination. A new candidate cycle is created only by an executable apparatus change or an explicitly governed treatment-specification change.
