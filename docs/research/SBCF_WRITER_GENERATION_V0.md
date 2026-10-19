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

## Two-host generation revocation and rollback probe - 2026-10-19

Implementation commit `5c92d51ec1a76610f0f187dcae233bbacb725a08`
was exercised with NeonPC as client and neontic as witness over a fresh verified
HTTPS service on port 4445.

A generation-1 writer first advanced sequence 1 successfully. A consistent
SQLite backup of the pre-revocation witness state was then captured. While the
service remained online, the witness required-generation record for the exact
source/run/policy was advanced from 0 to 2. The generation-1 writer then failed
closed when attempting sequence 2, and the reader still observed sequence 1.

The witness process was restarted against the unchanged database with a
generation-2 replacement writer. That writer successfully advanced sequence 2,
demonstrating ordinary restart persistence and replacement-generation use.

For falsification, the service was stopped and the pre-revocation SQLite backup
was restored. The restored database had no writer-generation row and retained
only the sequence-1 checkpoint. Restarting with the old generation-1 writer
allowed sequence 2 again. This reproduces the strict expected-failure
counterexample: revocation persisted in the witness database is not itself
rollback-resistant.

Retained secret-free receipt:
`docs/research/sbcf_offhost_evidence/2026-10-19/writer_generation_probe.json`.

The probe also preserves three operational failures without changing the
underlying test state: a post-restore one-line SQLite inspection failed from
PowerShell/Python quoting; the replacement inspection helper was initially
named `inspect.py` and shadowed Python's standard-library `inspect` module,
causing the first restored-state server restart to fail; and a `__pycache__`
directory remained after script cleanup until final cleanup verification removed
it.

Final cleanup verified no port-4445 listener. CA/server private keys, ephemeral
scripts, generation/token fixture files, pre-revocation snapshot, Python
bytecode cache, and client probe files were deleted. The witness database and
public certificates remain on neontic as local retained evidence.

This remains same-operator engineering evidence. It establishes
wall-clock-independent writer revocation against ordinary restart, but not
rollback-resistant revocation, independent custody, independent validation,
live containment, efficacy, or high assurance.
