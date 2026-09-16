# DGAF/PDMAL Project Status

> **Current-status entrypoint:** use [`CURRENT_STATE.md`](CURRENT_STATE.md) for the live repository/evidence boundary.

This path is retained for compatibility and is not an independent current-state authority. Historical snapshots remain under `docs/historical/` and must not be read as live state unless explicitly promoted by a later governing record.

For public terminology and industry-neutral explanations of DGAF-specific names, use [`PUBLIC_TRANSLATION_LAYER.md`](PUBLIC_TRANSLATION_LAYER.md).

## Current hard boundary

As of the 2026-09-16 post-#728/#730/#732 reconciliation:

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
- successor prospective primary-analysis authorization tooling: **ACCEPTED / TOOLING ONLY** through PR #728, with procedure reconciliation in PR #730 and current-state reconciliation in PR #732;
- successor real materialization: **NOT ESTABLISHED**;
- successor materialization receipt: **NOT ESTABLISHED**;
- successor primary-analysis authorization event: **NOT ESTABLISHED**;
- successor primary analysis: **NOT AUTHORIZED / NOT RUN**;
- scientific-N increment: **0**.

The accepted dataset-lock, bounded-unblinding, materialization-tooling, and primary-analysis-authorization-tooling records preserve separate event boundaries. They do not establish real materialization, a materialization receipt, primary-analysis authorization, efficacy, independent validation, or High-Assurance authorization.

## Next admissible transition

The current frontier is no longer retained-byte admission, dataset locking, or authorization-tooling preparation. It remains **controlled operator-side materialization of the real retained Epoch 002 evidence**, followed by bounded evidence admission and a separate immutable materialization receipt.

The accepted apparatus now provides:

1. a controlled operator-side Stage-1 materializer with wrong-key/archive-drift and unsafe-archive fail-closed behavior;
2. a non-secret Stage-2 evidence-bundle wrapper that records content-addressed identities without custody secrets;
3. atomic publication of the complete materialization bundle only after validation;
4. a prospective, read-only primary-analysis authorization gate that can validate a future exact authorization event only after an accepted immutable materialization receipt exists;
5. explicit preservation of `PRIMARY_ANALYSIS_AUTHORIZATION=NOT_ESTABLISHED`, `PRIMARY_ANALYSIS=NOT_AUTHORIZED_NOT_RUN`, scientific-N increment 0, and canonical efficacy `NOT_ESTABLISHED`.

Do not place private keys, passphrases, protected plaintext mappings, or other recoverable secret material in GitHub, Notion, chat, CI inputs, workflow logs, or committed files. Do not create a positive primary-analysis authorization event until a real materialization has been admitted and its immutable receipt has been accepted. Do not run primary analysis until that separate authorization event is itself accepted.

## Presentation boundary

The owner-private DGAF Governance Console is a read-only companion presentation surface. It mirrors the current evidence boundary and provides creator/external reading modes, gate filtering, evidence inspection, and live repository freshness with a timestamped fallback. It is not a source of governance authority and cannot execute transitions. Its private URL is intentionally not recorded in this public repository.
