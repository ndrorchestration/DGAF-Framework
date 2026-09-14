# DGAF/PDMAL Project Status

> **Current-status entrypoint:** use [`CURRENT_STATE.md`](CURRENT_STATE.md) for the live repository/evidence boundary.

This path is retained for compatibility and is not an independent current-state authority. Historical snapshots remain under `docs/historical/` and must not be read as live state unless explicitly promoted by a later governing record.

For public terminology and industry-neutral explanations of DGAF-specific names, use [`PUBLIC_TRANSLATION_LAYER.md`](PUBLIC_TRANSLATION_LAYER.md).

## Current hard boundary

As of the 2026-09-14 post-#689 reconciliation:

- canonical High-Assurance program: **PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / AUTHORIZATION NOT GRANTED / N=0**;
- canonical DGAF efficacy: **NOT ESTABLISHED**;
- Track A Epoch 001: **COMPLETE / BLINDED / DATASET LOCKED / CRYPTOGRAPHICALLY UNRECOVERABLE FOR PRIMARY ANALYSIS**;
- Track A Epoch 002 repository custody: **ACCEPTED / SAME_SYSTEM_NONINDEPENDENT**;
- Track A Epoch 002 immutable freeze, final closure, and bounded verification classification: **ACCEPTED**;
- Track A Epoch 002 collection authorization: **ACCEPTED** at commit `563152fdb254b8ee948a693c287126a8bf8314b8`;
- Track A Epoch 002 collection: **COMPLETE** at 50 paired seed units / 2,250 blinded observations;
- operator retained-byte provenance admission: **PENDING**;
- successor dataset lock: **NOT ESTABLISHED**;
- successor unblinding: **NOT AUTHORIZED**;
- successor materialization: **NOT ESTABLISHED**;
- successor primary analysis: **NOT AUTHORIZED / NOT RUN**.

Accepted engineering support now includes #687 retained-byte admission preparation, #688 retrospective 53-record blinded pre-lock-ledger preparation, and #689 truthful `OPERATOR_CODESPACE` dataset-lock evidence preparation/admission support. Those tools do not assert that the operator-retained archives passed or that a dataset-lock receipt exists.

## Next admissible transition

Run the accepted #687–#689 sequence in the original operator-controlled Codespace against the exact retained public and encrypted-protected archives:

1. require retained-byte admission dry-run PASS before persistent non-authorizing output;
2. generate and validate the 53-record blinded pre-lock ledger;
3. generate the non-secret dataset-lock evidence manifest using the truthful `OPERATOR_CODESPACE` path;
4. admit only the bounded canonical non-secret outputs;
5. create the dataset-lock receipt later as a separate exact one-parent, one-file event.

Do not rerun the collection, fabricate GitHub Actions run/artifact identities, decrypt protected material, inspect or aggregate outcomes, authorize unblinding or analysis, or increment canonical scientific N.

## Presentation boundary

The owner-private DGAF Governance Console is a read-only companion presentation surface. It mirrors the current evidence boundary and provides creator/external reading modes, gate filtering, evidence inspection, and live repository freshness with a timestamped fallback. It is not a source of governance authority and cannot execute transitions. Its private URL is intentionally not recorded in this public repository.
