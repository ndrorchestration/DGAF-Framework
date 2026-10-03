# Experiment 1275 Queryable State Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans to implement this plan task-by-task.

**Goal:** Add a minimal non-authorizing query report over existing ecosystem-state machinery and record the eight-question baseline without creating a new SSOT.

**Architecture:** Reuse ECOSYSTEM_STATE_POINTER_V1, its validator, the core-component registry, and execution-receipt schema. The new query layer only summarizes existing authoritative artifacts and reports missing bindings/currentness gaps; it does not infer or promote state.

**Tech Stack:** Python 3, pytest, JSON.

**Spec:** GitHub issue #1275 and Notion page "Ecosystem Supercharge Program — Falsifiable Experiments".

## Global Constraints
- SCIENTIFIC_N_INCREMENT=0.
- INDEPENDENT_VALIDATION=NOT_ESTABLISHED.
- CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED.
- HIGH_ASSURANCE=NOT_AUTHORIZED.
- No new SSOT or parallel knowledge graph.
- Unknown currentness fails closed.

## Review Focus
- Missing consumer binding must be reported, not inferred.
- Historical snapshot must not be presented as live current state.
- Receipt evidence must never imply follow-on authority.
- Invalid pointer structure must fail rather than produce a report.
- Query output must preserve claim ceilings exactly.

---

### Task 1: Minimal ecosystem query report

**Files:**
- Create: `scripts/query_ecosystem_state.py`
- Create: `tests/test_query_ecosystem_state.py`

**Interfaces:**
- Produces: `build_report(root: Path, required_consumers: list[str]) -> dict`
- Produces CLI JSON suitable for later reconciliation tooling.

- [ ] Write failing tests for historical-snapshot scope, receipt non-authority, missing required consumers, exact claim ceilings, and invalid-pointer refusal.
- [ ] Run tests and confirm RED.
- [ ] Implement minimal report builder.
- [ ] Run targeted tests and full relevant state suites.
- [ ] Commit.

### Task 2: Baseline characterization record

**Files:**
- Create: `docs/experiments/ECOSYSTEM_QUERY_BASELINE_1275.md`

- [ ] Record the eight fixed questions, current source paths, machine support classification, observed gaps, and measurement limitations.
- [ ] Verify documentation claim ceilings and exact artifact paths.
- [ ] Commit.

### Task 3: Verification

- [ ] Run targeted query/state/Structural Epistemics tests.
- [ ] Run full pytest suite.
- [ ] Run `git diff --check`.
- [ ] Review the branch against issue #1275; do not merge or promote claims.
