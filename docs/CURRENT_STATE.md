---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-09-03
applies_to_ref: main
corrected_apparatus_source: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
validated_p35_candidate: 0b1190fe91db6b963da0b31492d61fa1a34381e3
validated_p35_candidate_validation_run: 33697643625
validated_governance_run: 33697643702
current_control_plane_head: 746bd0b0f6c53742df8f7955a9183321556d97b0
---
# DGAF-Framework / PDMAL — Current State

GitHub is authoritative for implementation and CI; governance decisions must be recorded through the project's governance process. Historical evidence remains scoped to the exact SHA/run/deployment/artifact that produced it.

> **Current boundary:** `main` remains the documentation/control-plane lineage. The corrected apparatus source is `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1` and remains the canonical provenance anchor.
>
> **Validated P-35 implementation candidate:** PR #199 / branch `remediation/p35-minimal-mainline-2026-09-02`, exact candidate `0b1190fe91db6b963da0b31492d61fa1a34381e3`. Fresh exact-head PDMAL Pre-Freeze Runner Validation run `33697643625` and Governance CI run `33697643702` both passed. Later documentation-only commits are control-plane records and do not inherit or replace this candidate-bound evidence.
>
> **Previous runtime/completion candidates:** `92ff830b…` and `a43219b…` remain historical evidence boundaries for this cycle. Their evidence is not transferred to PR #199.
>
> **Current experimental boundary:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.

## Authoritative experimental state

| Boundary | Status | Meaning |
|---|---|---|
| Corrected apparatus source | CANONICAL PROVENANCE ANCHOR | `2a54a67d…` |
| P-35 implementation | **CLOSED / VALIDATED** | Exact candidate `0b1190fe…`; fresh pre-freeze and Governance CI passed |
| P1 Candidate Integrity | OPEN | Final experimental candidate/deployment binding still required |
| P2 Execution Contract / Runtime | HISTORICAL VERIFIED / RE-RUN REQUIRED | prior evidence bound to `92ff830b…` |
| P3 Artifact Contract | HISTORICAL WORKFLOW EVIDENCE / RE-RUN REQUIRED | fresh final-candidate artifact-contract closure required |
| P4 Security / Blinding | OPEN | historical attestation explicitly superseded; fresh current-cycle evidence required |
| P5 Provenance / Reproducibility | OPEN | current-cycle evidence required |
| P6 Durable Evidence Custody | OPEN / FAIL-CLOSED | durable archive/retrieval/hash event required |
| P6a Runtime/CORS | HISTORICAL VERIFIED / RE-RUN REQUIRED | prior evidence bound to `92ff830b…` |
| P7 Scientific Target | ADOPTED / FINAL BINDING OPEN | exact candidate/protocol/analysis/freeze binding required |
| P8 Analysis Lock | OPEN / FAIL-CLOSED | current-candidate prerequisites plus P9 required |
| P9 Independent Verification | HISTORICAL SCOPED PASS / RE-VERIFY REQUIRED | prior evidence bound to superseded candidate |
| Freeze | NOT ESTABLISHED | no frozen identity |
| Authorization | NOT GRANTED | separate governance transition |
| Empirical N | 0 | no authorized empirical execution |

## P-35 boundary

The validated implementation requires an explicit callable `PDMAL_PREMISE_CHECKER` in `module:attribute` form for DGAF execution. Missing, malformed, unloadable, or non-callable configuration is fail-closed. `ConsensusTask(condition="dgaf")` rejects omission. The resolved checker is propagated through `DGAF_TGLAdapter` into `TGLHooks`. The exact candidate `0b1190fe…` passed the real runner/task/adapter/TGL regression, including explicit checker invocation and the fail-closed `UNRECOVERED_FAILURE` / `ffcr_success=False` contract.

## Required closure sequence

1. Retain `0b1190fe…` as the validated P-35 implementation candidate and preserve its evidence boundary.
2. Select/reconcile the final experimental candidate and deployment identity.
3. Complete fresh P3 artifact-contract evidence.
4. Complete P4 operational blinding/custody evidence.
5. Complete P5 environment/toolchain/topology/RNG reproducibility evidence.
6. Complete P6 durable archive/retrieval/hash evidence.
7. Apply exact P7 candidate/protocol/analysis binding.
8. Close P8 from current-candidate evidence only.
9. Independently verify P9 against the final exact candidate.
10. Create and independently verify a new immutable freeze.
11. Obtain separate explicit pilot authorization.
12. Only then execute the blinded pilot.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**

## Anti-loop / evidence-transfer rule

Documentation commits, CI success, deployment readiness, historical evidence, and repeated audits do not authorize empirical execution or transfer evidence across candidates. Every closure claim must identify its exact candidate, run, artifact, deployment, and predicate scope.
