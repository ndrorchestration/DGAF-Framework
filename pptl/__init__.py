"""
PPTL — Phi-Pentagon Topology Lab
Multi-agent governance harness: HeraldAgent, TriadC orchestration,
DemiJoule RAG verification, DGAF gate stack.

DGAF-Framework governed · Agent Amethyst meta-orchestrated
"""
from .herald_agent   import HeraldAgent, TraceEventType
from .sinks          import JSONLSink, StdoutSink, N8nWebhookSink
from .rag_verifier   import SentinelRAGVerifier
from .orchestrator   import IntegratedOrchestrator
from .topology       import PHI, PENTAGON_EDGES

__version__ = "0.3.0"
__all__ = [
    "HeraldAgent", "TraceEventType",
    "JSONLSink", "StdoutSink", "N8nWebhookSink",
    "SentinelRAGVerifier",
    "IntegratedOrchestrator",
    "PHI", "PENTAGON_EDGES",
]
