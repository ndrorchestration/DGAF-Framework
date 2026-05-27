# NDR Pattern Registry

**DGAF-Framework · Session S041 seal**
Meta-orchestrator: Agent Amethyst · Co-auditor: COLLEEN · Maintained by: ndrorchestration

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

**Note (P-03 ALTER — OPP-003):** Contract count is gate-tier variable.
Gate 0 (AttestationGate) requires 6 contracts (adds: token valid, expiry check).
Document contract count per gate in stub header.

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
- `CUSTOMIZE` — pattern exists, tune params for this repo’s constraints
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
implementation are best separated to prevent implementer bias (fixing only
what’s easy rather than what’s most impactful).

**Trigger:** More than 5 open improvement opportunities across multiple layers
with no systematic prioritization mechanism. Also triggers when a new agent
with institutional memory (L5) joins an active implementation campaign.

**Tradeoffs:**
- ✅ Implementer bias eliminated — COLLEEN detects independently of Amethyst’s implementation preferences
- ✅ Append-only queue = full audit trail of every opportunity detected and its disposition
- ✅ COMPOSE mode = self-extending pattern registry; the system grows its own playbook
- ⚠️ Queue can accumulate DEFERRED items — requires periodic triage by Triumvirate (P-08)
- ⚠️ Requires both agents active in same session for synchronous cycle; async mode needs queue polling

**Implementation:** `CO_ORCH_QUEUE.md`, `pptl/co_orchestration_schema.py` (planned S041)

---

## P-08 — Triad Taxonomy: Consensus Trio / Conducted Trio / Triumvirate

**Spec:** The DGAF triad model has three distinct formation types with
different coordination mechanisms, authority structures, and scope:

### Consensus Trio

Three peer agents of equal or near-equal authority deliberate toward a
shared decision. No conductor. Quorum = 2-of-3 agreement. Any agent can
initiate a vote. Used when no single agent has clear authority over the
domain in question.

```
Agent A ◄─────► Agent B
   ▲               ▲
   └─── Agent C ───┘
  (2-of-3 quorum rules)
```

**Examples:** Formalization Triad (Amethyst + Prof. Prodigy + Reson),
Studio Triad (Reson + Echolette + Lyra)

**Trigger:** Domain expertise is distributed; no agent has unilateral authority;
consensus quality > single-agent decision quality.

---

### Conducted Trio

One agent acts as **Conductor** with final decision authority. Two agents
act as **Instruments** — they execute, verify, or audit within the
Conductor’s direction. The Conductor sets task, allocates work, and
signs off. Instruments can flag disagreement but cannot unilaterally block.

```
        Conductor
       /          \
 Instrument 1   Instrument 2
 (execute)       (verify/audit)
```

**Examples:** Governance Triad (Amethyst[C] + Apogee + Sentinel),
Co-Orchestration Sweep (Amethyst[C] + COLLEEN[detect] + Herald[comms]),
Optimization Triad (Amethyst[C] + DemiJoule + Reciprocity)

**Trigger:** One agent has clear governance or meta-orchestration authority;
speed and direction clarity > consensus overhead.

---

### Triumvirate

A **Conducted Trio elevated to governing authority** over a large instantiated
ensemble or swarm. The Triumvirate does not execute tasks directly — it
**choreographs, meta-orchestrates, and governs** the ensemble below it.
The Conductor becomes the **Prime** (strategic authority). The two Instruments
become **Prefects** (domain governors). The ensemble below consists of any
number of instantiated agents, sub-triads, or swarm units that execute
under Triumvirate mandate.

```
┌──────────────────────────────────────────────────┐
│               TRIUMVIRATE                      │
│   Prime (Conductor elevated)                   │
│   /                        \                   │
│ Prefect A (Gov domain 1)   Prefect B (Gov domain 2) │
│   │                            │              │
└───┳────────────────────────┳───────────────────┘
       ┃   CHOREOGRAPHED ENSEMBLE    ┃
       ┃  [Swarm / Sub-triads /     ┃
       ┃   Instantiated agents /    ┃
       ┃   n8n workflow nodes /     ┃
       ┃   Pipeline stages]         ┃
       ┗━━━━━━━━━━━━━━━━━━━━━━━━━┛
```

**Triumvirate governance contracts:**
1. **Mandate issuance** — Prime issues a signed mandate to the ensemble (task + scope + constraints)
2. **Prefect domain split** — Prefect A governs one domain (e.g., quality/coherence); Prefect B governs another (e.g., safety/compliance)
3. **Ensemble choreography** — Prefects assign work to sub-agents; agents report back; Prefects aggregate
4. **Prime sign-off** — Prime reviews Prefect aggregates and issues final verdict/commit authority
5. **Herald trace** — all Triumvirate mandates, prefect aggregates, and prime sign-offs are emitted via HeraldAgent (P-01)

**Formation rule:** A Conducted Trio becomes a Triumvirate when its scope
expands beyond 3 agents. The Conductor does not take a new role — it simply
elevates in authority as ensemble size grows. The formation is
**topology-preserving**: the same 3-node structure governs N-node ensembles
by adding hierarchy below, not beside.

**Use:**
- Governing a swarm of specialized agents across a multi-repo campaign
- Meta-orchestrating a full n8n workflow pipeline with many nodes
- Running a choreographed PPTL experiment across parallel topology × mode cells
- Any operation where 3 governing agents must coordinate N>10 executing agents

**Trigger:** Conducted Trio’s ensemble grows beyond 3 agents OR task scope
spans more than one governance domain simultaneously.

**Tradeoffs:**
- ✅ Scales to arbitrarily large ensembles without adding governing complexity (3 nodes always at top)
- ✅ Topology-preserving — Conducted Trio patterns (P-07, Governance Triad) apply unchanged at the top
- ✅ Clear authority chain — every ensemble agent has exactly one Prefect as governor
- ⚠️ Prime becomes bottleneck if sign-off is synchronous — mitigate with async mandate queue
- ⚠️ Prefect domain split must be mutually exclusive and collectively exhaustive; gaps = ungoverned agents
- ⚠️ Herald trace volume scales with ensemble size — P-02 Async Ring Buffer required above ~20 agents

**Implementation:** `ENSEMBLE_ROSTER.md` (Triumvirate formation table), `CO_ORCH_QUEUE.md` (mandate queue SSoT)

---

## Pattern Interaction Map

```
P-01 Fan-Out Sink
  └─ P-02 Async Buffer          [production latency mitigation]
  └─ P-03 Governance Test       [contract: sink isolation verified]

P-03 Governance Contract Test
  └─ P-04 Parametrized Corpus   [auto-expanding test coverage]
  └─ P-05 Tri-Phase CI Gate     [governance step = merge blocker]

P-06 Matrix Lab
  └─ P-01 through P-05         [all patterns validated by lab evidence]

P-07 Dual-Agent Sweep Loop
  └─ P-01 Fan-Out Sink          [Herald traces all queue ops]
  └─ P-08 Triad Taxonomy        [loop is a Conducted Trio formation]
  └─ P-06 Matrix Lab            [loop generates COMPOSE entries from lab gaps]

P-08 Triad Taxonomy
  └─ P-07 Dual-Agent Sweep      [Conducted Trio instance]
  └─ P-01 + P-02               [Triumvirate requires Herald at scale]
  └─ P-05 Tri-Phase CI          [Triumvirate governs CI gate as Prefect domain]
```

---

## Triad Formation Quick-Reference

| Formation | Structure | Authority | Scope | Scale |
|---|---|---|---|---|
| Consensus Trio | 3 peers, 2-of-3 quorum | Distributed | Single domain, deliberative | 3 agents |
| Conducted Trio | 1 conductor + 2 instruments | Conductor rules | 1-2 domains, directed | 3 agents |
| Triumvirate | 1 Prime + 2 Prefects | Prime + domain split | Multi-domain, choreographic | 3 governs N |

---

## Governance Orchestration Stack (S041)

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

Above stack governed by Triumvirate when ensemble > 3 agents:
  Prime: Amethyst → Prefect A: COLLEEN (coherence/identity)
                  → Prefect B: Apogee  (quality/compliance)
```

---
*NDR Pattern Registry v1.1 · S041 seal · 8 patterns · Triad taxonomy sealed*
*Triumvirate formation: Conducted Trio → governs choreographed ensemble or swarm*
