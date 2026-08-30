"""PPTL — Phi-Pentagon Topology Lab and DGAF governance harness."""
from .herald_agent import HeraldAgent, TraceEventType
from .sinks import JSONLSink, StdoutSink, N8nWebhookSink
from .n8n_herald_sink import N8nHeraldSink
from .rag_verifier import SentinelRAGVerifier
from .topology import PHI, PENTAGON_EDGES
from .attestation_gate import AttestationGate, AttestationRecord, AttestationResult, AttestationStatus
from .co_orchestration_schema import CoOrchQueue, Opportunity, AlignmentGate, load_queue, save_queue
from .governance_envelope import GovernanceEnvelope, ResourceBudget
from .state_identity import StateRegistry, canonical_state, state_id
from .budget_ledger import BudgetLedger, Consumption, BudgetExceeded
from .branch_registry import BranchRecord, BranchRegistry
from .commit_gate import CommitGate, CommitDenied, CommitRequest
from .control_plane import ControlPlane, ControlPlaneViolation, ControlTask, TaskState

__version__ = "0.5.0"
__all__ = [
    "HeraldAgent", "TraceEventType", "JSONLSink", "StdoutSink", "N8nWebhookSink", "N8nHeraldSink",
    "SentinelRAGVerifier", "AttestationGate", "AttestationRecord", "AttestationResult", "AttestationStatus",
    "PHI", "PENTAGON_EDGES", "CoOrchQueue", "Opportunity", "AlignmentGate", "load_queue", "save_queue",
    "GovernanceEnvelope", "ResourceBudget", "StateRegistry", "canonical_state", "state_id",
    "BudgetLedger", "Consumption", "BudgetExceeded", "BranchRecord", "BranchRegistry",
    "CommitGate", "CommitDenied", "CommitRequest", "ControlPlane", "ControlPlaneViolation", "ControlTask", "TaskState",
]
