# P7 Final Scientific Binding — Draft v2

**Status:** OPEN / PRE-FREEZE / FAIL-CLOSED  
**Control-plane base:** `4382a7b745c1abde3a68eb7848611412f5bd34d7`  
**Purpose:** Assemble the exact scientific identity tuple that must be accepted before P7 may close and P8 may construct an immutable freeze.

This document is a binding draft only. Unresolved values remain explicit and closure-blocking.

## Exact identities already established

| Binding | Exact value | State |
|---|---|---|
| Corrected apparatus provenance anchor | `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1` | KNOWN |
| Immutable P-35 validation boundary | `643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d` | KNOWN |
| Consolidated control-state anchor | `89be386b136aeb5f1fc5ca39d4aac4b3781a9f58` | KNOWN |
| Designated runtime candidate | `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8` | VERIFIED |
| Runtime candidate tree | `586c00d6dedb589e52108279f9759be3c4f927e1` | VERIFIED |
| Candidate production deployment | `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA` | VERIFIED FOR CANDIDATE |
| Protocol version | `0.7.5` | SELECTED / PRE-FREEZE |
| Analysis implementation Git blob | `a269ed226b1d261663994fc3ef0e8a1a96da6cd3` | BOUND |
| Analysis configuration SHA-256 | `6cab3f1ed6d4e040141598d293628dbab52442234c519b3e231b76a2896f09a8` | BOUND / INDEPENDENTLY RECOMPUTED |
| Pilot runner Git blob | `b5152fa3c9c4effe1c5201a45d58ac2d6b8e5243` | BOUND |
| Pilot artifact schema Git blob | `c620d3755a645c5f2ad14124f42ce07a1c670c5f` | BOUND |
| P5 binding merge | `2e325acdde74dde50d3d4dc4f493a834fbd28eb2` | AUTHORITATIVE MERGE / DEEP POST-MERGE VERIFICATION PASS |
| P5 Governance CI | `33945464907` | PASS |
| P5 Pre-Authorization Security | `33945464908` | PASS |
| P5 closure reconciliation merge | `fcf21ce9ab3739a7b5880c6f6896cf378a3dd2da` | CLOSED / VERIFIED ON MAIN |
| P4 custody procedure merge | `4382a7b745c1abde3a68eb7848611412f5bd34d7` | PROCEDURE ESTABLISHED / OPERATION NOT EXECUTED |
| P2 runtime run | `33730195621` | CLOSED / VERIFIED |
| P2 artifact | `9883521704` | CLOSED / VERIFIED |
| P2 digest | `sha256:5ca5bd3496c31f569a87338c1a0a3d93200e46106a5efda19d8269022adf696d` | CLOSED / VERIFIED |
| P3 structural run | `33939955138` | CLOSED / VERIFIED |
| P3 source artifact | `9961526468` | CLOSED / VERIFIED |
| P3 registry artifact | `9961526662` | CLOSED / VERIFIED |
| P6 durable custody | independent archive/retrieval/SHA equality | CLOSED / VERIFIED FOR RETAINED SET |
| P6a CORS run | `33728695806` | CLOSED / VERIFIED |
| P6a artifact | `9882965299` | CLOSED / VERIFIED |
| P6a digest | `sha256:527145195518f7ed147507e02b3ed7cdc4bd9be0c547645dedd094a4f4d3340f` | CLOSED / VERIFIED |

## Scientific target selected

- Primary contrast: full `dgaf` versus `null`.
- Primary endpoint: FFCR.
- Statistical unit: paired root seed.
- Seed-level effect: `Delta_s = FFCR_s(dgaf) - FFCR_s(null)`.
- Primary estimand: equal-weight mean paired seed effect.
- FFCR: proportion of complete topology × failure-count cells whose recorded `ffcr_success` is true.
- Bootstrap: 10,000 paired-seed percentile resamples.
- Deterministic bootstrap seed: `20260823`.
- Confidence interval: two-sided 95%, `alpha=0.05`.
- Directional support requires estimate > 0 and CI lower bound > 0.
- No outcome-dependent weighting, silent imputation, or silent exclusion.

These are design selections, not results.

## Closure-blocking unresolved identities

| Binding | Required value | Current state |
|---|---|---|
| P4 real Key Custodian identity | attributable human identity | `null` / NOT EXECUTED |
| P4 execution/analysis principal identity | distinct attributable human identity | `null` / NOT EXECUTED |
| P4 key commitment | nonce-hardened non-secret commitment | `null` / NOT EXECUTED |
| P4 mapping commitment | nonce-hardened non-secret commitment | `null` / NOT EXECUTED |
| P4 custody/access-separation attestation | independently reviewable operational evidence | `null` / NOT EXECUTED |
| Final protocol blob/commit identity | immutable protocol identity at freeze | `null` / NOT FROZEN |
| Final control-plane commit | exact accepted pre-freeze control state | `null` / NOT FROZEN |
| Freeze manifest identity | immutable manifest object/digest | `null` / NOT CREATED |
| Independent freeze verification | independently produced verification evidence | `null` / NOT EXECUTED |
| Final P9 verifier identity | independent verifier principal/system | `null` / NOT EXECUTED |
| Final P9 evidence artifact/digest | verification of complete final bound chain | `null` / NOT EXECUTED |
| Pilot authorization record | separate explicit authorization identity | `null` / NOT GRANTED |

Any `null` field above prevents P7 closure.

## P4 procedure boundary

`docs/governance/P4_HUMAN_KEY_CUSTODY_PROCEDURE.md` is now part of the control plane. It defines the required real-world role separation and nonce-hardened commitment scheme, but its existence is **not** evidence that custody occurred.

P4 therefore remains OPEN until distinct humans actually perform and independently attest the procedure.

## P5 boundary

P5 is now **CLOSED / VERIFIED** on `main`. The exact analysis/configuration/runner/schema identities were bound through `2e325acd…`; exact post-merge Governance CI `33945464907` and PDMAL Pre-Authorization Security `33945464908` both passed; and the authoritative P5 closure reconciliation merged as `fcf21ce9ab3739a7b5880c6f6896cf378a3dd2da`.

This P5 closure is provenance/reproducibility evidence only. It is not efficacy evidence, a freeze, authorization, or empirical execution.

## P7 closure rule

P7 may be considered for `CLOSED / VERIFIED` only when:

1. all scientific identities used by the experiment are exact and immutable;
2. P5 remains authoritative and internally consistent;
3. P4 real human/key custody and access separation are evidenced and independently reviewable;
4. no candidate/runtime/protocol/analysis identity conflict remains;
5. the final tuple can be copied into the immutable freeze manifest without inference or unresolved placeholders.

P7 closure is a binding decision, not empirical evidence and not authorization.

## Machine-readable draft

```yaml
p7_binding_version: "2"
status: "OPEN"
control_plane_base: "4382a7b745c1abde3a68eb7848611412f5bd34d7"
apparatus_anchor: "2a54a67d84870e4eeb71b8aaf04413e0ca492ba1"
p35_boundary: "643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d"
control_state_anchor: "89be386b136aeb5f1fc5ca39d4aac4b3781a9f58"
candidate_sha: "7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8"
candidate_tree_sha: "586c00d6dedb589e52108279f9759be3c4f927e1"
deployment_id: "dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA"
protocol_version: "0.7.5"
analysis_blob_sha: "a269ed226b1d261663994fc3ef0e8a1a96da6cd3"
analysis_config_sha256: "6cab3f1ed6d4e040141598d293628dbab52442234c519b3e231b76a2896f09a8"
runner_blob_sha: "b5152fa3c9c4effe1c5201a45d58ac2d6b8e5243"
artifact_schema_blob_sha: "c620d3755a645c5f2ad14124f42ce07a1c670c5f"
p5_binding_merge: "2e325acdde74dde50d3d4dc4f493a834fbd28eb2"
p5_deep_postmerge_verification:
  governance_ci_run: 33945464907
  preauthorization_security_run: 33945464908
  conclusion: "PASS"
p5_closure_reconciliation: "fcf21ce9ab3739a7b5880c6f6896cf378a3dd2da"
p4_procedure_merge: "4382a7b745c1abde3a68eb7848611412f5bd34d7"
p4_custody_evidence: null
final_protocol_identity: null
final_control_plane_commit: null
freeze_manifest_identity: null
freeze_verification_evidence: null
p9_final_evidence: null
pilot_authorization: null
empirical_n: 0
```

## Explicit non-claims

This draft does not close P4, P7, P8, or P9; create a freeze; authorize a pilot or unblinding; convert deployment/CI/synthetic evidence into empirical evidence; or increase empirical N.

**P5: CLOSED / VERIFIED.**  
**P7 remains ADOPTED / FINAL BINDING OPEN.**  
**Freeze: NOT ESTABLISHED.**  
**Pilot authorization: NOT GRANTED.**  
**Empirical N: 0.**
