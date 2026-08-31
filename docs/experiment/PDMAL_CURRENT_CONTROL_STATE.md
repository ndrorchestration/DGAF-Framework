---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-31
applies_to_sha: d56b5b3c44e39ddb8c883259584432ab39259306
pre_freeze_candidate_sha: d56b5b3c44e39ddb8c883259584432ab39259306
pre_freeze_candidate_ref: main / post-#170 restored apparatus boundary
candidate_status: PROVISIONAL / NOT FROZEN / REQUIRES FRESH CANDIDATE-SCOPED VERIFICATION
---

# PDMAL Current Control State

This is the current pre-authorization control record. Historical evidence remains scoped to its exact tested SHA; implemented controls are not equivalent to executed experimental verification evidence.

## Current state

| Control | State | Evidence / blocker |
|---|---|---|
| Historical freeze | HISTORICAL / SUPERSEDED | `3510b868…` is provenance only |
| Prior engineering/production source | VERIFIED / HISTORICAL SCOPE | `303f4424…`; prior P2/P6a deployment and evidence |
| Prior pre-remediation candidate | SUPERSEDED / HISTORICAL | `c6157158…`; evidence does not transfer |
| Superseded post-#151 candidate | SUPERSEDED / HISTORICAL | `05fa286…`; prior P2/P6a/P3-P9 package does not transfer |
| **Current restored apparatus / provisional candidate** | **DESIGNATED / NOT FROZEN** | `d56b5b3c44e39ddb8c883259584432ab39259306` from merged #170 |
| Current apparatus tree | IDENTIFIED | `8c13900c4ce2a503414f9dddf1d7ef7debead57e` |
| Current production deployment | IDENTIFIED / READY | `dpl_76UU8mCmCgKkphF9b1iWvFTVCsRb` |
| Corrected runner | IMPLEMENTED / EVIDENCE GATED | Fresh candidate execution evidence still required |
| Seven-gate constitutive restoration | IMPLEMENTED / PRE-FREEZE VALIDATED | P-31/P-33/P-27/P-29/P-30/P-32/DemiJoule restored and validated on pre-merge exact head |
| P7 scientific specification | ADOPTED / BINDING PENDING | Must bind to eventual final freeze identity |
| P8 analysis lock | OPEN / FAIL-CLOSED | Final candidate evidence incomplete |
| Artifact contract | IMPLEMENTED / OPEN | Fresh candidate-scoped execution evidence required |
| Blinding custody | OPEN | Current-cycle operational custody/separation evidence required |
| Durable retention | OPEN | Archive/retrieval/hash proof required |
| R1–R4 semantic recovery | CLOSED / FAIL-CLOSED | Do not reopen absent genuinely new authoritative semantic evidence |
| P2 runtime | NEW CANDIDATE OPEN | Fresh run required for `d56b5b3c…` + exact deployment |
| P6a CORS | NEW CANDIDATE OPEN | Fresh run required for same deployment + configured origin |
| P3 | IMPLEMENTED / OPEN | Current candidate evidence required |
| P4 | OPEN | Current-cycle blinding/custody evidence required |
| P5 | OPEN | Current-cycle reproducibility evidence required |
| P6 | OPEN / FAIL-CLOSED | Current-cycle durable custody proof required |
| P9 independent verification | NOT EXECUTED FOR CURRENT CANDIDATE | Independent audit/reproduction required |
| New freeze | NOT CREATED | Candidate is provisional, not frozen |
| Pilot authorization | NOT GRANTED | Separate governance transition |
| Empirical data | N = 0 | No authorized pilot execution |

## Candidate identity boundary

PR #170 merged the completed seven-gate restoration and provenance integration as apparatus-changing commit `d56b5b3c…`. This is the current restored apparatus/source boundary and provisional candidate basis.

The superseded post-#151 candidate `05fa286…` and its designation record `02c146d1…` remain historical. No evidence bound to either transfers to `d56b5b3c…`.

Documentation commits may advance the `main` control-plane lineage without changing `d56b5b3c…` as the apparatus source. The eventual frozen identity must additionally bind the exact candidate tree/protocol/dependencies/deployment and final P1-P9 state.

## Current deployment/runtime boundary

Current deployment identity:

- deployment ID: `dpl_76UU8mCmCgKkphF9b1iWvFTVCsRb`
- deployment URL: `https://dynamicgovernanceagenticformation-ltttt6oip-ndrorchestration.vercel.app`
- allowed CORS origin: `https://dynamicgovernanceagenticformation-ndrorchestration.vercel.app`
- Vercel source SHA must equal candidate SHA at every runtime verification.

These are candidate inputs, not P2/P6a evidence until the fresh authenticated workflows execute and emit retained artifacts.

## Historical runtime evidence

P2 run `33300481208` and P6a run `33302495240` remain exact historical evidence for `303f4424…` and its deployment boundary. They are not evidence for the current candidate.

## Required next evidence events

1. Execute fresh P2 runtime verification against `d56b5b3c…`, `dpl_76UU8mCmCgKkphF9b1iWvFTVCsRb`, and the exact deployment URL.
2. Execute fresh P6a CORS verification against the same candidate/deployment and the configured allowed origin.
3. Complete P3 current-candidate artifact-contract evidence.
4. Complete P4 operational blinding/custody evidence.
5. Complete P5 environment/topology/RNG reproducibility evidence.
6. Complete P6 durable archive/retrieval/hash evidence.
7. Bind P7 to the exact candidate/protocol/analysis/freeze identity.
8. Close P8 from current-candidate evidence.
9. Execute independent P9 verification.
10. Create and independently verify a new immutable freeze.
11. Obtain explicit pilot authorization.
12. Only then execute the blinded pilot.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**

## Anti-loop rule

A documentation-only commit, CI fan-out, deployment-health success, historical evidence artifact, or repeated semantic audit does not create a new apparatus candidate or reopen a completed recovery determination. A new candidate cycle is created only by an executable apparatus change or an explicitly governed treatment-specification change.
