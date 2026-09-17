# Current Documentation Reconciliation Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Bring DGAF's current-facing repository documentation into alignment with protected `main` after PRs #779, #782, and #785 while preserving all scientific/control boundaries.

**Architecture:** Update only current-facing public, technical, governance, status, and changelog surfaces. Historical records, completed design specs, and stale-lineage/TDD records remain immutable provenance and are not rewritten into current authority.

**Tech Stack:** Markdown, repository current-state records, GitHub PR/CI lineage.

**Spec:** Existing authority contract in `docs/CURRENT_STATE.md`, `README.md`, and repository SSoT rules.

## Global Constraints

- Protected `main` baseline for this sweep: `6b89529da3e7ff13e14eaea415756579d859fb26`.
- Preserve `PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0` for the canonical High-Assurance program.
- Preserve Track A Epoch 002 real materialization as `NOT ESTABLISHED` and primary analysis as `NOT AUTHORIZED / NOT RUN`.
- Do not promote UI/source verification into deployment, runtime-health, scientific, efficacy, independent-validation, or High-Assurance evidence.
- Preserve `PARTIAL_CORE_FAMILIES_ONLY`; the assurance catalog is not exhaustive.
- Distinguish protected-branch required contexts from the broader recurring assurance catalog.
- Treat open PRs as work in progress, not accepted current implementation.

---

### Task 1: Reconcile primary current-state surfaces

**Files:**
- Modify: `docs/CURRENT_STATE.md`
- Modify: `docs/PROJECT_STATUS.md`

**Interfaces:**
- Consumes: accepted protected-main history through `6b89529d...`
- Produces: current-facing repository state used by public and governance references

- [ ] **Step 1:** Update verification date and source baseline.
- [ ] **Step 2:** Record accepted presentation milestones #776 and #779 as presentation-only source state.
- [ ] **Step 3:** Record accepted assurance-catalog milestones #780, #782, and #785 with partial-coverage boundary.
- [ ] **Step 4:** Record #783 and #784 only as open workstreams, not accepted state.
- [ ] **Step 5:** Re-read the resulting files and verify scientific predicates are unchanged.

### Task 2: Reconcile public and technical entry points

**Files:**
- Modify: `README.md`
- Modify: `README.technical.md`
- Modify: `README.governance.md`

**Interfaces:**
- Consumes: reconciled current-state language from Task 1
- Produces: public, engineering, and governance-facing descriptions consistent with the same truth model

- [ ] **Step 1:** Add the accepted Decision Frontier and Governance Map to the public implementation summary without calling them governance authority.
- [ ] **Step 2:** Add the machine-readable partial assurance catalog and workflow coverage-gap scanner to the technical map.
- [ ] **Step 3:** Update audit/provenance guidance to distinguish mapped recurring assurance families from required protected-main contexts.
- [ ] **Step 4:** Preserve all existing non-claims and Track A boundaries.

### Task 3: Record the accepted change sequence

**Files:**
- Modify: `CHANGELOG.md`

**Interfaces:**
- Consumes: merged PR identities #776, #779, #780, #782, #785
- Produces: dated repository history without redefining current authority

- [ ] **Step 1:** Add a 2026-09-17 entry summarizing the accepted interface and assurance-inventory milestones.
- [ ] **Step 2:** Explicitly preserve scientific/control non-effects and deployment limitations.
- [ ] **Step 3:** Retain older changelog entries unchanged as event-time history.

### Task 4: Verify documentation-only scope

**Files:**
- Review all modified Markdown files.

**Interfaces:**
- Consumes: branch diff
- Produces: documentation-only candidate suitable for repository CI

- [ ] **Step 1:** Verify no source/runtime/configuration file changed.
- [ ] **Step 2:** Verify every accepted-state claim names only merged evidence.
- [ ] **Step 3:** Verify open PRs are labeled open/draft rather than accepted.
- [ ] **Step 4:** Run repository documentation/claim/governance CI through the PR workflow.
