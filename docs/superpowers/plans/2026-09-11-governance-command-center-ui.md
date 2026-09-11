# DGAF Governance Command Center UI Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the current debug-style ensemble dashboard with a responsive, accessible, truth-preserving DGAF Governance Command Center while retaining the existing health, audit, roster, and P-07 sweep functionality.

**Architecture:** Keep the existing hybrid Next.js application and Pages Router APIs. Move raw transport, response validation, state semantics, public translation, and governance display data into focused modules; keep `app/page.tsx` as composition. A project-local CSS design system provides the dark visual language without adding a component framework.

**Tech Stack:** Next.js 16.3.4, React 18.3.1, TypeScript 5.8.3, Node 24.x, existing Pages Router APIs, CSS custom properties, Node built-in test runner for pure TypeScript modules.

**Spec:** `docs/superpowers/specs/2026-09-11-governance-command-center-ui-design.md` plus factual correction `docs/superpowers/specs/2026-09-11-governance-command-center-ui-correction.md`.

## Global Constraints

- Preserve **PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0** and **efficacy NOT ESTABLISHED** as the canonical High-Assurance/public truth boundary until an authoritative later record changes it.
- Scientific-state effect: **NONE**. Authority effect: **NONE**.
- Existing transport remains `pages/api/health.ts`, `pages/api/audit.ts`, `pages/api/roster.ts`, and `pages/api/sweep.ts`; do not create duplicate App Router endpoints.
- `/api/audit` counters are ephemeral serverless runtime telemetry, not durable governance evidence.
- `/api/sweep` is non-mutating; `harmonic_score: null` / `NOT_COMPUTED` must never be rendered as a computed score.
- Public functional labels lead; DGAF codenames are secondary context.
- Loading, unknown, unavailable, stale, pass, verified, not-authorized, not-established, and failed states remain semantically distinct.
- No private keys, passphrases, encrypted custody backups, blinding secrets, or recoverable secret material may enter frontend code, payload examples, fixtures, logs, or UI copy.
- Do not add a large UI/component framework or external font dependency.
- Target WCAG 2.2 AA behavior; state is never conveyed by color alone.

---

## File Structure

**Create**
- `app/lib/types.ts` — raw API and normalized UI domain types.
- `app/lib/status.ts` — status normalization and display metadata.
- `app/lib/status.test.ts` — semantic-state regression tests.
- `app/lib/api.ts` — fetch/validation functions for existing API contracts.
- `app/lib/api.test.ts` — pure validator tests for valid/malformed payloads.
- `app/lib/governance.ts` — non-authoritative display snapshot of current ordered governance lifecycle and evidence boundary.
- `app/lib/public-translation.ts` — functional labels for runtime roster identities.
- `app/hooks/use-dashboard-data.ts` — polling, last-valid snapshot, freshness, retry behavior.
- `app/components/icons.tsx` — dependency-free SVG icon primitives.
- `app/components/status-chip.tsx` — semantic status rendering.
- `app/components/app-shell.tsx` — responsive navigation/header shell.
- `app/components/overview-view.tsx` — public/external overview.
- `app/components/control-room-view.tsx` — runtime telemetry and operational condition.
- `app/components/governance-view.tsx` — lifecycle rail and next transition.
- `app/components/agents-view.tsx` — searchable/filterable runtime agents and formations.
- `app/components/evidence-view.tsx` — evidence legend and Epoch 001/002 boundaries.
- `app/components/tools-view.tsx` — improved P-07 sweep working surface.
- `app/styles/globals.css` — design tokens, responsive layout, component primitives, accessibility states.

**Modify**
- `app/layout.tsx` — import global CSS and update metadata/body structure.
- `app/page.tsx` — replace monolith with command-center composition.
- `package.json` — add a zero-dependency UI logic test script.

**Do not modify unless verification exposes a contract defect**
- `pages/api/health.ts`
- `pages/api/audit.ts`
- `pages/api/roster.ts`
- `pages/api/sweep.ts`

---

### Task 1: Lock semantic states with failing tests

**Files:**
- Create: `app/lib/status.test.ts`
- Create after RED: `app/lib/types.ts`
- Create after RED: `app/lib/status.ts`
- Modify: `package.json`

**Interfaces:**
- Produces `UiState`, `StatusMeta`, `STATUS_META`, `statusMeta(state)` and `normalizeRuntimeStatus(value)`.

- [ ] **Step 1: Add the test command only**

Add `"test:ui": "node --test app/lib/*.test.ts"` to `scripts` without adding dependencies.

- [ ] **Step 2: Write failing semantic-state tests**

Test that:
- `loading` maps to a neutral label/tone, never failed/denied;
- `pass` and `verified` have distinct labels;
- `not_authorized` and `not_established` remain distinct;
- unknown input normalizes to `unknown`;
- runtime `ok` normalizes to `pass` but does not imply `verified`.

- [ ] **Step 3: Run RED**

Run `npm run test:ui`. Expected: failure because `status.ts` does not exist.

- [ ] **Step 4: Implement minimal types and status metadata**

Create the exact union from the approved spec and a semantic metadata record with label, tone, and explanation. Do not use raw hex colors in TypeScript; CSS consumes the tone through `data-tone`.

- [ ] **Step 5: Run GREEN**

Run `npm run test:ui`. Expected: all semantic-state tests pass.

- [ ] **Step 6: Commit**

Commit message: `test(ui): lock command center state semantics`.

---

### Task 2: Validate existing API contracts without replacing them

**Files:**
- Create: `app/lib/api.test.ts`
- Create after RED: `app/lib/api.ts`
- Extend: `app/lib/types.ts`

**Interfaces:**
- Produces `validateHealthData`, `validateAuditData`, `validateRosterData`, `validateSweepResult`, `fetchDashboardSnapshot`, and `runSweep`.
- `fetchDashboardSnapshot` returns a typed snapshot only when all three GET payloads are structurally valid.

- [ ] **Step 1: Write failing validator tests**

Cover one valid and one malformed payload for health, audit, roster, and sweep. Explicitly assert that a sweep with `harmonic_score: null` and `harmonic_score_status: 'NOT_COMPUTED'` is valid.

- [ ] **Step 2: Run RED**

Run `npm run test:ui`. Expected: validator imports fail because `api.ts` does not exist.

- [ ] **Step 3: Implement structural validators**

Use small type guards; no schema library dependency. Reject malformed success payloads with descriptive `Error` instances.

- [ ] **Step 4: Implement transport wrappers**

`fetchDashboardSnapshot` GETs `/api/health`, `/api/audit`, `/api/roster` in parallel, checks `response.ok`, validates payloads, and returns the typed snapshot. `runSweep(targets)` POSTs `/api/sweep`, validates HTTP success and response shape, and returns the result.

- [ ] **Step 5: Run GREEN**

Run `npm run test:ui`. Expected: all validator and semantic tests pass.

- [ ] **Step 6: Commit**

Commit message: `feat(ui): validate existing dashboard API contracts`.

---

### Task 3: Encode current governance/public translation display data

**Files:**
- Create: `app/lib/governance.ts`
- Create: `app/lib/public-translation.ts`
- Extend: `app/lib/status.test.ts`

**Interfaces:**
- `TRUTH_BOUNDARY`: display-only current state with explicit source/date.
- `GOVERNANCE_STAGES`: ordered stage objects with `predicateState` and optional `toolingPrepared`.
- `EPOCH_SUMMARIES`: exact current Epoch 001/002 public boundary.
- `agentDisplayName(id)`: functional label first, codename second where mapped.

- [ ] **Step 1: Add failing assertions**

Assert that the truth boundary includes `PRE-FREEZE`, `FAIL-CLOSED`, `NOT AUTHORIZED`, `N=0`, and `EFFICACY NOT ESTABLISHED`; assert that repository custody is `not_established` and collection is `not_authorized`; assert translation for `amethyst`, `colleen`, `apogee`, and legacy runtime id `demijole`.

- [ ] **Step 2: Run RED**

Expected: imports do not exist.

- [ ] **Step 3: Implement display snapshot and translation map**

Source wording from `docs/PROJECT_STATUS.md` and `docs/PUBLIC_TRANSLATION_LAYER.md`. Mark the snapshot as presentation data with `sourceUpdated: '2026-09-11'`; do not call it an authority source.

- [ ] **Step 4: Run GREEN**

All pure tests pass.

- [ ] **Step 5: Commit**

Commit message: `feat(ui): bind public labels and governance display state`.

---

### Task 4: Build the project-local dark design system and shell

**Files:**
- Create: `app/styles/globals.css`
- Create: `app/components/icons.tsx`
- Create: `app/components/status-chip.tsx`
- Create: `app/components/app-shell.tsx`
- Modify: `app/layout.tsx`

**Interfaces:**
- `StatusChip({ state, label? })`
- `AppShell({ activeView, onNavigate, children, runtimeMeta })`

- [ ] **Step 1: Create CSS tokens and accessibility primitives**

Use graphite canvas/surfaces, restrained cyan primary accent, violet secondary accent, semantic green/amber/red/neutral tones, system sans UI stack, system mono technical stack, visible `:focus-visible`, reduced-motion media query, and mobile/tablet/desktop breakpoints.

- [ ] **Step 2: Build status chip and icon primitives**

Icons are inline SVG with `aria-hidden` when decorative. Status chips include textual labels and semantic `data-tone` attributes so color is supplemental.

- [ ] **Step 3: Build responsive shell**

Desktop: left navigation + top command header. Mobile: compact header + menu control + stacked content. Navigation items: Overview, Control Room, Governance, Agents & Formations, Evidence & Research, Tools.

- [ ] **Step 4: Update root layout**

Import `./styles/globals.css`, replace inline body styling, and use metadata title `DGAF — Governance Command Center` with an industry-neutral description.

- [ ] **Step 5: Run `npm run build`**

Expected: Next production build succeeds before view work continues.

- [ ] **Step 6: Commit**

Commit message: `feat(ui): add governance command center design system`.

---

### Task 5: Implement polling with last-valid/stale semantics

**Files:**
- Create: `app/hooks/use-dashboard-data.ts`

**Interfaces:**
- Produces `{ snapshot, phase, error, lastSuccessAt, refresh }`.
- `phase` is `loading | fresh | stale | error`.

- [ ] **Step 1: Implement hook using tested transport**

Poll every 10 seconds, matching existing behavior. On first failure with no snapshot, expose error. On later failure, retain the last valid snapshot and expose stale state. Clear interval on unmount.

- [ ] **Step 2: Ensure screen-reader quiet refresh**

Do not use an assertive live region for each successful poll. Error/freshness text is visible but non-noisy.

- [ ] **Step 3: Run `npm run build`**

Expected: type/build success.

- [ ] **Step 4: Commit**

Commit message: `feat(ui): preserve last valid telemetry during poll failures`.

---

### Task 6: Implement Overview and Control Room

**Files:**
- Create: `app/components/overview-view.tsx`
- Create: `app/components/control-room-view.tsx`

**Interfaces:**
- `OverviewView({ onNavigate })`
- `ControlRoomView({ snapshot, phase, error, lastSuccessAt, onRefresh })`

- [ ] **Step 1: Build Overview**

Include product statement, prominent Truth Boundary, engineering-evidence-vs-efficacy explanation, Epoch 001/002 cards, current next admissible transition, and quick navigation actions. Do not present static truth-boundary copy as live API state.

- [ ] **Step 2: Build Control Room**

Display health, runtime/version, adapters, audit telemetry, freshness, cold-start warning, and compact lifecycle summary. Label audit counters as ephemeral when cold-start/in-memory warning is present.

- [ ] **Step 3: Verify negative-state treatment**

No initial loading badge may appear destructive red. Missing data renders neutral unknown/unavailable state.

- [ ] **Step 4: Run `npm run build`**

- [ ] **Step 5: Commit**

Commit message: `feat(ui): add overview and control room surfaces`.

---

### Task 7: Implement Governance and Evidence & Research

**Files:**
- Create: `app/components/governance-view.tsx`
- Create: `app/components/evidence-view.tsx`

**Interfaces:**
- `GovernanceView()` consumes only `GOVERNANCE_STAGES`/truth display data.
- `EvidenceView()` consumes `EPOCH_SUMMARIES` and evidence-state legend.

- [ ] **Step 1: Build ordered lifecycle rail**

Render all stages in exact predecessor order. Separate `toolingPrepared` from predicate state so later preparation never looks like established progression.

- [ ] **Step 2: Build next-transition callout**

Current next transition: repository admission of the exact existing non-secret custody certificate and receipt; include the prohibition against regenerating/substituting them.

- [ ] **Step 3: Build evidence legend and epoch comparison**

Explain PASS vs VERIFIED, non-independent vs independent verification, NOT AUTHORIZED vs NOT ESTABLISHED, and empirical evidence. Render Epoch 001 and successor Epoch 002 with the exact current public ceilings.

- [ ] **Step 4: Run `npm run build`**

- [ ] **Step 5: Commit**

Commit message: `feat(ui): visualize governance lifecycle and evidence boundaries`.

---

### Task 8: Implement Agents & Formations for internal and external readers

**Files:**
- Create: `app/components/agents-view.tsx`

**Interfaces:**
- `AgentsView({ roster })`

- [ ] **Step 1: Build search/filter controls**

Filter by free-text functional/codename/role text, tier, and runtime status. Use associated labels and keyboard-operable native controls.

- [ ] **Step 2: Build responsive agent cards**

Lead with `agentDisplayName(id)`, show runtime tier/status/role secondarily, and show formation/triad membership without claiming that the API snapshot is the entire canonical ontology.

- [ ] **Step 3: Build formation cards**

Render returned triads with type, member functional labels, and use case. Preserve API facts without inferring governance authority.

- [ ] **Step 4: Add explicit ontology note**

State that runtime roster presentation is not the authority for sovereign identity adjudication; link/copy-point to the public translation/ontology documentation path.

- [ ] **Step 5: Run `npm run build`**

- [ ] **Step 6: Commit**

Commit message: `feat(ui): add translated agent and formation explorer`.

---

### Task 9: Rebuild P-07 Sweep as a safe working surface

**Files:**
- Create: `app/components/tools-view.tsx`

**Interfaces:**
- `ToolsView()` calls tested `runSweep`.

- [ ] **Step 1: Implement target parsing and validation**

Trim lines, remove blanks, reject an empty target set before network submission, and associate error text with the textarea.

- [ ] **Step 2: Implement request states**

Idle, running, success, empty-findings, malformed/error. Disable submit while running.

- [ ] **Step 3: Render findings**

Severity filters for HIGH/MEDIUM/LOW/INFO; show agent, target, and message. Distinguish planned remediation candidates from performed mutations; surface `mutation_performed: false`.

- [ ] **Step 4: Render harmonic state truthfully**

If `harmonic_score` is null, display `NOT COMPUTED`, never a placeholder number or gauge.

- [ ] **Step 5: Add safe copy/export**

Copy the non-secret JSON response through `navigator.clipboard` when available; fallback to a visible status message if unavailable. No automatic download or secret collection.

- [ ] **Step 6: Run `npm run build`**

- [ ] **Step 7: Commit**

Commit message: `feat(ui): rebuild P-07 sweep workspace`.

---

### Task 10: Compose the command center and remove the monolith

**Files:**
- Modify: `app/page.tsx`

**Interfaces:**
- `Dashboard` owns only selected view and hook composition.

- [ ] **Step 1: Replace inline-styled page implementation**

Use `AppShell` and route the six in-page views from one selected-view state. Keep no raw API parsing or large style objects in `page.tsx`.

- [ ] **Step 2: Provide useful loading content**

Overview/Governance/Evidence remain usable from static display data while runtime telemetry loads. Runtime-dependent views use neutral loading placeholders.

- [ ] **Step 3: Run tests and build**

Run `npm run test:ui` and `npm run build`; both must exit 0.

- [ ] **Step 4: Commit**

Commit message: `feat(ui): compose DGAF governance command center`.

---

### Task 11: Exact-head repository and preview verification

**Files:** none unless fixes are required.

- [ ] **Step 1: Self-review against spec**

Check all six navigation surfaces, Truth Boundary wording, lifecycle order, API handling, sweep semantics, accessibility requirements, no-secret boundary, and non-goals.

- [ ] **Step 2: Open PR against `main`**

PR body must explicitly state scientific-state effect `NONE`, authority effect `NONE`, no experiment authorization, and that runtime APIs were preserved.

- [ ] **Step 3: Inspect exact-head checks**

Require repository-mandated checks plus npm lock/build validation to complete successfully. Do not transfer evidence from older heads.

- [ ] **Step 4: Inspect Vercel preview or explicit deployment**

Verify desktop and mobile composition, navigation, loading, stale/error semantics, roster filtering, and sweep interaction. If automatic preview is unavailable because deployment is disabled, use the project’s explicit deployment path without treating deployment readiness as scientific evidence.

- [ ] **Step 5: Keyboard/accessibility smoke**

Verify skip/focus order where applicable, menu/navigation controls, form labels, visible focus, no color-only status, and reduced-motion CSS.

- [ ] **Step 6: Merge decision**

Only recommend merge after the exact PR head has all required checks green and visual/runtime verification shows no blocking regression. Do not merge merely because code review looks correct.
