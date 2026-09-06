# P1–P9 Deliberative Predicate Evidence Matrix

**Status:** CURRENT / PRE-FREEZE / FAIL-CLOSED  
**Last reconciled:** 2026-09-06  
**Live v0.7.6 source boundary:** `972edd41f16c69c6912af08c7d6c3aa627fdd8a9`  
**Consolidated control-state anchor:** `89be386b136aeb5f1fc5ca39d4aac4b3781a9f58`  
**Corrected apparatus source:** `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`  
**Historical runtime-evidence candidate:** `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8` / tree `586c00d6dedb589e52108279f9759be3c4f927e1`  
**Final v0.7.6 candidate:** `NOT DESIGNATED` — Issue #309  
**Empirical N:** `0`  
**Pilot authorization:** `NOT GRANTED`  
**Freeze:** `NOT ESTABLISHED`

This matrix is the current planning/control surface. It does not itself constitute efficacy evidence, freeze, authorization, empirical execution, or final-candidate designation. Historical evidence remains exact-SHA/run/artifact/deployment/protocol scoped.

PR #308 changed the apparatus to protocol v0.7.6 / artifact schema 1.1. Therefore `7c1cc4bb…` remains provenance-valid for its exact evidence boundary but is no longer eligible as the final freeze/N=1 candidate. Issue #309 governs final-candidate reconstruction and evidence transfer/reverification. The consolidated control-state anchor `89be386b…` remains a control/provenance anchor, not a candidate designation.

## Predicate matrix

| Predicate | Current state | Evidence / remaining boundary |
|---|---|---|
| Historical P1 Candidate Integrity | **CLOSED / VERIFIED** | exact `7c1cc4bb…` apparatus/candidate/tree plus deployment binding; final-candidate transfer/reverification pending #309 |
| Historical P2 Execution Contract / Runtime | **CLOSED / VERIFIED** | run `33730195621`; artifact `9883521704`; digest `sha256:5ca5bd3496c31f569a87338c1a0a3d93200e46106a5efda19d8269022adf696d`; final-candidate transfer/reverification pending #309 |
| Historical P3 Artifact Contract | **CLOSED / VERIFIED** | run `33939955138`; artifacts `9961526468` / `9961526662`; structural/contract scope only; final-candidate transfer/reverification pending #309 |
| P4 Security / Blinding | **OPEN / PROCEDURE REVISED / OPERATION NOT EXECUTED** | canonical P4 procedure accepts Mode H human, Mode I institutional, or Mode T independently enforced technical custody; no real custody instance or no-unilateral-access evidence exists yet |
| Historical P5 Provenance / Reproducibility | **CLOSED / VERIFIED** | exact pre-v0.7.6 candidate identities, deterministic configuration, reproduction evidence, and authoritative binding; final-candidate transfer/reverification pending #309 |
| Historical P6 Durable Evidence Custody | **CLOSED / VERIFIED** | independent archive → retrieval → SHA-256 equality for retained historical evidence set; final-candidate rebind decision pending #309 |
| Historical P6a Runtime / CORS | **CLOSED / VERIFIED** | run `33728695806`; artifact `9882965299`; digest `sha256:527145195518f7ed147507e02b3ed7cdc4bd9be0c547645dedd094a4f4d3340f`; final-candidate transfer/reverification pending #309 |
| Final v0.7.6 candidate | **NOT DESIGNATED** | exact immutable v0.7.6-descended SHA/tree required under #309 |
| P7 Scientific Target | **ADOPTED / FINAL BINDING OPEN** | final exact tuple still blocked by final candidate identity, actual P4-A custody evidence, and final pre-freeze identities |
| P8 Analysis Lock | **OPEN / FAIL-CLOSED** | analysis identities are historically bound; immutable freeze has not been created/verified |
| P9 Independent Verification | **NOT EXECUTED / OPEN** | fresh independent verification of the final frozen chain remains required |

## Historical exact-scope evidence summary

### P1 — candidate/deployment identity

Historical candidate `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`, tree `586c00d6…`, is exact-bound to production deployment `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA`. This establishes deployment identity for that historical candidate, not current-main production health, efficacy, or final v0.7.6 candidate identity.

### P2 — authenticated runtime matrix

Run `33730195621` completed all five predeclared exact-candidate runtime cases successfully. Artifact `9883521704` is candidate/deployment bound. The expected HTTP 503 / `BLOCKED` valid-request result is fail-closed contract behavior because live audit state is not wired; it is not application-health evidence. This result remains valid for its historical scope and must be classified under #309 before use toward final-candidate closure.

### P3 — artifact contract

Run `33939955138` verified candidate/tree identity, canonical matrix/schema/cardinality constraints, deterministic contract behavior, duplicate rejection, and fail-closed unauthorized pilot behavior. P3 remains structural/contract evidence only and is historical to the pre-v0.7.6 candidate unless explicitly transferred/reverified under #309.

### P4 — synthetic evidence plus independently enforceable custody procedure

Synthetic mock-key blinding/bijection/leakage/freeze-order controls pass. The canonical procedure is now `docs/governance/P4_INDEPENDENT_BLINDING_CUSTODY_PROCEDURE.md`.

P4-A no longer equates independence with a mandatory personal second-human relationship. It requires the execution/analysis principal to lack unilateral early access to the raw blinding key, cleartext mapping, commitment nonces, or equivalent recovery material.

Three custody modes are admissible:

- `H`: genuinely distinct human custody;
- `I`: institutional/third-party custody outside the analyst's unilateral control;
- `T`: independently enforced technical custody with no analyst-controlled owner/admin/recovery/export/break-glass path capable of defeating the blind.

Every mode requires nonce-hardened key/mapping commitments, timestamp ordering, a complete control-path inventory, no-unilateral-access evidence, and independently inspectable review evidence. AI agents, aliases, same-operator accounts, ordinary repository secrets, analyst-recoverable vaults, analyst-administered KMS/HSM configurations, and preregistration alone are not substitutes.

No real custody instance has occurred. P4 therefore remains OPEN / NOT EXECUTED operationally.

### P5 — provenance / reproducibility

P5 is **CLOSED / VERIFIED** for its bounded historical `7c1cc4bb…` provenance/reproducibility claim.

Exact historical identities:

- analysis implementation blob `a269ed226b1d261663994fc3ef0e8a1a96da6cd3`;
- analysis configuration SHA-256 `6cab3f1ed6d4e040141598d293628dbab52442234c519b3e231b76a2896f09a8`;
- pilot runner blob `b5152fa3c9c4effe1c5201a45d58ac2d6b8e5243`;
- pilot artifact schema blob `c620d3755a645c5f2ad14124f42ce07a1c670c5f`;
- protocol `0.7.5`.

The analysis configuration digest was independently recomputed and matched exactly. PR #247 bound these identities into the authoritative control plane and merged as signed commit `2e325acdde74dde50d3d4dc4f493a834fbd28eb2`. Post-merge Governance CI run `33945464907` and PDMAL Pre-Authorization Security run `33945464908` both completed successfully, including locked P8 analysis, artifact-schema, execution-contract, retention, adversarial, formal-model, and non-empirical-mode checks.

P5 closure is not efficacy evidence and does not imply freeze or authorization. These identities do not silently become v0.7.6 final-candidate evidence.

### P6 — durable custody

The retained P3/P5 and P4 evidence ZIPs were independently archived, retrieved, and re-hashed; retrieved SHA-256 values matched the original GitHub artifact digests. Scope remains byte-integrity/retention for the specified historical evidence set; final-candidate rebind is governed by #309.

### P6a — authenticated CORS matrix

Run `33728695806` completed the four exact-candidate CORS cases successfully. This evidence is scoped to the tested endpoint, deployment, environment, and origins for `7c1cc4bb…` / `dpl_8Msuf…`, and must be classified under #309 before final-candidate use.

## Anti-transfer / fail-closed rule

No historical candidate, deployment, artifact, runtime result, protocol/schema identity, or empirical observation transfers to another identity merely because code or prose appears equivalent. Deployment health, CI success, synthetic evidence, control-plane reconciliation, preregistration, or a custody mechanism's existence are not empirical efficacy evidence.

## Remaining critical path

1. Complete any candidate-relevant P4 apparatus work required for the selected custody mode.
2. Explicitly designate one exact immutable v0.7.6-descended final candidate under Issue #309.
3. Classify historical evidence as transferable by construct, historical only, source/structure re-verifiable, runtime/deployment re-verifiable, re-archive/rebind, or not yet executable; regenerate only what is required.
4. Instantiate one acceptable P4-A custody mode for the exact final apparatus and independently verify the no-unilateral-access invariant.
5. Complete P7 final exact binding.
6. Construct and independently verify the immutable P8 freeze.
7. Execute independent P9 verification of the final frozen chain.
8. Record separate explicit pilot authorization.
9. Only then execute blinded empirical pilot observations.

**Current experimental boundary: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
