# Documentation Drift Correction Note — 2026-08-31

## Purpose

Record the distinction between the current `main` tip, the current apparatus source, and unmerged working branches so control-plane documents do not become self-stale after documentation-only merges.

## Verified identities

- **Current `main` documentation tip:** `60b0588d7a63597344fcecd3acaadd6dc7eff073` (documentation/control-plane lineage; advances with doc-only merges).
- **Current apparatus source:** `d56b5b3c44e39ddb8c883259584432ab39259306`, the signed squash merge of PR #170 (seven-gate restoration + provenance integration). PR #160 (`02e4c958…`) supplied only the P-31/P-33 RESTORE subset and is now a historical ancestor, not the current apparatus boundary.
- **PR #162:** `cdb63ca138cf6a60727f91067fe8f7338f19f4a6`, unmerged draft provenance-binding work based on the older `02e4c958…` apparatus; superseded by #170 and not part of current `main`.
- **Apparatus tree SHA:** `8c13900c4ce2a503414f9dddf1d7ef7debead57e` (`git rev-parse d56b5b3c^{tree}`).

> **Update (post-#170):** this note originally recorded `02e4c958…` as the current apparatus (pre-#170). After PR #170 merged the complete seven-gate restoration, the authoritative apparatus source is `d56b5b3c…`. The `CONTROL_STATE_2026-08-31.yaml` and `PDMAL_CURRENT_CONTROL_STATE.md` are the canonical post-#170 bindings.

## Control rule

A documentation-only merge advances the `main` documentation lineage but does **not** redefine the apparatus source or create a new experimental candidate. Candidate identity changes only when apparatus-defining content changes.

## Experimental boundary

The project remains **PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0**. Historical P2/P6a evidence remains bound to its original source/deployment identity and is not transferred to the current post-#160 apparatus without exact identity equivalence.
