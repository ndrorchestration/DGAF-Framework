# DGAF Control-Plane Adapter Boundary Audit

**Status:** ENGINEERING AUDIT / NON-AUTHORIZING
**Date:** 2026-08-29
**Current PR #139 head:** `228cf8db6f9f811574dc24310e822a2a2a882fff`

## Scope

This audit covers the boundary between the generic DGAF v1 recursive control plane and consequential external/internal adapters.

## Required invariants

1. Consequential side effects require an explicit `CommitGate` proposal and authorization.
2. Commit requests have unique immutable request identities.
3. Authorization is one-way and cannot replace an existing authorization.
4. A request cannot be committed more than once.
5. `COMMIT_READY` is not itself execution authority.
6. TGL/P-35 remains the per-turn governance kernel and cannot be bypassed by the control plane.
7. TGL status/seal evidence used for merge readiness must be valid sealed evidence; stale status is cleared when a new evaluation begins.
8. Task identity and lifecycle state are controller-managed; public control-plane views do not expose mutators for internal state.
9. Escalated or terminated tasks cannot consume additional resources.
10. Child governance scope cannot widen authority, tool/data scope, risk, budget, metadata, or side-effect permissions.
11. Child state registration occurs after successful submission at `PREFLIGHT`, avoiding phantom state identities on failed creation.
12. Branch provenance retains distinct branch identities even when multiple branches share a state ID.
13. Herald may publish/classify evidence but cannot manufacture evidence, authorization, or normative approval.
14. PDMAL remains an optional substrate; control-plane state cannot mutate experimental candidate identity, freeze, authorization, blinding, or empirical N.
15. `agent-control-plane` remains reference material unless a separately governed adapter contract adopts it.

## Evidence

The dedicated adapter-boundary and v1 control-plane workflows have produced historical successful checks on earlier PR merge refs. The first exact control-plane contract execution also exposed three concrete test-contract mismatches; those were diagnosed and corrected. No historical result is being relabeled as current-head verification.

Fresh exact-head CI remains required for `228cf8db…` after the latest hardening/documentation commits. The engineering audit therefore remains implemented but not promoted to stable current-head verification.

## Known external boundary

Production source identity remains separately governed under Issue #137. A READY Vercel preview or production deployment does not establish exact-current-main provenance unless the deployment source SHA exactly matches the intended Git SHA.

## Disposition

The boundary is implemented and covered by executable assertions. Current-head closure remains contingent on fresh CI after the latest commits and exact deployment identity where live adapters are involved.

**Experimental state:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.