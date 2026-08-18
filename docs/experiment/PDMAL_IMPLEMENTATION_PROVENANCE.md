# PDMAL Implementation Provenance

## Status

**PRE-FREEZE / IMPLEMENTATION VALIDATION IN PROGRESS**

This record distinguishes implementation existence from implementation verification. The harness changes below are not empirical results and do not authorize pilot execution.

## Current branch/head

- PR: `#65`
- Branch: `epistemic/evidence-architecture-v1`
- Current head at this record: `33d239de926b570d46b3ddb75bd880aa1bae5ba7`

## Implemented controls

### Experimental environment contract

`experiments/pdmal_pilot/pyproject.toml`

- Python: `3.12.0`
- NumPy: `2.5.1`
- NetworkX: `3.6.1`

`requirements-lock.txt` currently represents **direct dependency pins**, not a resolver-generated hash-complete lockfile. A full resolver/hash-locked environment remains a verification task.

NumPy 2.5.1 is a published release as of July 4, 2026. NetworkX 3.6.1 is a stable release and supports Python 3.12. These facts are external package metadata; they do not prove that the DGAF runner has been successfully installed in CI.

### RNG contract

`experiments/pdmal_pilot/harness_contract.py`

- `SeedSequence` root
- `SeedSequence.spawn()` child streams
- `Generator(PCG64)`
- distinct stream IDs for ordering, failure, topology construction, and analysis resampling
- deterministic fingerprinting

### Topology contract

The validation harness keeps the experimental-condition matrix separate from the topology-study matrix.

Experimental conditions:

```text
null
simple
static
dgaf
dgaf_pdmal
```

Topology-study candidates:

```text
ring
pdmal
deg 3 random regular
small-world (n=20, k=4, p=0.3)
complete K20
```

The harness validates node count, edge count, connectivity, regularity where specified, and PDMAL node connectivity.

### Blinding contract

A deterministic HMAC-SHA256 mapping primitive exists for blinded labels. The real secret is not stored in source and is not exercised by the validation harness with a production secret.

### Artifact contract

The harness defines required artifact metadata and canonical JSON hashing. The full experimental artifact schema and retention/attestation path remain pending implementation verification.

### CI validation

`.github/workflows/pdmal-harness-validation.yml` installs the direct pins, asserts Python/NumPy/NetworkX versions, runs the deterministic contract tests, emits an environment manifest, and uploads the validation artifact.

The workflow is **contract validation only**. It does not generate pilot data or efficacy outcomes.

## Current verification status

| Control | Status |
|---|---|
| Environment files committed | IMPLEMENTED |
| Exact dependency pins | IMPLEMENTED |
| Full hash-complete resolver lock | NOT YET IMPLEMENTED |
| SeedSequence/PCG64 harness | IMPLEMENTED |
| Deterministic RNG tests | IMPLEMENTED / CI PENDING |
| Topology generation/validation | IMPLEMENTED / CI PENDING |
| Trial timeout/retry/recovery runner | NOT YET IMPLEMENTED |
| Real experiment runner | NOT YET IMPLEMENTED |
| Sample-size implementation | NOT YET IMPLEMENTED |
| Canonical experimental artifact validator | PARTIALLY IMPLEMENTED |
| Protected mapping custody | NOT YET VERIFIED |
| Protocol deviation register | NOT YET IMPLEMENTED |
| 300-second runtime characterization | NOT YET VERIFIED |

## Evidence boundary

A green harness-validation workflow would establish that the implementation controls execute as specified in the validation environment. It would **not** establish PDMAL efficacy, topology superiority, or validation of the scientific hypothesis.

The following must remain false until the corresponding evidence exists:

```text
PDMAL empirical efficacy = VERIFIED
PDMAL superiority = VERIFIED
PDMAL real-world benefit = VERIFIED
Pilot authorized = TRUE
```

## Freeze criterion

Protocol freeze remains prohibited until the implementation controls marked `NOT YET IMPLEMENTED`, `NOT YET VERIFIED`, or equivalent are resolved and independently observed.
