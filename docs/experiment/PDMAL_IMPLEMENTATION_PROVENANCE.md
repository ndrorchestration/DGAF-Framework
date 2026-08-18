# PDMAL Implementation Provenance

## Status

**PRE-FREEZE / IMPLEMENTATION VERIFICATION CLOSED FOR CURRENT CI PATH / PILOT NOT AUTHORIZED**

This record distinguishes implementation existence from implementation verification. The current authoritative DGAF/PDMAL CI evidence closes the verified CI path, but does not by itself freeze the protocol, authorize the pilot, or establish empirical efficacy.

## Current branch/head

- PR: `#65`
- Branch: `epistemic/evidence-architecture-v1`
- Current PR head: `8677ea090b47b352a8acf76692f1aa548f6fe392`
- Authoritative DGAF/PDMAL-related CI evidence: GitHub Actions run `32098237208` — **SUCCESS**
- Important scope boundary: run `32098237208` validates the epistemic/PDMAL structural path; it does **not** by itself constitute observation of the dedicated `pdmal-harness-validation.yml` or `pdmal-pre-freeze-runner.yml` workflows.

## Implemented controls

### Experimental environment contract

`experiments/pdmal_pilot/pyproject.toml`

- Python: `3.12.0`
- NumPy: `2.5.1`
- NetworkX: `3.6.1`

`requirements-lock.txt` represents direct dependency pins, not a resolver-generated hash-complete lockfile. A full resolver/hash-locked environment remains a verification task.

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

- `PDMAL_MODE=contract` is the only mode that currently produces validation artifacts.
- Contract mode is fixed to exactly 2 validation seeds and emits contract artifacts only.
- `PDMAL_MODE=pilot` requires both `PDMAL_PROTOCOL_FROZEN=1` and `PDMAL_PILOT_AUTHORIZED=1`.
- Even with those flags, pilot mode currently fails closed because the real experimental task adapter is not implemented.
- Unset/unknown mode fails closed.

### Task/retry engine

`experiments/pdmal_pilot/task_engine.py`

The current engine implements protocol state semantics and a hard process-isolated timeout path:

- first-attempt success;
- failure followed by successful recovery;
- retry exhaustion → unrecovered failure;
- successful attempt exceeding configured timeout → timeout classification;
- hard timeout enforcement via isolated child process termination;
- 3-attempt retry budget;
- 30-second recovery-window parameter;
- separate 300-second seed-runtime ceiling predicate.

**Remaining boundary:** true timeout/isolation semantics are implemented in the task engine and require dedicated CI observation and runtime characterization before protocol freeze. The real experimental task adapter remains unimplemented.

### Blinding contract

A deterministic HMAC-SHA256 mapping primitive exists for blinded labels. The real secret is not stored in source. The validation path uses test-only keys and never produces pilot evidence.

**Remaining boundary:** operational secret custody and separation of duties must be verified before freeze.

### Sample-size implementation

`experiments/pdmal_pilot/sample_size.py`

A deterministic paired-difference planning function is implemented using:

- two-sided alpha `0.05`;
- power `0.80`;
- MDD `0.15`;
- pilot-estimated paired FFCR difference SD;
- `math.ceil` rounding.

This is a planning utility only; it does not consume or generate experimental observations.

**Remaining boundary:** implementation should be exercised by the dedicated pre-freeze validation workflow and its evidence retained before freeze.

### Protocol-deviation register

`experiments/pdmal_pilot/deviations.py`

Provides an append-oriented in-memory register and JSON serialization for deviation ID, timestamp, seed/trial, condition, cause, description, affected metrics, inclusion/exclusion decision, and authorization.

### Pre-freeze validation tests

`experiments/pdmal_pilot/test_harness_contract.py`
`experiments/pdmal_pilot/test_execution_contract.py`
`experiments/pdmal_pilot/test_task_engine.py`

These cover deterministic streams, topology contracts, blinding behavior, explicit mode requirements, pilot fail-closed behavior, retry/timeout state semantics, sample-size reference/error cases, and deviation serialization.

### CI validation workflows

`.github/workflows/pdmal-harness-validation.yml`
`.github/workflows/pdmal-pre-freeze-runner.yml`
`.github/workflows/epistemic-evidence-validation.yml`

Run `32098237208` is authoritative evidence that the epistemic/evidence-validation path passed. Dedicated PDMAL harness/pre-freeze workflow observations remain separate gates unless directly evidenced by their own successful run IDs.

## Current verification status

| Control | Status |
|---|---|
| Environment files committed | IMPLEMENTED |
| Exact direct dependency pins | IMPLEMENTED |
| Full hash-complete resolver lock | NOT YET IMPLEMENTED |
| SeedSequence/PCG64 harness | IMPLEMENTED |
| Deterministic RNG tests | IMPLEMENTED; exact dedicated harness CI observation NOT YET RECORDED |
| Topology generation/validation | IMPLEMENTED; exact dedicated harness CI observation NOT YET RECORDED |
| Fail-closed contract runner | IMPLEMENTED; exact dedicated harness CI observation NOT YET RECORDED |
| Retry/recovery state engine | IMPLEMENTED; exact dedicated harness CI observation NOT YET RECORDED |
| True wall-clock task timeout/isolation | IMPLEMENTED in `task_engine.py`; dedicated CI/runtime characterization NOT YET RECORDED |
| Real experimental task adapter | NOT YET IMPLEMENTED |
| Paired-seed FFCR execution | NOT YET IMPLEMENTED |
| Sample-size planning utility | IMPLEMENTED; dedicated CI observation NOT YET RECORDED |
| Canonical experimental artifact validator | PARTIALLY IMPLEMENTED |
| Protected mapping custody | NOT YET VERIFIED |
| Protocol deviation register | IMPLEMENTED; dedicated CI observation NOT YET RECORDED |
| 300-second runtime characterization | NOT YET VERIFIED |
| Harness/pre-freeze CI execution observed | NOT YET RECORDED |

## Evidence boundary

A green validation workflow establishes only that the covered controls execute as specified in the validation environment. It does **not** establish PDMAL efficacy, topology superiority, or validation of the scientific hypothesis.

The following must remain false until the corresponding evidence exists:

```text
PDMAL empirical efficacy = VERIFIED
PDMAL superiority = VERIFIED
PDMAL real-world benefit = VERIFIED
Pilot authorized = TRUE
```

## Freeze criterion

Protocol freeze remains prohibited until the remaining controls marked `NOT YET IMPLEMENTED`, `NOT YET VERIFIED`, or `NOT YET RECORDED` are resolved and independently observed, including:

- real experimental task adapter;
- complete artifact/provenance validation;
- protected mapping custody and separation of duties;
- dedicated PDMAL harness/pre-freeze CI evidence;
- runtime characterization against the frozen ceiling;
- exact execution-environment record;
- exact implementation identifiers and topology provenance;
- final analysis/sample-size implementation evidence;
- explicit pilot authorization record.

## No-data-collection invariant

Until the protocol is explicitly frozen and pilot authorization is recorded, no command in this pre-freeze implementation is permitted to generate the 50-seed pilot dataset. Contract and validation execution paths remain non-empirical.
