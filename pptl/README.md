# PPTL Python Harness

**Phi-Pentagon Topology Lab — Multi-Agent Governance Harness**
DGAF-governed · Agent Amethyst meta-orchestrated · NDR pattern registry

![pptl-ci](https://github.com/ndrorchestration/DGAF-Framework/actions/workflows/pptl-ci.yml/badge.svg)

---

## Module Map

| Module | Role | Size |
|--------|------|------|
| `topology.py` | PHI constant, pentagon edge weights, Triad-C role map | 1.1 KB |
| `herald_agent.py` | `HeraldAgent` — trace sink + audit fan-out | 7.3 KB |
| `sinks.py` | `JSONLSink`, `StdoutSink`, `N8nWebhookSink` | 5.7 KB |
| `n8n_herald_sink.py` | Production `N8nHeraldSink` — batching, retry, HMAC, dead-letter | new |
| `rag_verifier.py` | `SentinelRAGVerifier` — DemiJoule RAG hallucination check | 3.4 KB |
| `orchestrator.py` | `IntegratedOrchestrator` — Triad-C 3-gate stack | 5.4 KB |

---

## Quick Start

```python
from pptl import (
    HeraldAgent, JSONLSink, StdoutSink,
    SentinelRAGVerifier, IntegratedOrchestrator
)
from pptl.n8n_herald_sink import N8nHeraldSink
import os

herald = HeraldAgent(session_id="sess_001")
herald.register_sink(JSONLSink("output/herald_audit.jsonl"))
herald.register_sink(StdoutSink())
herald.register_sink(N8nHeraldSink(
    webhook_url = os.environ["HERALD_N8N_WEBHOOK_URL"],
    batch_size  = 20,
    dry_run     = False,
))

orch = IntegratedOrchestrator(
    herald   = herald,
    verifier = SentinelRAGVerifier(),
)

result = orch.run(
    task_id = "T001",
    prompt  = "Analyze phi-pentagon governance implications.",
)
print(result["status"])   # "pass"
herald.close()
```

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

## Swap Real LLM

In `orchestrator.py`, replace `_mock_apogee()`:

```python
import anthropic
_client = anthropic.Anthropic()

def _mock_apogee(self, prompt: str, round_n: int) -> str:
    msg = _client.messages.create(
        model="claude-opus-4-5",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text
```

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

```bash
# Full suite
pytest pptl/tests/ -v

# CI-equivalent governance gate
pytest pptl/tests/ -m governance -v

# Hallu corpus
pytest pptl/tests/test_orchestrator.py -k "hallu_signal" -v

# Obfuscation strict
pytest pptl/tests/test_orchestrator.py -k "obfuscation_detected_strict" -v
```

| Module | Count | Markers |
|--------|-------|---------|
| `test_herald_agent.py` | 18 | `unit` |
| `test_sinks.py` | 10 | `unit`, `integration` |
| `test_topology.py` | 8 | `unit`, `governance` |
| `test_orchestrator.py` | ~166+ | `governance`, `integration` |

---

## Related Repos

- **Dashboard:** [pptl-governance-dashboard](https://github.com/ndrorchestration/pptl-governance-dashboard)
- **DGAF core:** [DGAF-Framework](https://github.com/ndrorchestration/DGAF-Framework)

---
*Session S040 — Triad-C stack · Herald trace · 3-gate governance · parametrized test corpora · tri-phase CI*
*NDR Patterns active: P-01 through P-06*
