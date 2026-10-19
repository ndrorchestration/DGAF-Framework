# SBCF writer authorization generation v0

Status: RESEARCH PROTOTYPE / FAIL-CLOSED / NOT AUTHORIZED.

This increment adds a persisted minimum writer authorization generation to the
off-host witness store. A writer lease carries a generation number. The witness
can monotonically raise the required generation for an exact source/run/policy,
causing older leases to fail closed without relying on wall-clock expiry.

## Atomicity

Generation enforcement is checked inside the same SQLite `BEGIN IMMEDIATE`
transaction as checkpoint admission. This avoids a separate check-then-write
window between revocation state and checkpoint mutation.

The generation record is persisted in the witness database and survives an
ordinary process restart. Generation updates are monotonic: equal or lower
values are rejected.

## Demonstrated contract

- generation 0 is the default when no revocation generation has been recorded;
- a generation-1 writer can advance before revocation;
- raising the required generation to 2 blocks generation-1 writers;
- equal or lower generation updates are rejected;
- reopening the witness database preserves generation 2;
- a generation-2 writer can advance after restart;
- HTTP witness admission also rejects a lease whose generation has been revoked.

## Falsification boundary

Generation revocation is stored in the same witness SQLite database. The strict
expected-failure test
`test_witness_db_rollback_cannot_revive_revoked_writer_generation` preserves
the counterexample that restoring a pre-revocation database snapshot restores
the earlier generation and revives the old writer authority.

This means the mechanism provides wall-clock-independent revocation against
ordinary process restart, but **not rollback-resistant revocation**. Durable
anti-rollback storage or an independently protected monotonic generation anchor
remains required.

The management action in this research increment is an in-process/off-path
store method. No remote credential-management API, external issuer, independent
identity authority, hardware-backed key, rotation policy, or production
authorization is established.

This work does not establish independent custody, independent validation, live
containment, matched comparator efficacy, scientific N, canonical efficacy, or
high assurance.

Preserved ceilings:
`SCIENTIFIC_N_INCREMENT=0`;
`INDEPENDENT_VALIDATION=NOT_ESTABLISHED`;
`CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED`;
`HIGH_ASSURANCE=NOT_AUTHORIZED`.
