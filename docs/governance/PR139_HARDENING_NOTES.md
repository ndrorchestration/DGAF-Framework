# PR #139 Hardening Notes

## Current candidate

Current PR #139 head: `be3203868a9fe7a4c156a4c52885a15872a63fa0`

All findings below are engineering-control findings. They do not authorize PDMAL execution or transfer experimental evidence across SHA boundaries.

## Closed engineering findings

### Active-resource release

Escalated tasks now release their active concurrency slot immediately. This applies to recursion-depth refusal, lineage-concurrency refusal, TGL escalation, explicit veto, and budget-overrun escalation.

### TGL boundary

TGL evaluation is callable only from `EVALUATING`. Terminal TGL failure maps to control-plane escalation; the control plane does not reinterpret a terminal governance result as permission to continue recursion.

### Merge-promotion barrier

`MERGE_READY` now requires an actual successful sealed TGL result for the same lifecycle evaluation. A task cannot be promoted by state mutation alone, and starting a new evaluation clears stale TGL status/seal evidence.

### Evidence-shape validation

A TGL result must contain a valid 64-character seal before it can contribute to merge readiness. Invalid or missing sealed evidence fails closed.

### Controller capability boundary

Task identity, lifecycle state, TGL status/seal state, and concurrency state are controller-managed. Public access to tasks, ledgers, state registries, branch registries, and events is read-only. The configured TGL runner cannot be replaced through the public interface after construction.

### Child-state transaction integrity

Child creation checks duplicate task identity and repeated state before recording the post-submit `PREFLIGHT` snapshot. Failed duplicate creation therefore cannot pollute the state registry, and registry identity matches the actual lifecycle state observed.

### Governance inheritance monotonicity

Child authority scope, permitted tools, data classes, risk tier, resource budgets, metadata, and side-effect permissions can only remain equal or narrow. Parent provenance metadata is retained and cannot be overwritten by a child.

### Branch evidence integrity

Branch records are immutable after creation, including provenance collections and metadata. Multiple branches sharing a state ID are retained rather than silently collapsing to a single branch identity. Lineage traversal rejects cyclic parent relationships.

### Terminal consumption barrier

Escalated and terminated tasks cannot consume additional resources.

### Safe abort path

Active nonterminal lifecycle states can be explicitly terminated. This is a terminal abort path, not an authorization path, and does not bypass TGL or CommitGate requirements.

### CI exact-head/reproducibility hardening

The dedicated v1 control-plane workflow is configured to check out `${{ github.event.pull_request.head.sha || github.sha }}`, assert that the working tree SHA matches that exact value, install the pinned repository CI requirements plus a pinned pandas version, and execute the control-plane, TGL integration, adversarial, and capability-boundary suites.

### Herald final-status reduction

After Herald is appended, the TGL recomputes the monotonic final status over the complete gate set before sealing. A Herald `WARN` therefore cannot be hidden behind an earlier `PASS`, and a Herald `KILL` remains terminal.

## Verification-only findings

An earlier dedicated v1 contract execution exposed three contract-test failures on an earlier PR merge ref. The failures were fully diagnosed and corrected. A later exact-head run then exposed and corrected the side-effect narrowing test contract, and the substantive implementation checkpoint `7807d956…` passed the dedicated 40/40 suite before the integrated branch was reconciled with current `main`.

The current branch contains a later TGL semantic correction for Herald status reduction, so fresh exact-head validation is required before claiming the final integrated head is fully verified.

## External deployment boundary

Current-main → production exact source binding remains separately open under Issue #137. A green or rate-limited Vercel status is not itself proof of exact deployment-source identity.

## Experimental boundary

No experimental execution or PDMAL state transition is permitted by this document.

## Current experimental state

PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0
