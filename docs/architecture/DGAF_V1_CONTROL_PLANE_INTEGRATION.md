# DGAF v1 — Governed Recursive Control Plane

**Status:** IMPLEMENTATION CANDIDATE / NON-AUTHORIZING  
**Date:** 2026-08-29

DGAF v1 incorporates the viable governance-execution subset of the governed recursive control-plane concept around the existing TGL/P-35 stack.

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
3. Illegal lifecycle transitions fail closed without resource side effects.
4. Hard TGL/governance failures cannot be averaged away.
5. Exact repeated orchestration states cannot recurse indefinitely.
6. Rejected, correlated, incomplete, and vetoing branch records remain inspectable.
7. Consequential actions require explicit authorization through `CommitGate` with unique request identity and one-way authorization.
8. The control plane cannot replace or bypass TGL/P-35.
9. Consensus and semantic distance are not treated as proof of independent evidence.
10. PDMAL topology and harmonic/geometric motifs are not authorization signals.
11. TGL required `SKIP` states escalate, WARN propagates, terminal failure stops downstream execution, and the final audit seal covers the complete gate set including Herald.

## Agent and evidence boundaries

Generic roles are execution contracts only. Sentinel-Phi remains the canonical governance identity; Professor Prodigy remains non-orchestrating; DemiJoule remains advisory; Reciprocity remains an affected-party/fairness review role; Herald publishes/classifies evidence but cannot manufacture evidence or approval.

PDMAL remains an optional governed experimental substrate. This v1 layer cannot create a freeze, grant pilot authorization, unblind data, or increase empirical N.

## Verification

Source presence is not verification. Required sequence: deterministic contracts → exact-head CI → adversarial review → TGL/P-35 integration validation → only then live-provider/substrate adapters.

**Current experimental state:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.
