---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-09-15
canonical_high_assurance_empirical_n: 0
final_candidate_status: NOT_DESIGNATED
candidate_status: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED
canonical_dgaf_efficacy: NOT_ESTABLISHED
track_a_epoch_001_collection: COMPLETE_BLINDED_RETAINED
track_a_epoch_001_inferential_seed_units: 50
track_a_epoch_001_blinded_observations: 2250
track_a_epoch_001_dataset_lock: ESTABLISHED
track_a_epoch_001_unblinding_authorization: ESTABLISHED_HISTORICAL
track_a_epoch_001_unblinding_recoverability: CRYPTOGRAPHICALLY_UNRECOVERABLE
track_a_epoch_001_primary_analysis: UNANALYZABLE_NOT_RUN
track_a_successor_issue: 523
track_a_successor_repository_custody_admission: ACCEPTED_SAME_SYSTEM_NONINDEPENDENT
track_a_successor_collection_authorization: ACCEPTED_COMMIT_563152F
track_a_successor_collection: COMPLETE_50_PAIRED_SEED_UNITS_2250_BLINDED_OBSERVATIONS
track_a_successor_dataset_lock: ESTABLISHED
track_a_successor_unblinding: AUTHORIZED_BOUNDED_MAPPING_RELEASE_OR_DECRYPTION_ONLY
track_a_successor_materialization_tooling: ACCEPTED
track_a_successor_materialization: NOT_ESTABLISHED
track_a_successor_primary_analysis: NOT_AUTHORIZED_NOT_RUN
accepted_dataset_lock_tooling_pr: 622
accepted_unblinding_decision_tooling_pr: 627
accepted_stage_1_materializer_pr: 713
accepted_stage_2_operator_materialization_bundle_pr: 715
---

# DGAF-Framework / PDMAL — Current State

This file is the **primary current-facing repository summary**. GitHub is authoritative for implementation, immutable evidence identities, issues, and CI. The DGAF Operational Control Center in Notion is the interpreted governance/control-plane mirror. Historical records are authoritative only for the exact scope, identity, and time they bind.

The canonical High-Assurance program, Track A Epoch 001, and Track A Epoch 002 are separate governance/evidence boundaries. Evidence, authorization, N, verification class, and efficacy do not transfer between them without an explicit governed rule.

## Executive boundary

| Area | Current state |
|---|---|
| Canonical High-Assurance program | **PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / AUTHORIZATION NOT GRANTED / N=0** |
| Canonical DGAF efficacy | **NOT ESTABLISHED** |
| Track A Epoch 001 collection | **COMPLETE / BLINDED / RETAINED** |
| Epoch 001 dataset lock | **ESTABLISHED** |
| Epoch 001 protected mapping recoverability | **CRYPTOGRAPHICALLY UNRECOVERABLE** |
| Epoch 001 primary analysis | **UNANALYZABLE / NOT RUN** |
| Successor Track A lane | **ISSUE #523 OPEN** |
| Epoch 002 repository custody | **ACCEPTED / SAME_SYSTEM_NONINDEPENDENT** |
| Epoch 002 freeze / closure / verification classification | **ACCEPTED** |
| Epoch 002 collection authorization | **ACCEPTED** |
| Epoch 002 collection | **COMPLETE · 50 PAIRED SEED UNITS / 2,250 BLINDED OBSERVATIONS** |
| Epoch 002 dataset lock | **ESTABLISHED** |
| Epoch 002 bounded unblinding | **AUTHORIZED · CONTROLLED MAPPING RELEASE OR DECRYPTION ONLY** |
| Epoch 002 materialization tooling | **ACCEPTED** |
| Epoch 002 real materialization | **NOT ESTABLISHED** |
| Epoch 002 materialization receipt | **NOT ESTABLISHED** |
| Epoch 002 primary analysis | **NOT AUTHORIZED / NOT RUN** |
| Independent validation | **NOT ESTABLISHED** |

No row above establishes integrated DGAF efficacy, independent validation, production certification, High-Assurance authorization, or a completed successor Track A primary result.

## Successor Track A — controlling scientific lane

Issue #523 controls the replacement topology-robustness experiment after the Epoch 001 custody failure. Epoch 002 uses a new protocol identity, fresh seeds, fresh blinding, and recoverable solo custody while preserving the locked endpoint/estimand/matrix semantics.

The accepted Epoch 002 design remains:

- 50 prospective seeds: `20270201..20270250`;
- 5 topologies: ring, PDMAL, random-regular, small-world, complete;
- 9 failure counts: `0, 1, 2, 3, 4, 5, 6, 8, 10`;
- 45 blinded cells per seed / 2,250 raw observations;
- algorithm: `REFERENCE_NEIGHBOR_MEAN_ALPHA_0_5_V1`;
- primary endpoint: strict-boolean `ffcr_success`;
- inferential unit: paired seed;
- locked paired bootstrap: 10,000 resamples;
- Epoch 002 analysis seed: `20270251`.

### Current accepted evidence boundary

The successor collection is complete at **50 paired seed units / 2,250 blinded observations**. The content-addressed Epoch 002 `DATASET_LOCK_RECEIPT` exists on protected `main` with `status=PASS` and explicitly preserves `empirical_n_increment=0`, canonical DGAF efficacy `NOT_ESTABLISHED`, and separate authorization requirements.

A separate accepted `UNBLINDING_DECISION_RECORD` exists with `status=PASS` and scope **`CONTROLLED_MAPPING_RELEASE_OR_DECRYPTION_ONLY`**. That record does not authorize primary analysis and does not promote scientific N, efficacy, independent validation, or High-Assurance state.

### Accepted materialization apparatus

Repository engineering has now crossed the materialization-tooling milestone without performing real materialization:

1. prospective materialization receipt validation/procedure — accepted predecessor tooling;
2. OPERATOR_CODESPACE/content-addressed provenance correction — accepted;
3. controlled Stage-1 unblinded materializer — **PR #713 accepted**;
4. operator-side Stage-2 materialization evidence bundle — **PR #715 accepted**.

PR #713 introduced the controlled operator-side materializer with exact archive-member validation, duplicate-entry rejection, path/link/unexpected-member rejection, wrong-key and archive-drift fail-closed behavior, exclusive output creation, deterministic synthetic coverage, and the explicit source marker `PRIMARY_ANALYSIS=NOT_AUTHORIZED_NOT_RUN`.

PR #715 added the non-secret operator materialization evidence bundle. It binds accepted predecessor identities, emits the deterministic materialized-input digest sidecar plus non-secret manifest/receipt/evidence records, stages the complete five-member bundle before publication, and publishes atomically only after validation. Its exact-head verification completed successfully, including Python 3.10/3.11/3.12 and a Python 3.12 full suite of **928 passed / 4 skipped**.

Neither PR decrypted or admitted the real retained Epoch 002 material as a governed analysis input.

## Current frontier

The next admissible scientific transition is **controlled operator-side materialization of the real retained Epoch 002 evidence, followed by validation/admission and a separate immutable materialization receipt**.

The repository currently contains no canonical `TRACK_A_EPOCH_002_MATERIALIZATION_RECEIPT.json`. Therefore:

- `TRACK_A_EPOCH_002_MATERIALIZATION = NOT_ESTABLISHED`;
- `TRACK_A_EPOCH_002_PRIMARY_ANALYSIS = NOT_AUTHORIZED / NOT_RUN`;
- `SCIENTIFIC_N_INCREMENT = 0`;
- `CANONICAL_DGAF_EFFICACY = NOT_ESTABLISHED`;
- `INDEPENDENT_VALIDATION = NOT_ESTABLISHED`.

Private keys, passphrases, encrypted backup copies, blinding secrets, protected plaintext mappings, and other recoverable secret material remain prohibited from GitHub, Notion, chat, CI inputs, workflow logs, and committed files.

## Ordered successor transition chain

Tooling readiness never skips predecessor state. The governed order is:

`repository custody acceptance — ACCEPTED`
`→ precollection preflight — ACCEPTED`
`→ Epoch 002 immutable freeze — ESTABLISHED`
`→ final closure — ACCEPTED`
`→ bounded verification classification — ACCEPTED / NONINDEPENDENT`
`→ separate collection authorization — ACCEPTED`
`→ empirical collection — COMPLETE`
`→ operator evidence admission / QC — ACCEPTED PREDECESSOR CHAIN`
`→ dataset-lock receipt — ESTABLISHED`
`→ separate bounded unblinding decision — AUTHORIZED`
`→ controlled local materialization — CURRENT FRONTIER / NOT ESTABLISHED`
`→ immutable materialization receipt — NOT ESTABLISHED`
`→ separate primary-analysis authorization — NOT AUTHORIZED`
`→ locked primary analysis — NOT RUN`
`→ interpretation/adjudication — NOT REACHED`

Current predicates:

- `TRACK_A_EPOCH_002_REPOSITORY_CUSTODY = ACCEPTED / SAME_SYSTEM_NONINDEPENDENT`
- `TRACK_A_EPOCH_002_COLLECTION_AUTHORIZATION = ACCEPTED`
- `TRACK_A_EPOCH_002_COLLECTION = COMPLETE`
- `TRACK_A_EPOCH_002_DATASET_LOCK = ESTABLISHED`
- `TRACK_A_EPOCH_002_UNBLINDING = AUTHORIZED / BOUNDED`
- `TRACK_A_EPOCH_002_MATERIALIZATION_TOOLING = ACCEPTED`
- `TRACK_A_EPOCH_002_MATERIALIZATION = NOT_ESTABLISHED`
- `TRACK_A_EPOCH_002_PRIMARY_ANALYSIS = NOT_AUTHORIZED / NOT_RUN`
- `SCIENTIFIC_N_INCREMENT = 0`
- `CANONICAL_DGAF_EFFICACY = NOT_ESTABLISHED`
- `INDEPENDENT_VALIDATION = NOT_ESTABLISHED`
- `HIGH_ASSURANCE = PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0`

## Track A Epoch 001 — immutable historical boundary

Epoch 001 remains valid evidence that a prospective blinded panel was collected and retained under its exact frozen protocol:

- 50 paired inferential seed units;
- 2,250 blinded raw observations;
- dataset lock established;
- historical unblinding authorization established;
- protected mapping cryptographically unrecoverable under the retained evidence;
- primary analysis unanalyzable / not run;
- outcome aggregation not performed.

The retained CMS-protected mapping cannot be honestly reconstructed because the matching private-key escrow was not durably recoverable in the solo operating model. Do not brute-force, guess, infer, regenerate, or reconstruct the hidden assignment. Epoch 001 must not be pooled into the successor confirmatory analysis.

The custody failure is itself an engineering/governance finding. It does not erase the completed blinded collection, and it does not create an efficacy result.

For detailed historical event identities, use [`HISTORICAL_RECORDS_INDEX.md`](HISTORICAL_RECORDS_INDEX.md) and the immutable experiment/governance records rather than expanding this live summary into a second historical archive.

## Canonical High-Assurance provenance boundary

Repository `main` recency does not redefine the High-Assurance apparatus source, candidate identity, or deployment identity. Those remain exact-scope provenance records until an explicit governing transition replaces them.

- apparatus source: `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`
- apparatus source tree: `973c92335caf84f37fc2b3c4df6dd83b3b855087`;
- historical runtime-evidence candidate identity: `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`;
- historical runtime deployment identity: `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA`;
- final v0.7.6 High-Assurance candidate identity: **NOT DESIGNATED**.

The High-Assurance program therefore remains **PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / AUTHORIZATION NOT GRANTED / canonical empirical N=0**.

## Agent identity / vocabulary boundary

Issue #522 is **CLOSED / COMPLETED**. Current ontology authority is `docs/agents/AGENT_ROSTER.md` plus `registry/agent_ontology_adjudication.v1.json` and the accepted adjudication record.

- sovereign numbered seats come from the canonical roster;
- formation-local identifiers do not silently renumber sovereign seats;
- Sentinel and Sentinel-Phi are distinct ontology records;
- Agent Ionia is the sovereign A-13 identity;
- `IONIA_STATE` / Ionia 0Hz is a separate formation/runtime state and consumes no sovereign seat.

For industry-neutral terminology, use [`PUBLIC_TRANSLATION_LAYER.md`](PUBLIC_TRANSLATION_LAYER.md) and `VOCABULARY_TRANSLATION_MATRIX.json`.

## Evidence and authority rules

Current-facing documentation must preserve these distinctions:

1. Architecture is not implementation.
2. Implementation is not empirical evidence.
3. A passing test proves only its defined predicate and environment.
4. Developer self-verification is not independent verification.
5. Local custody recovery is not independent custody.
6. Freeze is not authorization.
7. Closure is not authorization.
8. Authorization is not execution.
9. Collection execution is not dataset lock.
10. Dataset lock is not unblinding authorization.
11. Unblinding authorization is not materialization.
12. Materialization is not primary-analysis authorization.
13. Primary-analysis authorization is not a positive result.
14. A completed blinded collection can still become unanalyzable if protected mapping custody fails.
15. Dependency, adjacency, documentation repetition, or shared authorship does not transfer evidence or scientific state.
16. Historical exact-scope evidence does not silently bind a later candidate, epoch, deployment, or apparatus.

## Current documentation routing

- **Primary live repository state:** this file, `docs/CURRENT_STATE.md`.
- **Compatibility status entrypoint:** [`PROJECT_STATUS.md`](PROJECT_STATUS.md).
- **Public overview:** [`../README.md`](../README.md).
- **Public / industry-neutral terminology:** [`PUBLIC_TRANSLATION_LAYER.md`](PUBLIC_TRANSLATION_LAYER.md).
- **Historical/provenance index:** [`HISTORICAL_RECORDS_INDEX.md`](HISTORICAL_RECORDS_INDEX.md).

No documentation update can itself promote scientific N, custody acceptance, freeze, authorization, independent verification, efficacy, or High-Assurance status.
