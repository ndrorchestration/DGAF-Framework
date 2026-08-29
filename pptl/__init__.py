"""
PPTL — Phi-Pentagon Topology Lab
Multi-agent governance harness: HeraldAgent, TriadC orchestration,
DemiJoule RAG verification, DGAF gate stack.

DGAF-Framework governed · Agent Amethyst meta-orchestrated
"""
from .herald_agent        import HeraldAgent, TraceEventType
from .sinks               import JSONLSink, StdoutSink, N8nWebhookSink
from .n8n_herald_sink     import N8nHeraldSink          # OPP-005: production sink
from .rag_verifier        import SentinelRAGVerifier
from .topology             import PHI, PENTAGON_EDGES
from .attestation_gate    import (
    AttestationGate, AttestationRecord, AttestationResult, AttestationStatus,
)
from .co_orchestration_schema import (
    CoOrchQueue, Opportunity, AlignmentGate,
    load_queue, save_queue,
)
from .governance_envelope import GovernanceEnvelope, ResourceBudget
from .state_identity import StateRegistry, canonical_state, state_id
from .budget_ledger import BudgetLedger, Consumption, BudgetExceeded
from .branch_registry import BranchRecord, BranchRegistry
from .commit_gate import CommitGate, CommitDenied, CommitRequest
from .control_plane import ControlPlane, ControlPlaneViolation, ControlTask, TaskState

__version__ = "0.5.0"
__all__ = [
    # Herald
    "HeraldAgent", "TraceEventType",
    # Sinks
    "JSONLSink", "StdoutSink", "N8nWebhookSink", "N8nHeraldSink",
    # Governance
    "SentinelRAGVerifier",
    "AttestationGate", "AttestationRecord", "AttestationResult", "AttestationStatus",
    # Topology
    "PHI", "PENTAGON_EDGES",
    # Co-orchestration
    "CoOrchQueue", "Opportunity", "AlignmentGate", "load_queue", "save_queue",
    # V1 control plane
    "GovernanceEnvelope", "ResourceBudget",
    "StateRegistry", "canonical_state", "state_id",
    "BudgetLedger", "Consumption", "BudgetExceeded",
    "BranchRecord", "BranchRegistry",
    "CommitGate", "CommitDenied", "CommitRequest",
    "ControlPlane", "ControlPlaneViolation", "ControlTask", "TaskState",
]
