# Ecosystem Orchestration Contract

## Purpose

This contract defines a reusable, non-authorizing integration boundary for the NDR ecosystem. It is intended to make project state, evidence, decisions, and drift visible across GitHub, Notion, Drive, deployments, and future adapters.

It does not establish experimental validity, protocol freeze, authorization, collection, unblinding, or efficacy. For DGAF, the current scientific state remains PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.

## Design rules

1. **One authority per fact.** GitHub is authoritative for source, commits, pull requests, and CI. Notion is authoritative for interpreted control state and navigation. Drive preserves durable mirrors and provenance. Runtime platforms establish only deployment/runtime evidence.
2. **Exact identity binding.** Every evidence-bearing record MUST name its subject identity (commit, artifact digest, deployment ID, or immutable record ID).
3. **No evidence transfer.** Evidence MAY NOT be reused after a subject identity changes. A post-merge or rebased candidate requires fresh validation.
4. **Fail closed.** Missing, stale, conflicting, or unverifiable evidence is non-authorizing.
5. **Append before revise.** New scientific or governance epochs are added as successor records; historical records are not rewritten to imply a new result.
6. **Secrets stay outside the contract.** Events and receipts MUST NOT contain private keys, passphrases, tokens, raw secrets, or secret-derived material.
7. **Automation proposes; authorized governance decides.** Reconciliation may open a repair item or report drift, but it cannot advance scientific state or grant authorization.

## Canonical event envelope

All adapters SHOULD emit this JSON-compatible envelope:

```json
{
  "schema_version": "1.0",
  "event_id": "uuid-or-content-addressed-id",
  "occurred_at": "RFC-3339 timestamp",
  "producer": {
    "system": "github|notion|drive|vercel|local-tool",
    "adapter_version": "semver-or-commit"
  },
  "subject": {
    "kind": "repository|pull_request|commit|workflow_run|artifact|deployment|control_record|custody_receipt",
    "immutable_id": "provider-specific immutable identity",
    "display_ref": "optional human-readable reference"
  },
  "event_type": "evidence.observed|state.reported|drift.detected|repair.proposed|decision.recorded",
  "classification": "operational|governance|scientific",
  "authority": {
    "system_of_record": "github|notion|drive|vercel|local-operator",
    "claim_scope": "what this producer may establish"
  },
  "evidence": [
    {
      "kind": "commit|workflow_run|artifact_digest|deployment|document|receipt",
      "locator": "stable URI or provider identifier",
      "sha256": "optional digest",
      "verification": "pass|fail|not_run|unverified|stale"
    }
  ],
  "state": {
    "value": "project-defined state label",
    "authorization_effect": "none"
  },
  "integrity": {
    "contains_secret": false,
    "subject_binding_verified": true
  }
}
```

## State and failure vocabulary

Use the following values consistently:

| Value | Meaning | Authorization effect |
|---|---|---|
| `PASS` / `VERIFIED` | Evidence validates the named subject and scope | None by itself |
| `FAIL` | A check executed and did not satisfy its rule | Blocks the applicable gate |
| `BLOCKED` | Required prerequisite or authority is absent | Blocks the applicable gate |
| `UNVERIFIED` | Evidence has not been independently established | Non-authorizing |
| `STALE` | Evidence is attached to a different or superseded identity | Non-authorizing |
| `NOT_RUN` | The required execution has not occurred | Non-authorizing |
| `NOT_APPLICABLE` | The rule genuinely does not apply, with recorded rationale | None |

## Reconciliation loop

A reconciliation run compares authoritative records without making authoritative changes:

1. Collect bounded snapshots from each authority.
2. Normalize identifiers into event envelopes.
3. Match by immutable identity, declared scope, and timestamp.
4. Emit `drift.detected` records for missing, contradictory, stale, or scope-mismatched facts.
5. Emit a `repair.proposed` record naming the authoritative owner and the minimum corrective action.
6. Require an authorized human or repository workflow to enact the repair.
7. Reconcile again and retain both the original drift record and its resolution evidence.

A reconciliation result is an operational observation, not a scientific finding or authorization decision.

## Implementation sequence

1. Implement a read-only GitHub adapter for pull-request head SHA, workflow conclusion, and merge identity.
2. Add a Notion adapter that reads only designated control-center fields and authority mappings.
3. Generate a machine-readable drift report with no write capability.
4. Add tests for stale-head detection, authority conflict detection, and secret-field rejection.
5. Only after read-only validation is stable, add narrowly scoped repair proposals.
6. Keep all writes explicit, reviewable, and independently validated.

## Required tests for any adapter

- Reject an event with no immutable subject identity.
- Reject an event that contains a secret-designated field.
- Mark evidence stale when its bound subject differs from the evaluated subject.
- Preserve the producing authority and claim scope.
- Demonstrate that a `PASS` event cannot change authorization state.
- Demonstrate that a reconciliation run cannot write to an authority of record.

## Adoption boundary

This document is a contract and implementation plan only. It does not replace existing DGAF/PDMAL governance controls. Any future implementation must be introduced through a bounded pull request with exact-head validation and must preserve the existing fail-closed controls.
