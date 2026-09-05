---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-09-05
main_at_reconciliation_base: 17fbe054f0b94f68f8b379ad1c8b92f0fab16da9
consolidated_control_state_anchor: 89be386b136aeb5f1fc5ca39d4aac4b3781a9f58
corrected_apparatus_source: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
immutable_p35_validation_boundary: 643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d
runtime_candidate_sha: 7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8
runtime_candidate_tree_sha: 586c00d6dedb589e52108279f9759be3c4f927e1
runtime_deployment_reference: dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA
candidate_status: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED
empirical_n: 0
---

# DGAF-Framework / PDMAL — Current State

GitHub is authoritative for implementation and CI; governance decisions remain separately recorded. Evidence is scoped to the exact identities and predicates that produced it. A successful CI, deployment, synthetic, or custody check is not empirical efficacy evidence.

## Identity boundary

- Corrected apparatus source: `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`.
- Immutable P-35 validation boundary: `643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d`.
- Consolidated control-state anchor: `89be386b136aeb5f1fc5ca39d4aac4b3781a9f58`.
- Designated runtime candidate: `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`.
- Runtime candidate tree: `586c00d6dedb589e52108279f9759be3c4f927e1`.
- Candidate deployment: `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA`.
- Repository reconciliation base: `17fbe054f0b94f68f8b379ad1c8b92f0fab16da9`.

Later documentation/evaluator/control-plane descendants do not automatically replace the designated runtime candidate or inherit its runtime evidence.

## Current gate board

| Boundary | Status | Scope |
|---|---|---|
| P-35 | VALIDATED | immutable boundary `643dc77a…` |
| P1 candidate integrity | CLOSED / VERIFIED | apparatus, candidate/tree, and live deployment identity |
| P2 runtime | CLOSED / VERIFIED | exact `7c1cc4bb…` / `dpl_8Msuf…` five-case runtime predicates |
| P3 artifact contract | CLOSED / VERIFIED | run `33939955138`; candidate-bound structural/matrix/integrity evidence |
| P4 security/blinding | OPEN / PROCEDURE ESTABLISHED / OPERATION NOT EXECUTED | synthetic controls pass; actual distinct-human key custody/access separation absent |
| P5 provenance/reproducibility | CLOSED / VERIFIED | exact analysis/config/runner/schema identities and deterministic provenance/reproducibility evidence; not efficacy evidence |
| P6 evidence custody | CLOSED / VERIFIED | defined archive → retrieval → SHA-256 equality contract |
| P6a CORS | CLOSED / VERIFIED | exact `7c1cc4bb…` / `dpl_8Msuf…` four-case CORS predicates |
| P7 scientific target | ADOPTED / FINAL BINDING OPEN | final exact scientific/freeze identity chain incomplete |
| P8 analysis lock / freeze readiness | OPEN / FAIL-CLOSED | immutable freeze not established/verified |
| P9 independent verification | NOT EXECUTED / OPEN | final frozen-chain verification absent |
| Freeze | NOT ESTABLISHED | no immutable pilot identity |
| Authorization | NOT GRANTED | separate governance decision |
| Empirical N | 0 | no authorized pilot execution |

## Current P5 closure basis

P5 is CLOSED / VERIFIED for provenance and reproducibility only. The designated candidate's analysis-control identities are bound in the canonical control record, including the analysis implementation/configuration, runner, schema, protocol, deterministic environment, RNG separation, and topology-determinism evidence. This closure does not establish model or scientific efficacy.

## Runtime evidence retrieval

On 2026-09-05, the P2 and P6a GitHub Actions records were freshly resolved:

- P2 run `33730195621`, artifact `9883521704`, digest `sha256:5ca5bd3496c31f569a87338c1a0a3d93200e46106a5efda19d8269022adf696d`.
- P6a run `33728695806`, artifact `9882965299`, digest `sha256:527145195518f7ed147507e02b3ed7cdc4bd9be0c547645dedd094a4f4d3340f`.

Both artifacts were unexpired and candidate-bound. This is retrieval, not re-execution, and does not extend closure beyond the exact runtime predicates.

## Evaluation-integrity update

PR #269 merged as `17fbe054f0b94f68f8b379ad1c8b92f0fab16da9` and hardens Issue #32 Task 4 (`audit_hallucination_rate`). The evaluator now fails closed without provenance-controlled ground truth plus independently generated outputs and uses deterministic six-field comparison. Exact-head regression evidence includes Python Tests & Quality Checks `33957199893`, Governance CI `33957199870`, and PDMAL Pre-Freeze `33957199849`.

No Task-4 performance result exists yet. The fixture/output corpus remains a separate evidence requirement.

## Current engineering-quality limitation

Issue #270 tracks current-lineage Black/isort/mypy debt. Those diagnostics are presently `continue-on-error`, so a successful Python workflow establishes passing blocking tests and retained diagnostics, not a clean formatting/type baseline.

Historical Issue #47 remains a valid exact-tree closure for its own prior execution boundary.

## Remaining substantive closure work

`real P4 custody → exact P7 final binding → P8 immutable freeze + independent freeze verification → final independent P9 → explicit authorization → blinded pilot`

Issue #232 is the active PDMAL completion-control record. No current-facing documentation or CI success changes empirical N or self-authorizes the experiment.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
