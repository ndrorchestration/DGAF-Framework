# DGAF v1 — File Tree and Ownership Plan

**Status:** IMPLEMENTATION CANDIDATE / NON-AUTHORIZING  
**Date:** 2026-08-29

```text
DGAF-Framework/
├── .github/workflows/
│   └── control-plane-contract.yml
├── docs/architecture/
│   ├── DGAF_V1_CONTROL_PLANE_INTEGRATION.md
│   ├── DGAF_V1_FILE_TREE_PLAN.md
│   └── DGAF_V1_AGENT_ROLE_MAPPING.md
└── pptl/
    ├── orchestrator.py
    ├── triadic_governance_loop.py
    ├── procluding_premise.py
    ├── governance_envelope.py
    ├── control_plane.py
    ├── state_identity.py
    ├── budget_ledger.py
    ├── branch_registry.py
    ├── commit_gate.py
    └── tests/
        ├── test_v1_control_plane.py
        ├── test_v1_tgl_integration.py
        └── test_v1_adversarial_contract.py
```

## Ownership

| Capability | Canonical owner |
|---|---|
| Inherited governance scope | `pptl/governance_envelope.py` |
| Lifecycle state machine | `pptl/control_plane.py` |
| Exact repeated-state identity | `pptl/state_identity.py` |
| Resource/concurrency accounting | `pptl/budget_ledger.py` |
| Branch provenance | `pptl/branch_registry.py` |
| Consequential-action authorization | `pptl/commit_gate.py` |
| Per-turn governance | `pptl/triadic_governance_loop.py` |
| Constitutional admission | `pptl/procluding_premise.py` |

One concept has one canonical semantic owner. TGL gate definitions are not duplicated in the recursive control plane.

## Integration boundary

`orchestrator.py` remains the integration point. The new control plane governs lifecycle and resource/branch boundaries; TGL remains the per-turn governance kernel.

## Evidence boundary

The final TGL audit seal must cover the complete gate set, including Herald, and required unwired gates must reduce the turn to `ESCALATE` rather than PASS. The generic control plane cannot infer authorization from `COMMIT_READY` alone.

## PDMAL boundary

PDMAL remains below the generic control plane as an optional governed experimental substrate. No v1 control-plane module may silently change experimental candidate identity, freeze state, or authorization.

## Cross-repository boundary

`ndrorchestration/agent-control-plane` is reference material for contract comparison only. It is not a DGAF runtime dependency.
