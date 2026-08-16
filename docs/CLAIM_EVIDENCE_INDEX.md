# Claim / Evidence Index

**Last reconciled:** 2026-08-16  
**Canonical source repository:** `ndrorchestration/DGAF-Framework`  
**Current main commit:** `082393da06a1860f000a6d6f204209a18a560ca5`

This index maps high-impact claims to the evidence class actually supported by current retained evidence. It is intentionally conservative and claim-specific.

| Claim | Current status | Evidence | Scope / limitations | Falsifier or revision trigger |
|---|---|---|---|---|
| DGAF containment specification is executable and checks its configured invariants/state space without TLC error. | `VERIFIED` — bounded model checking | Governance CI `31976717328`; TLC artifact digest `sha256:c0b364f0564b181976a789e11a6477afe63bd44dabd258d3451231df7795d07e`. | Bounded state graph defined by current `DGAFContainment.tla/.cfg`; not an unbounded mathematical proof; not live-production evidence. TLC Tools v1.8.0 is pinned and hashed. | TLC failure/counterexample, changed specification/bounds, or broader claim than checked scope. |
| DGAF deterministic circuit-breaker sequence executes as designed in the repository-local harness. | `VERIFIED` | Python CI `31976717339`; staging artifact digest `sha256:7945f7c115d0b24c01be1426d4f12a9a8530345e2e002e3fa32d50bdc61f91e3`. | Repository-local deterministic harness only; artifact records production execution as false. Not live staging. | Harness assertion failure, changed transition semantics, or contradictory live-stage observation. |
| DGAF Python test suite passes under the currently executed Python matrix. | `VERIFIED` for tested behavior | Python CI `31976717339`; Python 3.9/3.10/3.11/3.12 jobs all completed successfully. | Verifies tested behavior in exercised CI environments. Does not establish efficacy. The runtime document calls these CI-validated runtimes, not blanket compatibility guarantees. | Failing tests, unsupported runtime dependency, or behavior outside tested suite. |
| DGAF security scan completes successfully. | `VERIFIED` for configured scan | Python CI `31976717339`; security artifact digest `sha256:71aa1980a2f9eef732e7a3d9e2af83d4ca77e0ff801fac3bfea39da92fda97be`. | Only configured Bandit/Safety scope and dependency state at evaluated commit. | New findings, dependency changes, scope changes, or materially different tool interpretation. |
| P-42 recovery/conductor behavior matches deterministic regression tests. | `VERIFIED` for tested behavior | Governance CI `31976717328`; P-42 test stage passed. | Unit/regression behavior only; not real-world recovery efficacy. | Test regression, altered control logic, or contradictory independent evaluation. |
| `role_boundary_coherence` evaluator is reproducible on its canonical fixture corpus. | `VERIFIED` as evaluator/fixture behavior; `SYNTHETIC` | Governance CI `31976717328`; evaluation artifact digest `sha256:3828726b36bb5f887b085a29adb345524d66089b03e09103ff5cff31aca1f7b4`. | Fixture predictions are repository-authored evaluator inputs; a perfect fixture score is not DGAF/model performance. | Fixture corruption, scorer mismatch, generated model outputs differing from expected labels, or independent failure. |
| Deterministic staging evidence artifact is self-describing and provenance-backed. | `VERIFIED` | Python CI `31976717339`; staging artifact includes source commit, workflow run, Python/pytest versions, command, scope, production flag, and limitations. | Provenance strengthens traceability but does not convert local harness evidence into live staging evidence. | Artifact schema regression or missing provenance fields. |
| Python CI toolchain versions are reproducibly reported. | `VERIFIED` for reporting | Commit `082393da...` adds per-runtime toolchain manifests to Python test artifacts. | Tool versions are reported, not yet pinned/locked. | Missing manifest or materially incomplete version report. |
| DGAF has a release-level supported Python policy. | `PENDING` | `docs/SUPPORTED_RUNTIME_POLICY.md` defines the current CI-validated matrix but explicitly leaves the release-support decision open. | Requires explicit maintainer decisions on officially supported versions, informational versions, dependency bounds, deprecation, and release gates. | Approved support policy recorded and CI aligned to it. |
| DGAF has live end-to-end Sentinel → `aoga-dashboard` runtime integration. | `PENDING` | No retained end-to-end transaction trace currently establishes this claim. | Contracts/deployment configuration are insufficient. | Dated end-to-end request/event trace at a specific commit and deployment. |
| DGAF breaker sequence has been exercised in a live controlled staging runtime. | `PENDING` | Only deterministic local harness evidence is retained. | Local harness verification is not live staging evidence. | Dated staging trace with source ref, environment, injected fault, containment, rollback, and recovery output. |
| DGAF governance controls are empirically effective on real workloads. | `PENDING` | No independent real-workload efficacy dataset is retained. | Synthetic tests, fixture evaluation, and unit tests do not establish efficacy. | Reproducible real-workload evaluation under a defined protocol; negative/null results require claim downgrade. |
| DGAF formatting/type quality is clean. | `PENDING / QUALITY DEBT` | Latest Python 3.11 quality logs recorded Black on 20 files, isort on 15 files, and 11 mypy errors; checks remain non-blocking. | Functional pytest is green, but code-quality cleanliness is not established. | Black/isort/mypy pass as blocking gates under documented runtime/toolchain policy. |
| DGAF is deployed to Vercel and has current live runtime verification. | `NOT ESTABLISHED` | Deployment workflow `31976717330` on current main succeeded in the **configuration-unavailable** state; deploy and runtime jobs were skipped because required Vercel secrets are unavailable. | Proves workflow-state separation, not deployment or runtime health. | Current deployment with retained provenance plus independent health/regression/runtime evidence. |
| Repository-local epistemic evidence standard is canonical. | `VERIFIED` | `docs/EPISTEMIC_EVIDENCE_STANDARD.md`; repository-local standard. | Internal governance standard, not external scientific authority. | Reconcile if evidence classes, claim vocabulary, or closure rules change. |
| Canonical claim/evidence index is current. | `VERIFIED` | `docs/CLAIM_EVIDENCE_INDEX.md`; this reconciliation commit. | Claim-specific; does not globally certify the repository. | Any material source/evidence change requires index reconciliation. |

## Open repository quality backlog

- **#47** — formatting/type debt cleanup.
- **#51** — release-level supported-runtime policy and matrix alignment.
- **#53** — repository-wide overclaiming-language audit; current file-search index is insufficient for closure.
- **#54** — deterministic toolchain pinning/constraining; reporting is implemented, pinning remains open.

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
