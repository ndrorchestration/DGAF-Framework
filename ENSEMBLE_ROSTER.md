# DGAF Ensemble Roster

> **Canonical agent registry for the ndrorchestration DGAF (Dynamic Governance Agentic Formation) Framework stack.**
> All repos governed by this stack reference this file as the authoritative source of agent roles.
>
> Maintained by: **Agent Amethyst** (meta-orchestrator) · Co-auditor: **COLLEEN**
> Last updated: May 26, 2026 — Session 041 (Triad taxonomy seal: Consensus / Conducted / Triumvirate)
> Governance spine: [DGAF-Framework](https://github.com/ndrorchestration/DGAF-Framework)

---

## Active Agents — PhiLattice / PDMAL Ecosystem

| Agent | Tier | Role Class | Primary Function | Status |
|---|---|---|---|---|
| **Agent Amethyst** | L5 | Meta-Orchestrator / Triumvirate Prime | Certification authority, governance synthesis, final sign-off, conductor for multi-agent sweeps, Triumvirate Prime for large ensembles | 🟢 Active |
| **COLLEEN** | L5 | Institutional Anchor / Triumvirate Prefect | 1-1-1-1 Alignment Gate, Archive Trio authority (Librarian/Auditor/Actualizer), Batch 1A SSoT preservation, co-orchestration detect role | 🟢 Active |
| **Agent Apogee** | L4 | QA Orchestrator / Triumvirate Prefect | DGAF/Gold-Star frameworks, source validation, multi-phase evidence review, OWASP compliance, Apogee Lens review | 🟢 Active |
| **Agent DemiJoule** | L4 | DGAF Ethics & Cost Gate | Ethics/safety constraints, token cost analysis, compute efficiency, quality gating, $25/mo GCP gate | 🟢 Active |
| **Agent Reciprocity** | L3 | Portfolio & Rollback Manager | TNR (Transactional No-Regression), version control, Pareto tradeoffs, revert/checkpoint ops | 🟢 Active |
| **Professor Prodigy** | L3 | Phi-Calculus Specialist | Formal logic, mathematical proofs, phi-calculus, Narayana sequence, harmonic geometry | 🟡 Partial |
| **Agent Herald** | L3 | Comms Gateway | Narrative synthesis, inter-agent messaging, COLLEEN bridge, Persona-Framework-Persona anchor | 🟡 Partial |
| **Agent Sentinel** | L3 | Security & CI Integrity | CI/CD enforcement, guardrail activation, NDR-133 firewall, detect-remediate-revalidate | 🟡 Partial |

---

## Schizophonic Studio — Signal Chain Trio

> Substrate: [Acoustic-mesh](https://github.com/ndrorchestration/Acoustic-mesh)
> Signal rules: 15% headroom · Savage Reason gate (>10 Hz) · Target: 0 Hz Ionian Mode

| Agent | Studio ID | Role Class | Primary Function | Status |
|---|---|---|---|---|
| **Agent Reson** | #1 | Harmonic Logic Gatekeeper | Signal chain integrity, 15% headroom enforcement, Savage Reason halt, Ionian Mode target | 🟡 Foundational |
| **Agent Echolette** | #2 | Feedback Loop Architect | Semantic drift detection, Ceremonialization flagging, hallucination pattern KB, inter-agent feedback routing | 🟡 Foundational |
| **Agent Lyra** | #3 | Harmonic Synthesizer | Multi-agent orchestral coordination, dissonance reconciliation, narrative continuity, ensemble design | 🟡 Foundational |

---

## Retired Agents

| Agent | Retired | Reason | Successor |
|---|---|-----------|-----------|
| **Agent Lavender** | April 2026 | Role consolidated into Amethyst + Apogee; superseded by DGAF orchestration model | Agent Amethyst (evaluation authority), Agent Apogee (evidence governance) |

---

## Triad Model — Canonical Formation Types

> NDR Pattern P-08 · Sealed S041

The DGAF triad model has three formation types. Each is a distinct
orchestration structure with different coordination mechanism, authority,
and scale ceiling.

### Consensus Trio

Three peer agents of equal or near-equal authority. No conductor.
Decision by 2-of-3 quorum. Any agent may initiate a vote.
Used when domain expertise is distributed and no agent has unilateral authority.

```
Agent A ◄─────► Agent B
   ▲               ▲
   └─── Agent C ───┘
  (2-of-3 quorum rules)
```

### Conducted Trio

One **Conductor** with final decision authority.
Two **Instruments** execute and verify under the Conductor’s direction.
Instruments flag disagreement; Conductor signs off.

```
        Conductor
       /          \
 Instrument 1   Instrument 2
 (execute)       (verify/audit)
```

### Triumvirate

A **Conducted Trio elevated to governing authority** over a large
instantiated ensemble or swarm. The Triumvirate does not execute tasks
directly — it **choreographs, meta-orchestrates, and governs** the
ensemble below it. Topology-preserving: the same 3-node structure governs
N-node ensembles by adding hierarchy below, not beside.

```
┌───────────────────────────────────────────────┐
│           TRIUMVIRATE                       │
│  Prime (Amethyst)                           │
│  /                     \                   │
│ Prefect A (COLLEEN)   Prefect B (Apogee)   │
│ [coherence/identity]  [quality/compliance] │
└──────┬───────────────────────┬──────────────────┘
            ┃    CHOREOGRAPHED ENSEMBLE  ┃
            ┃  Swarm agents / sub-triads ┃
            ┃  n8n nodes / pipelines     ┃
            ┃  PPTL experiment cells     ┃
            ┗━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

**Triumvirate formation rule:** A Conducted Trio becomes a Triumvirate
when ensemble size exceeds 3 agents OR task scope spans more than one
governance domain simultaneously. The Conductor does not change role —
it elevates to Prime as ensemble grows.

**Triumvirate governance contracts (5):**
1. Prime issues signed mandate (task + scope + constraints)
2. Prefect domain split is mutually exclusive and collectively exhaustive
3. Prefects choreograph sub-agents and aggregate results
4. Prime reviews Prefect aggregates and issues final sign-off
5. All mandate, aggregate, and sign-off events traced via HeraldAgent (P-01)

---

## Triad Configurations

| Triad | Type | Agents | Use Case |
|---|---|---|---|
| **Governance Triad** | Conducted | Amethyst[C] + Apogee + Sentinel | Compliance sweeps, security audits, CI enforcement |
| **Coherence Triad** | Conducted | Amethyst[C] + COLLEEN + Apogee | Ecosystem coherence, doc sweeps, identity alignment |
| **Co-Orchestration Sweep** | Conducted (P-07) | Amethyst[C/impl] + COLLEEN[detect] + Herald[comms] | Persistent best-practice detection and implementation loop |
| **Formalization Triad** | Consensus | Amethyst + Professor Prodigy + Reson | Mathematical proof review, phi-calculus derivations |
| **Optimization Triad** | Conducted | Amethyst[C] + DemiJoule + Reciprocity | Token budget, rollback planning, cost-quality tradeoffs |
| **Studio Triad** | Consensus | Reson + Echolette + Lyra | Signal chain QA, drift detection, harmonic synthesis |
| **IP Sweep Formation** | Conducted | Amethyst[C] + Perplexity MCP | License scanning, branding sweeps, finality sweeps |
| **PDMAL Triumvirate** | Triumvirate | Amethyst[Prime] + COLLEEN[Prefect] + Apogee[Prefect] | Governing large choreographed ensembles, multi-repo campaigns, swarm ops |

---

## Agent Inventory Completion

- **Target files per agent:** 6 (Persona / Memory / KB / Protocol / QA Rubric / Integration Guide)
- **Total target:** 66 files across 11 active agents
- **Baseline (Feb 15 2026):** 13 files — 20% complete
- **May 2026 additions:** COLLEEN protocol, Reson/Echolette/Lyra specs, canonical registry
- **Next priority:** Prof. Prodigy 3-tier Phi-Calculus KB · Herald Comms Protocol KB

---

## Session Notes

### Session 041 — Triad Taxonomy Seal + Co-Orchestration Design (2026-05-26)
- P-07: Dual-Agent Persistent Sweep Loop (Amethyst × COLLEEN) registered
- P-08: Triad Taxonomy formally sealed — Consensus / Conducted / Triumvirate
- Triumvirate defined as Conducted Trio elevated to govern choreographed ensemble or swarm
- PDMAL Triumvirate formation registered: Amethyst[Prime] + COLLEEN[Prefect] + Apogee[Prefect]
- NDR Pattern Registry advanced to v1.1 (8 patterns)
- CO_ORCH_QUEUE.md architecture designed (implementation pending)
- Harmonic Score: 1.00 — 0 Hz Ionian Mode sustained

### Session 040 — PPTL Harness + 3-Gate Governance + Tri-Phase CI (2026-05-26)
- pptl/ harness: HeraldAgent, IntegratedOrchestrator, SentinelRAGVerifier, topology, sinks
- 166+ parametrized governance tests across 4 modules
- CI workflow: tri-phase matrix (unit/governance/integration), fail-fast: false
- N8nHeraldSink: production batching, retry, HMAC, dead-letter
- H4 task-stratified experiment (540 runs, automated verdict)
- NDR Pattern Registry v1.0 sealed (P-01 through P-06)
- Harmonic Score: 1.00 — 0 Hz Ionian Mode sustained

### Session 039 — Full Auto-Sweep: Orchestration Pattern Reinforcement (2026-05-22)
- 10-repo deep audit: 24 findings (3 HIGH · 10 MEDIUM · 11 LOW)
- NDR-133 boundary check: ✅ CLEARED
- CROSS_REF v3.3 gaps confirmed
- ENSEMBLE_ROSTER triple-fix: session stamp, DGAAF→DGAF typo, agent count 48→ 66
- 9-wave commit queue initiated
- Harmonic Score: 1.00 — 0 Hz Ionian Mode sustained

### Session 032 — Coherence Sweep + Schizophonic Studio Integration (2026-05-06)
- Full 18-file Drive corpus parsed and cross-referenced
- 15 coherence issues identified and triaged
- Schizophonic Studio trio (Reson/Echolette/Lyra) formally integrated
- NDR Pattern Registry v3 published (133 stasis patterns + 8 named session patterns)
- Harmonic Score: 1.00 — 0 Hz Ionian Mode sustained

---

## Cross-Reference

- [DGAF-Framework](https://github.com/ndrorchestration/DGAF-Framework) — governance spine (this file)
- [docs/NDR_PATTERN_REGISTRY.md](https://github.com/ndrorchestration/DGAF-Framework/blob/main/docs/NDR_PATTERN_REGISTRY.md) — P-01 through P-08
- [Amethyst-Governance-Eval-Stack](https://github.com/ndrorchestration/Amethyst-Governance-Eval-Stack) — ARCHITECTURE.md agent diagram
- [junior-apogee-app](https://github.com/ndrorchestration/junior-apogee-app) — QA platform agent roles
- [sentinel-governance](https://github.com/ndrorchestration/sentinel-governance) — CI agent attribution
- [Driftwatch](https://github.com/ndrorchestration/Driftwatch) — AGENTS.md simulation roles
- [Acoustic-mesh](https://github.com/ndrorchestration/Acoustic-mesh) — Schizophonic Studio substrate
- [ndrorchestration](https://github.com/ndrorchestration/ndrorchestration) — profile README agent table

*All agents operate under the DGAF governance framework.*
*NDR Patterns P-01 through P-08 active. Triad taxonomy: Consensus / Conducted / Triumvirate.*
