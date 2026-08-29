# DGAF v1 File-Tree and Ownership Plan

**Status:** IMPLEMENTATION IN PROGRESS / NON-AUTHORIZING

This is the canonical physical-placement and ownership map for the viable v1 Governed Recursive Control Plane. It extends existing DGAF/PPTL boundaries rather than creating a parallel runtime tree.

## Target tree

```text
DGAF-Framework/
├── .github/workflows/
│   ├── pptl-ci.yml
│   └── control-plane-contract.yml
├── docs/architecture/
│   ├── DGAF_V1_CONTROL_PLANE_INTEGRATION.md
│   └── DGAF_V1_FILE_TREE_PLAN.md
├── docs/governance/                 # existing governance/evidence records
├── docs/experiment/                 # PDMAL experiment only
├── docs/evidence/                   # evidence indexes/artifacts
└── pptl/
    ├── orchestrator.py
    ├── triadic_governance_loop.py
    ├── procluding_premise.py
    ├── co_orchestration_schema.py
    ├── herald_agent.py
    ├── sinks.py
    ├── governance_envelope.py
    ├── control_plane.py
    ├── state_identity.py
    ├── branch_registry.py
    ├── budget_ledger.py
    └── commit_gate.py
```

## Ownership

| Capability | Canonical implementation | Integration | Test/CI |
|---|---|---|---|
| Governance Envelope | `pptl/governance_envelope.py` | controller/orchestrator | `test_v1_control_plane.py` |
| Lifecycle controller | `pptl/control_plane.py` | orchestrator + TGL | same |
| State identity | `pptl/state_identity.py` | controller | same |
| Branch provenance | `pptl/branch_registry.py` | controller + Herald | same + evidence |
| Resource accounting | `pptl/budget_ledger.py` | controller/dispatch | same |
| Plan/commit barrier | `pptl/commit_gate.py` | controller/tool adapters | same |
| Per-turn governance | `pptl/triadic_governance_loop.py` | controller | existing TGL suite |
| Constitutional admission | `pptl/procluding_premise.py` | TGL/controller | P-35 tests |

## Canonical ownership rules

One concept has one canonical schema and one semantic owner. Do not duplicate TGL gate semantics or create another recursive engine.

```text
GovernanceEnvelope -> one schema
TaskState -> one transition table
BranchRecord -> one schema
BudgetLedger -> one ledger contract
CommitRequest -> one authorization contract
```

## Current implementation candidate

The integration branch contains the first executable v1 contract layer: GovernanceEnvelope, ControlTask/ControlPlane/TaskState, StateRegistry, BudgetLedger, BranchRecord/BranchRegistry, CommitRequest/CommitGate, deterministic tests, dedicated contract CI, and package exports.

These remain candidate implementation changes until CI/adversarial evidence closes the corresponding engineering predicates.

## Cross-repository boundary

`ndrorchestration/agent-control-plane` remains a separate experimental asset. Its lifecycle, dispatch, policy, evaluation, and provenance components are reference material for contract comparison, not an implicit dependency. Any extraction or reuse requires explicit ownership and compatibility review.

## PDMAL boundary

```text
DGAF control plane
      |
      +--> governed adapter
               |
               +--> PDMAL experiment
```

The generic control plane must operate without PDMAL. v1 work must not alter PDMAL candidate identity, freeze state, authorization, protocol, or empirical N.

## CI boundary

`pptl-ci.yml` remains the per-turn governance lane. `control-plane-contract.yml` is the deterministic v1 control-plane lane. Neither lane is an authorization mechanism.

## Future PR admission

Every new v1 module must specify its owner path, contract, reused components, invariants, failure behavior, provenance fields, test/CI lane, documentation owner, and PDMAL-boundary impact.
