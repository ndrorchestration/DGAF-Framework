# DGAF/PDMAL Project Status

> **Current-status entrypoint:** use [`CURRENT_STATE.md`](CURRENT_STATE.md) for the live repository/evidence boundary.

This path is retained for compatibility and is not an independent current-state authority. Historical snapshots remain under `docs/historical/` and must not be read as live state unless explicitly promoted by a later governing record.

For public terminology and industry-neutral explanations of DGAF-specific names, use [`PUBLIC_TRANSLATION_LAYER.md`](PUBLIC_TRANSLATION_LAYER.md).

## Current hard boundary

As of the 2026-09-17 protected-main reconciliation through commit `b1d91621bd73e70866d5ff8fd38fb98e440b30e9`:

- canonical High-Assurance program: **PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / AUTHORIZATION NOT GRANTED / N=0**;
- canonical DGAF efficacy: **NOT ESTABLISHED**;
- independent validation: **NOT ESTABLISHED**;
- Track A Epoch 001: **COMPLETE / BLINDED / DATASET LOCKED / CRYPTOGRAPHICALLY UNRECOVERABLE FOR PRIMARY ANALYSIS**;
- Track A Epoch 002 repository custody: **ACCEPTED / SAME_SYSTEM_NONINDEPENDENT**;
- Track A Epoch 002 immutable freeze, final closure, and bounded verification classification: **ACCEPTED**;
- Track A Epoch 002 collection authorization: **ACCEPTED** at commit `563152fdb254b8ee948a693c287126a8bf8314b8`;
- Track A Epoch 002 collection: **COMPLETE** at 50 paired seed units / 2,250 blinded observations;
- successor dataset lock: **ESTABLISHED** through an accepted PASS `DATASET_LOCK_RECEIPT`;
- successor bounded unblinding: **AUTHORIZED** for `CONTROLLED_MAPPING_RELEASE_OR_DECRYPTION_ONLY`;
- successor materialization tooling: **ACCEPTED**, including Stage-1 PR #713 and Stage-2 operator bundle PR #715;
- successor prospective primary-analysis authorization tooling: **ACCEPTED / TOOLING ONLY** through PR #728;
- successor real materialization: **NOT ESTABLISHED**;
- successor materialization receipt: **NOT ESTABLISHED**;
- successor primary-analysis authorization event: **NOT ESTABLISHED**;
- successor primary analysis: **NOT AUTHORIZED / NOT RUN**;
- scientific-N increment: **0**.

The accepted dataset-lock, bounded-unblinding, materialization-tooling, and primary-analysis-authorization-tooling records preserve separate event boundaries. They do not establish real materialization, a materialization receipt, primary-analysis authorization, efficacy, independent validation, or High-Assurance authorization.

## Accepted repository presentation state

The Governance Command Center now contains three accepted presentation-only Semantic Control Field tranches on protected `main`:

1. **Decision Frontier — PR #776**, merged as `3777b66277135a31da496661e0cb12e87cb05e3c`. It presents current governed state, evidence/provenance, blocking boundary, nearest admissible transition, unreachable transitions, consequence preview, and receipt semantics from the existing normalized governance model.
2. **Governance Map — PR #779**, merged as `29a7467b24e6709342874a048dd75b674a090463`. It projects vertical escalation from canonical governance stages, explicit lateral relationships, and global field constraints without creating a second state engine or readiness score.
3. **State-Space Explorer V0 — PR #783**, merged as `b1d91621bd73e70866d5ff8fd38fb98e440b30e9`. It projects canonical lifecycle stages into discrete categorical `established`, `frontier`, and `blocked_by_predecessor` regions while preserving each stage's native predicate state and explicit model limits.

These interfaces are explanatory projections. They do not create governance authority, authorize actions, establish deployment health, change scientific state, or promote empirical support.

State-Space Explorer V0 does **not** establish continuous tensor/manifold coordinates, authorization distance, readiness percentages, confidence scores, efficacy gradients, inferred consequence, or inferred reversibility. Consequence and reversibility remain explicitly **NOT MODELED — DO NOT INFER** in V0.

## Accepted repository assurance-inventory state

Protected `main` contains a machine-readable but explicitly partial recurring-assurance inventory:

- **PR #780** introduced `registry/audit_catalog.v1.json` plus deterministic validation and preserved `coverage.status = PARTIAL_CORE_FAMILIES_ONLY`;
- **PR #782** added a workflow coverage-gap scanner that discovers `.github/workflows/*.yml|*.yaml` definitions not exactly bound by the catalog, without inferring that every unmapped workflow is or is not an assurance control;
- **PR #785**, merged as `6b89529da3e7ff13e14eaea415756579d859fb26`, added seven source-verified recurring assurance families while explicitly preserving partial coverage.

Current protected-main required status contexts remain separately read as **PPTL CI**, **Governance CI**, and **PR Issue-State Keyword Guard**. Catalog membership does not mean a workflow is a required branch-protection context, and non-membership means only **UNMAPPED / UNCLASSIFIED pending adjudication**, not “non-assurance.”

Known assurance-inventory gaps remain: wider workflow/script/test classification, exact job/workflow/ruleset mapping, shared-dependency and independence analysis, external-runtime ingress assurance, presentation-projection coverage, and historical family-versus-execution-instance reconciliation.

## Next admissible scientific transition

The current scientific frontier is still **controlled operator-side materialization of the real retained Epoch 002 evidence**, followed by bounded evidence admission and a separate immutable materialization receipt.

The accepted apparatus provides:

1. a controlled operator-side Stage-1 materializer with wrong-key/archive-drift and unsafe-archive fail-closed behavior;
2. a non-secret Stage-2 evidence-bundle wrapper that records content-addressed identities without custody secrets;
3. atomic publication of the complete materialization bundle only after validation;
4. a prospective, read-only primary-analysis authorization gate that can validate a future exact authorization event only after an accepted immutable materialization receipt exists;
5. explicit preservation of `PRIMARY_ANALYSIS_AUTHORIZATION=NOT_ESTABLISHED`, `PRIMARY_ANALYSIS=NOT_AUTHORIZED_NOT_RUN`, scientific-N increment 0, and canonical efficacy `NOT_ESTABLISHED`.

Do not place private keys, passphrases, protected plaintext mappings, or other recoverable secret material in GitHub, Notion, chat, CI inputs, workflow logs, or committed files. Do not create a positive primary-analysis authorization event until a real materialization has been admitted and its immutable receipt has been accepted. Do not run primary analysis until that separate authorization event is itself accepted.

## Presentation boundary

The DGAF Governance Command Center and ORBIT/Evidence Observer surfaces are read-only or presentation-layer companions to repository truth. They may expose current state, evidence, blockers, reachability, provenance, and runtime freshness, but they are not independent governance authorities and cannot upgrade evidence or scientific state.

A deployment being READY, unavailable, stale, quota-blocked, or otherwise operationally healthy/unhealthy is a separate dimension from source verification, governance authority, experimental authorization, and empirical support.
