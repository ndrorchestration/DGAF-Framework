# PPTL Python Harness

**Phi-Pentagon Topology Lab — Multi-Agent Governance Harness**
DGAF-governed · Agent Amethyst meta-orchestrated · NDR pattern registry

---

## Module Map

| Module | Role |
|--------|------|
| `topology.py` | PHI constant, pentagon edge weights, Triad-C role map |
| `herald_agent.py` | `HeraldAgent` — trace sink + audit fan-out |
| `sinks.py` | `JSONLSink`, `StdoutSink`, `N8nWebhookSink` |
| `rag_verifier.py` | `SentinelRAGVerifier` — DemiJoule RAG hallucination check |
| `orchestrator.py` | `IntegratedOrchestrator` — Phase 3C full Triad-C stack |

## Quick Start

```python
from pptl import (
    HeraldAgent, JSONLSink, StdoutSink, N8nWebhookSink,
    SentinelRAGVerifier, IntegratedOrchestrator
)

herald = HeraldAgent(session_id="sess_001")
herald.register_sink(JSONLSink("output/herald_audit.jsonl"))
herald.register_sink(StdoutSink())
herald.register_sink(N8nWebhookSink(
    webhook_url = "https://your-dashboard.vercel.app/api/herald-ingest",
    dry_run     = False,
))

orch = IntegratedOrchestrator(
    herald     = herald,
    rag_scorer = SentinelRAGVerifier(),
)

result = orch.run(
    task_id = "T001",
    prompt  = "Analyze phi-pentagon governance implications.",
)
print(result["status"])   # "pass"

herald.close()
```

## Wire to Live Dashboard

```bash
export HERALD_N8N_WEBHOOK_URL=https://your-dashboard.vercel.app/api/herald-ingest
# In code: dry_run=False in N8nWebhookSink
# Replay existing audit JSONL to backfill Postgres
INGEST_URL=https://your-dashboard.vercel.app/api/herald-ingest \
npx ts-node ../../pptl-governance-dashboard/scripts/replay-jsonl.ts \
  output/herald_audit.jsonl
```

## Swap Real LLM

In `orchestrator.py`, replace `_mock_task_llm()`:

```python
import anthropic
client = anthropic.Anthropic()

def _mock_task_llm(self, prompt: str) -> str:
    msg = client.messages.create(
        model="claude-opus-4-5",
        max_tokens=512,
        messages=[{"role": "user", "content": prompt}],
    )
    return msg.content[0].text
```

## Related Repos

- **Dashboard:** [pptl-governance-dashboard](https://github.com/ndrorchestration/pptl-governance-dashboard)
- **DGAF core:** [DGAF-Framework](https://github.com/ndrorchestration/DGAF-Framework)

---
*Phase 3C — Herald trace sink + n8n webhook + Postgres fan-out*
*NDR Patterns: Fan-Out Trace Sink w/ Dead-Letter, Async-Persist Ring Buffer*
