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

- `pptl/governance_envelope.py` — immutable inherited authority/tool/data/resource scope.
- `pptl/state_identity.py` — canonical state representation and SHA-256 identity for exact cycle detection.
- `pptl/budget_ledger.py` — fail-closed reservation and actual resource consumption accounting.
- `pptl/branch_registry.py` — append-oriented branch lineage and retained outcome metadata.
- `pptl/commit_gate.py` — explicit proposal/authorization/commit boundary.
- `pptl/control_plane.py` — deterministic lifecycle state machine and bounded child creation.
- `pptl/tests/test_v1_control_plane.py` — deterministic contract tests.
- `.github/workflows/control-plane-contract.yml` — dedicated contract CI lane.

These modules are implementation candidates on the current integration branch; their existence is not itself evidence of merge-level verification.

## Governance invariants

1. Child authority/tool/data scope cannot exceed parent scope.
2. Child budget cannot exceed parent budget.
3. Illegal lifecycle transitions fail closed.
4. Hard vetoes escalate rather than being averaged away or recursively bypassed.
5. Exact repeated states cannot recurse indefinitely.
6. Rejected/correlated/escalated/vetoing branch evidence remains retained.
7. Consequential actions require explicit authorization.
8. Generic control-plane lifecycle does not replace or bypass TGL/P-35.
9. Semantic distance or agent consensus is not treated as proof of independence.
10. PDMAL topology and harmonic/geometric motifs are not authorization signals.

## Typed branch roles

The initial role contracts are:

- `EXPLOIT` — improve the strongest current candidate;
- `DIVERGE` — generate a materially different alternative;
- `VERIFY` — challenge claims, evidence, premises, and contradictions;
- `GOVERN` — check authority, safety, policy, budget, and action constraints.

## Explicit exclusions

V1 does not include adaptive topology optimization, learned sycophancy classification, semantic-diversity scoring as proof of independence, autonomous policy learning, harmonic/geometric authorization logic, distributed execution, or live provider integrations as a precondition of the deterministic kernel.

## PDMAL boundary

PDMAL remains an optional governed execution substrate. The control plane must be operable without PDMAL; PDMAL-specific experiments remain below the generic control-plane boundary and retain their existing candidate/evidence rules.

## Agent Control Plane boundary

`ndrorchestration/agent-control-plane` remains a separate experimental implementation asset. Its task lifecycle, dispatch, policy, evaluation, and provenance components are reference material for contract comparison rather than an automatic dependency or copied implementation.

## Verification sequence

1. deterministic module contracts;
2. dedicated v1 CI;
3. adversarial control-plane tests;
4. TGL/P-35 integration;
5. only then live provider/substrate adapters.

## Non-authorizing boundary

This architecture does not alter PDMAL candidate identity, create a freeze, grant pilot authorization, unblind data, or increase empirical N.

**Current experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
