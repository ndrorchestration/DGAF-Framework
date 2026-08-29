# CommitGate Integrity Note — 2026-08-29

## Finding

The v1 `CommitGate` implementation currently keys authorization by `request_id` and selects the first matching proposal. A duplicate `request_id` can therefore create ambiguous request-to-authorization provenance.

## Required disposition

Before merge-level verification, `CommitGate` must enforce unique request identity within a gate instance and test the duplicate-request path as fail-closed behavior.

## Boundary

This is an engineering-integrity requirement. It does not authorize PDMAL execution, alter candidate identity, create a freeze, permit unblinding, or increase empirical N.

**Experimental state: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
