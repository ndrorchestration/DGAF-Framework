# P4 Mode T — Confidential Space prelaunch contract

Date: 2026-09-06  
Issue: #310  
Status: **PREDECLARATION / SYNTHETIC VALIDATION ONLY / NO GCP ACTION EXECUTED**

Controlling state remains **PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N=0**.

## Purpose

The next real Mode-T gate requires an authenticated Google Cloud project and a reviewed workload/launch configuration. Before any cloud execution, this tranche makes that launch surface explicit and machine-checkable so the real attempt cannot be assembled ad hoc from mutable flags.

The validator does not authenticate to Google, build/push an image, create a VM, grant IAM, request an attestation token, or execute the pilot.

## Current Google control surface used by this contract

Google's current Confidential Space documentation establishes the controls this contract freezes:

- CPU workloads are launched with an explicit Confidential Computing technology and Shielded Secure Boot;
- production workloads use the `confidential-space` image family rather than `confidential-space-debug`;
- `tee-image-reference` identifies the workload container;
- `tee-restart-policy` supports `Never`, `Always`, and `OnFailure`, with `Never` the required DGAF value;
- `tee-container-log-redirect` can expose stdout/stderr to Cloud Logging or serial console, so DGAF requires it disabled;
- `tee-monitoring-memory-enable` can expose workload memory-usage metrics, so DGAF requires it disabled;
- workload-author launch-policy labels can prevent added capabilities, cgroup mounts, command overrides, environment overrides, mounts, log redirection, and memory monitoring;
- attestation assertions expose the resulting workload image digest, command/environment overrides, restart policy, service accounts, hardware model, monitoring state, production debug state, and support attributes for later reconciliation.

Google currently recommends using the production image's `STABLE` support attribute rather than pinning a Confidential Space OS version number. The latest release notes at review time list Confidential Space image `260701` as available, but this prelaunch contract does not convert that mutable release number into the scientific trust root. The later real token must establish production state and `STABLE` support.

## Fail-closed predeclared contract

`mode_t_confidential_space_launch.py` requires all of the following:

### Workload and run identity

- full candidate commit SHA;
- predeclared freeze digest fixture/identity;
- exact workload container digest `sha256:<hex>`;
- workload image reference pinned with `@sha256:<same digest>`, not `:latest` or another mutable tag;
- exact project, zone, instance name, and workload service account;
- explicit `synthetic_admission_only=true` and `empirical_n=0`.

### Confidential VM substrate

- `confidential_compute_type = TDX`;
- Shielded Secure Boot enabled;
- maintenance policy `TERMINATE`;
- production `confidential-space` image family;
- GCE automatic restart disabled;
- disposable synthetic-admission VM intent recorded.

### Operator metadata

The only permitted Confidential Space metadata keys are:

- exact digest-pinned `tee-image-reference`;
- `tee-restart-policy=Never`;
- `tee-container-log-redirect=false`;
- `tee-monitoring-memory-enable=false`.

The contract rejects `tee-cmd`, all `tee-env-*`, added capabilities, cgroup namespace, mounts, service-account impersonation metadata, GPU-driver installation, Intel Trust Authority API fields, and any otherwise unreviewed metadata key.

The first admission remains explicitly on **Google Cloud Attestation**, matching the #313 signing-key trust path; alternate attestation providers are outside this tranche.

### Workload-author launch policies

The workload image must later be independently shown to carry this exact fail-closed policy set:

```text
tee.launch_policy.allow_capabilities=false
tee.launch_policy.allow_cgroups=false
tee.launch_policy.allow_cmd_override=false
tee.launch_policy.allow_env_override=
tee.launch_policy.allow_mount_destinations=
tee.launch_policy.log_redirect=never
tee.launch_policy.monitoring_memory_allow=never
```

The empty allowlists are deliberate: no operator environment or mount override is admitted for the first attempt.

## Evidence produced by validation

A passing local/CI contract produces a canonical launch-contract SHA-256 over the normalized declaration and retains:

- exact project/zone/instance/service-account declaration;
- candidate and freeze identities;
- digest-pinned workload reference;
- TDX/Secure Boot/production-image requirements;
- exact metadata and launch-policy sets;
- explicit synthetic-only / N=0 state.

It also explicitly records:

- `real_gcp_configuration_verified=false`;
- `real_confidential_space_admission=false`;
- `freeze_established=false`;
- `pilot_authorized=false`;
- `empirical_n=0`.

Therefore `PASS_PREDECLARED_ONLY` means only that a proposed launch declaration is internally consistent with the reviewed contract.

## Required real-admission reconciliation

Before any future Mode-T PASS can rely on this declaration, an authenticated real run must independently prove at least:

1. the actual GCP project/zone/VM/service account correspond to the reviewed declaration;
2. the resolved workload image digest equals the predeclared digest;
3. the workload image actually contains the reviewed launch-policy labels;
4. the Confidential Space image is production with `dbgstat=disabled-since-boot` and `STABLE` support;
5. hardware attests TDX and Secure Boot;
6. restart policy attests exactly `Never`;
7. command override is empty;
8. environment overrides are empty and explicit environment equals the frozen non-secret run inputs;
9. memory monitoring is false;
10. no log/diagnostic surface contains protected key, mapping, or plaintext;
11. the real PRE token binds C and is signature/key-source verified through #313/#314;
12. the real POST token binds the exact final output/evidence manifest;
13. both real tokens and the launch evidence are independently retrieved and reverified.

## Remaining blocker

This tranche removes ambiguity from the launch configuration but cannot satisfy the authenticated-project requirement. A real GCP project, image build/review, workload-service-account setup, VM creation, token retrieval, and independent evidence review remain **NOT EXECUTED** here.

**P4 remains OPEN / PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N=0.**
