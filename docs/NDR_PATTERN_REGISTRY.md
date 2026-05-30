# NDR Pattern Registry

**DGAF-Framework · Session S066 update (base: S041 seal)**
Meta-orchestrator: Agent Amethyst · Co-auditor: COLLEEN · Maintained by: ndrorchestration

---

> NDR Patterns are reusable, named orchestration/governance constructs with a
> canonical spec, trigger condition, and known tradeoff profile. They are the
> building blocks of the DGAF multi-agent governance stack.

> **Registry status (S066):** P-01–P-10 are full-spec canonical patterns held in
> this file. P-11–P-30 are held in `docs/patterns/NDR_PATTERN_REGISTRY.md` (v2.2).
> P-31–P-33 are held as individual cards in `patterns/`. P-34 is a COMPOSE entry
> registered this session. A full unified merge is pre-planned in
> `docs/NDR_REGISTRY_MERGE_PLAN.md`. See also `docs/NDR_REGISTRY_DIFFERENTIATION.md`
> for authoritative registry map.

---

## P-01 — Fan-Out Trace Sink w/ Dead-Letter

**Spec:** `HeraldAgent` holds a list of registered `Sink` objects. On every
`emit()` call, it iterates all sinks, wraps each write in `try/except`, and
routes any failure to a dead-letter JSONL file. Sink failures are logged but
never re-raised. Downstream sinks always execute regardless of upstream failures.

**Use:** Any multi-agent system requiring audit trace across multiple
destinations (JSONL file, stdout, webhook, database) where a single sink
failure must not interrupt the trace pipeline.

**Trigger:** More than one sink registered; any sink does I/O.

**Tradeoffs:**
- ✅ Strong isolation — one bad sink cannot corrupt the audit record
- ✅ Dead-letter preserves all events for replay/backfill
- ⚠️ Fan-out is synchronous — latency = sum of all sink write times
- ⚠️ Dead-letter file must be monitored; silent accumulation is a hidden failure mode

**Implementation:** `pptl/herald_agent.py`, `pptl/sinks.py`

---

## P-02 — Async-Persist Ring Buffer

**Spec:** High-throughput trace events are written to an in-process ring buffer
(bounded `deque`). A background thread drains the buffer to persistent storage
(JSONL / DB) on a configurable interval or when buffer reaches capacity.
All write operations acquire a `threading.Lock`. On `close()`, the drain loop
flushes all remaining events before terminating.

**Use:** Production Herald deployments where sink I/O latency (disk, HTTP)
would otherwise block the main agent execution thread.

**Trigger:** `emit()` latency measured > 5ms in profiling; multi-threaded agent
workloads where trace emission must not introduce backpressure.

**Tradeoffs:**
- ✅ Decouples agent execution speed from sink I/O latency
- ✅ Bounded buffer prevents unbounded memory growth
- ⚠️ Events in buffer are lost on hard process crash (mitigated by short drain interval)
- ⚠️ Adds background thread complexity; requires careful shutdown sequencing

**Implementation:** `pptl/n8n_herald_sink.py` (batch flush), `pptl/sinks.py`

---

## P-03 — Governance Contract Test

**Spec:** For every governance gate (Gate 1 input scan, Gate 2 safety score,
Gate 3 RAG verify), assert four contracts independently:
  1. Correct status string returned
  2. Correct `event_type` emitted to sinks
  3. Correct downstream execution state (rounds, llm_call count)
  4. Correct gate-specific invariant (e.g., `rounds == 0` for Gate 1,
     `rounds > 0` for Gate 3)

Each contract is a separate test function. All are marked
`@pytest.mark.governance`.

**Note (P-03 ALTER — OPP-003):** Contract count is gate-tier variable.
Gate 0 (AttestationGate / P-30 Apogee-Attestation-Gate) requires 6 contracts
(adds: token valid, expiry check). Document contract count per gate in stub header.
See **P-30** (`docs/patterns/NDR_PATTERN_REGISTRY.md`) for full AttestationGate spec.
**PM-02: ✅ CLOSED S066** — P-30 reference added to ALTER note.

**Use:** CI merge gate. Any PR touching gate logic, threshold values, or event
emission order must pass all `governance` tests before merge.

**Trigger:** Adding a new gate, modifying a gate threshold, changing event
type names, or altering downstream execution flow.

**Tradeoffs:**
- ✅ Catches silent regressions where status string changes but behavior doesn't
- ✅ Four-contract structure documents architectural invariants as executable code
- ⚠️ Requires fixture isolation (`fresh_orch` per test) — adds test count
- ⚠️ Must be updated when gate logic is intentionally changed

**Implementation:** `pptl/tests/test_orchestrator.py`

---

## P-04 — Parametrized Corpus

**Spec:** Signal lists (`BYPASS_SIGNALS`, `HALLU_SIGNALS`) are defined as
module-level constants in the production source (`rag_verifier.py`). Test files
import these constants and build parametrize inputs dynamically:
```python
BYPASS_CORPUS = [(sig, sig[:30].replace(" ", "_")) for sig in BYPASS_SIGNALS]
@pytest.mark.parametrize("signal,sig_id", BYPASS_CORPUS, ids=[b[1] for b in BYPASS_CORPUS])
```
Adding a signal to the source auto-expands the test suite with zero test-code changes.

**Use:** Any governance gate with an enumerable signal corpus. Obfuscation
variants are added as a second parametrize group with the same contract set.

**Trigger:** New signal added to `BYPASS_SIGNALS` or `HALLU_SIGNALS`. Also
triggered when a new bypass vector class is identified (e.g., Unicode homoglyphs,
base64 encoding).

**Tradeoffs:**
- ✅ Single source of truth — no drift between production signal list and test corpus
- ✅ Auto-expansion — new signals are tested immediately without PR to test file
- ⚠️ Test count scales linearly with corpus size — large corpora slow `unit` runs
- ⚠️ Obfuscation variants require manual curation; no automatic generation

**Implementation:** `pptl/tests/test_orchestrator.py`, `pptl/rag_verifier.py`

---

## P-05 — Tri-Phase CI Gate

**Spec:** GitHub Actions matrix with three named jobs: `unit`, `governance`,
`integration`. `fail-fast: false` ensures all three report independently.
Governance step is the designated merge blocker (branch protection rule).
Each step uploads a JUnit XML artifact for downstream reporting.

```yaml
strategy:
  fail-fast: false
  matrix:
    include:
      - step: unit
        markers: unit
      - step: governance
        markers: governance
      - step: integration
        markers: integration
```

**Use:** Any repo where governance contract correctness must be independently
verifiable from functional behavior.

**Trigger:** First PR touching gate logic, sink behavior, or signal corpora.
Activate branch protection rule on `governance` step immediately.

**Tradeoffs:**
- ✅ Governance failures are immediately locatable without re-running full suite
- ✅ `fail-fast: false` gives complete failure picture in one CI run
- ⚠️ 3× runner cost vs single step — acceptable given governance audit value
- ⚠️ Branch protection must be manually configured after workflow is merged

**Implementation:** `.github/workflows/pptl-ci.yml`

---

## P-06 — Topology × Orchestration Matrix Lab

**Spec:** Enumerate all `(topology, orchestration_mode)` cell combinations.
For each cell, run N seeds × M task families × K noise levels. Score each run
with a composite metric (governance-weighted). Report five canonical outputs:
  1. Topology ranking
  2. Mode ranking
  3. Interaction heatmap
  4. Triadic lift
  5. Noise resilience curves

**Use:** Any governance architecture decision requiring empirical differentiation
between structural topology choices and orchestration control patterns.

**Trigger:** Topology choice disputed, new orchestration mode proposed,
or noise resilience requirements need quantification.

**Tradeoffs:**
- ✅ Evidence-based architecture decisions
- ✅ Interaction effects surface non-obvious topology × mode combinations
- ⚠️ Simulation results depend on scoring model validity
- ⚠️ Combinatorial explosion at high N/M/K

**Implementation:** `pptl/experiments/h4_task_stratified.py`, PPTL Phase 1 lab results

---

## P-07 — Dual-Agent Persistent Sweep Loop

**Spec:** Two agents with separated **detect** and **implement** roles share
a markdown+JSON queue (`CO_ORCH_QUEUE.md`) as the persistent SSoT hand-off
substrate. The Detector (COLLEEN) scores each discovered opportunity through
a binary 4-gate alignment check (fit / risk / effort / priority). Passing
opportunities are classified into one of four implementation modes and written
to the queue. The Implementer (Amethyst) reads the queue, validates NDR fit,
executes the change, commits with SHA, and marks the entry `DONE`. The queue
is append-only — completed entries are archived, never deleted. New patterns
discovered during implementation are fed back as `COMPOSE` entries.

**Opportunity classification modes:**
- `ADOPT` — known NDR pattern, implement as-is
- `CUSTOMIZE` — pattern exists, tune params for this repo's constraints
- `ALTER` — pattern exists, modify trigger condition or scope
- `COMPOSE` — no covering pattern; Detector proposes spec, Implementer registers as P-N+

**1-1-1-1 Alignment Gate (COLLEEN):**
```
fit      — belongs in this repo/layer
risk     — CI-safe to implement
effort   — completable in ≤1 session
priority — unblocks something downstream
All four must pass; fail any → DEFERRED or REJECTED, never silent drop.
```

**Use:** Long-running governance improvement campaigns where detection and
implementation are best separated to prevent implementer bias.

**Trigger:** More than 5 open improvement opportunities across multiple layers
with no systematic prioritization mechanism.

**Tradeoffs:**
- ✅ Implementer bias eliminated
- ✅ Append-only queue = full audit trail
- ✅ COMPOSE mode = self-extending pattern registry
- ⚠️ Queue can accumulate DEFERRED items — requires periodic Triumvirate triage
- ⚠️ Async mode needs queue polling

**Implementation:** `CO_ORCH_QUEUE.md`, `pptl/co_orchestration_schema.py`

---

## P-08 — Triad Taxonomy: Consensus Trio / Conducted Trio / Triumvirate

**Spec:** Three canonical triad formation types. See full spec in ENSEMBLE_ROSTER.md.
Summary:

| Formation | Structure | Authority | Scale |
|---|---|---|---|
| Consensus Trio | 3 peers, 2-of-3 quorum | Distributed | 3 agents |
| Conducted Trio | 1 conductor + 2 instruments | Conductor rules | 3 agents |
| Triumvirate | 1 Prime + 2 Prefects | Prime + domain split | 3 governs N |

**Formation rule:** Conducted Trio → Triumvirate when ensemble > 3 agents.
Topology-preserving: 3-node structure governs N by adding hierarchy below.

**Triumvirate governance contracts (5):**
1. Prime issues signed mandate
2. Prefect domain split is MECE
3. Prefects choreograph + aggregate
4. Prime reviews aggregates + signs off
5. All events traced via HeraldAgent

**Implementation:** `ENSEMBLE_ROSTER.md`, `pptl/triumvirate_mandate.py` (P-09)

---

## P-09 — Triumvirate Mandate Schema

**Spec:** Machine-readable mandate lifecycle for Triumvirate governance (P-08).
`TriumvirateMandate` dataclass enforces the 5 P-08 contracts in code:

1. **`issue()`** — Prime issues mandate; emits `mandate_issued` to HeraldAgent
2. **MECE enforcement** — `__post_init__` raises `ValueError` if Prefect domains
   overlap or share agents; no ungoverned ensemble agents permitted
3. **`submit_prefect_aggregate(agent, report)`** — Prefect submits results;
   emits `prefect_aggregate`; raises if mandate not yet issued
4. **`sign_off(note)`** — Prime signs off after both Prefect aggregates received;
   raises if either Prefect has not submitted; emits `mandate_signed_off`
5. **Herald trace** — all 3 lifecycle events routed through P-01 Fan-Out Sink

```python
mandate = TriumvirateMandate(
    prime="Amethyst", task="S042 sweep",
    scope="DGAF-Framework", constraints=["CI green"],
    prefect_a=PrefectDomain("COLLEEN", "coherence", ["Herald", "Lyra"]),
    prefect_b=PrefectDomain("Apogee",  "quality",   ["Sentinel", "DemiJoule"]),
    herald=herald,
)
mandate.issue()
mandate.submit_prefect_aggregate("COLLEEN", "...")
mandate.submit_prefect_aggregate("Apogee",  "...")
mandate.sign_off("Cycle 2 complete")
```

**Implementation:** `pptl/triumvirate_mandate.py`

---

## P-10 — Session Graduation Check

**Spec:** Automated 4-check script verifying session is ready to graduate.
Checks:
1. SESSION_ANCHOR sealed
2. CROSS_REF complete
3. CO_ORCH_QUEUE clear
4. Zero open BLGs

Outputs `GRADUATION_REPORT.md`. `sys.exit(1)` on any failure — CI-integrable.

**Implementation:** `scripts/session_graduation_check.py`

---

## P-11 through P-30 — Cross-Reference Index

> Full specs held in `docs/patterns/NDR_PATTERN_REGISTRY.md` (v2.2, S066).

| Pattern | Name | Layer | Session | Ref |
|---------|------|-------|---------|-----|
| P-11 | 11Q Attestation Scoring | Quality gate | S033 | `docs/qa/` |
| P-12–P-26 | Stasis patterns | Various | Pre-S033 | `docs/patterns/` |
| P-27 | Adaptive-Weighting-with-Confidence-Gates | Router calibration | S033/S034 | `components/KAPPA/` |
| P-28 | Pipeline-Composition-with-Confidence-Gated-Routing | Pipeline | S033 | `components/evaluate_router.py` |
| P-29 | Sentinel-Annotated Risk Pass | Safety | S034 | `components/evaluate_router_v1_1.py` |
| P-30 | Apogee-Attestation-Gate | Quality / Gate 0 | S035 | `docs/qa/APOGEE_11Q_*.json` |

---

## P-31 through P-33 — Cross-Reference Index

| Pattern | Name | Layer | Session | Card |
|---------|------|-------|---------|------|
| P-31 | SCPE — Structural Context Pruning Engine | Long-context safety | S042 | `patterns/NDR_SCPE_v1.md` |
| P-32 | Phi-Closure Gate | Long-context drift | S042 | `patterns/NDR_PHI_CLOSURE_GATE_v1.md` |
| P-33 | PDMAL Convergence Monitor | Alignment drift detection | S042 | `patterns/NDR_PDMAL_CONVERGENCE_MONITOR_v1.md` |

---

## P-34 — Empirical-Threshold-Sweep-over-ML-Classifier *(COMPOSE — S066)*

**Spec:** When a confidence calibration gap exists in a routing or scoring
component, prefer grid search over threshold space before introducing an ML
classifier. A threshold sweep is: bounded, interpretable, auditable, and
reversible.

**Decision gate — prefer sweep when ALL hold:**
1. Gap is expressible as a threshold misalignment
2. Grid search over ≥10×10 combinations is computationally feasible
3. Feature space stable for next 2 releases
4. Target metric directly optimizable without proxy loss

**Evidence basis:** KAPPA v3.5 → v3.6 (S034). `governance_clear` 82.6% → 100%
via 14×12 grid sweep. STRONG=0.22, BLENDED=0.18. BLG-01 closed.

**Attestation:** PENDING — PM-07: P-30 Apogee attestation pass required.

**NIST:** Measure | **EU AI Act:** Art.9
**Registered:** S066 · 2026-05-30 · Agent Amethyst

---

## Pattern Interaction Map (S066 — PM-01 PM-02 CLOSED)

```
P-03 Governance Contract Test
  └─ P-04 Parametrized Corpus
  └─ P-05 Tri-Phase CI Gate
  └─ P-30 Attestation Gate      [Gate 0 — 6 contracts; see P-30 spec]

P-32 Phi-Closure Gate
  └─ P-29 Sentinel Risk Pass    [KILL_REC → risk_block @ hook_point=2]
  └─ P-33 PDMAL Monitor
  └─ HPG                        [only invoked on PASS]

P-34 Empirical-Threshold-Sweep
  └─ P-27 Adaptive-Weighting    [calibration prerequisite]
  └─ P-30 Attestation Gate      [sweep result requires P-30 attestation]
  └─ P-03 Governance Test       [new thresholds require contract re-assertion]
```

---

## Governance Orchestration Stack (S066 — PM-01 PM-02 CLOSED)

```
Prompt input
  │
  ├── Gate 0: AttestationGate  (P-30 + P-03 × 6 contracts)
  ├── Gate 1: bypass scan  (P-03 + P-04)
  ├── KAPPA Router (P-27 + P-28)  [P-34 calibrated]
  ├── Apogee [Task] ──phi──→ Reson [Style]
  ├── Gate 2: safety floor  (P-03)
  ├── Sentinel [P-29 hook points × 3]
  ├── Gate 3: RAG verify (P-03 + P-04)
  ├── SCPE (P-31)  [T0 immune]
  ├── Phi-Closure Gate (P-32)  ──KILL_REC──→ P-29 risk_block @ hook_point=2
  ├── PDMAL Monitor (P-33)
  └── status=pass → P-01 Fan-Out → P-02 Buffer → N8n Dashboard
```

---

*NDR Pattern Registry v1.4 · S066 (PM-01 PM-02 CLOSED) · P-01–P-10 full spec*
*P-11–P-34 cross-referenced · Merge pre-plan: docs/NDR_REGISTRY_MERGE_PLAN.md*
