# P1–P9 Deliberative Predicate Evidence Matrix

**Status:** CURRENT / PRE-FREEZE / FAIL-CLOSED  
**Last reconciled:** 2026-09-05  
**Control-plane reconciliation base:** `4382a7b745c1abde3a68eb7848611412f5bd34d7`  
**Consolidated control-state anchor:** `89be386b136aeb5f1fc5ca39d4aac4b3781a9f58`  
**Corrected apparatus source:** `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`  
**Runtime candidate:** `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`  
**Runtime candidate tree:** `586c00d6dedb589e52108279f9759be3c4f927e1`  
**Empirical N:** `0`  
**Pilot authorization:** `NOT GRANTED`  
**Freeze:** `NOT ESTABLISHED`

This matrix is the current planning/control surface. It does not itself constitute efficacy evidence, freeze, authorization, or empirical execution. Historical evidence remains exact-SHA/run/artifact/deployment scoped.

## Predicate matrix

| Predicate | Current state | Evidence / remaining boundary |
|---|---|---|
| P1 Candidate Integrity | **CLOSED / VERIFIED** | exact apparatus/candidate/tree plus deployment-to-candidate binding retained |
| P2 Execution Contract / Runtime | **CLOSED / VERIFIED** | run `33730195621`; artifact `9883521704`; digest `sha256:5ca5bd3496c31f569a87338c1a0a3d93200e46106a5efda19d8269022adf696d` |
| P3 Artifact Contract | **CLOSED / VERIFIED** | run `33939955138`; artifacts `9961526468` / `9961526662`; structural/contract scope only |
| P4 Security / Blinding | **OPEN / PROCEDURE ESTABLISHED / OPERATION NOT EXECUTED** | synthetic controls pass; merged `P4_HUMAN_KEY_CUSTODY_PROCEDURE.md` defines real custody requirements; distinct-human custody evidence remains absent |
| P5 Provenance / Reproducibility | **CLOSED / VERIFIED** | exact candidate identities, deterministic configuration, exact-candidate reproduction evidence, authoritative binding merge `2e325acd…`, and post-merge Governance CI / pre-authorization security PASS; see `P5_PROVENANCE_REPRODUCIBILITY_ATTESTATION_2026-09-05.md` |
| P6 Durable Evidence Custody | **CLOSED / VERIFIED** | independent archive → retrieval → SHA-256 equality for retained current-candidate evidence set |
| P6a Runtime / CORS | **CLOSED / VERIFIED** | run `33728695806`; artifact `9882965299`; digest `sha256:527145195518f7ed147507e02b3ed7cdc4bd9be0c547645dedd094a4f4d3340f` |
| P7 Scientific Target | **ADOPTED / FINAL BINDING OPEN** | final exact tuple still blocked by P4 real custody and final freeze identities |
| P8 Analysis Lock | **OPEN / FAIL-CLOSED** | analysis identities are bound; immutable freeze has not been created/verified |
| P9 Independent Verification | **NOT EXECUTED / OPEN** | fresh independent verification of the final frozen chain remains required |

## Current-candidate evidence summary

### P1 — candidate/deployment identity

Designated candidate `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`, tree `586c00d6…`, is exact-bound to production deployment `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA`. This establishes deployment identity for the candidate, not current-main production health or efficacy.

### P2 — authenticated runtime matrix

Run `33730195621` completed all five predeclared exact-candidate runtime cases successfully. Artifact `9883521704` is candidate/deployment bound. The expected HTTP 503 / `BLOCKED` valid-request result is fail-closed contract behavior because live audit state is not wired; it is not application-health evidence.

### P3 — artifact contract

Run `33939955138` verified candidate/tree identity, canonical matrix/schema/cardinality constraints, deterministic contract behavior, duplicate rejection, and fail-closed unauthorized pilot behavior. P3 remains structural/contract evidence only.

### P4 — synthetic evidence plus real-world procedure

Synthetic mock-key blinding/bijection/leakage/freeze-order controls pass. The merged P4 human/key custody procedure requires distinct human principals, secret nonce-hardened key/mapping commitments, attributable custody/no-access attestations, timestamp ordering, and independent release/continuity verification.

No such real custody event has occurred. P4 therefore remains OPEN / NOT EXECUTED operationally.

### P5 — provenance / reproducibility

P5 is now **CLOSED / VERIFIED** for its bounded provenance/reproducibility claim.

Exact candidate identities:

- analysis implementation blob `a269ed226b1d261663994fc3ef0e8a1a96da6cd3`;
- analysis configuration SHA-256 `6cab3f1ed6d4e040141598d293628dbab52442234c519b3e231b76a2896f09a8`;
- pilot runner blob `b5152fa3c9c4effe1c5201a45d58ac2d6b8e5243`;
- pilot artifact schema blob `c620d3755a645c5f2ad14124f42ce07a1c670c5f`;
- protocol `0.7.5`.

The analysis configuration digest was independently recomputed and matched exactly. PR #247 bound these identities into the authoritative control plane and merged as signed commit `2e325acdde74dde50d3d4dc4f493a834fbd28eb2`. Post-merge Governance CI run `33945464907` and PDMAL Pre-Authorization Security run `33945464908` both completed successfully, including locked P8 analysis, artifact-schema, execution-contract, retention, adversarial, formal-model, and non-empirical-mode checks.

P5 closure is not efficacy evidence and does not imply freeze or authorization.

### P6 — durable custody

The retained P3/P5 and P4 evidence ZIPs were independently archived, retrieved, and re-hashed; retrieved SHA-256 values matched the original GitHub artifact digests. Scope remains byte-integrity/retention for the specified evidence set.

### P6a — authenticated CORS matrix

Run `33728695806` completed the four exact-candidate CORS cases successfully. This evidence is scoped to the tested endpoint, deployment, environment, and origins.

## Anti-transfer / fail-closed rule

No historical candidate, deployment, artifact, runtime result, or empirical observation transfers to another identity merely because code or prose appears equivalent. Deployment health, CI success, synthetic evidence, and control-plane reconciliation are not empirical efficacy evidence.

## Remaining critical path

1. Perform and independently verify real P4 human/key custody and access separation.
2. Complete P7 final exact binding using the already-closed P1/P2/P3/P5/P6/P6a evidence plus actual P4 custody evidence.
3. Construct and independently verify the immutable P8 freeze.
4. Execute independent P9 verification of the final frozen chain.
5. Record separate explicit pilot authorization.
6. Only then execute blinded empirical pilot observations.

**Current experimental boundary: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
