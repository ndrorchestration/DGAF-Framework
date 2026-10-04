# PPTL Python Harness

**Phi-Pentagon Topology Lab — Multi-Agent Governance Harness**
DGAF-governed · functional authority resolves through the role/capability registry · NDR pattern registry

![pptl-ci](https://github.com/ndrorchestration/DGAF-Framework/actions/workflows/pptl-ci.yml/badge.svg)

---

## Compatibility identity boundary

The names `Apogee`, `Reson`, `Sentinel`, `DemiJoule`, and `Herald` in the PPTL topology are **stable experimental/compatibility node identifiers**. They are retained because experiment fixtures, routing tests, and APIs consume them as treatment/node labels. They do **not** create current governance authority.

Current executable authority resolves through `governance/role_capability_registry.v1.json`; identity lineage resolves through `governance/persona_role_lineage.v1.json`. In particular, bare `Sentinel` remains a historical/compatibility label and must not be interpreted as an active authority seat. Any future node rename requires explicit compatibility and experiment-equivalence evidence rather than bulk textual substitution.

---

## Module Map

| Module | Role | Size |
|--------|------|------|
| `topology.py` | PHI constant, pentagon edge weights, Triad-C role map | 1.1 KB |
| `herald_agent.py` | `HeraldAgent` — trace sink + audit fan-out | 7.3 KB |
| `sinks.py` | `JSONLSink`, `StdoutSink`, `N8nWebhookSink` | 5.7 KB |
| `n8n_herald_sink.py` | Production `N8nHeraldSink` — batching, retry, HMAC, dead-letter | new |
| `rag_verifier.py` | `SentinelRAGVerifier` — DemiJoule RAG hallucination check | 3.4 KB |
| `orchestrator.py` | `IntegratedOrchestrator` — config-first adapter over canonical TGL | current |

---

## Quick Start

The authoritative IntegratedOrchestrator API is configuration-first and wraps
the canonical TriadicGovernanceLoop turn contract:

```python
from pptl.orchestrator import IntegratedOrchestrator, OrchestratorConfig

config = OrchestratorConfig(
    session_id="sess_001",
    domain="general",
    dry_run=True,
)
orch = IntegratedOrchestrator(config)

result = orch.orchestrate_turn(
    "Analyze phi-pentagon governance implications.",
    turn_id="T001",
)

print(result.tgl_passed)
print(result.final_status)
print(result.gate_records)
print(result.response)
```

The default wrapper wires only the premise hook. Unwired required TGL gates
produce `ESCALATE`: `tgl_passed=False`, `response=None`, and an explicit
`blocked_reason`, with gate records retained. `final_status` preserves the
TGL verdict. Fully wired `PASS` and the existing `WARN` policy permit the
placeholder response; `KILL`, `KILL_REC`, and `ESCALATE` do not. These wrapper
results do not grant execution authority. The optional trailing status field
keeps existing positional `TurnResult` construction compatible; manually
constructed legacy results may have `final_status=None`.

Custom P-35 premise predicates use the canonical signature
`(input_text, invariant) -> bool`, where `True` means the invariant is
satisfied and `False` causes a fail-fast premise violation. The built-in
credit and justice signal corpora are detection predicates and are adapted to
this satisfaction contract by IntegratedOrchestrator.

The historical injected-Herald/RAG constructor and `orch.run(...)` API are
retired and are not compatibility entry points.

---

## Wire to Live Dashboard

```bash
# 1. Set env var
export HERALD_N8N_WEBHOOK_URL=https://your-dashboard.vercel.app/api/herald-ingest
export HERALD_N8N_HMAC_SECRET=your-hmac-secret-here

# 2. Run with live sink (dry_run=False in N8nHeraldSink)
python -m pptl.experiments.h4_task_stratified

# 3. Backfill Postgres from existing audit JSONL
INGEST_URL=https://your-dashboard.vercel.app/api/herald-ingest \
npx ts-node ../../pptl-governance-dashboard/scripts/replay-jsonl.ts \
  output/herald_audit.jsonl
```

---

## Extending the governed turn

IntegratedOrchestrator is a convenience adapter over the canonical
TriadicGovernanceLoop. Provider/model execution is not implicitly injected by
the wrapper. Add or replace model-facing behavior through separately governed
TGL hooks/adapters and preserve the gate, evidence, and authority contracts.

Do not restore the retired `_mock_apogee()` / `orch.run()` examples as a
provider integration path.

---

## Orchestration Best Practices (S040)

1. **Gate order is load-bearing** — Gate 1 (input scan) must precede Gate 2 (safety score) must precede Gate 3 (RAG verify). Reordering breaks H3/H4 contract tests.
2. **Case-insensitive signal scan** — always `prompt.lower()` before substring match. Mixed-case obfuscation is the most common real-world bypass vector.
3. **Sink isolation** — `HeraldAgent` must catch per-sink exceptions and route to dead-letter. One crashing sink must never block trace emission to others.
4. **Single source of truth for signal corpora** — `BYPASS_SIGNALS` and `HALLU_SIGNALS` live in `rag_verifier.py` only. Tests import from there; never duplicate in test files.
5. **Parametrize over corpora, not instances** — `@pytest.mark.parametrize` over the corpus list. Adding a signal to the source auto-expands the test suite with zero test-code changes.
6. **Phi edge weights are architectural constants** — `PENTAGON_EDGES` in `topology.py` is the only source. Routing tests assert exact float equality from that source.
7. **Fresh fixture per test** — `fresh_orch` fixture recreates `HeraldAgent` + `CaptureSink` per test function. No shared state across parametrize runs.
8. **Governance marker = merge gate** — `@pytest.mark.governance` tests are the CI blocker. `unit` and `integration` are informational on first failure.
9. **Tri-phase CI matrix** — `unit → governance → integration`, `fail-fast: false`. All three report independently so regressions are locatable without re-running.
10. **Dead-letter sink** — all production sinks (JSONL, n8n) must write failed events to a dead-letter file. Events must never be silently dropped.

---

## NDR Pattern Registry (S040)

| # | Pattern Name | Gate/Layer | Trigger |
|---|---|---|---|
| P-01 | Fan-Out Trace Sink w/ Dead-Letter | Herald | Any multi-sink audit requirement |
| P-02 | Async-Persist Ring Buffer | Sinks | High-throughput trace with I/O latency |
| P-03 | Governance Contract Test | Test | Any gate with enumerable signal corpus |
| P-04 | Parametrized Corpus | Test | New signal added to source list |
| P-05 | Tri-Phase CI Gate | CI | First PR touching gate or sink logic |
| P-06 | Topology × Orchestration Matrix Lab | Experiment | Topology/mode choice needs empirical evidence |

Full specs: [`docs/NDR_PATTERN_REGISTRY.md`](../docs/NDR_PATTERN_REGISTRY.md)

---

## Test Suite

The required `PPTL CI` context executes the complete current PPTL suite after
installing the repository's hash-locked Python-3.12 dependency set.

```bash
PYTHONPATH=. python -m pytest pptl/tests -q
```

Key current contracts include:

- `test_orchestrator_tgl.py` — Config + `orchestrate_turn()` wrapper contract.
- `test_triadic_governance_loop.py` — canonical TGL sequencing/status/seal behavior.
- `test_procluding_premise.py` — P-35 invariant-satisfaction predicate semantics.
- `test_n8n_herald_sink.py` — Herald `emit` protocol, batching, retry, and dead-letter behavior.
- v1 control-plane/TGL/adversarial/capability/seal suites.

The removed `test_orchestrator.py` suite belonged to the retired
injected-Herald/RAG `run()` architecture and is not part of the current API.

---

## Related Repos

- **Dashboard:** [pptl-governance-dashboard](https://github.com/ndrorchestration/pptl-governance-dashboard)
- **DGAF core:** [DGAF-Framework](https://github.com/ndrorchestration/DGAF-Framework)

---
*Session S040 — Triad-C stack · Herald trace · 3-gate governance · parametrized test corpora · tri-phase CI*
*NDR Patterns active: P-01 through P-06*
