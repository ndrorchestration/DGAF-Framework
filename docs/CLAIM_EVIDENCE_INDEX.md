# Claim / Evidence Index

**Last reconciled:** 2026-08-16  
**Canonical source repository:** `ndrorchestration/DGAF-Framework`

This index maps high-impact claims to the evidence class actually supported by current retained evidence. It is intentionally conservative.

| Claim | Current status | Evidence | Scope / limitations | Falsifier or revision trigger |
|---|---|---|---|---|
| DGAF containment specification is executable and checks its configured invariants/state space without TLC error. | `VERIFIED` — bounded model checking | Main Governance CI run `31976439830`; TLC Tools v1.8.0; 12 states generated, 11 distinct, no error. | Bounded state graph defined by the current `DGAFContainment.tla/.cfg`; not an unbounded mathematical proof; not live-production evidence. | TLC failure, counterexample, changed specification, changed bounds, or a materially broader claim than the checked scope. |
| DGAF deterministic circuit-breaker sequence executes as designed in the repository-local harness. | `VERIFIED` | Main Python CI run `31976439883`; staging artifact SHA-256 `5ecbe157077953b597c979329e92316f1473a2b72d9b3ff2d620ee6dd11b00f8`. | Local deterministic harness only; no production/live-staging execution. | Harness assertion failure, changed transition semantics, or contradictory live-stage observation. |
| DGAF Python test suite passes under the currently executed Python matrix. | `VERIFIED` for tested behavior | Main Python CI run `31976439883`; test jobs for Python 3.9, 3.10, 3.11, 3.12 all completed successfully; pytest diagnostics retained. | Verifies tested repository behavior under that CI environment. Does not establish efficacy or external workload performance. | Any failing test, unsupported runtime dependency, or behavior outside the tested suite. |
| DGAF security scan completes successfully. | `VERIFIED` for configured scan | Main Python CI `31976439883`; security reports artifact retained, SHA-256 `aab87a189c348c90b4e772a72712f58d5bc90a16d36e2ff124b65165645d4a18`. | Only the configured Bandit/Safety scope and current dependency state. | New findings, dependency changes, scan-scope changes, or tool-version drift that changes interpretation. |
| P-42 recovery/conductor behavior matches the repository's deterministic tests. | `VERIFIED` for tested behavior | Governance CI `31976439830`; `78 passed, 3 skipped`. | Unit/regression behavior only; does not establish improved real-world recovery. | Test regression, altered scoring logic, or contradictory independent evaluation. |
| `role_boundary_coherence` evaluator is reproducible on its canonical fixture corpus. | `VERIFIED` as evaluator/fixture behavior; `SYNTHETIC` evidence class | Governance CI `31976439830`; artifact digest `26d0c7d54eeb186f008fccf9ecc15c984cf9325c9f266d72d85369fdbcf53d15`. | Fixture predictions are repository-authored evaluator inputs; score 1.0 is not DGAF/model performance. | Fixture corruption, scorer mismatch, generated model outputs differing from expected labels, or independent failure. |
| DGAF has live end-to-end Sentinel → `aoga-dashboard` runtime integration. | `PENDING` | No retained end-to-end transaction trace currently establishes this claim. | Contracts and deployment configuration are not sufficient. | A dated end-to-end trace can establish the claim; contradictory runtime observations would keep it pending. |
| DGAF breaker sequence has been exercised in a live controlled staging runtime. | `PENDING` | Only the deterministic local harness is currently retained. | Harness verification is not live staging evidence. | Dated staging trace with source ref, environment, injected fault, containment, rollback, and recovery output. |
| DGAF governance controls are empirically effective on real workloads. | `PENDING` | No independent real-workload efficacy dataset is currently retained. | Synthetic tests and unit tests do not establish efficacy. | Reproducible real-workload evaluation showing defined benefit under a specified protocol; negative or null results require claim downgrade. |
| DGAF formatting/type quality is clean. | `PENDING / QUALITY DEBT` | Historical and current CI logs show Black/isort/mypy findings, while those checks remain non-blocking. | Passing the overall workflow does not imply these checks passed. | Black, isort, and mypy must pass under documented supported runtimes/configuration. |
| Deployment of `DGAF-Framework` demonstrates production readiness. | `NOT ESTABLISHED` | Deployment workflow on main currently fails; core verification workflows succeed. | Deployment readiness and application verification are separate evidence classes. | A successful deployment plus independent runtime smoke/e2e evidence can establish a narrower deployment claim. |

## Current evidence hierarchy

1. Current main-branch execution evidence outranks historical runs for present-state claims.
2. Machine-readable retained artifacts outrank narrative status text.
3. Exact-claim evidence outranks adjacent or proxy evidence.
4. Independent evidence outranks self-authored assertions when validating efficacy.
5. Contradictory evidence remains visible and must trigger reconciliation or claim downgrade.

## Repository quality backlog

- **#47** — formatting/type debt cleanup.
- **#48** — self-describing evidence artifact schema.
- **#49** — falsifier/revision conditions.
- **#50** — explicit separation of CI correctness and evidence gates.
- **#51** — supported-runtime policy.
- **#52** — current-state provenance.
- **#53** — overclaiming language scan.
- **#54** — toolchain version pin/reporting.
- **#55** — canonical claim/evidence indexing.
- **#56** — formal-model scope control.

## Status vocabulary

Use the canonical ladder in [`EPISTEMIC_EVIDENCE_STANDARD.md`](EPISTEMIC_EVIDENCE_STANDARD.md):

`DEFINED → IMPLEMENTED → TESTED → VERIFIED → ATTESTED → VALIDATED → EMPIRICALLY SUPPORTED`

The status is claim-specific. A repository is never globally `VERIFIED` merely because one subsystem or workflow passes.
