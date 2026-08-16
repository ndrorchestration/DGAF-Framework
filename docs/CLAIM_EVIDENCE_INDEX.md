# Claim / Evidence Index

**Last reconciled:** 2026-08-16  
**Canonical source repository:** `ndrorchestration/DGAF-Framework`  
**Current main commit:** `233b2f9c40f8650ccbaed7a6dc61f1fc3419fe72`

This index maps high-impact claims to the evidence class actually supported by current retained evidence. It is intentionally conservative and claim-specific.

The repository also runs a deterministic claim-language audit (`.github/workflows/claim-hygiene.yml`). The initial audit on 2026-08-16 retained 342 textual matches across the configured vocabulary. Most matches are standards language, explicit caveats, historical records, or evidence-status labels; textual presence alone is not treated as an overclaim. Two current registry summaries were identified for focused review because they assert broader status than the retained evidence presently establishes. The detailed review is recorded in `docs/QUALITY_REGISTRY_CLAIM_REVIEW_2026-08-16.md`.

| Claim | Current status | Evidence | Scope / limitations | Falsifier or revision trigger |
|---|---|---|---|---|
| DGAF containment specification is executable and checks its configured invariants/state space without TLC error. | `VERIFIED` — bounded model checking | Governance CI `31976717328`; TLC artifact digest `sha256:c0b364f0564b181976a789e11a6477afe63bd44dabd258d3451231df7795d07e`. | Bounded state graph defined by current `DGAFContainment.tla/.cfg`; not an unbounded mathematical proof; not live-production evidence. TLC Tools v1.8.0 is pinned and hashed. | TLC failure/counterexample, changed specification/bounds, or broader claim than checked scope. |
| DGAF deterministic circuit-breaker sequence executes as designed in the repository-local harness. | `VERIFIED` | Python CI `31976717339`; staging artifact digest `sha256:7945f7c115d0b24c01be1426d4f12a9a8530345e2e002e3fa32d50bdc61f91e3`. | Repository-local deterministic harness only; artifact records production execution as false. Not live staging. | Harness assertion failure, changed transition semantics, or contradictory live-stage observation. |
| DGAF Python test suite passes under the currently executed Python matrix. | `VERIFIED` for tested behavior | Python CI `31976717339`; Python 3.9, 3.10, 3.11, and 3.12 jobs all completed successfully. | Verifies tested repository behavior in exercised CI environments. Does not establish efficacy. Runtime support policy remains separately open in #51. | Failing tests, unsupported runtime dependency, or behavior outside tested suite. |
| DGAF security scan completes successfully. | `VERIFIED` for configured scan | Python CI `31976717339`; security artifact digest `sha256:71aa1980a2f9eef732e7a3d9e2af83d4ca77e0ff801fac3bfea39da92fda97be`. | Only the configured Bandit/Safety scope and dependency state at the evaluated commit. | New findings, dependency changes, scan-scope changes, or materially different tool interpretation. |
| P-42 recovery/conductor behavior matches the repository's deterministic regression tests. | `VERIFIED` for tested behavior | Governance CI `31976717328`; P-42 test stage passed. | Unit/regression behavior only; does not establish improved real-world recovery. | Test regression, altered scoring/control logic, or contradictory independent evaluation. |
| `role_boundary_coherence` evaluator is reproducible on its canonical fixture corpus. | `VERIFIED` as evaluator/fixture behavior; `SYNTHETIC` evidence class | Governance CI `31976717328`; evaluation artifact digest `sha256:3828726b36bb5f887b085a29adb345524d66089b03e09103ff5cff31aca1f7b4`. | Fixture predictions are repository-authored evaluator inputs; a perfect fixture score is not DGAF/model performance. | Fixture corruption, scorer mismatch, generated model outputs differing from expected labels, or independent failure. |
| DGAF has live end-to-end Sentinel → `aoga-dashboard` runtime integration. | `PENDING` | No retained end-to-end transaction trace currently establishes this claim. | Contracts/deployment configuration are insufficient. | A dated end-to-end request/event trace at a specific commit and deployment can establish a narrower runtime claim. |
| DGAF breaker sequence has been exercised in a live controlled staging runtime. | `PENDING` | Only the deterministic local harness is currently retained. | Local harness verification is not live staging evidence. | Dated staging trace with source ref, environment, injected fault, containment, rollback, and recovery output. |
| DGAF governance controls are empirically effective on real workloads. | `PENDING` | No independent real-workload efficacy dataset is currently retained. | Synthetic tests, fixture evaluation, and unit tests do not establish efficacy. | Reproducible real-workload evaluation showing defined benefit under a specified protocol; negative/null results require claim downgrade. |
| DGAF formatting/type quality is clean. | `PENDING / QUALITY DEBT` | Latest Python 3.11 quality logs record Black on 20 files, isort on 15 files, and 11 mypy errors; these checks remain non-blocking. | Functional pytest is green, but code-quality cleanliness is not established. | Black, isort, and mypy must pass under the documented supported runtime policy/configuration. |
| DGAF is deployed to Vercel and has current live runtime verification. | `NOT ESTABLISHED` | Deployment workflow `31976717330` on current main succeeded in the explicit configuration-unavailable state: deployment not attempted because required secrets are absent; runtime verification skipped. | This proves workflow-state separation, not deployment or runtime health. | A current deployment with retained deployment provenance plus independent health/regression/runtime evidence. |
| Repository-local epistemic evidence standard is canonical and current. | `VERIFIED` | `docs/EPISTEMIC_EVIDENCE_STANDARD.md`; commit `e1104fa2cc2dd5c14184d0e0d127430151e179e8`. | Repository-local governance standard, not external scientific authority. | Reconciliation required if evidence classes, claim vocabulary, or closure rules change. |
| Canonical claim/evidence index is present and current. | `VERIFIED` | `docs/CLAIM_EVIDENCE_INDEX.md`; reconciliation commit `233b2f9c40f8650ccbaed7a6dc61f1fc3419fe72`. | The index remains claim-specific and conservative; it does not certify the repository globally. | Any material source/evidence change requires index reconciliation. |

## Open repository quality backlog

- **#47** — formatting/type debt cleanup.
- **#51** — supported-runtime policy and Python matrix alignment.
- **#53** — repository-wide audit for overclaiming verification language; deterministic scan implemented, focused registry review remains.
- **#54** — pin/report toolchain versions used by evidence gates; pin file added, workflow adoption still required.
- **#58** — registry summary claim cleanup identified by the claim-hygiene audit.

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
