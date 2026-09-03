---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-09-03
applies_to_ref: main
corrected_apparatus_source: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
active_p35_remediation_branch: remediation/p35-minimal-mainline-2026-09-02
active_p35_remediation_pr: 199
validated_p35_candidate: 0b1190fe91db6b963da0b31492d61fa1a34381e3
validated_p35_candidate_validation_run: 33697643625
current_control_plane_head: 86cb2052480a2d317e34d601522ac9c137591382
---
# DGAF-Framework / PDMAL — Current State

GitHub is authoritative for implementation and CI; governance decisions must be recorded through the project's governance process. Historical evidence remains scoped to the exact SHA/run/deployment/artifact that produced it.

> **Current boundary:** `main` remains the documentation/control-plane lineage. The corrected apparatus source is `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1` and remains the canonical provenance anchor.
>
> **Validated P-35 candidate:** PR #199 / branch `remediation/p35-minimal-mainline-2026-09-02`, exact candidate `0b1190fe91db6b963da0b31492d61fa1a34381e3`. Fresh exact-head PDMAL Pre-Freeze Runner Validation run `33697643625` and Governance CI run `33697643702` both passed. The current control-plane documentation may advance independently; this does not transfer candidate-bound evidence to later documentation commits.
>
> **Previous runtime/completion candidates:** `92ff830b…` and `a43219b…` remain historical evidence boundaries for this cycle. Their evidence is not transferred to PR #199.
>
> **Current experimental boundary:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.

## Identity roles

- `2a54a67d…` — corrected seven-gate apparatus provenance anchor.
- `275756fd…` — current `main` control-plane base from which PR #199 was created.
- `0b1190fe…` — exact candidate on which P-35 was freshly validated; implementation candidate for this closure stage.
- `86cb2052…` — current documentation/control-plane head; not a replacement experimental candidate.
- `92ff830b…` — superseded mainline runtime candidate; P2/P6a evidence remains bound to its exact tree/deployment.
- `a43219b…` — superseded controlled completion candidate; PDMAL/P9 evidence remains bound to its exact tree.
- `dpl_Br3muEJGN8eMNCWSpzZqSag6Ptrc` — historical deployment identity for `92ff830b…` P2/P6a evidence.
- `dpl_6f3AAA6MMqtHQP26qZ9efHmn4r17` — historical preview deployment for `a43219b…`; not a deployment identity for PR #199.

## Authoritative experimental state

| Boundary | Status | Meaning |
|---|---|---|
| Corrected apparatus source | CANONICAL PROVENANCE ANCHOR | `2a54a67d…` |
| P-35 implementation | **VALIDATED** | Exact candidate `0b1190fe…`; fresh exact-head pre-freeze and Governance CI passed |
| P-35 candidate | VALIDATED / NOT FROZEN | `0b1190fe…`; PR #199 |
| P1 | OPEN | Final candidate/provenance/deployment binding still required before freeze |
| P2 | HISTORICAL VERIFIED / RE-RUN REQUIRED | prior evidence bound to `92ff830b…` |
| P3 | HISTORICAL WORKFLOW EVIDENCE / RE-RUN REQUIRED | current final-candidate artifact-contract evidence required |
| P4 | OPEN | current-cycle operational blinding/custody evidence required |
| P5 | OPEN | current-cycle reproducibility evidence required |
| P6 | OPEN / FAIL-CLOSED | current-cycle durable custody proof required |
| P6a | HISTORICAL VERIFIED / RE-RUN REQUIRED | prior evidence bound to `92ff830b…` |
| P7 | ADOPTED / FINAL BINDING OPEN | exact candidate/protocol/analysis/freeze binding required |
| P8 | OPEN / FAIL-CLOSED | current-candidate analysis/TGL prerequisites and P9 required |
| P9 | HISTORICAL SCOPED PASS / RE-VERIFY REQUIRED | prior pass bound to `a43219b…` |
| Freeze | NOT ESTABLISHED | no frozen identity |
| Authorization | NOT GRANTED | separate governance transition |
| Empirical N | 0 | no authorized empirical execution |

## P-35 integration boundary

The validated candidate requires an explicit callable `PDMAL_PREMISE_CHECKER` in `module:attribute` form for DGAF execution. Missing, malformed, unloadable, and non-callable configuration is fail-closed. `ConsensusTask(condition="dgaf")` rejects omission. The resolved checker is propagated through `DGAF_TGLAdapter` into `TGLHooks`.

Fresh candidate-bound validation established the regression contract on exact candidate `0b1190fe…`: the explicit checker is exercised through the runner/task/adapter/TGL path, and rejection remains fail-closed with `UNRECOVERED_FAILURE` and `ffcr_success=False`. P-35 is CLOSED / VALIDATED for this exact candidate.

## Required closure sequence

1. Retain `0b1190fe…` as the validated P-35 implementation candidate; do not substitute a later documentation-only head as experimental evidence.
2. Select/reconcile the final experimental candidate identity and any required deployment identity.
3. Complete fresh P3 artifact-contract evidence.
4. Complete P4 operational blinding/custody evidence.
5. Complete P5 environment/topology/RNG reproducibility evidence.
6. Complete P6 durable archive/retrieval/hash evidence.
7. Apply exact candidate/protocol/analysis binding for P7.
8. Close P8 from current-candidate evidence only.
9. Independently verify P9 against the final exact candidate.
10. Create and independently verify a new immutable freeze.
11. Obtain separate pilot authorization.
12. Only then execute the blinded pilot.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**

## Anti-loop / evidence-transfer rule

Documentation commits, CI success, deployment readiness, historical evidence, and repeated audits do not authorize empirical execution or transfer evidence across candidates. Every closure claim must identify its exact candidate, run, artifact, deployment, and predicate scope.
