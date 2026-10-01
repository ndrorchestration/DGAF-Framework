# Governed Repo Primitive Receipt Bridge

Controller: #1208.

This bridge converts canonical serialized receipts from Evidence Gate v0,
ClaimGraph v0, and Action Admission v0 into Governed Repo `UpstreamDecision`
records.

It does not rerun or reinterpret primitive semantics.

## Mappings

- Evidence Gate → `decision_class="evidence"`; preserves `admitted` and
  `reason_code`; requires `authorization_effect=NONE`.
- ClaimGraph → `decision_class="claim_scope"`; preserves `valid` and
  `reason_code`; requires `truth_effect=NONE` and
  `authorization_effect=NONE`.
- Action Admission → `decision_class="authority"`; preserves `admitted`
  and `reason_code`; requires `execution_enabled=false`.

Receipt IDs are caller-supplied provenance references. The bridge does not
invent them.

## Fail-closed boundary

Malformed receipts, wrong schema versions, non-NONE truth/authorization
effects, or Action Admission receipts that enable execution are rejected.

The bridge never merges, pushes, deploys, mutates a repository, or grants
authorization.

## Dependency hold

This draft may be tested before Evidence Gate acceptance, but CGAP-5 remains
open until the integration is verified against accepted primitive versions on
their canonical branches.

## Claim ceiling

A passing composition demonstrates only bounded translation of three primitive
decisions into the non-mutating Governed Repo evaluator. It does not establish
merge authority, production safety, complete branch-protection correctness,
High Assurance, independent validation, certification, or product-market fit.
