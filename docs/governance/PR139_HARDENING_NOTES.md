# PR #139 Hardening Notes

## Current candidate

Current PR #139 head: `ce93394302e64d7d4f687846a9b6e7c24567ab3e`

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

### CI completeness

The v1 control-plane CI lane executes core, TGL integration, and adversarial contract suites. Missing test files are treated as repository errors rather than silently skipped.

## Resource accounting

Expansion startup consumes one round and one node through `BudgetLedger.consume()`. Reservations remain explicit and budget-aware; concurrency acquisition/release is bounded and validated.

## Commit integrity

Commit requests are immutable after proposal, request IDs are unique within a gate instance, authorization is one-way, and a successfully committed request cannot be replayed through the same gate.

## Verification-only findings

The first dedicated v1 contract execution exposed three contract-test failures on an earlier PR merge ref. The failures were fully diagnosed: a stale side-effect inheritance expectation, an assertion using the wrong post-escalation error branch, and a test assuming `ADMITTED → TERMINATED` before that abort path was formalized. Those failures are historical diagnostics; they are not current-head verification.

Current candidate `ce933943…` requires a fresh exact-head CI matrix after the latest hardening commits.

## External deployment boundary

Current-main → production exact source binding remains separately open under Issue #137. Deployment readiness cannot be promoted to exact-current-main evidence without source-SHA binding.

## Experimental boundary

No experimental execution or PDMAL state transition is permitted by this document.

**PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0**