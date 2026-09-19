# Accessibility & Responsive Contract

Status: **ACCEPTED FOUNDATION / CURRENT-MAIN RECONCILIATION PENDING FOR #850 DELTA**

Scientific/control effect: **NONE**

`PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0`

Current interface-status authority: [`UI_CURRENT_STATE.md`](UI_CURRENT_STATE.md).

## Purpose

The DGAF command center must remain operable and legible when navigation is
keyboard-only, when the viewport is narrow, when technical identifiers are
long, and when platform accessibility modes override ordinary presentation.

## Current implementation boundary

The accepted shell already provides skip-to-content, focus restoration, touch-target, wrapping, reduced-motion, and forced-colors foundations. The additional closed-drawer `visibility` / `pointer-events` containment and grouped audience-navigation treatment were implemented and validated on historical stacked PR #850, but that candidate is stale-lineage because its base PR #849 is stale. Those deltas must be reconstructed on current protected main before they are treated as accepted implementation.

## Keyboard path

The shell now provides a visible-on-focus **Skip to main content** link.

On narrow viewports:

1. the menu button exposes `aria-expanded` and `aria-controls`;
2. opening the navigation focuses its first control;
3. `Escape` closes the navigation and returns focus to the menu button;
4. scrim dismissal also returns focus to the menu button.

The main-content target is programmatically focusable without adding it to the
ordinary tab sequence.

## Touch targets

Primary buttons, navigation items, icon buttons, text actions, and severity
filter controls use a minimum 44px interaction height. Mobile navigation uses a
48px minimum.

## Technical identity resilience

Hashes, source stamps, artifact identifiers, and tool-contract identities may
wrap rather than force horizontal overflow.

This is particularly important for DGAF because immutable identities are part
of the evidence/provenance model and must not be truncated into ambiguity.

## Small-screen behavior

- mobile navigation scrolls independently when needed;
- top-bar content is constrained instead of widening the page;
- primary page gutters tighten at very narrow widths;
- the semantic hero field remains visible;
- truth and governance semantics remain present rather than being hidden for
  compactness.

## Platform accessibility modes

The existing forced-colors structural cues remain authoritative. The skip link
also receives explicit forced-colors treatment.

Reduced-motion mode removes the skip-link transition while preserving the
focus behavior itself.

## Non-effects

This tranche changes no governance interpretation, authorization status,
scientific state, evidence claim, empirical N, or runtime truth.
