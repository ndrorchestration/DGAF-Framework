# DGAF v1 — File Tree and Ownership Plan

**Status:** IMPLEMENTATION CANDIDATE / NON-AUTHORIZING  
**Date:** 2026-08-29

The current canonical integration lane is PR #139. Earlier implementation/remediation PRs are historical or superseded and do not constitute parallel authority.

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
        ├── test_v1_adversarial_contract.py
        └── test_triadic_governance_loop.py
```

## Canonical semantic owners

| Capability | Owner |
|---|---|
| Inherited governance scope | `pptl/governance_envelope.py` |
| Recursive lifecycle | `pptl/control_plane.py` |
| Exact state identity | `pptl/state_identity.py` |
| Resource/concurrency accounting | `pptl/budget_ledger.py` |
| Branch provenance | `pptl/branch_registry.py` |
| Consequential-action authorization | `pptl/commit_gate.py` |
| Per-turn governance | `pptl/triadic_governance_loop.py` |
| Constitutional admission | `pptl/procluding_premise.py` |

TGL gate semantics are not duplicated in the recursive control plane.

## Boundaries

The control plane cannot replace or bypass TGL/P-35. Required TGL `SKIP` states escalate; `WARN` propagates; terminal failures stop downstream execution; the final audit seal covers the complete gate set.

PDMAL remains an optional governed experimental substrate. The v1 layer does not alter candidate identity, freeze state, authorization, blinding, or empirical N.

`ndrorchestration/agent-control-plane` remains reference material for contract comparison only.
