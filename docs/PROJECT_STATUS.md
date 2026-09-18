# DGAF/PDMAL Project Status

> **Current-status entrypoint:** use [`CURRENT_STATE.md`](CURRENT_STATE.md) for the live repository/evidence boundary.

This path is retained for compatibility and is not an independent current-state authority. Historical snapshots remain under `docs/historical/` and must not be read as live state unless explicitly promoted by a later governing record.

For public terminology and industry-neutral explanations of DGAF-specific names, use [`PUBLIC_TRANSLATION_LAYER.md`](PUBLIC_TRANSLATION_LAYER.md).

## Current hard boundary

This 2026-09-18 reconciliation was prepared against protected `main` `037e9e878fb8d9ea7a4658219734158bb5300b1e`. Exact current protected-main identity must be read from Git at use time; this compatibility page does not maintain a self-referential standing SHA.

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
- successor materialization tooling: **ACCEPTED**, with PR #713/#715 retained as predecessor tooling, Stage-1 repaired by #794, Stage 2 rebound by #797, the bounded local operator bridge accepted through #806, the stdio MCP adapter accepted through #809, and the one-command local materialization autopilot accepted through #813;
- successor prospective primary-analysis authorization tooling: **ACCEPTED** through PR #728;
- successor real materialization evidence: **ESTABLISHED / ACCEPTED** through PR #824;
- successor materialization receipt: **ESTABLISHED** through creation-only PR #826;
- successor locked-analysis runner tooling: **ACCEPTED** through PR #831;
- successor primary-analysis authorization event: **ACCEPTED / LOCKED_PRIMARY_ANALYSIS_ONLY** through PR #828;
- successor primary analysis: **AUTHORIZED_BOUNDED / NOT RUN**;
- successor locked-analysis result: **NOT ESTABLISHED**;
- successor result-admission tooling: **ACCEPTED / NON-EXECUTING** through PR #835;
- scientific-N increment: **0**.

These accepted records preserve separate event boundaries. Materialization, its receipt, and bounded primary-analysis authorization are established at their exact scopes; the primary analysis has not run, no locked result has been admitted, and efficacy, independent validation, and High-Assurance authorization remain unestablished.

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

Accepted assurance inventory has since expanded through PRs #789, #791, #792, and #793, including exact mappings for the currently observed protected-main required contexts, core exact-head verification families, provider-neutral external runtime ingress, and Semantic Control Field projection contracts. Coverage remains **PARTIAL_CORE_FAMILIES_ONLY**; catalog membership still does not imply protected-branch requiredness or complete assurance coverage.

## Accepted materialization-tooling repair lineage

### Accepted Stage-1 repair and Stage-2 rebind

- **PR #794** accepted the exact retained public archive's harmless dot-prefixed flat-member representation while preserving both locked archive byte identities and fail-closed rejection of absolute/nested/traversal/link/duplicate/unreadable/unexpected members.
- **PR #797** rebound Stage 2 to accepted Stage-1 commit `cf32a62bbf08a1b8db39709f4989be1be800d64e` and blob `3a825b026423952c2844cb18664eb6395b72fdc1`.
- **PR #806** accepted the bounded local operator bridge.
- **PR #809** accepted the local stdio MCP adapter as transport tooling only.
- **PR #813** accepted the one-command local materialization autopilot, which performs secret-bearing materialization only on the operator machine, prepares exactly one non-secret evidence-admission path, and stops before receipt or primary-analysis authorization.
- PR #824 subsequently admitted the exact non-secret materialization evidence and PR #826 established the creation-only materialization receipt.
- PR #831 accepted the fail-closed local locked-analysis runner; PR #828 accepted the separate bounded authorization event; PR #835 accepted content-addressed result-admission tooling.
- These later events establish materialization/receipt/authorization only at their exact scopes; they do not establish analysis execution, a result, efficacy, independent validation, or High-Assurance authorization.

## Next admissible scientific transition

The current scientific frontier is **local execution of the authorized frozen Epoch 002 primary analysis**. Materialization evidence and receipt are accepted, and the separate bounded authorization event is accepted. Execution must use the accepted fail-closed runner against the retained content-addressed input in the exact locked Python 3.12.0 / NumPy 2.5.1 environment; the resulting local output is then admitted by content address through a separate result-record event before interpretation.

The accepted apparatus now provides:

1. a controlled operator-side Stage-1 materializer with wrong-key/archive-drift and unsafe-archive fail-closed behavior;
2. a non-secret evidence-bundle and immutable receipt chain already accepted for Epoch 002;
3. a bounded human-controlled authorization record with exact scope `LOCKED_PRIMARY_ANALYSIS_ONLY`;
4. a fail-closed local locked-analysis runner bound to the frozen analysis/configuration, exact materialized-input digest, and exact Python 3.12.0 / NumPy 2.5.1 runtime;
5. a separate non-executing result-admission lane that validates and content-addresses the local output without copying numerical outcomes into the repository record;
6. explicit preservation of scientific-N increment 0, canonical efficacy `NOT_ESTABLISHED`, independent validation `NOT_ESTABLISHED`, and High-Assurance `NOT AUTHORIZED`.

Do not place private keys, passphrases, protected plaintext mappings, or other recoverable secret material in GitHub, Notion, chat, CI inputs, workflow logs, or committed files. Do not alter the frozen endpoint, estimand, bootstrap contract, historical pooling boundary, or locked runtime after outcome access. Analysis execution, result admission, and later interpretation remain separate events.

## Presentation boundary

The DGAF Governance Command Center and ORBIT/Evidence Observer surfaces are read-only or presentation-layer companions to repository truth. They may expose current state, evidence, blockers, reachability, provenance, and runtime freshness, but they are not independent governance authorities and cannot upgrade evidence or scientific state.

A deployment being READY, unavailable, stale, quota-blocked, or otherwise operationally healthy/unhealthy is a separate dimension from source verification, governance authority, experimental authorization, and empirical support.
