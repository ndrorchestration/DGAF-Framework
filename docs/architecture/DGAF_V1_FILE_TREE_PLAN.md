# DGAF v1 File-Tree and Ownership Plan

**Status:** IMPLEMENTATION CANDIDATE / NON-AUTHORIZING

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
├── docs/governance/
├── docs/experiment/
├── docs/evidence/
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
    ├── commit_gate.py
    └── tests/
        ├── test_v1_control_plane.py
        └── test_v1_tgl_integration.py
```

## Ownership

| Capability | Canonical implementation | Integration | Test/CI |
|---|---|---|---|
| Governance Envelope | `pptl/governance_envelope.py` | controller/orchestrator | `test_v1_control_plane.py` |
| Lifecycle controller | `pptl/control_plane.py` | orchestrator + TGL | `test_v1_control_plane.py` + TGL integration |
| State identity | `pptl/state_identity.py` | controller | `test_v1_control_plane.py` |
| Branch provenance | `pptl/branch_registry.py` | controller + Herald | `test_v1_control_plane.py` + evidence |
| Resource accounting | `pptl/budget_ledger.py` | controller/dispatch | `test_v1_control_plane.py` |
| Plan/commit barrier | `pptl/commit_gate.py` | controller/tool adapters | `test_v1_control_plane.py` |
| Per-turn governance | existing `pptl/triadic_governance_loop.py` | controller | existing TGL suite + `test_v1_tgl_integration.py` |
| Constitutional admission | existing `pptl/procluding_premise.py` | TGL/controller | P-35 tests + `test_v1_tgl_integration.py` |

## Canonical ownership rules

One concept has one canonical schema and one semantic owner. Do not duplicate TGL gate semantics or create another recursive engine.

## Current implementation candidate

The integration branch contains the first executable v1 contract layer: GovernanceEnvelope, ControlTask/ControlPlane/TaskState, StateRegistry, BudgetLedger/Consumption, BranchRecord/BranchRegistry, CommitRequest/CommitGate, deterministic tests, a TGL integration test, dedicated control-plane CI, and package exports.

The Governance Envelope now explicitly carries `max_depth` and `max_concurrency`; depth and risk inheritance are fail-closed. The controller can invoke a supplied TGL runner only from `EVALUATING`, and terminal TGL failure maps to lifecycle escalation.

These remain candidate implementation changes until CI and adversarial review close their corresponding engineering predicates.

## Cross-repository boundary

The separate `ndrorchestration/agent-control-plane` project is a reference/integration asset. Its lifecycle, dispatch, policy, evaluation, and provenance components can inform contract comparison, but DGAF does not depend on or silently copy that implementation.

## PDMAL boundary

```text
DGAF control plane
      |
      +--> governed adapter
               |
               +--> PDMAL experiment
```

The control plane must remain usable without PDMAL. No v1 implementation may alter PDMAL candidate identity, freeze state, authorization, or empirical N.

## CI boundary

`pptl-ci.yml` remains the per-turn governance lane. `control-plane-contract.yml` is the deterministic v1 control-plane lane and now executes both the core contract suite and the TGL integration suite. Neither workflow is an authorization mechanism.

## Admission rule

Every new v1 module must specify owner path, contract, reused components, invariants, failure behavior, provenance fields, test/CI lane, documentation owner, and PDMAL-boundary impact.

## Non-authorizing boundary

This plan does not create a freeze, authorize a pilot, change the PDMAL candidate boundary, or increase empirical N.
