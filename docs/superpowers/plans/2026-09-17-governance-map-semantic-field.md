# Governance Map Semantic Field Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a presentation-only Governance Map that exposes vertical escalation, lateral coupling, global constraints, and provenance while preserving the existing canonical governance model.

**Architecture:** Derive the map from `GOVERNANCE_STAGES`, `TRUTH_BOUNDARY`, and a small presentation-only relationship registry. Render the map inside the existing Governance view before the detailed lifecycle, with no new backend or authority state.

**Tech Stack:** Next.js 16, React, TypeScript, Node test runner, CSS.

**Spec:** `docs/superpowers/specs/2026-09-17-governance-map-semantic-field-design.md`

## Global Constraints

- Preserve **PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0**.
- `GOVERNANCE_STAGES` remains the only lifecycle source.
- `TRUTH_BOUNDARY` remains the only global constraint source.
- No readiness percentages, inferred authorization, efficacy score, or continuous manifold semantics.
- Every lateral relationship must resolve to canonical stage IDs and expose a `doesNotEstablish` boundary.
- Presentation-only changes must not mutate scientific or authorization predicates.

---

### Task 1: Define the Governance Map semantic contract

**Files:**

- Create: `app/lib/governance-map.test.ts`
- Create: `app/lib/governance-map.ts`

**Interfaces:**

- Consumes: `GOVERNANCE_STAGES`, `TRUTH_BOUNDARY` from `app/lib/governance.ts`.
- Produces: `GOVERNANCE_MAP`, `GOVERNANCE_RELATIONSHIPS`, `GovernanceMapRelationship`.

- [ ] **Step 1: Write the failing semantic test** proving the map derives its ordered stages from canonical governance state, exposes the current materialization blocker, validates all relationship endpoints, preserves global constraints, and contains no readiness score.
- [ ] **Step 2: Trigger `npm run test:ui` on the test-only head and verify RED because `./governance-map.ts` does not exist.**
- [ ] **Step 3: Implement the minimal `governance-map.ts` projection** with four explicit relationships: custody→operator evidence admission, dataset lock→unblinding, materialization→analysis authorization, analysis authorization→locked analysis.
- [ ] **Step 4: Re-run UI semantic tests and require GREEN.**

### Task 2: Render the structural Governance Map

**Files:**

- Create: `app/components/governance-map.tsx`
- Modify: `app/components/governance-view.tsx`
- Modify: `app/lib/governance-map.test.ts`

**Interfaces:**

- Consumes: `GOVERNANCE_MAP` and `GOVERNANCE_RELATIONSHIPS`.
- Produces: `<GovernanceMap />` presentation component.

- [ ] **Step 1: Extend the failing test** to require `<GovernanceMap />` in the Governance view before the detailed lifecycle and forbid a second local lifecycle registry.
- [ ] **Step 2: Verify RED on the exact test-only head.**
- [ ] **Step 3: Implement `<GovernanceMap />`** with an enclosing global-constraint frame, vertical stage spine, explicit blocking boundary, and relationship inspector text.
- [ ] **Step 4: Insert `<GovernanceMap />` in `governance-view.tsx` before `.lifecycle`.**
- [ ] **Step 5: Re-run UI tests and production build; both must pass.**

### Task 3: Add DGAF-specific visual grammar and responsive semantics

**Files:**

- Create: `app/styles/governance-map.css`
- Modify: `app/layout.tsx`
- Modify: `app/lib/governance-map.test.ts`

**Interfaces:**

- Consumes: semantic class names emitted by `<GovernanceMap />`.
- Produces: map-specific state rail, boundary band, relationship filament, global constraint frame, mobile collapse, and reduced-motion behavior.

- [ ] **Step 1: Add semantic source assertions** for non-color-only labels, relationship provenance text, global constraint labels, and the authority/authorization distinction.
- [ ] **Step 2: Add dedicated CSS** for `.governance-map`, `.governance-field-frame`, `.governance-spine`, `.governance-node`, `.governance-boundary-band`, `.governance-relations`, and responsive/reduced-motion rules.
- [ ] **Step 3: Load `governance-map.css` from `app/layout.tsx`.**
- [ ] **Step 4: Run `npm run test:ui` and `npm run build`.**

### Task 4: Verify and prepare a draft PR

**Files:**

- No new production files.

- [ ] **Step 1: Open a draft PR against `main` with exact scope and explicit scientific/control non-effects.**
- [ ] **Step 2: Verify all exact-head GitHub workflow families.**
- [ ] **Step 3: Fix only evidenced failures; do not broaden scope.**
- [ ] **Step 4: Reconcile the DGAF Interface & Experience Design Control Area in Notion only after exact-head verification is known.**
