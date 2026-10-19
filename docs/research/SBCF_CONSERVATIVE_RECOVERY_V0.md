# SBCF conservative two-store recovery gate (synthetic only)

Research state: PROPOSED / PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED.

The read-only `reconcile_stores` check compares a source/run high-water counter in the primary admission store with the same counter in a separate on-host witness database. Missing, unreadable, invalid or inconsistent records produce BLOCKED. The checker does not modify files or issue authority, and neither a matching result nor any test establishes trusted custody or successful quarantine.

## Bounded QA / intentional counterexample

- Deny deleted, corrupt, missing and mismatched records.
- Verify that absent databases are not recreated during read-only checking.
- Detect a simulated interrupted admission leaving the primary store ahead of the witness.
- Retain the coordinated-rollback demonstration: rolling both files back makes counters match and evades this check; a match is strictly `CONSISTENT_SYNTHETIC`, not `AUTHORIZED`.

## Nonclaims and next gates

This is not transaction recovery, rollback prevention, off-host attestation, OS containment or a secure token broker. It provides a conservative diagnostic outcome to route into a future independent policy decision point. Integration with an actual policy enforcement boundary is NOT established.

Before promotion: trusted external witness, anchored monotonic counter, crash-point tests in real processes, concurrent processes, tamper protection, authenticated source fields, and independent review. SCIENTIFIC_N_INCREMENT=0; INDEPENDENT_VALIDATION=NOT_ESTABLISHED; CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED; HIGH_ASSURANCE=NOT_AUTHORIZED.
