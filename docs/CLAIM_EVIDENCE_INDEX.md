# Claim / Evidence Index

**Current reconciliation:** 2026-08-31  
**Canonical source repository:** `ndrorchestration/DGAF-Framework`  
**Current main commit:** `02e4c958e435f1faaa6fbf15909f9141ed2a6e39`

> **Reconciliation notice:** The claim/evidence rows below were last substantively reconciled on 2026-08-16 and therefore contain historical evidence references. They must not be read as a current-candidate status ledger. The current apparatus source is `02e4c958…` after PR #160 restored P-31/P-33. PR #162 is an unmerged draft provenance-binding change and is not part of `main`. Historical P2/P6a evidence remains scoped to its original source/deployment boundary and is not transferred.
>
> **Current experimental boundary:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0. P-31/P-33 are implemented on the current apparatus; P-27/P-29/P-30/P-32/DemiJoule remain incomplete or fail-closed pending contract/adapter resolution and candidate-scoped verification.

**Last substantive evidence reconciliation:** 2026-08-16  
**Canonical source repository:** `ndrorchestration/DGAF-Framework`

This index maps high-impact claims to the evidence class actually supported by retained evidence. It is intentionally conservative and claim-specific. Historical rows below preserve their original evidence scope; current-state assertions should be taken from `docs/CURRENT_STATE.md` and exact current GitHub evidence.

The repository runs a deterministic claim-language audit (`.github/workflows/claim-hygiene.yml`). The initial audit on 2026-08-16 retained 342 textual matches. The registry-reconciliation rerun completed successfully and retained a current artifact. Textual presence alone is not treated as proof of overclaiming; contextual review is required. Residual contextual candidates are documented in `docs/SEMANTIC_CLAIM_REVIEW_2026-08-16.md`.

The evidence-gate toolchain was pinned and consumed by the Python CI workflow at the historical reconciliation point. Full matrix closure was not established there: workflow run `31977296400` passed staging evidence, security scanning, and Python 3.10/3.11/3.12, while Python 3.9 failed during dependency installation because the pinned `pip==26.2.1` requires Python >=3.10. This historical evidence does not by itself describe the current candidate.

| Claim | Current status | Evidence | Scope / limitations | Falsifier or revision trigger |
|---|---|---|---|---|
| DGAF containment specification is executable and checks its configured invariants/state space without TLC error. | `VERIFIED` — bounded model checking | Governance CI `31976717328`; TLC artifact digest `sha256:c0b364f0564b181976a789e11a6477afe63bd44dabd258d3451231df7795d07e`. | Bounded state graph defined by current `DGAFContainment.tla/.cfg` at the historical evaluation point; not an unbounded mathematical proof; not live-production evidence. | TLC failure/counterexample, changed specification/bounds, or broader claim than checked scope. |
| DGAF deterministic circuit-breaker sequence executes as designed in the repository-local harness. | `VERIFIED` — historical scope | Python CI `31977296400`; staging evidence stage passed with the historical pinned toolchain. | Repository-local deterministic harness only; not live staging and not automatically transferred to the current apparatus. | Harness assertion failure, changed transition semantics, or contradictory live-stage observation. |
| DGAF Python test suite passes under the historically executed Python matrix. | `VERIFIED` for Python 3.10, 3.11, and 3.12; `PENDING` for full matrix | Python CI `31977296400`; 3.10, 3.11, and 3.12 jobs completed successfully; 3.9 failed at dependency resolution before tests. | Historical evidence; does not establish current-candidate runtime support. | Successful 3.9 run after policy reconciliation, explicit removal of 3.9 from supported matrix, or current-candidate failure. |
| DGAF security scan completes successfully. | `VERIFIED` — historical configured scan | Python CI `31977296400`; pinned Bandit/Safety steps completed successfully. | Historical configured scope and dependency state. | New findings, dependency changes, scan-scope changes, or materially different tool interpretation. |
| P-42 recovery/conductor behavior matches the repository's deterministic regression tests. | `VERIFIED` — historical tested behavior | Governance CI `31976717328`; P-42 test stage passed. | Unit/regression behavior only; does not establish improved real-world recovery or current-candidate behavior. | Test regression, altered scoring/control logic, or contradictory independent evaluation. |
| `role_boundary_coherence` evaluator is reproducible on its canonical fixture corpus. | `VERIFIED` as evaluator/fixture behavior; `SYNTHETIC` evidence class | Governance CI `31976717328`; evaluation artifact digest `sha256:3828726b36bb5f887b085a29adb345524d66089b03e09103ff5cff31aca1f7b4`. | Fixture predictions are repository-authored evaluator inputs; a perfect fixture score is not DGAF/model performance. | Fixture corruption, scorer mismatch, generated model outputs differing from expected labels, or independent failure. |
| DGAF has live end-to-end Sentinel → `aoga-dashboard` runtime integration. | `PENDING` | No retained end-to-end transaction trace currently establishes this claim. | Contracts/deployment configuration are insufficient. | A dated end-to-end request/event trace at a specific commit and deployment can establish a narrower runtime claim. |
| DGAF breaker sequence has been exercised in a live controlled staging runtime. | `PENDING` | Only the deterministic local harness is retained in the historical index. | Local harness verification is not live staging evidence. | Dated staging trace with source ref, environment, injected fault, containment, rollback, and recovery output. |
| DGAF governance controls are empirically effective on real workloads. | `PENDING` | No independent real-workload efficacy dataset is currently retained. | Synthetic tests, fixture evaluation, and unit tests do not establish efficacy. | Reproducible real-workload evaluation showing defined benefit under a specified protocol; negative/null results require claim downgrade. |
| DGAF formatting/type quality is clean. | `PENDING / QUALITY DEBT` | Historical quality logs remain non-blocking for formatting/type checks; full quality gate closure is not established. | Functional pytest success does not establish global formatting/type cleanliness. | Black, isort, and mypy must pass under the documented supported runtime policy/configuration. |
| Evidence-gate toolchain is pinned and fully verified across the supported Python matrix. | `IMPLEMENTED / PENDING VERIFICATION` — historical index | `requirements-ci.txt` and run `31977296400`. | Pinning was implemented, but the supported-runtime policy and pin set were not reconciled at the historical checkpoint. | Full matrix success after runtime-policy reconciliation and current-candidate rerun. |
| DGAF is deployed to Vercel and has current live runtime verification. | `NOT ESTABLISHED` | Historical deployment workflow `31976717330` explicitly separated configuration-unavailable state from runtime verification. | A later Vercel deployment or preview does not itself establish live-regression verification. | Current deployment with retained deployment provenance plus independent health/regression/runtime evidence. |
| Repository-local epistemic evidence standard is canonical and current. | `VERIFIED` — standard scope | `docs/EPISTEMIC_EVIDENCE_STANDARD.md`; commit `e1104fa2cc2dd5c14184d0e0d127430151e179e8`. | Repository-local governance standard, not external scientific authority. | Reconciliation required if evidence classes, claim vocabulary, or closure rules change. |
| Canonical claim/evidence index is present and current. | `RECONCILED 2026-08-31; substantive evidence rows remain historical` | This document. | Current lineage metadata is reconciled; individual evidence rows retain their historical scope until re-verified. | Any material source/evidence change requires index reconciliation. |

## Current apparatus additions requiring candidate-scoped evidence

- **P-31:** restored by PR #160 on `02e4c958…`; implementation and parity tests are present. This is engineering completion, not experimental verification.
- **P-33:** restored by PR #160 on `02e4c958…`; implementation and parity tests are present. This is engineering completion, not experimental verification.
- **PR #162:** draft provenance-binding work based on `02e4c958…`; not merged. Its Vercel Preview Comments success is not equivalent to the skipped Live Regression (Vercel) gate.
- **P-27:** contract-qualified restoration remains pending.
- **P-29:** normative contract and halt-enforcement semantics remain unresolved.
- **P-30:** acceptance-schema contradiction remains unresolved.
- **P-32:** historical restoration remains pending implementation on the current candidate.
- **DemiJoule:** constitutive contract remains unresolved between the efficiency-advisory specification and implemented six-axis semantic-safety behavior.

## Open repository quality backlog

- **#47** — formatting/type debt cleanup.
- **#51** — supported-runtime policy and Python matrix alignment.
- **#53** — repository-wide semantic audit for overclaiming verification language; deterministic scan implemented, residual contextual review remains.
- **#54** — evidence-gate toolchain pinning is implemented; full verification remains blocked by Python/runtime alignment.
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
