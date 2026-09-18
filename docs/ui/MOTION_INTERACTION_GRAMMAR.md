# Motion & Interaction Grammar

Status: **DESIGN-SYSTEM SUCCESSOR TO #800**

Scientific/control effect: **NONE**

`PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0`

## Purpose

DGAF motion exists only when it helps a user understand causality, reachability,
focus, or provenance. Motion must never imply authorization, completion, or
scientific validity on its own.

## Motion roles

- **Provenance flow** — subtle directional movement along evidence/relation
  filaments. The static filament remains when animation is disabled.
- **Frontier emphasis** — restrained breathing around the nearest admissible
  frontier. Border style, text, and status remain the source of meaning.
- **Interaction focus** — small hover/press displacement to clarify which
  surface is actionable or inspectable.
- **State-space inspection** — minimal translation on reachable/dimensional
  surfaces to reinforce spatial structure without changing state semantics.

## Timing

The semantic system exposes:

- `--motion-fast`
- `--motion-standard`
- `--motion-slow`
- `--motion-flow`
- `--motion-focus`
- `--ease-control`
- `--ease-emphasis`

Durations are intentionally short except for continuous provenance/frontier
motion, which remains low-amplitude.

## Reduced motion

`prefers-reduced-motion: reduce` removes all continuous and interaction
animation introduced by this tranche.

No state meaning disappears when motion is removed:

- established/frontier/unreachable remain structurally distinct;
- authorization boundaries retain explicit labels and border treatments;
- governance relations retain static filament patterns;
- status chips retain shape/border semantics.

## Non-effects

This layer does not change:

- governance truth;
- authorization state;
- evidence status;
- empirical N;
- canonical efficacy;
- runtime or scientific claims.

Motion is presentation only and cannot create an admissible transition.
