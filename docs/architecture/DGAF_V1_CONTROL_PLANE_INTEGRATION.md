# DGAF v1 — Governed Recursive Control Plane Integration

**Status:** IMPLEMENTATION CANDIDATE / NON-AUTHORIZING  
**Date:** 2026-08-29

DGAF v1 incorporates the viable implementation-oriented subset of the Governed Recursive Lattice / compiler-trace architecture as a generic control plane. It is designed to make recursive multi-agent work bounded, auditable, provenance-preserving, and resistant to authority escalation or action leakage.

## Canonical v1 model

```text
GovernanceEnvelope
       |
       v
ControlPlane / TaskState
       |
       +--> bounded child derivation
       +--> StateRegistry / cycle detection
       +--> BudgetLedger
       +--> BranchRegistry
       +--> CommitGate
       |
       v
existing TGL / P-35 governance
       |
       v
optional execution substrate (including PDMAL)
```

## Implemented v1 contracts

- `pptl/governance_envelope.py` — immutable inherited authority/tool/data/resource scope, including bounded depth/concurrency metadata and non-increasing risk.
- `pptl/state_identity.py` — canonical state representation and SHA-256 identity for exact cycle detection.
- `pptl/budget_ledger.py` — fail-closed reservation, actual resource consumption accounting, and explicit active-concurrency accounting.
- `pptl/branch_registry.py` — append-oriented branch lineage and retained outcome metadata.
- `pptl/commit_gate.py` — explicit proposal/authorization/commit boundary.
- `pptl/control_plane.py` — deterministic lifecycle state machine, bounded child creation, lineage-wide concurrency enforcement, budget-overrun escalation, and optional TGL invocation from `EVALUATING`.
- `pptl/tests/test_v1_control_plane.py` — deterministic core contract tests, including negative authorization and concurrency cases.
- `pptl/tests/test_v1_tgl_integration.py` — cross-module TGL/control-plane contract tests.
- `.github/workflows/control-plane-contract.yml` — dedicated contract CI lane covering both suites.

These modules are implementation candidates on the current integration branch; their existence is not itself evidence of merge-level verification.

## Governance invariants

1. Child authority/tool/data scope cannot exceed parent scope.
2. Child budget cannot exceed parent budget.
3. Child risk tier cannot increase.
4. Child recursion depth cannot exceed the parent envelope ceiling.
5. Illegal lifecycle transitions fail closed.
6. Hard vetoes escalate rather than being averaged away or recursively bypassed.
7. Exact repeated states cannot recurse indefinitely.
8. Rejected/correlated/escalated/vetoing branch evidence remains retained.
9. Consequential actions require explicit authorization.
10. Generic control-plane lifecycle cannot bypass TGL/P-35.
11. Semantic distance or agent consensus is not treated as proof of independence.
12. PDMAL topology and harmonic/geometric motifs are not authorization signals.
13. Active concurrency is accounted separately from node counts and is bounded across a recursive lineage.
14. A task marked `COMMIT_READY` does not itself execute a side effect; execution remains behind `CommitGate` and explicit authorization.

## Typed branch roles

The initial role contracts are:

- `EXPLOIT` — improve the strongest current candidate;
- `DIVERGE` — generate a materially different alternative;
- `VERIFY` — challenge claims, evidence, premises, and contradictions;
- `GOVERN` — check authority, safety, policy, budget, and action constraints.

These are role contracts, not guarantees of independent reasoning.

## Lifecycle state machine

```text
RECEIVED
   -> PREFLIGHT
   -> ADMITTED
   -> EXPANDING / EVALUATING
   -> MERGE_READY
   -> COMMIT_READY
   -> TERMINATED

Governed failures may enter ESCALATED; ESCALATED -> TERMINATED.
```

`COMMIT_READY` only means the lifecycle has passed its controller checks. The consequential side effect remains owned by `CommitGate` and its explicit authorization artifact.

## Resource accounting

The v1 ledger is telemetry-based. It tracks input tokens, output tokens, tool calls, elapsed time, rounds, and nodes. Reservations are atomic within the ledger object; an over-budget reservation fails closed. Active concurrency is tracked independently from node counts, and the control plane enforces a root-lineage ceiling while each task ledger records its own acquired slot. Provider pricing is not part of the safety boundary.

`max_depth` and `max_concurrency` are envelope constraints. The current implementation explicitly accounts for active branch slots and releases them on task termination. Distributed scheduling remains outside the deterministic kernel.

## TGL relationship

The lifecycle controller and TGL have different scopes:

- **Lifecycle controller:** governs whether a task may exist, expand, recur, merge, escalate, terminate, or enter commit.
- **TGL:** governs the ordered gate evaluation inside an execution turn.
- **P-35:** remains the constitutional Layer-0 gate.
- **Herald:** remains evidence/fan-out infrastructure and must remain on the correct side of the sealed audit boundary.

No replacement of TGL is proposed. A TGL result is interpreted only from the `EVALUATING` state, and terminal `KILL`/`ESCALATE` outcomes cannot be converted into commit readiness by the generic controller.

## Evidence and provenance model

Every branch should produce one durable `BranchRecord` containing branch identity, parent lineage, role, state identity, claims, evidence identifiers, assumptions, uncertainty, policy verdict, merge status, terminal state, and metadata. Rejected and correlated work is retained rather than discarded during synthesis. The current registry enforces retention when branch records are registered; adapter-level automatic persistence remains an integration responsibility and is not claimed as closed by these core contracts.

Independence metadata may describe source overlap, dependency overlap, prompt lineage, model identity, toolchain identity, and common assumptions. These fields are descriptive and must not be promoted to an unvalidated proof of independence.

## Plan / commit boundary

All action-capable tooling follows:

```text
PROPOSE
  -> GOVERN
  -> VERIFY
  -> AUTHORIZE
  -> COMMIT
```

A model response is never treated as authorization. `CommitGate.commit()` is the final kernel-side authorization check; concrete provider/tool adapters must call it before consequential side effects and must not infer authorization from `COMMIT_READY` alone.

## Explicit exclusions

V1 does not include adaptive topology optimization, learned sycophancy classification, semantic-diversity scoring as proof of independence, autonomous policy learning, harmonic/geometric authorization logic, distributed execution, or live-provider integrations as a precondition of the deterministic kernel.

## PDMAL boundary

PDMAL remains an optional governed execution substrate. The control plane must be operable without PDMAL; PDMAL-specific experiments remain below the generic control-plane boundary and retain their existing candidate/evidence rules. Control-plane verification does not constitute PDMAL experimental evidence, freeze, authorization, unblinding, or an increase in empirical N.

## Agent Control Plane boundary

`ndrorchestration/agent-control-plane` remains a separate experimental implementation asset. Its task lifecycle, dispatch, policy, evaluation, and provenance components are reference material for contract comparison rather than an automatic dependency or copied implementation. Any duplicated concept must have an explicitly declared canonical owner before being treated as synchronized behavior.

## Verification sequence

1. deterministic module contracts;
2. dedicated v1 CI;
3. adversarial control-plane tests;
4. TGL/P-35 integration;
5. adapter bypass audit and provider/tool side-effect boundary verification;
6. cross-repository authority/identity/documentation reconciliation;
7. only then live provider/substrate adapters.

The current branch contains deterministic core and TGL integration coverage. Dedicated CI has verified the v1 core contract suite; adversarial adapter-boundary review and cross-layer reconciliation remain separate verification gates.

## Non-authorizing boundary

This architecture does not alter PDMAL candidate identity, create a freeze, grant pilot authorization, unblind data, or increase empirical N.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
