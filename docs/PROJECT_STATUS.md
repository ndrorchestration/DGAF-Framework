# DGAF/PDMAL Project Status

> **Current-status entrypoint:** use [`CURRENT_STATE.md`](CURRENT_STATE.md) for the live repository/evidence boundary.

This path is retained for compatibility and is not an independent current-state authority. Historical snapshots remain under `docs/historical/` and must not be read as live state unless explicitly promoted by a later governing record.

For public terminology and industry-neutral explanations of DGAF-specific names, use [`PUBLIC_TRANSLATION_LAYER.md`](PUBLIC_TRANSLATION_LAYER.md).

## Current hard boundary

As of the 2026-09-11 post-#644 reconciliation:

- canonical High-Assurance program: **PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / AUTHORIZATION NOT GRANTED / N=0**;
- canonical DGAF efficacy: **NOT ESTABLISHED**;
- Track A Epoch 001 prospective collection: **COMPLETE / BLINDED / RETAINED**;
- Epoch 001 inferential seed units: **50**;
- Epoch 001 blinded raw observations: **2,250**;
- Epoch 001 dataset lock: **ESTABLISHED**;
- Epoch 001 protected mapping: **CRYPTOGRAPHICALLY UNRECOVERABLE**;
- Epoch 001 primary analysis: **UNANALYZABLE / NOT RUN**;
- successor Track A scientific-control lane: **issue #523 OPEN**;
- successor operator-local custody-v2 recovery: **PASS_CURRENT_V2 / STRUCTURAL_SELF_ATTESTED_ONLY / NONINDEPENDENT**;
- successor repository custody admission: **ESTABLISHED / SAME_SYSTEM_NONINDEPENDENT** via accepted #644;
- successor precollection preflight: **NOT ESTABLISHED**;
- successor empirical collection: **NOT AUTHORIZED / NOT EXECUTED**;
- successor dataset lock: **NOT ESTABLISHED**;
- successor unblinding: **NOT AUTHORIZED**;
- successor materialization: **NOT ESTABLISHED**;
- successor primary analysis: **NOT AUTHORIZED / NOT RUN**.

Repository-side prospective tooling is accepted through precollection preflight (#612), immutable freeze (#613), final closure (#614), bounded verification classification (#615), separate human-controlled collection-authorization validation (#616), post-collection result-record semantics (#618), content-addressed dataset-lock validation (#622), and separate fail-closed unblinding-decision validation (#627).

Those controls are **preparation and validation tooling only**. They do not create preflight, freeze, authorization, empirical data, dataset lock, unblinding, materialization, analysis authority, independent validation, efficacy, High-Assurance authorization, or scientific N.

## Next admissible scientific transition

PR #644 accepted the exact public certificate and non-secret schema-v2 recovery receipt and satisfied repository `real_custody_v2`. Custody remains explicitly `SAME_SYSTEM_NONINDEPENDENT`; recoverability does not establish independence.

The first preflight attempt, #646, is **CLOSED / UNMERGED / SUPERSEDED**. It exposed repository-state-coupled predecessor-absence tests and then correctly failed the dedicated one-file scientific-event constraint once test maintenance shared the branch. No preflight state from #646 was accepted and none of its CI evidence transfers.

PR #648 is the active **test-only** maintenance prerequisite. After #648 is accepted, the next admissible scientific transition is a freshly rebuilt one-file `TRACK_A_EPOCH_002_PRECOLLECTION_PREFLIGHT.json` event from the then-current exact signed `main`, with newly bound candidate SHA/tree.

The ordered predecessor chain is now:

`accepted repository custody → precollection preflight → immutable freeze → final closure → verification classification → collection authorization → empirical collection → QC → dataset lock → separate unblinding decision → controlled materialization + immutable receipt → separate primary-analysis authorization → locked analysis`

Private keys, passphrases, encrypted backup copies, blinding secrets, and other recoverable secret material remain outside GitHub, Notion, chat, CI inputs, logs, and committed files.

Epoch 001 remains immutable historical evidence of a completed blinded prospective collection and dataset lock plus a custody/recovery design failure. It must not be brute-forced, reconstructed, pooled into a successor confirmatory analysis, or promoted into a canonical efficacy claim.
