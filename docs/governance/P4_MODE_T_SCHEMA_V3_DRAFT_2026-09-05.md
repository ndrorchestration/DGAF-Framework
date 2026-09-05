# P4 Custody Schema v3 Draft — Mode T Lifecycle Extension

**Status:** DRAFT / NOT CANONICAL / NOT EXECUTED  
**Issue:** #287  
**Purpose:** Design a mode-specific schema extension that permits zero-human Mode T secret instantiation after authorization without weakening Mode H or Mode I pre-freeze requirements.

## Non-regression rule

Schema v3 is additive in scientific meaning.

- Mode H retains the current v2 requirement that the real protected material and nonce-hardened key/mapping commitments exist before P4-A closure, P7, and freeze.
- Mode I retains the same current v2 pre-freeze commitment requirement.
- Only Mode T may use the mechanism-first lifecycle defined here, and only when its pre-freeze evidence proves the independently enforced mechanism contract.

A Mode H/I record must never use Mode T null-secret fields to bypass existing requirements.

## Pre-freeze common envelope

```yaml
p4_custody_version: "3-draft"
record_type: "execution-instance"
experiment_id: "PDMAL-PILOT-V1"
custody_mode: null  # H | I | T
custody_instance_id: null
execution_principal_id: null
custody_authority_id: null
protected_material_scope_sha256: null
control_path_inventory_sha256: null
no_unilateral_access_evidence_sha256: null
independent_review_evidence_sha256: null
mode_evidence_sha256: null
release_rule: null
release_rule_committed_at: null
p4_pre_freeze_status: "OPEN"
```

## Mode H/I pre-freeze extension — unchanged scientific requirement

```yaml
p4_pre_freeze_class: "instantiated-custody"
commitment_scheme: "sha256-domain-separated-secret-nonce-v1"
key_commitment_sha256: null      # REQUIRED before closure
mapping_commitment_sha256: null  # REQUIRED before closure
custody_assigned_at: null        # REQUIRED before closure
secret_instantiation_status: "INSTANTIATED"
```

P4-A H/I closure remains impossible while either commitment is null.

## Mode T pre-freeze extension

```yaml
p4_pre_freeze_class: "mechanism"
key_commitment_sha256: null
mapping_commitment_sha256: null
secret_instantiation_status: "NOT_EXECUTED"
mode_t:
  mechanism_version: null
  runner_class: "github-hosted-standard-vm"
  runner_contract_sha256: null
  workflow_sha256: null
  helper_sha256: null
  helper_supply_chain_sha256: null
  timelock_client_version: null
  timelock_client_sha256: null
  timelock_chain_hash: "52db9ba70e0cc0f6eaf7803dd07447a1f5477735fd3f661792ba94600c84e971"
  timelock_chain_public_key_sha256: null
  timelock_round_policy_sha256: null
  minimum_release_margin_seconds: null
  analysis_lock_policy_sha256: null
  rerun_policy_sha256: null
  no_secret_output_contract_sha256: null
  p6_retention_contract_sha256: null
  transparency_contract_sha256: null
  live_runner_memory_access_disposition: "UNKNOWN"
```

Mode T pre-freeze closure is **MECHANISM VERIFIED / SECRET NOT YET INSTANTIATED**. It is not equivalent to a closed H/I instantiated-custody record.

## Run-reservation and authorization records

Before P4-T-X can begin, a pre-secret workflow attempt reserves one exact run identity:

```yaml
record_type: "PDMAL_MODE_T_RUN_RESERVATION"
freeze_commit_sha: null
freeze_sha256: null
workflow_sha256: null
github_run_id: null
github_run_attempt: 1
github_sha: null
reserved_at_server_time: null
reservation_evidence_sha256: null
transparency_bundle_sha256: null
p6_archive_identity: null
```

Separate authorization then binds that exact reservation:

```yaml
record_type: "PDMAL_PILOT_AUTHORIZATION"
status: "GRANTED"
freeze_commit_sha: null
freeze_sha256: null
reservation_evidence_sha256: null
github_run_id: null
allowed_run_attempt: 1
authorization_id: null
authorized_at: null
authorization_record_sha256: null
```

The execution workflow must fail before secret generation unless both records match the frozen tuple exactly.

## Single-use authorization-consumption record

After the reserved run verifies the exact authorization and **before** any key, mapping, or commitment nonce exists, it must create and independently retain:

```yaml
record_type: "PDMAL_MODE_T_AUTHORIZATION_CONSUMPTION"
status: "CONSUMED_PRE_SECRET"
freeze_sha256: null
reservation_evidence_sha256: null
authorization_record_sha256: null
authorization_id: null
github_run_id: null
github_run_attempt: 1
secret_instantiation_status: "NOT_EXECUTED"
consumption_evidence_sha256: null
transparency_bundle_sha256: null
p6_archive_identity: null
```

One authorization may correspond to at most one accepted consumption record. Once this record exists, the authorization is consumed even if the run later crashes. A second secret-instantiating attempt requires a new custody-instance identity and a new explicit authorization decision; it may not silently reuse the consumed authorization.

This rule prevents a failed post-secret/pre-X run from disappearing into history and being replaced by a second usable execution under the same authorization.

## P4-T-X execution evidence

The first and only accepted consumed authorization emits:

```yaml
record_type: "PDMAL_P4_T_EXECUTION"
status: "COMPLETED_BLINDED"
custody_instance_id: null
github_run_id: null
github_run_attempt: 1
freeze_commit_sha: null
authorization_id: null
consumption_evidence_sha256: null
secret_instantiated_at: null
commitment_scheme: "sha256-domain-separated-secret-nonce-v1"
key_commitment_sha256: null
mapping_commitment_sha256: null
timelock_chain_hash: "52db9ba70e0cc0f6eaf7803dd07447a1f5477735fd3f661792ba94600c84e971"
timelock_release_round: null
timelock_ciphertext_sha256: null
blinded_dataset_sha256: null
leak_scan_status: null
execution_evidence_sha256: null
transparency_bundle_sha256: null
p6_archive_identity: null
```

The record contains no raw key, cleartext mapping, unreleased nonce, recovery seed, or equivalent plaintext recovery material.

## P4-T-L analysis-lock evidence

```yaml
record_type: "PDMAL_P4_T_ANALYSIS_LOCK"
status: "LOCKED_BEFORE_RELEASE"
github_run_id: null
consumption_evidence_sha256: null
blinded_dataset_sha256: null
analysis_blob_sha: null
analysis_config_sha256: null
primary_result_sha256: null
analysis_completed_at_server_time: null
timelock_release_round: null
timelock_release_time: null
ordering_verified: null
analysis_lock_evidence_sha256: null
transparency_bundle_sha256: null
p6_archive_identity: null
```

`ordering_verified` may be true only when independently verifiable transparency evidence places the primary-analysis lock strictly before the release time represented by the frozen drand round policy. A self-asserted payload timestamp is insufficient.

## P4-B post-release continuity evidence

```yaml
record_type: "PDMAL_P4_B_CONTINUITY_AUDIT"
status: null  # PASS | FAIL
custody_instance_id: null
timelock_ciphertext_sha256: null
released_mapping_commitment_nonce_sha256: null
recomputed_mapping_commitment_sha256: null
mapping_commitment_matches: null
key_continuity_checked: null
key_commitment_matches: null
analysis_lock_preceded_release: null
exceptions: []
audit_evidence_sha256: null
```

P4-B never rewrites the historical pre-freeze, consumption, or P4-T-X record.

## Mode-specific P7/P8/P9 consequence

For H/I, final P7/freeze/P9 retain the current v2 requirement to bind real `key_commitment_sha256` and `mapping_commitment_sha256` pre-freeze.

For T, pre-authorization P7/freeze/P9 instead bind the exact mechanism tuple:

- custody mode/instance/authority/execution principal identities;
- control-path, no-unilateral-access, independent-review and mode-evidence digests;
- frozen workflow/helper identities;
- exact timelock client and chain identities;
- round/release-margin policy;
- no-secret-output contract;
- analysis-lock policy;
- rerun/single-use authorization policy;
- P6 independent-retention contract;
- transparency contract;
- `secret_instantiation_status: NOT_EXECUTED`.

Final pre-authorization P9 must reject a Mode T freeze containing a real key/mapping commitment because that would mean protected material was instantiated before the authorized P4-T-X phase under this lifecycle.

## Migration rule

The existing v2 canonical procedure and verifier remain authoritative until a separately reviewed schema migration is implemented and exact-head tests prove:

1. H/I behavior is byte/semantic compatible with the existing scientific requirement;
2. T cannot use H/I fields to bypass mechanism closure;
3. H/I cannot use T null-secret semantics;
4. P9 remains pre-authorization and empirical N=0;
5. one authorization cannot yield more than one accepted consumption/secret-instantiation lineage;
6. no real secret is created by schema/test migration.

**This draft does not alter the canonical P4 procedure, P7 binding, freeze schema, P9 verifier, authorization state, or empirical state.**
