# DGAF-Framework

**Dynamic Governance Agentic Formation (DGAF)** — a research and implementation repository for agent orchestration, evaluation, provenance, and governance controls.

> **Epistemic status:** This README describes repository scope and the current pre-freeze governance state. Individual claims require exact evidence and defined scope. Historical evidence remains scoped to the SHA/run/deployment/artifact that produced it.

## Current project state — 2026-09-01

The DGAF/PDMAL experimental track remains **PRE-FREEZE / FAIL-CLOSED**. The currently controlled completion candidate is `566273c6c2906bdf71827381493a26ee7697034c` on draft PR #187. It is not merged to `main`, no new immutable freeze exists, pilot authorization has not been granted, and empirical **N = 0**.

The current candidate contains governance/completion-control and independent-verification machinery. Evidence produced by earlier candidates is not transferred to this SHA. The latest candidate-bound PDMAL cycle exposed a CI-only quoting defect in the final one-seed structural dry-run command after the substantive deterministic verification machinery had passed; this remains an engineering defect to repair, not experimental evidence.

## Current verification architecture

- **PDMAL Instrumentation Dry Run:** deterministic structural/instrumentation verification only; it does not execute the 9,000-observation empirical experiment.
- **P9 Independent Verification:** independently checks candidate identity, canonicalization/hash equality, authority identity, and durable P9 evidence integrity.
- **Completion Controller:** reconciles exact-candidate evidence and remains fail-closed; it cannot manufacture authorization, freeze, or empirical results.
- **Evidence binding:** candidate SHA, workflow run, artifact ID, and artifact digest are treated as distinct provenance dimensions and are checked before evidence is promoted into the completion registry.
- **Stale-evidence prevention:** evidence from a superseded candidate remains historical and cannot be silently inherited by the current candidate.

## Current gate state

| Gate / control | Current state |
|---|---|
| E2b | CLOSED / VERIFIED at its historical exact execution boundary |
| M6 | CLOSED / VERIFIED at its historical exact candidate boundary |
| P2 | OPEN / fresh exact-candidate runtime evidence required |
| P3 | OPEN / fresh exact-candidate artifact evidence required |
| P4 | OPEN / fresh exact-candidate security/blinding evidence required |
| P5 | OPEN / fresh exact-candidate reproducibility evidence required |
| P6 | OPEN / fresh exact-candidate custody/retrieval/hash evidence required |
| P6a | OPEN / fresh exact-candidate authenticated CORS evidence required |
| P7 | OPEN / external scientific decision and exact final binding required |
| P8 | OPEN / FAIL-CLOSED |
| P9 | OPEN / current-candidate independent verification required |
| Freeze | NOT CREATED |
| Pilot authorization | NOT GRANTED |
| Empirical N | 0 |

## Governance boundary

Engineering CI success, deterministic fixtures, deployment readiness, documentation updates, artifact custody, or independent structural verification do **not** constitute PDMAL efficacy evidence or experimental authorization. P7 remains a scientific/governance decision; P8 remains fail-closed until its exact prerequisites are satisfied; freeze and pilot authorization remain separate transitions.

## Canonical mathematical notation

`φ` is the conventional Golden Ratio, `(1+√5)/2 ≈ 1.618033989`.

`σ_{p,q}` denotes the Spinadel metallic-means family, the positive solution of `x² - px - q = 0`.

`ρ` denotes the mathematical plastic number, `≈1.3247179572447454`, the unique real root of `x³ - x - 1 = 0`.

`pP` / **Platinum Mean** is intentional DGAF-specific notation for the regular-hendecagon unit-side circumradius, `1/(2 sin(π/11)) ≈ 1.774732842`. It must not be substituted for `ρ` in plastic-number mathematics.

## Evidence boundary

Historical evidence remains scoped to the exact application source, deployment, workflow run, and artifact that produced it. A successful verification on a prior candidate does not certify `566273c6c2906bdf71827381493a26ee7697034c`.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
