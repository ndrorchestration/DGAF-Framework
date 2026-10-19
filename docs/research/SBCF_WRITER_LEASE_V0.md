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
