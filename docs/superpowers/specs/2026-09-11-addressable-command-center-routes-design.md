# DGAF Addressable Command Center Routes Design

**Date:** 2026-09-11  
**Status:** APPROVED DIRECTION / DESIGN SPEC FOR REVIEW  
**Issue:** #642  
**Branch:** `ui/addressable-command-center-routes-642`  
**Stack base:** PR #649 exact head `4a97f68181da0e343e673b7fc82cab6ba7e2335f`  
**Merge target:** none until #649/#636 dependencies and the preflight-first merge barrier resolve  
**Scope:** frontend routing, shared-shell composition, persistent runtime polling ownership, navigation semantics, route metadata, and routing regression coverage  
**Scientific-state effect:** NONE  
**Authority effect:** NONE

## 1. Purpose

Convert the Governance Command Center's six client-local views into stable, directly addressable Next.js App Router destinations without changing DGAF's runtime API contract, governance predicates, scientific state, authority model, or evidence semantics.

The current implementation stores the selected destination in local React state inside `app/page.tsx`. That works visually, but it prevents durable deep links, normal browser back/forward behavior, route-specific metadata, direct references to a particular control surface, and normal route-level 404 behavior.

The design must make URL state the single source of truth for navigation while preserving one shared shell and one runtime polling owner.

## 2. Required Public Routes

The route contract is fixed unless a later repository convention requires an explicitly reviewed change:

- `/` — Overview
- `/control` — Control Room
- `/governance` — Governance
- `/agents` — Agents & Formations
- `/evidence` — Evidence & Research
- `/tools` — Tools

Unknown routes must follow normal Next.js not-found behavior. No unknown path may silently redirect or coerce to Overview.

## 3. Architectural Decision

Use native Next.js App Router pages under a shared command-center route-group layout.

Recommended structure:

```text
app/
  layout.tsx
  (command-center)/
    layout.tsx
    page.tsx
    control/page.tsx
    governance/page.tsx
    agents/page.tsx
    evidence/page.tsx
    tools/page.tsx
  components/
    dashboard-runtime-provider.tsx
    routed-app-shell.tsx
    ...existing view components
  lib/
    navigation.ts
```

The route group preserves the clean public URLs while giving all six pages one persistent layout boundary.

This approach is preferred over a dynamic `[view]` route because the information architecture is explicit in the filesystem, route-specific metadata is straightforward, and invalid paths naturally fail closed. It is preferred over synchronizing local view state with `router.push()` because that would preserve two competing navigation state sources.

## 4. Route Registry

Create one navigation registry as the canonical presentation-routing contract. It should contain only presentation facts:

- `ViewId`
- public `href`
- label
- short description
- audience-journey stage (`UNDERSTAND`, `VERIFY`, `INSPECT`, `OPERATE`)
- icon identity or icon component reference as appropriate to client/server boundaries

The registry must not contain governance predicates, scientific states, runtime health, or authorization decisions.

Expected mapping:

```text
overview    -> /
evidence    -> /evidence
governance  -> /governance
agents      -> /agents
tools       -> /tools
control     -> /control
```

The audience journey remains:

`UNDERSTAND -> VERIFY -> INSPECT -> OPERATE`

The current #649 ordering is preserved.

## 5. Shared Runtime Provider

`useDashboardData()` remains the sole runtime polling implementation.

Introduce a client `DashboardRuntimeProvider` that calls `useDashboardData()` exactly once and exposes its existing return contract through React context:

- `snapshot`
- `phase`
- `error`
- `lastSuccessAt`
- `refresh`

The provider belongs inside the persistent command-center layout, not inside individual pages.

### Invariants

1. Client-side navigation between command-center routes must not create parallel 10-second polling intervals.
2. A successful runtime snapshot must remain available across client-side navigation.
3. A failed poll after a successful snapshot must continue to produce the existing `stale` behavior rather than erasing the last valid snapshot.
4. An initial failure without any valid snapshot must remain `error`.
5. Runtime observability must not mutate or infer repository governance/scientific state.
6. Navigating to a static page must not start a second poller.

The polling algorithm itself is not redesigned in this PR.

## 6. Shared Routed Shell

Replace the current `activeView` / `onNavigate` shell contract with a routed shell that derives active navigation from the current pathname.

`AppShell` may be renamed to `RoutedAppShell` or adapted in place, but its responsibilities remain bounded to presentation and interaction:

- render the shared sidebar and topbar;
- derive the active route from pathname plus the route registry;
- render primary navigation with `next/link`;
- apply `aria-current="page"` to the active destination;
- preserve mobile drawer state;
- close the mobile drawer after route activation;
- close the drawer on Escape;
- preserve the skip link and `#main-content` target;
- preserve runtime-status labeling as observability only;
- preserve the Truth Beacon and repository-authority boundary.

The shell must not maintain a second `ViewId` state machine.

## 7. Page Composition

Each public route should be a thin page that renders its existing view component.

### `/`

Render `OverviewView`.

Overview CTAs must become actual links to `/governance`, `/evidence`, and `/control`. The overview component should no longer accept an `onNavigate` callback.

### `/control`

Render `ControlRoomView` with data from `DashboardRuntimeProvider`:

- snapshot
- phase
- error
- last success time
- explicit refresh callback

### `/agents`

Render `AgentsView` using the validated roster from the shared runtime snapshot or `null` if no valid snapshot exists.

### `/governance`

Render `GovernanceView`. It must continue to consume repository presentation constants only and must not infer state from runtime health.

### `/evidence`

Render `EvidenceView` with the same repository evidence semantics as before routing.

### `/tools`

Render `ToolsView`. Existing tool behavior remains unchanged except that `/tools` becomes directly addressable.

## 8. Metadata

Each route receives factual metadata only.

Recommended titles:

- `/` — `DGAF — Governance Command Center`
- `/control` — `Control Room — DGAF`
- `/governance` — `Governance — DGAF`
- `/agents` — `Agents & Formations — DGAF`
- `/evidence` — `Evidence & Research — DGAF`
- `/tools` — `Tools — DGAF`

Descriptions may summarize the surface's purpose but must not claim authority, validation, efficacy, or capabilities beyond what the existing UI implements.

Prefer server-page metadata exports or static metadata where possible. Do not move the entire page tree to client components solely for metadata convenience.

## 9. Navigation and Accessibility

Primary navigation changes from button-only view switching to semantic links.

Required behavior:

- keyboard navigation follows native link behavior;
- `aria-current="page"` appears only on the active primary destination;
- visible `:focus-visible` styling remains intact;
- mobile navigation exposes `aria-expanded` and `aria-controls` as today;
- activating a mobile navigation link closes the drawer;
- Escape closes an open drawer;
- the skip link remains the first focusable page action and targets `#main-content`;
- browser back and forward move between command-center routes without local-state desynchronization.

No custom client-side history abstraction should be introduced.

## 10. Error and Boundary Behavior

Routing errors fail normally.

- Unknown route: normal Next.js not-found behavior.
- Runtime fetch failure: existing runtime `error` or `stale` semantics inside the shared provider.
- Runtime unavailable while viewing governance/evidence: page remains usable; runtime failure does not become governance failure.
- No snapshot on `/agents`: preserve the current empty/unavailable roster presentation rather than fabricate agent state.
- Malformed API response: preserve existing dashboard validation behavior.

Routing must not add redirects that hide invalid paths.

## 11. Testing Strategy

Add focused routing/navigation regression coverage in addition to all existing UI semantic/contract tests.

Required assertions:

1. The route registry contains exactly the six primary public paths.
2. Each `ViewId` maps to exactly one public href.
3. Primary navigation uses links rather than button-only destination switching.
4. Active route selection produces exactly one `aria-current="page"` destination.
5. Overview actions link to the correct routes.
6. The old `useState<ViewId>` navigation contract is absent from `app/page.tsx` / the routed page layer.
7. Runtime polling ownership exists only in the shared provider/layout path; individual route pages do not instantiate `useDashboardData()`.
8. Control Room and Agents consume the shared dashboard context.
9. Static route pages do not create independent polling loops.
10. All six route modules are present and directly buildable.
11. Production `next build` succeeds.
12. Existing UI semantic/contract tests remain green.
13. Existing governance/scientific-state assertions remain unchanged.

Where practical, prefer contract tests over brittle DOM implementation-detail tests.

## 12. Migration Sequence

Implementation should proceed in small reversible steps:

1. add routing registry and tests;
2. add `DashboardRuntimeProvider` and provider contract tests;
3. adapt the shared shell from callback navigation to pathname/link navigation;
4. create thin route pages;
5. convert Overview callback CTAs to links;
6. remove the old local `ViewId` state switcher;
7. add route metadata;
8. run focused UI/routing tests;
9. run the full existing UI semantic suite;
10. run production Next.js build;
11. run the repository's required exact-head validation wave.

Do not merge or retarget to `main` during implementation while the preflight-first merge barrier is active.

## 13. Stacking and Merge Policy

This branch is intentionally based on PR #649 exact head `4a97f68181da0e343e673b7fc82cab6ba7e2335f` so it inherits the current audience-journey shell and accessibility work.

Dependency order:

1. #651 scientific preflight transition resolves first under the standing all-checks-pass policy;
2. #636 is reconciled to the resulting accepted main and admitted only after its own exact-head validation/status set is fully green;
3. #649 is reconciled/retargeted after #636 and revalidated if its head changes;
4. #642 route work is then reconciled to the accepted UI lineage and must receive a fresh exact-head validation wave before merge.

This route branch must not be merged directly into `main` ahead of its UI dependencies or ahead of #651.

## 14. Governance and Scientific Non-Effects

This change is information architecture only.

It does not:

- establish or satisfy precollection preflight;
- establish immutable freeze;
- create final closure;
- create verification classification;
- authorize successor collection;
- run empirical collection;
- change dataset-lock state;
- authorize unblinding;
- authorize or run primary analysis;
- establish efficacy;
- change custody classification;
- establish independent verification;
- change scientific N;
- change High-Assurance authority.

The controlling accepted posture remains:

`PRE-FREEZE · FAIL-CLOSED · SUCCESSOR COLLECTION NOT AUTHORIZED · N=0`

Canonical DGAF efficacy remains `NOT_ESTABLISHED`.

## 15. Success Criteria

The design is complete when implementation can demonstrate all of the following without semantic drift:

- every primary command-center view has a stable direct URL;
- copied URLs reproduce the intended view;
- browser back/forward behaves normally;
- one shared shell persists across command-center navigation;
- one runtime polling owner preserves last-valid-snapshot behavior;
- runtime state remains explicitly separate from governance authority;
- primary navigation is semantic, keyboard-complete, and mobile-safe;
- every route renders correctly on direct navigation and refresh;
- unknown routes fail normally;
- route-specific metadata exists without overstated claims;
- focused routing tests, existing UI semantic tests, and production build pass;
- no governance or scientific transition occurs.