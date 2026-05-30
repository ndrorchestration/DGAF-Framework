# NDR Registry Differentiation Index

**DGAF-Framework · S066**
Authority: COLLEEN (archival) | Amethyst (meta-orchestration)
Created: 2026-05-30 | Status: **Active — pre-merge tracking document**

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
| **Primary** | `docs/NDR_PATTERN_REGISTRY.md` | v1.3 / S066 | Harness, CI, triads, mandate, graduation, cross-ref index | P-01–P-10 (full spec) + P-11–P-34 (index) | ✅ Active |
| **KAPPA/Governance** | `docs/patterns/NDR_PATTERN_REGISTRY.md` | v2.1 / S035 | Router calibration, pipeline composition, sentinel, attestation | P-27–P-30 (full spec) + P-01–P-26 (133 stasis) | ✅ Active |
| **Runtime Cards** | `patterns/NDR_*.md` | v1.0 cards | Long-context safety, drift, convergence | P-31 (SCPE), P-32 (Phi-Closure), P-33 (PDMAL) | ✅ Active |
| **Machine-readable** | `patterns/ndr_patterns.json` | — | JSON index of pattern IDs and names | Subset | ⚠️ Needs sync |
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

These are the seams where patterns in different registries interact directly.
They are the highest-priority items to verify during merge:

1. **P-27 ↔ P-34** — P-34 (Empirical-Sweep) is the calibration prerequisite for
   P-27 (Adaptive-Weighting). P-27 lives in KAPPA/Gov; P-34 lives in Primary.
   After merge, these must be adjacent sections.

2. **P-29 ↔ P-32** — Phi-Closure Gate (P-32, Runtime) `KILL_REC` action should
   trigger P-29 `risk_block` at hook point 2. Currently undocumented in either card.
   **Pre-merge action required:** add cross-ref note to P-32 card before merge.

3. **P-30 ↔ P-03** — AttestationGate (P-30) requires 6 P-03 contracts. P-30 lives
   in KAPPA/Gov; P-03 lives in Primary. After merge, the P-03 ALTER note must
   reference P-30 explicitly by pattern number (currently references "Gate 0" only).

4. **P-31 ↔ P-33** — SCPE (P-31) feeds compressed context to PDMAL (P-33).
   Both in Runtime Cards. This interaction is documented in cards but not in
   `ndr_patterns.json`. **Pre-merge action:** sync JSON index.

5. **P-07 ↔ P-34** — Dual-Agent Sweep Loop (P-07) is the process by which
   new COMPOSE patterns like P-34 are discovered and registered. P-34 is the
   first pattern registered directly from issue resolution (not from COLLEEN
   COMPOSE proposal). This is a precedent — document in P-07 spec under
   COMPOSE mode definition.

---

## Open Pre-Merge Actions

| # | Action | Owner | Priority | Blocking merge? |
|---|--------|-------|----------|-----------------|
| PM-01 | Add P-32 ↔ P-29 cross-ref note to `patterns/NDR_PHI_CLOSURE_GATE_v1.md` | Amethyst | High | ✅ Yes |
| PM-02 | Update P-03 ALTER note to reference P-30 by pattern number | Amethyst | High | ✅ Yes |
| PM-03 | Sync `patterns/ndr_patterns.json` with P-31–P-34 | Amethyst | Medium | ⚠️ Soft |
| PM-04 | Update P-07 COMPOSE mode note re: issue-resolution as valid COMPOSE source | Amethyst | Medium | ⚠️ Soft |
| PM-05 | Resolve P-numbering in stasis block (P-12–P-26): confirm no gaps or duplicates | COLLEEN | High | ✅ Yes |
| PM-06 | Write unified header + table of contents for merged file | Amethyst | Low | 🔲 Final step |
| PM-07 | P-30 attestation pass on P-34 before canonical promotion | Apogee | High | ✅ Yes |
| PM-08 | Archive individual `patterns/NDR_*.md` cards after merge (move to `patterns/archive/`) | Amethyst | Low | 🔲 Final step |

---

## Registry Merge Status

```
[S066] Pre-merge plan created ← YOU ARE HERE
[S0??] PM-01 through PM-05 resolved
[S0??] COLLEEN stasis audit (P-12–P-26) complete
[S0??] Apogee P-30 attestation on P-34 complete
[S0??] Draft unified registry written to docs/NDR_PATTERN_REGISTRY_UNIFIED.md
[S0??] Triumvirate review (Amethyst + COLLEEN + Apogee sign-off)
[S0??] PR: replace docs/NDR_PATTERN_REGISTRY.md with unified
[S0??] PR: deprecate docs/patterns/NDR_PATTERN_REGISTRY.md (redirect note)
[S0??] PR: archive patterns/NDR_*.md cards → patterns/archive/
[S0??] PR: delete patterns/ndr_patterns.json or replace with unified JSON export
[S0??] Session graduation check (P-10) — CROSS_REF updated to unified path
```

---

*Created: S066 · 2026-05-30 · Agent Amethyst*
*Next review: first session that opens a CO_ORCH_QUEUE cycle*
