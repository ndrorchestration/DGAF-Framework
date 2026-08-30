# DGAF v1 Control-Plane Finalization

**Status:** IMPLEMENTATION CANDIDATE / NON-AUTHORIZING

PR #139 is the canonical combined engineering lane for the governed recursive control plane and current TGL contract remediation. Earlier PRs #132/#133/#134 are historical or superseded and are not separate current execution authorities.

The candidate is based on current `main`. Exact-head CI and adversarial review are required before final verification claims. Production source binding remains a separate infrastructure gate under Issue #137.

## Closed engineering invariants

- GovernanceEnvelope authority, tool, data, risk, budget, metadata, and side-effect scope can only remain equal or narrow across child derivation.
- Task identity fields are immutable after construction.
- Lifecycle state, TGL status/seal, and concurrency state are controller-managed and cannot be externally assigned.
- Public task, ledger, registry, and event surfaces are read-only views.
- Merge readiness requires successful sealed TGL evaluation; stale evaluation evidence is cleared when a new evaluation begins.
- Escalated/terminated tasks cannot consume additional resources.
- Child registration is transactionally ordered so failed creation cannot pollute state identity; post-submit `PREFLIGHT` is the observed child state.
- Branch provenance preserves distinct branch identities even when state IDs coincide.
- CommitGate remains the explicit proposal/authorization barrier; `COMMIT_READY` does not itself execute or authorize a consequential side effect.
- Safe terminal abort is available from active lifecycle states without creating an authorization path.

## TGL contract boundary

Required unwired `SKIP` remains fail-closed to escalation; `WARN` propagates unless a stronger failure applies; HPG is conditional on Phi-Closure; terminal failures stop downstream execution; and final audit sealing must cover the authoritative returned audit object.

## Experimental boundary

The control plane does not rebind PDMAL, create a freeze, grant pilot authorization, unblind data, or increase empirical N.

## Current experimental state

PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0
