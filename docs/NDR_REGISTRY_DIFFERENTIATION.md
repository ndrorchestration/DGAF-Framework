# NDR Registry Differentiation Index

**DGAF-Framework · S066**
Authority: COLLEEN (archival) | Amethyst (meta-orchestration)
Created: 2026-05-30 | Updated: 2026-05-30 (PM-01 PM-02 PM-03 closed)
Status: **Active — pre-merge tracking document**

---

## Purpose

This document is the single authoritative map of all NDR pattern registries
in the DGAF-Framework repo. It exists because three separate registries
evolved across sessions for legitimate reasons (layer separation, tooling
constraints, session scope). It tracks their differentiation and serves
as the pre-planning substrate for the eventual unified merge.

**When a new pattern is registered, this file must be updated first.**

---

## Registry Map

| Registry | Path | Version | Scope | Patterns | Status |
|----------|------|---------|-------|----------|--------|
| **Primary** | `docs/NDR_PATTERN_REGISTRY.md` | v1.4 / S066 | Harness, CI, triads, mandate, graduation, cross-ref index | P-01–P-10 (full spec) + P-11–P-34 (index) | ✅ Active |
| **KAPPA/Governance** | `docs/patterns/NDR_PATTERN_REGISTRY.md` | v2.2 / S066 | Router calibration, pipeline, sentinel, attestation | P-27–P-30 (full spec) + P-01–P-26 (133 stasis) | ✅ Active |
| **Runtime Cards** | `patterns/NDR_*.md` | v1.1 (Phi-Closure) / v1.0 (SCPE, PDMAL) | Long-context safety, drift, convergence | P-31 (SCPE), P-32 (Phi-Closure), P-33 (PDMAL) | ✅ Active |
| **Machine-readable** | `patterns/ndr_patterns.json` | v0.3.0 / S066 | JSON index — P-31–P-34 + ndr.* entries | P-31–P-34 + 2 ndr.* | ✅ Synced |
| **Merged (target)** | `docs/NDR_PATTERN_REGISTRY_UNIFIED.md` | v3.0 (planned) | All patterns, all layers | P-01–P-34+ | 🔲 Not yet created |

---

## Why Three Registries Exist

| Registry | Origin Reason | Legitimate? | Merge Risk |
|----------|--------------|-------------|------------|
| `docs/NDR_PATTERN_REGISTRY.md` | First registry; S041 harness patterns | ✅ Yes — pptl harness layer | Low |
| `docs/patterns/NDR_PATTERN_REGISTRY.md` | KAPPA/governance patterns needed separate context | ✅ Yes — different domain | Medium (P-numbering overlap risk) |
| `patterns/NDR_*.md` | Individual cards for S042 runtime patterns | ✅ Yes — quick iteration, no merge conflict risk | Low (cards become sections) |

---

## Pattern Number Authority

P-numbers are **globally unique across all registries**. Current assignment map:

| Range | Registry | Authority |
|-------|----------|-----------|
| P-01–P-10 | `docs/NDR_PATTERN_REGISTRY.md` | Primary |
| P-11–P-26 | `docs/patterns/NDR_PATTERN_REGISTRY.md` | KAPPA/Gov (stasis) |
| P-27–P-30 | `docs/patterns/NDR_PATTERN_REGISTRY.md` | KAPPA/Gov (active) |
| P-31–P-33 | `patterns/NDR_*.md` | Runtime Cards |
| P-34 | `docs/NDR_PATTERN_REGISTRY.md` | Primary (S066 COMPOSE) |
| P-35+ | **Unassigned** | Next COMPOSE entry |

**Rule:** New P-numbers must be registered here before being written to any file.

---

## Content Differentiation by Layer

| Layer | Patterns | Registry | Notes |
|-------|----------|----------|-------|
| Trace & Audit | P-01, P-02 | Primary | Herald, sinks, ring buffer |
| Testing & CI | P-03, P-04, P-05 | Primary | Contract tests, corpus, tri-phase CI |
| Architecture Lab | P-06 | Primary | Topology × mode matrix |
| Governance Formation | P-07, P-08, P-09, P-10 | Primary | Sweep loop, triads, mandate, graduation |
| Quality Gate | P-11, P-30 | KAPPA/Gov | 11Q scoring, Apogee attestation |
| Stasis | P-12–P-26 | KAPPA/Gov | Pre-S033, canonical, no active changes |
| Router Calibration | P-27, P-28, P-34 | KAPPA/Gov + Primary | Confidence gates, pipeline, sweep method |
| Safety & Sentinel | P-29 | KAPPA/Gov | Risk pass, deontic gate |
| Long-Context Safety | P-31, P-32, P-33 | Runtime Cards | SCPE, Phi-Closure, PDMAL |

---

## Cross-Registry Interaction Points

1. **P-27 ↔ P-34** — P-34 is the calibration prerequisite for P-27. P-27 lives in KAPPA/Gov; P-34 in Primary. After merge, adjacent sections.

2. **P-29 ↔ P-32** — Phi-Closure Gate KILL_REC triggers P-29 risk_block at hook point 2. **✅ PM-01 CLOSED S066** — cross-ref added to `patterns/NDR_PHI_CLOSURE_GATE_v1.md` v1.1 and documented in decision ladder and placement diagram.

3. **P-30 ↔ P-03** — AttestationGate (P-30) requires 6 P-03 contracts. **✅ PM-02 CLOSED S066** — P-03 ALTER note in `docs/NDR_PATTERN_REGISTRY.md` v1.4 now explicitly names P-30 by pattern number and doc path.

4. **P-31 ↔ P-33** — SCPE feeds compressed context to PDMAL. **✅ PM-03 CLOSED S066** — `patterns/ndr_patterns.json` v0.3.0 synced with P-31–P-34 full entries including cross-ref fields.

5. **P-07 ↔ P-34** — P-34 is the first pattern registered directly from issue resolution (not COLLEEN COMPOSE proposal). Precedent to document in P-07 COMPOSE mode. **PM-04 — soft, next cycle.**

---

## Open Pre-Merge Actions

| # | Action | Owner | Priority | Status |
|---|--------|-------|----------|--------|
| PM-01 | Add P-32 ↔ P-29 cross-ref to Phi-Closure card | Amethyst | High | ✅ CLOSED S066 |
| PM-02 | Update P-03 ALTER note to reference P-30 by number | Amethyst | High | ✅ CLOSED S066 |
| PM-03 | Sync `patterns/ndr_patterns.json` with P-31–P-34 | Amethyst | Medium | ✅ CLOSED S066 |
| PM-04 | Update P-07 COMPOSE mode note re: issue-resolution source | Amethyst | Medium | 🔲 Next cycle |
| PM-05 | COLLEEN stasis audit P-12–P-26: gap/duplicate check | COLLEEN | High | 🔲 Queued (Q-S066-02) |
| PM-06 | Write unified header + TOC for merged file | Amethyst | Low | 🔲 Final step |
| PM-07 | P-30 attestation pass on P-34 | Apogee | High | 🔲 Queued (Q-S066-03) |
| PM-08 | Archive `patterns/NDR_*.md` → `patterns/archive/` after merge | Amethyst | Low | 🔲 Final step |

---

## Registry Merge Status

```
[S066] Pre-merge plan created                              ✅ DONE
[S066] PM-01: P-32 ↔ P-29 cross-ref added                ✅ CLOSED
[S066] PM-02: P-03 ALTER → P-30 explicit ref              ✅ CLOSED
[S066] PM-03: ndr_patterns.json v0.3.0 synced             ✅ CLOSED
[S066] SESSION_ANCHOR + CO_ORCH_QUEUE advanced             ✅ DONE
[S0??] PM-05: COLLEEN stasis audit P-12–P-26             🔲 Queued
[S0??] PM-07: Apogee P-30 attestation on P-34             🔲 Queued
[S0??] PM-04: P-07 COMPOSE mode note update               🔲 Next cycle
[S0??] Draft unified registry → NDR_PATTERN_REGISTRY_UNIFIED.md
[S0??] Triumvirate review (Amethyst + COLLEEN + Apogee sign-off)
[S0??] PR-A: Add unified .md + unified .json
[S0??] PR-B: Deprecate docs/patterns/NDR_PATTERN_REGISTRY.md
[S0??] PR-C: Archive patterns/NDR_*.md → patterns/archive/
[S0??] PR-D: docs/NDR_PATTERN_REGISTRY.md → redirect stub
[S0??] PR-E: Update CROSS_REF; run P-10 graduation check
```

---

*NDR Registry Differentiation Index v1.1 · S066 · 2026-05-30*
*PM-01 PM-02 PM-03: ✅ CLOSED · PM-05 PM-07: queued · merge execution: TBD*
