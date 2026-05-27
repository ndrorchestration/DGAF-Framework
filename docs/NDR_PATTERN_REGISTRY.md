# NDR Pattern Registry

**DGAF-Framework · Session S040 seal**
Meta-orchestrator: Agent Amethyst · Maintained by: ndrorchestration

---

> NDR Patterns are reusable, named orchestration/governance constructs with a
> canonical spec, trigger condition, and known tradeoff profile. They are the
> building blocks of the DGAF multi-agent governance stack.

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

**Use:** CI merge gate. Any PR touching gate logic, threshold values, or event
emission order must pass all `governance` tests before merge.

**Trigger:** Adding a new gate, modifying a gate threshold, changing event
type names, or altering downstream execution flow.

**Tradeoffs:**
- ✅ Catches silent regressions where status string changes but behavior doesn’t
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
Adding a signal to the source auto-expands the test suite with zero test-code
changes.

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
verifiable from functional behavior. Separating governance into its own CI step
makes it a named, auditable gate — not a subset of a general test run.

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
  1. Topology ranking (mean composite per topology across all modes)
  2. Mode ranking (mean composite per mode across all topologies)
  3. Interaction heatmap (topology × mode grid)
  4. Triadic lift (mean difference: triadic modes vs non-triadic per topology)
  5. Noise resilience curves (composite vs noise level per topology × mode)

**Use:** Any governance architecture decision requiring empirical differentiation
between structural topology choices and orchestration control patterns —
specifically when both topology and orchestration interact and both need justification.

**Trigger:** Topology choice disputed, new orchestration mode proposed,
or noise resilience requirements need quantification.

**Tradeoffs:**
- ✅ Evidence-based architecture decisions — topology choice is justified, not assumed
- ✅ Interaction effects surface topology × mode combinations that are non-obvious
- ⚠️ Simulation results depend on scoring model validity — calibrate against real LLM runs
- ⚠️ Combinatorial explosion at high N/M/K — fix topology after Phase 1 to reduce search space

**Implementation:** `pptl/experiments/h4_task_stratified.py`, PPTL Phase 1 lab results

---

## Pattern Interaction Map

```
P-01 Fan-Out Sink
  └─ P-02 Async Buffer        [production latency mitigation]
  └─ P-03 Governance Test     [contract: sink isolation verified]

P-03 Governance Contract Test
  └─ P-04 Parametrized Corpus  [auto-expanding test coverage]
  └─ P-05 Tri-Phase CI Gate   [governance step = merge blocker]

P-06 Matrix Lab
  └─ P-01 through P-05        [all patterns validated by lab evidence]
```

---

## Governance Orchestration Stack (S040)

```
Prompt input
  │
  ├── Gate 1: bypass scan  (case-insensitive, P-03 + P-04)
  │     └─ input_vetoed → Herald emit → Fan-Out (P-01)
  │
  ├── Apogee [Task]   ────phi───→ Reson [Style]
  │     └─ llm_call event        └─ judge_call event
  │
  ├── Gate 2: safety floor  (per-round, rounds 1–3)
  │     └─ output_vetoed → Herald emit → Fan-Out (P-01)
  │
  ├── Sentinel [Safety]  ─── Gate 3: RAG verify (P-03 + P-04)
  │     └─ output_vetoed → Herald emit → Fan-Out (P-01)
  │
  └── status=pass → Herald emit → Fan-Out → N8nHeraldSink (P-02) → Dashboard
```

---
*NDR Pattern Registry v1.0 · S040 seal · 6 patterns · Phi-pentagon topology confirmed dominant*
