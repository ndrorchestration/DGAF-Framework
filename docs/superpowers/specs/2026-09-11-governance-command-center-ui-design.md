# DGAF Governance Command Center UI/UX Design

**Date:** 2026-09-11  
**Status:** APPROVED DIRECTION / DESIGN SPEC FOR REVIEW  
**Branch:** `design/governance-command-center-ui-2026-09-11`  
**Base:** `17574b7995977ea728e38e61f8dccf387c5ba623`  
**Scope:** Frontend information architecture, visual system, live-state presentation, and existing dashboard-tool integration.  
**Scientific-state effect:** NONE.  
**Authority effect:** NONE.

## 1. Purpose

Replace the current single-page debug-style dashboard with a production-quality **Governance Command Center** that serves both internal operators and external technical readers without weakening DGAF's evidence, authority, or scientific-state boundaries.

The redesign must remain a truthful presentation layer over authoritative project evidence. It must never make an implemented feature look empirically validated, a passed preparatory gate look authorizing, an unknown/loading state look failed, or an internal verification step look independently verified.

The UI should make DGAF understandable before it makes DGAF impressive.

## 2. Product Principles

1. **Truth before decoration.** Governance and evidence states must be visually explicit and semantically correct.
2. **Capability is not authority.** UI affordances must preserve DGAF's distinction between what the system can do and what it is permitted to do.
3. **Public translation first.** External-facing labels lead with industry-neutral function; DGAF codenames are secondary context.
4. **Progress is not promotion.** Preparation tooling, verified predicates, authorization, empirical collection, analysis, and efficacy remain visually distinct.
5. **Operator depth without outsider confusion.** The same application supports two reading depths without maintaining two competing truth layers.
6. **Dark by design, not dark by default.** The visual language is deliberately dark, restrained, legible, and professional rather than a generic terminal aesthetic.
7. **Responsive and keyboard-complete.** Every core workflow remains usable on desktop, tablet, and mobile and without a pointer.
8. **No fabricated telemetry.** Missing, unavailable, or stale runtime data is shown as such.

## 3. Expert-Lens Review Model

The design is evaluated from these complementary perspectives:

- **Product design:** Is there a clear primary purpose and reading order?
- **Information architecture:** Can a first-time user distinguish overview, governance, evidence, agents, and tools?
- **Operator UX:** Can the maintainer see current state, blockers, next admissible transition, and runtime health quickly?
- **External/customer UX:** Can a reviewer understand DGAF without learning internal codenames first?
- **Research integrity:** Are engineering evidence, scientific evidence, authorization, and efficacy clearly separated?
- **Governance integrity:** Does fail-closed behavior remain obvious and non-negotiable?
- **Accessibility:** Are color, contrast, keyboard focus, semantics, and reduced motion handled intentionally?
- **Frontend engineering:** Are components bounded, testable, maintainable, and decoupled from data transport?
- **Reliability:** Are loading, stale, error, unavailable, and successful states modeled independently?
- **Security/privacy:** Does the interface avoid exposing secrets or implying access to non-public custody material?

## 4. Current-State Problems

The current `app/page.tsx` is an approximately 18 KB client component with most visual styling in inline style objects. It combines data fetching, navigation, state semantics, table/card rendering, live polling, and the P-07 sweep tool in one file.

Current UX limitations:

- single-column debug-console composition;
- heavy monospace usage that reduces readability for narrative and stakeholder-facing content;
- weak visual hierarchy and limited onboarding;
- no explicit separation between operator and external-reader needs;
- status rendering conflates loading and negative states in places;
- limited mobile behavior because several grids and tables assume desktop width;
- governance progression is presented as a static list rather than as a stateful lifecycle;
- agent codenames lead over their public functions;
- no strong separation of engineering evidence from scientific/authorization state;
- no consistent state vocabulary for `loading`, `unknown`, `unavailable`, `stale`, `pass`, `verified`, `open`, `blocked`, `not_authorized`, and `not_established`;
- no reusable design tokens or component system.

Integration risk discovered during design review:

- the client references `/api/health`, `/api/audit`, `/api/roster`, and `/api/sweep`;
- the committed `app/` tree currently contains only `layout.tsx` and `page.tsx`;
- the root `api/` directory currently exposes `ahg_herald.py` only;
- therefore live dashboard transport must be verified and normalized during implementation rather than assumed.

## 5. Audience Model

### 5.1 External / Overview reader

Examples: hiring manager, engineer, researcher, governance reviewer, potential collaborator.

Needs:

- what DGAF is;
- what it is trying to solve;
- what is implemented;
- what is verified;
- what is not yet authorized or established;
- current experiment boundary;
- understandable agent and governance terminology;
- links into evidence rather than unexplained internal jargon.

### 5.2 Internal / Control Room operator

Needs:

- live runtime health;
- freshness / last successful poll;
- audit counters and cold-start state;
- gate/lifecycle state;
- blockers and next admissible transition;
- agent and formation status;
- P-07 sweep operation and findings;
- exact technical identifiers when useful;
- visible separation between project truth state and ephemeral runtime telemetry.

The application uses a single data/state model but provides distinct presentation depth through navigation and progressive disclosure.

## 6. Information Architecture

Primary desktop navigation:

1. **Overview**
2. **Control Room**
3. **Governance**
4. **Agents & Formations**
5. **Evidence & Research**
6. **Tools**

Mobile uses a compact navigation drawer/sheet with the same labels and order.

### 6.1 Overview

Purpose: explain DGAF in under 60 seconds without overstating its status.

Required sections:

- concise product statement derived from `docs/PUBLIC_TRANSLATION_LAYER.md`;
- **Truth Boundary** panel containing:
  - `PRE-FREEZE`
  - `FAIL-CLOSED`
  - `NOT AUTHORIZED`
  - `N=0` for the canonical High-Assurance program
  - `EFFICACY NOT ESTABLISHED`
- concise distinction: engineering/governance implementation evidence is not canonical efficacy;
- current Track A Epoch 001 / Epoch 002 summary;
- current next admissible transition from the canonical current-state documents;
- quick links to Governance, Evidence, and Control Room.

### 6.2 Control Room

Purpose: current operational condition and actionable runtime status.

Required modules:

- runtime health;
- data freshness indicator;
- adapter status;
- session/audit counters;
- warnings such as cold-start/reset state;
- current blocking conditions;
- current next admissible transition;
- compact current lifecycle rail;
- explicit distinction between repository governance state and transient runtime state.

### 6.3 Governance

Purpose: make ordered progression and fail-closed semantics visible.

Render the current admissible chain as a stateful rail/timeline:

`repository custody acceptance → precollection preflight → immutable freeze → final closure → verification classification → collection authorization → empirical collection → QC → dataset lock → separate unblinding decision → controlled materialization + immutable receipt → separate primary-analysis authorization → locked analysis`

Each stage uses a normalized status object and cannot infer completion from later preparation tooling.

Preparation tooling that exists for later stages may be shown as **tooling prepared** while the underlying predicate remains **not established** or **not authorized**.

### 6.4 Agents & Formations

Purpose: expose the orchestration model without forcing outsiders to memorize internal vocabulary.

Card/table presentation must use the first-use form:

- `Governance Orchestrator (Amethyst)`
- `Continuity & Provenance Coordinator (COLLEEN)`
- `Evidence & Verification Reviewer (Apogee)`
- etc., sourced from the public translation authority.

Requirements:

- search/filter by role, tier, status, and formation/triad membership;
- responsive card view on narrow screens;
- technical codename secondary to public function;
- tooltips/details must preserve identity vs role vs formation-state distinctions;
- Agent Ionia and `IONIA_STATE` must never be visually collapsed.

### 6.5 Evidence & Research

Purpose: explain what evidence exists and what it can support.

Required modules:

- evidence-state legend (`PROPOSED`, `IMPLEMENTED`, `TESTED`, `PASS`, `VERIFIED`, developer self-attested/nonindependent, independently verified, not authorized, not established, empirically demonstrated);
- Epoch 001 summary:
  - completed blinded prospective collection;
  - 50 paired inferential seed units / 2,250 blinded raw observations;
  - dataset lock established;
  - protected mapping cryptographically unrecoverable;
  - primary analysis unanalyzable / not run;
- Epoch 002 successor summary:
  - custody-v2 local recovery status represented at its exact accepted evidence level;
  - repository custody not established unless canonical state later changes;
  - collection not authorized unless canonical state later changes;
  - no efficacy promotion from preparation tooling;
- links/references to authoritative repository records.

### 6.6 Tools

Purpose: preserve and improve working utilities, beginning with P-07 Sweep.

P-07 Sweep requirements:

- multiline target input;
- clear accepted-input guidance;
- validation before submission;
- explicit idle/loading/success/error states;
- disable duplicate submission while running;
- findings count and harmonic score presentation;
- severity filter;
- sortable or grouped findings;
- empty-result state;
- narrative result section;
- copy/export affordance using browser APIs only where safe;
- no success presentation if response is malformed or unavailable.

## 7. Visual System

### 7.1 Color

Use CSS custom properties rather than ad hoc inline hex values.

Suggested semantic palette:

- `--bg-canvas`: near-black graphite;
- `--bg-surface-1`: elevated charcoal;
- `--bg-surface-2`: slate-charcoal;
- `--border-subtle`: low-contrast cool gray;
- `--text-primary`: near-white;
- `--text-secondary`: cool light gray;
- `--text-muted`: accessible muted gray;
- `--accent-primary`: restrained cyan / ice blue;
- `--accent-secondary`: violet;
- `--state-pass`: green;
- `--state-warning`: amber;
- `--state-denied`: red;
- `--state-info`: blue;
- `--state-unknown`: neutral gray.

Red is reserved for actual failed/denied/critical states. Loading, missing, or unknown states use neutral presentation.

### 7.2 Typography

- UI/narrative: modern system sans-serif stack to avoid external font dependency.
- Technical IDs/hashes/predicates/code: system monospace stack.
- Monospace must not be used for the entire application.

### 7.3 Layout

Desktop:

- persistent left navigation;
- compact command/header bar;
- max-width content shell with 12-column grid;
- responsive card spans;
- sticky truth-boundary summary only where it improves orientation.

Tablet:

- collapsible nav;
- 6-column responsive grid.

Mobile:

- single-column flow;
- navigation drawer;
- tables convert to stacked cards or horizontally scroll only when exact tabular comparison is essential;
- status chips wrap without clipping.

### 7.4 Motion

- short transitions for hover/focus/status expansion;
- no decorative continuous animation;
- honor `prefers-reduced-motion`;
- no motion that implies live progress when the underlying state is static or unknown.

## 8. State Semantics

Define a single visual state vocabulary:

```ts
type UiState =
  | 'loading'
  | 'unknown'
  | 'unavailable'
  | 'stale'
  | 'info'
  | 'open'
  | 'blocked'
  | 'pass'
  | 'verified'
  | 'not_authorized'
  | 'not_established'
  | 'failed'
```

Rules:

- `loading` is never red;
- `unknown` is never interpreted as false;
- `pass` and `verified` are separate labels even if both use positive color families;
- `not_authorized` is not an execution failure; it is a governance prohibition;
- `not_established` is not equivalent to disproven;
- stale data must display age/freshness where possible;
- UI must not infer a governance predicate from API health.

## 9. Data Architecture

The presentation layer consumes normalized frontend domain objects rather than binding components directly to raw API response shapes.

Proposed modules:

- `app/lib/types.ts` — raw/runtime and normalized domain types;
- `app/lib/status.ts` — state normalization and display metadata;
- `app/lib/api.ts` — runtime fetch functions and response validation;
- `app/lib/governance.ts` — canonical display constants and ordered lifecycle model, constrained by current repository authority;
- `app/lib/public-translation.ts` — public-facing agent/function labels derived from the repository translation authority;
- `app/components/*` — bounded presentation components;
- `app/styles/globals.css` — tokens, reset, accessibility, responsive layout, shared primitives;
- `app/page.tsx` — composition only.

No component may invent authoritative state from presentation defaults.

## 10. Runtime API Contract Requirement

Before live widgets are treated as functional, implementation must verify the actual deployed transport for:

- health;
- audit;
- roster;
- sweep.

If the current endpoints do not exist or do not produce stable JSON contracts, implementation must introduce the smallest compatible route layer or adapter necessary to restore the already-intended dashboard behavior.

Requirements:

- preserve existing underlying DGAF/PDMAL logic where available;
- do not fabricate values;
- validate response shape before rendering a success state;
- return/use explicit errors rather than silently filling placeholder data;
- keep secrets and custody material out of frontend payloads;
- polling failures must not erase the last valid snapshot without indicating staleness.

## 11. Accessibility Requirements

Target WCAG 2.2 AA behavior for the implemented surface.

Required:

- semantic landmarks (`header`, `nav`, `main`, `section`, appropriate headings);
- visible keyboard focus;
- logical tab order;
- buttons are buttons; navigation is navigation;
- state is never conveyed by color alone;
- text contrast meets AA targets;
- focus/hover states do not depend solely on low-contrast borders;
- form labels are programmatically associated;
- error text is associated with inputs where applicable;
- reduced motion honored;
- mobile controls meet practical touch target sizing;
- live-refresh regions avoid noisy screen-reader announcements.

## 12. Error, Loading, Empty, and Stale States

Every remote-data module supports:

- initial loading skeleton/placeholder;
- valid empty result;
- last-valid-data + stale indicator;
- request error;
- malformed-response error;
- retry action where useful;
- timestamp of last successful refresh when available.

A failed poll must not convert every previously valid metric to a destructive red state.

## 13. Security and Privacy Boundaries

The UI must never request, store, expose, or suggest upload of:

- private keys;
- passphrases;
- encrypted custody backup copies;
- blinding secrets;
- recoverable secret material.

The current project-status rule that secret custody material remains outside GitHub, Notion, chat, CI inputs, logs, and committed files remains unchanged.

## 14. Testing Strategy

Implementation uses test-driven development where practical.

Minimum verification:

- pure tests for state normalization and semantic color/label mapping;
- tests that `loading`, `unknown`, `not_authorized`, `not_established`, `pass`, and `verified` remain distinct;
- API adapter tests for malformed/unavailable responses;
- component-level behavior tests where the existing dependency policy permits them;
- `npm run build` as a mandatory type/build gate;
- repository-required CI checks on the exact PR head;
- Vercel preview inspection at desktop and mobile widths;
- keyboard-navigation smoke test;
- visual check that current truth-boundary claims match canonical state.

New testing dependencies should be minimized. If a UI test library is added, it must have a concrete behavioral purpose rather than being introduced solely for framework preference.

## 15. Maintainability Boundaries

The existing monolithic page should be decomposed by responsibility, not by arbitrary component count.

No single new component should simultaneously own:

- remote transport;
- domain-state normalization;
- navigation;
- unrelated content sections.

The design system remains project-local. Do not introduce a large external component framework for this pass.

## 16. Non-Goals

This redesign does not:

- authorize any experiment;
- change scientific predicates;
- claim DGAF efficacy;
- redesign the underlying DGAF governance protocol;
- create a new customer account/authentication system;
- create billing, multi-tenancy, or organization administration;
- replace Notion/GitHub as governance authority;
- expose private custody workflows in the browser;
- turn every repository document into a web page;
- introduce decorative 3D/topology visualization unless it serves a concrete comprehension task in a later approved scope.

## 17. Acceptance Criteria

The redesign is acceptable when all of the following are true:

1. A first-time technical reader can state what DGAF is and its current evidence boundary from the Overview without decoding internal terminology.
2. The canonical boundary `PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0` remains prominent and cannot be visually mistaken for an authorized experiment.
3. `EFFICACY NOT ESTABLISHED` is visible on external-facing status surfaces.
4. Operators can reach runtime health, governance progression, agents, evidence, and P-07 Sweep from persistent navigation.
5. Loading/unknown/unavailable states are distinct from failed/denied states.
6. Agent public functions lead over codenames on external-facing surfaces.
7. The governance lifecycle differentiates tooling preparedness from predicate establishment and authorization.
8. Existing intended dashboard functions are either verified operational or restored through a minimal validated integration layer.
9. The page is usable at desktop, tablet, and narrow mobile widths.
10. Keyboard focus, semantics, contrast, and reduced-motion behavior meet the accessibility requirements above.
11. No secret custody material is exposed or requested.
12. The production code is decomposed into bounded modules rather than returning to a monolithic inline-styled page.
13. Exact-head repository CI and the Next production build are green before merge is considered.
14. A Vercel preview is visually inspected before merge.
15. Merge remains subject to the repository's existing fail-closed checks and user policy: merge only after all required checks pass.

## 18. Implementation Sequence

After this design spec is approved, the implementation plan should sequence work as:

1. establish frontend types, normalized state semantics, and CSS token foundation;
2. verify/repair live dashboard API transport with response validation;
3. build application shell and responsive navigation;
4. build Overview and Truth Boundary;
5. build Control Room telemetry and stale/error behavior;
6. build Governance lifecycle rail;
7. build Agents & Formations translation-aware surfaces;
8. build Evidence & Research surfaces;
9. rebuild P-07 Sweep as a robust tool surface;
10. accessibility/responsive hardening;
11. production build and repository test wave;
12. Vercel preview visual review and correction pass;
13. PR review and merge decision only after exact-head required checks pass.

## 19. Design Decision Summary

Selected approach: **single-application Governance Command Center with progressive disclosure**, instead of either a cosmetic reskin of the existing dashboard or separate public/operator applications.

Why:

- it removes the current debug-console feel;
- it serves internal and external readers from one truth model;
- it avoids duplicated status logic;
- it preserves YAGNI by not introducing auth/multi-app infrastructure prematurely;
- it provides a scalable information architecture for future DGAF surfaces;
- it aligns the visual hierarchy with DGAF's core conceptual hierarchy: evidence, verification, authority, and permission are related but not interchangeable.
