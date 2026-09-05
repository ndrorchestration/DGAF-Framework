# Claim / Evidence Index

**Current reconciliation:** 2026-09-05  
**Canonical source repository:** `ndrorchestration/DGAF-Framework`  
**Current main control-plane lineage:** resolve `main` directly in GitHub; the literal post-reconciliation tip is intentionally not treated as the runtime candidate.  
**Corrected apparatus source:** `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`  
**Current designated runtime candidate:** `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8` with exact tree `586c00d6dedb589e52108279f9759be3c4f927e1`.  
**Candidate deployment identity:** `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA`.

> **Reconciliation notice:** Historical claim/evidence rows preserve their original evidence scope. They must not be read as a current-candidate status ledger. Current gate authority is `docs/experiment/PDMAL_CURRENT_CONTROL_STATE.md` plus the exact retained evidence named there.
>
> **Current experimental boundary:** **PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.** P1, P2, P3, P5, P6, and P6a are closed within bounded engineering/governance evidence contracts. P4 real human custody/access separation remains operationally open. P7 final binding remains open; P8 remains fail-closed; final P9 is not executed; no immutable freeze or pilot authorization exists.

This index maps high-impact claims to the evidence class actually supported. It is intentionally conservative and claim-specific. A repository or subsystem is never globally “verified” merely because one workflow succeeds.

The repository runs deterministic claim-language checks. Textual presence alone is not proof; evidence identity, scope, and claim class determine admissibility.

| Claim | Current status | Evidence | Scope / limitations | Falsifier or revision trigger |
|---|---|---|---|---|
| DGAF containment specification is executable and checks its configured bounded invariants/state space without TLC error. | `VERIFIED` — bounded model-check scope | Governance CI / retained TLC evidence under the applicable exact runs. | Bounded state graph only; not an unbounded theorem and not efficacy evidence. | TLC counterexample, changed spec/config/bounds, or broader claim than checked scope. |
| DGAF deterministic circuit-breaker sequence executes as designed in the repository-local harness. | `VERIFIED` — deterministic harness scope | Python/staging-evidence harness under exact runs. | Repository-local control-flow evidence; not live-staging efficacy. | Harness assertion failure or contradictory independently retained execution. |
| Repository blocking pytest suite passes on the PR #269 supported Python matrix. | `VERIFIED` — exact PR-head test scope | Python Tests & Quality Checks `33957199893`; Python 3.10/3.11/3.12 jobs successful; Python 3.12 190 passed / 4 skipped. | Does not imply advisory Black/isort/mypy diagnostics are clean. | Blocking pytest regression or supported-runtime policy change. |
| DGAF formatting/import/type quality is clean on the current lineage. | `OPEN / QUALITY DEBT` | Issue #270; diagnostics from run `33957199893`. | Black/isort/mypy are currently `continue-on-error`; green workflow does not prove clean quality baseline. | Clean exact-run diagnostics plus blocking-gate hardening. |
| P-42 recovery/conductor behavior matches the repository's deterministic regression tests. | `VERIFIED` — tested behavior | Governance CI P-42 stage under applicable exact runs. | Unit/regression behavior only; not AHG efficacy. | Test regression or altered control/scoring logic. |
| `role_boundary_coherence` evaluator reproduces its canonical repository-authored fixture labels. | `VERIFIED` as evaluator/fixture behavior; `SYNTHETIC` | Historical retained evaluation artifact. | Synthetic fixture evidence; not DGAF/model performance. | Fixture/scorer mismatch or independent failure. |
| `audit_hallucination_rate` cannot emit a synthetic/random passing performance result without required evidence. | `VERIFIED` — evaluator-mechanism scope | PR #269; seven collected Task-4 regressions; run `33957199893`. | Verifies fail-closed deterministic comparison mechanics only. No model-performance result exists. | Regression allowing missing/malformed evidence to produce a performance result or answer leakage. |
| DGAF has live end-to-end Sentinel → AOGA runtime integration. | `NOT IMPLEMENTED / NOT EVIDENCED` | PR #268 evidence-boundary record. | AOGA runtime exists separately; Sentinel operator supports GitHub/configurable orchestrator target, but no direct Sentinel→AOGA path was found. | Explicit implementation plus exact retained end-to-end runtime trace. |
| DGAF breaker sequence has been exercised in a live controlled staging runtime. | `PENDING` | No current retained controlled staging transaction proving this claim. | Local harness/runtime predicates are not a staging safety-efficacy experiment. | Dated staging trace with source, environment, injected fault, containment, rollback, and recovery. |
| DGAF governance controls are empirically effective on real workloads. | `PENDING` | No independent real-workload efficacy dataset retained. | Engineering validation, synthetic evidence, and deployment health do not establish efficacy. | Reproducible authorized real-workload evaluation under the defined protocol. |
| P1 candidate identity/integrity is closed for the designated PDMAL candidate. | `CLOSED / VERIFIED` | Canonical PDMAL control state and exact candidate/deployment/provenance evidence. | Candidate-integrity engineering scope only. | Candidate rotation, identity mismatch, or contradictory retained evidence. |
| P2 runtime predicates are satisfied for the designated candidate deployment. | `CLOSED / VERIFIED` | run `33730195621`; artifact `9883521704`; candidate `7c1cc4bb…`; deployment `dpl_8Msuf…`. | Five authenticated runtime predicates only; not general health/efficacy. | Candidate/deployment change or contradictory current runtime evidence. |
| P3 artifact contract is satisfied for the designated candidate. | `CLOSED / VERIFIED` | run `33939955138`; exact-candidate structural/matrix evidence. | Artifact-contract/structural scope only. | Contract/schema mismatch or candidate rotation. |
| P4 real custody/access separation is established. | `OPEN / NOT EXECUTED` | Procedure and synthetic controls exist; no real distinct-human custody execution evidence. | Cannot be closed by documentation or CI alone. | Completed real custody commitments/attestations plus applicable independent review. |
| P5 provenance/reproducibility is closed for the designated candidate. | `CLOSED / VERIFIED` | Canonical PDMAL control state; run `33939955138`; bound analysis/config/runner/schema identities and deterministic environment/RNG/topology evidence. | Provenance/reproducibility only; not efficacy. | Identity/config/environment mismatch or reproducibility failure. |
| P6 durable evidence custody is closed within the defined archive/retrieval/hash contract. | `CLOSED / VERIFIED` | Current P6 attestation and independent archive→retrieval→SHA-256 equality evidence. | Byte-custody/integrity scope; does not imply human P4 custody or efficacy. | Retrieval/hash mismatch or loss of required retained object. |
| P6a CORS predicates are satisfied for the candidate deployment. | `CLOSED / VERIFIED` | run `33728695806`; artifact `9882965299`; candidate `7c1cc4bb…`; deployment `dpl_8Msuf…`. | Four authenticated CORS cases only. | Candidate/deployment change or contradictory CORS result. |
| P7 is finally bound. | `OPEN` | Scientific target adopted; final exact binding not complete. | Blocked by remaining prerequisite/freeze identity chain. | Completed exact binding under canonical governance. |
| P8 immutable analysis/freeze state exists. | `OPEN / FAIL-CLOSED` | Preparation/tooling exists; immutable freeze not established/verified. | No final frozen pilot identity. | Valid freeze object plus independent verification. |
| Final P9 independent verification has executed. | `NOT EXECUTED / OPEN` | Verifier tooling exists; final frozen-chain execution absent. | Tooling presence is not execution. | Successful final independent frozen-chain verification. |
| Repository-local epistemic evidence standard is canonical. | `VERIFIED` — repository-governance scope | `docs/EPISTEMIC_EVIDENCE_STANDARD.md`. | Repository-local standard, not external scientific authority. | Formal governance revision. |

## Designated candidate runtime binding

- Corrected apparatus source: `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`
- Designated runtime candidate: `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`
- Runtime candidate tree: `586c00d6dedb589e52108279f9759be3c4f927e1`
- Production deployment: `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA`
- P2 artifact: `9883521704`
- P6a artifact: `9882965299`
- Later documentation/evaluator/control-plane commits do not replace this scientific runtime identity without an explicit provenance transition.

## Current quality and evaluation backlog

- **#32** — Task-4 fixture/output corpus and remaining model-specific/real-workload evaluation evidence.
- **#36** — residual STRUCT-QA runtime/staging/portfolio claims; Sentinel→AOGA is currently bounded as not implemented/evidenced.
- **#64** — evaluation-integrity/adversarial measurement track.
- **#122** — P-38 historical source recovery; blocked on authoritative source.
- **#144** — branch/process reconciliation and safe-ref pruning capability gap.
- **#232** — canonical PDMAL P4/P7/P8/P9 closure chain.
- **#270** — current-lineage Black/isort/mypy cleanup and eventual quality-gate hardening.

## Current evidence hierarchy

1. Exact current or designated-candidate execution evidence outranks stale narrative state for present claims.
2. Machine-readable retained artifacts outrank summary prose when they conflict.
3. Exact-claim evidence outranks adjacent or proxy evidence.
4. Independent evidence outranks self-authored assertions for efficacy claims.
5. Contradictory evidence remains visible and triggers reconciliation or downgrade.
6. Historical exact-tree evidence remains valid within its original scope; later state changes do not rewrite history.

## Status vocabulary

Use the canonical ladder in [`EPISTEMIC_EVIDENCE_STANDARD.md`](EPISTEMIC_EVIDENCE_STANDARD.md):

`DEFINED → IMPLEMENTED → TESTED → VERIFIED → ATTESTED → VALIDATED → EMPIRICALLY SUPPORTED`

The status is claim-specific. A repository is never globally `VERIFIED` merely because one subsystem, workflow, deployment, or synthetic evaluator passes.
