# P4 Independent Custody Execution Record — Pre-Filled Handoff

**Status:** OPEN / NOT EXECUTED / FAIL-CLOSED  
**Control-plane base:** `2d8a525b3f1717c5675907769615207e5aa59fd5`  
**Related issue:** #285  
**Purpose:** Provide one operational record for instantiating P4 under human, institutional, or independently enforced technical custody without inferring or fabricating independence, secret material, commitments, freeze state, authorization, or empirical execution.

This record is governed by `docs/governance/P4_INDEPENDENT_BLINDING_CUSTODY_PROCEDURE.md`.

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

These identities are repository facts only. They do not establish that P4 has been executed.

## Custody-mode selection

Select exactly one mode only when its real control arrangement exists:

| Mode | Meaning | Current state |
|---|---|---|
| `H` | distinct-human custodian | NOT SELECTED |
| `I` | institutional / third-party custody | NOT SELECTED |
| `T` | independently enforced technical custody | NOT SELECTED |

`custody_mode` remains `null` until an actual mechanism is chosen.

## Required operational assignments

| Field | Required value | Current state |
|---|---|---|
| Custody mode | `H`, `I`, or `T` | `null` / NOT EXECUTED |
| Custody instance ID | unique non-secret identifier | `null` / NOT EXECUTED |
| Execution/analysis principal identity | attributable identity | `null` / NOT EXECUTED |
| Custody authority/system identity | human, institution/service, or technical control identity | `null` / NOT EXECUTED |
| Custody assignment timestamp | RFC3339 with timezone | `null` / NOT EXECUTED |
| Custody system/storage class | non-secret description | `null` / NOT EXECUTED |
| Key generation method class | non-secret description | `null` / NOT EXECUTED |
| Release rule | predeclared non-secret rule | `null` / NOT EXECUTED |
| Release-rule commitment timestamp | RFC3339 with timezone | `null` / NOT EXECUTED |

## Secret-material boundary

The raw blinding key, cleartext mapping before authorized unblinding, unreleased commitment nonces, recovery seeds, backup tokens, and equivalent secret recovery material must never be entered into this file, GitHub issues, pull-request text, ChatGPT, logs, or public artifacts.

Only the following pre-execution public cryptographic values are permitted:

- `key_commitment_sha256`
- `mapping_commitment_sha256`
- non-secret hashes/digests of custody policy/configuration evidence

Commitment scheme:

```text
SHA256(b"DGAF-P4-KEY-v1\x00" || key_commitment_nonce || raw_blinding_key)
SHA256(b"DGAF-P4-MAP-v1\x00" || mapping_commitment_nonce || canonical_mapping_bytes)
```

## Control-path inventory

Before P4-A closure review, enumerate every path by which the execution/analysis principal could potentially recover or alter protected material before release.

Required categories:

- owner/root/admin access;
- IAM/policy modification;
- credential reset/account recovery;
- key export/decrypt/re-encryption;
- backup/restore;
- break-glass/emergency access;
- alternate credentials or service identities;
- local copies/recovery seeds/tokens;
- provider support/recovery paths known to the operator.

### Inventory record

`null / NOT EXECUTED`

The inventory must be retained in non-secret form and assigned a SHA-256 digest or immutable record identity.

## Mode-specific evidence

### Mode H — distinct-human custody

Required only if `custody_mode: H`:

- attributable Key Custodian identity;
- execution/analysis principal is a genuinely distinct human;
- custodian custody/access attestation;
- execution/analysis no-access attestation;
- independent review of role distinctness and access separation.

### Mode I — institutional / third-party custody

Required only if `custody_mode: I`:

- attributable service/organization identity;
- custody and release-policy evidence;
- administrator/recovery/export model;
- evidence that the execution/analysis principal cannot unilaterally alter or bypass that model;
- provider/audit evidence sufficient for independent inspection.

### Mode T — independently enforced technical custody

Required only if `custody_mode: T`:

- exact system/cryptographic mechanism identity;
- access-policy/configuration identity and digest;
- evidence for non-exportability or controlled release, where claimed;
- evidence that the execution/analysis principal lacks owner/admin/recovery/export/break-glass paths capable of defeating the blind;
- independently inspectable or machine-verifiable evidence for the enforcement claim.

A technical mechanism controlled end-to-end by the same analyst remains **NOT INDEPENDENT**.

## Universal P4-A evidence checklist

- [ ] Custody mode selected and justified.
- [ ] Custody instance ID assigned.
- [ ] Execution/analysis principal identified.
- [ ] Custody authority/system identified.
- [ ] Raw key, mapping, nonces, and recovery material held outside analyst access.
- [ ] Key commitment digest published before empirical execution.
- [ ] Mapping commitment digest published before empirical execution.
- [ ] Release rule fixed before empirical execution.
- [ ] Full control-path inventory retained.
- [ ] Evidence supports absence of every unilateral early-recovery path.
- [ ] Independent review evidence retained.
- [ ] No contradictory access record is known.
- [ ] Freeze remains NOT ESTABLISHED.
- [ ] Pilot authorization remains NOT GRANTED.
- [ ] Empirical N remains 0.
- [ ] Unblinding remains NOT EXECUTED.

P4 remains OPEN if any applicable item is missing, contradictory, or supported only by self-assertion.

## Machine-readable execution state

```yaml
p4_custody_version: "2"
record_type: "execution-instance"
status: "OPEN"
control_plane_base: "2d8a525b3f1717c5675907769615207e5aa59fd5"
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
commitment_scheme: "sha256-domain-separated-secret-nonce-v1"
custody_mode: null
custody_instance_id: null
execution_principal_id: null
custody_authority_id: null
custody_system_class: null
key_commitment_sha256: null
mapping_commitment_sha256: null
custody_assigned_at: null
key_generation_method_class: null
release_rule: null
release_rule_committed_at: null
control_path_inventory_digest: null
no_unilateral_access_evidence: null
independent_review_evidence: null
p4a_closed_at: null
freeze_id: null
freeze_verified_at: null
p9_final_evidence: null
pilot_authorization_id: null
empirical_execution_started_at: null
unblinding_authorization_id: null
unblinding_released_at: null
p4b_continuity_audit: null
empirical_n: 0
```

## Completion rule

This execution record remains **OPEN / NOT EXECUTED** until one acceptable custody mode is instantiated and evidence establishes the governing no-unilateral-access invariant.

A human friend is not required. Effective control separation is required.

**P4-A: OPEN / NOT EXECUTED.**  
**P7: ADOPTED / FINAL BINDING OPEN.**  
**P8: OPEN / FAIL-CLOSED.**  
**P9: NOT EXECUTED.**  
**Freeze: NOT ESTABLISHED.**  
**Pilot authorization: NOT GRANTED.**  
**Empirical N: 0.**
