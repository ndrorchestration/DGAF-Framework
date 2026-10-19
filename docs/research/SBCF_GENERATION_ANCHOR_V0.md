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

## Live probe status — BLOCKED by host routing

A bounded two-host live probe was attempted at candidate
`b3846ac710676b63783eb356cde8558e3a2cff5f`. The planned topology placed
the generation anchor and client on NeonPC and the witness on neontic. This
would have tested witness-database rollback while the generation floor remained
on the other machine. It would still have been same-operator evidence, not
independent custody.

The anchor service started successfully on NeonPC with fresh ephemeral TLS
material and an empty generation store. The first verified cross-host read from
neontic failed before TLS with Windows socket error 10013. NeonPC's Ethernet
profile was Public while the first temporary inbound rule was Private-only; the
rule was replaced with an exact-source, exact-port rule applying to all
profiles. Connectivity still failed. Direct `Test-NetConnection` to
`192.168.1.81:4447` remained false, and the alternate Tailscale route to
`100.107.237.63:4447` also failed/timed out.

The witness service was therefore **not started**. No writer checkpoint,
generation advance, witness rollback, or coordinated rollback was attempted in
the live environment. This is an environment/network block, not a failed
protocol assertion.

Cleanup was verified after the blocked attempt: the anchor service was stopped,
the temporary firewall rule was removed, no listeners remained on ports 4447 or
4446, and both ephemeral probe directories—including all private keys and test
credentials—were deleted.

Secret-free blocked-probe receipt:
`docs/research/sbcf_offhost_evidence/2026-10-19/generation_anchor_probe_blocked.json`.

At that blocked checkpoint, the evidence boundary remained the hosted/synthetic
result: witness-only database rollback was blocked while a separate generation
floor remained intact, while coordinated rollback of both SQLite failure
domains remained a preserved strict counterexample.

## Reversed two-host live QA — 2026-10-19

After the first topology was blocked by one-way host routing, the same bounded
property was tested with the roles reversed: neontic hosted the generation
anchor on port 4448, while NeonPC hosted both the witness and the client. This
kept the generation floor on a different machine from the witness database
without claiming independent custody.

The initial remote floor was 0. A generation-1 writer advanced sequence 1, and
consistent pre-revocation SQLite snapshots of both failure domains were then
captured.

The anchor was advanced to generation 2 over verified HTTPS. The generation-1
writer was rejected at sequence 2, while a generation-2 writer was accepted.

For the positive rollback phase, only the witness database was restored to its
pre-revocation sequence-1 snapshot. The remote anchor remained at generation 2.
The generation-1 writer was still rejected, while the generation-2 writer was
accepted and restored sequence 2. This is bounded live evidence that separating
the generation floor from the witness database prevents **witness-only**
rollback from undoing revocation.

The anchor service was then stopped while the witness remained live. The witness
could not obtain a generation floor; a generation-2 sequence-3 write failed
closed and checkpoint state stayed at sequence 2. After the unchanged anchor
service restarted, floor 2 was observed again and the generation-2 writer
advanced sequence 3.

Finally, both services were stopped and both pre-revocation SQLite snapshots
were restored. After restart the anchor floor had returned to 0, and the old
generation-1 writer successfully advanced sequence 2. This directly reproduces
the coordinated-rollback counterexample across the two machines.

The result therefore strengthens the bounded claim and strengthens the
falsification boundary at the same time:

- **supported:** a separately hosted generation floor can survive witness-only
  database rollback and enforce revocation after witness restore;
- **supported:** anchor unavailability causes fail-closed witness behavior;
- **falsified:** ordinary SQLite separation alone provides durable anti-rollback
  protection against coordinated rollback.

The first blocked topology remains separately recorded rather than overwritten.

Secret-free receipts:

- `docs/research/sbcf_offhost_evidence/2026-10-19/generation_anchor_probe.json`
- `docs/research/sbcf_offhost_evidence/2026-10-19/generation_anchor_probe_blocked.json`

After capture, both services were stopped. No listeners remained on ports 4448
or 4449. All private keys, ephemeral scripts, and fixture credentials were
deleted from both Git worktrees. Only non-secret SQLite evidence and public
certificates were retained outside the repositories.

The first documentation validation of these appended live-QA sections found two
MD012 double-blank defects. Only those extra blank lines were removed before
publication; no evidence content or result was changed.

This remains same-operator evidence with client and witness co-resident on
NeonPC. It does not establish independent custody, independent validation,
production containment, comparative efficacy, or high assurance.
