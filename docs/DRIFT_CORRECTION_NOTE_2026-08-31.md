# Documentation Drift Correction Note — 2026-08-31

## Purpose

Record the distinction between the current `main` tip, the current apparatus source, and unmerged working branches so control-plane documents do not become self-stale after documentation-only merges.

## Verified identities

- **Current `main` documentation tip:** `34e1a05725cdb1a4d7773fb34f55047249d7ec14`.
- **Current apparatus source:** `02e4c958e435f1faaa6fbf15909f9141ed2a6e39`, merged by PR #160 and containing the P-31/P-33 RESTORE.
- **PR #162:** `cdb63ca138cf6a60727f91067fe8f7338f19f4a6`, unmerged draft provenance-binding work based on the apparatus source above.

## Control rule

A documentation-only merge advances the `main` documentation lineage but does **not** redefine the apparatus source or create a new experimental candidate. Candidate identity changes only when apparatus-defining content changes.

## Experimental boundary

The project remains **PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0**. Historical P2/P6a evidence remains bound to its original source/deployment identity and is not transferred to the current post-#160 apparatus without exact identity equivalence.
