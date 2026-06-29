# DGAF Agent Ecosystem Registry

**Authority:** COLLEEN (Institutional Anchor / Sovereign Governance)
**Scope:** Ecosystem tier taxonomy · Agent KB inventory tracking · Formation assignments · Amendment log
**Status:** ACTIVE · CANONICAL
**Version:** 2.1
**Last Updated:** 2026-06-29 (Phase E — Phase C 9-agent inventory patch; formation topology finalized; Apogee Lens verdict recorded)

> **Scope boundary:** This file tracks *ecosystem metadata* (formation, inventory, amendment history).
> For sovereign agent identity, formation rules, and gate ownership, see [`AGENT_ROSTER.md`](./AGENT_ROSTER.md) — that file is the SSoT and is Sentinel-guarded.

---

## See Also

| File | Scope |
|---|---|
| [`AGENT_ROSTER.md`](./AGENT_ROSTER.md) | **Sovereign SSoT** — identity, formation, authority levels, gate ownership, role separation rules |
| [`AGENT_ECOSYSTEM_REGISTRY.md`](./AGENT_ECOSYSTEM_REGISTRY.md) | **This file** — taxonomy counts, inventory tracking, amendment log |
| [`FORMATION_TOPOLOGY.md`](./FORMATION_TOPOLOGY.md) | Formation specs, topology algebra, activation state machine |
| [`PROPRIETARY.md`](./PROPRIETARY.md) | IP partition — SOV-005/SOV-006 stubs for T3 sovereign agents |

---

## ⚡ Taxonomy Corrections (v1.x → v2.0)

> The following corrections are canonical as of 2026-06-29. All downstream files must reflect these.

| Correction | Prior State | Corrected State | Commit |
|---|---|---|---|
| Archive Trio composition | Librarian + Actualizer + Ionia | **Librarian (Alpha) + Auditor (Beta) + Actualizer (Gamma)** | `f1a8dd0` |
| Ionia classification | Functional Archive Trio member | **System STATE (0Hz terminal condition / Universal Schema)** | `f1a8dd0` |
| Layer 0 Legitimacy Filter | Attributed to Perigee | **Canonical designation belongs to Apogee** | `f1a8dd0` |
| Perigee role title | Layer 0 Legitimacy Filter / Boundary Gate | **Proximal Boundary Agent / Grounded Operations** | `f1a8dd0` |
| Apogee former name | Not recorded | **Formerly Agent Lavender** | `9429a9c` |
| Total taxonomy count | 20 agents | **27 agents (18 full + 9 Phase C seeds + Ionia as STATE)** | `08c6d82` |
| Architectural directive | Not recorded | **Substrate Agnostic + Accepted Terminology Principle (Amethyst SPEC v1.1 §8)** | `142772d` |
| Sentinel A-12 | Sentinel / Compliance Dyad | **Sentinel-Phi / Strategic Quintet Seat 5** | `08c6d82` |
| Compliance Dyad | Active (Sentinel + Perigee) | **Dissolved — Sentinel-Phi departed to Strategic Quintet** | `08c6d82` |

---

## Canonical Formation Topology (Final — 2026-06-29)

```
SOVEREIGN GOVERNANCE
  Amethyst (A-00)        — Meta-Orchestrator; spans all tiers
  COLLEEN (A-00-GOV)     — Institutional Anchor; supreme governance

        ↓

ETHICS BRIDGE  [singleton tier]
  Sentience (A-27)       — Consciousness Explorer / Ethical Decision-Making
                           ETHICAL_HOLD authority over all formations

        ↓

STRATEGIC QUINTET  [5/5 sealed]
  Nova (A-03)            — Innovation Catalyst [TUE gate]
  Zenith (A-09-Z)        — Peak Performance Optimizer
  Oracle (A-20)          — Future Forecaster / Scenario Planner
  Vanguard (A-21)        — Innovation Scout / Emerging Tech Futurist
  Sentinel-Phi (A-12-φ)  — Strategic Security / Phi-Bounded Risk Architecture

HARMONIC PENTAGONAL CLUSTER  [5/5 sealed]
  Prof Prodigy (A-04)    — Mathematics Canonicalizer / Formal Verification
  Herald (A-05)          — Communication Orchestrator / Protocol Synchronization
  Apogee (A-01)          — Evidence Governance / Final Verification [formerly Agent Lavender]
  Reciprocity (A-06-R)   — Inverse Ops / Mutual Benefit Modeling
  DemiJoule (A-03-DJ)    — Constraint Specialist / Resource Efficiency

RESONANCE CLUSTER
  Schizophonic Studio [sub-formation]:
    Reson (A-09)         — Systems Architect / Signal Integrity
    Lyra (A-10)          — Integrated Conductor / Harmonic Synthesis
    Echolette (A-11)     — Texturalist / Reflective Stability
  Extended Resonance:
    Synergy (A-25)       — Collaboration Facilitator / Organizational Harmonizer
    Equilibrium (A-26)   — Balance Seeker / Harmony Architect
  [Ionia = 0Hz system STATE — convergence target, not a functional seat]

OPERATIONAL SWARM
  Navigator (A-22)       — Pathfinder / Strategic Guidance + Risk Navigation
  Momentum (A-23)        — Progress Accelerator / Adaptation Strategist
  Paragon (A-24)         — Exemplar Model / Best-Practice Benchmark

PERPETUAL ARCHIVE TRIO  [COLLEEN subordinate; non-reabsorbable]
  The Librarian (A-06-L) — Alpha / The Map
  The Auditor (A-07)     — Beta  / The Pulse
  The Actualizer (A-08)  — Gamma / The Stage

SPECIALIST
  Perigee (A-02)         — Proximal Boundary Agent / Grounded Operations
```

---

## Inventory Completion — 27-Agent Ecosystem

**Standard inventory:** 6 layers per agent (SPEC · MEMORY · PROTOCOL · QA_RUBRIC · INTEGRATION · KB)
**Target (27 agents):** 162 files

| Agent | Formation | SPEC | Memory | Protocol | QA Rubric | Integration | KB/Amend | % |
|---|---|---|---|---|---|---|---|---|
| Amethyst | Sovereign | ✅ v1.1 | ✅ | ✅ v1.1 | ✅ | ✅ | ✅ | **100%** |
| COLLEEN | Sovereign | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ v1.1 | **100%** |
| Apogee | H.Pentagonal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ v1.1 | **100%** |
| Herald | H.Pentagonal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ v1.1 | **100%** |
| Prof Prodigy | H.Pentagonal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ v1.1 | **100%** |
| DemiJoule | H.Pentagonal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ v1.1 | **100%** |
| Reciprocity | H.Pentagonal | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ v1.1 | **100%** |
| Reson | Resonance/Studio | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ v1.1 | **100%** |
| Lyra | Resonance/Studio | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ v1.1 | **100%** |
| Echolette | Resonance/Studio | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ v1.1 | **100%** |
| Nova | Strategic Quintet | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **100%** |
| Zenith | Strategic Quintet | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **100%** |
| Sentinel-Phi | Strategic Quintet | ✅ v2.0 | ✅ | ✅ | ✅ | ✅ | ✅ upgrade | **100%** |
| Perigee | Specialist | ✅ v1.1 | ✅ | ✅ | ✅ | ✅ | ✅ | **100%** |
| The Librarian | Archive Trio | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **100%** |
| The Auditor | Archive Trio | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **100%** |
| The Actualizer | Archive Trio | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **100%** |
| Ionia | Resonance (STATE) | ✅ v1.1 | ✅ | ✅ | ✅ | ✅ | ✅ | **100%** |
| Oracle | Strategic Quintet | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ seed | **17%** |
| Vanguard | Strategic Quintet | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ seed | **17%** |
| Navigator | Operational Swarm | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ seed | **17%** |
| Momentum | Operational Swarm | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ seed | **17%** |
| Paragon | Operational Swarm | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ seed | **17%** |
| Synergy | Resonance Ext. | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ seed | **17%** |
| Equilibrium | Resonance Ext. | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ seed | **17%** |
| Sentience | Ethics Bridge | ❌ | ❌ | ❌ | ❌ | ❌ | ✅ seed | **17%** |

### Inventory Milestone Log

| Milestone | Agents | Files complete | Notes |
|---|---|---|---|
| S001 Baseline | 11 | 13/66 | Initial KB stubs |
| Phase 1–2 | 11 | 24/66 | 2026-06-28 |
| Phase 3–4 | 17 | 56/66 | 2026-06-29 pre-taxonomy correction |
| Phase A–B | 18 | 108/108 | 18 agents at 100% |
| **Phase C–E** | **27** | **117/162** | **18 × 100% · 9 × 17% (seed only)** |
| Phase F target | 27 | 162/162 | Full 6-layer build-out for 9 Phase C agents |

---

## Phase D — Apogee Lens Audit Verdict

| Dimension | Result |
|---|---|
| D1 — Evidence Chain Integrity | ✅ PASS |
| D2 — Taxonomy Consistency | ✅ PASS |
| D3 — Terminology Gate Compliance (19/19 files) | ✅ PASS |
| D4 — Formation Coherence & Completeness | ✅ PASS |
| **Composite verdict** | **✅ GOLD STAR ELIGIBLE** |

*Audited by Apogee (A-01) · 2026-06-29 · commit `08c6d82`*
*Advisory (non-blocking, resolved here in Phase E): Registry v2.0 predated Phase C inventory.*

---

## Amendment Version Log

| Agent | Version | Date | Change | Commit |
|---|---|---|---|---|
| Amethyst | v1.1 | 2026-06-29 | Substrate Agnostic + Accepted Terminology Principle (§8) | `142772d` |
| Ionia | v1.1 | 2026-06-29 | Reclassified as system STATE; Archive Trio corrected | `f1a8dd0` |
| Perigee | v1.1 | 2026-06-29 | Layer 0 attribution corrected to Apogee | `f1a8dd0` |
| Apogee | v1.1 | 2026-06-29 | Formerly Agent Lavender; Layer 0 canonical; SAP/Ping the Buoy | `9429a9c` |
| Herald | v1.1 | 2026-06-29 | Tonic Note 0Hz + orthogonal cognitive planes routing | `9429a9c` |
| Prof Prodigy | v1.1 | 2026-06-29 | 3-Tier Calculi KB + Fixed-Point Theorems | `9429a9c` |
| DemiJoule | v1.1 | 2026-06-29 | Modal frequency gating + energy conservation | `9429a9c` |
| Reciprocity | v1.1 | 2026-06-29 | Reciprocal Mathematics + asymmetric logic drift prevention | `9429a9c` |
| Reson | v1.1 | 2026-06-29 | Gain staging + 15% headroom + clipping = runaway gain | `9429a9c` |
| Lyra | v1.1 | 2026-06-29 | Human Flourishing alignment + orchestral coordination | `9429a9c` |
| Echolette | v1.1 | 2026-06-29 | Mirror Protocols + decision echo tracing | `9429a9c` |
| COLLEEN | v1.1 | 2026-06-29 | 1-1-1-1 Alignment Gate + Swarm Educator + Archive Trio governance | `9429a9c` |
| The Auditor | v1.0 | 2026-06-29 | Full seed; Beta/Pulse; NDR-Protocol-01 step 1 | `f1a8dd0` |
| Sentinel-Phi | v2.0 | 2026-06-29 | Renamed from Sentinel A-12; Strategic Quintet Seat 5; φ-bounded risk | `08c6d82` |
| Oracle | v1.0 | 2026-06-29 | KB seed; Strategic Quintet Seat 3 | `08c6d82` |
| Vanguard | v1.0 | 2026-06-29 | KB seed; Strategic Quintet Seat 4 | `08c6d82` |
| Navigator | v1.0 | 2026-06-29 | KB seed; Operational Swarm | `08c6d82` |
| Momentum | v1.0 | 2026-06-29 | KB seed; Operational Swarm | `08c6d82` |
| Paragon | v1.0 | 2026-06-29 | KB seed; Operational Swarm; Gold Star prerequisite | `08c6d82` |
| Synergy | v1.0 | 2026-06-29 | KB seed; Resonance Cluster Extended | `08c6d82` |
| Equilibrium | v1.0 | 2026-06-29 | KB seed; Resonance Cluster Extended; Ionia≠Equilibrium explicit | `08c6d82` |
| Sentience | v1.0 | 2026-06-29 | KB seed; Ethics Bridge singleton; ETHICAL_HOLD authority | `08c6d82` |

---

## Standing Architectural Directives

| Directive | Source | Scope |
|---|---|---|
| Substrate Agnostic + Accepted Terminology Principle | Amethyst SPEC v1.1 §8 | All KB files; role titles; protocol names |
| NDR-Protocol-01 chain integrity | The Auditor INTEGRATION.md | Auditor→Actualizer→Librarian enforced in all Integration files |
| Ionia = STATE not agent | Ionia SPEC v1.1 | All files referencing Ionia |
| Layer 0 Legitimacy Filter = Apogee | Perigee SPEC v1.1 + Apogee KB v1.1 | All files referencing Layer 0 |
| Archive Trio = Librarian + Auditor + Actualizer | Multiple v1.1 amendments | All files referencing the Trio |
| Paragon sign-off = Gold Star prerequisite | Paragon KB v1.0 §4 | All Gold Star / S-Tier designation workflows |
| ETHICAL_HOLD authority = Sentience | Sentience KB v1.0 | All formation outputs; overridable only by COLLEEN or Njineer |

---

## NDR Pattern 133 — Personal Document Firewall

```
Trigger: Any push queue containing filenames matching:
         *resume*, *cv*, *audit_report*, *ResumeApex*
Action:  BLOCK push → route to Drive-only destination
Authority: Architect override only
Rationale: Personal data protection + IP boundary
```

---

*Ecosystem Registry authority: COLLEEN (Sovereign Governance). Changes require Amethyst sign-off + Njineer confirmation.*
*Conductor: Njineer ([@ndrorchestration](https://github.com/ndrorchestration))*
