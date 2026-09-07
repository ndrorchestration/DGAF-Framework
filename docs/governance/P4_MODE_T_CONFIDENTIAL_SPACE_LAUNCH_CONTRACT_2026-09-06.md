# P4 Mode T — Confidential Space prelaunch contract

Date: 2026-09-06  
Issues: #310 / #316  
Status: **PREDECLARATION / SYNTHETIC VALIDATION ONLY / NO GCP ACTION EXECUTED**

Controlling state remains **PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N=0**.

## Purpose

The next real Mode-T gate requires an authenticated Google Cloud project and a reviewed workload/launch configuration. Before any cloud execution, this tranche makes that launch surface explicit and machine-checkable so the real attempt cannot be assembled ad hoc from mutable flags.

The validator does not authenticate to Google, build/push an image, create a VM, grant IAM, request an attestation token, or execute the pilot.

This launch declaration is also deliberately distinct from the #316 admission-policy trust root. The exact created-instance subject/selfLink is not known until the instance exists, and a launch-contract digest cannot substitute for independently retained R/A/C authorization evidence.

## Pre-freeze identity semantics

Immutable freeze **F is not an input to P4 qualification or final P4 acceptance**. Freeze F is downstream of final P4 and final P7.

The current `dgaf-mode-t-launch-v1` synthetic validator predates that terminology clarification and carries fixture fields named `candidate_sha` and `freeze_sha256`. In this contract version:

- `candidate_sha` is a synthetic full-commit fixture used to exercise exact identity binding; before Issue #309 designates the final candidate it is not candidate authority;
- `freeze_sha256` is a synthetic pre-freeze fixture identifier only;
- `freeze_sha256` must not be represented as the digest of immutable freeze F because the same validator explicitly emits `freeze_established=false`;
- a future real production launch contract must bind the exact final candidate plus an exact **pre-freeze execution-contract identity**, not a nonexistent future freeze-F digest.

This clarification preserves the existing synthetic test surface without conflating it with the later P8/P9 frozen-chain identity. Before real Stage-B P4 acceptance, the production-facing schema must make the pre-freeze role explicit or otherwise demonstrate an equivalent non-circular binding.

## Current Google control surface used by this contract

The reviewed Confidential Space control surface includes:

- an explicit Confidential Computing technology and Shielded Secure Boot;
- production `confidential-space` rather than debug image family;
- digest-pinned `tee-image-reference` for the workload container;
- `tee-restart-policy=Never` for the DGAF first admission attempt;
- container log redirection disabled;
- memory monitoring disabled;
- workload-author launch policies preventing added capabilities, cgroups, command/environment overrides, mounts, log redirection, and memory monitoring;
- later attestation reconciliation of image/configuration, service-account, hardware, monitoring, debug, restart, and support-state claims.

The scientific trust root is the reviewed immutable workload/run identity and independently verified attestation/authorization lineage, not a mutable Confidential Space OS release number.

## Fail-closed predeclared contract

`mode_t_confidential_space_launch.py` requires:

### Workload and run identity

- full commit SHA fixture for exact source/run binding;
- predeclared 64-hex pre-freeze fixture identity currently carried in the legacy field `freeze_sha256`;
- exact workload container digest `sha256:<hex>`;
- workload image reference pinned with `@sha256:<same digest>`, never a mutable `:latest` reference;
- exact project, zone, instance name, and workload service account;
- explicit `synthetic_admission_only=true` and `empirical_n=0`.

Neither legacy fixture field designates a final candidate or establishes immutable freeze F.

### Confidential VM substrate

- `confidential_compute_type = TDX`;
- Shielded Secure Boot enabled;
- maintenance policy `TERMINATE`;
- production `confidential-space` image family;
- GCE automatic restart disabled;
- disposable synthetic-admission VM intent recorded.

### Operator metadata

Only these Confidential Space metadata keys are admitted:

- exact digest-pinned `tee-image-reference`;
- `tee-restart-policy=Never`;
- `tee-container-log-redirect=false`;
- `tee-monitoring-memory-enable=false`.

The contract rejects `tee-cmd`, all `tee-env-*`, added capabilities, cgroup namespace, mounts, service-account impersonation metadata, GPU-driver installation, Intel Trust Authority API fields, and every otherwise unreviewed metadata key.

The first admission remains on Google Cloud Attestation, matching the #313 signing-key trust path; alternate attestation providers are outside this tranche.

### Workload-author launch policies

The workload image must later be independently shown to carry exactly:

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

A passing local/CI contract produces a canonical launch-contract SHA-256 over the normalized declaration and retains the exact declared project/zone/instance/service account, exact source/run fixture identities, digest-pinned workload, TDX/Secure Boot/production-image requirements, exact metadata and launch policies, and synthetic-only/N=0 state.

It explicitly records:

- `authorization_policy_complete=false`;
- `admission_policy_sha256=null`;
- `instance_subject_resolved=false`;
- `policy_binding_issue=316`;
- `real_gcp_configuration_verified=false`;
- `real_confidential_space_admission=false`;
- `freeze_established=false`;
- `pilot_authorized=false`;
- `empirical_n=0`.

Therefore `PASS_PREDECLARED_ONLY` means only that a proposed synthetic launch declaration is internally consistent with the reviewed launch contract. It does not establish final-candidate or freeze identity.

## Required real-admission reconciliation

Before any future Mode-T PASS can rely on a launch declaration, a real authenticated run must independently prove at least:

1. actual project/zone/VM/service account correspond to the reviewed declaration;
2. resolved workload image digest equals the predeclared digest;
3. workload image actually contains the reviewed launch-policy labels;
4. Confidential Space production state, production debug status, and accepted support attributes;
5. TDX and Secure Boot;
6. restart policy exactly `Never`;
7. empty command override;
8. empty environment override and exact frozen explicit non-secret environment;
9. memory monitoring disabled;
10. no protected material on logs/diagnostic surfaces;
11. independently retained R/A/C evidence binds the exact canonical #316 admission policy including the resolved subject;
12. the real PRE token binds exact C and is signature/key-source verified;
13. the real POST token binds the exact output/evidence manifest; and
14. tokens, launch evidence, policy evidence, and retained records are independently retrieved and reverified.

For a pre-candidate Stage-A qualification run, the record must label itself qualification-only and must not claim final P4 acceptance. After Issue #309 designates the exact final candidate, Stage-B P4 acceptance must bind or rerun the above evidence against that final candidate and an exact pre-freeze execution contract before P7/freeze.

## Remaining blocker

This tranche removes launch-configuration ambiguity but cannot satisfy the authenticated-project or independently retained authorization requirements. Real project setup, image build/review, workload service account, VM creation, token retrieval, independent C/policy retention, and independent evidence review remain **NOT EXECUTED** here.

**P4 remains OPEN / PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N=0.**
