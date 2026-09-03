---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-09-03
applies_to_ref: main
current_successor_candidate_sha: 48c12c6660df7decb61f9aac4d8560526a8754eb
current_successor_candidate_branch: candidate/p35-validated-control-state-2026-09-02
current_successor_pr: 200
current_successor_deployment: dpl_CW4SqTjvGui2dGmfYfjxWBm6rp5K
corrected_apparatus_source: 2a54a67d84870e4eeb71b8aaf04413e0ca492ba1
empirical_n: 0
pilot_authorization: NOT_GRANTED
freeze: NOT_CREATED
scope_note: >-
  This index records evidence and gate state. Historical evidence remains scoped
  to the exact SHA/run/deployment/artifact that produced it. Candidate verification
  does not inherit historical verification automatically. No freeze or authorization
  is implied by this registry.
---

# PDMAL Evidence Index

This is a control-plane registry, not empirical evidence and not a self-authorizing freeze record.

## Evidence inventory

| Evidence | State | Identity | Interpretation |
|---|---|---|---|
| Current documentation lineage | CURRENT | `main` | Active control/documentation lineage |
| Corrected apparatus source | CANONICAL PROVENANCE ANCHOR | `2a54a67d…` | Seven restored behavior-affecting gate-state substrates |
| Immutable P-35 validation boundary | VALIDATED / IMMUTABLE | `643dc77a…` / PR #199 | Evidence boundary preserved across successor transition |
| Current successor candidate | CURRENT / NOT FROZEN | `48c12c…` / PR #200 | Exact candidate for current closure path |
| Current successor deployment | READY / CANDIDATE-BOUND | `dpl_CW4SqTjvGui2dGmfYfjxWBm6rp5K` | Independently verified for `48c12c…` |
| PR #200 validation wave | GREEN | `48c12c…` | Current PR-triggered engineering/pre-freeze validation |
| P2 runtime | RERUN REQUIRED | No current exact-candidate artifact | Historical P2 evidence is non-transferable |
| P6a CORS runtime | RERUN REQUIRED | No current exact-candidate artifact | Exact-deployment observation matches predicates, but preserved artifact is historical |
| P3 artifact contract | STRUCTURAL / DRY-RUN PASS | Run `33701204328`; artifact `9873580197` | Exact-candidate structural evidence; operational closure separate |
| P4 blinding/security | SYNTHETIC / WORKFLOW-LEVEL PRESENT | Run `33701204328` | Secret presence and masked output controls exercised; operational custody remains open |
| P5 reproducibility | STRUCTURAL / DRY-RUN PASS | Run `33701204328` | Determinism and test controls passed; final environment/topology/RNG binding remains open |
| P6 evidence custody | WORKFLOW-LEVEL PRESENT / DURABLE OPEN | Run `33701204328` | Artifact upload/checksum controls passed; durable external archive remains open |
| P7 scientific target | ADOPTED / FINAL BINDING OPEN | Current governance specification | Exact candidate/protocol/analysis/freeze binding remains open |
| P8 analysis lock | OPEN / FAIL-CLOSED | Current control plan | Requires complete current-candidate prerequisites and exact analysis binding |
| P9 independent verification | OPEN FOR CURRENT SUCCESSOR | `48c12c…` | Fresh independent verification required |
| Freeze | NOT CREATED | — | No immutable pilot identity exists |
| Authorization | NOT GRANTED | — | Separate governance transition required |
| Empirical data | ZERO | N=0 | No authorized pilot execution |

## Current exact-candidate evidence

The current successor candidate `48c12c6660df7decb61f9aac4d8560526a8754eb` has a completed green PR validation wave. The exact-candidate instrumentation dry run is run `33701204328`, artifact `9873580197`, ZIP SHA-256 `8df8c67d694f35c35824ac5511593e72ef9c2f182e835e5dbf5ee2aacb7e6dfa`.

That dry run verifies the blinding secret is present without disclosure, deterministic smoke reproduction, structural/artifact tests, masked one-seed output, schema validation, checksum integrity, and artifact upload. It remains structural/synthetic evidence and does not constitute empirical efficacy evidence or pilot authorization.

## P2/P6a evidence boundary

The current exact deployment is `dpl_CW4SqTjvGui2dGmfYfjxWBm6rp5K`, associated with candidate `48c12c…`. P6a runtime traffic observed the four expected CORS cases at that deployment, including the workflow-permitted 503 POST outcomes, allowed-origin preflight 204, and disallowed-origin preflight 403. Because the preserved provenance artifact remains tied to superseded candidate `92ff830b…`, this runtime observation is supportive only and does not close current P6a.

P2 has no preserved current-candidate workflow artifact and remains RERUN REQUIRED.

## Evidence inheritance rule

Historical P2/P6a/P3/P9 evidence does not automatically qualify a different candidate. Candidate-bound evidence must be regenerated whenever the exact candidate or deployment identity changes in a way relevant to the predicate.

Documentation-only commits do not authorize scientific execution, but a control-plane document must accurately identify the candidate that the control plane currently governs.

## Required closure sequence

1. Execute and preserve exact-candidate P2 and P6a workflow artifacts.
2. Complete operational P4 blinding/custody evidence.
3. Complete final P5 environment/topology/RNG reproducibility binding.
4. Complete durable P6 archive/retrieval/hash proof.
5. Finalize P7 exact candidate/protocol/analysis binding.
6. Close P8 from current-candidate evidence only.
7. Execute fresh independent P9 against the same closing candidate.
8. Create and independently verify a new immutable freeze.
9. Obtain separate explicit pilot authorization.
10. Only then execute the blinded pilot.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
