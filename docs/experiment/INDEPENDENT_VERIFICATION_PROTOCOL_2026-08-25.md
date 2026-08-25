# Independent Verification Protocol — 2026-08-25

**Status:** Design-only; authorization not granted.

## Objective

Separate verification of implementation integrity from verification of scientific efficacy.

## Independence boundaries

An independent verifier must receive a frozen evidence package without access to protected blinding mappings before the controlled unblinding stage.

The package must contain:

- frozen commit SHA;
- protocol SHA;
- artifact schema/profile SHA;
- dependency lock SHA;
- environment fingerprint;
- workflow logs;
- raw artifacts and SHA sidecars;
- machine-readable metadata;
- reproduction instructions.

The verifier should independently recompute:

1. artifact hashes;
2. sidecar hashes;
3. protocol/artifact SHA bindings;
4. environment fingerprint;
5. deterministic contract outputs;
6. selected statistical summaries from raw artifacts.

## Independence requirements

The verifier must not rely solely on the same generated summary or validator output used by the primary execution path. At least one independent implementation or independent recomputation is required for each critical integrity predicate.

## Scientific boundary

Independent reproduction does not itself establish superiority, efficacy, or novelty. It establishes whether the reported computational result can be reconstructed from the frozen evidence package.

## Closure criteria

Independent verification closes only when the verifier records PASS/FAIL for every predetermined predicate and any discrepancy is resolved through a versioned correction without altering the original evidence.

**Pilot authorization:** NOT GRANTED  
**Empirical N:** 0
