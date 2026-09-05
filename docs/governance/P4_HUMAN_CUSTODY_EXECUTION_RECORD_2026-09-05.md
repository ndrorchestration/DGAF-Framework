# P4 Human Custody Execution Record — Pre-Filled Handoff

**Status:** OPEN / NOT EXECUTED / FAIL-CLOSED  
**Control-plane base:** `d317d1957d3e6725cffc4f07a846d933f43485c1`  
**Purpose:** Provide a single operational record for performing the already-defined P4 human/key custody procedure without inferring or fabricating human participation, secret material, commitments, freeze state, authorization, or empirical execution.

This record does not replace `docs/governance/P4_HUMAN_KEY_CUSTODY_PROCEDURE.md`. The procedure remains authoritative. This file is only an execution instance whose unresolved fields must remain null until the corresponding real-world event occurs and is evidenced.

## Pre-bound experiment identities

| Field | Value | State |
|---|---|---|
| Experiment ID | `PDMAL-PILOT-V1` | SELECTED |
| Corrected apparatus source | `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1` | KNOWN |
| Immutable P-35 validation boundary | `643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d` | KNOWN |
| Designated runtime candidate | `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8` | VERIFIED |
| Runtime candidate tree | `586c00d6dedb589e52108279f9759be3c4f927e1` | VERIFIED |
| Candidate production deployment | `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA` | VERIFIED FOR CANDIDATE |
| Protocol version | `0.7.5` | SELECTED / PRE-FREEZE |
| Analysis implementation blob | `a269ed226b1d261663994fc3ef0e8a1a96da6cd3` | BOUND |
| Analysis configuration SHA-256 | `6cab3f1ed6d4e040141598d293628dbab52442234c519b3e231b76a2896f09a8` | BOUND |
| Pilot runner blob | `b5152fa3c9c4effe1c5201a45d58ac2d6b8e5243` | BOUND |
| Pilot artifact schema blob | `c620d3755a645c5f2ad14124f42ce07a1c670c5f` | BOUND |
| P5 closure reconciliation | `fcf21ce9ab3739a7b5880c6f6896cf378a3dd2da` | CLOSED / VERIFIED |
| P7 binding control-plane merge | `d317d1957d3e6725cffc4f07a846d933f43485c1` | ADOPTED / FINAL BINDING OPEN |

These identities are pre-bound repository facts only. They do not establish that P4 has been executed.

## Required real-world assignments

The following fields must be completed only by attributable real humans participating in the custody procedure.

| Field | Required value | Current state |
|---|---|---|
| Key Custodian identity | attributable human identity | `null` / NOT EXECUTED |
| Execution principal identity | distinct attributable human identity | `null` / NOT EXECUTED |
| Analyst / verifier identity | attributable human identity, if separate | `null` / NOT EXECUTED |
| Custody assignment timestamp | RFC3339 with timezone | `null` / NOT EXECUTED |
| Storage class | non-secret description | `null` / NOT EXECUTED |
| Key generation method class | non-secret description | `null` / NOT EXECUTED |

The Key Custodian and execution/analysis principal must be genuinely distinct humans. Strings, accounts, agents, bots, pseudonymous duplicates, or AI personas do not satisfy this requirement by themselves.

## Secret material and commitment fields

The raw blinding key, cleartext mapping before authorized unblinding, and unreleased commitment nonces must never be entered into this file, GitHub issues, pull-request text, logs, or public artifacts.

The only pre-execution public cryptographic values permitted here are the commitment digests produced by the authoritative P4 procedure:

- `key_commitment_sha256 = SHA256(b"DGAF-P4-KEY-v1\x00" || key_commitment_nonce || raw_blinding_key)`
- `mapping_commitment_sha256 = SHA256(b"DGAF-P4-MAP-v1\x00" || mapping_commitment_nonce || canonical_mapping_bytes)`

| Field | Required value | Current state |
|---|---|---|
| Key commitment SHA-256 | 64-hex digest | `null` / NOT EXECUTED |
| Mapping commitment SHA-256 | 64-hex digest | `null` / NOT EXECUTED |
| Commitment scheme | `sha256-domain-separated-secret-nonce-v1` | PREDECLARED |

## Required attributable attestations

P4 remains open until all required operational evidence exists and can be independently reviewed.

### Key Custodian attestation

`null / NOT EXECUTED`

Must attest, at minimum:

- identity and role;
- custody assignment time;
- association with the exact experiment/candidate above;
- key-generation method class without revealing the key;
- published key and mapping commitment digests;
- storage class;
- who had access to the key, mapping, and commitment nonces;
- commitment not to disclose them to the execution/analysis principal before authorized release.

### Execution / analysis principal no-access attestation

`null / NOT EXECUTED`

Must attest, at minimum:

- identity and role;
- distinctness from the Key Custodian;
- no possession of the raw key, cleartext mapping, or commitment nonces during the blinded period;
- agreement not to seek or infer the cleartext mapping before authorized unblinding.

### Independent custody review

`null / NOT EXECUTED`

Must establish that the role split, timestamps, commitments, access statements, and evidence packet satisfy the authoritative P4 procedure without revealing secret material.

## Ordering gates

The following sequence remains mandatory and fail-closed:

1. P4 real human roles assigned and commitments published.
2. P4 custody evidence independently reviewed.
3. P7 final exact binding completed using actual P4 custody evidence.
4. P8 immutable freeze constructed.
5. Freeze independently verified.
6. P9 independent final-chain verification completed.
7. Separate pilot authorization granted.
8. Only then may blinded empirical execution begin.

No later step may be marked complete merely because this execution record exists.

## Machine-readable execution state

```yaml
p4_custody_version: "1"
record_type: "execution-instance"
status: "OPEN"
control_plane_base: "d317d1957d3e6725cffc4f07a846d933f43485c1"
experiment_id: "PDMAL-PILOT-V1"
apparatus_source: "2a54a67d84870e4eeb71b8aaf04413e0ca492ba1"
p35_boundary: "643dc77a56d3b5a92d16981d5d8ca01c3ed5b55d"
candidate_sha: "7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8"
candidate_tree_sha: "586c00d6dedb589e52108279f9759be3c4f927e1"
deployment_id: "dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA"
protocol_version: "0.7.5"
analysis_blob_sha: "a269ed226b1d261663994fc3ef0e8a1a96da6cd3"
analysis_config_sha256: "6cab3f1ed6d4e040141598d293628dbab52442234c519b3e231b76a2896f09a8"
runner_blob_sha: "b5152fa3c9c4effe1c5201a45d58ac2d6b8e5243"
artifact_schema_blob_sha: "c620d3755a645c5f2ad14124f42ce07a1c670c5f"
p5_closure_reconciliation: "fcf21ce9ab3739a7b5880c6f6896cf378a3dd2da"
p7_binding_merge: "d317d1957d3e6725cffc4f07a846d933f43485c1"
commitment_scheme: "sha256-domain-separated-secret-nonce-v1"
key_custodian_id: null
execution_principal_id: null
analyst_principal_id: null
key_commitment_sha256: null
mapping_commitment_sha256: null
custody_assigned_at: null
storage_class: null
key_generation_method_class: null
custodian_attestation: null
execution_no_access_attestation: null
independent_custody_review: null
freeze_id: null
freeze_verified_at: null
p9_final_evidence: null
pilot_authorization_id: null
empirical_execution_started_at: null
unblinding_authorization_id: null
unblinding_released_at: null
empirical_n: 0
```

## Completion rule

This execution record must remain **OPEN / NOT EXECUTED** until attributable real-world custody evidence is added. Repository authors may pre-bind public identities and schema, but must not populate human-role, commitment, access, freeze, authorization, unblinding, or empirical-execution fields by inference.

**P4 real custody: OPEN / NOT EXECUTED.**  
**P7: ADOPTED / FINAL BINDING OPEN.**  
**P8: OPEN / FAIL-CLOSED.**  
**P9: NOT EXECUTED.**  
**Freeze: NOT ESTABLISHED.**  
**Pilot authorization: NOT GRANTED.**  
**Empirical N: 0.**
