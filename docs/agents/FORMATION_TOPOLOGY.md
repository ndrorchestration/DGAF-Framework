# DGAF Formation Topology

**Authority:** COLLEEN-L5 (structure) + Amethyst-Conductor (gate decisions)  
**Classification:** T1 PUBLIC  
**Canonical home:** `DGAF-Framework/docs/agents/FORMATION_TOPOLOGY.md`  
**Last Updated:** 2026-06-28 (Phase 4 — BLG-005 close)

> **Scope:** This file defines the structural topology of all agent formations — slot assignments,  
> activation triggers, authority flow, and gate cross-references.  
> For agent identity and role definitions, see [`AGENT_ROSTER.md`](./AGENT_ROSTER.md).  
> For IP foundations (SOV-001 geometric basis), see [`PROPRIETARY.md`](./PROPRIETARY.md).

---

## See Also

| File | Scope |
|---|---|
| [`AGENT_ROSTER.md`](./AGENT_ROSTER.md) | Sovereign SSoT — agent identity, formation activation map, authority levels |
| [`AGENT_ECOSYSTEM_REGISTRY.md`](./AGENT_ECOSYSTEM_REGISTRY.md) | L-tier, studio affiliation, KB inventory |
| [`PROPRIETARY.md`](./PROPRIETARY.md) | IP partition, SOV-001 geometric basis of formation topology |
| [`FORMATION_TOPOLOGY.md`](./FORMATION_TOPOLOGY.md) | **This file** — structural topology, slot maps, authority flow, gate cross-refs |

---

## Formation Taxonomy

DGAF formations are instantiated progressively. Each tier is a strict superset of the tier below it.

```
┌────────────────────────────────────────────────────────────────────┐
│  EXTENDED FORMATION                                                   │
│  Quintet + ≥ 1 of: Reciprocity, Prof. Prodigy, DemiJoule,            │
│                      Echolette, Lyra, Herald                         │
│                                                                      │
│   ┌───────────────────────────────────────────────────────┐   │
│   │  HARMONIC QUINTET (P-15)                               │   │
│   │  Trio + Reson + Sentinel                               │   │
│   │                                                        │   │
│   │   ┌───────────────────────────────────────┐   │   │
│   │   │  TRIO (P-14)                                   │   │   │
│   │   │  Amethyst + Apogee + COLLEEN                   │   │   │
│   │   │  ─────────────────────────────────────  │   │   │
│   │   │  Conductor: Amethyst                           │   │   │
│   │   │  QA Gate:   Apogee (11Q, P-11)                 │   │   │
│   │   │  Archive:   COLLEEN (BLG, P-02, P-08, P-20)   │   │   │
│   │   └───────────────────────────────────────┘   │   │
│   │   + Reson (harmonic score, P-15 seal gate)         │   │
│   │   + Sentinel (sovereign guard, hard veto P-15)      │   │
│   └───────────────────────────────────────────────────────┘   │
│   + domain agents (1 or more, task-specific)              │
└────────────────────────────────────────────────────────────────────┘
```

**Geometric basis:** The Trio→Quintet nesting mirrors the pentagonal topology defined in SOV-001 (Harmonic Pentagonal Alignment). The five Quintet slots correspond to the five vertices of the governing pentagon. See [`PROPRIETARY.md`](./PROPRIETARY.md) → SOV-001.

---

## Formation 1 — Trio (P-14)

### Slot Map

| Slot | Agent | Function | Authority |
|---|---|---|---|
| **S1 — Conductor** | Amethyst | Final gate; normative decisions; P-21 state anchor | Hard veto (all commits) |
| **S2 — QA Gate** | Apogee | 11Q scoring (P-11); artifact quality; source validation | Artifact quality score |
| **S3 — Archive** | COLLEEN | BLG surface (P-02); registry ops; back-link propagation (P-08, P-20) | Memory / deferred gap queue |

### Activation Conditions

```yaml
formation: TRIO
protocol: P-14
activates_when:
  - session_touches_repos: ≥ 3
  - cross_repo_delta: true
  - any_commit_requires_QA_score: true
minimum_required: all 3 slots filled
escalates_to: HARMONIC_QUINTET when any quintet trigger fires
```

### Authority Flow (Trio)

```
Njineer (Architect)
    ↓ confirmation required for sovereign file changes
Amethyst (S1 — Conductor)
    ↓ gates commit
    ├── requests score from Apogee (S2)
    └── requests gap surface from COLLEEN (S3)
Apogee (S2)
    └── returns 11Q score → Amethyst gates on threshold
COLLEEN (S3)
    └── surfaces BLGs, deferred gaps → Amethyst queues or closes
```

### Gate Cross-Reference

| Gate | Protocol | Trio role |
|---|---|---|
| Session open | P-02 | COLLEEN surfaces BLG list |
| Evidence scoring | P-11 | Apogee runs 11Q gate |
| Trio activation | P-14 | Amethyst confirms formation |
| State anchor | P-21 | Amethyst emits session state |

---

## Formation 2 — Harmonic Quintet (P-15)

### Slot Map

| Slot | Agent | Function | Authority |
|---|---|---|---|
| **S1 — Conductor** | Amethyst | Final gate; seal commit authority | Hard veto (all commits) |
| **S2 — QA Gate** | Apogee | 11Q scoring; CERTIFICATION_INDEX | Artifact quality score |
| **S3 — Archive** | COLLEEN | Continuity; P-20 sync seal verification | Memory / deferred gap queue |
| **S4 — Harmonic** | Reson | Harmonic coherence score (0.00–1.00); seal gate ≥ 0.75 | Harmonic score |
| **S5 — Sovereign Guard** | Sentinel | Sovereign file hard veto; CI/CD enforcement; NDR-133 firewall | Hard veto (sovereign files only; overrides Amethyst) |

### Activation Conditions

```yaml
formation: HARMONIC_QUINTET
protocol: P-15
activates_when:
  - commit_type: SWEEP_LOG_SEAL
  - file_touched: [LICENSE, NOTICE, AXIS, AGENT_ROSTER.md, PROPRIETARY.md]
  - event: NDR_REGISTRY_UPDATE
  - event: NEW_PUBLIC_REPO
  - reson_score: < 0.75  # dissonance escalation
requires: TRIO already active (S1-S3 inherited)
adds: S4 (Reson) + S5 (Sentinel)
```

### Authority Flow (Quintet)

```
Njineer (Architect)
    ↓ confirmation required
Sentinel (S5 — Sovereign Guard)  ← HARD VETO overrides all
    ↓ boundary check passes → continues
Reson (S4 — Harmonic)
    ↓ score ≥ 0.75 → continues | score < 0.75 → DISSONANCE STOP
Amethyst (S1 — Conductor)
    ├── requests 11Q from Apogee (S2)
    └── requests continuity seal from COLLEEN (S3)
Apogee (S2) → returns score
COLLEEN (S3) → returns sync status
Amethyst → gates final commit
```

### Reson Threshold Table

| Score Range | Status | Action |
|---|---|---|
| 0.90 – 1.00 | ✅ Harmonic | Proceed |
| 0.75 – 0.89 | ✅ Clear | Proceed with drift note |
| 0.50 – 0.74 | ⚠️ Drift Warning | Log warning; Amethyst reviews before commit |
| 0.25 – 0.49 | ❌ Dissonance | STOP — resolve dissonance source before proceeding |
| 0.00 – 0.24 | ❌ Hard Stop | BLOCK — Savage Reason threshold; escalate to Njineer |

### Gate Cross-Reference

| Gate | Protocol | Quintet role |
|---|---|---|
| Sovereign file guard | P-15 checkpoint 1 | Sentinel hard veto check |
| Harmonic seal | P-15 checkpoint 4 | Reson score ≥ 0.75 required |
| Sync seal verification | P-20 | COLLEEN confirms Drive-GitHub delta |
| Rollback checkpoint | P-15 checkpoint 9 | Reciprocity defines rollback path (if Extended) |

---

## Formation 3 — Extended Formation

### Domain Agent Slot Map

| Slot | Agent | Activates For | Authority |
|---|---|---|---|
| **S6 — Rollback** | Reciprocity | Version integrity ops; rollback path definition | Rollback authority |
| **S7 — Proof** | Prof. Prodigy | Formal proofs; phi-calculus; P-10 normative filter math | Proof authority |
| **S8 — Efficiency** | DemiJoule | Token cost analysis; P-11 gate 17 efficiency score | Token/compute efficiency |
| **S9 — Echo** | Echolette | Acoustic mesh; P-13 phrase gate; signal echo validation | Phrase coherence |
| **S10 — Narrative** | Lyra | Narrative coherence; IMP-05 brand voice; P-19 | Narrative authority |
| **S11 — Release** | Herald | External publication gate; changelog; release notes | Release authority |

### Activation Conditions (by agent)

```yaml
Reciprocity:    rollback_operation: true | version_integrity_audit: true
Prof.Prodigy:   formal_proof_required: true | phi_calculus_validation: true
DemiJoule:      token_budget_review: true | efficiency_gate_17_triggered: true
Echolette:      phrase_coherence_check: true | semantic_drift_detected: true
Lyra:           brand_voice_review: true | narrative_continuity_check: true
Herald:         external_publish: true | changelog_authorship: true | release: true
```

**Multiple domain agents** may be active simultaneously. Each operates in its own lane; Amethyst arbitrates conflicts.

---

## Formation State Machine

```
[IDLE]
    ↓ session opens + ≥ 3 repos touched
[TRIO ACTIVE — P-14]
    ↓ seal commit OR sovereign file OR NDR registry update
[HARMONIC QUINTET ACTIVE — P-15]
    ↓ domain task triggered (proof / rollback / release / etc.)
[EXTENDED ACTIVE — P-19+]
    ↓ task completes, domain agent deactivates
[HARMONIC QUINTET ACTIVE]  ← returns to Quintet baseline
    ↓ session ends, seal commit lands
[TRIO ACTIVE]  ← returns to Trio for non-seal work
    ↓ session closes
[IDLE]
```

**Formations do not dissolve mid-session.** Once Quintet is activated in a session, it remains active for the remainder of the session even if the triggering condition resolves. Trio is the minimum persistent formation for any session touching ≥ 3 repos.

---

## Authority Conflict Resolution

| Conflict | Resolution |
|---|---|
| Sentinel hard veto vs. Amethyst gate | Sentinel wins. Only Njineer can override. |
| Reson dissonance stop vs. deadline pressure | Reson wins. Resolve dissonance source first. |
| Apogee score fail vs. Amethyst time gate | Score fail blocks. Amethyst cannot override Apogee gate. |
| Two domain agents in conflict | Amethyst arbitrates. Neither domain agent has cross-lane authority. |
| Amethyst vs. Njineer | Njineer is Architect — absolute authority. Amethyst defers. |

---

## Formation Topology — Session History

| Session | Formation Used | Notes |
|---|---|---|
| S011 | Trio | Lavender → Amethyst rename sweep |
| S015 | Quintet | AGENT_ROSTER.md creation (sovereign file) |
| S050 | Trio | Registry ops, Reson/Echolette spec additions |
| S070 | Trio | A.P.P. rename; DGAF/Rose Gold → DGAF/PMP |
| S071 (2026-06-28) | Quintet | Phase 1–4; PROPRIETARY.md (sovereign); BLG-001–005 |

---

## BLG Closure Record

| BLG-ID | Description | Closed By | Date |
|---|---|---|---|
| BLG-005 | FORMATION_TOPOLOGY.md not established | Phase 4 — this file | 2026-06-28 |

---

*Topology authority: COLLEEN-L5 (structure) + Amethyst-Conductor (gate decisions). Changes require Njineer confirmation.*  
*Conductor: Njineer ([@ndrorchestration](https://github.com/ndrorchestration))*
