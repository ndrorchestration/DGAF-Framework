# Blinding, Retention, and Reproducibility Audit — 2026-08-25

**Status:** Pre-authorization audit; no empirical execution authorized.

## Blinding

The runner requires an out-of-band `PDMAL_BLINDING_KEY`, converts condition labels to `blind_<digest>`, and removes the key from the process environment before pilot execution continues. This supports separation of condition labels from the artifact stream.

Required closure evidence:

- documented key custody outside the repository;
- role separation between key custodian, executor, and analyst;
- protected condition mapping;
- controlled unblinding event;
- audit record of who/when/why unblinding occurred;
- verification that published artifacts contain no raw condition labels.

Current status: **PARTIAL / NOT OPERATIONALLY VERIFIED**.

## Durable retention

The pilot runner requires a configured archive root before pilot execution and archives seed artifacts and sidecars under the frozen SHA. This establishes an execution prerequisite but does not itself prove durable external retention.

Required closure evidence:

- actual durable archive location;
- immutable or access-controlled retention semantics;
- successful retrieval test;
- raw artifact SHA verification after retrieval;
- sidecar verification;
- documented retention owner and retention period.

Current status: **PARTIAL / NOT OPERATIONALLY VERIFIED**.

## Reproducibility

The runner binds pilot records to a full frozen Git SHA and records an environment fingerprint derived from runtime versions. Dependency locks exist, including the PDMAL lock and CI dependency layer.

Required closure evidence:

- exact frozen tree SHA;
- protocol SHA;
- canonical artifact-schema/profile SHA;
- dependency-lock SHA;
- runtime/environment fingerprint;
- deterministic seed/RNG separation evidence;
- independent reproduction procedure;
- successful reproduction from the frozen package.

Current status: **PARTIAL / NOT OPERATIONALLY VERIFIED**.

## Fail-closed boundary

These three areas remain prerequisites for authorization. Their implementation must not be confused with operational verification. No pilot may proceed solely because the runner contains the corresponding controls.

**Authorization:** NOT GRANTED  
**Empirical N:** 0
