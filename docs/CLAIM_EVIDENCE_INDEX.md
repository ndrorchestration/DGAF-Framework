# Claim / Evidence Index

**Current reconciliation:** 2026-09-06  
**Canonical source repository:** `ndrorchestration/DGAF-Framework`  
**v0.7.6 apparatus-introduction boundary:** `972edd41f16c69c6912af08c7d6c3aa627fdd8a9` (legacy lineage boundary; not current `main`)
**Corrected apparatus source:** `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`  
**Consolidated control-state anchor:** `89be386b136aeb5f1fc5ca39d4aac4b3781a9f58`  
**Historical runtime-evidence candidate:** `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8` with exact tree `586c00d6dedb589e52108279f9759be3c4f927e1` and deployment `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA`.  
**Final v0.7.6 candidate:** `NOT DESIGNATED` — Issue #309.

> **Reconciliation notice:** Historical claim/evidence rows preserve their original evidence scope. They must not be read as automatic final-candidate closure. Current gate authority is `docs/experiment/PDMAL_CURRENT_CONTROL_STATE.md` plus the exact retained evidence named there.
>
> **Current experimental boundary:** **PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.** Historical P1, P2, P3, P5, P6, and P6a evidence remains exact-scope provenance for `7c1cc4bb…`. PR #326 integrated Mode-T engineering mechanisms, but real H/I/T custody/access separation remains operationally open pending independent/external acceptance. P7 final binding remains open; P8 remains fail-closed; final P9 is not executed; no immutable freeze or pilot authorization exists.

This index maps high-impact claims to the evidence class actually supported. It is intentionally conservative and claim-specific. A repository or subsystem is never globally “verified” merely because one workflow succeeds.

The repository runs deterministic claim-language checks. Textual presence alone is not proof; evidence identity, scope, and claim class determine admissibility.

| Claim | Current status | Evidence | Scope / limitations | Falsifier or revision trigger |
|---|---|---|---|---|
| DGAF containment specification is executable and checks its configured bounded invariants/state space without TLC error. | `VERIFIED` — bounded model-check scope | Governance CI / retained TLC evidence under the applicable exact runs. | Bounded state graph only; not an unbounded theorem and not efficacy evidence. | TLC counterexample, changed spec/config/bounds, or broader claim than checked scope. |
| DGAF deterministic circuit-breaker sequence executes as designed in the repository-local harness. | `VERIFIED` — deterministic harness scope | Python/staging-evidence harness under exact runs. | Repository-local control-flow evidence; not live-staging efficacy. | Harness assertion failure or contradictory independently retained execution. |
| Repository blocking pytest suite passes on the PR #269 supported Python matrix. | `VERIFIED` — exact PR-head test scope | Python Tests & Quality Checks `33957199893`; Python 3.10/3.11/3.12 jobs successful; Python 3.12 190 passed / 4 skipped. | Historical exact PR-head scope; later quality remediation is tracked separately. | Blocking pytest regression or supported-runtime policy change. |
| DGAF formatting/import/type quality is clean on the remediated current lineage. | `CLOSED / VERIFIED` | Issue #270; PR #276 exact-head and mainline Python quality evidence. | Workflow behavior is fail-closed when executed; repository-required merge enforcement is a separate #277 control. | Quality regression or removal/weakening of fail-closed checks. |
| P-42 recovery/conductor behavior matches the repository's deterministic regression tests. | `VERIFIED` — tested behavior | Governance CI P-42 stage under applicable exact runs. | Unit/regression behavior only; not AHG efficacy. | Test regression or altered control/scoring logic. |
| `role_boundary_coherence` evaluator reproduces its canonical repository-authored fixture labels. | `VERIFIED` as evaluator/fixture behavior; `SYNTHETIC` | Historical retained evaluation artifact. | Synthetic fixture evidence; not DGAF/model performance. | Fixture/scorer mismatch or independent failure. |
| `audit_hallucination_rate` cannot emit a synthetic/random passing performance result without required evidence. | `VERIFIED` — evaluator-mechanism scope | PR #269; seven collected Task-4 regressions; run `33957199893`. | Verifies fail-closed deterministic comparison mechanics only. No model-performance result exists. | Regression allowing missing/malformed evidence to produce a performance result or answer leakage. |
| DGAF has live end-to-end Sentinel → AOGA runtime integration. | `NOT IMPLEMENTED / NOT EVIDENCED` | PR #268 evidence-boundary record. | AOGA runtime exists separately; Sentinel operator supports GitHub/configurable orchestrator target, but no direct Sentinel→AOGA path was found. | Explicit implementation plus exact retained end-to-end runtime trace. |
| DGAF breaker sequence has been exercised in a live controlled staging runtime. | `PENDING` | No current retained controlled staging transaction proving this claim. | Local harness/runtime predicates are not a staging safety-efficacy experiment. | Dated staging trace with source, environment, injected fault, containment, rollback, and recovery. |
| DGAF governance controls are empirically effective on real workloads. | `PENDING` | No independent real-workload efficacy dataset retained. | Engineering validation, synthetic evidence, and deployment health do not establish efficacy. | Reproducible authorized real-workload evaluation under the defined protocol. |
| Historical P1 candidate identity/integrity is closed for `7c1cc4bb…`. | `CLOSED / VERIFIED AT HISTORICAL SCOPE` | Canonical PDMAL control state and exact candidate/deployment/provenance evidence. | Candidate-integrity engineering scope only; does not designate or close the future v0.7.6 final candidate. | Contradictory retained evidence or invalidated provenance. |
| Historical P2 runtime predicates are satisfied for `7c1cc4bb…` / `dpl_8Msuf…`. | `CLOSED / VERIFIED AT HISTORICAL SCOPE` | run `33730195621`; artifact `9883521704`. | Five authenticated runtime predicates only; final-candidate transfer/re-run decision belongs to #309. | Contradictory exact-scope evidence. |
| Historical P3 artifact contract is satisfied for `7c1cc4bb…`. | `CLOSED / VERIFIED AT HISTORICAL SCOPE` | run `33939955138`; exact-candidate structural/matrix evidence. | Artifact-contract/structural scope only; final-candidate transfer/reverification belongs to #309. | Contract/schema mismatch or contradictory retained evidence. |
| P4 real custody/access separation is established. | `OPEN / FAIL-CLOSED` | PR #326 integrated Mode-T mechanism controls; no real H/I/T custody execution/admission evidence has been independently accepted. | Mechanism integration cannot close custody; #316/#320 and production trust/retention/admission evidence remain open. | Completed real custody commitments/attestations plus applicable independent review. |
| Historical P5 provenance/reproducibility is closed for `7c1cc4bb…`. | `CLOSED / VERIFIED AT HISTORICAL SCOPE` | Canonical PDMAL control state; run `33939955138`; bound analysis/config/runner/schema identities and deterministic environment/RNG/topology evidence. | Protocol 0.7.5 provenance/reproducibility only; does not silently become v0.7.6 final-candidate evidence. | Identity/config/environment mismatch or reproducibility failure. |
| Historical P6 durable evidence custody is closed within the defined archive/retrieval/hash contract. | `CLOSED / VERIFIED AT HISTORICAL SCOPE` | Current P6 attestation and independent archive→retrieval→SHA-256 equality evidence. | Byte-custody/integrity scope; final-candidate rebind decision belongs to #309. | Retrieval/hash mismatch or loss of required retained object. |
| Historical P6a CORS predicates are satisfied for `7c1cc4bb…` / `dpl_8Msuf…`. | `CLOSED / VERIFIED AT HISTORICAL SCOPE` | run `33728695806`; artifact `9882965299`. | Four authenticated CORS cases only; final-candidate transfer/re-run decision belongs to #309. | Contradictory exact-scope CORS evidence. |
| Final v0.7.6 candidate is designated. | `NOT DESIGNATED` | Issue #309. | `main`, PR heads, deployments, and documentation checkpoints do not become the candidate by recency. | Explicit immutable candidate designation under canonical governance. |
| P7 is finally bound. | `OPEN` | Scientific target adopted; final exact binding not complete. | Blocked by final candidate identity, actual P4-A custody evidence, and final freeze identity chain. | Completed exact binding under canonical governance. |
| P8 immutable analysis/freeze state exists. | `OPEN / FAIL-CLOSED` | Preparation/tooling exists; immutable freeze not established/verified. | No final frozen pilot identity. | Valid freeze object plus independent verification. |
| Final P9 independent verification has executed. | `NOT EXECUTED / OPEN` | Verifier tooling exists; final frozen-chain execution absent. | Tooling presence is not execution. | Successful final independent frozen-chain verification. |
| Repository-local epistemic evidence standard is canonical. | `VERIFIED` — repository-governance scope | `docs/EPISTEMIC_EVIDENCE_STANDARD.md`. | Repository-local standard, not external scientific authority. | Formal governance revision. |

## Historical runtime-evidence binding

- Corrected apparatus source: `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`
- Consolidated control-state anchor: `89be386b136aeb5f1fc5ca39d4aac4b3781a9f58`
- Historical runtime-evidence candidate: `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`
- Runtime candidate tree: `586c00d6dedb589e52108279f9759be3c4f927e1`
- Historical production deployment: `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA`
- P2 artifact: `9883521704`
- P6a artifact: `9882965299`
- Final v0.7.6 candidate: **NOT DESIGNATED**; Issue #309 governs reconstruction and evidence classification/regeneration.

## Current quality and evaluation backlog

- **#32** — Task-4 fixture/output corpus and remaining model-specific/real-workload evaluation evidence.
- **#36** — residual STRUCT-QA runtime/staging/portfolio claims; Sentinel→AOGA is currently bounded as not implemented/evidenced.
- **#64** — evaluation-integrity/adversarial measurement track.
- **#122** — P-38 historical source recovery; blocked on authoritative source.
- **#144** — branch/process reconciliation and safe-ref pruning capability gap.
- **#232** — canonical PDMAL P4/P7/P8/P9 closure chain.
- **#277** — repository-level merge enforcement for intended quality/security checks.
- **#309** — v0.7.6 final-candidate reconstruction and identity-dependent evidence regeneration.
- **#316** — independently retained admission-policy/R-A-C binding before production key generation.
- **#320** — independent security review of the Mode-T Google OIDC verifier.

## Current evidence hierarchy

1. Exact current or historical-candidate execution evidence outranks stale narrative state for claims within that exact identity/scope.
2. Machine-readable retained artifacts outrank summary prose when they conflict.
3. Exact-claim evidence outranks adjacent or proxy evidence.
4. Independent evidence outranks self-authored assertions for efficacy claims and security acceptance.
5. Contradictory evidence remains visible and triggers reconciliation or downgrade.
6. Historical exact-tree evidence remains valid within its original scope; later state changes do not rewrite history.
7. Historical evidence does not transfer to a new candidate without an explicit provenance/transfer classification.

## Status vocabulary

Use the canonical ladder in [`EPISTEMIC_EVIDENCE_STANDARD.md`](EPISTEMIC_EVIDENCE_STANDARD.md):

`DEFINED → IMPLEMENTED → TESTED → VERIFIED → ATTESTED → VALIDATED → EMPIRICALLY SUPPORTED`

The status is claim-specific. A repository is never globally `VERIFIED` merely because one subsystem, workflow, deployment, or synthetic evaluator passes.
