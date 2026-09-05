# P7 Final Scientific Binding — Draft

**Status:** DRAFT / NOT CLOSED / PRE-FREEZE / FAIL-CLOSED  
**Purpose:** Assemble the exact scientific identity tuple that must be accepted before P7 may close and P8 may construct the immutable freeze.

This document is a binding draft only. Missing fields remain explicit and prevent closure.

## Current known identities

| Binding | Exact value | State |
|---|---|---|
| Corrected apparatus provenance anchor | `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1` | KNOWN |
| Immutable P-35 validation boundary | `643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d` | KNOWN |
| Consolidated control-state anchor | `89be386b136aeb5f1fc5ca39d4aac4b3781a9f58` | KNOWN |
| Designated runtime candidate | `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8` | KNOWN |
| Runtime candidate tree | `586c00d6dedb589e52108279f9759be3c4f927e1` | KNOWN |
| Exact production deployment | `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA` | KNOWN / CANDIDATE-BOUND |
| Protocol version | `0.7.5` | SELECTED / PRE-FREEZE |
| Analysis implementation Git blob | `a269ed226b1d261663994fc3ef0e8a1a96da6cd3` | KNOWN |
| Analysis configuration SHA-256 | `6cab3f1ed6d4e040141598d293628dbab52442234c519b3e231b76a2896f09a8` | KNOWN |
| Pilot runner Git blob | `b5152fa3c9c4effe1c5201a45d58ac2d6b8e5243` | KNOWN |
| Pilot artifact schema Git blob | `c620d3755a645c5f2ad14124f42ce07a1c670c5f` | KNOWN |
| P2 runtime run | `33730195621` | CLOSED / VERIFIED |
| P2 artifact | `9883521704` | CLOSED / VERIFIED |
| P2 artifact digest | `sha256:5ca5bd3496c31f569a87338c1a0a3d93200e46106a5efda19d8269022adf696d` | CLOSED / VERIFIED |
| P3 structural run | `33939955138` | CLOSED / VERIFIED |
| P3 source artifact | `9961526468` | CLOSED / VERIFIED |
| P3 registry artifact | `9961526662` | CLOSED / VERIFIED |
| P6 durable custody | independent archive/retrieval/hash equality | CLOSED / VERIFIED FOR RETAINED SET |
| P6a CORS run | `33728695806` | CLOSED / VERIFIED |
| P6a artifact | `9882965299` | CLOSED / VERIFIED |
| P6a artifact digest | `sha256:527145195518f7ed147507e02b3ed7cdc4bd9be0c547645dedd094a4f4d3340f` | CLOSED / VERIFIED |

## Scientific target selected

- Primary contrast: full `dgaf` versus `null`.
- Primary endpoint: FFCR.
- Statistical unit: paired root seed.
- Seed-level effect: `Delta_s = FFCR_s(dgaf) - FFCR_s(null)`.
- Primary estimand: equal-weight mean paired seed effect.
- Bootstrap: 10,000 paired-seed percentile resamples.
- Deterministic bootstrap seed: `20260823`.
- Confidence interval: two-sided 95%, `alpha=0.05`.
- Directional support: estimate > 0 and confidence-interval lower bound > 0.
- No outcome-dependent weighting, silent imputation, or silent exclusion.

These are design selections, not results.

## Required fields that remain unresolved

| Binding | Required value | Current state |
|---|---|---|
| P4 real Key Custodian identity | attributable human identity | `null` / NOT EXECUTED |
| P4 execution/analysis principal identity | attributable distinct human identity | `null` / NOT EXECUTED |
| P4 key commitment | non-secret commitment created before execution | `null` / NOT EXECUTED |
| P4 mapping commitment | non-secret commitment created before execution | `null` / NOT EXECUTED |
| P4 custody/access-separation attestation | independently reviewable evidence | `null` / NOT EXECUTED |
| P5 authoritative binding merge | commit containing accepted analysis/config/runner/schema binding | `null` / PENDING REVIEW |
| Final protocol blob/commit identity | immutable identity of protocol text at freeze | `null` / NOT FROZEN |
| Final governance/control-plane commit | immutable accepted control state | `null` / NOT FROZEN |
| Freeze manifest identity | immutable manifest commit/object/digest | `null` / NOT CREATED |
| Independent freeze verification | independent verifier evidence | `null` / NOT EXECUTED |
| Final P9 verifier identity | independent verifier principal/system | `null` / NOT EXECUTED |
| Final P9 evidence artifact/digest | verification of complete final bound chain | `null` / NOT EXECUTED |
| Pilot authorization record | separate explicit authorization identity | `null` / NOT GRANTED |

Any `null` field above is closure-blocking. It must not be substituted with a placeholder value that looks complete.

## P7 closure rule

P7 may be considered for `CLOSED / VERIFIED` only when:

1. every scientific identity used by the experiment is exact and immutable;
2. the final analysis implementation/configuration binding has been accepted on the authoritative branch;
3. P4 real human/key custody and access separation are evidenced and independently reviewable;
4. no candidate/runtime/protocol identity conflict remains;
5. the exact final tuple is ready to be copied into the immutable freeze manifest without interpretation or guesswork.

P7 closure is a binding decision. It is not empirical evidence and does not itself authorize execution.

## Machine-readable draft

```yaml
p7_binding_version: "1"
status: "OPEN"
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
p4_custody_evidence: null
p5_authoritative_binding_commit: null
final_protocol_identity: null
final_control_plane_commit: null
freeze_manifest_identity: null
freeze_verification_evidence: null
p9_final_evidence: null
pilot_authorization: null
empirical_n: 0
```

## Explicit non-claims

This draft does not:

- close P4, P5, P7, P8, or P9;
- create an immutable freeze;
- authorize a pilot;
- authorize unblinding;
- convert synthetic or deployment evidence into empirical evidence;
- increase empirical N.

**P7 remains ADOPTED / FINAL BINDING OPEN.**  
**Freeze: NOT ESTABLISHED.**  
**Pilot authorization: NOT GRANTED.**  
**Empirical N: 0.**
