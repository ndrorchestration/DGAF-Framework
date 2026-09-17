---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-09-17
current_protected_main: b1d91621bd73e70866d5ff8fd38fb98e440b30e9
canonical_high_assurance_empirical_n: 0
final_candidate_status: NOT_DESIGNATED
candidate_status: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED
canonical_dgaf_efficacy: NOT_ESTABLISHED
track_a_epoch_001_collection: COMPLETE_BLINDED_RETAINED
track_a_epoch_001_primary_analysis: UNANALYZABLE_NOT_RUN
track_a_successor_collection: COMPLETE_50_PAIRED_SEED_UNITS_2250_BLINDED_OBSERVATIONS
track_a_successor_dataset_lock: ESTABLISHED
track_a_successor_unblinding: AUTHORIZED_BOUNDED_MAPPING_RELEASE_OR_DECRYPTION_ONLY
track_a_successor_materialization_tooling: ACCEPTED
track_a_successor_materialization: NOT_ESTABLISHED
track_a_successor_primary_analysis_authorization_tooling: ACCEPTED
track_a_successor_primary_analysis: NOT_AUTHORIZED_NOT_RUN
accepted_decision_frontier_pr: 776
accepted_governance_map_pr: 779
accepted_audit_catalog_pr: 780
accepted_workflow_coverage_scanner_pr: 782
accepted_assurance_catalog_expansion_pr: 785
accepted_state_space_explorer_pr: 783
assurance_catalog_coverage: PARTIAL_CORE_FAMILIES_ONLY
---

# DGAF-Framework / PDMAL — Current State

This file is the **primary current-facing repository summary**. GitHub is authoritative for source, CI, immutable evidence identities, issues, and merge history. Runtime/deployment providers remain authoritative for runtime facts. The DGAF Operational Control Center in Notion is the interpreted governance/control-plane mirror. Historical records remain authoritative only for the exact scope, identity, and time they bind.

## Executive boundary

| Area | Current state |
|---|---|
| Protected repository `main` | **`b1d91621bd73e70866d5ff8fd38fb98e440b30e9`** |
| Canonical High-Assurance program | **PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / AUTHORIZATION NOT GRANTED / N=0** |
| Canonical DGAF efficacy | **NOT ESTABLISHED** |
| Independent validation | **NOT ESTABLISHED** |
| Track A Epoch 001 | **COLLECTION COMPLETE / DATASET LOCKED / PROTECTED MAPPING CRYPTOGRAPHICALLY UNRECOVERABLE / PRIMARY ANALYSIS UNANALYZABLE-NOT-RUN** |
| Track A Epoch 002 collection | **COMPLETE · 50 PAIRED SEED UNITS / 2,250 BLINDED OBSERVATIONS** |
| Epoch 002 dataset lock | **ESTABLISHED** |
| Epoch 002 bounded unblinding | **AUTHORIZED · CONTROLLED MAPPING RELEASE OR DECRYPTION ONLY** |
| Epoch 002 materialization tooling | **ACCEPTED** |
| Epoch 002 real materialization | **NOT ESTABLISHED** |
| Epoch 002 immutable materialization receipt | **NOT ESTABLISHED** |
| Epoch 002 primary analysis | **NOT AUTHORIZED / NOT RUN** |
| Decision Frontier | **ACCEPTED PRESENTATION-ONLY SOURCE STATE · PR #776** |
| Governance Map | **ACCEPTED PRESENTATION-ONLY SOURCE STATE · PR #779** |
| State-Space Explorer V0 | **ACCEPTED PRESENTATION-ONLY DISCRETE/CATEGORICAL SOURCE STATE · PR #783** |
| Repository assurance catalog | **ACCEPTED · PARTIAL_CORE_FAMILIES_ONLY** |
| Workflow coverage-gap scanner | **ACCEPTED · PR #782** |
| Expanded recurring assurance mappings | **ACCEPTED · PR #785** |

No row above establishes integrated DGAF efficacy, independent validation, successful/current deployment, production certification, High-Assurance authorization, or a completed successor Track A primary result.

## Protected-main repository sequence

Current protected `main` is signed/verified commit `b1d91621bd73e70866d5ff8fd38fb98e440b30e9`, produced by **PR #783 — State-Space Explorer V0** after the accepted interface and assurance-inventory sequence below.

### Semantic Control Field / presentation state

The Governance Command Center now has three accepted presentation-only tranches:

1. **PR #776 — Decision Frontier** (`3777b66277135a31da496661e0cb12e87cb05e3c`): presents current governed state, evidence/provenance, blocking boundary, nearest admissible transition, unreachable transitions, consequence preview, and receipt semantics from the canonical governance model.
2. **PR #779 — Governance Map** (`29a7467b24e6709342874a048dd75b674a090463`): projects ordered vertical escalation, explicitly named lateral relationships, and global field conditions without introducing a second state engine or readiness score.
3. **PR #783 — State-Space Explorer V0** (`b1d91621bd73e70866d5ff8fd38fb98e440b30e9`): projects canonical governance stages into discrete `established`, `frontier`, and `blocked_by_predecessor` reachability regions. Native predicate state remains separate from derived reachability. V0 explicitly does **not** establish continuous/manifold coordinates, readiness distance, authorization probability, scalar evidence quality, efficacy gradients, or inferred consequence/reversibility values.

These interfaces are explanatory projections. They do not create governance authority, grant permission, establish runtime health, or upgrade scientific/empirical evidence.

### Repository assurance inventory

- **PR #780** established `registry/audit_catalog.v1.json` plus deterministic validation with `coverage.status = PARTIAL_CORE_FAMILIES_ONLY`.
- **PR #782** added deterministic discovery of current `.github/workflows/*.yml|*.yaml` definitions not exactly bound by accepted catalog `implementation` paths.
- **PR #785** added seven source-verified recurring assurance families while explicitly preserving partial coverage.
- **PR #784** was closed unmerged and remains test-first/stale-lineage provenance only; its proposed workflow-role census is **not accepted current implementation**.

Current protected-main required status contexts are separately read as **PPTL CI**, **Governance CI**, and **PR Issue-State Keyword Guard**. Catalog membership is not branch-protection requiredness. `UNMAPPED` / `UNCLASSIFIED` means the assurance role has not yet been adjudicated; it is not evidence that a workflow is non-assurance.

Known assurance-inventory gaps remain: exhaustive remaining workflow/script/test/method classification, exact job/workflow/ruleset requiredness, shared-dependency and independence analysis, external-runtime ingress assurance, presentation-projection assurance, and historical family-versus-execution-instance reconciliation.

## Track A Epoch 002 — controlling scientific lane

Issue #523 controls the successor prospective topology-robustness experiment. The accepted design remains:

- 50 prospective seeds: `20270201..20270250`;
- 5 topologies: ring, PDMAL, random-regular, small-world, complete;
- 9 failure counts: `0, 1, 2, 3, 4, 5, 6, 8, 10`;
- 45 blinded cells per seed / 2,250 raw observations;
- algorithm: `REFERENCE_NEIGHBOR_MEAN_ALPHA_0_5_V1`;
- primary endpoint: strict-boolean `ffcr_success`;
- inferential unit: paired seed;
- locked paired bootstrap: 10,000 resamples;
- analysis seed: `20270251`.

### Accepted evidence boundary

The successor collection is complete at **50 paired seed units / 2,250 blinded observations**. A content-addressed Epoch 002 `DATASET_LOCK_RECEIPT` is accepted with `status=PASS`. A separate accepted `UNBLINDING_DECISION_RECORD` has `status=PASS` and scope **`CONTROLLED_MAPPING_RELEASE_OR_DECRYPTION_ONLY`**.

Those records do not establish real materialization, primary-analysis authority, a scientific result, efficacy, independent validation, or High-Assurance authorization.

### Accepted materialization and authorization tooling

- **PR #713** accepted the controlled Stage-1 materializer with exact-member validation and fail-closed handling for wrong keys, archive drift, duplicate entries, traversal/link hazards, and unexpected members.
- **PR #715** accepted the non-secret Stage-2 evidence bundle with deterministic content-addressed identities and atomic publication only after validation.
- **PR #728** accepted prospective primary-analysis authorization validation/procedure/CI/test tooling.

No accepted record establishes that the real retained Epoch 002 material was materialized, admitted, or analyzed.

## Current scientific frontier

The next admissible scientific transition remains:

`controlled operator-side real materialization`
`→ validated non-secret materialization evidence admission`
`→ separate immutable materialization receipt`
`→ separate primary-analysis authorization`
`→ locked primary analysis`
`→ interpretation / adjudication`

Current controlling predicates:

- `TRACK_A_EPOCH_002_COLLECTION = COMPLETE`
- `TRACK_A_EPOCH_002_DATASET_LOCK = ESTABLISHED`
- `TRACK_A_EPOCH_002_UNBLINDING = AUTHORIZED / BOUNDED`
- `TRACK_A_EPOCH_002_MATERIALIZATION_TOOLING = ACCEPTED`
- `TRACK_A_EPOCH_002_PRIMARY_ANALYSIS_AUTHORIZATION_TOOLING = ACCEPTED / TOOLING ONLY`
- `TRACK_A_EPOCH_002_MATERIALIZATION = NOT_ESTABLISHED`
- `TRACK_A_EPOCH_002_MATERIALIZATION_RECEIPT = NOT_ESTABLISHED`
- `TRACK_A_EPOCH_002_PRIMARY_ANALYSIS = NOT_AUTHORIZED / NOT RUN`
- `SCIENTIFIC_N_INCREMENT = 0`
- `CANONICAL_DGAF_EFFICACY = NOT_ESTABLISHED`
- `INDEPENDENT_VALIDATION = NOT_ESTABLISHED`
- `HIGH_ASSURANCE = PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0`

Private keys, passphrases, encrypted backup copies, blinding secrets, protected plaintext mappings, and other recoverable secret material remain prohibited from GitHub, Notion, chat, CI inputs, workflow logs, and committed files.

## Track A Epoch 001 — immutable historical boundary

Epoch 001 remains valid evidence that a prospective blinded panel was collected and retained under its exact frozen protocol: 50 paired inferential seed units / 2,250 blinded observations, dataset lock established, historical unblinding authorization established, protected mapping cryptographically unrecoverable, primary analysis unanalyzable/not run, outcome aggregation not performed.

The retained protected mapping must not be guessed, regenerated, or reconstructed. Epoch 001 is not pooled into the successor confirmatory analysis.

## Canonical High-Assurance provenance boundary

Repository recency does not redefine the historical High-Assurance apparatus/candidate/runtime identities:

- apparatus source: `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`
- apparatus source tree: `973c92335caf84f37fc2b3c4df6dd83b3b855087`;
- historical runtime-evidence candidate identity: `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`;
- historical runtime deployment identity: `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA`;
- final v0.7.6 High-Assurance candidate: **NOT DESIGNATED**.

The canonical High-Assurance program therefore remains **PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / AUTHORIZATION NOT GRANTED / N=0**.

## Evidence and authority rules

Current-facing documentation must preserve these distinctions:

1. Architecture is not implementation.
2. Implementation is not empirical evidence.
3. A passing test proves only its defined predicate and environment.
4. Developer self-verification is not independent verification.
5. Freeze is not authorization; authorization is not execution.
6. Collection is not dataset lock; dataset lock is not unblinding authorization.
7. Unblinding authorization is not materialization.
8. Materialization is not primary-analysis authorization.
9. Primary-analysis authorization is not a positive result.
10. Historical exact-scope evidence does not silently bind a later candidate, epoch, deployment, or apparatus.
11. UI projection is not governance authority.
12. Source verification is not deployment/runtime health.
13. Catalog membership is not branch-protection requiredness.
14. `UNMAPPED` / `UNCLASSIFIED` is a fail-closed inventory state, not a negative assurance judgment.
15. Discrete State-Space reachability is not continuous distance, probability, confidence, efficacy, consequence, or reversibility geometry.

## Current documentation routing

- **Primary live repository state:** this file.
- **Compatibility status entrypoint:** [`PROJECT_STATUS.md`](PROJECT_STATUS.md).
- **Public overview:** [`../README.md`](../README.md).
- **Technical implementation map:** [`../README.technical.md`](../README.technical.md).
- **Governance / standards crosswalk:** [`../README.governance.md`](../README.governance.md).
- **Public terminology:** [`PUBLIC_TRANSLATION_LAYER.md`](PUBLIC_TRANSLATION_LAYER.md).
- **Historical/provenance index:** [`HISTORICAL_RECORDS_INDEX.md`](HISTORICAL_RECORDS_INDEX.md).

No documentation update can itself promote scientific N, custody acceptance, freeze, authorization, independent verification, efficacy, deployment health, or High-Assurance status.
