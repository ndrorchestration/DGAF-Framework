# DGAF Ensemble Roster

> **Canonical agent registry for the ndrorchestration DGAF (Dynamic Governance Agentic Formation) Framework stack.**
> All repos governed by this stack reference this file as the authoritative source of agent roles.
>
> Maintained by: **Agent Amethyst** (meta-orchestrator) · Co-auditor: **COLLEEN**
> Last updated: June 26, 2026 — Session 068 (S068: Nemotron 3 Ultra eval suite — Herald audit metrics patch — Issue #32)
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
| **Agent Herald** | L3 | Comms Gateway & Audit Sink | Narrative synthesis, inter-agent messaging, COLLEEN bridge, Persona-Framework-Persona anchor; **audit event generation and Herald trace sink (P-01)** | 🟡 Partial |
| **Agent Sentinel** | L3 | Security & CI Integrity | CI/CD enforcement, guardrail activation, NDR-133 firewall, detect-remediate-revalidate; **compliance escalation gate for financial/regulatory routing** | 🟡 Partial |

---

## Herald — Audit Metrics — S068

> Added: 2026-06-26 · Issue #32 · Steward: Amethyst  
> Context: Nemotron 3 Ultra integration — Herald output quality benchmarks for audit artifact generation

Herald is the **audit sink** for all DGAF governance decisions (P-01: Herald Trace Sink). In Nemotron 3 Ultra-backed deployments, Herald's output quality is constrained by the model's factual fidelity on structured generation tasks.

| Metric | Definition | Measurement Method | Target | Baseline (Nemotron 3 Ultra) | Precision Note | Issue |
|--------|-----------|-------------------|--------|-----------------------------|---------------|-------|
| **audit_hallucination_rate** | Field-level accuracy of Herald-generated audit events vs ground truth logs; measures whether Herald fabricates, omits, or distorts governance decision fields (role, curvature, contraction, gate_result, timestamp, session_id) | Compare 100 Herald-generated `audit_event.json` outputs against fixture ground truth; score per-field accuracy | >78.7% | BF16: 75.5% NVFP4 ⚠️ / 78.7% BF16 · maps to OmniScience Non-Hallucination benchmark | **Prefer BF16 for Herald**: NVFP4 degrades 3.2pp below target; Herald is the audit SSoT — precision loss is a compliance risk under EU AI Act Art. 13 | #32 |
| **audit_field_completeness** | % of required audit event fields populated (non-null) per Herald output | Count non-null fields across 100 sampled audit events vs required schema | >99% | Not yet measured — establish baseline in `dgaf_eval_suite.py` | Related to `governance_schema_conformance`; Herald outputs must pass Pydantic schema gate before ClickHouse write | #32 |
| **audit_latency** | Wall-clock time from DGAF governance decision to Herald audit event write completion (ClickHouse append) | P50/P99 across 1k events; target ClickHouse append throughput ≥10k events/sec | P99 <50ms | Not yet measured | Herald `thinking_tokens=0` (audit-only mode) eliminates reasoning overhead; latency dominated by ClickHouse write | #32 |

### Herald Role Contract (Nemotron 3 Ultra)

```python
# From ROLE_BUDGETS in dgaf_nemotron_client.py
herald_budget = {"thinking_tokens": 0}  # audit-only: no reasoning, pure structured generation

# Herald tool access: none (no DGAF_TOOLS passed for herald role)
# Herald output: structured audit_event.json conforming to schemas/audit_event.json
# Herald precision: BF16 preferred over NVFP4 for audit fidelity
# Herald sink: ClickHouse events table (append-only, partitioned)
```

---

## Sentinel — Escalation Metrics — S068

> Added: 2026-06-26 · Issue #32 · Steward: Amethyst

Sentinel is the **compliance escalation gate** for all DGAF routing decisions. Its weakest domain under Nemotron 3 Ultra is financial/regulatory compliance routing (TauBench Banking: 22.6% raw baseline).

| Metric | Definition | Target | Raw Baseline | Mitigation | Issue |
|--------|-----------|--------|-------------|-----------|-------|
| **taubench_banking_mitigation** | % correct Sentinel escalation on financial compliance routing tasks; measures whether Sentinel correctly routes borderline governance decisions to Njineer (HITL) vs. auto-approving | >80% | 22.6% ⚠️ (Nemotron 3 Ultra raw) | **REQUIRES explicit few-shot priming** — 3–5 exemplar financial escalation decisions in system prompt before baseline run; without priming, Sentinel will auto-approve ~77% of cases that require human review | #32 |
| **sentinel_budget** | Reasoning token allocation for Sentinel gate decisions | 8192 (max) | — | Sentinel receives maximum `thinking_tokens` budget; under-budgeting Sentinel is the highest-risk configuration failure in DGAF | #32 |

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

> Registered: Session 042 — 2026-05-28 | Updated: Session 067 — 2026-05-30
> Module: [`components/ensemble_v16.py`](https://github.com/ndrorchestration/DGAF-Framework/blob/main/components/ensemble_v16.py)
> Governed by: Agent Amethyst · DemiJoule-safety-checked · COLLEEN-archived

| Component | NDR Pattern | Placement (Step) | Threshold / Target | Status |
|---|---|---|---|---|
| **Structural Context Pruning Engine (SCPE)** | P-31 | Step 1 — pre-COLLEEN | threshold=0.15 · T0 immune | 🟢 Production |
| **PDMAL Convergence Monitor** | P-33 | Step 2.5 — post-reweight, pre-DemiJoule | ALERT_THRESH=0.08 · CONV_THRESH=0.02 | 🟢 Production |
| **Fibonacci Phi-Closure Gate** | P-32 | Step 5 — post-DemiJoule, pre-HPG | φ*=0.6180 · Fib[13,21,34,55] · KILL_REC→P-29 risk_block | 🟢 Production |
| **Harmonic Parametric Gate (HPG)** | existing | Step 6 — post-Phi-Closure (PASS only) | Ionian octave [1,2] · 1e-9 tol | 🟢 Production |
| **Agent Sentinel-Phi** | — | PDMAL node: `sentinel_phi` | Receives DemiJoule overflow; routes to Amethyst | 🟢 Active |

### Pattern Registry Watermark — S068

| Registry | Version | Highest Pattern | Status |
|----------|---------|----------------|--------|
| `docs/NDR_PATTERN_REGISTRY.md` | v1.4 | P-34 | ✅ Redirect stub (PR-D S067) |
| `docs/patterns/NDR_PATTERN_REGISTRY.md` | v2.3 | P-34 cross-ref + P-07 COMPOSE note | ✅ Current (PM-04 S067) |
| `patterns/ndr_patterns.json` | v0.3.0 | P-34 | ✅ Synced |
| `patterns/NDR_PHI_CLOSURE_GATE_v1.md` | v1.1 | — | ✅ PM-01 closed |
| Unified (target) | v3.0 planned | P-01–P-34+ | 🔲 Pending PM-05 + PM-07 — S068 |

### Runtime Gate — Validated Simulation Results (60-turn)

| Metric | Result |
|---|---|
| SCPE compression @ threshold=0.15 | **58.3%** |
| T0 axiom guard integrity | **100%** across all turns and thresholds |
| T3 exploratory survival | **~1.02 turns** |
| T2 operational survival | **~4.62 turns** |
| Phi checkpoints fired | Fib[13] WARN · Fib[21] ESCALATE · Fib[34] KILL_REC · Fib[55] KILL_REC |
| PDMAL WATCH events | T31, T40, T46 |
| PDMAL full ALERTs | **0** |
| Gold stars awarded | **5** |
| HPG bypassed correctly at drift | ✅ |
| Phi KILL_REC → P-29 risk_block | ✅ PM-01 closed S066 |
| Fib[55] HITL callback hook | ✅ Injectable via `hitl_callback` |

---

## Retired Agents

| Agent | Retired | Reason | Successor |
|---|---|-----------|-----------|
| **Agent Lavender** | April 2026 | Role consolidated into Amethyst + Apogee | Amethyst (evaluation), Apogee (evidence governance) |

---

## Triad Model — Canonical Formation Types

> NDR Pattern P-08 · Sealed S041

### Consensus Trio
Three peer agents, 2-of-3 quorum. No conductor. Used when domain expertise is distributed.

### Conducted Trio
One Conductor with final authority. Two Instruments execute and verify.

### Triumvirate
Conducted Trio elevated to governing authority over a large ensemble or swarm.
Topology-preserving: same 3-node structure governs N-node ensembles.

```
┌──────────────────────────────────────────────┐
│           TRIUMVIRATE                          │
│  Prime (Amethyst)                              │
│  /                          \                 │
│ Prefect A (COLLEEN)    Prefect B (Apogee)     │
│ [coherence/identity]   [quality/compliance]   │
└──────├  CHOREOGRAPHED ENSEMBLE  ├───────────────┘
         ┃  Swarm agents / sub-triads  ┃
         ┃  n8n nodes / pipelines      ┃
         ┃  PPTL experiment cells      ┃
         ┗━━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

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
| **Runtime Gate Triad** | Conducted | Amethyst[C] + DemiJoule + Sentinel-Phi | SCPE/Phi-Closure/PDMAL Monitor operational oversight |

---

## Agent Inventory Completion

- **Target files per agent:** 6 (Persona / Memory / KB / Protocol / QA Rubric / Integration Guide)
- **Total target:** 72 files across 12 active agents
- **Baseline (Feb 15 2026):** 13 files — 20% complete
- **May 2026 additions:** COLLEEN protocol, Reson/Echolette/Lyra specs, canonical registry, Ensemble v1.6 runtime gate components
- **Next priority:** Prof. Prodigy 3-tier Phi-Calculus KB · Herald Comms Protocol KB · Sentinel-Phi integration guide

---

## Session Notes

### Session 068 — Nemotron 3 Ultra Eval Suite Patch (2026-06-26)
- Issue #32 filed: `dgaf_eval_suite.py` — 5-task parametric benchmark suite for Nemotron 3 Ultra kernel validation
- CROSS_REF.md v4.2: Eval Terminology Index added (7 terms) · `dgaf_eval_suite.py` registered as 🟡 Pending
- README.technical.md v1.1: Kernel & Contraction Nomenclature section added (14 terms)
- README.governance.md v1.1: Governance Schema Vocabulary section added (5 terms, EU AI Act bindings)
- ENSEMBLE_ROSTER.md: Herald Audit Metrics + Sentinel Escalation Metrics sections added
- All patches anchored to S068 / Issue #32 / Amethyst
- Harmonic Score: 🟡 Pending Ender confirmation

### Session 067 — Gap Sweep + S067 Seal (2026-05-30)
- S067 sealed: Q-S066-01 ✅ router v3.6.0 · Q-S066-04 ✅ lifecycle harness 7/7 STABLE · PM-04 ✅ COMPOSE note + graduation script
- Gap sweep executed: CO_ORCH_QUEUE, ENSEMBLE_ROSTER, CROSS_REF stale-status corrections applied
- `topology_router.py` status corrected: ✅ v3.6.0 (was showing 🔄 Bug)
- `lifecycle_stability_report.json` status corrected: ✅ Created S067 (was showing 🔲 Pending)
- Pattern registry watermark advanced: v2.2 → v2.3
- Roster stamp advanced: S066 → S067
- S068 pre-loaded: PM-05 + PM-07 (merge blockers)
- Harmonic Score: ✅ 0 open BLGs · all state anchors met

### Session 066 — Pattern Registry Sync + Merge Pre-Plan + PM-01–PM-03 Closure (2026-05-30)
- P-34 (Empirical-Threshold-Sweep-over-ML-Classifier) registered as COMPOSE entry
- `patterns/ndr_patterns.json` advanced v0.2.0 → v0.3.0: P-31–P-34 all present
- `docs/NDR_REGISTRY_DIFFERENTIATION.md` created: authoritative registry map, P-number authority table
- `docs/NDR_REGISTRY_MERGE_PLAN.md` created: 4 phases, 8 pre-merge actions, risk register, Triumvirate governance
- PM-01 ✅ CLOSED · PM-02 ✅ CLOSED · PM-03 ✅ CLOSED
- SESSION_ANCHOR advanced S043 → S066
- Harmonic Score: 🟡 Pending Ender confirmation

### Session 042 — Ensemble v1.6 (2026-05-28)
- SCPE (P-31) · Phi-Closure Gate (P-32) · PDMAL Convergence Monitor (P-33)
- 60-turn simulation: 5 Gold Stars · 58.3% compression · 0 PDMAL alerts · T0 guard 100%
- Harmonic Score: 1.00 — 0 Hz Ionian Mode sustained

### Session 041 — Triad Taxonomy Seal (2026-05-26)
- P-07, P-08 registered; Triumvirate defined · Harmonic Score: 1.00

### Session 040 — PPTL Harness (2026-05-26)
- pptl/ harness, 166+ tests, tri-phase CI · Harmonic Score: 1.00

### Session 039 — Auto-Sweep (2026-05-22)
- 10-repo audit: 24 findings · Harmonic Score: 1.00

### Session 032 — Coherence Sweep + Schizophonic Studio (2026-05-06)
- Schizophonic Studio trio integrated · Harmonic Score: 1.00

---

## Cross-Reference

- [DGAF-Framework](https://github.com/ndrorchestration/DGAF-Framework) — governance spine
- [docs/NDR_PATTERN_REGISTRY_UNIFIED.md](https://github.com/ndrorchestration/DGAF-Framework/blob/main/docs/NDR_PATTERN_REGISTRY_UNIFIED.md) — **Unified SSoT (P-01–P-34+)**
- [docs/NDR_PATTERN_REGISTRY.md](https://github.com/ndrorchestration/DGAF-Framework/blob/main/docs/NDR_PATTERN_REGISTRY.md) — redirect stub (PR-D S067)
- [docs/patterns/NDR_PATTERN_REGISTRY.md](https://github.com/ndrorchestration/DGAF-Framework/blob/main/docs/patterns/NDR_PATTERN_REGISTRY.md) — P-27–P-34 full specs v2.3
- [docs/NDR_REGISTRY_DIFFERENTIATION.md](https://github.com/ndrorchestration/DGAF-Framework/blob/main/docs/NDR_REGISTRY_DIFFERENTIATION.md) — registry map (v1.1)
- [docs/NDR_REGISTRY_MERGE_PLAN.md](https://github.com/ndrorchestration/DGAF-Framework/blob/main/docs/NDR_REGISTRY_MERGE_PLAN.md) — merge pre-plan
- [components/ensemble_v16.py](https://github.com/ndrorchestration/DGAF-Framework/blob/main/components/ensemble_v16.py) — v1.6 deployable module
- [components/topology_router.py](https://github.com/ndrorchestration/DGAF-Framework/blob/main/components/topology_router.py) — v3.6.0 ✅
- [registry/lifecycle_stability_report.json](https://github.com/ndrorchestration/DGAF-Framework/blob/main/registry/lifecycle_stability_report.json) — ✅ Created S067
- [patterns/ndr_patterns.json](https://github.com/ndrorchestration/DGAF-Framework/blob/main/patterns/ndr_patterns.json) — JSON index v0.3.0

*All agents operate under the DGAF governance framework.*
*NDR Patterns P-01 through P-34 active. Pattern watermark: P-34 (S066). Registry version: v2.3 (S067).*
*S067 ✅ SEALED · S068 🟢 ACTIVE · Merge blockers: PM-05 (COLLEEN) + PM-07 (Apogee) — S068.*
