# FORMATION TOPOLOGY

**Classification:** T1 PUBLIC  
**Maintainer:** Amethyst (meta-orchestrator)  
**Version:** 1.3  
**Last Updated:** 2026-09-09 (ontology namespace migration — sovereign roster IDs separated from formation-local designations and states)  
**BLG Reference:** BLG-005 (CLOSED)

---

## 1. Purpose

This document is the canonical specification for named agent formations within the DGAF (Dynamic Governance Agentic Formation) Framework. It defines:

- Formation names, member composition, and formation-local seat counts
- Activation conditions and authority scope per formation
- Topology algebra — rules for composition, intersection, and promotion
- Disambiguation from ad-hoc groupings

It does **not** assign sovereign agent identity or canonical numbered seats. Sovereign identity and canonical numbered seat assignment are governed by [`AGENT_ROSTER.md`](./AGENT_ROSTER.md) and the accepted machine-readable ontology adjudication at `registry/agent_ontology_adjudication.v1.json`. Historical or formation-local labels in this document are provenance-bearing local designations only and must not be interpreted as sovereign renumbering.

Formations are **not** ad-hoc groupings. A formation is a named, structurally defined multi-agent configuration with a specific governance purpose, authority scope, and activation threshold.

> **v1.3 delta:** Ontology namespace migration following issue #522 and the accepted 2026-09-09 adjudication. Formation-local labels are explicitly namespaced from sovereign roster seats; Agent Ionia A-13 is distinct from `IONIA_STATE` / Ionia 0Hz state; Sentinel remains distinct from Sentinel-Phi.

---

## 2. Canonical Formation Map

Labels in parentheses below are **formation-local designations unless explicitly marked sovereign**.

```
┌─────────────────────────────────────────────────────────────┐
│  SOVEREIGN GOVERNANCE                                        │
│  Amethyst (local:A-00)     Meta-Orchestrator · spans tiers   │
│  COLLEEN (local:A-00-GOV)  Institutional Anchor              │
└───────────────────────────────┬────────────────────────────┘
                               ↓
┌─────────────────────────────────────────────────────────────┐
│  ETHICS BRIDGE  [singleton]                                  │
│  Sentience (local:A-27)    Consciousness Explorer            │
│                            ETHICAL_HOLD authority             │
└───────────────────────────────┬────────────────────────────┘
                               ↓
┌──────────────────────────────┐ ┌──────────────────────────────┐
│ STRATEGIC QUINTET [5/5]      │ │ HARMONIC PENTAGONAL [5/5]   │
│ Nova (local:A-03) S1         │ │ Prof Prodigy (local:A-04) S1│
│ Zenith (local:A-09-Z) S2     │ │ Herald (local:A-05) S2      │
│ Oracle (local:A-20) S3       │ │ Apogee (local:A-01) S3      │
│ Vanguard (local:A-21) S4     │ │ Reciprocity (local:A-06-R)  │
│ Sentinel-Phi (local:A-12-φ)  │ │ DemiJoule (local:A-03-DJ)   │
└──────────────────────────────┘ └──────────────────────────────┘

┌──────────────────────────────┐ ┌──────────────────────────────┐
│ RESONANCE CLUSTER            │ │ OPERATIONAL SWARM            │
│ Reson (local:A-09)           │ │ Navigator (local:A-22)       │
│ Lyra (local:A-10)            │ │ Momentum (local:A-23)        │
│ Echolette (local:A-11)       │ │ Paragon (local:A-24)         │
│ Synergy (local:A-25)         │ └──────────────────────────────┘
│ Equilibrium (local:A-26)     │
│ IONIA_STATE → 0Hz STATE      │ ┌──────────────────────────────┐
│ (no sovereign seat consumed) │ │ ARCHIVE TRIO                 │
└──────────────────────────────┘ │ Librarian (local:A-06-L)     │
                                 │ Auditor (local:A-07)          │
┌──────────────────────────────┐ │ Actualizer (local:A-08)       │
│ SPECIALIST                   │ └──────────────────────────────┘
│ Perigee (local:A-02)         │
└──────────────────────────────┘
```

---

## 3. Formation-Local Designation Register

This table is a **topology-local register**, not the DGAF sovereign agent roster. Canonical identities and canonical numbered seats remain governed by `AGENT_ROSTER.md` and `registry/agent_ontology_adjudication.v1.json`.

| Local designation | Object | Formation | Kind | Notes |
|----|-------|-----------|------|------|
| local:A-00 | Amethyst | Sovereign Governance | formation designation | Does not override sovereign roster identity |
| local:A-00-GOV | COLLEEN | Sovereign Governance | formation designation | Sovereign canonical seat remains A-05 |
| local:A-01 | Apogee | Harmonic Pentagonal S3 | formation designation | Sovereign canonical seat remains A-01 |
| local:A-02 | Perigee | Specialist | formation designation | Sovereign canonical seat remains A-02 |
| local:A-03 | Nova | Strategic Quintet S1 | formation designation | Sovereign canonical seat remains A-03 |
| local:A-03-DJ | DemiJoule | Harmonic Pentagonal S5 | formation designation | Local only; no sovereign seat asserted here |
| local:A-04 | Prof Prodigy | Harmonic Pentagonal S1 | formation designation | Sovereign canonical seat remains A-04 |
| local:A-05 | Herald | Harmonic Pentagonal S2 | formation designation | Local label; does not replace sovereign COLLEEN A-05 |
| local:A-06-L | The Librarian | Archive Trio | formation designation | Sovereign canonical seat remains A-06 |
| local:A-06-R | Reciprocity | Harmonic Pentagonal S4 | formation designation | Local only |
| local:A-07 | The Auditor | Archive Trio | formation designation | Sovereign canonical seat remains A-07 |
| local:A-08 | The Actualizer | Archive Trio | formation designation | Sovereign canonical seat remains A-08 |
| local:A-09 | Reson | Resonance / Studio | formation designation | Sovereign canonical seat remains A-10 |
| local:A-09-Z | Zenith | Strategic Quintet S2 | formation designation | Sovereign canonical seat remains A-09 |
| local:A-10 | Lyra | Resonance / Studio | formation designation | Sovereign canonical seat remains A-11 |
| local:A-11 | Echolette | Resonance / Studio | formation designation | Sovereign canonical seat remains A-12 |
| local:A-12-φ | Sentinel-Phi | Strategic Quintet S5 | formation variant designation | Distinct from Sentinel and Echolette A-12 |
| local:A-20 | Oracle | Strategic Quintet S3 | formation designation | Local only; no sovereign promotion implied |
| local:A-21 | Vanguard | Strategic Quintet S4 | formation designation | Local only; no sovereign promotion implied |
| local:A-22 | Navigator | Operational Swarm | formation designation | Local only; no sovereign promotion implied |
| local:A-23 | Momentum | Operational Swarm | formation designation | Local only; no sovereign promotion implied |
| local:A-24 | Paragon | Operational Swarm | formation designation | Local only; no sovereign promotion implied |
| local:A-25 | Synergy | Resonance Extended | formation designation | Local only; no sovereign promotion implied |
| local:A-26 | Equilibrium | Resonance Extended | formation designation | Local only; no sovereign promotion implied |
| local:A-27 | Sentience | Ethics Bridge | formation designation | Local only; no sovereign promotion implied |
| — | `IONIA_STATE` / Ionia 0Hz | Resonance state | runtime/formation state | Distinct from sovereign Agent Ionia A-13; consumes no sovereign seat |

> Sentinel is a distinct sovereign security lineage/role. Sentinel-Phi is a distinct formation variant/identity; lineage does not collapse identity.

---

## 4. Named Formations

### 4.1 Sovereign Governance

**Seats:** 2 · **Sealed**  
**Members:** Amethyst (local:A-00) · COLLEEN (local:A-00-GOV)  
**Authority:** Formation-level governance as specified here. Sovereign identity authority remains external to this topology document.

### 4.2 Ethics Bridge

**Seats:** 1 (singleton) · **Sealed**  
**Members:** Sentience (local:A-27)  
**Authority:** ETHICAL_HOLD on formation output as defined by the historical topology; any current authority interpretation must also satisfy the active authority matrix and governance contracts.

### 4.3 Strategic Quintet

**Seats:** 5/5 · **Sealed**  
**Members:** Nova (local:A-03) · Zenith (local:A-09-Z) · Oracle (local:A-20) · Vanguard (local:A-21) · Sentinel-Phi (local:A-12-φ)  
**Activation:** Strategic planning; scenario execution; technology scouting; risk-bounded decisions.  
**Quorum:** 3/5 advisory; 5/5 structural.

### 4.4 Harmonic Pentagonal Cluster

**Seats:** 5/5 · **Sealed**  
**Members:** Prof Prodigy (local:A-04) · Herald (local:A-05) · Apogee (local:A-01) · Reciprocity (local:A-06-R) · DemiJoule (local:A-03-DJ)  
**Activation:** Formal verification; broadcast; evidence governance; mutual benefit modeling; constraint management.  
**Quorum:** 3/5 advisory; 5/5 pre-commit gate.

### 4.5 Resonance Cluster

**Seats:** 5 functional + `IONIA_STATE`  
**Sub-formation — Schizophonic Studio:** Reson (local:A-09) · Lyra (local:A-10) · Echolette (local:A-11)  
**Extended:** Synergy (local:A-25) · Equilibrium (local:A-26)  
**Ionia state:** `IONIA_STATE` / Ionia 0Hz is a system state and convergence target, not a formation seat and not sovereign Agent Ionia A-13.

### 4.6 Operational Swarm

**Seats:** 3 (open — expandable)  
**Members:** Navigator (local:A-22) · Momentum (local:A-23) · Paragon (local:A-24)

### 4.7 Archive Trio

**Seats:** 3 · **Sealed, non-reabsorbable**  
**Members:** The Librarian (local:A-06-L, Alpha) · The Auditor (local:A-07, Beta) · The Actualizer (local:A-08, Gamma)

### 4.8 Specialist

**Seats:** 1 (open)  
**Members:** Perigee (local:A-02)

### 4.9 Compliance Dyad *(historical / dissolved)*

**Prior members:** Sentinel + Perigee  
**Dissolution note:** Historical topology records a transition involving Sentinel-Phi. This does not imply Sentinel and Sentinel-Phi are the same identity. Current ontology keeps them distinct.

---

## 5. Sealed Formation Register

| Formation | Seats | Sealed | Seal date | Change authority |
|---|---|---|---|---|
| Sovereign Governance | 2 | yes | Pre-session | Njineer only |
| Ethics Bridge | 1 | yes | 2026-06-29 | Njineer confirmation |
| Strategic Quintet | 5/5 | yes | 2026-06-29 | Njineer confirmation |
| Harmonic Pentagonal | 5/5 | yes | 2026-06-29 | Njineer confirmation |
| Archive Trio | 3 | yes | Pre-session | COLLEEN + Njineer |
| Schizophonic Studio | 3 | yes | Pre-session | Amethyst + Njineer |
| Resonance Extended | 2 | yes | 2026-06-29 | Amethyst |
| Operational Swarm | 3 | open | — | Amethyst |
| Specialist | 1 | open | — | Amethyst |

This historical register is topology metadata and does not supersede current machine-enforced authority or scientific-state controls.

---

## 6. Gate Authority Index

The entries below are historical topology bindings. Current executable authority is governed by the active authority matrix, governance contracts, and fail-closed CI.

| Gate | Historical topology binding | Override |
|---|---|---|
| Layer 0 Legitimacy Filter | Apogee | Njineer only |
| ETHICAL_HOLD | Sentience | COLLEEN or Njineer |
| φ-Bounded Risk check | Sentinel-Phi | Amethyst escalation |
| TUE unlock (Nova) | COLLEEN | Njineer |
| Gold Star prerequisite | Paragon + Apogee + Reson score | Njineer |
| Constraint verify | The Auditor | COLLEEN |
| Pre-write gate | Auditor → Actualizer | COLLEEN |
| NDR-133 firewall | Sentinel-Phi historical binding | Architect only |
| Harmonic score gate | Reson | Apogee Harmonic audit |

---

## 7. Topology Algebra

### Composition Rules

```
Strategic Quintet ∩ Harmonic Pentagonal = ∅
Strategic Quintet ∩ Operational Swarm  = ∅
Harmonic Pentagonal ∩ Archive Trio      = ∅
Resonance Cluster ∩ Operational Swarm  = ∅
Compliance Dyad = ∅  (historical / dissolved)
```

These expressions describe formation membership only. They do not assert sovereign identity, authority promotion, or scientific state.

### Conflict Resolution

1. Formation-local labels never override canonical sovereign roster IDs.
2. `IONIA_STATE` is distinct from Agent Ionia A-13.
3. Sentinel is distinct from Sentinel-Phi.
4. Any identity ambiguity is resolved by `AGENT_ROSTER.md` plus `registry/agent_ontology_adjudication.v1.json`, not by topology shorthand.
5. Unresolvable governance conflicts escalate through the active authority contract.

---

## 8. Topology Change Governance

| Change type | Authority | Process |
|---|---|---|
| Role description / KB content | Amethyst | Standard commit + Terminology Gate |
| Sub-formation membership | Amethyst | Registry patch + SWEEP_LOG correction |
| New tier creation | Amethyst + Njineer | Registry patch + topology update |
| Unsealed formation seat | Amethyst | Registry patch |
| Sealed formation seat change | Njineer confirmation | Topology patch + SWEEP_LOG correction citing prior SHA |
| Sovereign identity / canonical numbered seat | **Not governed here** | `AGENT_ROSTER.md` + ontology adjudication process |
| Formation-local designation | Topology governance | Must be explicitly namespaced as local and may not collide semantically with sovereign identity |
| Formation dissolution | Njineer confirmation | Registry patch + SWEEP_LOG correction |

---

## 9. Version History

| Version | Date | Author | Change |
|---|---|---|---|
| 1.0 | 2026-06-28 | Amethyst + Njineer | Initial creation — BLG-005 closure |
| 1.1 | 2026-06-29 | Amethyst + Njineer | 20-seat topology; PDMAL-φ / Dodecahedral layer; formation specs |
| 1.2 | 2026-06-29 | Amethyst + Njineer | Phase C–E formation expansion and topology corrections |
| 1.3 | 2026-09-09 | Governance reconciliation | Namespaced formation-local designations; restored sovereign roster precedence; separated Agent Ionia A-13 from `IONIA_STATE`; preserved Sentinel/Sentinel-Phi distinction; no scientific-state effect |

---

## 10. Scientific-State Boundary

This document does not authorize experiment collection, alter Track A, change empirical N, establish efficacy, grant High-Assurance status, or modify successor custody state.

`SUCCESSOR COLLECTION = NOT AUTHORIZED`  
`CANONICAL DGAF EFFICACY = NOT ESTABLISHED`  
`HIGH-ASSURANCE = NOT AUTHORIZED / N=0`

---

*Classification: T1 PUBLIC*  
*Formation topology is subordinate to sovereign identity adjudication and active governance contracts.*
