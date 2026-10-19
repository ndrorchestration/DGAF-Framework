# SBCF bounded writer lease v0

Status: RESEARCH PROTOTYPE / FAIL-CLOSED / NOT AUTHORIZED.

This increment narrows the authority of an off-host witness writer credential.
A server-configured writer lease binds one bearer credential to an exact source,
run and policy, an inclusive minimum/maximum sequence range, and an expiry time.
A request with a known writer credential but outside those bounds is denied
before the witness store is mutated.

## Demonstrated contract

- The read credential cannot be reused as a writer lease credential.
- Duplicate writer credentials are rejected at server construction.
- A writer credential cannot cross its source, run or policy scope.
- A writer credential cannot advance below or above its configured sequence
  window.
- A lease is rejected at or after its configured expiry according to the
  witness host clock.
- The existing monotonic-store replay and policy checks remain in force after
  lease authorization.

## Security boundary

This is blast-radius reduction, not independent identity or high-assurance
authorization. Writer leases are static server configuration containing bearer
credentials. They are not signed by an independent authority, hardware-bound,
rotated, revoked, or externally governed.

Expiry trusts the witness host wall clock. The strict expected-failure test
`test_wall_clock_rollback_cannot_revive_expired_writer_lease` preserves the
counterexample that moving ordinary wall time backward can make an expired lease
appear valid again. A stronger design needs rollback-resistant trusted time or
another monotonic authorization epoch.

A compromised writer can still advance the witness within its authorized
source/run/policy and sequence window, causing fail-closed denial of service in
that bounded scope. Witness-host compromise or rollback remains outside the
demonstrated protection.

This work does not establish independent custody, independent validation, live
containment, matched comparator efficacy, scientific N, canonical efficacy, or
high assurance.

Preserved ceilings:
`SCIENTIFIC_N_INCREMENT=0`;
`INDEPENDENT_VALIDATION=NOT_ESTABLISHED`;
`CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED`;
`HIGH_ASSURANCE=NOT_AUTHORIZED`.

## Two-host lease QA and falsification probe - 2026-10-19

Implementation commit `71efab9a213d7fe7645f9c792f6d4ce3db28d194`
was exercised with NeonPC as client and neontic as witness over a fresh verified
HTTPS service on port 4444. Port 4444 had no listener before the probe.

At injected witness test time 100, a lease scoped to source `broker`, run
`lease-live-run`, policy `policy-lease`, and sequences 1 through 2 accepted
sequence one. The same writer credential failed closed for a different source, run and
policy, for sequence 3 above the configured maximum, and when the read
credential attempted to write. The read credential returned only the accepted
sequence-1 checkpoint.

At injected test time 150, equal to the configured expiry, sequence 2 was
denied and the retained witness checkpoint remained sequence 1.

The test time source was then deliberately moved backward to 100. The same
writer lease accepted sequence 2, and the read credential returned
`lease-cp-2`. This reproduces the strict local expected-failure finding in a
two-host HTTPS setup. It is **falsification evidence** for rollback-resistant
expiry, not a successful trusted-time control.

The probe changed an explicit test clock supplied through `now_fn`; it did not
change the physical witness operating-system clock. The result therefore shows
that the current lease logic depends on a trustworthy rollback-resistant time
source that has not been established.

Retained secret-free receipt:
`docs/research/sbcf_offhost_evidence/2026-10-19/writer_lease_probe.json`.

After capture, the service was stopped and port 4444 was verified without a
listener. CA/server private keys, ephemeral scripts, the injected test clock,
and the client probe directory were deleted. The witness database and public
CA/server certificates remain on neontic as local retained evidence.

Setup notes are preserved in the receipt: a narrow Git fetch initially failed
to create the expected remote-tracking ref and was corrected with an explicit
refspec before service start; an initial PowerShell test-clock write created a
stray untracked file named `100`, which was deleted before service start and
replaced with an explicit file write.

This remains same-operator engineering evidence only. It does not establish
independent custody, independent validation, trusted time, live containment,
efficacy, or high assurance.
