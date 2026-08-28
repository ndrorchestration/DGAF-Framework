# Platinum Mean / Plastic Constant Semantic Correction

**Date:** 2026-08-28  
**Status:** Active semantic-control record  
**Scope:** DGAF terminology and PDMAL mathematical references

## Correction

DGAF intentionally uses **pP / Platinum Mean** for the regular-hendecagon unit-side circumradius:

`pP = 1 / (2 sin(π/11)) ≈ 1.774732842`

The mathematical **plastic constant** is instead:

`ρP ≈ 1.3247179572447454`, the real root of `x³ = x + 1`.

These quantities are distinct and must not be conflated.

## PDMAL boundary

The PDMAL plastic-constant convergence mathematics uses `ρP`, not `pP`. Historical documents that call `1.7747` or `1.77473` `ρP`/"Platinum Ratio" are semantic predecessors and must be treated as historical/superseded terminology unless independently re-derived under current governance.

The correction does **not** invalidate the geometric quantity `1.774732842`; it changes its semantic classification to the DGAF-defined `pP / Platinum Mean` where that notation is intended.

## Affected historical material

Repository-wide searches identified historical/current-surface references including:

- `docs/formalism/constants/11Q-derivation.md`
- `docs/formalism/hensel-general-formalism.md`
- `docs/registry/PLATINUM_REGISTRY_TIERS_v1.md`
- `docs/architecture/platinum-convergence-audit-v1.md`

Those documents must not be treated as current mathematical authority solely because they remain in the repository. Where practical, their current status should be revised or an explicit supersession note should be added. Historical evidence should be preserved rather than silently deleted.

## Epistemic boundary

This correction establishes terminology only. It does not establish PDMAL convergence, contraction, robustness, security, superiority, production efficacy, or empirical validity.

**Current DGAF/PDMAL control state remains: PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0.**
