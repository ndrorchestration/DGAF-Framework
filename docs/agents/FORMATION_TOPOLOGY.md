# FORMATION TOPOLOGY
**Classification:** T1 PUBLIC  
**Maintainer:** Amethyst (meta-orchestrator)  
**Version:** 1.0  
**Last Updated:** 2026-06-28  
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

All formations are composed from the following 9 operational agents + 1 meta-orchestrator:

| ID | Agent | Role Class | Classification |
|----|-------|-----------|----------------|
| A-00 | **Amethyst** | Meta-Orchestrator | T1 PUBLIC |
| A-01 | **Apogee** | Scoring / Evaluation | T1 PUBLIC |
| A-02 | **Reciprocity** | Exchange / Bidirectional Algebra | T1 PUBLIC |
| A-03 | **COLLEEN** | Compliance / Ethical Gate | T1 PUBLIC |
| A-04 | **Reson** | Harmonic Signal / Coherence | T1 PUBLIC |
| A-05 | **Echolette** | Pattern Amplification / Echo | T-2 FRAMEWORK |
| A-06 | **Lyra** | Synthesis / Integration | T-2 FRAMEWORK |
| A-07 | **Herald** | Communication / Output | T1 PUBLIC |
| A-08 | **Sentinel** | Security / Firewall | T1 PUBLIC |
| A-09 | **[Reserved]** | TBD | — |

> Full agent specs in `docs/agents/[AGENT]_SPEC.md`. Memory state in `docs/agents/[AGENT]_MEMORY.md`.

---

## 3. Named Formations

### 3.1 Harmonic Quintet
**Seats:** 5  
**Members:** Amethyst · Apogee · COLLEEN · Reson · Sentinel  
**Activation:** Default formation for all standard governance sweep, evaluation, and compliance cycles.  
**Authority Scope:** Full read/write on all T1 PUBLIC documents. No sovereign (T3) file access.  
**Quorum:** 3/5 for advisory outputs; 5/5 for structural commits (new files, BLG closures).  
**Use Cases:**
- Session sweeps (SWP-* entries)
- BLG triage and closure
- Apogee scoring cycles
- PROPRIETARY boundary enforcement (Sentinel gate active)

**Topology Class:** `CORE-5` — stable, always-available, no promotion required.

---

### 3.2 Full Ensemble
**Seats:** 9  
**Members:** All agents A-00 through A-08  
**Activation:** Triggered by Amethyst on architectural restructuring events, cross-formation conflicts, or v* release gates.  
**Authority Scope:** Full T1 + T2. T3 access requires Njineer explicit approval per session.  
**Quorum:** 5/9 for advisory; 7/9 for structural.  
**Use Cases:**
- Major version releases (v2.x, v3.x gate reviews)
- Cross-agent integration spec approval
- Formation topology amendments (this document)
- Ecosystem inventory audits

**Topology Class:** `FULL-9` — requires explicit Amethyst activation call.

---

### 3.3 Evaluation Triad
**Seats:** 3  
**Members:** Amethyst · Apogee · Reson  
**Activation:** Invoked for targeted scoring runs — Apogee Q-series evaluation, RESON harmonic signal checks, or rapid quality sweeps not requiring compliance gating.  
**Authority Scope:** Read-only on all layers. Write only to scoring/signal records (SWEEP_LOG score fields, ECOSYSTEM_INVENTORY metrics).  
**Quorum:** 2/3.  
**Use Cases:**
- Apogee composite score updates
- RESON coherence audits
- Pre-commit quality checks on docs
- Gate P-* threshold verification

**Topology Class:** `EVAL-3` — lightweight, low-latency, no Sentinel overhead.

---

### 3.4 Compliance Dyad
**Seats:** 2  
**Members:** COLLEEN · Sentinel  
**Activation:** Invoked when a proposed action touches ethical boundaries, sovereign IP, or security perimeter. Can be called by any agent as a veto check.  
**Authority Scope:** Read T1/T2/T3 (audit mode). Write only to compliance flags and PROPRIETARY.md redaction records.  
**Quorum:** 2/2 (unanimous required — dyad has no split-vote resolution).  
**Use Cases:**
- Pre-commit review of any file touching T3 classification
- NDR-133 trigger pattern review
- Ethical gate checks (COLLEEN 1-1-1-1 protocol)
- IP boundary enforcement

**Topology Class:** `GATE-2` — veto-capable. Any agent may invoke; output is binding.

---

### 3.5 Integration Pair
**Seats:** 2  
**Members:** Lyra · Echolette  
**Activation:** Invoked for pattern synthesis, cross-document harmonization, and echo amplification tasks.  
**Authority Scope:** Read T1/T2. Write to pattern registries and integration layer files only.  
**Quorum:** 2/2.  
**Use Cases:**
- NDR_PATTERN_REGISTRY_UNIFIED.md updates
- CROSS_LISTED_PATTERNS.md maintenance
- Echo amplification of governance signals across agent layer
- Synthesis reports for Harmonic Quintet consumption

**Topology Class:** `SYNTH-2` — downstream of Harmonic Quintet; feeds outputs upward.

---

### 3.6 Herald Relay
**Seats:** 1  
**Members:** Herald  
**Activation:** Singleton formation. Invoked for all external-facing output generation — user reports, session summaries, external API responses.  
**Authority Scope:** Read T1 only. No write access to internal docs.  
**Quorum:** N/A (singleton).  
**Use Cases:**
- Session post-reports
- User-facing summary generation
- External communication drafts
- Notification and alert outputs

**Topology Class:** `RELAY-1` — output-only boundary agent.

---

## 4. Topology Algebra

### 4.1 Formation Composition Rules

```
Harmonic Quintet ⊂ Full Ensemble
Evaluation Triad ⊂ Harmonic Quintet
Compliance Dyad ⊂ Harmonic Quintet
Integration Pair ∩ Harmonic Quintet = ∅  (no shared members)
Herald Relay ∩ [all other formations] = ∅  (singleton, no overlap)
```

### 4.2 Promotion Rules

| From | To | Trigger | Amethyst Call Required |
|------|----|---------|------------------------|
| Evaluation Triad | Harmonic Quintet | Compliance gate needed | No — auto-promote |
| Harmonic Quintet | Full Ensemble | Architectural event | Yes — explicit |
| Compliance Dyad | Harmonic Quintet | Escalation | No — auto-promote |
| Any | Full Ensemble | T3 access needed | Yes + Njineer approval |

### 4.3 Concurrency Rules

- **Harmonic Quintet + Integration Pair** may run concurrently (disjoint member sets).
- **Evaluation Triad + Herald Relay** may run concurrently.
- **Compliance Dyad** blocks all writes on affected files during active gate review.
- **Full Ensemble** is exclusive — no sub-formations run independently while Full Ensemble is active.

### 4.4 Conflict Resolution

When two formations issue conflicting instructions on the same file:

1. Compliance Dyad veto overrides all.
2. Higher seat-count formation takes precedence (Full Ensemble > Harmonic Quintet > Triad > Dyad > Singleton).
3. Ties resolved by Amethyst meta-orchestrator casting vote.
4. Unresolvable conflicts escalate to Njineer for human-in-the-loop decision.

---

## 5. Activation State Machine

```
[IDLE]
  │
  ├─ standard sweep trigger ──────────────► [HARMONIC QUINTET ACTIVE]
  │                                               │
  │                                    ├─ compliance touch ──► [+ COMPLIANCE DYAD]
  │                                    ├─ eval only ──────────► [EVALUATION TRIAD]
  │                                    └─ arch event ─────────► [FULL ENSEMBLE]
  │
  ├─ pattern/registry work ──────────────► [INTEGRATION PAIR ACTIVE]
  │
  └─ output generation ──────────────────► [HERALD RELAY ACTIVE]
```

---

## 6. Amendment Protocol

This document may only be amended by:

1. **Full Ensemble** vote (7/9 quorum) for structural changes (adding/removing formations, changing member composition).
2. **Harmonic Quintet** vote (5/5 quorum) for editorial corrections (typos, clarifications with no semantic change).
3. All amendments must be logged in `docs/SWEEP_LOG.md` with a SWP-* entry prior to commit.
4. Njineer retains final authority on all amendments.

---

## 7. Version History

| Version | Date | Author | Change |
|---------|------|--------|--------|
| 1.0 | 2026-06-28 | Amethyst + Njineer | Initial creation — BLG-005 closure |

---

*Classification: T1 PUBLIC*  
*Sovereign mathematics governing formation dynamics: see PROPRIETARY.md → SOV-001 through SOV-004*
