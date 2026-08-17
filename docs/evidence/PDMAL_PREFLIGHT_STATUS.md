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

## Epistemic boundary

The pre-flight work establishes that safeguards and execution machinery are implemented and that fail-closed behavior has been observed. It does **not** establish that the experimental protocol is empirically sound, that its metrics are valid for all intended uses, or that PDMAL has any performance advantage. Those questions remain subject to the preregistered experiment and later validation.

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

## Post-verification execution sequence

After instrumentation verification:

1. Execute the frozen 50-seed pilot.
2. Assess only the preregistered blinded pilot criteria.
3. Determine final sample size using the preregistered power-analysis method.
4. Freeze and record any justified protocol amendment before confirmatory execution.
5. Execute the final blinded experiment.
6. Archive raw data and checksums before unblinding.
7. Unblind only after data collection and sample-size decisions are locked.
8. Run the preregistered analysis and report effect estimates, uncertainty, deviations, and scope limitations.

## Pilot prohibition

The 50-seed pilot remains blocked until the full instrumentation gate passes. No exploratory analysis, unblinding, power analysis, or performance claim is permitted before that point.
