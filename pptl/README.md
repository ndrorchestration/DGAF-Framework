# PPTL Python Harness

**Phi-Pentagon Topology Lab (PPTL)** is a Python harness for experimenting with agent orchestration, topology, trace capture, and project-defined governance controls.

PPTL is an implementation and experimentation surface. Passing tests establish behavior for the tested contracts; they do not by themselves establish real-world safety, performance, or efficacy.

## What is here

| Module | Role |
|---|---|
| `topology.py` | Topology constants and role-map utilities |
| `herald_agent.py` | `HeraldAgent` trace collection and sink fan-out |
| `sinks.py` | JSONL, stdout, and webhook sink implementations |
| `n8n_herald_sink.py` | Webhook sink with batching, retry, authentication, and failure handling |
| `rag_verifier.py` | Project-defined RAG verification utilities |
| `orchestrator.py` | Integrated orchestration flow |

## Quick start

```python
from pptl import HeraldAgent, JSONLSink, StdoutSink, SentinelRAGVerifier, IntegratedOrchestrator

herald = HeraldAgent(session_id="example")
herald.register_sink(JSONLSink("output/herald_audit.jsonl"))
herald.register_sink(StdoutSink())

orchestrator = IntegratedOrchestrator(
    herald=herald,
    verifier=SentinelRAGVerifier(),
)

result = orchestrator.run(
    task_id="example",
    prompt="Analyze a topology question.",
)
print(result["status"])
herald.close()
```

For external integrations, configure credentials through environment variables or the deployment's secret-management mechanism. Do not place credentials in source files or documentation examples intended for production use.

## Testing

```bash
# Full suite
pytest pptl/tests/ -v

# Project-defined governance-marked tests
pytest pptl/tests/ -m governance -v
```

Test names and markers describe repository-local contracts. Inspect the relevant test and implementation before treating a result as evidence for a broader claim.

## Design notes

The harness emphasizes a few engineering properties:

- ordered control checks where ordering is part of the tested contract;
- isolated trace sinks so one sink failure can be handled without silently losing unrelated traces;
- centralized signal corpora to reduce divergence between implementation and tests;
- explicit failure handling and retained diagnostics;
- reproducible test execution for supported environments.

These are design goals and tested behaviors, not universal guarantees.

## Related documentation

- [DGAF technical reference](../README.technical.md)
- [Current project state](../docs/CURRENT_STATE.md)
- [Evidence ladder policy](../docs/evidence/EVIDENCE_LADDER_POLICY.md)
- [Legacy documentation status policy](../docs/governance/LEGACY_DOCUMENTATION_STATUS_POLICY.md)

## Related projects

- urlPPTL governance dashboardhttps://github.com/ndrorchestration/pptl-governance-dashboard
- urlDGAF-Frameworkhttps://github.com/ndrorchestration/DGAF-Framework
