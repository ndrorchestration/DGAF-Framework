# DGAF v1 — Governed Recursive Control Plane

**Status:** IMPLEMENTATION CANDIDATE / NON-AUTHORIZING  
**Date:** 2026-08-29

DGAF v1 is a governed recursive control-plane layer around the existing TGL/P-35 kernel.

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

## Core invariants

1. Child authority, tools, data, risk, and budgets cannot exceed the parent.
2. Illegal lifecycle transitions fail closed without resource side effects.
3. Exact repeated orchestration states cannot recurse indefinitely.
4. Branch outcomes remain inspectable.
5. Consequential actions require explicit, unique proposal/authorization/commit identity.
6. TGL/P-35 cannot be bypassed or replaced by the recursive controller.
7. Required TGL `SKIP` states escalate rather than become PASS.
8. `WARN` propagates to turn status unless a stronger failure applies.
9. Terminal failure stops downstream execution.
10. The final TGL audit seal covers the complete gate set, including Herald.
11. Consensus, semantic distance, or harmonic/geometric motifs are not authorization signals or proof of independent evidence.

## Agent and experimental boundaries

Generic roles are execution contracts only. They do not create or elevate agent authority. Sentinel-Phi remains canonical governance identity; Professor Prodigy remains non-orchestrating; DemiJoule remains advisory; Reciprocity remains affected-party/fairness review; Herald publishes/classifies evidence but cannot manufacture evidence or approval.

PDMAL remains an optional governed experimental substrate. This layer cannot create a freeze, grant pilot authorization, unblind data, or increase empirical N.

## Verification

Source presence is not verification. Required sequence is deterministic contracts → exact-head CI → adversarial review → TGL/P-35 integration validation → live-provider/substrate adapters.

**Current experimental state:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.
