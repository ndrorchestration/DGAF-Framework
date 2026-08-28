# NDR Registry Reconciliation — 2026-08-28

## Finding

The two repository registry representations are not currently synchronized:

- Markdown registry: `docs/NDR_PATTERN_REGISTRY_UNIFIED.md` declares registry watermark **P-41**, 41 P-series entries, version 1.6, and identifies its machine-readable counterpart as pending schema v2.2 synchronization.
- Machine-readable registry: `docs/ndr_patterns_unified.json` declares version **2.4**, registry watermark **P-42**, and `total_p_series: 42`.
- P-42 has an explicit pattern card at `patterns/P-42_AHG.md`, whose status is **Partially Implemented — live recovery/evaluation evidence pending**.

## Evidence interpretation

The machine-readable registry and P-42 pattern card establish that P-42 is represented in current repository state. They do not, by themselves, establish that P-42 has independent validation or production efficacy.

The mismatch is a **registry synchronization defect**, not evidence of experimental efficacy or a reason to alter PDMAL freeze or authorization state.

## Required reconciliation

1. Reconcile the Markdown registry metadata and pattern table to P-42 using the existing authoritative P-42 pattern card and machine-readable registry.
2. Update the Markdown registry version/history and counterpart schema reference consistently.
3. Verify the resulting pair with deterministic registry consistency tests.
4. Preserve the existing historical version lineage; do not rewrite prior ratification history.

## Current boundary

This reconciliation is documentation/registry hygiene only.

- Experimental verification boundary: `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a`
- Freeze: NOT CREATED
- Authorization: NOT GRANTED
- Empirical N: 0

## Related controls

- `CROSS_REF.md` identifies this P-41/P-42 mismatch as an active synchronization issue.
- `patterns/P-42_AHG.md` is the P-42 pattern-card authority for implementation/evidence status.
- `docs/ndr_patterns_unified.json` is the current machine-readable registry representation.

**Disposition: OPEN / DOCUMENTATION SYNCHRONIZATION REQUIRED.**
