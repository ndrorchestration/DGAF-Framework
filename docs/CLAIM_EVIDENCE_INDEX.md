# Claim / Evidence Index

**Last reconciled:** 2026-08-16  
**Canonical source repository:** `ndrorchestration/DGAF-Framework`  
**Current main commit:** `ce1a4c959cc703590440b9e626bdaa008308f181`

This index maps high-impact claims to the evidence class actually supported by current retained evidence. It is intentionally conservative and claim-specific.

The repository runs a deterministic claim-language audit (`.github/workflows/claim-hygiene.yml`). The initial audit on 2026-08-16 retained 342 textual matches. The registry-reconciliation rerun completed successfully and retained a current artifact. Textual presence alone is not treated as proof of overclaiming; contextual review is required. Residual contextual candidates are documented in `docs/SEMANTIC_CLAIM_REVIEW_2026-08-16.md`.

The evidence-gate toolchain is now pinned and consumed by the Python CI workflow. Full matrix closure is **not yet established**: workflow run `31977296400` passed staging evidence, security scanning, and Python 3.10/3.11/3.12, while Python 3.9 failed during dependency installation because the pinned `pip==26.2.1` requires Python >=3.10. This is a runtime-policy/toolchain alignment issue, not a pytest failure.

| Claim | Current status | Evidence | Scope / limitations | Falsifier or revision trigger |
|---|---|---|---|---|
| DGAF containment specification is executable and checks its configured invariants/state space without TLC error. | `VERIFIED` — bounded model checking | Governance CI `31976717328`; TLC artifact digest `sha256:c0b364f0564b181976a789e11a6477afe63bd44dabd258d3451231df7795d07e`. | Bounded state graph defined by current `DGAFContainment.tla/.cfg`; not an unbounded mathematical proof; not live-production evidence. TLC Tools v1.8.0 is pinned and hashed. | TLC failure/counterexample, changed specification/bounds, or broader claim than checked scope. |
| DGAF deterministic circuit-breaker sequence executes as designed in the repository-local harness. | `VERIFIED` | Python CI `31977296400`; staging evidence stage passed with the pinned toolchain. | Repository-local deterministic harness only; artifact records production execution as false. Not live staging. | Harness assertion failure, changed transition semantics, or contradictory live-stage observation. |
| DGAF Python test suite passes under the currently executed Python matrix. | `VERIFIED` for Python 3.10, 3.11, and 3.12; `PENDING` for full matrix | Python CI `31977296400`; 3.10, 3.11, and 3.12 jobs completed successfully; 3.9 failed at dependency resolution before tests. | Does not establish that Python 3.9 remains supported. Runtime support policy remains separately open in #51. | Successful 3.9 run after policy reconciliation, or explicit removal of 3.9 from supported matrix. |
| DGAF security scan completes successfully. | `VERIFIED` for configured scan | Python CI `31977296400`; pinned Bandit/Safety steps completed successfully. | Only the configured Bandit/Safety scope and dependency state at the evaluated commit. | New findings, dependency changes, scan-scope changes, or materially different tool interpretation. |
| P-42 recovery/conductor behavior matches the repository's deterministic regression tests. | `VERIFIED` for tested behavior | Governance CI `31976717328`; P-42 test stage passed. | Unit/regression behavior only; does not establish improved real-world recovery. | Test regression, altered scoring/control logic, or contradictory independent evaluation. |
| `role_boundary_coherence` evaluator is reproducible on its canonical fixture corpus. | `VERIFIED` as evaluator/fixture behavior; `SYNTHETIC` evidence class | Governance CI `31976717328`; evaluation artifact digest `sha256:3828726b36bb5f887b085a29adb345524d66089b03e09103ff5cff31aca1f7b4`. | Fixture predictions are repository-authored evaluator inputs; a perfect fixture score is not DGAF/model performance. | Fixture corruption, scorer mismatch, generated model outputs differing from expected labels, or independent failure. |
| DGAF has live end-to-end Sentinel → `aoga-dashboard` runtime integration. | `PENDING` | No retained end-to-end transaction trace currently establishes this claim. | Contracts/deployment configuration are insufficient. | A dated end-to-end request/event trace at a specific commit and deployment can establish a narrower runtime claim. |
| DGAF breaker sequence has been exercised in a live controlled staging runtime. | `PENDING` | Only the deterministic local harness is currently retained. | Local harness verification is not live staging evidence. | Dated staging trace with source ref, environment, injected fault, containment, rollback, and recovery output. |
| DGAF governance controls are empirically effective on real workloads. | `PENDING` | No independent real-workload efficacy dataset is currently retained. | Synthetic tests, fixture evaluation, and unit tests do not establish efficacy. | Reproducible real-workload evaluation showing defined benefit under a specified protocol; negative/null results require claim downgrade. |
| DGAF formatting/type quality is clean. | `PENDING / QUALITY DEBT` | Latest quality logs remain non-blocking for formatting/type checks; full quality gate closure is not established. | Functional pytest is green in the passing matrix, but code-quality cleanliness is not established globally. | Black, isort, and mypy must pass under the documented supported runtime policy/configuration. |
| Evidence-gate toolchain is pinned and fully verified across the supported Python matrix. | `PENDING` | `requirements-ci.txt` is pinned and consumed by CI; run `31977296400` passed on 3.10/3.11/3.12 and failed on 3.9 because `pip==26.2.1` requires Python >=3.10. | Pinning is implemented, but the supported-runtime policy and pin set are not yet reconciled. | Full matrix success after closing #51 and rerunning #54. |
| DGAF is deployed to Vercel and has current live runtime verification. | `NOT ESTABLISHED` | Deployment workflow `31976717330` on main succeeded in the explicit configuration-unavailable state: deployment not attempted because required secrets are absent; runtime verification skipped. | This proves workflow-state separation, not deployment or runtime health. | A current deployment with retained deployment provenance plus independent health/regression/runtime evidence. |
| Repository-local epistemic evidence standard is canonical and current. | `VERIFIED` | `docs/EPISTEMIC_EVIDENCE_STANDARD.md`; commit `e1104fa2cc2dd5c14184d0e0d127430151e179e8`. | Repository-local governance standard, not external scientific authority. | Reconciliation required if evidence classes, claim vocabulary, or closure rules change. |
| Canonical claim/evidence index is present and current. | `VERIFIED` | `docs/CLAIM_EVIDENCE_INDEX.md`; reconciled with current CI state on 2026-08-16. | The index remains claim-specific and conservative; it does not certify the repository globally. | Any material source/evidence change requires index reconciliation. |

## Open repository quality backlog

- **#47** — formatting/type debt cleanup.
- **#51** — supported-runtime policy and Python matrix alignment.
- **#53** — repository-wide semantic audit for overclaiming verification language; deterministic scan implemented, residual contextual review remains.
- **#54** — evidence-gate toolchain pinning is implemented; full verification remains blocked by Python 3.9/runtime alignment.
- **#59** — semantic triage of residual high-impact claim-language findings.

## Closed epistemic/quality controls

- **#44** — bounded TLC/model-check result retained; formal scope controlled.
- **#46** — canonical epistemic evidence standard.
- **#48** — self-describing deterministic evidence artifact.
- **#49** — falsifier/revision conditions.
- **#50** — separation of correctness/evaluation/formal/security/runtime evidence classes.
- **#52** — current-state provenance requirement.
- **#55** — canonical claim/evidence index.
- **#56** — explicit formal-model scope control.
- **#57** — explicit deployment-unavailable vs deployment/runtime state separation.
- **#58** — registry claim reconciliation completed and re-audited.

## Current evidence hierarchy

1. Current main-branch execution evidence outranks historical runs for present-state claims.
2. Machine-readable retained artifacts outrank narrative status text.
3. Exact-claim evidence outranks adjacent or proxy evidence.
4. Independent evidence outranks self-authored assertions when validating efficacy.
5. Contradictory evidence remains visible and must trigger reconciliation or claim downgrade.

## Status vocabulary

Use the canonical ladder in [`EPISTEMIC_EVIDENCE_STANDARD.md`](EPISTEMIC_EVIDENCE_STANDARD.md):

`DEFINED → IMPLEMENTED → TESTED → VERIFIED → ATTESTED → VALIDATED → EMPIRICALLY SUPPORTED`

The status is claim-specific. A repository is never globally `VERIFIED` merely because one subsystem or workflow passes.
