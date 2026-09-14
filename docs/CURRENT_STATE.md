---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-09-14
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
track_a_successor_operator_local_custody_recovery: PASS_CURRENT_V2_SELF_ATTESTED_NONINDEPENDENT
track_a_successor_repository_custody_admission: ACCEPTED_SAME_SYSTEM_NONINDEPENDENT
track_a_successor_collection_authorization: ACCEPTED_COMMIT_563152F
track_a_successor_collection: COMPLETE_50_PAIRED_SEED_UNITS_2250_BLINDED_OBSERVATIONS
track_a_successor_operator_provenance: PENDING_RETAINED_BYTE_ADMISSION
track_a_successor_dataset_lock: NOT_ESTABLISHED
track_a_successor_unblinding: NOT_AUTHORIZED
track_a_successor_materialization: NOT_ESTABLISHED
track_a_successor_primary_analysis: NOT_AUTHORIZED_NOT_RUN
accepted_dataset_lock_tooling_pr: 622
accepted_unblinding_decision_tooling_pr: 627
accepted_operator_admission_tooling_pr: 687
accepted_pre_lock_ledger_tooling_pr: 688
accepted_operator_dataset_lock_evidence_tooling_pr: 689
---

# DGAF-Framework / PDMAL — Current State

This file is the **primary current-facing repository summary**. GitHub is authoritative for implementation, immutable evidence identities, issues, and CI. The DGAF Operational Control Center in Notion is the interpreted governance/control-plane mirror. Historical records are authoritative only for the exact scope, identity, and time they bind.

The canonical High-Assurance program, Track A Epoch 001, and Track A Epoch 002 are separate governance/evidence boundaries. Evidence, authorization, N, verification class, and efficacy do not transfer between them without an explicit governed rule.

## Executive boundary

| Area | Current state |
|---|---|
| Canonical High-Assurance program | **PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / AUTHORIZATION NOT GRANTED / N=0** |
| Canonical DGAF efficacy | **NOT ESTABLISHED** |
| Track A Epoch 001 prospective collection | **COMPLETE / BLINDED / RETAINED** |
| Epoch 001 inferential seed units | **50** |
| Epoch 001 blinded raw observations | **2,250** |
| Epoch 001 dataset lock | **ESTABLISHED** |
| Epoch 001 protected mapping recoverability | **CRYPTOGRAPHICALLY UNRECOVERABLE** |
| Epoch 001 primary analysis | **UNANALYZABLE / NOT RUN** |
| Successor Track A lane | **ISSUE #523 OPEN** |
| Successor operator-local custody recovery | **PASS_CURRENT_V2 / STRUCTURAL_SELF_ATTESTED_ONLY / NONINDEPENDENT** |
| Successor repository custody admission | **ACCEPTED / SAME_SYSTEM_NONINDEPENDENT** |
| Successor empirical collection | **AUTHORIZED THEN COMPLETE · 50 PAIRED SEED UNITS / 2,250 BLINDED OBSERVATIONS** |
| Successor operator retained-byte admission | **PENDING** |
| Successor dataset lock | **NOT ESTABLISHED** |
| Successor unblinding | **NOT AUTHORIZED** |
| Successor materialization | **NOT ESTABLISHED** |
| Successor primary analysis | **NOT AUTHORIZED / NOT RUN** |
| B1 standalone non-empirical lane | **COMPLETE** |
| B2 standalone non-empirical lane | **COMPLETE** |
| B3 standalone non-empirical lane | **COMPLETE** |
| Track C composition | **MERGED NON-EMPIRICAL PROPOSAL** |
| Track C empirical execution | **NOT AUTHORIZED** |

No row above establishes independent validation, production certification, integrated DGAF efficacy, High-Assurance authorization, or a completed successor Track A primary result.

## Successor Track A — controlling scientific lane

Issue #523 controls the replacement topology-robustness experiment after the Epoch 001 custody failure. Epoch 002 uses a new protocol identity, fresh seeds, fresh blinding, and recoverable solo custody while preserving the locked endpoint/estimand/matrix semantics unless a change is separately justified before outcome access.

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

### Accepted prospective tooling

Repository-side engineering has prepared the following **without creating the governed transition itself**:

1. Epoch 002 primary-analysis implementation lock — PR #585;
2. fail-closed Epoch 002 runner and machine contract — PR #591;
3. custody schema-v2 hardening and runner/custody-source rebinding — PR #597;
4. non-authorizing Completion State Reconciler — PR #601;
5. custody receipt-to-certificate byte-binding hardening — PR #603;
6. precollection-preflight validation — PR #612;
7. immutable-freeze validation — PR #613;
8. final-closure validation — PR #614;
9. bounded verification-classification validation — PR #615;
10. separate human-controlled collection-authorization validation — PR #616;
11. fail-closed post-collection result-record schema/ledger/semantics — PR #618;
12. content-addressed dataset-lock validation — PR #622;
13. separate fail-closed human-controlled unblinding-decision validation — PR #627;
14. operator-local retained-byte admission preparation — PR #687;
15. retrospective 53-record blinded pre-lock-ledger preparation — PR #688;
16. truthful `OPERATOR_CODESPACE` dataset-lock evidence preparation/admission support — PR #689.

Protected `main` is `b409403624181c86738113b029c4a12e42f0b318` after accepted PR #689. PRs #687–#689 provide engineering support for the operator-local retained-byte sequence. Their acceptance does not assert that the retained archives were processed or that canonical repository evidence exists.

The unblinding-decision validator still requires a future accepted PASS `DATASET_LOCK_RECEIPT`, exact event/content binding, and a separate human-controlled authorization event. A future positive unblinding decision remains bounded to controlled mapping release/decryption and cannot authorize primary analysis.

### Current retained-byte admission frontier

The separately authorized Track A Epoch 002 collection completed in the operator-controlled Codespace:

- execution class: `OPERATOR_CODESPACE`;
- accepted authorization commit: `563152fdb254b8ee948a693c287126a8bf8314b8`;
- 50 paired seed units / 2,250 blinded observations;
- public and encrypted-protected surfaces retained separately;
- custody classification remains `SAME_SYSTEM_NONINDEPENDENT`.

The actual retained archive bytes remain outside the repository. Accepted PRs #687–#689 provide a dry-run-first path to validate those exact bytes, prepare the 53-record blinded pre-lock ledger, and produce the bounded non-secret dataset-lock evidence manifest. They do not claim that this operator step has occurred.

The next admissible transition is therefore **operator-local validation and bounded admission of the exact retained evidence**. Run the accepted preparers in the original Codespace, require their non-authorizing PASS states, and admit only the canonical non-secret evidence manifest and pre-lock ledger. Do not rerun collection, decrypt protected material, aggregate outcomes, or fabricate GitHub Actions identities.

Private keys, passphrases, encrypted backup copies, blinding secrets, protected plaintext mappings, and any other recoverable secret material remain prohibited from GitHub, Notion, chat, CI inputs, workflow logs, and committed files.

## Ordered successor transition chain

Tooling readiness never skips predecessor state. The current governed order is:

`repository custody acceptance — ACCEPTED`
`→ precollection preflight — ACCEPTED`
`→ Epoch 002 immutable freeze — ESTABLISHED`
`→ final closure — ACCEPTED`
`→ bounded verification classification — ACCEPTED / NONINDEPENDENT`
`→ separate collection authorization — ACCEPTED`
`→ empirical collection — COMPLETE`
`→ operator retained-byte admission — CURRENT FRONTIER`
`→ PASS QC ledger`
`→ dataset-lock receipt`
`→ separate human-controlled unblinding decision`
`→ controlled local materialization`
`→ immutable materialization receipt`
`→ separate primary-analysis authorization`
`→ locked primary analysis`
`→ interpretation/adjudication`

Current predicates remain:

- `TRACK_A_EPOCH_002_REPOSITORY_CUSTODY = ACCEPTED / SAME_SYSTEM_NONINDEPENDENT`
- `TRACK_A_EPOCH_002_COLLECTION_AUTHORIZATION = ACCEPTED`
- `TRACK_A_EPOCH_002_COLLECTION = COMPLETE`
- `TRACK_A_EPOCH_002_OPERATOR_PROVENANCE = PENDING_RETAINED_BYTE_ADMISSION`
- `TRACK_A_EPOCH_002_DATASET_LOCK = NOT_ESTABLISHED`
- `TRACK_A_EPOCH_002_UNBLINDING = NOT_AUTHORIZED`
- `TRACK_A_EPOCH_002_MATERIALIZATION = NOT_ESTABLISHED`
- `TRACK_A_EPOCH_002_PRIMARY_ANALYSIS = NOT_AUTHORIZED / NOT_RUN`
- `CANONICAL_DGAF_EFFICACY = NOT_ESTABLISHED`
- `HIGH_ASSURANCE = PRE-FREEZE / NOT AUTHORIZED / N=0`

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
5. Local custody recovery is not repository custody acceptance and is not independent custody.
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
