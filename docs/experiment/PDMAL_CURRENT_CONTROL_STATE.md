---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-09-03
applies_to_sha: 0b1190fe91db6b963da0b31492d61fa1a34381e3
corrected_apparatus_source: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
validated_p35_candidate: 0b1190fe91db6b963da0b31492d61fa1a34381e3
candidate_status: P-35 VALIDATED / NOT FROZEN / P3-P9 EVIDENCE REMAINING
active_p35_remediation_branch: remediation/p35-minimal-mainline-2026-09-02
active_p35_remediation_pr: 199
active_p35_pre_freeze_run: 33697643625 PASS
active_governance_run: 33697643702 PASS
---

# PDMAL Current Control State

This is the current pre-authorization control record. The validated implementation candidate is PR #199 at exact candidate `0b1190fe91db6b963da0b31492d61fa1a34381e3`. Later documentation-only commits are control-plane records and do not inherit or become experimental candidate evidence.

## Identity boundary

The corrected apparatus source is `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`. It remains the canonical provenance anchor for the restored behavior-affecting DGAF/TGL gate-state substrates.

The previous runtime candidate `92ff830b1c67413df745e37087e6447c9c251b9a` remains historical/non-closing for the current completion cycle. It is not promoted merely because documentation references the remediation candidate.

PR #199 / branch `remediation/p35-minimal-mainline-2026-09-02` has a validated P-35 implementation candidate at `0b1190fe91db6b963da0b31492d61fa1a34381e3`. No pilot authorization, freeze, unblinding, or empirical execution is enabled.

## Current state

| Control | State | Evidence / scope |
|---|---|---|
| Historical freeze | HISTORICAL / SUPERSEDED | provenance only |
| Corrected apparatus source | CANONICAL PROVENANCE ANCHOR | `2a54a67d…` |
| Validated P-35 candidate | CURRENT / NOT FROZEN | `0b1190fe…`; PR #199 |
| P-35 validation | **CLOSED / VALIDATED** | Pre-Freeze Runner `33697643625`; Governance CI `33697643702`; exact candidate `0b1190fe…` |
| P2 runtime | HISTORICAL VERIFIED / RE-RUN REQUIRED | prior evidence bound to `92ff830b…` / historical deployment |
| P3 | HISTORICAL WORKFLOW EVIDENCE / RE-RUN REQUIRED | fresh final-candidate artifact-contract evidence required |
| P4 | OPEN | current-cycle operational blinding/custody evidence required |
| P5 | OPEN | current-cycle reproducibility evidence required |
| P6 | OPEN / FAIL-CLOSED | current-cycle durable custody proof required |
| P6a | HISTORICAL VERIFIED / RE-RUN REQUIRED | prior evidence bound to `92ff830b…` / historical deployment |
| P7 scientific specification | ADOPTED / FINAL BINDING OPEN | exact candidate/protocol/analysis/freeze binding required |
| P8 analysis lock | OPEN / FAIL-CLOSED | current-candidate prerequisites and independent P9 required |
| P9 independent verification | HISTORICAL SCOPED PASS / RE-VERIFY REQUIRED | prior evidence bound to superseded candidate |
| New freeze | NOT CREATED | candidate is not frozen |
| Pilot authorization | NOT GRANTED | separate governance transition |
| Empirical data | N = 0 | no authorized pilot execution |

## P-35 boundary and closure

The validated implementation requires an explicit callable `PDMAL_PREMISE_CHECKER` in `module:attribute` form for DGAF execution. Missing, malformed, unloadable, or non-callable configuration is fail-closed. `ConsensusTask(condition="dgaf")` rejects omission. The resolved checker is propagated into `DGAF_TGLAdapter` and then `TGLHooks`.

The exact candidate `0b1190fe…` completed the fresh P-35/pre-freeze/governance validation wave successfully. The regression verifies explicit checker invocation on the real runner/task/adapter/TGL path and preserves the fail-closed `UNRECOVERED_FAILURE` / `ffcr_success=False` contract. P-35 is therefore **CLOSED / VALIDATED** for exact candidate `0b1190fe…`.

## Required closure sequence

1. Retain `0b1190fe…` as the validated P-35 implementation candidate and preserve its exact evidence boundary.
2. Reconcile the final experimental candidate and deployment identity.
3. Complete fresh P3 artifact-contract evidence.
4. Complete P4 operational blinding/custody evidence.
5. Complete P5 environment/toolchain/topology/RNG reproducibility evidence.
6. Complete P6 durable archive/retrieval/hash evidence.
7. Apply final exact P7 candidate/protocol/analysis binding.
8. Close P8 from current-candidate evidence only.
9. Independently verify P9 against the final exact candidate.
10. Create and independently verify a new immutable freeze.
11. Obtain separate explicit pilot authorization.
12. Only then execute the blinded pilot.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**

## Anti-loop / evidence-transfer rule

Documentation commits, CI success, deployment readiness, historical evidence, and repeated audits do not authorize empirical execution or transfer evidence across candidates. Every closure claim must identify its exact candidate, run, artifact, deployment, and predicate scope.
