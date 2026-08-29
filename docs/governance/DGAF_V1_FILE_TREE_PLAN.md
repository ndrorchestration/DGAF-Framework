# DGAF v1 — File Tree and Ownership Plan

**Status:** IMPLEMENTATION CANDIDATE / NON-AUTHORIZING
**Date:** 2026-08-29

PR #139 is the canonical current engineering lane for the governed recursive control plane and TGL contract remediation.

| Capability | Canonical owner |
|---|---|
| Inherited governance scope | `pptl/governance_envelope.py` |
| Recursive lifecycle | `pptl/control_plane.py` |
| Exact state identity | `pptl/state_identity.py` |
| Resource/concurrency accounting | `pptl/budget_ledger.py` |
| Branch provenance | `pptl/branch_registry.py` |
| Consequential-action authorization | `pptl/commit_gate.py` |
| Per-turn governance | `pptl/triadic_governance_loop.py` |
| Constitutional admission | `pptl/procluding_premise.py` |

TGL semantics are not duplicated in the recursive control plane. Required TGL `SKIP` states escalate, `WARN` propagates, terminal failures stop downstream execution, and final audit sealing covers the complete gate set.

PDMAL remains an optional governed experimental substrate. The v1 layer does not alter candidate identity, freeze state, authorization, blinding, or empirical N.
