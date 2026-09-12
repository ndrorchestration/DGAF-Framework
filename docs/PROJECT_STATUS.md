# DGAF/PDMAL Project Status

> **Current-status entrypoint:** use [`CURRENT_STATE.md`](CURRENT_STATE.md) for the live repository/evidence boundary.

This path is retained for compatibility and is not an independent current-state authority. Historical snapshots remain under `docs/historical/` and must not be read as live state unless explicitly promoted by a later governing record.

For public terminology and industry-neutral explanations of DGAF-specific names, use [`PUBLIC_TRANSLATION_LAYER.md`](PUBLIC_TRANSLATION_LAYER.md).

## Current hard boundary

As of the 2026-09-12 reconciliation:

- canonical High-Assurance program: **PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0**;
- canonical DGAF efficacy: **NOT ESTABLISHED**;
- Track A Epoch 001 prospective collection: **COMPLETE / BLINDED / RETAINED**;
- Epoch 001 inferential seed units: **50**;
- Epoch 001 blinded raw observations: **2,250**;
- Epoch 001 dataset lock: **ESTABLISHED**;
- Epoch 001 protected mapping: **CRYPTOGRAPHICALLY UNRECOVERABLE**;
- Epoch 001 primary analysis: **UNANALYZABLE / NOT RUN**;
- successor Track A scientific-control lane: **issue #523 OPEN**;
- successor repository custody-v2: **ESTABLISHED / SAME_SYSTEM_NONINDEPENDENT**;
- successor precollection preflight: **ACCEPTED**;
- successor immutable freeze: **ESTABLISHED**;
- successor final closure: **ACCEPTED**;
- successor verification classification: **NOT ACCEPTED**;
- successor empirical collection: **NOT AUTHORIZED / NOT EXECUTED**;
- successor dataset lock: **NOT ESTABLISHED**;
- successor unblinding: **NOT AUTHORIZED**;
- successor materialization: **NOT ESTABLISHED**;
- successor primary analysis: **NOT AUTHORIZED / NOT RUN**.

Current controlling posture is **FREEZE ESTABLISHED · FINAL CLOSURE ACCEPTED · VERIFICATION CLASSIFICATION NOT ACCEPTED · FAIL-CLOSED · SUCCESSOR COLLECTION NOT AUTHORIZED · N=0**.

## Current frontier

Protected `main` is `203026f5222a446466796cf0dc7cfa5e9c0c3586` after accepted final-closure PR #661.

Verification-classification attempts #663/#664 are closed/unmerged RED provenance. Maintenance PR #665 repairs the test-isolation defect they exposed without modifying scientific records or authorization state. Its exact head `336534603b2374ccfcec0342ae80734f6efc086e` is GitHub-green but remains held because that exact SHA still carries an external Vercel build-rate-limit failure.

No successful deployment from a different SHA may substitute for #665 exact-head evidence.

The next admissible sequence is:

`exact-head external success for #665 → guarded acceptance of #665 → fresh one-file verification-classification event from resulting exact main → fresh exact-head validation → separate human-controlled collection-authorization decision`

Verification classification does not authorize collection. Collection remains NOT AUTHORIZED / NOT EXECUTED and scientific N remains 0.

## Parallel engineering

Discovery Harness PR #660 is a separate non-authorizing engineering lane. Exact head `35a844d3ea7dd719a81671108b709916236f8878` is GitHub-green and has exact-head Vercel READY/SUCCESS evidence. It remains draft / sequencing-HOLD until the #665 → fresh verification-classification sequence stabilizes so non-authorizing engineering work does not move `main` underneath the scientific transition lane.

## Remaining ordered scientific chain

`verification classification → separate collection authorization → empirical collection → PASS QC ledger → dataset-lock receipt → separate unblinding decision → controlled materialization + immutable receipt → separate primary-analysis authorization → locked analysis → interpretation/adjudication`

Repository-side tooling for downstream gates does not itself create those states.

Private keys, passphrases, encrypted backup copies, blinding secrets, protected plaintext mappings, and other recoverable secret material remain outside GitHub, Notion, chat, CI inputs, logs, and committed files.

Epoch 001 remains immutable historical evidence of a completed blinded prospective collection and dataset lock plus a custody/recovery design failure. It must not be brute-forced, reconstructed, pooled into the successor confirmatory analysis, or promoted into a canonical efficacy claim.
