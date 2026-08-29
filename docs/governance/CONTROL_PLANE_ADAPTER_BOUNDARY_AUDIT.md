# DGAF v1 Control-Plane Adapter Boundary Audit

**Status:** OPEN / ENGINEERING VERIFICATION
**Scope:** PR #136 generic control-plane integration
**Experimental state:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0

## Purpose

Establish an explicit engineering audit boundary between the generic DGAF v1 control plane and concrete consequential adapters, evidence publication paths, and external integration assets.

## Required invariants

1. Consequential side effects require an explicit `CommitGate` authorization artifact.
2. `COMMIT_READY` is a controller state, not permission to execute an external side effect.
3. TGL/P-35 governance remains authoritative for per-turn governance and cannot be bypassed by recursive lifecycle code.
4. Herald/evidence publication cannot create, alter, or confer authorization.
5. External `agent-control-plane` components remain reference/integration material unless a separately governed adapter contract makes them canonical.
6. PDMAL experiment adapters cannot mutate candidate identity, freeze state, authorization state, blinding state, or empirical N without the separate experimental governance transition.
7. Provider, deployment, storage, and messaging integrations must expose provenance for the exact action request and authorization reference.

## Audit method

Sweep all action-capable paths for direct calls to GitHub, Vercel, Supabase, filesystem mutation, messaging/publication, deployment, or other consequential tooling. Classify each path as:

`PROPOSE -> GOVERN -> VERIFY -> AUTHORIZE -> COMMIT`

Any path that reaches a consequential effect without the complete chain is an engineering defect.

## Evidence required

- Static path inventory of consequential adapters.
- Negative tests for unauthorized direct invocation.
- Positive tests showing authorization identity is bound to the committed request.
- Herald boundary tests proving evidence publication cannot mutate governance authority.
- PDMAL adapter tests proving experimental state is unchanged by generic control-plane execution.
- Exact-tree CI evidence for the audit suite.

## Non-authorizing boundary

This audit does not authorize any experiment, change PDMAL candidate identity, create a freeze, unblind data, or increase empirical N.
