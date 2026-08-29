# DGAF v1 File-Tree and Ownership Plan

**Status:** IMPLEMENTATION IN PROGRESS / NON-AUTHORIZING  
**Parent architecture:** `docs/architecture/DGAF_V1_CONTROL_PLANE_INTEGRATION.md`  
**Date:** 2026-08-29

## Purpose

This file is the concrete placement map for implementing the viable v1 control-plane additions inside the existing DGAF repository. It is intentionally narrower than a full architecture specification.

The governing principle is **extend existing boundaries before creating new ones**.

## Target tree

```text
DGAF-Framework/
├── .github/
│   └── workflows/
│       ├── pptl-ci.yml
│       └── control-plane-contract.yml                 # v1 contract lane
├── docs/
│   ├── architecture/
│   │   ├── DGAF_V1_CONTROL_PLANE_INTEGRATION.md
│   │   ├── DGAF_V1_FILE_TREE_PLAN.md
│   │   └── [future distinct ADR/spec files only]
│   ├── governance/
│   │   ├── P1_TO_P9_EVIDENCE_MATRIX.md
│   │   ├── TGL_PR132_ADVERSARIAL_REVIEW_*.md
│   │   └── [existing governance records]
│   ├── experiment/
│   │   ├── PDMAL_EXPERIMENT_PROTOCOL.md
│   │   └── [PDMAL experimental records]
│   └── evidence/
│       └── [claim/evidence indexes and retained artifacts]
├── pptl/
│   ├── __init__.py
│   ├── procluding_premise.py
│   ├── triadic_governance_loop.py
│   ├── orchestrator.py
│   ├── co_orchestration_schema.py
│   ├── herald_agent.py
│   ├── sinks.py
│   ├── governance_envelope.py                     # v1 implemented
│   ├── control_plane.py                            # v1 implemented
│   ├── state_identity.py                           # v1 implemented
│   ├── branch_registry.py                          # v1 implemented
│   ├── budget_ledger.py                            # v1 implemented
│   └── commit_gate.py                              # v1 implemented
├── scripts/
│   ├── [claim/evidence validators]
│   └── [future control-plane validators]
└── tests/
    └── [repository-level integration tests as conventions require]
```

## Ownership matrix

| Capability | Canonical implementation location | Primary existing integration | Evidence/test location |
|---|---|---|---|
| Governance envelope | `pptl/governance_envelope.py` | `pptl/orchestrator.py` | `pptl/tests/test_v1_control_plane.py` |
| Lifecycle controller | `pptl/control_plane.py` | `pptl/orchestrator.py` + TGL | `pptl/tests/test_v1_control_plane.py` |
| State identity / cycle detection | `pptl/state_identity.py` | controller | `pptl/tests/test_v1_control_plane.py` |
| Branch registry/provenance | `pptl/branch_registry.py` | controller + Herald | `pptl/tests/test_v1_control_plane.py` |
| Resource ledger | `pptl/budget_ledger.py` | controller + dispatch | `pptl/tests/test_v1_control_plane.py` |
| Plan/commit barrier | `pptl/commit_gate.py` | controller + tool adapters | `pptl/tests/test_v1_control_plane.py` |
| Per-turn gate semantics | existing `pptl/triadic_governance_loop.py` | controller | existing TGL tests |
| Constitutional admission | existing `pptl/procluding_premise.py` | TGL/controller | existing P-35 tests |
| Evidence publication | existing `pptl/herald_agent.py`, `pptl/sinks.py` | branch registry/TGL | evidence layer |
| P1–P9 governance status | existing docs | release/evidence process | governance docs |
| PDMAL experiment | existing `pptl/experiments/` + `docs/experiment/` | governed adapter only | candidate-scoped evidence |

## Module boundaries

### `governance_envelope.py`

Owns validation and immutable representation of inherited authority, tool, data, policy, and resource scope.

Must not own prompting, experiment statistics, deployment credentials, or autonomous authorization outside the explicit commit contract.

### `control_plane.py`

Owns lifecycle states and legal transitions.

It may be integrated with TGL, but must not duplicate TGL gate definitions.

### `state_identity.py`

Owns canonicalization and stable identity for detecting repeated/equivalent orchestration states.

It must not infer semantic truth from identity alone.

### `branch_registry.py`

Owns branch lineage and retained branch artifacts.

It is append-oriented and retains rejected, correlated, escalated, and vetoing records.

### `budget_ledger.py`

Owns reservations, consumption, release, and overrun decisions.

It measures actual telemetry. Pricing is optional reporting metadata.

### `commit_gate.py`

Owns proposal-to-action separation.

It accepts only an explicitly authorized `CommitRequest` and never infers authorization from a model response.

## Existing-file modification policy

Prefer minimal modifications to:

- `pptl/orchestrator.py` for lifecycle integration;
- `pptl/co_orchestration_schema.py` if existing schema fields can be extended rather than duplicated;
- `pptl/herald_agent.py` / `pptl/sinks.py` only where new branch provenance must be published;
- existing TGL code only when a new lifecycle invariant genuinely crosses the per-turn boundary.

Do not fork or copy TGL semantics into a second controller.

Do not create another recursive-engine implementation beside `orchestrator.py`.

## Schema ownership rule

There must be one canonical definition for each concept:

```text
GovernanceEnvelope -> one schema
Task/Lifecycle State -> one transition table
BranchRecord -> one schema
BudgetLedger -> one ledger contract
CommitRequest -> one authorization contract
```

Adapters may serialize/deserialize these structures, but they must not redefine their semantics.

## Test placement

### Unit tests

The first executable contract suite is centralized in:

```text
pptl/tests/test_v1_control_plane.py
```

It currently covers scope inheritance, budget reservation failure, deterministic state identity, branch retention, explicit commit authorization, lifecycle transitions, illegal transitions, and child derivation.

Additional module-local tests may be split out later when the test surface becomes large enough to justify it.

### Deterministic harness

The first harness uses mocks and fixed telemetry. It does not require live model calls, external credentials, or the PDMAL experimental candidate.

## CI placement

The existing `PPTL CI` workflow remains the per-turn governance test lane.

The new `DGAF v1 Control-Plane Contract` workflow is the dedicated control-plane contract lane and currently covers the deterministic v1 suite. It must remain independent of PDMAL experimental authorization.

Future extensions should cover:

1. schema/contract validation;
2. lifecycle transition tests;
3. scope inheritance;
4. budget reservation atomicity;
5. cycle detection;
6. veto propagation;
7. commit-gate enforcement;
8. deterministic trace reconstruction.

## Documentation ownership

| Document | Canonical purpose | Update trigger |
|---|---|---|
| `DGAF_V1_CONTROL_PLANE_INTEGRATION.md` | Architecture and v1 boundary | architecture change |
| `DGAF_V1_FILE_TREE_PLAN.md` | Physical placement and module ownership | tree/module change |
| `CURRENT_STATE.md` | Current status and evidence boundary | verified state change |
| `P1_TO_P9_EVIDENCE_MATRIX.md` | Predicate closure/evidence | predicate evidence change |
| `DGAF_RELATED_WORK_MATRIX.md` | Prior-art/comparative map | new relevant prior art |
| `DGAF_RECURSIVE_REFINEMENT_ANALYSIS.md` | Historical/design rationale | substantive refinement model change |
| `DEFERRED_ITEMS.md` | Explicitly postponed scope | defer/admit decision |

The v1 integration documents must not become substitutes for current-state or evidence records.

## Cross-repository boundary

The separate `ndrorchestration/agent-control-plane` repository is an existing experimental implementation asset. Its current implementation includes a task lifecycle object, deterministic capability dispatch, policy decision hooks, provenance events, and evaluation hooks. It explicitly states that it is not a complete governance or production-ready platform. These components may inform DGAF contracts, but are not automatically imported or treated as equivalent. 

The v1 implication is:

| ACP capability already present | DGAF v1 relationship |
|---|---|
| `Task` identity/lifecycle | candidate source material for DGAF `TaskState` contract |
| `ControlPlane` dispatch | candidate source material for lifecycle controller boundaries |
| policy decision hooks | compatible with Governance Envelope policy evaluation |
| provenance events | candidate input to BranchRecord/evidence lineage |
| evaluation hooks | compatible with deterministic verification harness |

Potential future extraction direction:

```text
DGAF governance/evidence semantics
        |
        +--> reusable control-plane package
                    |
                    +--> DGAF runtime
                    +--> other governed agent systems
```

Extraction is a later architectural decision, not a v1 prerequisite.

## PDMAL boundary

PDMAL-specific experimental code stays below the control-plane boundary.

```text
DGAF control plane
    |
    +--> governed adapter
             |
             +--> PDMAL experimental topology
```

The control plane must be able to operate without PDMAL. PDMAL must never become a hidden dependency of generic governance contracts.

## Planning hygiene rules

1. One concept, one canonical schema.
2. One lifecycle controller.
3. One TGL implementation.
4. Extend existing documents before creating new ones.
5. Keep experimental, governance, and implementation evidence distinct.
6. Never use documentation lineage as apparatus identity.
7. Never copy historical code into a new implementation merely because it is easier to reference.
8. Every new module requires tests before live-provider integration.
9. Every new workflow must have a defined evidence purpose.
10. Speculative topology or mathematical features remain research lanes unless independently validated and explicitly promoted.

## Implementation status

The v1 contract layer currently exists on the integration branch:

- `GovernanceEnvelope` / `ResourceBudget`
- `StateRegistry`
- `BudgetLedger` / `Consumption`
- `BranchRecord` / `BranchRegistry`
- `CommitRequest` / `CommitGate`
- `ControlTask` / `ControlPlane` / `TaskState`
- deterministic contract tests
- dedicated control-plane CI workflow
- package-level exports through `pptl.__init__`

These are **candidate implementation changes**, not yet independently verified as merged `main` capabilities.

## Non-authorizing status

This planning/implementation artifact does not modify candidate identity, freeze state, authorization state, or empirical N.
