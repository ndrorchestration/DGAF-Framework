---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-09-02
applies_to_sha: ecffc0a25e7ab63a1032f08ebd80db06fa74dfd7
corrected_apparatus_source: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
runtime_candidate_sha: ecffc0a25e7ab63a1032f08ebd80db06fa74dfd7
candidate_status: P-35 VALIDATED / NOT FROZEN / P3-P9 EVIDENCE REMAINING
active_p35_remediation_head: ecffc0a25e7ab63a1032f08ebd80db06fa74dfd7
active_p35_pre_freeze_run: 33696841449 PASS
---

# PDMAL Current Control State

This is the current pre-authorization control record. The active implementation candidate is PR #199 / branch `remediation/p35-minimal-mainline-2026-09-02`. Historical evidence remains scoped to its exact tested SHA; implemented controls are not equivalent to executed experimental verification evidence.

## Identity boundary

The corrected apparatus source is `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`. It remains the canonical provenance anchor for the restored behavior-affecting DGAF/TGL gate-state substrates.

The previous runtime candidate `92ff830b1c67413df745e37087e6447c9c251b9a` remains historical/non-closing for the current completion cycle. It is not promoted merely because documentation references the remediation candidate.

The active P-35 remediation is PR #199 / branch `remediation/p35-minimal-mainline-2026-09-02`, at `ecffc0a25e7ab63a1032f08ebd80db06fa74dfd7`. The exact-head pre-freeze validation run `33696841449` passed. No pilot authorization or empirical execution is enabled.

## Current state

| Control | State | Evidence / scope |
|---|---|---|
| Historical freeze | HISTORICAL / SUPERSEDED | `3510b868…` is provenance only |
| Corrected apparatus source | CANONICAL PROVENANCE ANCHOR | `2a54a67d…` |
| Previous runtime candidate | HISTORICAL / SUPERSEDED FOR CURRENT CYCLE | `92ff830b…`; tree `73cf3ad…` |
| Active completion candidate | CURRENT P-35 REMEDIATION / NOT FROZEN | `ecffc0a25e7…`; PR #199 |
| Candidate lineage | ESTABLISHED | current `main` `275756fd…` → PR #199 |
| P-35 implementation | VALIDATED / EXACT-HEAD | run `33696841449`; contract and fail-closed integration checks passed |
| P2 runtime | HISTORICAL VERIFIED / RE-RUN REQUIRED | prior evidence remains candidate-specific |
| P6a CORS | HISTORICAL VERIFIED / RE-RUN REQUIRED | prior evidence remains candidate-specific |
| P3 | OPEN / RE-RUN REQUIRED | current-candidate artifact contract evidence required |
| P4 | OPEN | current-cycle operational blinding/custody evidence required |
| P5 | OPEN | current-cycle reproducibility evidence required |
| P6 | OPEN / FAIL-CLOSED | current-cycle durable custody proof required |
| P7 scientific specification | ADOPTED / FINAL BINDING OPEN | must bind exact candidate/protocol/analysis/freeze identity |
| P8 analysis lock | OPEN / FAIL-CLOSED | requires current-candidate prerequisites and final P9 evidence |
| P9 independent verification | NOT EXECUTED FOR ACTIVE CANDIDATE | independent audit/reproduction required |
| New freeze | NOT CREATED | candidate is not frozen |
| Pilot authorization | NOT GRANTED | separate governance transition |
| Empirical data | N = 0 | no authorized pilot execution |

## P-35 boundary

The active implementation requires an explicit callable `PDMAL_PREMISE_CHECKER` in `module:attribute` form for DGAF pilot execution. Missing, malformed, unloadable, or non-callable configuration is fail-closed. `ConsensusTask(condition="dgaf")` rejects omission. The resolved checker is propagated into `DGAF_TGLAdapter` and then into `TGLHooks`. The exact-head regression also verifies checker invocation and the resulting fail-closed `UNRECOVERED_FAILURE` / `ffcr_success=False` contract.

Exact-head validation is now complete at `ecffc0a25e7ab63a1032f08ebd80db06fa74dfd7`, using pre-freeze runner `33696841449`. This closes the P-35 predicate for this candidate only.

## Required closure sequence

1. Complete current-candidate P3 artifact-contract evidence.
2. Complete P4 operational blinding/custody evidence.
3. Complete P5 environment/topology/RNG reproducibility evidence.
4. Complete P6 durable archive/retrieval/hash evidence.
5. Bind P7 to the exact candidate/protocol/analysis/final-freeze identity.
6. Close P8 from current-candidate evidence only.
7. Execute independent P9 verification against the final exact candidate.
8. Create and independently verify a new immutable freeze.
9. Obtain explicit pilot authorization.
10. Only then execute the blinded pilot.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**

## Anti-loop rule

A documentation-only commit, CI fan-out, deployment-health success, runtime verification result, historical evidence artifact, or repeated semantic audit does not authorize scientific execution. Evidence must remain bound to its exact candidate/deployment/predicate scope.
