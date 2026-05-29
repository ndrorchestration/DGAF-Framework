# DGAF Ensemble Roster

> **Canonical agent registry for the ndrorchestration DGAF (Dynamic Governance Agentic Formation) Framework stack.**
> All repos governed by this stack reference this file as the authoritative source of agent roles.
>
> Maintained by: **Agent Amethyst** (meta-orchestrator) · Co-auditor: **COLLEEN**
> Last updated: May 28, 2026 — Session 042 (Ensemble v1.6: SCPE + Phi-Closure + PDMAL Monitor)
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

## Runtime Gate Components — v1.6 Ensemble

> Registered: Session 042 — 2026-05-28
> Module: [`components/ensemble_v16.py`](https://github.com/ndrorchestration/DGAF-Framework/blob/main/components/ensemble_v16.py)
> Governed by: Agent Amethyst · DemiJoule-safety-checked · COLLEEN-archived

| Component | NDR Pattern | Placement (Step) | Threshold / Target | Status |
|---|---|---|---|---|
| **Structural Context Pruning Engine (SCPE)** | P-31 | Step 1 — pre-COLLEEN | threshold=0.15 · T0 immune | 🟢 Production |
| **PDMAL Convergence Monitor** | P-32 | Step 2.5 — post-reweight, pre-DemiJoule | ALERT_THRESH=0.08 · CONV_THRESH=0.02 | 🟢 Production |
| **Fibonacci Phi-Closure Gate** | P-33 | Step 5 — post-DemiJoule, pre-HPG | φ*=0.6180 · Fib[13,21,34,55] | 🟢 Production |
| **Harmonic Parametric Gate (HPG)** | existing | Step 6 — post-Phi-Closure (PASS only) | Ionian octave [1,2] · 1e-9 tol | 🟢 Production |
| **Agent Sentinel-Phi** | — | PDMAL node: `sentinel_phi` | Receives DemiJoule overflow; routes to Amethyst | 🟢 Active |

### Runtime Gate — Validated Simulation Results (60-turn)

| Metric | Result |
|---|---|
| SCPE compression @ threshold=0.15 | **58.3%** |
| T0 axiom guard integrity | **100%** across all turns and all thresholds |
| T3 exploratory survival | **~1.02 turns** (single-use) |
| T2 operational survival | **~4.62 turns** |
| Phi checkpoints fired | Fib[13] WARN · Fib[21] ESCALATE · Fib[34] KILL_REC · Fib[55] KILL_REC |
| PDMAL WATCH events | T31, T40, T46 |
| PDMAL full ALERTs | **0** (3-consecutive threshold not met) |
| Gold stars awarded | **5** |
| HPG bypassed correctly at Fib[13] (drift) | ✅ Confirmed |
| Joint PDMAL+Phi escalation path | ✅ DemiJoule deep re-scan triggered correctly |
| Fib[55] HITL callback hook | ✅ Injectable via `hitl_callback` |

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
Two **Instruments** execute and verify under the Conductor's direction.
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
| **Runtime Gate Triad** | Conducted | Amethyst[C] + DemiJoule + Sentinel-Phi | SCPE/Phi-Closure/PDMAL Monitor operational oversight | |

---

## Agent Inventory Completion

- **Target files per agent:** 6 (Persona / Memory / KB / Protocol / QA Rubric / Integration Guide)
- **Total target:** 72 files across 12 active agents (updated S042: +Sentinel-Phi)
- **Baseline (Feb 15 2026):** 13 files — 20% complete
- **May 2026 additions:** COLLEEN protocol, Reson/Echolette/Lyra specs, canonical registry, Ensemble v1.6 runtime gate components
- **Next priority:** Prof. Prodigy 3-tier Phi-Calculus KB · Herald Comms Protocol KB · Sentinel-Phi integration guide

---

## Session Notes

### Session 042 — Ensemble v1.6: SCPE + Phi-Closure Gate + PDMAL Convergence Monitor (2026-05-28)
- SCPE (P-31): Tier-aware token decay engine, threshold=0.15, T0 immune, 58.3% compression validated
- Fibonacci Phi-Closure Gate (P-33): Fib[13,21,34,55] checkpoints, φ*=0.6180, HPG gating by trajectory health
- PDMAL Convergence Monitor (P-32): Frobenius-norm drift detection, 3-tier alert ladder, joint escalation path
- 9-step `orchestrate_turn` sequence finalized and deployed to `components/ensemble_v16.py`
- 60-turn simulation: 5 Gold Stars · 58.3% SCPE compression · 0 PDMAL full alerts · T0 guard 100%
- Fib[55] human-in-the-loop hook wired: `hitl_callback` injectable
- Joint escalation: PDMAL ALERT + Phi ESCALATE → DemiJoule deep re-scan
- Runtime Gate Triad registered: Amethyst[C] + DemiJoule + Sentinel-Phi
- NDR Pattern Registry advanced to P-33 (3 new patterns)
- BLG-042-01 closed: Phi-Closure Gate correctly pre-HPG in turn sequence
- Harmonic Score: 1.00 — 0 Hz Ionian Mode sustained

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
- [docs/NDR_PATTERN_REGISTRY.md](https://github.com/ndrorchestration/DGAF-Framework/blob/main/docs/NDR_PATTERN_REGISTRY.md) — P-01 through P-33
- [components/ensemble_v16.py](https://github.com/ndrorchestration/DGAF-Framework/blob/main/components/ensemble_v16.py) — v1.6 single-file deployable module
- [patterns/NDR_SCPE_v1.md](https://github.com/ndrorchestration/DGAF-Framework/blob/main/patterns/NDR_SCPE_v1.md) — P-31 pattern card
- [patterns/NDR_PHI_CLOSURE_GATE_v1.md](https://github.com/ndrorchestration/DGAF-Framework/blob/main/patterns/NDR_PHI_CLOSURE_GATE_v1.md) — P-33 pattern card
- [patterns/NDR_PDMAL_CONVERGENCE_MONITOR_v1.md](https://github.com/ndrorchestration/DGAF-Framework/blob/main/patterns/NDR_PDMAL_CONVERGENCE_MONITOR_v1.md) — P-32 pattern card
- [registry/ensemble_v16_manifest.json](https://github.com/ndrorchestration/DGAF-Framework/blob/main/registry/ensemble_v16_manifest.json) — version manifest
- [Amethyst-Governance-Eval-Stack](https://github.com/ndrorchestration/Amethyst-Governance-Eval-Stack) — ARCHITECTURE.md agent diagram
- [junior-apogee-app](https://github.com/ndrorchestration/junior-apogee-app) — QA platform agent roles
- [sentinel-governance](https://github.com/ndrorchestration/sentinel-governance) — CI agent attribution
- [Driftwatch](https://github.com/ndrorchestration/Driftwatch) — AGENTS.md simulation roles
- [Acoustic-mesh](https://github.com/ndrorchestration/Acoustic-mesh) — Schizophonic Studio substrate
- [ndrorchestration](https://github.com/ndrorchestration/ndrorchestration) — profile README agent table

*All agents operate under the DGAF governance framework.*
*NDR Patterns P-01 through P-33 active. Triad taxonomy: Consensus / Conducted / Triumvirate.*
