# DGAF-Framework

**Dynamic Governance Agentic Formation (DGAF)** — a research and implementation repository for agent orchestration, formation governance, evaluation, provenance, and governance controls.

> **Epistemic status:** This README describes repository scope and the current pre-freeze governance state. Individual claims require exact evidence and defined scope. Historical evidence remains scoped to the SHA/run/deployment/artifact that produced it.

## Current project state — 2026-09-03

The DGAF/PDMAL experimental track remains **PRE-FREEZE / FAIL-CLOSED**. No pilot authorization has been granted and empirical **N = 0**.

`main` is the documentation/control-plane lineage. The immutable P-35 validation boundary is `643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d` (PR #199). The current successor candidate is PR #200 at exact SHA `48c12c6660df7decb61f9aac4d8560526a8754eb`, branch `candidate/p35-validated-control-state-2026-09-02`. Its exact Vercel deployment is `dpl_CW4SqTjvGui2dGmfYfjxWBm6rp5K`, which is READY and source-bound to that SHA.

These identities are deliberately distinct. Historical candidates and their evidence are not promoted merely because the repository structure or workflow is shared.

## Current TGL / governance boundary

- required unwired gates reduce to fail-closed escalation rather than PASS;
- `WARN` remains distinct from terminal failure;
- conditional HPG cannot execute after terminal failure;
- terminal failures stop downstream gate execution;
- the final audit seal covers the complete gate set, including Herald;
- invalid or missing gate outcomes do not silently become PASS;
- the P-35 premise checker is explicitly injectable and missing/malformed/unloadable configuration remains fail-closed.

## Canonical agent-role boundary

- Sentinel-Phi — canonical governance/security identity.
- Professor Prodigy — formalization/proof; non-orchestrating.
- DemiJoule — advisory resource/constraint analysis; no independent normative authorization.
- Reciprocity — fairness and affected-party review.
- Herald — evidence/public-surface publication; cannot manufacture evidence or approval.
- Amethyst — meta-orchestration/lifecycle coordination.
- COLLEEN — continuity/archive/provenance/routing integrity.
- Apogee — independent evidence/integrity review.

Generic execution roles do not create or elevate agent authority.

## Experimental gate state

| Boundary | Status |
|---|---|
| Immutable P-35 validation boundary | `643dc77a…` / PR #199 |
| Current successor candidate | `48c12c6660df7decb61f9aac4d8560526a8754eb` / PR #200 |
| Exact successor deployment | `dpl_CW4SqTjvGui2dGmfYfjxWBm6rp5K` / READY |
| P2 runtime verification | `RERUN REQUIRED` — no preserved exact-candidate workflow artifact |
| P3 | `DRY-RUN PASS / CLOSURE OPEN` |
| P4 | `OPEN` — operational blinding/custody closure required |
| P5 | `DRY-RUN PASS / CLOSURE OPEN` |
| P6 | `OPEN / FAIL-CLOSED` — durable archive/retrieval/hash proof required |
| P6a CORS verification | `RERUN REQUIRED` — exact-deployment observations match the defined predicates, but preserved workflow artifact is historical |
| P7 | `ADOPTED / FINAL BINDING OPEN` |
| P8 | `OPEN / FAIL-CLOSED` |
| P9 | `OPEN FOR CURRENT SUCCESSOR` |
| New immutable freeze | Not created |
| Pilot authorization | Not granted |
| Empirical N | 0 |

## Current successor validation

PR #200's exact SHA `48c12c6660df7decb61f9aac4d8560526a8754eb` has a completed green PR-triggered validation wave covering the control-state binding, Governance CI and bounded TLC model check, PDMAL harness validation, instrumentation dry run, truth-layer validation/tests, epistemic evidence validation, regression, propagation consistency, repository coverage, claim/IP hygiene, pre-authorization security, and pre-freeze runner validation.

The exact-candidate instrumentation dry-run artifact is run `33701204328`, artifact `9873580197`, ZIP SHA-256 `8df8c67d694f35c35824ac5511593e72ef9c2f182e835e5dbf5ee2aacb7e6dfa`. This evidence is structural/synthetic and does not advance empirical N.

The pre-freeze runner artifact is `9873664736`, ZIP SHA-256 `8ebbeeb635fb63d682ba4c95287cf7c6fe0eb9f669f7e1e68e8925bf5bc8ee54`; its manifest records `empirical_data_collection=false`, `status=pre-freeze`, and exact commit `48c12c66…`.

## P2 / P6a execution boundary

The P2 and P6a workflows are intentionally `workflow_dispatch`-only and require exact candidate/deployment inputs plus the protected-deployment bypass secret. The connected GitHub integration used for this repository exposes workflow inspection and rerun operations, but no workflow-dispatch write operation.

P6a runtime traffic was nevertheless observed at the exact deployment. The four observed cases matched the workflow predicates, including the permitted `503` POST outcomes, the allowed-origin `204` preflight, and the disallowed-origin `403` preflight. This is supportive runtime observation, not a substitute for the candidate-bound provenance artifact.

Historical P2/P6a artifacts remain scoped to superseded candidate `92ff830b…` and must not be transferred to `48c12c…`.

## P8 / P7 boundary

P7's scientific target has been adopted, but exact final binding remains open across candidate, protocol, analysis, deployment, and eventual freeze identity.

P8 remains fail-closed until the current candidate has complete prerequisite evidence, the analysis lock is rebound to the closing candidate, and current P2–P7/P9 evidence satisfies the defined predicates.

## Required closure sequence

1. Execute and preserve candidate-bound P2 and P6a artifacts.
2. Complete operational P4 blinding/custody evidence.
3. Complete final P5 environment/topology/RNG reproducibility binding.
4. Complete durable P6 archive/retrieval/hash proof.
5. Finalize P7 exact scientific/protocol/apparatus/analysis binding.
6. Close P8 from current-candidate evidence only.
7. Execute fresh independent P9 against the same closing candidate.
8. Create and independently verify a new immutable freeze.
9. Obtain separate explicit pilot authorization.
10. Only then execute the blinded pilot and allow empirical N to advance.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**

## Anti-transfer rule

No historical candidate, deployment, runtime result, artifact, verification result, or experimental observation becomes current merely through documentation or shared implementation. Exact identity must be re-established for the closing candidate.
