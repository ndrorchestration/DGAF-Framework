# FORMATION TOPOLOGY
**Classification:** T1 PUBLIC  
**Maintainer:** Amethyst (meta-orchestrator)  
**Version:** 1.1  
**Last Updated:** 2026-06-29 (Phase 4 — 20-seat roster expansion; PDMAL-φ / Dodecahedral T3 extension layer registered; Strategic Quintet + Operational Swarm + Resonance Cluster formation specs added)
**BLG Reference:** BLG-005 (CLOSED)

---

## 1. Purpose

This document is the canonical specification for all named agent formations within the DGAF (Dynamic Governance Agentic Formation) Framework. It defines:

- Formation names, member composition, and seat counts
- Activation conditions and authority scope per formation
- Topology algebra — rules for composition, intersection, and promotion
- Disambiguation from ad-hoc groupings

Formations are **not** ad-hoc groupings. A formation is a named, structurally defined multi-agent configuration with a specific governance purpose, authority scope, and activation threshold.

---

## 2. Agent Roster (Formation Atoms)

The full DGAF taxonomy spans **20 agent seats** across three operational tiers plus a T3 SOVEREIGN extension layer.

### T1/T2 Operational Layer (GitHub-resident specs)

| ID | Agent | Role Class | Tier | Classification |
|----|-------|-----------|------|----------------|
| A-00 | **Amethyst** | Meta-Orchestrator | Strategic Quintet | T1 PUBLIC |
| A-01 | **Apogee** | Verification / Scoring | Strategic Quintet | T1 PUBLIC |
| A-02 | **Perigee** | Boundary / Security Filter | Strategic Quintet | T1 PUBLIC |
| A-03 | **Nova** | Innovation / Simulation | Strategic Quintet | T2 FRAMEWORK |
| A-04 | **Professor Prodigy** | Intellectual Catalyst | Strategic Quintet | T1 PUBLIC |
| A-05 | **COLLEEN** | Swarm Lead / Continuity | Operational Swarm | T1 PUBLIC |
| A-06 | **The Librarian** | Archive / Provenance | Operational Swarm | T1 PUBLIC |
| A-07 | **The Auditor** | QA / Constraint Verify | Operational Swarm | T1 PUBLIC |
| A-08 | **The Actualizer** | Execution / Code Gen | Operational Swarm | T1 PUBLIC |
| A-09 | **Zenith** | System High / Compute | Operational Swarm | T2 FRAMEWORK |
| A-10 | **Reson** | Harmonic Coherence | Resonance Cluster | T1 PUBLIC |
| A-11 | **Lyra** | Synthesis / Narrative | Resonance Cluster | T2 FRAMEWORK |
| A-12 | **Echolette** | Pattern Amplification | Resonance Cluster | T2 FRAMEWORK |
| A-13 | **Ionia** | Modal Lock (0Hz) | Resonance Cluster | T2 FRAMEWORK |

### T3 SOVEREIGN Extension Layer (Drive-resident specs)

> Agent names and operational specs for A-14 through A-19 are T3 SOVEREIGN. Full definitions reside in Google Drive. See `PROPRIETARY.md` → SOV-005 (PDMAL-φ) and SOV-006 (Dodecahedral). GitHub holds seat IDs and geometry pointers only. Njineer supplies names when ready to surface.

| ID | Stub | Geometry | SOV Ref |
|----|------|----------|--------|
| A-14 | [PDMAL Node 1] | PDMAL-φ | SOV-005 |
| A-15 | [PDMAL Node 2] | PDMAL-φ | SOV-005 |
| A-16 | [PDMAL Node 3] | PDMAL-φ | SOV-005 |
| A-17 | [Dodecahedral Face 1] | Dodecahedral | SOV-006 |
| A-18 | [Dodecahedral Face 2] | Dodecahedral | SOV-006 |
| A-19 | [Dodecahedral Face 3] | Dodecahedral | SOV-006 |

> Full agent specs in `docs/agents/[AGENT]_SPEC.md`. Memory state in `docs/agents/[AGENT]_MEMORY.md`.

---

## 3. Named Formations

### 3.1 Harmonic Quintet
**Seats:** 5  
**Members:** Amethyst (A-00) · Apogee (A-01) · COLLEEN (A-05) · Reson (A-10) · Sentinel  
**Activation:** Default formation for all standard governance sweep, evaluation, and compliance cycles.  
**Authority Scope:** Full read/write on all T1 PUBLIC documents. No sovereign (T3) file access.  
**Quorum:** 3/5 for advisory outputs; 5/5 for structural commits (new files, BLG closures).  
**Topology Class:** `CORE-5` — stable, always-available, no promotion required.

---

### 3.2 Strategic Quintet
**Seats:** 5  
**Members:** Amethyst (A-00) · Apogee (A-01) · Perigee (A-02) · Nova (A-03) · Professor Prodigy (A-04)  
**Activation:** Governance cycles; vision-to-execution Logic Bridge; 10-year simulation runs; formal proof reviews.  
**Authority Scope:** T1/T2 read/write for governance docs. T3 access requires Njineer approval.  
**Quorum:** 3/5 advisory; 5/5 for architectural decisions.  
**Activation constraint:** Nova (A-03) is advisory-only until COLLEEN Terminal Unblocking Event (L5 Executor gate) clears.  
**Topology Class:** `GOV-5` — governance layer; runs concurrently with Operational Swarm.

---

### 3.3 Operational Swarm
**Seats:** 5  
**Members:** COLLEEN (A-05) · The Librarian (A-06) · The Auditor (A-07) · The Actualizer (A-08) · Zenith (A-09)  
**Activation:** Trunk stabilization; L5 Executor delivery; code generation; archival; Batch 1A extraction.  
**Authority Scope:** T1/T2 write (code, artifacts, archives). NDR-Protocol-01 State Sync governs write order.  
**Quorum:** 3/5 for task outputs; 5/5 for canonical doc updates.  
**Write order:** Auditor → Actualizer → COLLEEN → Apogee → Amethyst (NDR-Protocol-01).  
**Topology Class:** `OPS-5` — heavy-lifting layer; highest throughput formation.

---

### 3.4 Resonance Cluster
**Seats:** 4  
**Members:** Reson (A-10) · Lyra (A-11) · Echolette (A-12) · Ionia (A-13)  
**Activation:** Talent quantization; harmonic tuning; Schizophonic studio work; Signal Chain / Gain Staging sessions.  
**Authority Scope:** Read T1/T2. Write to pattern registries, harmonic score records, and integration layer files.  
**Quorum:** 3/4.  
**Ionia role:** Locks formation to Ionian Modal Harmonic (0Hz) — ensures outputs feel harmonious and audit-ready.  
**Topology Class:** `RESONANCE-4` — downstream of Operational Swarm; feeds harmonic validation upward.

---

### 3.5 Full Ensemble
**Seats:** 14 (T1/T2 operational) + 6 (T3 stubs when Njineer surfaces names)  
**Members:** All A-00 through A-13 (operational); A-14 through A-19 (T3 — activated by Njineer only)  
**Activation:** Triggered by Amethyst on architectural restructuring events, cross-formation conflicts, or v* release gates.  
**Authority Scope:** Full T1 + T2. T3 access requires Njineer explicit approval per session.  
**Quorum:** 8/14 operational advisory; 11/14 for structural commits.  
**Topology Class:** `FULL-20` — requires explicit Amethyst activation call.

---

### 3.6 Evaluation Triad
**Seats:** 3  
**Members:** Amethyst (A-00) · Apogee (A-01) · Reson (A-10)  
**Activation:** Targeted scoring runs; pre-commit quality checks; gate P-* threshold verification.  
**Authority Scope:** Read-only all layers. Write to scoring/signal records only.  
**Quorum:** 2/3.  
**Topology Class:** `EVAL-3` — lightweight, low-latency, no Sentinel overhead.

---

### 3.7 Compliance Dyad
**Seats:** 2  
**Members:** COLLEEN (A-05) · Sentinel  
**Activation:** Any action touching ethical boundaries, sovereign IP, or security perimeter.  
**Authority Scope:** Read T1/T2/T3 (audit mode). Write to compliance flags and PROPRIETARY.md redaction records only.  
**Quorum:** 2/2 (unanimous — no split-vote resolution).  
**Topology Class:** `GATE-2` — veto-capable. Any agent may invoke; output is binding.

---

### 3.8 Integration Pair
**Seats:** 2  
**Members:** Lyra (A-11) · Echolette (A-12)  
**Activation:** Pattern synthesis, cross-document harmonization, echo amplification.  
**Authority Scope:** Read T1/T2. Write to pattern registries and integration layer files only.  
**Quorum:** 2/2.  
**Topology Class:** `SYNTH-2` — downstream of Harmonic Quintet; feeds outputs upward.

---

### 3.9 Herald Relay
**Seats:** 1  
**Members:** Herald  
**Activation:** External-facing output generation — user reports, session summaries, external API responses.  
**Authority Scope:** Read T1 only. No write access to internal docs.  
**Topology Class:** `RELAY-1` — output-only boundary agent.

---

## 4. Topology Algebra

### 4.1 Formation Composition Rules

```
Strategic Quintet ∩ Operational Swarm = {Amethyst}  (shared conductor)
Strategic Quintet ∩ Resonance Cluster = ∅
Operational Swarm ∩ Resonance Cluster = {Reson via Harmonic Quintet bridge}
Harmonic Quintet ⊂ Full Ensemble
Evaluation Triad ⊂ Harmonic Quintet
Compliance Dyad ⊂ Harmonic Quintet
Integration Pair ⊂ Resonance Cluster
Herald Relay ∩ [all other formations] = ∅
T3 Extension (A-14→A-19) ⊂ Full Ensemble only (Njineer activation required)
```

### 4.2 Promotion Rules

| From | To | Trigger | Amethyst Call Required |
|---|---|---|---|
| Evaluation Triad | Harmonic Quintet | Compliance gate needed | No — auto-promote |
| Harmonic Quintet | Full Ensemble | Architectural event | Yes — explicit |
| Compliance Dyad | Harmonic Quintet | Escalation | No — auto-promote |
| Any | Full Ensemble | T3 access needed | Yes + Njineer approval |
| Strategic Quintet | Full Ensemble | 10-year simulation requires T3 geometry | Yes + Njineer approval |
| Operational Swarm | Full Ensemble | L5 Executor + moonshot activation | Yes — Nova gate clears after COLLEEN TUE |

### 4.3 Concurrency Rules

- **Strategic Quintet + Operational Swarm** may run concurrently (single shared member: Amethyst as conductor).
- **Resonance Cluster + Operational Swarm** may run concurrently (disjoint).
- **Compliance Dyad** blocks all writes on affected files during active gate review.
- **Full Ensemble** is exclusive — no sub-formations run independently while Full Ensemble is active.
- **NDR-Protocol-01:** Only one tier writes to Canonical Protocol at a time (Auditor → Actualizer → COLLEEN → Apogee → Amethyst).

### 4.4 Conflict Resolution

1. Compliance Dyad veto overrides all.
2. Higher seat-count formation takes precedence.
3. Ties resolved by Amethyst casting vote.
4. Perigee boundary block auto-executes — no vote required.
5. Unresolvable conflicts escalate to Njineer.

---

## 5. Activation State Machine

```
[IDLE]
  │
  ├─ governance / vision cycle ──────────► [STRATEGIC QUINTET ACTIVE]
  │                                               │
  │                                    └─ arch event ─────► [FULL ENSEMBLE]
  │
  ├─ standard sweep trigger ──────────────► [HARMONIC QUINTET ACTIVE]
  │                                               │
  │                                    ├─ compliance touch ──► [+ COMPLIANCE DYAD]
  │                                    ├─ eval only ──────────► [EVALUATION TRIAD]
  │                                    └─ arch event ─────────► [FULL ENSEMBLE]
  │
  ├─ trunk / L5 delivery ─────────────────► [OPERATIONAL SWARM ACTIVE]
  │                                               │
  │                                    └─ Nova TUE cleared ──► [+ STRATEGIC QUINTET]
  │
  ├─ talent / harmonic work ──────────────► [RESONANCE CLUSTER ACTIVE]
  │
  ├─ pattern/registry work ──────────────► [INTEGRATION PAIR ACTIVE]
  │
  └─ output generation ──────────────────► [HERALD RELAY ACTIVE]
```

---

## 6. Sovereign Topology Reference

The full 20-agent formation geometry is grounded in two T3 SOVEREIGN mathematical structures:

| SOV ID | Structure | Role in Topology | Drive Ref |
|---|---|---|---|
| SOV-005 | PDMAL-φ Agent Taxonomy | Defines operational logic for A-14, A-15, A-16 | `Drive://DGAF/Sovereign/SOV-005_PDMAL_Taxonomy.md` |
| SOV-006 | Dodecahedral Formation Geometry | Maps A-17, A-18, A-19 to pentagonal face nodes; provides structural closure for 20-seat swarm and Substrate Independence (0Hz) | `Drive://DGAF/Sovereign/SOV-006_Dodecahedral_Geometry.md` |

The Dodecahedral geometry (12 pentagonal faces) is the spatial substrate that maintains **Substrate Independence (0Hz)** across the full 20-agent formation, preventing Type 2 Implementation Drift.

---

## 7. Amendment Protocol

1. **Full Ensemble** vote (11/14 quorum) for structural changes.
2. **Harmonic Quintet** vote (5/5) for editorial corrections.
3. All amendments logged in `docs/SWEEP_LOG.md` with SWP-* entry prior to commit.
4. Njineer retains final authority on all amendments.

---

## 8. Version History

| Version | Date | Author | Change |
|---|---|---|---|
| 1.0 | 2026-06-28 | Amethyst + Njineer | Initial creation — BLG-005 closure |
| 1.1 | 2026-06-29 | Amethyst + Njineer | 20-seat roster; PDMAL-φ / Dodecahedral T3 layer; Strategic Quintet, Operational Swarm, Resonance Cluster formation specs; NDR-Protocol-01 write order; Nova TUE gate |

---

*Classification: T1 PUBLIC*  
*Sovereign mathematics governing formation dynamics: see PROPRIETARY.md → SOV-001 through SOV-006*
