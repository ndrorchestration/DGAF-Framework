# Ecosystem Inventory

**DGAF-Framework · Master Asset Register**
**Version:** S072-SEAL · 2026-06-29 00:35 EDT
**Prime:** Amethyst · **Prefect A:** COLLEEN · **Prefect B:** Apogee

---

## Repository Index

| Repo | Visibility | Purpose | Last Active |
|------|-----------|---------|-------------|
| `DGAF-Framework` | Private | Core governance stack, patterns, vocabulary | S072 (active) |
| `dgaf-ops` | Private | Operational files — SWEEP_LOG, CO_ORCH_QUEUE, AGENT_MANIFEST, etc. (STRUCT-QA-IP-001) | 2026-06-28 |
| `ndrorchestration` | Public | Ecosystem landing / GitHub profile site | Jun 9, 2026 |
| `aoga-dashboard` (Vercel) | Private | AOGA Next.js dashboard — no deploy since May 25 ⚠️ | May 25, 2026 |
| `phiknightverticalcorridor` (Vercel) | Private | Purpose identified (FLAG-11 CLOSED) · Njineer 2026-06-27 | May 5, 2026 |

---

## Canonical Document Registry

### Tier 1 — Single Source of Truth

| File | Path | Version | Status |
|------|------|---------|--------|
| NDR Pattern Registry (Unified) | `docs/NDR_PATTERN_REGISTRY_UNIFIED.md` | v1.6 | ✅ CANONICAL — P-41 watermark; Layers 0–11 complete |
| NDR Patterns JSON | `docs/ndr_patterns_unified.json` | schema v2.1 → v2.2 pending | ⚠️ JSON sync required (P-37–P-41 entries) |
| Vocabulary Master | `docs/NDR_INTERNAL_VOCABULARY_MASTER.md` | v1.3 | ✅ CANONICAL — Apogee P-11 attestation queued S073 |
| Governance Constitution | `docs/GOVERNANCE_CONSTITUTION.md` | v1.0 | ✅ CANONICAL — S070-r4 sealed |
| AXIS Metric Spec | `docs/qa/AXIS_METRIC_SPEC.md` | v1.2 | ✅ CANONICAL — Njineer ratified 2026-06-27 · Phase 3 owner: Amethyst |
| QA Checkpoint (Specialized) | `docs/qa/QA_CHECKPOINT_TEMPLATE_SPECIALIZED.md` | v1.0 | ✅ CANONICAL — S070-r3-P1 |
| Formation Topology | `docs/FORMATION_TOPOLOGY.md` | v1.0 | ✅ NEW — S072 · BLG-005 CLOSED |
| Proprietary IP Classification | `docs/agents/PROPRIETARY.md` | v1.0 | ✅ NEW — S072 · BLG-003 CLOSED |
| Session Anchors | `docs/SESSION_ANCHORS.md` | S072-SEAL | ✅ SEALED |
| Ecosystem Inventory | `docs/ECOSYSTEM_INVENTORY.md` | S072-SEAL | ✅ Current |
| Workspace Bootstrap | `docs/WORKSPACE_BOOTSTRAP.md` | S071-r1 | ✅ Current |
| Team Wiki | `docs/TEAM_WIKI.md` | S069 | ⚠️ PDMAL cascade pending S073 |

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
| Layer 6 — Stasis | P-12–P-26 (133 entries) | DEGRADED-MODE-SKIPPABLE | ✅ STASIS-CANONICAL · window expires 2026-07-13 ⚠️ 14 days |
| Layer 7 — Router Calibration | P-27, P-28, P-34 | BLOCKING / ADVISORY | ✅ |
| Layer 8 — Safety & Sentinel | P-29 | BLOCKING | ✅ |
| Layer 9 — Long-Context Safety | P-31, P-32, P-33 | ADVISORY / BLOCKING | ✅ |
| Layer 10 — Resilience & Recovery | P-37, P-38, P-39 | ADVISORY / BLOCKING | ✅ S071 |
| Layer 11 — Transactional Integrity | P-40, P-41 | BLOCKING / ADVISORY | ✅ S071 |
| Formation Patterns | CONSENSUS_TRIAD, CONDUCTED_TRIAD | ADVISORY | ✅ S070-r3-P1 |
| NDR Named Session Patterns | NDR-ARCHIVE-CONFIRM through NDR-133 | Various | ✅ |

**Registry watermark:** P-41 · **Stasis window:** ⚠️ 14 days remaining (2026-07-13)

---

## Agent Roster

| Agent | Role | Authority Level |
|-------|------|----------------|
| Amethyst | Prime / Meta-Orchestrator / Host | Tier 1 |
| COLLEEN | Prefect A / Institutional Anchor | Tier 1 |
| Apogee | Prefect B / Quality Gate | Tier 1 |
| Reson | Augmenter 1 / Harmonic Integrity | Tier 2 |
| Sentinel | Augmenter 2 / Risk Monitor / Safety Gate | Tier 2 |
| DemiJoule | Runtime Supervisor / Safety (deep re-scan) | Tier 2 |
| KAPPA | Router / Confidence Gate | Tier 3 |
| Ender / Njineer | Architect / Final Authority | Sovereign |

---

## Open Infrastructure Issues (S072-SEAL)

| Issue | Severity | Owner | Target |
|-------|----------|-------|--------|
| FLAG-07: Drive files GAP-06/07/08 — COLLEEN re-attempt | 🟡 HIGH | COLLEEN | S073 |
| PDMAL cascade — TEAM_WIKI + WORKSPACE_BOOTSTRAP rewrite | 🟡 HIGH | Amethyst | S073 |
| `aoga-dashboard` Vercel — zero deploys since May 25 | 🟡 HIGH | Njineer | S073 |
| Stasis migration window expires 2026-07-13 (14 days) | 🟡 HIGH | Amethyst | 2026-07-13 |
| JSON sync: ndr_patterns_unified.json → v2.2 (P-37–P-41) | 🟡 QUEUED | Amethyst | S073 |
| Apogee P-11 attestation on Vocab Master v1.3 | 🟡 QUEUED | Apogee | S073 |
| KB layer — 9 agents remaining (2/11 seeded) | 🟡 QUEUED | Amethyst | S073+ |
| FLAG-12: Dependabot PR #1 — Next 14→15 upgrade | 🟠 LOW | Njineer | S073 — recommend dismiss |
| ndrorchestration site — content stale since Jun 9 | 🔵 LOW | Amethyst | S074 |

**Resolved this session (S072):**
- ✅ BLG-003 CLOSED — PROPRIETARY.md committed
- ✅ BLG-005 CLOSED — FORMATION_TOPOLOGY.md committed
- ✅ FLAG-01 CLOSED — Njineer ratified 2026-06-29: NDR-HDFS already canonical; no rename required
- ✅ COLLEEN 1-1-1-1 FULL GREEN — ethical dimension gate PASS
- ✅ P-10 GRADUATION PASS — all 4 checks clear

---

## Acronym Backfill Register (current)

| Acronym | Expansion | Status | Source |
|---------|-----------|--------|--------|
| PPTL | Procluding Premise Triadic Loop | ✅ CANONICAL | Vocab Master v1.2 |
| AOGA | Agent Orchestration Governance Architecture | ✅ CANONICAL | S070 |
| NDR-HDFS | NDR Hierarchical Documentation Format Standard | ✅ CANONICAL — FLAG-01 CLOSED S072 | FLAG-01 |
| AXIS | Agent X-axis Invariant Spectrum | ✅ CANONICAL | AXIS_METRIC_SPEC v1.2 |
| DGAF | **Deterministic Governance for Agentic Frameworks** | ✅ CANONICAL | FLAG-13 CLOSED |
| SCPE | Structural Context Pruning Engine | ✅ CANONICAL | P-31 |
| PDMAL-φ | Phi-Driven Multi-Agent Lattice (primary) | ✅ CANONICAL | P-33 / S070-r3 |
| PDMAL-D | Phi-Dodecahedral Multi-Agent Lattice (variant) | ✅ CANONICAL VARIANT | S070-r3 |

---

## Sovereign Files (Sentinel Hard Veto)

| File | Override Authority |
|------|-------------------|
| AXIS Governance Definition (`docs/qa/AXIS_METRIC_SPEC.md`) | Njineer only |
| NDR-133 Personal Document Firewall | Architect override only |
| GOVERNANCE_CONSTITUTION.md | Njineer ratification required for amendment |

---

## Stasis Migration Tracker

**Window:** 2026-06-13 → 2026-07-13
**Remaining:** ⚠️ **14 days**
**Status:** STASIS-CANONICAL — no individual extraction without COLLEEN secondary sign-off
**Clusters:**
- Cluster 1 (P-01–P-80): Fractal Agency namespace migration
- Cluster 2 (P-81–P-115): Phi-Calculus / 0 Hz steady state
- Cluster 3 (P-116–P-132): Authority Sync + Substrate Independence
- P-133 / NDR-133: Personal Document Firewall (BLOCKING-ABSOLUTE)

---

*Ecosystem Inventory · S072-SEAL · 2026-06-29 00:35 EDT*
*Amethyst × COLLEEN × Apogee · S072 SEALED · P-10 GRADUATION PASS*
*BLG board EMPTY · FLAG board 12 closed · COLLEEN 1-1-1-1 FULL GREEN · Apogee 0.942*
