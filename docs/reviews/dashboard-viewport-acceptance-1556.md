# Dashboard viewport QA acceptance — draft PR #1556

Status: PROPOSED / NOT EXECUTED. This is a test plan, not a verification report.

## Exact source and dependencies

- Candidate: PR #1556, stacked on unmerged #1411.
- Overlap: sibling PR #1420 supplies comparable confidence segmentation and an isolated QA workflow. Choose one reconciled implementation before protected-main admission.
- Local unit/build checks do **not** establish browser rendering or accessibility.
- Existing root `package.json` lists Next.js build and Node UI contract tests, but no browser automation runner. Do not infer that the legacy `dashboard/components` files are wired into the production Next.js page.

## Observed route boundary (2026-10-31)

- Verified Next.js overview route `app/(command-center)/page.tsx` imports `OverviewView` from `app/components/overview-view.tsx`.
- The current candidate modifies `dashboard/components/PhiTrajectory.jsx`, `OrchestratePanel.jsx`, and `TurnTable.jsx`. The verified overview route does **not** directly import these legacy components.
- Do not infer that the dashboard chart is rendered from the Next.js build; confirm a real route and import chain or create a separately authorized, explicitly labeled preview surface.
- Do not present an unmounted legacy UI as an integrated command-center feature.

## Prerequisites

1. Confirm the real dashboard route/entry point and how it imports `OrchestratePanel`, `TurnTable`, and `PhiTrajectory`. If it is not deployed, record **NOT EXECUTED** and avoid claiming browser QA.
2. Use a trusted preview of the exact reviewed candidate, with no live authority or private data. Synthetic fixtures only.
3. Capture browser/runtime version, viewport, device scale, candidate commit and screenshots/video when permitted.

## Scenarios and oracles

| Case | Fixture | Expected observable behavior |
| --- | --- | --- |
| Mobile viewport | 320x640 and 375x812 | No horizontal overflow attributable to confidence SVG; controls and labels remain readable |
| Desktop viewport | 1280x800 | Chart axes, reference line and markers remain visible |
| Missing series | Empty records, all-null effective confidence | Explicit `No observed confidence values are available` status; no data polyline |
| Broken series | 0.2, null, 0.8 | Two isolated observations, no interpolating line |
| Malformed series | NaN, Infinity, negative, greater than 1, string | No synthesized numeric points |
| Diagnostic PASS | decision PASS, evidence.status PASS | No green admission appearance; local response is not authorization |
| Partial evidence | decision PASS, evidence.status PARTIAL | Clearly qualified, not presented as approved |
| Blocked/rejected | BLOCKED, REJECT, KILL with absent confidence | Color-independent blocked marker and table status; no invented confidence |
| Keyboard/screen reader | Focus navigation and chart inspection | Accessible label/title/status; no information conveyed by color alone |

## Evidence and pass criteria

Mark each scenario PASS/FAIL/NOT EXECUTED with exact screenshot or reproduction link, browser/runtime and commit SHA. A single failing case blocks viewport-acceptance, but does not silently change release or scientific status. Source-pattern tests and hosted Next.js build are separate evidence classes and must not be substituted for browser outcomes.

No merge, security exception, Gate 0 promotion, independent scientific validation, High Assurance authorization or N increment is implied.

## Default-branch code-search evidence (2026-10-31)

GitHub repository code search on protected main `1a95b94332dffb404c5a3ce026d70781a8c10b90` for `PhiTrajectory`, `OrchestratePanel`, and `TurnTable` returned only each respective legacy component definition (no importer match). Search for `overview-view` returned the App Router overview page plus tests; `/` renders `OverviewView`. This supports **not wired in the searched default-branch index**, not a mathematically exhaustive negative across draft refs, generated code, or runtime dynamic imports. Route-level visual acceptance remains NOT EXECUTED. A testable preview should be explicitly isolated and reviewed rather than portrayed as the live production dashboard.
