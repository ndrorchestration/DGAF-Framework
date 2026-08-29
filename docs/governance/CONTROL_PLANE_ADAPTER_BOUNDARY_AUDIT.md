# DGAF v1 Control-Plane Adapter Boundary Audit

**Status:** IN PROGRESS / ENGINEERING VERIFICATION
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
8. Commit request identities must be unique within a gate instance; authorization must resolve to exactly one proposal identity.

## Audit method

Sweep all action-capable paths for direct calls to GitHub, Vercel, Supabase, filesystem mutation, messaging/publication, deployment, or other consequential tooling. Classify each path as:

`PROPOSE -> GOVERN -> VERIFY -> AUTHORIZE -> COMMIT`

Any path that reaches a consequential effect without the complete chain is an engineering defect.

## Evidence required

- Static path inventory of consequential adapters.
- Negative tests for unauthorized direct invocation.
- Positive tests showing authorization identity is bound to the committed request.
- Duplicate request-identity tests proving ambiguity fails closed.
- Herald boundary tests proving evidence publication cannot mutate governance authority.
- PDMAL adapter tests proving experimental state is unchanged by generic control-plane execution.
- Exact-tree CI evidence for the audit suite after the latest integrity corrections.

## Current findings

- Adapter-boundary contract workflow has passed on the prior integration head.
- Current source now enforces unique `CommitRequest.request_id` values within a `CommitGate` instance.
- Current test suite now covers duplicate request identity and exact-request authorization lookup.
- Full audit remains open until the latest exact-head CI wave and any remaining external integration evidence are resolved.

## Non-authorizing boundary

This audit does not authorize any experiment, change PDMAL candidate identity, create a freeze, unblind data, or increase empirical N.
