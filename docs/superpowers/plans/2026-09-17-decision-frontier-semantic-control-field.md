# Decision Frontier Semantic Control Field Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Turn the Control Room's existing next-transition summary into a first-class Decision Frontier that visually exposes current governed state, the blocking boundary, nearest admissible transition, downstream unreachable transitions, consequence, and provenance without creating a parallel state engine.

**Architecture:** Derive a presentation-only `DECISION_FRONTIER` object directly from `GOVERNANCE_STAGES` and existing governance copy. Render that object through a dedicated `DecisionFrontier` component and integrate it at the top of the Control Room before runtime telemetry. Style it through project-local CSS using semantic structure, not percentage readiness or decorative-only motion.

**Tech Stack:** Next.js 16.3.4, React 18.3.1, TypeScript 5.8.3, project-local CSS, Node test runner.

**Spec:** `docs/superpowers/specs/2026-09-11-governance-command-center-ui-design.md`

## Global Constraints

- Presentation-only: no governance, authorization, scientific-state, efficacy, empirical-N, or runtime-authority mutation.
- One truth model: derive from `GOVERNANCE_STAGES`; do not duplicate canonical lifecycle state.
- Preserve `pass`, `not_established`, `not_authorized`, `unknown`, `unavailable`, and `blocked` as distinct semantics.
- No readiness percentages, composite scores, or inferred authorization.
- Color is never the sole carrier of state.
- Motion, if present, must clarify causality and honor `prefers-reduced-motion`.
- Existing runtime observability remains explicitly subordinate to governance authority.

---

### Task 1: Derive the Decision Frontier model

**Files:**

- Create: `app/lib/decision-frontier.ts`
- Test: `app/lib/decision-frontier.test.ts`

**Interfaces:**

- Consumes: `GOVERNANCE_STAGES` and `UiState`.
- Produces: `DECISION_FRONTIER` with `current`, `blocking`, `nearest`, `downstream`, `why`, `consequence`, and source/provenance fields.

- [x] **Step 1: Write the failing semantic contract**

The RED test already exists on PR #776 and asserts the accepted unblinding state, materialization blocker, unreachable analysis stages, consequence text, and absence of readiness scores.

- [ ] **Step 2: Run the focused test and preserve RED evidence**

Run: `npm run test:ui`
Expected before implementation: FAIL only because `app/lib/decision-frontier.ts` is absent.

- [ ] **Step 3: Implement the minimal derived model**

Implement helpers that find stages by id and fail closed if a required stage is missing. Do not hard-code independent status values that can drift from `GOVERNANCE_STAGES`.

- [ ] **Step 4: Run focused semantic tests**

Run: `npm run test:ui`
Expected: all UI semantic tests pass.

### Task 2: Render the flagship Decision Frontier component

**Files:**

- Create: `app/components/decision-frontier.tsx`
- Modify: `app/components/control-room-view.tsx`

**Interfaces:**

- Consumes: `DECISION_FRONTIER` and existing `StatusChip`.
- Produces: a semantic section exposing current state → why → blocking boundary → nearest admissible transition → downstream prohibited transitions → consequence/provenance.

- [ ] **Step 1: Add semantic markup**

Use a `<section>` with explicit headings and labeled regions. Each transition must display text plus a `StatusChip`; state must not rely on color alone.

- [ ] **Step 2: Put Decision Frontier before runtime metrics**

Integrate the new component immediately after the Control Room page heading and stale/error notice, before `metric-grid`, so governance hierarchy precedes telemetry.

- [ ] **Step 3: Remove the old bottom-only `NEXT_TRANSITION` card**

Avoid two competing frontier summaries. Runtime observability remains present but secondary.

- [ ] **Step 4: Build**

Run: `npm run build`
Expected: SUCCESS.

### Task 3: Establish the Semantic Control Field visual grammar

**Files:**

- Modify: `app/styles/globals.css`

**Interfaces:**

- Consumes: existing design tokens and responsive conventions.
- Produces: reusable `decision-frontier-*` styles for state node, boundary, transition path, provenance, consequence, and downstream denied/unreachable states.

- [ ] **Step 1: Add a distinct frontier container**

Use layered borders/surfaces and structural lines to encode current state, boundary, and transition direction. Avoid neon spectacle or generic KPI-card repetition.

- [ ] **Step 2: Differentiate semantic structures**

Current state, blocking boundary, admissible transition, and unreachable downstream states must differ by geometry/layout in addition to text and status chips.

- [ ] **Step 3: Add responsive behavior**

At narrow widths, preserve reading order and relationships rather than merely shrinking the desktop composition.

- [ ] **Step 4: Add reduced-motion equivalence**

Any transition/hover motion must be disabled or simplified under `prefers-reduced-motion` without loss of meaning.

### Task 4: Exact-head verification and PR reconciliation

**Files:**

- No new product files unless validation exposes a defect.

- [ ] **Step 1: Run UI semantic suite**

Run: `npm run test:ui`
Expected: PASS.

- [ ] **Step 2: Run production build**

Run: `npm run build`
Expected: PASS.

- [ ] **Step 3: Inspect effective diff**

Confirm the effective delta is presentation-only plus this plan/test and that no scientific/governance authority file is mutated except derived frontend presentation modules.

- [ ] **Step 4: Push exact candidate and require fresh CI**

No validation from the RED head transfers. Require fresh exact-head UI/build/governance workflow results before readiness or merge.

- [ ] **Step 5: Update PR #776 description with final exact-head evidence**

Record exact head, UI test count, build result, workflow disposition, and explicit non-effects.
