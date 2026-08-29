# DGAF v1 File-Tree and Ownership Plan

**Status:** IMPLEMENTATION IN PROGRESS / NON-AUTHORIZING  
**Parent architecture:** `docs/architecture/DGAF_V1_CONTROL_PLANE_INTEGRATION.md`  
**Date:** 2026-08-29

This is the canonical physical-placement and ownership map for the viable v1 Governed Recursive Control Plane. It extends existing DGAF/PPTL boundaries rather than creating a parallel runtime tree.

## Target tree

```text
DGAF-Framework/
├── .github/
│   └── workflows/
│       ├── pptl-ci.yml
│       └── control-plane-contract.yml
├── docs/
│   ├── architecture/
│   │   ├── DGAF_V1_CONTROL_PLANE_INTEGRATION.md
│   │   ├── DGAF_V1_FILE_TREE_PLAN.md
│   │   └── [future distinct ADR/spec files only]
│   ├── governance/
│   ├── experiment/
│   └── evidence/
├── pptl/
│   ├── orchestrator.py
│   ├── triadic_governance_loop.py
│   ├── procluding_premise.py
│   ├── co_orchestration_schema.py
│   ├── herald_agent.py
│   ├── sinks.py
│   ├── governance_envelope.py
│   ├── control_plane.py
│   ├── state_identity.py
│   ├── branch_registry.py
│   ├── budget_ledger.py
│   └── commit_gate.py
└── scripts/
```

## Ownership matrix

| Capability | Canonical implementation | Existing integration | Test/evidence |
|---|---|---|---|
| Governance Envelope | `pptl/governance_envelope.py` | orchestrator/controller | `pptl/tests/test_v1_control_plane.py` |
| Lifecycle controller | `pptl/control_plane.py` | orchestrator + TGL | same contract suite |
| State identity | `pptl/state_identity.py` | controller | same contract suite |
| Branch provenance | `pptl/branch_registry.py` | controller + Herald | same contract suite + evidence layer |
| Resource accounting | `pptl/budget_ledger.py` | controller/dispatch | same contract suite |
| Plan/commit barrier | `pptl/commit_gate.py` | controller/tool adapters | same contract suite |
| Per-turn governance | existing `pptl/triadic_governance_loop.py` | controller | existing TGL tests |
| Constitutional admission | existing `pptl/procluding_premise.py` | TGL/controller | existing P-35 tests |

## Schema ownership rule

One concept has one canonical schema and one semantic owner. Adapters may serialize these contracts but may not redefine them.

```text
GovernanceEnvelope -> one schema
TaskState -> one transition table
BranchRecord -> one schema
BudgetLedger -> one ledger contract
CommitRequest -> one authorization contract
```

## Integration rules

- Extend `pptl/orchestrator.py`; do not create a second recursive runtime.
- Reuse TGL; do not duplicate gate semantics.
- Use Herald/sinks for publication rather than inventing a second evidence channel.
- Keep PDMAL below the generic control-plane boundary.
- Keep experimental evidence separate from engineering implementation evidence.

## Current implementation candidate

The integration branch now contains the first executable v1 contract layer:

- `GovernanceEnvelope` / `ResourceBudget`
- `ControlTask` / `ControlPlane` / `TaskState`
- `StateRegistry`
- `BudgetLedger` / `Consumption`
- `BranchRecord` / `BranchRegistry`
- `CommitRequest` / `CommitGate`
- deterministic contract tests
- dedicated control-plane CI
- package exports through `pptl.__init__`

These changes remain candidate implementation until CI and adversarial review close their corresponding engineering predicates.

## Cross-repository boundary

The separate `ndrorchestration/agent-control-plane` project is a reference/integration asset. Its existing task lifecycle, dispatch, policy, evaluation, and provenance components can inform contract comparison, but DGAF does not depend on or silently copy that implementation.

Potential later extraction:

```text
DGAF governance/evidence semantics
        |
        +--> reusable control-plane package
```

Extraction is not a v1 prerequisite.

## PDMAL boundary

```text
DGAF control plane
      |
      +--> governed adapter
               |
               +--> PDMAL experiment
```

The control plane must remain usable without PDMAL. No v1 implementation may alter PDMAL candidate identity, freeze state, authorization, or empirical N.

## CI

`pptl-ci.yml` remains the per-turn governance test lane. `control-plane-contract.yml` is the dedicated deterministic v1 contract lane. Neither workflow is an authorization mechanism.

## Admission checklist

Every future v1 implementation PR must specify its owner path, contract, reused existing components, invariants, failure behavior, provenance fields, test/CI lane, documentation owner, and any effect on the PDMAL candidate boundary.
