# PDMAL Instrumentation Pre-Flight Status

**Protocol version:** 1.2-pilot  
**Current state:** BLOCKED ON SECRET CONFIGURATION  
**No pilot data generated. No PDMAL performance claim asserted.**

## Verified safeguards

- CI workflow trigger is operational.
- The instrumentation workflow reaches the secret gate in GitHub Actions.
- Missing/invalid `PDMAL_BLINDING_KEY` causes fail-closed termination before experiment execution.
- Experiment dependencies install successfully in the CI environment.
- Topology control uses valid Watts-Strogatz parameters (`k=4, p=0.3`).
- Structural metrics use the preregistered original-population denominator.
- Independent RNG streams are defined for topology, failure, workload, and initialization conditions.
- Byte-level determinism, semantic, schema, checksum, and artifact checks are included in the dry-run workflow.

## Blocking condition

The GitHub Actions repository secret `PDMAL_BLINDING_KEY` is not currently available to the workflow. The last dry run therefore stopped at the fail-closed gate. This is a successful safety-gate failure, not an instrumentation pass.

## Required owner action

Configure a high-entropy `PDMAL_BLINDING_KEY` repository Actions secret with at least 32 characters. Do not commit or print it.

## Next verification gate

After configuration, the next dry run must pass:

1. secret presence/length check without disclosure;
2. byte-for-byte deterministic replay;
3. structural topology invariants;
4. post-failure semantic tests;
5. masked CSV schema validation;
6. SHA-256 sidecar verification;
7. artifact upload and retention;
8. one-seed execution across all five topologies.

Only then may the state change to **Instrumentation: VERIFIED**.

## Pilot prohibition

The 50-seed pilot remains blocked until the full instrumentation gate passes. No exploratory analysis, unblinding, power analysis, or performance claim is permitted before that point.
