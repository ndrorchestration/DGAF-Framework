# State-Space Explorer V0 — Implementation Plan

> **Execution mode:** test-first, presentation-only, fail-closed

## Goal

Implement the first State-Space Explorer as a discrete reachability projection over canonical DGAF UI truth. Do not introduce new governance semantics, continuous geometry, inferred authority, or scalar readiness metrics.

## Task 1 — Lock the projection contract RED

Create `app/lib/state-space-projection.test.ts` before the production projection module exists.

The contract must assert:

- projection stage IDs equal `GOVERNANCE_STAGES` IDs in order;
- the current frontier is `materialization`;
- all stages before the frontier are `established`;
- `materialization` is `frontier` and retains native `not_established`;
- `primary-analysis-authorization` and `locked-analysis` are `blocked_by_predecessor` while retaining native `not_authorized`;
- global constraints preserve PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0;
- consequence and reversibility are `not_modeled`;
- no readiness/score/probability/distance/continuous coordinate fields exist;
- the future component exposes explicit non-color truth labels;
- the future route uses the shared projection rather than copying `GOVERNANCE_STAGES`.

Expected RED signature: existing UI tests pass; the new test file fails because `app/lib/state-space-projection.ts` does not yet exist.

## Task 2 — Implement the projection model

Create `app/lib/state-space-projection.ts`.

Requirements:

- import `GOVERNANCE_STAGES` and `TRUTH_BOUNDARY`;
- locate the first non-`pass` canonical stage;
- derive `established | frontier | blocked_by_predecessor` independently of native predicate state;
- preserve canonical stage identity, label, order, native state, evidence boundary, and `doesNotEstablish`;
- define a fixed dimension-description registry whose classifications are semantic metadata, not state values;
- classify `consequence` and `reversibility` as `not_modeled`;
- expose no numeric readiness, probability, score, distance, or continuous coordinate.

## Task 3 — Build the V0 expert surface

Create `app/components/state-space-view.tsx` and `app/styles/state-space.css`.

Required composition:

1. representation-contract band;
2. discrete reachability corridor;
3. visible frontier boundary;
4. stage inspection cards/rows preserving native state + evidence boundary + non-transfer clause;
5. independent dimension matrix with `PROJECTABLE`, `BOUNDED`, and `NOT MODELED — DO NOT INFER` treatments.

Required literal labels for semantic testing:

- `DISCRETE REACHABILITY`
- `NO CONTINUOUS INTERPOLATION`
- `CURRENT FRONTIER`
- `BLOCKED BY PREDECESSOR`
- `NOT MODELED — DO NOT INFER`

Use geometry/border/pattern + text, never color alone.

## Task 4 — Add the separate State Space view

Update:

- `app/components/app-shell.tsx`
- `app/page.tsx`
- `app/layout.tsx`

Add `state-space` to `ViewId`, expose a `State Space` navigation item with subtitle `Reachability model`, route it to `StateSpaceView`, and load the dedicated stylesheet.

Do not remove or collapse the Governance view. Governance Map remains the structural inspection surface; State Space is the expert modeling projection.

## Task 5 — GREEN verification

Run/observe the exact-head UI lane.

Required GREEN evidence:

- semantic/contract suite succeeds;
- production Next.js build succeeds;
- no pre-existing UI test regresses.

Then allow the full repository workflow matrix to complete on the same exact head.

## Task 6 — Panel QA

Review against the two panel contracts:

- native state remains distinguishable from reachability region;
- blocked vs not-authorized vs not-established are not visually collapsed;
- no continuous/manifold implication appears in V0;
- no color-only state distinctions;
- mobile ordering preserves reachability semantics;
- reduced-motion behavior preserves meaning;
- no generic dashboard KPI treatment is introduced;
- external technical reader can identify frontier and unmodeled dimensions quickly.

Any discovered semantic defect must receive a focused failing contract before correction when practical.

## Task 7 — Integration

Keep the PR draft until exact-head checks terminate successfully.

Before merge:

- reconcile PR body to the final candidate SHA and verification state;
- ensure protected `main` has not advanced;
- if `main` advanced, rebase cleanly and rerun exact-head verification;
- merge through branch protection with expected-head SHA;
- read back protected `main` and merge-commit verification.

## Task 8 — Documentation reconciliation

After merge, update the DGAF Interface & Experience Design Control Area with:

- the V0 discrete-reachability boundary;
- exact candidate and merge SHA;
- panel QA outcome;
- verification matrix;
- explicit statement that full tensor/manifold continuity remains future research/formalization work;
- unchanged scientific/control posture.

## Non-effects

This plan and implementation do not establish materialization, analysis authorization/execution, scientific-N promotion, efficacy, independent validation, deployment health, or High-Assurance authorization. `PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0` remains unchanged.
