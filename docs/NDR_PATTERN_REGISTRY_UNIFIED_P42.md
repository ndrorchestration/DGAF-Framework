# NDR Pattern Registry — P-42 Current-State Reconciliation

**Status:** Current-state reconciliation companion to `docs/ndr_patterns_unified.json`  
**Date:** 2026-09-02  
**Current main baseline at reconciliation:** `275756fd81c975f17ae3d16d24e599db0617cf85`  
**Transversal overlay:** `docs/NDR_PATTERN_REGISTRY_UNIFIED_TRANSVERSAL_OVERLAY_2026-09-02.md`

## Current registry state

- **Registry watermark:** P-42
- **Total P-series:** 42
- **Machine-readable source:** `docs/ndr_patterns_unified.json`
- **P-42 implementation card:** `patterns/P-42_AHG.md`
- **Transversal pattern card:** `patterns/NDR_TRANSVERSAL_CANDIDATE_AGREEMENT_v1.md`
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

## Transversal agreement semantics

For any live candidate cycle, pattern-registry assertions must be interpreted against the same scoped identity tuple used by the evidence-control layer:

`apparatus/source SHA + candidate SHA/tree + deployment identity/source SHA + workflow/evidence run + artifact identity + protocol/analysis binding + freeze identity + authorization state`

Cross-registry agreement distinguishes:

- `ROLE DIFFERENCE` — distinct identities intentionally serving different semantic roles;
- `HISTORICAL DIFFERENCE` — prior identity retained for provenance and explicitly non-closing;
- `TRANSVERSAL DRIFT` — conflicting live projections without an intentional role distinction;
- `BLOCKING CONTRADICTION` — discrepancy capable of permitting invalid evidence transfer or governance transition.

Pattern registry membership does not upgrade a pattern from `DEFINED`/`IMPLEMENTED` to `VERIFIED`, and a registry entry cannot create freeze, authorization, or empirical execution.

## P-35 / P-42 boundary

`P-35` is **Procluding Premise Gate**. `P-42` is **Adaptive Harmonic Governance**.

Current P-35 remediation requires an explicit `premise_check_fn` at the DGAF/TGL/ConsensusTask boundary. This is an engineering/wiring dependency. It does not define a PDMAL-specific constitutional premise policy; that checker remains a separate experimental-control prerequisite.

## Historical registry note

`docs/NDR_PATTERN_REGISTRY_UNIFIED.md` contains the older P-41 snapshot and should be treated as historical until its canonical text is reconciled. This companion and the transversal overlay prevent that snapshot from being interpreted as evidence that the current registry watermark is P-41.

**Current transversal overlay:** `docs/NDR_PATTERN_REGISTRY_UNIFIED_TRANSVERSAL_OVERLAY_2026-09-02.md`
**Machine-readable overlay:** `docs/ndr_patterns_unified_transversal_overlay.json`

*No experimental authorization, freeze, or empirical N has been changed by this documentation correction.*
