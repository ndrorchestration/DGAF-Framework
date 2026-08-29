# DGAF Control-Plane Adapter Boundary Audit

**Status:** ENGINEERING AUDIT / NON-AUTHORIZING
**Date:** 2026-08-29

## Scope

This audit covers the boundary between the generic DGAF v1 recursive control plane and consequential external/internal adapters.

## Required invariants

1. Consequential side effects require an explicit `CommitGate` proposal and authorization.
2. Commit requests have unique immutable request identities.
3. Authorization is one-way and cannot replace an existing authorization.
4. A request cannot be committed more than once.
5. `COMMIT_READY` is not itself execution authority.
6. TGL/P-35 remains the per-turn governance kernel and cannot be bypassed by the control plane.
7. Herald may publish/classify evidence but cannot manufacture evidence, authorization, or normative approval.
8. PDMAL remains an optional substrate; control-plane state cannot mutate experimental candidate identity, freeze, authorization, blinding, or empirical N.
9. `agent-control-plane` remains reference material unless a separately governed adapter contract adopts it.

## Evidence

The dedicated adapter-boundary contract workflow and v1 control-plane contract workflow have passed on the previously verified exact PR head. After the latest TGL hardening commits, fresh exact-head CI is required before promoting this audit from engineering verification to a stable current-head verification record.

## Known external boundary

Production source identity remains separately governed under Issue #137. A READY Vercel preview or production deployment does not establish exact-current-main provenance unless the deployment source SHA exactly matches the intended Git SHA.

## Disposition

The boundary is implemented and covered by executable assertions. Full current-head closure remains contingent on fresh CI after the latest commits and exact deployment identity where live adapters are involved.

**Experimental state:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.
