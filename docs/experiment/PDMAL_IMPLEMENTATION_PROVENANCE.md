# PDMAL Implementation Provenance

## Status

**PRE-FREEZE / IMPLEMENTATION VALIDATION IN PROGRESS**

This record distinguishes implementation existence from implementation verification. The harness and pre-freeze runner changes below are not empirical results and do not authorize pilot execution.

## Current branch/head

- PR: `#65`
- Branch: `epistemic/evidence-architecture-v1`
- Last known implementation head when this record was updated: `b74228644af9d9966c2b17aa5a43e74178bd75ce`
- Harness/runner CI execution: **NOT OBSERVED THROUGH CURRENT CONNECTOR SURFACE**

## Implemented controls

### Experimental environment contract

`experiments/pdmal_pilot/pyproject.toml`

- Python: `3.12.0`
- NumPy: `2.5.1`
- NetworkX: `3.6.1`

`requirements-lock.txt` currently represents **direct dependency pins**, not a resolver-generated hash-complete lockfile. A full resolver/hash-locked environment remains a verification task.

### RNG contract

`experiments/pdmal_pilot/harness_contract.py`

- `SeedSequence` root
- `SeedSequence.spawn()` child streams
- `Generator(PCG64)`
- distinct stream IDs for ordering, failure, topology construction, and analysis resampling
- deterministic stream fingerprinting

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

### Fail-closed execution modes

`experiments/pdmal_pilot/run_pilot.py`

- `PDMAL_MODE=contract` is the only mode that can currently execute.
- Contract mode is fixed to 2 validation seeds and emits no empirical data.
- `PDMAL_MODE=pilot` requires both `PDMAL_PROTOCOL_FROZEN=1` and `PDMAL_PILOT_AUTHORIZED=1`.
- Even with those flags, pilot mode currently fails closed because the real experimental task executor has not yet been implemented.
- Unset/unknown mode fails closed.

This creates two independent controls: protocol-freeze authorization and explicit pilot authorization.

### Blinding contract

A deterministic HMAC-SHA256 mapping primitive exists for blinded labels. The real secret is not stored in source. The validation path uses test-only keys and never produces pilot evidence.

### Sample-size implementation

`experiments/pdmal_pilot/sample_size.py`

A deterministic paired-difference planning function is implemented using:

- two-sided alpha `0.05`;
- power `0.80`;
- MDD `0.15`;
- pilot-estimated paired FFCR difference SD;
- `math.ceil` rounding.

This is a planning utility only; it does not consume or generate experimental observations.

### Protocol-deviation register

`experiments/pdmal_pilot/deviations.py`

Provides an append-oriented in-memory register and JSON serialization for deviation ID, timestamp, seed/trial, condition, cause, description, affected metrics, comparability impact, inclusion/exclusion decision, and authorization.

### Pre-freeze validation tests

`experiments/pdmal_pilot/test_harness_contract.py`
`experiments/pdmal_pilot/test_execution_contract.py`

These cover deterministic streams, topology contracts, blinding behavior, explicit mode requirements, pilot fail-closed behavior, sample-size reference/error cases, and deviation serialization.

### CI validation workflows

`.github/workflows/pdmal-harness-validation.yml`
`.github/workflows/pdmal-pre-freeze-runner.yml`

Both are contract-validation workflows. They must not be treated as empirical execution.

## Current verification status

| Control | Status |
|---|---|
| Environment files committed | IMPLEMENTED |
| Exact direct dependency pins | IMPLEMENTED |
| Full hash-complete resolver lock | NOT YET IMPLEMENTED |
| SeedSequence/PCG64 harness | IMPLEMENTED |
| Deterministic RNG tests | IMPLEMENTED / CI PENDING |
| Topology generation/validation | IMPLEMENTED / CI PENDING |
| Fail-closed contract runner | IMPLEMENTED / CI PENDING |
| Trial timeout/retry/recovery engine | NOT YET IMPLEMENTED |
| Real experimental task executor | NOT YET IMPLEMENTED |
| Paired-seed FFCR execution | NOT YET IMPLEMENTED |
| Sample-size planning utility | IMPLEMENTED / CI PENDING |
| Canonical experimental artifact validator | PARTIALLY IMPLEMENTED |
| Protected mapping custody | NOT YET VERIFIED |
| Protocol deviation register | IMPLEMENTED / CI PENDING |
| 300-second runtime characterization | NOT YET VERIFIED |
| Harness/prefreeze CI execution observed | NOT OBSERVED |

## Evidence boundary

A green pre-freeze validation workflow would establish that the implementation controls execute as specified in the validation environment. It would **not** establish PDMAL efficacy, topology superiority, or validation of the scientific hypothesis.

The following must remain false until the corresponding evidence exists:

```text
PDMAL empirical efficacy = VERIFIED
PDMAL superiority = VERIFIED
PDMAL real-world benefit = VERIFIED
Pilot authorized = TRUE
```

## Freeze criterion

Protocol freeze remains prohibited until the implementation controls marked `NOT YET IMPLEMENTED`, `NOT YET VERIFIED`, or equivalent are resolved and independently observed, including the exact execution environment, complete artifact/provenance architecture, real task executor, timeout/recovery semantics, blinding custody, runtime characterization, and CI verification.

## No-data-collection invariant

Until the protocol is explicitly frozen and pilot authorization is recorded, no command in this pre-freeze implementation is permitted to generate the 50-seed pilot dataset. The default and contract execution paths are validation-only.