# P1–P9 Deliberative Predicate Evidence Matrix

**Status:** CURRENT / PRE-FREEZE / FAIL-CLOSED  
**Last reconciled:** 2026-09-03  
**Control-plane lineage:** `main`  
**Corrected apparatus source:** `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`  
**Immutable P-35 validation boundary:** `643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d` (PR #199)  
**Current successor candidate:** `48c12c6660df7decb61f9aac4d8560526a8754eb` (PR #200)  
**Current successor branch:** `candidate/p35-validated-control-state-2026-09-02`  
**Exact successor deployment:** `dpl_CW4SqTjvGui2dGmfYfjxWBm6rp5K` (READY; `/api/orchestrate` reachable; GET returns 405 as expected for a POST endpoint)  
**Empirical N:** `0`  
**Pilot authorization:** `NOT GRANTED`  
**Freeze:** `NOT CREATED`

This matrix is a control surface, not efficacy evidence. Every experimental predicate remains candidate-, deployment-, artifact-, and run-scoped. Historical evidence never transfers merely because code or workflow structure is shared.

## Identity roles

- `2a54a67d…` — canonical corrected seven-gate apparatus/provenance source.
- `643dc77a…` — immutable P-35 validation boundary established by PR #199.
- `48c12c66…` — current successor candidate established by PR #200 from the P-35 boundary.
- `dpl_CW4SqTjvGui2dGmfYfjxWBm6rp5K` — deployment independently verified for `48c12c66…`; authenticated runtime verification is still outstanding.
- PR #200 — current candidate/control-state reconciliation record; remains open and draft.
- Prior runtime candidate/deployment and prior completion-candidate evidence are historical and non-closing for `48c12c66…`.

## Predicate matrix

| Predicate | Required evidence | Current state | Closure condition |
|---|---|---|---|
| P1 Candidate Integrity | exact final apparatus/source, candidate/tree, deployment, provenance | **OPEN** | retain one exact candidate/deployment/provenance binding for the closing cycle |
| P2 Execution Contract / Runtime | authenticated five-case runtime matrix on exact deployment | **RERUN REQUIRED** | dispatch workflow against `48c12c66…` + exact deployment; all five cases pass |
| P3 Artifact Contract | schema, identity, uniqueness, balance, canonicalization, deviation integrity | **DRY-RUN PASS / CLOSURE OPEN** | fresh current-candidate artifact-contract evidence |
| P4 Security / Blinding | operational key custody, access separation, independent bijection verification, no premature unblinding | **OPEN** | exact-candidate operational blinding/custody evidence |
| P5 Provenance / Reproducibility | exact environment/toolchain/topology/RNG identity and deterministic reproduction | **DRY-RUN PASS / CLOSURE OPEN** | fresh exact-candidate reproducibility evidence and independent fingerprint checks |
| P6 Durable Evidence Custody | durable archive, independent retrieval, source/archive/retrieved hash equality | **OPEN / FAIL-CLOSED** | current-candidate durable archive plus independent retrieval/hash proof |
| P6a Runtime/CORS | authenticated four-case CORS matrix on exact deployment | **RERUN REQUIRED** | dispatch workflow against the same exact candidate/deployment; all four checks pass |
| P7 Scientific Target | adopted scientific decision plus exact apparatus/candidate/protocol/analysis binding | **ADOPTED / FINAL BINDING OPEN** | exact binding retained for closing cycle |
| P8 Analysis Lock | locked analysis/schema/runner/protocol and prerequisite evidence | **OPEN / FAIL-CLOSED** | current-candidate P2–P7 evidence + final lock predicates all pass |
| P9 Independent Verification | independent identity/artifact/analysis/invariant/adversarial verification | **NOT EXECUTED FOR SUCCESSOR** | fresh independent P9 against the closing candidate |

## Current successor validation wave

PR #200 exact head `48c12c6660df7decb61f9aac4d8560526a8754eb` has a completed green PR validation wave, including:

- control-state HEAD binding;
- document lint;
- PDMAL harness validation;
- epistemic evidence validation;
- governance CI;
- propagation consistency;
- instrumentation dry run;
- full repository coverage audit;
- truth-layer validation/tests;
- claim/IP hygiene;
- DGAF regression;
- pre-authorization security;
- pre-freeze runner validation.

The instrumentation dry run is structural evidence only. Its artifact was `9873580197`, ZIP SHA-256 `8df8c67d694f35c35824ac5511593e72ef9c2f182e835e5dbf5ee2aacb7e6dfa`; the inner CSV checksum sidecar matched recomputation. This does not advance empirical N and does not close P3–P6 operationally.

The pre-freeze runner validation produced artifact `9873664736`, ZIP SHA-256 `8ebbeeb635fb63d682ba4c95287cf7c6fe0eb9f669f7e1e68e8925bf5bc8ee54`. The manifest recorded `empirical_data_collection=false`, `status=pre-freeze`, and exact commit `48c12c66…`.

Governance freeze-control evidence remains explicitly negative for the current cycle: authorization `NOT_GRANTED`, empirical N `0`, freeze `NOT_CREATED`, with no pilot mode selected and no pilot artifacts in the verification workspace.

## P-35 boundary

The immutable P-35 remediation/validation boundary is PR #199 at exact SHA `643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d`. PR #200 is a successor candidate derived from that boundary and does not modify the evidence boundary.

The successor candidate inherits no P2/P6a/P3/P9 evidence from prior candidates. Any affected predicate must be re-earned against the exact successor candidate.

## P2 / P6a execution blocker

`.github/workflows/p2-runtime-verification.yml` and `.github/workflows/p6a-cors-verification.yml` are correctly `workflow_dispatch`-only and require exact candidate SHA, exact deployment ID, deployment URL, and the configured `VERCEL_AUTOMATION_BYPASS_SECRET`. The repository integration available for this session does not expose a workflow-dispatch write operation. Therefore these authenticated gates cannot truthfully be marked executed from this control surface.

This is an execution-interface limitation, not a predicate failure. Historical P2/P6a passes remain bound to their original candidate/deployment and do not transfer.

## Required closure sequence

1. Complete PR #200 identity review without changing its exact validated tree unless a new candidate is intentionally established.
2. Execute authenticated P2 and P6a against `48c12c66…` and `dpl_CW4SqTjvGui2dGmfYfjxWBm6rp5K` using the configured bypass secret.
3. Produce fresh current-candidate P3–P6 operational evidence, including blinding, reproducibility, and durable custody.
4. Finalize P7 exact scientific/protocol/apparatus/analysis binding.
5. Close P8 only from current-candidate evidence.
6. Execute fresh independent P9 against the same closing candidate.
7. Create and independently verify a new immutable freeze.
8. Obtain separate explicit pilot authorization.
9. Only then execute the blinded pilot; empirical N may advance from `0` only after that transition.

**Current experimental boundary: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
