# DGAF v1 — Governed Recursive Control Plane

**Status:** IMPLEMENTATION CANDIDATE / NON-AUTHORIZING  
**Date:** 2026-08-29

DGAF v1 incorporates the viable governance-execution subset of the Governed Recursive Lattice / compiler-trace concept around the existing TGL/P-35 stack.

## Canonical boundary

```text
GovernanceEnvelope
      ↓
ControlPlane / TaskState
      ├─ bounded child derivation
      ├─ StateRegistry
      ├─ BudgetLedger
      ├─ BranchRegistry
      └─ CommitGate
      ↓
existing TGL / P-35
      ↓
optional execution substrate (including PDMAL)
```

## v1 invariants

1. Child authority, tools, data, and risk cannot exceed the parent.
2. Child budgets cannot exceed the parent's declared limits.
3. Illegal lifecycle transitions fail closed.
4. Hard TGL/governance failures escalate and cannot be averaged away.
5. Exact repeated orchestration states cannot recurse indefinitely.
6. Rejected, correlated, incomplete, and vetoing branch records remain inspectable.
7. Consequential actions require explicit authorization through `CommitGate`.
8. The control plane cannot replace or bypass TGL/P-35.
9. Consensus and semantic distance are not treated as proof of independent evidence.
10. PDMAL topology and harmonic/geometric motifs are not authorization signals.

## Implemented candidate modules

- `pptl/governance_envelope.py`
- `pptl/control_plane.py`
- `pptl/state_identity.py`
- `pptl/budget_ledger.py`
- `pptl/branch_registry.py`
- `pptl/commit_gate.py`
- `pptl/tests/test_v1_control_plane.py`
- `pptl/tests/test_v1_tgl_integration.py`
- `.github/workflows/control-plane-contract.yml`

## Agent-role boundary

Generic roles (`EXPLOIT`, `DIVERGE`, `VERIFY`, `GOVERN`) are execution contracts, not new agent identities. See `DGAF_V1_AGENT_ROLE_MAPPING.md` for the mapping to Sentinel-Phi, Amethyst, COLLEEN, DemiJoule, Reciprocity, Professor Prodigy, Apogee, and Herald.

## PDMAL boundary

PDMAL remains a governed experimental substrate. This v1 layer must operate without PDMAL and does not alter candidate identity, protocol, freeze state, authorization, or empirical N.

## Verification

Source presence is not verification. Required sequence: deterministic contracts → CI execution → adversarial review → TGL/P-35 integration validation → only then live-provider/substrate adapters.

**Current experimental state:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.
