# P-36: Gate Priority Schema

```
Status:       DRAFT
Certified-by: PENDING (Apogee)
Cert-date:    PENDING
Last-updated: 2026-06-13 (Session S069)
```

**Version:** 1.0
**Maintained by:** Agent Amethyst
**Session:** S069 · 2026-06-13
**Ender ratification:** PENDING

> Converts the linear NDR governance orchestration stack into a DAG by classifying every pattern as BLOCKING, ADVISORY, or DEGRADED-MODE-SKIPPABLE, without changing any pattern’s logic or specification.

---

## Rationale

The NDR governance stack (P-01 through P-35) is currently documented as a strictly sequential pipeline. This creates a single-thread-of-failure problem: a latency spike or error in any pattern holds everything downstream, including patterns that have no logical dependency on the failing one. P-36 introduces a priority taxonomy that preserves all hard sequential dependencies while allowing independent patterns to execute asynchronously or be gracefully skipped under load, with every skip producing a signed audit entry.

---

## Priority Classes

### BLOCKING
Hard sequential dependency. Must complete and return PASS before any downstream pattern in the same dependency chain fires. A FAIL in a BLOCKING pattern halts the pipeline at that point.

**Properties:**
- Synchronous execution required
- Timeout budget: 5 seconds (configurable per pattern)
- FAIL → pipeline halt; PROCLUDE or escalate per pattern spec
- Cannot be skipped in any mode (production, staging, or test)

### ADVISORY
Runs concurrently with other ADVISORY patterns and with BLOCKING patterns in independent chains. Result is appended to the session audit log. FAIL or WARN is surfaced but does not halt the pipeline.

**Properties:**
- Async execution permitted
- Timeout budget: 10 seconds; timeout itself is a WARN, not a FAIL
- Result appended to P-01 audit stream with `advisory: true` flag
- Timeout or FAIL → logged; pipeline continues

### DEGRADED-MODE-SKIPPABLE
Permitted to skip under load conditions, but every skip must produce a signed audit entry with: pattern ID, skip reason (LOAD / TIMEOUT / EXPLICIT), session ID, timestamp, and Amethyst sign-off flag. Skips are surfaced to the next Session Graduation Check (P-10).

**Properties:**
- Skip requires explicit `degraded_mode: true` flag in session config
- Skip audit entry committed to P-01 dead-letter channel
- Accumulated skips ≥ 3 in one session → WARN surfaced to COLLEEN
- Cannot be skipped in production if any Crucible (P-36 attack surface) finding is open

---

## Pattern Classification Table

| Pattern | Name | Priority Class | Rationale |
|---------|------|----------------|-----------|
| P-35 | Procluding Premise Gate | **BLOCKING** | Constitutional pre-admissibility; nothing fires without it |
| P-30 | Apogee-Attestation-Gate | **BLOCKING** | Gate 0; quality threshold before any orchestration |
| P-29 hook 1 | Sentinel Risk Pass — hook point 1 | **BLOCKING** | Pre-routing safety check; must complete before KAPPA fires |
| P-03 | Governance Contract Test | **BLOCKING** | CI merge gate; hard dependency for any gate logic change |
| P-27 | Adaptive-Weighting | **BLOCKING** | Core routing; pipeline cannot produce output without it |
| P-28 | Pipeline Composition | **BLOCKING** | Defines stage order; structural dependency |
| P-29 hook 2 | Sentinel Risk Pass — hook point 2 | **BLOCKING** | Post-Phi-Closure KILL_REC feed; must complete before HPG |
| P-29 hook 3 | Sentinel Risk Pass — hook point 3 | **BLOCKING** | Post-RAG verify; final safety check before output |
| P-32 | Fibonacci Phi-Closure Gate | **BLOCKING** | Temporal stability; halts pipeline on KILL_REC |
| P-01 | Fan-Out Trace Sink | **BLOCKING** | Audit spine; all other patterns depend on it |
| P-11 | 11Q Attestation Scoring | **BLOCKING** | Required for canonical promotion; not skippable |
| P-04 | Parametrized Corpus | **ADVISORY** | Test suite expansion; runs in CI, async |
| P-05 | Tri-Phase CI Gate | **ADVISORY** | CI pipeline; advisory in runtime, blocking in CI context |
| P-09 | Triumvirate Mandate Schema | **ADVISORY** | Mandate lifecycle; appended to audit log |
| P-10 | Session Graduation Check | **ADVISORY** | End-of-session check; surfaces to next cycle |
| P-31 | SCPE | **ADVISORY** | Context pruning; latency risk if blocking; T0 tokens always safe |
| P-33 | PDMAL Convergence Monitor | **ADVISORY** | Trust graph health; third orthogonal axis; async safe |
| P-34 | Empirical Threshold Sweep | **ADVISORY** | Calibration methodology; not a runtime gate |
| P-02 | Async Ring Buffer | **ADVISORY** | Infrastructure; always async by design |
| P-06 | Topology × Orchestration Matrix Lab | **ADVISORY** | Methodology pattern; not a runtime gate |
| P-07 | Dual-Agent Persistent Sweep Loop | **ADVISORY** | Governance campaign; async by design |
| P-08 | Triad Taxonomy | **ADVISORY** | Formation classification; referenced, not executed |
| P-33 joint escalation | PDMAL + Phi-Closure joint rule | **BLOCKING** | If both hit severity ≥3 simultaneously, DemiJoule deep re-scan is BLOCKING |
| P-12–P-26 | Stasis Patterns | **DEGRADED-MODE-SKIPPABLE** | Block-declared; STASIS-CANONICAL; individually unenumerated |

---

## Updated DAG (Simplified)

```
[BLOCKING chain — sequential]
P-35 → P-30 → P-29:hook1 → P-27/P-28 (KAPPA) → P-29:hook2 → P-32 → P-29:hook3 → P-01 output

[ADVISORY — async, concurrent with BLOCKING chain]
P-31 (SCPE)        ──► audit log
P-33 (PDMAL)       ──► audit log [joint escalation rule: if P-33 + P-32 both severity≥3 → BLOCKING override]
P-02 (ring buffer) ──► persistent store
P-10 (grad check)  ──► next session

[DEGRADED-MODE-SKIPPABLE — skip with signed audit entry]
P-12–P-26          ──► skip log → P-10 surface
```

---

## Timeout Budget Table

| Priority Class | Default Timeout | Timeout Consequence |
|----------------|-----------------|--------------------|
| BLOCKING | 5 seconds | Pipeline halt; escalate to Njineer |
| ADVISORY | 10 seconds | WARN logged; pipeline continues |
| DEGRADED-MODE-SKIPPABLE | N/A (skipped) | Signed skip entry to P-01 dead-letter |

---

## References

| Field | Value |
|-------|-------|
| Parent patterns | P-35 (pre-admissibility), P-01 (audit spine), P-07 (sweep loop) |
| Related gate | P-10 (graduation check surfaces skip accumulation) |
| Research program | `docs/governance/NDR_RESEARCH_PROGRAM_CHARTER_v1.md` |
| NIST Control | GV-1.1, MS-2.5 |
| EU AI Act | Art. 9, Art. 17 |
| Supersedes | Linear stack diagram in `NDR_PATTERN_REGISTRY_UNIFIED.md` (augmented, not replaced) |

---

## Provenance

| Field | Value |
|-------|-------|
| Pattern | P-36 |
| Layer | Layer 0.5 — Stack Architecture |
| Session | S069 |
| Date | 2026-06-13 |
| Author | Agent Amethyst |
| Certifier | Apogee (PENDING) |
| Registered by | Amethyst × COLLEEN (meta-orchestration) |
| Ender ratification | PENDING |
| Architect | Hensel, Andrew Vance (Ndr / ndrorchestration) |
| Governance spine | [DGAF-Framework](https://github.com/ndrorchestration/DGAF-Framework) |

---
*P-36 Gate Priority Schema v1.0 · DRAFT · S069 · 2026-06-13*
