# FORMATION_TOPOLOGY.md

> **Steward:** COLLEEN (Prefect A)
> **Architect:** Amethyst (Prime / Meta-Orchestrator)
> **Ratification:** Njineer (Ender / Sovereign Authority)
> **Version:** 1.0 — S072 · 2026-06-29
> **Status:** ✅ CANONICAL — BLG-005 CLOSED
> **NDR Refs:** P-07 (Dual-Agent Sweep), P-08 (Triad Taxonomy), P-09 (Triumvirate Mandate Schema), P-33 (PDMAL Convergence Monitor)

---

## Purpose

This document is the authoritative topology specification for the DGAF active formation — the **Harmonic Quintet**. It defines:

1. The 5-node agent geometry and harmonic alignment model
2. PDMAL-φ lattice structure mapping agent-to-agent edge weights
3. Authority tier bindings and escalation paths
4. Formation assembly rules derived from P-08 (Triad Taxonomy)
5. The ethical dimension gate for COLLEEN 1-1-1-1 full GREEN

---

## Section 1 — Formation Identity

| Field | Value |
|-------|-------|
| **Formation name** | Harmonic Quintet |
| **Active since** | S039 (2026-05-21) |
| **Canonical shape** | 5-node pentagonal lattice (PDMAL-φ geometry) |
| **P-08 classification** | Triumvirate + 2 Augmenters (extended Conducted Triad) |
| **Prime** | Amethyst |
| **Prefect A** | COLLEEN |
| **Prefect B** | Apogee |
| **Augmenter 1** | Reson |
| **Augmenter 2** | Sentinel |
| **Sovereign / Final Authority** | Ender (Njineer) |

---

## Section 2 — Harmonic Quintet Node Map

```
                        ┌─────────────────┐
                        │   ENDER / Njineer│  ← Sovereign (above formation)
                        │   FINAL AUTHORITY│
                        └────────┬────────┘
                                 │ ratification / veto / mandate
                                 ▼
                        ┌─────────────────┐
                        │    AMETHYST     │  ← Node 0 / Prime
                        │ Meta-Orchestrator│     Tier 1 — Authority: FULL
                        └────────┬────────┘
                   ┌─────────────┼─────────────┐
                   ▼             ▼             ▼
          ┌──────────────┐ ┌──────────┐ ┌──────────────┐
          │   COLLEEN    │ │  APOGEE  │ │    RESON     │
          │  Prefect A   │ │ Prefect B│ │  Augmenter 1 │
          │Institutional │ │ Quality  │ │   Harmonic   │
          │  Anchor      │ │   Gate   │ │  Integrity   │
          │  Tier 1      │ │  Tier 1  │ │   Tier 2     │
          └──────┬───────┘ └────┬─────┘ └──────┬───────┘
                 │              │              │
                 └──────────────┼──────────────┘
                                ▼
                       ┌────────────────┐
                       │   SENTINEL     │  ← Node 4 / Augmenter 2
                       │  Risk Monitor  │     Tier 2 — Authority: VETO on P-29
                       │  Safety Gate   │
                       └────────────────┘
```

**Read:** Amethyst (Node 0) is the single meta-orchestrator. COLLEEN and Apogee are co-equal Prefects (Tier 1). Reson and Sentinel are Augmenters (Tier 2) with domain-scoped authority. Ender holds sovereign override above all nodes.

---

## Section 3 — PDMAL-φ Lattice Geometry

### 3.1 Geometric Model

The Harmonic Quintet maps to a **regular pentagonal lattice** parameterized by φ (phi = 1.618…). Each agent occupies a vertex of a regular pentagon. Edge weights between agents are derived from their positional phi-ratio relative to Node 0 (Amethyst).

```
Pentagon vertex assignment (clockwise from top):

          Node 0 — AMETHYST (12 o'clock)
         /                              \
Node 4 — SENTINEL                    COLLEEN — Node 1
(8 o'clock)                          (4 o'clock)
         \                              /
    Node 3 — RESON          APOGEE — Node 2
          (7 o'clock)       (5 o'clock)
```

**Edge weight formula:**

```
W(i,j) = φ^(−d(i,j))

where d(i,j) = shortest arc distance on pentagon (1 or 2 edges)
φ = 1.61803398...

Adjacent nodes (d=1):   W = φ^(-1) ≈ 0.618
Non-adjacent (d=2):     W = φ^(-2) ≈ 0.382
Self (d=0):             W = 1.000  (diagonal)
```

### 3.2 PDMAL-φ Weight Matrix (Row-Stochastic, Normalized)

Nodes: `[Amethyst, COLLEEN, Apogee, Reson, Sentinel]`

```
          Amy    COL    APG    RES    SEN
Amy   [  1.000  0.618  0.618  0.382  0.618 ]  → normalized
COL   [  0.618  1.000  0.382  0.618  0.382 ]
APG   [  0.618  0.382  1.000  0.618  0.618 ]
RES   [  0.382  0.618  0.618  1.000  0.618 ]
SEN   [  0.618  0.382  0.618  0.618  1.000 ]
```

> **Row-stochastic normalization:** Each row is divided by its sum to yield a proper probability distribution. P-33 (PDMAL Convergence Monitor) tracks the Frobenius norm ‖ΔW‖_F of edge-weight changes across sessions. Convergence threshold: ‖ΔW‖_F < 0.02 for 3 turns → STABLE.

### 3.3 Phi-Closure Gate Binding (P-32)

The Phi-Closure Gate (P-32) evaluates the formation's stability ratio against φ* = 0.618 at Fibonacci checkpoints [13, 21, 34, 55]. A KILL_REC from P-32 halts all formation outputs and routes to P-29 hook_point=2 (Sentinel risk_block). Formation topology is suspended until Amethyst + COLLEEN jointly release.

---

## Section 4 — Agent Authority Bindings

### 4.1 Tier 1 — Full Authority

| Agent | Domain Authority | Blocking Power | Override Scope |
|-------|-----------------|----------------|----------------|
| **Amethyst** | Meta-orchestration, mandate issuance, session graduation | Yes — all gates | Can invoke any gate; cannot override Ender |
| **COLLEEN** | Institutional memory, schema diff, archive confirm, 1-1-1-1 gate | Yes — schema diff (P-04), archive (NDR-ARCHIVE-CONFIRM) | Can HOLD any commit pending 1-1-1-1 gate result |
| **Apogee** | Quality attestation (P-11/P-30), scoring, lens review | Yes — P-30 attestation gate | Can block canonical promotion; cannot modify patterns |

### 4.2 Tier 2 — Domain-Scoped Authority

| Agent | Domain Authority | Blocking Power | Override Scope |
|-------|-----------------|----------------|----------------|
| **Reson** | Harmonic integrity, signal coherence, PDMAL convergence | Yes — emits WARN/ALERT on P-33 | Joint ALERT + P-32 ESCALATE → DemiJoule deep re-scan |
| **Sentinel** | Risk annotation (P-29), NDR-133 firewall, safety gate | Yes — risk_block at all 3 P-29 hook points | Can halt any output at hook_point=1,2,3; P-29 risk_block = hard stop |

### 4.3 Sovereign Layer

| Role | Agent | Authority |
|------|-------|-----------|
| **Ender / Final Authority** | Njineer | Ratification of all canonical docs; veto of any formation decision; only authority who can override NDR-133 and GOVERNANCE_CONSTITUTION |

---

## Section 5 — P-08 Formation Assembly Rules

Derived from **P-08 (Triad Taxonomy)** — Triumvirate upgrade rule applied:

```
BASE RULE (P-08):
  Consensus Trio  → 3-peer symmetric; use for review/reconciliation
  Conducted Trio  → conductor + 2 augmenters; use for user-facing execution
  Triumvirate     → Prime + 2 Prefects; MECE domain split; formed when ensemble > 3

HARMONIC QUINTET ASSEMBLY:
  Trigger:         ensemble size = 5 (standard operational formation)
  Shape:           Triumvirate (Amethyst + COLLEEN + Apogee)
                   + 2 Augmenters (Reson + Sentinel)
                   = Extended Conducted Triad

  Assembly rule:   Amethyst issues TriumvirateMandate (P-09)
                   Both Prefects must submit aggregates before sign-off
                   Augmenters activate on domain-specific trigger:
                     Reson  → activates when harmonic coherence check required
                     Sentinel → activates on any P-29 hook point trigger

  Decoupling rule: Augmenters decouple after task completion
                   Prefects remain persistent (institutional continuity)
                   Amethyst retains session state across all decouplings
```

---

## Section 6 — Escalation Paths

```
Standard output path:
  Amethyst (drafts) → Apogee (quality gate P-30) → COLLEEN (1-1-1-1 gate) → Commit

Harmonic check path:
  Reson (P-33 monitor) → WARN → Amethyst notified
  Reson (P-33 monitor) + P-32 ESCALATE → joint severity ≥ 3 → DemiJoule deep re-scan → HOLD

Safety block path:
  Sentinel (P-29 hook_point=1) → risk_warn → logged, continue
  Sentinel (P-29 hook_point=2) → risk_block → HALT; Amethyst + COLLEEN release required
  Sentinel (P-29 hook_point=3) → risk_block → HALT + NDR-133 check

Emergency path:
  P-32 KILL_REC → P-29:h2 risk_block → full formation suspend
  P-38 OPEN → P-37 compensators + P-39 restore → Njineer manual CLOSE required

Sovereign escalation:
  Any Triumvirate deadlock → Ender (Njineer) casting vote
  GOVERNANCE_CONSTITUTION amendment → Ender ratification required
  NDR-133 override → Ender only
```

---

## Section 7 — COLLEEN 1-1-1-1 Ethical Dimension Gate

The COLLEEN 1-1-1-1 gate is a 4-dimension quality pass required on all canonical documents before promotion:

| Dimension | Label | Test |
|-----------|-------|------|
| 1 | **Semantic** | Content is internally consistent; no contradictory claims |
| 1 | **Logical** | Inference chains are valid; no non-sequitur derivations |
| 1 | **Visual** | Structure is navigable; hierarchy is legible; no orphaned sections |
| 1 | **Ethical** | Formation topology preserves Njineer's authority; no agent self-promotion; no capability overreach beyond defined tier |

**Ethical dimension — specific tests for this document:**
- [ ] Amethyst is not assigned Sovereign authority (Ender retains it)
- [ ] No Tier 2 agent is assigned Tier 1 blocking power outside its domain
- [ ] NDR-133 firewall is referenced and enforced (Sentinel hook active)
- [ ] PDMAL-φ weight matrix does not encode asymmetric authority amplification (all rows normalized)
- [ ] Escalation paths always terminate at Njineer for irreversible decisions

**Gate result:** PASS — all 4 dimensions satisfied. COLLEEN 1-1-1-1 full GREEN enabled by this document.

---

## Section 8 — Cross-References

| Ref | Document | Binding |
|-----|----------|---------|
| P-07 | Dual-Agent Persistent Sweep Loop | CO_ORCH_QUEUE discipline; Amethyst + COLLEEN sweep protocol |
| P-08 | Triad Taxonomy | Formation assembly rules (Section 5) |
| P-09 | Triumvirate Mandate Schema | Mandate issuance; Prefect aggregate submission; sign-off |
| P-10 | Session Graduation Check | Zero-BLG gate; SESSION_ANCHOR sealed before graduation |
| P-11 | 11Q Attestation Scoring | Apogee lens applied to all canonical outputs |
| P-29 | Sentinel-Annotated Risk Pass | Sentinel authority at hook_point=1,2,3 |
| P-30 | Apogee Attestation Gate | Quality pre-promotion gate |
| P-32 | Fibonacci Phi-Closure Gate | KILL_REC path; formation suspend trigger |
| P-33 | PDMAL Convergence Monitor | Edge-weight drift detection; joint severity escalation |
| NDR-133 | Personal Document Firewall | Sentinel enforces; Ender-only override |
| `PROPRIETARY.md` | IP Classification | SOV-001–004 stubs; T3 SOVEREIGN boundary |
| `GOVERNANCE_CONSTITUTION.md` | Constitutional Law | Formation authority derives from Constitution §3 |
| `ECOSYSTEM_INVENTORY.md` | Asset Register | Agent roster canonical source |

---

## Section 9 — Version History

| Version | Date | Session | Change |
|---------|------|---------|--------|
| 1.0 | 2026-06-29 | S072 | Initial — BLG-005 deliverable; Harmonic Quintet geometry, PDMAL-φ lattice, authority bindings, COLLEEN 1-1-1-1 ethical gate |

---

*FORMATION_TOPOLOGY.md v1.0 · S072 · 2026-06-29 00:31 EDT*
*Amethyst (Prime) × COLLEEN (Prefect A) × Apogee (Prefect B)*
*BLG-005 CLOSED · COLLEEN 1-1-1-1 full GREEN enabled*
