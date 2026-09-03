---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-09-03
applies_to_ref: main
corrected_apparatus_source: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
current_successor_candidate_sha: 48c12c6660df7decb61f9aac4d8560526a8754eb
current_successor_candidate_branch: candidate/p35-validated-control-state-2026-09-02
current_successor_pr: 200
current_successor_deployment: dpl_CW4SqTjvGui2dGmfYfjxWBm6rp5K
candidate_status: POST-P-35 VALIDATION / PRE-FREEZE / FAIL-CLOSED / P2/P6a RERUN REQUIRED
empirical_n: 0
pilot_authorization: NOT_GRANTED
freeze: NOT_CREATED
---

# PDMAL Current Control State

This is the current pre-authorization control record. Historical evidence remains scoped to its exact tested SHA, run, deployment, and artifact. Implemented controls, deterministic dry runs, deployment readiness, and runtime observations are not equivalent to experimental efficacy evidence or authorization.

## Identity boundary

The corrected apparatus source is `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`. It remains the canonical provenance anchor for the restored behavior-affecting DGAF/TGL gate-state substrates.

The immutable P-35 validation boundary is PR #199 / exact SHA `643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d`. That evidence boundary is preserved and is not rewritten by the successor transition.

The current successor candidate is PR #200, branch `candidate/p35-validated-control-state-2026-09-02`, exact SHA `48c12c6660df7decb61f9aac4d8560526a8754eb`. This exact candidate has a green PR-triggered validation wave and remains PRE-FREEZE / FAIL-CLOSED.

The exact Vercel deployment bound to this successor candidate is `dpl_CW4SqTjvGui2dGmfYfjxWBm6rp5K`. Vercel independently reports it READY with Git SHA `48c12c6660df7decb61f9aac4d8560526a8754eb`. No historical deployment or candidate is promoted across this identity boundary.

## Current state

| Control | State | Evidence / scope |
|---|---|---|
| Immutable P-35 boundary | VALIDATED / IMMUTABLE | `643dc77a…` |
| Corrected apparatus source | CANONICAL PROVENANCE ANCHOR | `2a54a67d…` |
| Current successor candidate | CURRENT / NOT FROZEN | `48c12c…` / PR #200 |
| Exact successor deployment | READY / CANDIDATE-BOUND | `dpl_CW4SqTjvGui2dGmfYfjxWBm6rp5K` |
| PR validation wave | GREEN | Exact candidate `48c12c…` |
| P2 runtime | RERUN REQUIRED | No preserved exact-`48c12c…` workflow artifact |
| P6a CORS | RERUN REQUIRED | Runtime observation matches contract, but preserved workflow artifact is superseded |
| P3 | STRUCTURAL / DRY-RUN EVIDENCE PRESENT | Exact-candidate instrumentation dry run; operational closure remains separate |
| P4 | WORKFLOW-LEVEL / SYNTHETIC EVIDENCE PRESENT | Current-candidate blinding controls exercised; operational custody closure remains required |
| P5 | WORKFLOW-LEVEL EVIDENCE PRESENT | Determinism/RNG separation checks present; final reproducibility binding remains required |
| P6 | WORKFLOW-LEVEL EVIDENCE PRESENT | Artifact round-trip/checksum controls present; durable external retention remains required |
| P7 | ADOPTED / FINAL BINDING OPEN | Exact candidate/protocol/analysis/freeze identity still required |
| P8 | OPEN / FAIL-CLOSED | Current candidate requires exact TGL/P-35 and analysis-lock verification |
| P9 | OPEN FOR CURRENT SUCCESSOR | Independent exact-candidate verification required |
| New freeze | NOT CREATED | No immutable pilot identity exists |
| Pilot authorization | NOT GRANTED | Separate governance transition |
| Empirical data | N = 0 | No authorized pilot execution |

## Current exact-candidate validation

The PR #200 candidate passed the current PR-triggered validation wave, including control-state head binding, Governance CI and bounded TLC model checking, PDMAL harness validation, instrumentation dry run, truth-layer validation/tests, epistemic evidence validation, regression, propagation consistency, repository coverage, IP hygiene, claim hygiene, and pre-authorization/pre-freeze checks.

The exact-candidate instrumentation dry-run artifact is run `33701204328`, artifact `9873580197`, on SHA `48c12c6660df7decb61f9aac4d8560526a8754eb`. The workflow verifies the blinding secret is present without disclosure, deterministic smoke reproduction, structural/artifact tests, masked one-seed output, schema validation, checksum integrity, and artifact upload. This remains structural/synthetic evidence, not empirical efficacy evidence.

## P2/P6a boundary

The exact P2 and P6a workflows are intentionally `workflow_dispatch`-only and require the candidate SHA, exact deployment identity, protected-deployment bypass secret, and exact runtime inputs.

For P6a, the defined contract accepts an allowed-origin POST status of 200, 400, or 503 when the expected `Access-Control-Allow-Origin` header is present. The observed exact-deployment runtime pattern matched the defined four P6a predicates: allowed POST 503 with the allowed origin, disallowed POST 503 without an allow-origin header, allowed preflight 204 with the required headers, and disallowed preflight 403 without the allow-origin header.

That runtime observation is supportive diagnosis only. It is not a substitute for the candidate-bound P6a provenance artifact. The preserved GitHub P6a artifact remains bound to superseded candidate `92ff830b…` and cannot close current P6a. P2 likewise remains RERUN REQUIRED because no current candidate-bound P2 artifact is preserved.

## Required closure sequence

1. Execute and preserve exact-candidate P2 and P6a workflow artifacts.
2. Complete operational P4 blinding/custody evidence for the same candidate.
3. Complete final P5 environment/topology/RNG reproducibility binding.
4. Complete durable P6 archive/retrieval/hash proof.
5. Bind P7 to the exact candidate, protocol, analysis, and final-freeze identity.
6. Close P8 from current-candidate TGL/P-35 and analysis-lock evidence.
7. Execute independent P9 verification against the same final candidate.
8. Create and independently verify a new immutable freeze.
9. Obtain explicit pilot authorization.
10. Only then execute the blinded pilot.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**

## Anti-loop rule

Documentation changes, CI fan-out, deployment-health success, runtime observations, historical artifacts, or repeated audits do not silently create a new candidate, transfer candidate-bound evidence, create a freeze, or authorize scientific execution.
