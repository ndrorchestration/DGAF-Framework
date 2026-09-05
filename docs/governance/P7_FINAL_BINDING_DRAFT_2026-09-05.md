# P7 Final Scientific Binding — Draft v4

**Status:** OPEN / PRE-FREEZE / FAIL-CLOSED  
**Draft lineage anchor:** `4382a7b745c1abde3a68eb7848611412f5bd34d7`  
**Purpose:** Assemble the exact pre-freeze scientific identity tuple that must be accepted before P7 may close and P8 may construct an immutable freeze.

This document is a binding draft only. Unresolved pre-freeze values remain explicit and closure-blocking. Outputs that can exist only after P7 closure are tracked separately and are not permitted to create a circular P7 dependency.

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
| P4 original human procedure merge | `4382a7b745c1abde3a68eb7848611412f5bd34d7` | HISTORICAL PROCEDURE ANCHOR |
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

## P7 closure-blocking pre-freeze identities

Only facts that can legitimately exist before immutable-freeze construction may block P7 closure.

| Binding | Required value | Current state |
|---|---|---|
| P4 custody mode | exactly one of `H`, `I`, `T` | `null` / NOT EXECUTED |
| P4 custody instance ID | unique non-secret identity | `null` / NOT EXECUTED |
| P4 custody authority/system identity | attributable human, institution/service, or technical control identity | `null` / NOT EXECUTED |
| P4 execution/analysis principal identity | attributable identity | `null` / NOT EXECUTED |
| P4 key commitment | nonce-hardened non-secret commitment | `null` / NOT EXECUTED |
| P4 mapping commitment | nonce-hardened non-secret commitment | `null` / NOT EXECUTED |
| P4 control-path inventory identity/digest | all relevant ordinary/admin/recovery/backup/export/break-glass paths | `null` / NOT EXECUTED |
| P4 no-unilateral-access evidence | evidence analyst cannot defeat custody alone | `null` / NOT EXECUTED |
| P4 independent review evidence | independently inspectable support for effective control separation | `null` / NOT EXECUTED |
| Final protocol Git blob | exact protocol blob selected for freeze | `null` / BIND AT P7 CLOSURE |
| Final protocol content SHA-256 | exact protocol bytes selected for freeze | `null` / BIND AT P7 CLOSURE |
| Final accepted pre-freeze control-plane commit | exact accepted state from which freeze is constructed | `null` / NOT SELECTED |
| Selected final-P9 verifier script SHA-256 | exact verifier content at accepted pre-freeze control state | `null` / BIND AT P7 CLOSURE |
| Selected final-P9 workflow SHA-256 | exact workflow content at accepted pre-freeze control state | `null` / BIND AT P7 CLOSURE |

Any `null` field in this pre-freeze table prevents P7 closure.

## Downstream outputs — not P7 closure blockers

| Downstream output | Current state |
|---|---|
| Immutable freeze commit identity | `null` / P8 NOT EXECUTED |
| External immutable-freeze byte SHA-256 | `null` / P8 NOT EXECUTED |
| Separate P8 freeze-verification record commit | `null` / P8 NOT EXECUTED |
| External P8 verification-record byte SHA-256 | `null` / P8 NOT EXECUTED |
| Final P9 evidence artifact/digest | `null` / P9 NOT EXECUTED |
| Pilot authorization record | `null` / NOT GRANTED |

These values remain null at legitimate P7 closure. They are populated by P8, P9, and separate authorization steps in that order.

## Non-circular P8/P9 identity rule

P8 uses two immutable identity layers:

1. **Freeze commit F** — contains the finalized freeze object, final P7 binding, candidate/control identities, and selected P9 verifier definition. The exact freeze-object byte SHA-256 is retained externally.
2. **P8 verification record V** — produced only after F has been independently retrieved and re-hashed. V is stored separately in a descendant verification commit and references F plus the exact freeze digest. V is never embedded back into F and does not self-embed the SHA of its containing commit.

Final P9 executes from the verification-record commit, independently resolves F, verifies the freeze and verification-record digests, verifies the final protocol/control-plane/verifier bindings declared by closed P7, and proves the P9 script/workflow definitions have not drifted from those frozen at F.

## P4 procedure boundary

`docs/governance/P4_INDEPENDENT_BLINDING_CUSTODY_PROCEDURE.md` is the canonical P4 control. It preserves the original human-custody path as Mode H and also permits Mode I institutional/third-party custody or Mode T independently enforced technical custody.

P4-A closure depends on the same invariant for every mode: **the execution/analysis principal cannot unilaterally recover the protected blinding material before the predeclared release condition**.

A second human is therefore not mandatory, but apparent separation that remains under the analyst's effective owner/admin/recovery/export/break-glass control is not acceptable. AI agents, aliases, same-operator accounts, ordinary repository secrets, analyst-recoverable vaults, and preregistration alone do not satisfy P4.

The canonical procedure's existence is not evidence that custody occurred. P4 remains OPEN until one selected custody mode is actually instantiated and independently verified.

## P5 boundary

P5 is **CLOSED / VERIFIED** on `main`. The exact analysis/configuration/runner/schema identities were bound through `2e325acd…`; exact post-merge Governance CI `33945464907` and PDMAL Pre-Authorization Security `33945464908` both passed; and the authoritative P5 closure reconciliation merged as `fcf21ce9ab3739a7b5880c6f6896cf378a3dd2da`.

This P5 closure is provenance/reproducibility evidence only. It is not efficacy evidence, a freeze, authorization, or empirical execution.

## P7 closure rule

P7 may be considered for `CLOSED / VERIFIED` only when:

1. all pre-freeze scientific identities used by the experiment are exact;
2. P5 remains authoritative and internally consistent;
3. P4-A is closed under one declared custody mode with evidence that the execution/analysis principal lacks every unilateral early-recovery path relevant to that mode;
4. final protocol blob/content and accepted pre-freeze control-plane identities are fixed;
5. selected P9 verifier script/workflow SHA-256 identities are fixed before freeze;
6. no candidate/runtime/protocol/analysis/custody identity conflict remains; and
7. the complete P7 tuple can be copied into the immutable freeze object without inference or unresolved pre-freeze placeholders.

P7 closure is a binding decision, not empirical evidence and not authorization. P7 does not require downstream P8/P9/auth outputs that do not yet exist.

## Machine-readable draft

```yaml
p7_binding_version: "4"
status: "OPEN"
draft_lineage_anchor: "4382a7b745c1abde3a68eb7848611412f5bd34d7"
apparatus_anchor: "2a54a67d84870e4eeb71b8aaf04413e0ca492ba1"
p35_boundary: "643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d"
control_state_anchor: "89be386b136aeb5f1fc5ca39d4aac4b3781a9f58"
candidate_sha: "7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8"
candidate_tree_sha: "586c00d6dedb589e52108279f9759be3c4f927e1"
deployment_id: "dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA"
protocol_version: "0.7.5"
protocol_blob_sha: null
protocol_content_sha256: null
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
p4_procedure: "docs/governance/P4_INDEPENDENT_BLINDING_CUSTODY_PROCEDURE.md"
p4_custody_mode: null
p4_custody_instance_id: null
p4_custody_authority_id: null
p4_execution_principal_id: null
p4_key_commitment_sha256: null
p4_mapping_commitment_sha256: null
p4_control_path_inventory_digest: null
p4_no_unilateral_access_evidence: null
p4_independent_review_evidence: null
final_control_plane_commit: null
selected_p9_verifier_script_sha256: null
selected_p9_workflow_sha256: null
downstream_outputs:
  freeze_commit_sha: null
  freeze_sha256: null
  p8_verification_commit_sha: null
  p8_verification_sha256: null
  p9_final_evidence: null
  pilot_authorization: null
empirical_n: 0
```

## Explicit non-claims

This draft does not close P4, P7, P8, or P9; instantiate a custody mode; create a freeze; authorize a pilot or unblinding; convert deployment/CI/synthetic evidence into empirical evidence; or increase empirical N.

**P5: CLOSED / VERIFIED.**  
**P4-A: OPEN / NOT EXECUTED.**  
**P7 remains ADOPTED / FINAL BINDING OPEN.**  
**Freeze: NOT ESTABLISHED.**  
**Pilot authorization: NOT GRANTED.**  
**Empirical N: 0.**
