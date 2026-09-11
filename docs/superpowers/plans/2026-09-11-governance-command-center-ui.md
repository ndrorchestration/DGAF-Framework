# DGAF Governance Command Center UI Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Replace the current debug-style ensemble dashboard with a responsive, accessible, truth-preserving DGAF Governance Command Center while retaining the existing health, audit, roster, and P-07 sweep functionality.

**Architecture:** Keep the existing hybrid Next.js application and Pages Router APIs. Move transport, validation, state semantics, public translation, governance display data, polling, and presentation into focused modules. Keep `app/page.tsx` as composition and use project-local CSS instead of a component framework.

**Tech Stack:** Next.js 16.3.4, React 18.3.1, TypeScript 5.8.3, Node 24.x, existing Pages Router APIs, CSS custom properties, and the Node built-in test runner.

**Spec:** `docs/superpowers/specs/2026-09-11-governance-command-center-ui-design.md` plus `docs/superpowers/specs/2026-09-11-governance-command-center-ui-correction.md`.

## Global Constraints

- Preserve **PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0** and canonical efficacy **NOT ESTABLISHED** until an authoritative later record changes them.
- Scientific-state effect is **NONE** and authority effect is **NONE**.
- Preserve `pages/api/health.ts`, `pages/api/audit.ts`, `pages/api/roster.ts`, and `pages/api/sweep.ts` as the existing transport.
- Treat audit counters as ephemeral serverless telemetry rather than durable governance evidence.
- Treat P-07 sweep as non-mutating and render a null harmonic score as **NOT COMPUTED**.
- Lead public presentation with functional labels and use DGAF codenames as secondary context.
- Keep loading, unknown, unavailable, stale, pass, verified, not-authorized, not-established, and failed states semantically distinct.
- Keep private keys, passphrases, encrypted custody backups, blinding secrets, and recoverable secret material out of frontend code, fixtures, payload examples, logs, and UI copy.
- Do not add a large component framework or external font dependency.
- Target WCAG 2.2 AA behavior and never convey state by color alone.

## File Map

### New modules

- `app/lib/types.ts` defines raw API and normalized UI domain types.
- `app/lib/status.ts` defines state normalization and display metadata.
- `app/lib/status.test.ts` locks semantic state behavior.
- `app/lib/api.ts` validates and fetches existing API contracts.
- `app/lib/api.test.ts` covers valid and malformed contracts.
- `app/lib/governance.ts` holds the presentation-only current lifecycle and evidence boundary.
- `app/lib/public-translation.ts` maps runtime identities to public-first labels.
- `app/hooks/use-dashboard-data.ts` owns polling, freshness, and last-valid snapshots.
- `app/components/*.tsx` contains bounded presentation surfaces and primitives.
- `app/styles/globals.css` contains tokens, responsive layout, accessibility states, and shared component styling.

### Modified modules

- `app/layout.tsx` imports global CSS and updates metadata.
- `app/page.tsx` becomes composition-only.
- `package.json` adds the zero-dependency UI logic test command.
- `tsconfig.json` permits explicit TypeScript extensions required by the Node test runner.
- `.github/workflows/ui-command-center-validation.yml` runs UI tests and the production build on relevant pull-request changes.

### Existing API routes retained

- `pages/api/health.ts`
- `pages/api/audit.ts`
- `pages/api/roster.ts`
- `pages/api/sweep.ts`

## Task 1: Lock Semantic States

**Interfaces:** `UiState`, `StatusMeta`, `STATUS_META`, `statusMeta(state)`, and `normalizeRuntimeStatus(value)`.

- [x] Add `npm run test:ui` without adding dependencies.
- [x] Write tests before production state code.
- [x] Observe RED because `status.ts` does not exist.
- [x] Implement the state union and semantic metadata.
- [x] Observe GREEN with all semantic tests passing.
- [x] Confirm the production Next build succeeds on the exact head.

## Task 2: Validate Existing API Contracts

**Interfaces:** `validateHealthData`, `validateAuditData`, `validateRosterData`, `validateSweepResult`, `fetchDashboardSnapshot`, and `runSweep`.

- [x] Add valid and malformed contract tests before `api.ts` exists.
- [x] Include the nullable `harmonic_score` and `NOT_COMPUTED` sweep case.
- [x] Observe RED because the adapter module does not exist.
- [x] Implement dependency-free structural validation and transport wrappers.
- [x] Preserve the existing Pages Router endpoints rather than duplicating them.
- [x] Observe GREEN for semantic and API tests.
- [x] Confirm the production Next build succeeds on the exact head.

## Task 3: Lock Governance and Public Translation

**Interfaces:** `TRUTH_BOUNDARY`, `GOVERNANCE_STAGES`, `NEXT_TRANSITION`, `EPOCH_SUMMARIES`, `EVIDENCE_STATES`, and `agentDisplayName(id)`.

- [x] Add tests for the current truth boundary before the display modules exist.
- [x] Add tests proving prepared tooling does not imply an established predicate.
- [x] Add tests for public-first agent labels, including the legacy runtime id `demijole`.
- [x] Observe RED before the governance and translation modules exist.
- [x] Implement the presentation-only lifecycle and translation maps from current canonical documentation.
- [x] Observe GREEN for the expanded test suite.
- [x] Confirm the production Next build succeeds on the exact head.

## Task 4: Build the Dark Design System and Shell

**Interfaces:** `StatusChip`, dependency-free icon primitives, `AppShell`, and the six-view navigation model.

- [x] Create graphite, cyan, violet, and semantic state tokens in CSS custom properties.
- [x] Use system sans for narrative UI and monospace only for technical material.
- [x] Add visible focus states, practical touch targets, and reduced-motion handling.
- [x] Build the desktop sidebar, command header, and mobile navigation drawer.
- [x] Update root metadata to `DGAF — Governance Command Center`.

## Task 5: Preserve Last-Valid Runtime Telemetry

**Interface:** `useDashboardData(refreshMs)` returns `snapshot`, `phase`, `error`, `lastSuccessAt`, and `refresh`.

- [x] Poll every 10 seconds through the validated transport layer.
- [x] Abort superseded requests and clean up the interval on unmount.
- [x] Keep the last valid snapshot when a later refresh fails.
- [x] Distinguish initial error from stale-but-usable data.
- [x] Avoid noisy screen-reader announcements for routine polling.

## Task 6: Implement Overview and Control Room

- [x] Build a public-first Overview with DGAF purpose, Truth Boundary, conceptual pillars, Epoch summaries, and next admissible transition.
- [x] Keep static governance truth separate from live runtime telemetry.
- [x] Build Control Room health, version, PSI check, adapters, constants, audit telemetry, freshness, cold-start, stale, and error states.
- [x] Label audit counters as ephemeral runtime telemetry.
- [x] Ensure loading and missing data never appear as destructive failures by default.

## Task 7: Implement Governance and Evidence Surfaces

- [x] Render the exact ordered lifecycle from repository custody through locked analysis.
- [x] Show `toolingPrepared` separately from each predicate state.
- [x] Highlight the exact existing custody artifacts as the next admissible transition.
- [x] Preserve the prohibition against regenerating or substituting custody evidence.
- [x] Build the evidence-state legend and exact Epoch 001 and Epoch 002 claim ceilings.
- [x] Keep canonical efficacy visibly **NOT ESTABLISHED**.

## Task 8: Implement Agents and Formations

- [x] Search agents by public function, codename, runtime role, and formation terms.
- [x] Filter by runtime tier and status.
- [x] Lead cards with public functional labels and show runtime facts secondarily.
- [x] Render returned formations without inferring governance authority.
- [x] State explicitly that the runtime roster is not the authority for sovereign identity adjudication.

## Task 9: Rebuild the P-07 Sweep Workspace

- [x] Parse and deduplicate repository-relative target paths.
- [x] Reject an empty target set before submission.
- [x] Model idle, running, error, validated success, empty-filter, and clipboard states.
- [x] Disable duplicate submission while the sweep is running.
- [x] Filter findings by severity.
- [x] Surface `mutation_performed: false` when present.
- [x] Render a null harmonic score as **NOT COMPUTED** rather than a placeholder metric.
- [x] Allow safe copying of the validated non-secret JSON response.

## Task 10: Compose and Build the Integrated Command Center

- [x] Replace the old monolithic `app/page.tsx` with a composition-only page.
- [x] Keep Overview, Governance, and Evidence useful even before live telemetry arrives.
- [x] Batch the integrated visual implementation so CI evaluates the application as a coherent unit.
- [x] Confirm the repository NPM lock/build gate completes successfully on integrated head `e76aa43b1fe95faba1313a2d48f5b750e4758faa`.

## Task 11: Exact-Head Review, Preview, and Merge Decision

- [ ] Keep the PR in draft while implementation verification is incomplete.
- [ ] Remove only new documentation-lint debt introduced by this plan.
- [ ] Require `npm run test:ui` and `npm run build` on the final exact head.
- [ ] Require repository-mandated governance checks on the final exact head.
- [ ] Inspect the deployed UI at desktop and mobile widths.
- [ ] Smoke-test keyboard focus, mobile navigation, loading, stale/error states, roster filtering, and the P-07 sweep interaction.
- [ ] Verify the displayed Truth Boundary still matches the current canonical state.
- [ ] Mark the PR ready only after exact-head validation and visual verification have no blocking defect.
- [ ] Recommend merge only after required exact-head checks are green.
