# NDR Pattern Registry — P-42 Current-State Reconciliation

**Status:** Current-state reconciliation companion to `docs/ndr_patterns_unified.json`  
**Date:** 2026-08-26  
**Current main baseline at reconciliation:** `0770a3ea825430b7d8847e3c737f674561e86474`  
**Prior baseline referenced by the original companion:** `83e1678f55d16f32b5ce363e091ac74479cbfe1f`

## Current registry state

- **Registry watermark:** P-42
- **Total P-series:** 42
- **Machine-readable source:** `docs/ndr_patterns_unified.json`
- **P-42 implementation card:** `patterns/P-42_AHG.md`
- **Migration commit:** `b7058340aaeb788cbd652382867faf94b857888d`

## P-42 provenance

The June 29, 2026 migration explicitly renumbered Adaptive Harmonic Governance (AHG) from P-35 to **P-42** because P-35 was occupied by the Procluding Premise Gate. The migration synchronized `CROSS_REF`, `CHANGELOG`, `ENSEMBLE_ROSTER`, session-anchor provenance, the unified registry, and the JSON registry.

This establishes P-42 as an explicit repository lineage item, not an accidental later divergence.

## Evidence boundary

P-42 implementation history, tests, wiring, recovery scoring, and registry membership establish repository provenance and implementation status only. They do **not** establish empirical efficacy, independent validation, production readiness, or scientific superiority.

## Canonical-state precedence

For current repository state:

1. GitHub live objects and checks.
2. Exact repository files and evidence artifacts tied to explicit SHAs.
3. Notion operational records.
4. Prior reports and summaries as historical context.

An open PR is candidate state, not current `main` state. A historical commit remains historical even when its documentation is later referenced.

## P-series summary

| Range | Current interpretation |
|---|---|
| P-01–P-34 | Existing registered/canonical governance patterns as represented in the machine-readable registry |
| P-35 | Procluding Premise Gate — current occupied P-35 slot |
| P-36 | Gate Priority Schema |
| P-37–P-41 | Later resilience/transactional registrations |
| **P-42** | **Adaptive Harmonic Governance (AHG) — Layer 12 Cognitive Control Plane; specified with implementation lineage** |

## Historical registry note

`docs/NDR_PATTERN_REGISTRY_UNIFIED.md` contains the older P-41 snapshot and should be treated as historical until its canonical text is reconciled. This companion exists to prevent the stale P-41 text from being interpreted as evidence that the current registry watermark is P-41.

*No experimental authorization, freeze, or empirical N has been changed by this documentation correction.*
