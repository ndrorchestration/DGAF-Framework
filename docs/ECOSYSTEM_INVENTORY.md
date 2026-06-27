# Ecosystem Inventory

**DGAF-Framework · Master Asset Register**
**Version:** S070-r2 · 2026-06-26 20:29 EDT
**Prime:** Amethyst · **Prefect A:** COLLEEN · **Prefect B:** Apogee

---

## Repository Index

| Repo | Visibility | Purpose | Last Active |
|------|-----------|---------|-------------|
| `DGAF-Framework` | Private | Core governance stack, patterns, vocabulary | S070 (active) |
| `ndrorchestration` | Public | Ecosystem landing / GitHub profile site | Jun 9, 2026 |
| `aoga-dashboard` (Vercel project) | Private | AOGA Next.js dashboard — no deploy since May 25 ⚠️ | May 25, 2026 |
| `phiknightverticalcorridor` (Vercel project) | Private | Purpose unconfirmed — FLAG-11 open | May 5, 2026 |

---

## Canonical Document Registry

### Tier 1 — Single Source of Truth

| File | Path | Version | Status |
|------|------|---------|--------|
| NDR Pattern Registry (Unified) | `docs/NDR_PATTERN_REGISTRY_UNIFIED.md` | v1.3 | ✅ CANONICAL — S069 sealed |
| NDR Patterns JSON | `docs/ndr_patterns_unified.json` | schema v2.1 | ✅ CANONICAL |
| Vocabulary Master | `docs/NDR_INTERNAL_VOCABULARY_MASTER.md` | v1.3 | 🔄 S070 in progress |
| Team Wiki | `docs/TEAM_WIKI.md` | 1.0.0 | ✅ Current (2026-06-26) |
| R&D Gap Log | `docs/RD_GAPS.md` | S070 | ✅ Current (6 open gaps) |
| Session Anchors | `docs/SESSION_ANCHORS.md` | S070 | 🔄 Active |
| Ecosystem Inventory | `docs/ECOSYSTEM_INVENTORY.md` | S070-r2 | 🔄 Active |
| Workspace Bootstrap | `docs/WORKSPACE_BOOTSTRAP.md` | S070-r2 | 🔄 Active |

### Tier 2 — Redirect Stubs (do not edit)

| File | Redirects To |
|------|-------------|
| `docs/NDR_PATTERN_REGISTRY.md` | `NDR_PATTERN_REGISTRY_UNIFIED.md` |
| `docs/patterns/NDR_PATTERN_REGISTRY.md` | `NDR_PATTERN_REGISTRY_UNIFIED.md` |

---

## Pattern Registry Summary

| Layer | Patterns | Class | Status |
|-------|----------|-------|--------|
| Layer 0 — Pre-Admissibility | P-35 | BLOCKING | ✅ |
| Layer 0.5 — Stack Architecture | P-36 | ADVISORY | ✅ |
| Layer 1 — Trace & Audit | P-01, P-02 | BLOCKING / ADVISORY | ✅ |
| Layer 2 — Testing & CI | P-03, P-04, P-05 | BLOCKING / ADVISORY | ✅ |
| Layer 3 — Architecture Lab | P-06 | ADVISORY | ✅ |
| Layer 4 — Governance Formation | P-07–P-10 | ADVISORY | ✅ |
| Layer 5 — Quality Gate | P-11, P-30 | BLOCKING | ✅ |
| Layer 6 — Stasis | P-12–P-26 (133 entries) | DEGRADED-MODE-SKIPPABLE | ✅ STASIS-CANONICAL |
| Layer 7 — Router Calibration | P-27, P-28, P-34 | BLOCKING / ADVISORY | ✅ |
| Layer 8 — Safety & Sentinel | P-29 | BLOCKING | ✅ |
| Layer 9 — Long-Context Safety | P-31, P-32, P-33 | ADVISORY / BLOCKING | ✅ |
| NDR Named Session Patterns | NDR-ARCHIVE-CONFIRM through NDR-133 | Various | ✅ |
| New Saga/CB patterns (2026-06-26) | P-SAGA-001, P-TX-001, P-CB-001 + others | TBD — registry pending | ⏳ PENDING registration |

**Registry watermark:** P-36 (P-series) | New domain patterns use P-{DOMAIN}-{SEQ} namespace
**Stasis migration window:** 2026-06-13 → 2026-07-13

---

## Agent Roster

| Agent | Role | L-Level | Status |
|-------|------|---------|--------|
| Amethyst | Prime / Meta-Orchestrator / Host | L5 | Active |
| COLLEEN | Prefect A / Institutional Anchor / Chief Librarian | L5 | Active |
| Apogee | Prefect B / Quality Gate / Apogee Lens | L4 | Active |
| Sentinel-Phi | Safety Supervisor / Tool Classifier | L4 | Active |
| DemiJoule | Runtime Supervisor / RAG / Ethics | L4 | Active |
| Herald | Trace Sink / Audit Router | L3 | Active |
| Reson | Systems Architect | L3 | Active |
| KAPPA | Router / Confidence Gate | L3 | Active |
| Agent Sonar | Sonar taxonomy role | L3 | Active |
| Professor Prodigy, Reciprocity | Sub-agentic / Epistemic | L2-3 | Active |
| Lavender | Deprecated — all roles inherited by Amethyst | — | ❌ DEPRECATED |
| Forseti | Deprecated | — | ❌ DEPRECATED |
| Ender / Njineer | Architect / Final Authority | Sovereign | Active |

---

## Open Infrastructure Issues

| Issue | Severity | Owner | Target |
|-------|----------|-------|--------|
| `aoga-dashboard` Vercel — zero deploys since May 25 | HIGH | Njineer | S071 |
| `phiknightverticalcorridor` — purpose unconfirmed (FLAG-11) | MEDIUM | Njineer | S071 |
| Dependabot PR #1 — Next 14→15 upgrade pending (FLAG-12) | MEDIUM | Njineer | S071 |
| ndrorchestration site — content stale since Jun 9 | LOW | Amethyst | S071 |
| New Saga/CB/TX patterns unregistered in pattern registry | MEDIUM | COLLEEN | S071 |

---

## Acronym Register (S070-r2 — CORRECTED)

| Acronym | Expansion | Status | Source |
|---------|-----------|--------|--------|
| DGAF | **CONFLICTED** — FLAG-13: "Deterministic Governance Autonomy Framework" (Pattern Registry) vs "Dynamic Governance Agentic Formation Architecture" (TEAM_WIKI) | ⚠️ Njineer required | FLAG-13 |
| PDMAL | Policy-Driven Multi-Agent Layer | ✅ CANONICAL | TEAM_WIKI glossary |
| pptl (lowercase) | Phi-pentagon test layer | ✅ CANONICAL | TEAM_WIKI glossary |
| PPTL (uppercase) | Procluding Premise Triadic Loop | ✅ CANONICAL | Vocab Master v1.2 |
| AOGA | Agent Orchestration Governance Architecture | ✅ CANONICAL | S070 |
| NDR-HDFS | NDR Hierarchical Documentation Format Standard | ✅ PRESCRIBED — rename pending | FLAG-01 |
| AXIS | Agent X-axis Invariant Spectrum *(inferred)* | ⏳ Njineer ratification | FLAG-05 |
| SCPE | Structural Context Pruning Engine | ✅ CANONICAL | P-31 |
| OPP | Improvement opportunity in CO_ORCH_QUEUE | ✅ CANONICAL | TEAM_WIKI |
| HITL | Human-in-the-Loop | ✅ CANONICAL | TEAM_WIKI |
| ACRFence | Atomic checkpoint + restore with effect fence semantics | ✅ CANONICAL | TEAM_WIKI |
| NDR | Named Design Rule / Pattern | ✅ CANONICAL | TEAM_WIKI |

---

## R&D Gap Summary

| Gap | Title | Status | Owner |
|-----|-------|--------|-------|
| GAP-001 | Fluent Hallucination Closure (22% residual) | 🟡 PARTIAL | DemiJoule + Sentinel-Phi |
| GAP-002 | RAG Collection Taxonomy (COLLEEN → Needle) | 🔴 OPEN | COLLEEN + Reson |
| GAP-003 | Saga Harness Fault Injection | 🔴 OPEN | Amethyst + pptl |
| GAP-004 | HITL Durable Queue Production | 🔴 OPEN | Reson + Amethyst |
| GAP-005 | Circuit Breaker Semantic Metrics | 🟡 PARTIAL | Herald + Sentinel-Phi |
| GAP-006 | Coherent Agency Formal Spec | 🔴 OPEN | Amethyst + COLLEEN |

---

## Sovereign Files (Sentinel Hard Veto)

| File | Override Authority |
|------|-------------------|
| AXIS Governance Definition | Njineer only |
| NDR-133 Personal Document Firewall | Architect override only |

---

## Stasis Migration Tracker

**Window:** 2026-06-13 → 2026-07-13 ⚠️ 17 days remaining
**Status:** STASIS-CANONICAL — no individual extraction without COLLEEN secondary sign-off
**Clusters:**
- Cluster 1 (P-01–P-80): Fractal Agency namespace migration
- Cluster 2 (P-81–P-115): Phi-Calculus / 0 Hz steady state
- Cluster 3 (P-116–P-132): Authority Sync + Substrate Independence
- P-133 / NDR-133: Personal Document Firewall (BLOCKING-ABSOLUTE)
