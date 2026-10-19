# SBCF separate generation anchor prototype v0

Status: RESEARCH PROTOTYPE / FAIL-CLOSED / NOT AUTHORIZED.

This increment moves the minimum admitted writer generation into a separately
addressable HTTPS service. The off-host witness can consult that generation
floor before mutating its checkpoint database. The intent is to separate
revocation state from witness-database rollback, not to claim durable
anti-rollback storage.

## Bounded improvement

The witness accepts an optional generation-floor callback. When configured, a
write is rejected unless the callback returns a non-negative integer and the
writer lease generation is at least that floor. Missing, malformed, or
unavailable floor values fail closed before checkpoint mutation.

The separate generation-anchor store provides:

- a monotonic generation floor scoped to exact source/run/policy;
- distinct read and administration credentials;
- strict monotonic generation updates inside SQLite `BEGIN IMMEDIATE`;
- an HTTPS client that requires an explicit trust anchor;
- fail-closed reads and updates on transport, TLS, HTTP, or parsing failure.

A bounded rollback test now demonstrates that restoring only the witness
database does **not** revive a generation-1 writer after the separate anchor has
advanced to generation 2. The rolled-back witness may locally report generation
0, but the external floor remains 2 and the old write is rejected before
mutation.

## Preserved falsification

A strict expected-failure test restores both a pre-revocation witness database
and a pre-revocation generation-anchor database. The old writer can then advance
again. This deliberately preserves the remaining limitation:

**separate SQLite failure domains are not rollback-resistant storage.**

A stronger claim requires a generation anchor whose monotonic state cannot be
silently restored with the witness state. Candidate next mechanisms include an
independently administered append-only service, hardware-backed monotonic
storage, or another externally verifiable anti-rollback primitive. Any such
mechanism requires its own threat model and failure injection; it must not be
inferred from this prototype.

## Current local QA

At the initial implementation checkpoint:

- generation-anchor focused tests: 9 passed / 1 strict xfailed;
- complete SBCF group: 127 passed / 6 strict xfailed / 37 subtests;
- Black passes across the complete SBCF Python set;
- changed generation-anchor implementation/tests pass isort individually and as
  a changed-file group.

The sixth strict xfail is the coordinated witness + generation-anchor rollback
counterexample. The prior five falsification cases remain unchanged.

## Security and authority boundary

The generation-anchor service is still same-operator research infrastructure.
Its bearer credentials are not hardware-bound identities. Its SQLite store can
be copied, deleted, or rolled back by a sufficiently privileged operator. The
prototype does not establish independent custody, outside validation, live
production containment, matched comparative efficacy, availability guarantees,
scientific efficacy, or high assurance.

No merge, release, freeze, or authority expansion is implied.

`SCIENTIFIC_N_INCREMENT=0`

`INDEPENDENT_VALIDATION=NOT_ESTABLISHED`

`CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED`

`HIGH_ASSURANCE=NOT_AUTHORIZED`
