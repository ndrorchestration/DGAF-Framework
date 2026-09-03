---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-09-03
applies_to_ref: main
corrected_apparatus_source: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
immutable_p35_validation_boundary: 643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d
current_successor_candidate_sha: 48c12c6660df7decb61f9aac4d8560526a8754eb
current_successor_candidate_branch: candidate/p35-validated-control-state-2026-09-02
current_successor_pr: 200
current_successor_deployment: dpl_CW4SqTjvGui2dGmfYfjxWBm6rp5K
empirical_n: 0
pilot_authorization: NOT_GRANTED
freeze: NOT_CREATED
---
# DGAF-Framework / PDMAL — Current State

GitHub is authoritative for implementation and CI; governance decisions remain separately recorded through the project control process. Historical evidence is scoped to the exact SHA, run, deployment, and artifact that produced it.

> **Current control-plane state:** `main` remains the documentation/control-plane lineage. The corrected apparatus source is `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`.
>
> **Immutable P-35 boundary:** PR #199 established the validated boundary at exact SHA `643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d`. That evidence boundary is preserved and is not rewritten by the successor candidate.
>
> **Current successor candidate:** PR #200 establishes exact candidate `48c12c6660df7decb61f9aac4d8560526a8754eb` on branch `candidate/p35-validated-control-state-2026-09-02`. Its current PR validation wave is green. The candidate remains PRE-FREEZE / FAIL-CLOSED.
>
> **Exact deployment:** `dpl_CW4SqTjvGui2dGmfYfjxWBm6rp5K` was independently verified for the exact successor SHA. Authenticated P2/P6a execution remains outstanding.
>
> **Current experimental boundary:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0. No empirical or unblinded pilot state has been created.

## Authoritative experimental state

| Boundary | Status | Meaning |
|---|---|---|
| Corrected apparatus source | CANONICAL PROVENANCE ANCHOR | `2a54a67d…` |
| Immutable P-35 validation boundary | VALIDATED / IMMUTABLE | `643dc77a…`; PR #199 |
| Successor candidate | CURRENT / NOT FROZEN | `48c12c66…`; PR #200 |
| Successor deployment | VERIFIED / NOT YET RUNTIME-CLOSED | `dpl_CW4SqTjvGui2dGmfYfjxWBm6rp5K` |
| PR #200 validation wave | GREEN | Control-state binding, governance/security, truth-layer, PDMAL, regression, hygiene, and pre-freeze checks passed |
| P2 runtime | RERUN REQUIRED | Workflow is authenticated and candidate/deployment bound; no current dispatch was executed |
| P3 | DRY-RUN PASS / CLOSURE OPEN | Structural contract evidence exists on exact successor candidate; operational closure still required |
| P4 | OPEN | Current-cycle blinding/custody evidence still required |
| P5 | DRY-RUN PASS / CLOSURE OPEN | Current structural checks pass; full current-cycle reproducibility closure still required |
| P6 | OPEN / FAIL-CLOSED | Durable archive/retrieval/hash proof still required |
| P6a CORS | RERUN REQUIRED | Workflow is authenticated and candidate/deployment bound; no current dispatch was executed |
| P7 | ADOPTED / FINAL BINDING OPEN | Exact apparatus/candidate/protocol/analysis binding remains to be finalized |
| P8 | OPEN / FAIL-CLOSED | Cannot close until current-candidate prerequisite evidence is complete |
| P9 | NOT EXECUTED FOR CURRENT SUCCESSOR | Fresh independent verification required |
| Freeze | NOT CREATED | No immutable pilot identity exists |
| Authorization | NOT GRANTED | Separate governance transition required |
| Empirical N | 0 | No authorized pilot execution |

## Successor validation evidence

The current successor candidate has passed the completed PR validation wave on exact SHA `48c12c6660df7decb61f9aac4d8560526a8754eb`, including PDMAL harness validation, epistemic evidence validation, governance CI, propagation consistency, instrumentation dry run, repository coverage, truth-layer validation/tests, claim/IP hygiene, DGAF regression, pre-authorization security, and pre-freeze runner validation.

The instrumentation dry run produced artifact `9873580197` with ZIP SHA-256 `8df8c67d694f35c35824ac5511593e72ef9c2f182e835e5dbf5ee2aacb7e6dfa`. Its inner CSV checksum sidecar matched recomputation. This remains structural/dry-run evidence and does not advance empirical N.

The pre-freeze runner validation produced artifact `9873664736` with ZIP SHA-256 `8ebbeeb635fb63d682ba4c95287cf7c6fe0eb9f669f7e1e68e8925bf5bc8ee54`. Its manifest recorded `empirical_data_collection=false`, `status=pre-freeze`, and exact commit `48c12c66…`.

Governance freeze-control evidence remains negative for the current cycle: authorization `NOT_GRANTED`, empirical N `0`, freeze `NOT_CREATED`, and no pilot mode/artifacts in the verification workspace.

## P2 / P6a dispatch boundary

`.github/workflows/p2-runtime-verification.yml` requires the exact candidate SHA, exact deployment ID, exact deployment URL, and the configured `VERCEL_AUTOMATION_BYPASS_SECRET`. `.github/workflows/p6a-cors-verification.yml` requires the same exact candidate/deployment binding plus the allowed origin and the same bypass secret.

Both workflows are intentionally `workflow_dispatch`-only. The connected GitHub action surface available during this reconciliation exposes inspection and rerun operations but no workflow-dispatch write operation. Consequently P2/P6a are correctly recorded as **rerun required**, not passed or failed.

Historical P2/P6a evidence from other candidates remains non-transferable.

## Anti-transfer rule

No historical candidate, deployment, runtime result, artifact, P9 result, or experimental observation may be promoted to the current successor solely because the repository or workflow structure is shared. Exact identity must be re-established for the closing candidate.

## Required closure sequence

1. Complete the remaining review of PR #200 without unnecessary candidate-tree churn.
2. Execute authenticated P2 and P6a against the exact successor candidate and exact successor deployment.
3. Produce current-cycle P3–P6 operational evidence, including blinding, reproducibility, and durable custody.
4. Finalize P7 exact scientific/protocol/apparatus/analysis binding.
5. Close P8 from current-candidate evidence only.
6. Execute fresh independent P9 against the same closing candidate.
7. Create and independently verify a new immutable freeze.
8. Obtain separate explicit pilot authorization.
9. Only then execute the blinded pilot and allow empirical N to advance above `0`.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
