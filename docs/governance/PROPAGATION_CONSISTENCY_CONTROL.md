# Propagation Consistency Control

**DGAF-Framework · Documentation / Provenance Integrity**  
**Status:** Advisory QA control  
**Established:** 2026-08-21

## Purpose

Propagation consistency checks a failure mode that ordinary claim/provenance linting does not cover:

> A claim may be corrected in one canonical location while an earlier form of the same claim remains active elsewhere.

The control detects known corrected claims that recur without their required current-state qualifier. It is a regression/provenance control, not an empirical truth detector.

## Governance Boundary

Propagation consistency is supporting documentation/provenance integrity and belongs under **Predicate 5**. It is not an additional epistemic predicate and must not be used to establish empirical validity.

The checker therefore distinguishes:

| Classification | Meaning | Default result |
|---|---|---|
| `current_claim` | Current quantitative/semantic claim subject to propagation control | Bare recurrence = ERROR; qualified recurrence = PASS |
| `historical_reference` | Historical evidence or audit record retaining terminology from its original state | ALLOWED / REVIEW |
| `terminology_migration` | Identifier whose meaning changed over time | REVIEW; do not mechanically rewrite historical records |

## FLAG-02 Temporal Namespace Rule

`FLAG-02` has a temporal namespace collision in the repository:

- **Historical FLAG-02:** identifier used for the 340% coordination-gain metric-definition issue.
- **Current terminology:** qualitative evaluation-mode terminology.

Historical documents may retain the historical identifier when provenance requires it. New documents must not introduce `FLAG-02` ambiguously for either meaning.

**FLAG closure is not claim verification.** Closing a tracking flag records disposition of the governance task; it does not establish empirical verification of the underlying 340% coordination-gain claim.

## 340% Coordination-Gain Rule

The 340% coordination-gain figure remains **UNVERIFIED** unless and until the applicable research protocol establishes its baseline, method, substrate, and empirical validation.

A propagation hit must therefore not be resolved by merely changing a tracking status. Current occurrences must either:

1. retain an appropriate `UNVERIFIED`/equivalent qualifier; or
2. be explicitly identified as historical; or
3. be removed when they are obsolete current-state documentation.

## Historical Records

Historical audit/session records should preserve their original terminology and state when that terminology is necessary to reconstruct what the repository believed or recorded at the time. They should not be rewritten solely to make the propagation checker pass.

## Checker Semantics

`scripts/propagation_check.py` uses registry classifications in `registry/propagation_registry.json`.

The checker deliberately avoids treating an arbitrary qualifier anywhere in a broad character window as sufficient. Qualifier matching prefers the occurrence's sentence and then its containing paragraph. This reduces false qualification from unrelated nearby text.

### Modes

- **Advisory:** default; reports classified findings and never blocks on bare current claims.
- **Strict:** exits non-zero only for `ERROR_BARE_CURRENT` findings. This mode should not be adopted as a release/freeze gate until the registry and affected documentation have been adjudicated.

## Initial Adjudication Targets

1. `docs/SESSION_ANCHORS.md` — clarify that historical FLAG-02 closure does not establish empirical verification of the 340% claim.
2. `docs/governance/OPEN_FLAGS_SURFACE_REQUEST_S069.md` — preserve as historical S069 evidence; do not treat its OPEN state as current authority.
3. `docs/NDR_INTERNAL_VOCABULARY_MASTER.md` — ensure any current 340% recurrence is qualified.
4. `docs/governance/NDR_RESEARCH_PROGRAM_CHARTER_v1.md` — preserve the binding UNVERIFIED/falsifiability requirement.
5. `docs/governance/RECURSIVE_AUDIT_2026-07-03.md` — preserve historical audit terminology unless it is explicitly presented as current state.

## Freeze Implication

Until the canonical-state contradiction in `SESSION_ANCHORS.md` is adjudicated, documentation propagation integrity is **NOT CLEAN**. This is a documentation/governance readiness issue and must not be misreported as evidence that the underlying 340% claim is true or false.
