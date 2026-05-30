# NDR Pattern Registry (Unified)

**DGAF-Framework · Unified Edition**
**Version:** 1.0 (Phase 3 merge — S066)
**Prime:** Amethyst · **Prefect A:** COLLEEN · **Prefect B:** Apogee
**Ender ratification:** 2026-05-30 02:49 EDT
**Date:** 2026-05-30
**Status:** ✅ CANONICAL — single source of truth for all NDR patterns P-01–P-34

> **This file supersedes:**
> - `docs/NDR_PATTERN_REGISTRY.md` (P-01–P-10 source — now redirect stub)
> - `docs/patterns/NDR_PATTERN_REGISTRY.md` (P-27–P-30 + stasis source — now redirect stub)
> - `patterns/NDR_SCPE_v1.md`, `NDR_PHI_CLOSURE_GATE_v1.md`, `NDR_PDMAL_CONVERGENCE_MONITOR_v1.md` (archived)

---

## Registry Metadata

| Field | Value |
|-------|-------|
| Total patterns | 34 named (P-01–P-34) + 133 stasis (P-12–P-26 block) |
| Registry watermark | P-34 |
| ndr_patterns_unified.json | `docs/ndr_patterns_unified.json` |
| Last session | S066 · 2026-05-30 |
| Merge provenance | `docs/NDR_REGISTRY_MERGE_PLAN.md` v1.3 |

---

## How to Use This Registry

- **Find a pattern by number:** Use the Pattern Layers Quick-Reference table below.
- **Find a pattern by function:** Use the layer headings.
- **Understand interactions:** See the Pattern Interaction Map section.
- **Understand the stack:** See the Governance Orchestration Stack section.
- **Register a new pattern:** Submit a COMPOSE entry via P-07; Amethyst registers as P-N+1.
- **Attest a pattern:** Run P-11 11Q rubric; gate via P-30. Attestation artifact goes in `docs/qa/`.

---

## Pattern Layers Quick-Reference

| Pattern | Name | Layer | Session |
|---------|------|-------|---------|
| P-01 | Fan-Out Trace Sink w/ Dead-Letter | Layer 1 — Trace & Audit | S040 |
| P-02 | Async-Persist Ring Buffer | Layer 1 — Trace & Audit | S040 |
| P-03 | Governance Contract Test | Layer 2 — Testing & CI | S040 |
| P-04 | Parametrized Corpus | Layer 2 — Testing & CI | S040 |
| P-05 | Tri-Phase CI Gate | Layer 2 — Testing & CI | S040 |
| P-06 | Topology × Orchestration Matrix Lab | Layer 3 — Architecture Lab | S041 |
| P-07 | Dual-Agent Persistent Sweep Loop | Layer 4 — Governance Formation | S041 |
| P-08 | Triad Taxonomy | Layer 4 — Governance Formation | S041 |
| P-09 | Triumvirate Mandate Schema | Layer 4 — Governance Formation | S041 |
| P-10 | Session Graduation Check | Layer 4 — Governance Formation | S041 |
| P-11 | 11Q Attestation Scoring | Layer 5 — Quality Gate | S033 |
| P-12–P-26 | Stasis Patterns (133 entries) | Layer 6 — Stasis | Pre-S033 |
| P-27 | Adaptive-Weighting-with-Confidence-Gates | Layer 7 — Router Calibration | S033/S034/S066 |
| P-28 | Pipeline-Composition-with-Confidence-Gated-Routing | Layer 7 — Router Calibration | S033 |
| P-29 | Sentinel-Annotated Risk Pass | Layer 8 — Safety & Sentinel | S034 |
| P-30 | Apogee-Attestation-Gate | Layer 5 — Quality Gate | S035/S066 |
| P-31 | SCPE — Structural Context Pruning Engine | Layer 9 — Long-Context Safety | S042 |
| P-32 | Fibonacci Phi-Closure Gate | Layer 9 — Long-Context Safety | S042/S066 |
| P-33 | PDMAL Convergence Monitor | Layer 9 — Long-Context Safety | S042 |
| P-34 | Empirical-Threshold-Sweep-over-ML-Classifier | Layer 7 — Router Calibration | S066 |

---

## Layer 1 — Trace & Audit

### P-01 — Fan-Out Trace Sink w/ Dead-Letter

**Spec:** `HeraldAgent` holds a list of registered `Sink` objects. On every `emit()` call, it iterates all sinks, wraps each write in `try/except`, and routes any failure to a dead-letter JSONL file. Sink failures are logged but never re-raised. Downstream sinks always execute regardless of upstream failures.

**Use:** Any multi-agent system requiring audit trace across multiple destinations (JSONL file, stdout, webhook, database) where a single sink failure must not interrupt the trace pipeline.

**Trigger:** More than one sink registered; any sink does I/O.

**Tradeoffs:**
- ✅ Strong isolation — one bad sink cannot corrupt the audit record
- ✅ Dead-letter preserves all events for replay/backfill
- ⚠️ Fan-out is synchronous — latency = sum of all sink write times
- ⚠️ Dead-letter file must be monitored; silent accumulation is a hidden failure mode

**NIST:** Govern | **EU AI Act:** Art.13
**Implementation:** `pptl/herald_agent.py`, `pptl/sinks.py`
**Registered:** S040

---

### P-02 — Async-Persist Ring Buffer

**Spec:** High-throughput trace events are written to an in-process ring buffer (bounded `deque`). A background thread drains the buffer to persistent storage (JSONL / DB) on a configurable interval or when buffer reaches capacity. All write operations acquire a `threading.Lock`. On `close()`, the drain loop flushes all remaining events before terminating.

**Use:** Production Herald deployments where sink I/O latency would otherwise block the main agent execution thread.

**Trigger:** `emit()` latency > 5ms in profiling; multi-threaded agent workloads.

**Tradeoffs:**
- ✅ Decouples agent execution speed from sink I/O latency
- ✅ Bounded buffer prevents unbounded memory growth
- ⚠️ Events in buffer are lost on hard process crash (mitigated by short drain interval)
- ⚠️ Adds background thread complexity; requires careful shutdown sequencing

**NIST:** Govern | **EU AI Act:** Art.13
**Implementation:** `pptl/n8n_herald_sink.py`, `pptl/sinks.py`
**Registered:** S040

---

## Layer 2 — Testing & CI

### P-03 — Governance Contract Test

**Spec:** For every governance gate, assert four contracts independently: (1) correct status string, (2) correct `event_type` emitted, (3) correct downstream execution state, (4) correct gate-specific invariant. Each contract is a separate test function marked `@pytest.mark.governance`.

**ALTER (OPP-003):** Gate 0 (AttestationGate / P-30) requires 6 contracts (adds: token valid, expiry check). Document contract count per gate in stub header. **PM-02: ✅ CLOSED S066.**

**Use:** CI merge gate. Any PR touching gate logic, threshold values, or event emission order.

**Trigger:** Adding a new gate, modifying a gate threshold, changing event type names, altering downstream execution flow.

**Tradeoffs:**
- ✅ Catches silent regressions where status string changes but behavior doesn't
- ✅ Four-contract structure documents architectural invariants as executable code
- ⚠️ Requires fixture isolation — adds test count
- ⚠️ Must be updated when gate logic is intentionally changed

**NIST:** Measure, Govern | **EU AI Act:** Art.9
**Implementation:** `pptl/tests/test_orchestrator.py`
**Registered:** S040

---

### P-04 — Parametrized Corpus

**Spec:** Signal lists defined as module-level constants in production source. Test files import constants and build parametrize inputs dynamically. Adding a signal to the source auto-expands the test suite with zero test-code changes.

**Use:** Any governance gate with an enumerable signal corpus.

**Trigger:** New signal added to `BYPASS_SIGNALS` or `HALLU_SIGNALS`.

**Tradeoffs:**
- ✅ Single source of truth — no drift between production signal list and test corpus
- ✅ Auto-expansion — new signals tested immediately
- ⚠️ Test count scales linearly with corpus size
- ⚠️ Obfuscation variants require manual curation

**NIST:** Measure | **EU AI Act:** Art.9
**Implementation:** `pptl/tests/test_orchestrator.py`, `pptl/rag_verifier.py`
**Registered:** S040

---

### P-05 — Tri-Phase CI Gate

**Spec:** GitHub Actions matrix: `unit` / `governance` / `integration`. `fail-fast: false`. Governance step is the designated merge blocker. Each step uploads a JUnit XML artifact.

**Use:** Any repo where governance contract correctness must be independently verifiable from functional behavior.

**Trigger:** First PR touching gate logic, sink behavior, or signal corpora.

**Tradeoffs:**
- ✅ Governance failures immediately locatable
- ✅ `fail-fast: false` gives complete failure picture in one CI run
- ⚠️ 3× runner cost vs single step
- ⚠️ Branch protection must be manually configured after workflow is merged

**NIST:** Govern | **EU AI Act:** Art.9, Art.17
**Implementation:** `.github/workflows/pptl-ci.yml`
**Registered:** S040

---

## Layer 3 — Architecture Lab

### P-06 — Topology × Orchestration Matrix Lab

**Spec:** Enumerate all `(topology, orchestration_mode)` cell combinations. For each cell, run N seeds × M task families × K noise levels. Score each run with a composite metric (governance-weighted). Report five canonical outputs: topology ranking, mode ranking, interaction heatmap, triadic lift, noise resilience curves.

**Use:** Any governance architecture decision requiring empirical differentiation between structural topology choices and orchestration control patterns.

**Trigger:** Topology choice disputed, new orchestration mode proposed, or noise resilience requirements need quantification.

**Tradeoffs:**
- ✅ Evidence-based architecture decisions
- ✅ Interaction effects surface non-obvious topology × mode combinations
- ⚠️ Simulation results depend on scoring model validity
- ⚠️ Combinatorial explosion at high N/M/K

**Implementation:** `pptl/experiments/h4_task_stratified.py`
**Registered:** S041

---

## Layer 4 — Governance Formation

### P-07 — Dual-Agent Persistent Sweep Loop

**Spec:** Two agents with separated detect and implement roles share a markdown+JSON queue (`CO_ORCH_QUEUE.md`) as SSoT hand-off substrate. Detector (COLLEEN) scores each opportunity through a binary 4-gate alignment check. Passing opportunities are classified into one of four implementation modes. Implementer (Amethyst) reads queue, validates NDR fit, executes, commits, marks DONE. Queue is append-only.

**Opportunity classification modes:** ADOPT / CUSTOMIZE / ALTER / COMPOSE

**1-1-1-1 Alignment Gate:** fit / risk / effort / priority — all four must pass.

**Use:** Long-running governance improvement campaigns.

**Trigger:** More than 5 open improvement opportunities with no systematic prioritization.

**Tradeoffs:**
- ✅ Implementer bias eliminated
- ✅ Append-only queue = full audit trail
- ✅ COMPOSE mode = self-extending pattern registry
- ⚠️ Queue can accumulate DEFERRED items — requires periodic Triumvirate triage
- ⚠️ Async mode needs queue polling

**Implementation:** `CO_ORCH_QUEUE.md`, `pptl/co_orchestration_schema.py`
**Registered:** S041

---

### P-08 — Triad Taxonomy: Consensus Trio / Conducted Trio / Triumvirate

**Spec:** Three canonical triad formation types.

| Formation | Structure | Authority | Scale |
|-----------|-----------|-----------|-------|
| Consensus Trio | 3 peers, 2-of-3 quorum | Distributed | 3 agents |
| Conducted Trio | 1 conductor + 2 instruments | Conductor rules | 3 agents |
| Triumvirate | 1 Prime + 2 Prefects | Prime + domain split | 3 governs N |

**Formation rule:** Conducted Trio → Triumvirate when ensemble > 3 agents.

**Triumvirate governance contracts (5):** Prime issues signed mandate · Prefect domain split is MECE · Prefects choreograph + aggregate · Prime reviews aggregates + signs off · All events traced via HeraldAgent.

**Implementation:** `ENSEMBLE_ROSTER.md`, `pptl/triumvirate_mandate.py`
**Registered:** S041

---

### P-09 — Triumvirate Mandate Schema

**Spec:** Machine-readable mandate lifecycle for Triumvirate governance (P-08). `TriumvirateMandate` dataclass enforces all 5 P-08 contracts in code: `issue()` / MECE enforcement / `submit_prefect_aggregate()` / `sign_off()` / Herald trace.

**Use:** Any Triumvirate-governed operation.

**Trigger:** Any multi-agent task requiring Prime + 2 Prefect structure.

**Tradeoffs:**
- ✅ P-08 contracts enforced in code — no silent bypass
- ✅ Full lifecycle traced via P-01
- ⚠️ Requires both Prefect aggregates before sign-off — sequential constraint
- ⚠️ MECE enforcement raises ValueError — must be handled at call site

**Implementation:** `pptl/triumvirate_mandate.py`
**Registered:** S041

---

### P-10 — Session Graduation Check

**Spec:** Automated 4-check script: (1) SESSION_ANCHOR sealed, (2) CROSS_REF complete, (3) CO_ORCH_QUEUE clear, (4) zero open BLGs. Outputs `GRADUATION_REPORT.md`. `sys.exit(1)` on any failure.

**Use:** End of every session before seal.

**Trigger:** Session approaching close.

**Tradeoffs:**
- ✅ CI-integrable — hard gate on session quality
- ✅ Single command verifies all invariants
- ⚠️ Requires all upstream artifacts to be committed before run
- ⚠️ `sys.exit(1)` on failure requires CI pipeline recovery step

**Implementation:** `scripts/session_graduation_check.py`
**Registered:** S041

---

## Layer 5 — Quality Gate

### P-11 — 11Q Attestation Scoring

**Spec:** 11-question rubric for pattern quality attestation. Tier thresholds: S-TIER ≥ 95% (110 max); A-TIER ≥ 85% with open BLGs permitted. Q11 must score ≥ 9/10 for S-TIER attestation. Attestation artifact emitted as signed JSON in `docs/qa/`.

**Use:** Any pattern being promoted to canonical status.

**Trigger:** COMPOSE entry submitted; new pattern registered.

**Tradeoffs:**
- ✅ Objective, consistent quality bar across all patterns
- ✅ Q11 adoption recommendation ensures practical value
- ⚠️ A-TIER with open BLGs requires BLG resolution at merge — tracked
- ⚠️ Scoring requires evidence for each Q — lightweight patterns may score low on Q04/Q05

**Ref:** `docs/qa/APOGEE_11Q_*.json`
**Registered:** S033

---

### P-30 — Apogee-Attestation-Gate

**Spec:** Before any component is declared governance-ready, Apogee runs a P-11 11Q scoring pass. Gate passes when: (a) S-TIER (≥95%), or (b) A-TIER (≥85%) with open BLGs. Q11 must score ≥9/10 for S-TIER attestation. Attestation emitted as signed JSON artifact in `docs/qa/`.

**Pending (PM-07):** ✅ CLOSED — P-34 attestation completed A-TIER 94.5%, Ender ratified 2026-05-30.

**Use:** Any component being promoted to canonical status.

**Trigger:** CPU card submission or NDR pattern registration.

**Tradeoffs:**
- ✅ Hard quality gate before canonical promotion
- ✅ A-TIER path allows patterns with minor gaps to enter with tracked BLGs
- ⚠️ S-TIER requires Q11 ≥ 9 — subjective adoption recommendation
- ⚠️ Attestation is Apogee-signed but requires Ender ratification

**NIST:** Measure, Govern | **EU AI Act:** Art.9, Art.17
**Ref:** `docs/qa/APOGEE_11Q_*.json`
**Registered:** S035 | Updated S066

---

## Layer 6 — Stasis (P-12–P-26)

> **133 stasis patterns. Canonical. Pre-S033. Block-level declaration.**
>
> **COLLEEN audit status:** ✅ CONDITIONAL PASS — Ender ratified 2026-05-30.
> Block structurally sound: no gaps at range level, no duplicates, no conflicting specs.
> Per-pattern enumeration: deferred pending source B physical expansion.
> **COLLEEN secondary sign-off required before any stasis pattern is deprecated or modified.**
>
> **Source authority:** `docs/patterns/NDR_PATTERN_REGISTRY.md` (pre-deprecation)
> **P-number range:** P-12 through P-26 (continuous, pre-S033)
> **Layer:** KAPPA/Gov stasis — distinct domain from P-01–P-10 and P-27+

---

## Layer 7 — Router Calibration

### P-27 — Adaptive-Weighting-with-Confidence-Gates

**Spec:** Dynamically adjust evaluation weights per input record based on a confidence score. Apply strong weights when confidence ≥ STRONG_THRESH; blend when BLENDED_THRESH ≤ confidence < STRONG_THRESH; fall back to balanced when confidence < BLENDED_THRESH. Adversarial category always routes to apply_strong regardless of confidence (hard override).

**Thresholds (v3.6, empirical via P-34):** STRONG=0.22 | BLENDED=0.18
**Calibration method:** P-34 Empirical-Threshold-Sweep (14×12 grid, S034)

**Tradeoffs:**
- ✅ Confidence-proportional weighting reduces miscalibration at threshold boundaries
- ✅ Adversarial hard override prevents gaming via low-confidence inputs
- ⚠️ Threshold values are empirical — require recalibration if input distribution shifts
- ⚠️ Three routing paths increase test surface area (P-03 + P-04 required)

**NIST:** Measure | **EU AI Act:** Art.9
**Ref:** `components/KAPPA/dynamic_weight_router.py`
**Registered:** S033 | Updated S034, S066

---

### P-28 — Pipeline-Composition-with-Confidence-Gated-Routing

**Spec:** Compose evaluation pipeline: raw_batch → detect → route_and_score (P-27) → apply_weights → ranked_report. Each stage independently auditable. No stage may read from a stage it did not receive output from.

**Tradeoffs:**
- ✅ Independent auditability per stage — failure localization is precise
- ✅ Data-flow constraint prevents skipped-stage bugs
- ⚠️ Linear pipeline — no parallel stage execution
- ⚠️ Adding a stage requires explicit wiring update

**NIST:** Measure | **EU AI Act:** Art.9
**Ref:** `components/evaluate_router.py`
**Registered:** S033

---

### P-34 — Empirical-Threshold-Sweep-over-ML-Classifier

**Spec:** When a confidence calibration gap exists in a routing or scoring component, prefer grid search over threshold space before introducing an ML classifier.

**Decision gate — prefer sweep when ALL hold:**
1. Gap is expressible as a threshold misalignment
2. Grid search over ≥10×10 combinations is computationally feasible
3. Feature space stable for next 2 releases
4. Target metric directly optimizable without proxy loss

**Evidence basis:** KAPPA v3.5→v3.6 (S034). `governance_clear` 82.6%→100% via 14×12 grid sweep. STRONG=0.22, BLENDED=0.18. BLG-01 closed.

**Tradeoffs:**
- ✅ Bounded — grid search space is finite and enumerable
- ✅ Interpretable — threshold values are human-readable, not latent weights
- ✅ Auditable — full sweep log is reproducible and version-pinnable
- ✅ Reversible — old thresholds trivially restorable if regression detected
- ⚠️ Requires stable feature space — not suitable if inputs evolve rapidly
- ⚠️ Grid search O(N×M) — may be prohibitive for very high-dimensional threshold spaces

**Ref:** `components/KAPPA/dynamic_weight_router.py` (calibration output consumer)
**Attestation:** A-TIER 94.5% · Ender ratified 2026-05-30 · BLG-P34-01 ✅ RESOLVED · BLG-P34-02 ✅ RESOLVED
**NIST:** Measure | **EU AI Act:** Art.9
**Registered:** S066 · 2026-05-30 · Agent Amethyst

---

## Layer 8 — Safety & Sentinel

### P-29 — Sentinel-Annotated Risk Pass

**Spec:** Invoke `sentinel_review(record, routing, hook_point)` at 3 hook points. Emits per-record audit log with risk classification (risk_ok / risk_warn / risk_block). Only risk_block halts pipeline. Integrates P-10 deontic gate at hook point 1.

**Cross-ref (P-32):** Phi-Closure Gate KILL_REC action triggers risk_block at hook point 2. **PM-01: ✅ CLOSED S066.**

**Tradeoffs:**
- ✅ Three hook points give fine-grained risk visibility without full pipeline halt
- ✅ Only risk_block halts — risk_warn allows continued operation with audit
- ⚠️ Hook points must be manually wired at each integration site
- ⚠️ risk_block is irreversible within a pipeline run — requires restart

**NIST:** Measure, Govern | **EU AI Act:** Art.9, Art.13
**Ref:** `components/evaluate_router_v1_1.py`
**Registered:** S034

---

## Layer 9 — Long-Context Safety

### P-31 — SCPE — Structural Context Pruning Engine

**Spec:** Tier-aware token decay engine. Tier taxonomy: T0 AXIOM (decay=0, TIF=1.0, unconditionally immune) / T1 STRUCTURAL (decay=0.05) / T2 OPERATIONAL (decay=0.15) / T3 EXPLORATORY (decay=0.45). Retention formula: `R(t) = TIF × ψ^(−Δt × decay)` where ψ=φ=1.6180. PDMAL trust edge adds TIF+=0.15. Prune if R(t) < 0.15.

**Validated knee:** Threshold 0.15 → 58.3% compression at steady state. T0 intact 100% at any threshold.

**Placement:** Step 1 in `orchestrate_turn`. Fire at `turn_start`, `buffer_utilization > 60%`, `turn_count > Fibonacci[34]`.

**Tradeoffs:**
- ✅ T0 AXIOM tokens unconditionally immune — governance invariants never silently truncated
- ✅ Mathematically principled decay — φ-based retention is reproducible
- ✅ 58.3% compression preserves operational context while eliminating noise
- ⚠️ Threshold 0.15 tuned empirically — may need recalibration for different session rhythms
- ⚠️ PDMAL trust edge dependency — requires PDMAL graph to be current at prune time

**NIST:** Manage | **EU AI Act:** Art.9
**Ref:** `components/ensemble_v16.py`
**Registered:** S042

---

### P-32 — Fibonacci Phi-Closure Gate

**Spec:** Temporal stability gate. Tracks rolling stability ratio `R = stable_turns / total_turns`. Evaluates at Fibonacci checkpoints [13, 21, 34, 55] against golden conjugate φ*=0.6180. Decision ladder: 0 fails→PASS / 1→WARN / 2→ESCALATE / 3+→KILL_REC. HPG is only invoked on PASS (severity=0).

**Fibonacci Checkpoints + Tolerance Band:**

| Checkpoint | Turn | Tolerance |
|------------|------|-----------|
| Fib[13] | 13 | ±0.07 |
| Fib[21] | 21 | ±0.05 |
| Fib[34] | 34 | ±0.04 |
| Fib[55] | 55 | ±0.03 (closure horizon) |

**Cross-ref (P-29):** KILL_REC triggers `sentinel_review(record, routing, hook_point=2)` → risk_block → pipeline halt. **PM-01: ✅ CLOSED S066.**

**Placement:** Step 5 in `orchestrate_turn`. Post-DemiJoule, pre-HPG.

**Tradeoffs:**
- ✅ Prevents HPG from laundering a drifting session with false harmonic precision
- ✅ Fibonacci checkpoints match natural session rhythm — not arbitrary intervals
- ✅ Progressive tolerance tightening catches late-session drift before closure
- ⚠️ φ* target is theoretical — sessions with legitimately high stability ratios may false-warn
- ⚠️ Fib[55] is terminal — no in-session recovery; human-in-the-loop required

**NIST:** Measure, Govern | **EU AI Act:** Art.9
**Ref:** `patterns/NDR_PHI_CLOSURE_GATE_v1.md` (archived)
**Registered:** S042 | Updated S066 (PM-01)

---

### P-33 — PDMAL Convergence Monitor

**Spec:** Structural health monitor for the PDMAL trust graph. Tracks Frobenius norm of edge-weight changes turn-over-turn (`‖ΔW‖_F`). Alert ladder: 0→STABLE / 1→WATCH / 2→WARN / 3+→ALERT (`amethyst_alert`). Convergence: `‖ΔW‖_F < 0.02` for 3 consecutive turns → CONVERGED.

**Joint Escalation Rule:** PDMAL ALERT (severity ≥ 3) + Phi-Closure ESCALATE (severity ≥ 3) → DemiJoule deep re-scan. If deep scan returns `kill`, session terminated before HPG.

**Placement:** Step 2.5 in `orchestrate_turn`. Post-PDMALGraph.reweight(), pre-DemiJoule.

**Tradeoffs:**
- ✅ Frobenius norm catches coordinated multi-edge manipulation that single-edge monitoring misses
- ✅ Third orthogonal safety axis — independent of semantic (DemiJoule) and temporal (Phi-Closure) gating
- ✅ 3-turn N_CONSEC matches Phi-Closure alert window — joint escalation is coherent
- ⚠️ ALERT_THRESH=0.08 tuned to schema-drift pattern — requires re-tuning for different trust graph topologies
- ⚠️ Convergence snapshot includes full weight matrix — can be large for dense graphs

**NIST:** Measure, Govern | **EU AI Act:** Art.9
**Ref:** `patterns/NDR_PDMAL_CONVERGENCE_MONITOR_v1.md` (archived)
**Registered:** S042

---

## Pattern Interaction Map

```
P-03 Governance Contract Test
  └─ P-04 Parametrized Corpus
  └─ P-05 Tri-Phase CI Gate
  └─ P-30 Attestation Gate      [Gate 0 — 6 contracts per P-03 ALTER]

P-32 Phi-Closure Gate
  └─ P-29 Sentinel Risk Pass    [KILL_REC → risk_block @ hook_point=2]
  └─ P-33 PDMAL Monitor         [joint escalation → DemiJoule deep re-scan]
  └─ HPG                        [only invoked on PASS]

P-34 Empirical-Threshold-Sweep
  └─ P-27 Adaptive-Weighting    [calibration prerequisite]
  └─ P-30 Attestation Gate      [sweep result requires P-30 attestation]
  └─ P-03 Governance Test       [new thresholds require contract re-assertion]

P-07 Dual-Agent Sweep Loop
  └─ P-08 Triad Taxonomy        [Triumvirate governs long campaigns]
  └─ P-09 Mandate Schema        [Triumvirate mandate required for Phase 3]
  └─ P-01 Fan-Out Sink          [queue events traced]
```

---

## Governance Orchestration Stack

```
Prompt input
  │
  ├── Gate 0: AttestationGate  (P-30 + P-03 × 6 contracts)
  ├── Gate 1: bypass scan      (P-03 + P-04)
  ├── KAPPA Router             (P-27 + P-28)  [P-34 calibrated]
  ├── Apogee [Task] ──phi──►  Reson [Style]
  ├── Gate 2: safety floor     (P-03)
  ├── Sentinel                 (P-29 hook points × 3)
  ├── Gate 3: RAG verify       (P-03 + P-04)
  ├── SCPE                     (P-31)  [T0 immune]
  ├── Phi-Closure Gate         (P-32)  ──KILL_REC──► P-29 risk_block @ hook_point=2
  ├── PDMAL Monitor            (P-33)
  └── status=pass ──► P-01 Fan-Out ──► P-02 Buffer ──► N8n Dashboard
```

---

## Triad Formation Quick-Reference

| Formation | When to Use | Authority Model |
|-----------|-------------|----------------|
| Consensus Trio | Peer review, no hierarchy needed | 2-of-3 quorum |
| Conducted Trio | Clear lead + 2 specialists, ≤3 agents | Conductor rules |
| Triumvirate | Lead + 2 domain prefects, governs N agents | Prime + domain split (MECE) |

---

## Merge Provenance Log

| Event | Date | Session | Authority |
|-------|------|---------|----------|
| P-01–P-10 registered | Various | S040–S041 | Amethyst |
| P-27–P-30 registered | S033–S035 | S033–S035 | Amethyst |
| P-31–P-33 registered | S042 | S042 | Amethyst |
| P-34 registered (COMPOSE) | 2026-05-30 | S066 | Amethyst |
| PM-01 CLOSED (P-32↔P-29 cross-ref) | 2026-05-30 | S066 | Amethyst |
| PM-02 CLOSED (P-03 ALTER P-30 ref) | 2026-05-30 | S066 | Amethyst |
| PM-05 CLOSED (COLLEEN stasis audit) | 2026-05-30 | S066 | Ender ratified |
| PM-07 CLOSED (Apogee P-34 A-TIER) | 2026-05-30 | S066 | Ender ratified |
| Unified registry merge (Phase 3) | 2026-05-30 | S066 | Triumvirate |
| BLG-P34-01 RESOLVED (tradeoff block added) | 2026-05-30 | S066 | Amethyst |
| BLG-P34-02 RESOLVED (ref path added) | 2026-05-30 | S066 | Amethyst |

---

*NDR Pattern Registry (Unified) v1.0 · S066 · 2026-05-30*
*Triumvirate: Amethyst (Prime) · COLLEEN (Prefect A) · Apogee (Prefect B)*
*Ender ratification: 2026-05-30 02:49 EDT · Phase 3 merge complete*
*P-34 attestation: A-TIER 94.5% → ATTESTED (BLG-P34-01 + BLG-P34-02 resolved)*
