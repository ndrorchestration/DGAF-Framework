---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-09-12
canonical_high_assurance_empirical_n: 0
final_candidate_status: NOT_DESIGNATED
canonical_dgaf_efficacy: NOT_ESTABLISHED
track_a_epoch_001_collection: COMPLETE_BLINDED_RETAINED
track_a_epoch_001_inferential_seed_units: 50
track_a_epoch_001_blinded_observations: 2250
track_a_epoch_001_dataset_lock: ESTABLISHED
track_a_epoch_001_unblinding_authorization: ESTABLISHED_HISTORICAL
track_a_epoch_001_unblinding_recoverability: CRYPTOGRAPHICALLY_UNRECOVERABLE
track_a_epoch_001_primary_analysis: UNANALYZABLE_NOT_RUN
track_a_successor_issue: 523
track_a_successor_repository_custody: ESTABLISHED_SAME_SYSTEM_NONINDEPENDENT
track_a_successor_precollection_preflight: ACCEPTED
track_a_successor_immutable_freeze: ESTABLISHED
track_a_successor_final_closure: ACCEPTED
track_a_successor_verification_classification: NOT_ACCEPTED
track_a_successor_collection_authorization: NOT_ESTABLISHED
track_a_successor_collection: NOT_AUTHORIZED_NOT_EXECUTED
track_a_successor_dataset_lock: NOT_ESTABLISHED
track_a_successor_unblinding: NOT_AUTHORIZED
track_a_successor_materialization: NOT_ESTABLISHED
track_a_successor_primary_analysis: NOT_AUTHORIZED_NOT_RUN
---

# DGAF-Framework / PDMAL — Current State

This file is the **primary current-facing repository summary**. GitHub is authoritative for implementation, immutable evidence identities, issues, pull requests, and CI. The DGAF Operational Control Center in Notion is the interpreted governance/control-plane mirror. Historical records are authoritative only for the exact scope, identity, and time they bind.

The canonical High-Assurance program, Track A Epoch 001, and Track A Epoch 002 are separate governance/evidence boundaries. Evidence, authorization, N, verification class, and efficacy do not transfer between them without an explicit governed rule.

## Executive boundary

| Area | Current state |
|---|---|
| Canonical High-Assurance program | **PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0** |
| Canonical DGAF efficacy | **NOT ESTABLISHED** |
| Track A Epoch 001 prospective collection | **COMPLETE / BLINDED / RETAINED** |
| Epoch 001 dataset lock | **ESTABLISHED** |
| Epoch 001 protected mapping recoverability | **CRYPTOGRAPHICALLY UNRECOVERABLE** |
| Epoch 001 primary analysis | **UNANALYZABLE / NOT RUN** |
| Successor Track A lane | **ISSUE #523 OPEN** |
| Epoch 002 repository custody | **ESTABLISHED / SAME_SYSTEM_NONINDEPENDENT** |
| Epoch 002 precollection preflight | **ACCEPTED / RETAINED** |
| Epoch 002 immutable freeze | **ESTABLISHED** |
| Epoch 002 final closure | **ACCEPTED** |
| Epoch 002 verification classification | **NOT ACCEPTED** |
| Epoch 002 empirical collection | **NOT AUTHORIZED / NOT EXECUTED** |
| Epoch 002 dataset lock | **NOT ESTABLISHED** |
| Epoch 002 unblinding | **NOT AUTHORIZED** |
| Epoch 002 materialization | **NOT ESTABLISHED** |
| Epoch 002 primary analysis | **NOT AUTHORIZED / NOT RUN** |

**Current controlling posture:** **FREEZE ESTABLISHED · FINAL CLOSURE ACCEPTED · VERIFICATION CLASSIFICATION NOT ACCEPTED · FAIL-CLOSED · SUCCESSOR COLLECTION NOT AUTHORIZED · N=0**.

No current state establishes independent validation, production certification, integrated DGAF efficacy, High-Assurance authorization, or a successor Track A empirical result.

## Successor Track A — current frontier

Issue #523 controls the replacement topology-robustness experiment after the Epoch 001 custody failure. Epoch 002 uses a new protocol identity, fresh seeds, fresh blinding, and recoverable solo custody while preserving the prospectively locked endpoint/estimand/matrix semantics.

Accepted predecessor chain now includes:

1. repository custody-v2 evidence accepted and classified `SAME_SYSTEM_NONINDEPENDENT`;
2. Epoch 002 precollection preflight accepted;
3. Epoch 002 immutable freeze established through accepted PR #655;
4. lifecycle-maintenance repair #657 accepted;
5. Epoch 002 final closure accepted through PR #661 on protected `main` `203026f5222a446466796cf0dc7cfa5e9c0c3586`.

Verification-classification attempts #663 and #664 are **CLOSED / UNMERGED / RED PROVENANCE**. They exposed test-isolation defects in hypothetical verification-absence negative controls; they did not establish verification classification and their validation evidence does not transfer.

Maintenance PR #665 is the controlling repair lane. Its exact head is `336534603b2374ccfcec0342ae80734f6efc086e`. GitHub validation is terminal-green, but that exact head still carries an external Vercel failure caused by the Hobby deployment-rate limit. A deployment or status from another SHA cannot substitute.

Therefore the next admissible transition is:

`exact-head external success for #665`
`→ guarded acceptance of #665`
`→ fresh one-file Epoch 002 verification-classification event from resulting exact main`
`→ fresh exact-head GitHub + external validation`
`→ separate human-controlled collection-authorization decision`

The intended verification class remains bounded to developer self-attestation / nonindependent verification. Verification classification is **not** collection authorization.

## Ordered successor transition chain

Tooling readiness never skips predecessor state. The governed order is:

`repository custody acceptance [COMPLETE]`
`→ precollection preflight [COMPLETE]`
`→ immutable freeze [COMPLETE]`
`→ final closure [COMPLETE]`
`→ verification classification [CURRENT FRONTIER]`
`→ separate collection authorization`
`→ empirical collection`
`→ PASS QC ledger`
`→ dataset-lock receipt`
`→ separate human-controlled unblinding decision`
`→ controlled local materialization`
`→ immutable materialization receipt`
`→ separate primary-analysis authorization`
`→ locked primary analysis`
`→ interpretation/adjudication`

Current predicates:

- `TRACK_A_EPOCH_002_REPOSITORY_CUSTODY = ESTABLISHED / SAME_SYSTEM_NONINDEPENDENT`
- `TRACK_A_EPOCH_002_PREFLIGHT = ACCEPTED`
- `TRACK_A_EPOCH_002_FREEZE = ESTABLISHED`
- `TRACK_A_EPOCH_002_FINAL_CLOSURE = ACCEPTED`
- `TRACK_A_EPOCH_002_VERIFICATION_CLASSIFICATION = NOT_ACCEPTED`
- `TRACK_A_EPOCH_002_COLLECTION = NOT_AUTHORIZED / NOT_EXECUTED`
- `TRACK_A_EPOCH_002_DATASET_LOCK = NOT_ESTABLISHED`
- `TRACK_A_EPOCH_002_UNBLINDING = NOT_AUTHORIZED`
- `TRACK_A_EPOCH_002_MATERIALIZATION = NOT_ESTABLISHED`
- `TRACK_A_EPOCH_002_PRIMARY_ANALYSIS = NOT_AUTHORIZED / NOT_RUN`
- `CANONICAL_DGAF_EFFICACY = NOT_ESTABLISHED`
- `HIGH_ASSURANCE = NOT_AUTHORIZED / N=0`

## Parallel engineering lane

Discovery Harness PR #660 is non-authorizing engineering infrastructure. Exact head `35a844d3ea7dd719a81671108b709916236f8878` has terminal-green GitHub validation and an exact-head READY/SUCCESS Vercel deployment. It remains draft / sequencing-HOLD so it does not move protected `main` underneath the active #665 → verification-classification scientific transition sequence.

Its success is engineering evidence only. It does not establish efficacy, independent verification, collection authorization, empirical execution, High-Assurance status, or scientific N.

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

## Canonical High-Assurance provenance boundary

Repository `main` recency does not redefine the separate High-Assurance apparatus, candidate, deployment, or authorization state. The currently bound exact-scope identities remain:

- apparatus source: `2a54a67d84870e4eeb71b8aaf04413e0ca492ba1`
- apparatus source tree: `973c92335caf84f37fc2b3c4df6dd83b3b855087`
- candidate identity: `NOT_DESIGNATED`
- deployment identity: `NOT_ESTABLISHED_FOR_FINAL_CANDIDATE`
- historical runtime-evidence candidate: `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`
- historical runtime deployment: `dpl_8MsufVUMXHMGqx9d1dcK9va5EWUA`

The High-Assurance program remains **PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / canonical empirical N=0** until its own governed transition occurs.

## Evidence and authority rules

1. Architecture is not implementation.
2. Implementation is not empirical evidence.
3. A passing test proves only its defined predicate and environment.
4. Developer self-verification is not independent verification.
5. Recoverable solo custody is not independent custody.
6. Freeze is not authorization.
7. Closure is not authorization.
8. Verification classification is not collection authorization.
9. Authorization is not execution.
10. Collection execution is not dataset lock.
11. Dataset lock is not unblinding authorization.
12. Unblinding authorization is not materialization.
13. Materialization is not primary-analysis authorization.
14. Primary-analysis authorization is not a positive result.
15. Dependency, adjacency, documentation repetition, or shared authorship does not transfer evidence or scientific state.
16. Historical exact-scope evidence does not silently bind a later candidate, epoch, deployment, or apparatus.

## Current documentation routing

- **Primary live repository state:** this file, `docs/CURRENT_STATE.md`.
- **Compatibility status entrypoint:** [`PROJECT_STATUS.md`](PROJECT_STATUS.md).
- **Public overview:** [`../README.md`](../README.md).
- **Public / industry-neutral terminology:** [`PUBLIC_TRANSLATION_LAYER.md`](PUBLIC_TRANSLATION_LAYER.md).
- **Historical/provenance index:** [`HISTORICAL_RECORDS_INDEX.md`](HISTORICAL_RECORDS_INDEX.md).

No documentation update can itself promote scientific N, custody independence, verification classification, freeze, authorization, efficacy, or High-Assurance status.
