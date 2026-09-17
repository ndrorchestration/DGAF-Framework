# Current Documentation Reconciliation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Bring DGAF current-facing repository and Notion documentation into alignment with protected `main` after the accepted Decision Frontier, Governance Map, assurance-inventory, and State-Space Explorer work while preserving every scientific/control boundary.

**Current baseline:** `b1d91621bd73e70866d5ff8fd38fb98e440b30e9` (PR #783 merged).

## Constraints

- Preserve canonical High-Assurance **PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0**.
- Preserve Track A Epoch 002 real materialization and materialization receipt as **NOT ESTABLISHED**.
- Preserve primary analysis as **NOT AUTHORIZED / NOT RUN**.
- Preserve canonical efficacy and independent validation as **NOT ESTABLISHED**.
- Preserve assurance coverage as **PARTIAL_CORE_FAMILIES_ONLY**.
- Keep protected-main required contexts separate from recurring-assurance catalog membership.
- Treat `UNMAPPED` / `UNCLASSIFIED` as fail-closed inventory states, not negative assurance judgments.
- Treat Decision Frontier, Governance Map, and State-Space Explorer V0 as presentation-only projections.
- State-Space V0 remains discrete/categorical; do not invent continuous coordinates, readiness distance, authorization probability, efficacy gradients, or consequence/reversibility values.
- Preserve historical specs, snapshots, and stale-lineage PRs as event-time provenance rather than rewriting them.

## Task 1 — Primary current-state surfaces

**Files:**

- `docs/CURRENT_STATE.md`
- `docs/PROJECT_STATUS.md`

- [x] Bind protected-main identity to `b1d91621…`.
- [x] Record #776, #779, and #783 as accepted presentation-only source state.
- [x] Record #780/#782/#785 as accepted partial assurance-inventory state.
- [x] Record #784 as closed/unmerged provenance only.
- [x] Preserve the scientific transition chain and evidence ceilings.

## Task 2 — Public / technical / governance entry points

**Files:**

- `README.md`
- `README.technical.md`
- `README.governance.md`

- [x] Add the accepted State-Space Explorer V0 to the Semantic Control Field architecture.
- [x] Preserve categorical reachability vs native predicate-state separation.
- [x] Preserve required-context vs assurance-catalog separation.
- [x] Preserve runtime/deployment vs source/CI vs scientific-state separation.

## Task 3 — Source-provenance synchronization

**Files:**

- `app/lib/governance-current-state.test.ts`
- `app/lib/governance.ts`

- [x] Preserve focused RED evidence from stale-lineage #786: the only UI semantic failure was `sourceUpdated` actual `2026-09-16` vs expected `2026-09-17`.
- [x] Carry the minimal GREEN production metadata correction onto exact post-#783 source.
- [ ] Revalidate UI semantic tests and production build on this fresh lineage.

## Task 4 — Change history

**File:** `CHANGELOG.md`

- [x] Record #776/#779/#783 Semantic Control Field progression.
- [x] Record #780/#782/#785 assurance-inventory progression.
- [x] Record #784 closed/unmerged and #786 stale-lineage reconciliation provenance.
- [x] Preserve historical changelog entries unchanged as event-time history.

## Task 5 — Notion projections

- [x] Refresh DGAF Operational Control Center.
- [x] Refresh Interface & Experience Design Control Area.
- [x] Refresh Visual Design & Cohesion Expert Agents.
- [x] Refresh DGAF portfolio registry and Repository Scope record.
- [x] Refresh vocabulary/taxonomy, Research Program Registry, Experiment Register, Audit & Assurance Registry, and Ecosystem Home current overlays.
- [ ] Reconcile those overlays to #783 accepted / #784 closed after the post-#783 repository candidate is validated.

## Task 6 — Final verification

- [ ] Run fresh exact-head repository workflow set on the post-#783 documentation candidate.
- [ ] Require UI Command Center Validation, Doc Lint, Doc Lint (PR Scope), Python quality, Governance CI, PDMAL Pre-Freeze, PPTL CI, PR Issue-State Keyword Guard, truth/control/custody/claim/coverage families to complete without failure.
- [ ] Re-check protected `main` immediately before merge.
- [ ] If `main` moved, refresh/reconcile again instead of transferring stale acceptance evidence.
- [ ] After merge, update Notion to the actual merge SHA and only then classify the reconciliation as accepted.
