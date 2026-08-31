# Preflight Failure-Mode Register — 2026-08-31

**Scope:** Authorized restoration path for the full constitutive DGAF/TGL treatment.
**Status:** PRE-FREEZE engineering control; no empirical execution authorized by this record.
**Boundary:** PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0.

## Purpose

Capture concrete known and hidden failure modes that could delay completion or invalidate a future candidate, so each is addressed once and not rediscovered in later audits.

## Critical failure modes

| ID | Failure mode | Consequence | Required control | State |
|---|---|---|---|---|
| FM-01 | Historical candidate `05fa2866…` remains treated as current after later apparatus changes | Candidate/evidence contamination | Treat post-#151 manifest as historical; derive a fresh candidate only after complete seven-gate restoration | FIXED IN THIS BRANCH |
| FM-02 | Canonical provenance includes configurable P-31 fields that historical engine actually takes from fixed class constants | Claimed state can diverge from executed semantics | Enforce `trust_edge_boost=0.15` and `last_k_anchor=3` invariants until a governed semantic change is explicitly specified | FIXED IN THIS BRANCH |
| FM-03 | P-31 retention uses host wall clock | Identical replay inputs can yield different pruning | Require explicit `evaluation_time` when token-bearing state exists and evaluate historical engine at that bound instant | FIXED IN THIS BRANCH |
| FM-04 | P-33 event identity derived from a truncated canonical payload prefix | Event IDs can collide across turns | Derive `turn_id` from explicit seed + iteration context | FIXED IN THIS BRANCH |
| FM-05 | P-33 `W_t`/`W_{t-1}` transition depends on an implicit upstream mutation contract | Apparent convergence may be measuring unchanged state | Add two-turn transition test and require explicit state producer before freeze | TEST REQUIRED |
| FM-06 | Required TGL hooks remain `None` | Full treatment cannot execute; TGL correctly remains fail-closed | Integrated 7/7 hook-completeness test before candidate creation | OPEN |
| FM-07 | P-32 current copy diverges from historical `PHI_STAR/KILL_REC` behavior | Treatment semantics change silently | Historical parity test anchored to `49854ea1…` | OPEN |
| FM-08 | P-27 threshold lineage ambiguity | Different route behavior under same input | Bind recovered v3.5 contract + implementation as one restoration oracle | OPEN |
| FM-09 | P-30 acceptance schema ambiguity | Acceptance outcome changes without explicit decision | Use operator-designated S/A/B/C/D contract and test rejected alternatives | AUTHORIZED / IMPLEMENTATION PENDING |
| FM-10 | DemiJoule SPEC-vs-code identity conflict | Blocking behavior can change silently | Use authorized six-axis semantic-safety contract; efficiency framing is non-constitutive | AUTHORIZED / IMPLEMENTATION PENDING |
| FM-11 | Preview deployment mistaken for Live Regression | Runtime evidence falsely promoted | Candidate checklist must require actual live-regression result, not preview readiness | OPEN |
| FM-12 | Historical P2/P6a evidence reused for new apparatus | Evidence transfer across identity boundary | Hard-bind candidate source + deployment ID and reject mismatch | OPEN |
| FM-13 | Documentation-only commit mistaken for apparatus change | False candidate churn | Maintain separate identities: main tip ≠ apparatus source ≠ candidate ≠ deployment | CONTROL ESTABLISHED |
| FM-14 | Freeze created before complete provenance binding | Frozen identity may omit behavior-affecting state | Require complete canonical state and evidence binding before freeze | OPEN |
| FM-15 | Unresolved semantics silently implemented by proxy | Hypothesis changes without acknowledgement | No proxy substitution; unresolved gate remains FAIL-CLOSED | CONTROL ESTABLISHED |

## Required pre-candidate checklist

Before deriving a new candidate identity:

1. P-29, P-30, DemiJoule designated semantics are implemented and tested.
2. P-27 and P-32 restored against authoritative historical anchors.
3. P-31/P-33 restored-state provenance binding is integrated and verified.
4. All seven constitutive hooks are wired; no required hook returns SKIP in the valid-path fixture.
5. P-31 deterministic evaluation-time behavior passes replay tests.
6. P-33 two-turn `W_t`/`W_{t-1}` transition is demonstrated.
7. P-32 `PHI_STAR/KILL_REC` parity is verified.
8. P-27 threshold lineage is pinned.
9. Candidate identity and deployment identity are separate, exact, and bound.
10. Prior P2/P6a/P3–P9 evidence remains historical unless exact identity equivalence is explicitly demonstrated.

## Anti-loop rule

A resolved failure mode is not re-audited unless new evidence changes its status. New work must target an affected predicate or a newly discovered failure mode.

## Empirical boundary

This register does not authorize freeze, pilot execution, unblinding, or empirical-N advancement.

**Empirical N: 0.**
