# PDMAL Implementation Provenance

## Status

**PRE-FREEZE / PRE-FREEZE CI PATH VERIFIED / PILOT NOT AUTHORIZED**

This record distinguishes implementation existence from implementation verification. The current authoritative pre-freeze CI evidence closes the verified adapter/contract path, but does not by itself freeze the protocol, authorize the pilot, or establish empirical efficacy.

## Current branch and authoritative CI evidence

- PR: `#65`
- Branch: `epistemic/evidence-architecture-v1`
- Verified pre-freeze source SHA: `ffde0b9a52d114649a5a0603d9499cecfcd3e7c6`
- Workflow: `PDMAL Pre-Freeze Runner Validation`
- Run: `32102382285` / `#42`
- Job: `Fail-closed runner and provenance contract` / `95605277441`
- Conclusion: **SUCCESS**
- Contract suite: **30 passed**, including `test_dgaf_tgl_adapter.py`
- Provenance artifact: `9312000148`
- Artifact SHA-256: `2af2a89124b699be2175f767552a1f58fb32864268b4e4c5d98dc9124a6b3184`

Run #42 explicitly checked out the branch at `ffde0b9a52d114649a5a0603d9499cecfcd3e7c6`. The run therefore constitutes direct CI evidence against the corrected source, not a historical or pre-fix execution.

## Verified controls

### Experimental environment contract

`experiments/pdmal_pilot/pyproject.toml`

- Python: `3.12.0`
- Direct PDMAL pins include NumPy `2.5.1`, NetworkX `3.6.1`, and pytest `8.4.1`.
- CI additionally installs `pptl/requirements.txt`; run #42 installed pandas `3.0.5` and its required dependencies.

`experiments/pdmal_pilot/requirements-lock.txt` remains a direct-pin manifest, not a resolver-generated hash-complete lockfile. A full resolver/hash-locked reproducibility artifact remains a separate freeze control.

### RNG contract

`experiments/pdmal_pilot/harness_contract.py`

- `SeedSequence` root
- `SeedSequence.spawn()` child streams
- `Generator(PCG64)`
- distinct stream IDs for ordering, failure, topology construction, and analysis resampling
- deterministic stream fingerprinting

The contract suite is covered by run #42; exact freeze-time environment/stream manifest still requires recording.

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

**Remaining freeze boundary:** exact implementation/source SHAs, parameters, generated-graph fingerprints, and validation evidence must be recorded for every topology that enters the final experiment.

### Fail-closed execution modes

`experiments/pdmal_pilot/run_pilot.py`

- `PDMAL_MODE=contract` is the only mode currently producing validation artifacts.
- Contract mode exercised exactly 2 validation seeds in run #42 and emitted no empirical data.
- `PDMAL_MODE=pilot` requires both `PDMAL_PROTOCOL_FROZEN=1` and `PDMAL_PILOT_AUTHORIZED=1`.
- Run #42 verified that pilot mode fails closed when those controls are disabled.
- Unset/unknown mode fails closed.

### DGAF/TGL adapter

`experiments/pdmal_pilot/dgaf_tgl_adapter.py`

The adapter is implemented and **CI-verified** against the current TGL interface:

- consumes `pptl.triadic_governance_loop.TriadicGovernanceLoop.run_turn()` directly;
- uses `TGLHooks` explicitly;
- canonicalizes the PDMAL consensus state deterministically;
- maps structured TGL outcomes into the finite decision vocabulary;
- fails closed on the `FAIL_CLOSED` decision;
- preserves an audit seal hash and input hash.

Run #42 executed the adapter contract test successfully as part of the 30-test pre-freeze suite.

The stale `IntegratedOrchestrator` import in `pptl/__init__.py` was removed at `ffde0b9`. The earlier `TGLConfig`/`TurnContext` collection failure was therefore a pre-fix package import-boundary failure, not evidence that the adapter requires the older orchestrator API.

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

**Remaining boundary:** the engine's semantics are implemented and contract-tested, but the final freeze record must pin the exact operational timeout/retry/runtime values and include dedicated characterization evidence where required by the protocol.

### Experimental task adapter

**Not yet implemented.**

The verified DGAF/TGL adapter is a governance-decision bridge. It is not the complete experimental workload/task adapter required to execute the planned 50-seed empirical experiment end-to-end.

This remains a genuine pre-freeze implementation boundary and must be resolved before the pilot can be authorized.

### Blinding contract

A deterministic HMAC-SHA256 mapping primitive exists for blinded labels. The real secret is not stored in source. The validation path uses test-only keys and never produces pilot evidence.

**Remaining boundary:** operational secret custody, separation of duties, protected mapping storage, and the unblinding event record must be verified before freeze.

### Sample-size implementation

`experiments/pdmal_pilot/sample_size.py`

A deterministic paired-difference planning function is implemented using:

- two-sided alpha `0.05`;
- power `0.80`;
- MDD `0.15`;
- pilot-estimated paired FFCR difference SD;
- `math.ceil` rounding.

This is a planning utility only; it does not consume or generate experimental observations.

**Remaining boundary:** dedicated verification against the final protocol equation and the exact frozen implementation is still required.

### Protocol-deviation register

`experiments/pdmal_pilot/deviations.py`

Provides an append-oriented in-memory register and JSON serialization for deviation ID, timestamp, seed/trial, condition, cause, description, affected metrics, inclusion/exclusion decision, and authorization.

### Pre-freeze validation tests

`experiments/pdmal_pilot/test_harness_contract.py`
`experiments/pdmal_pilot/test_execution_contract.py`
`experiments/pdmal_pilot/test_task_engine.py`
`experiments/pdmal_pilot/test_dgaf_tgl_adapter.py`

Run #42 provides direct evidence that the current pre-freeze contract suite executes successfully on the corrected source.

## Current verification status

| Control | Status |
|---|---|
| Environment files committed | IMPLEMENTED |
| Direct dependency pins | IMPLEMENTED / CI-VERIFIED |
| `pptl` dependency installation | CI-VERIFIED in run #42 |
| Full resolver/hash-complete environment lock | NOT YET IMPLEMENTED |
| SeedSequence/PCG64 harness | IMPLEMENTED / CI-VERIFIED |
| Deterministic RNG tests | CI-VERIFIED in run #42 |
| Topology generation/validation | CI-VERIFIED in run #42; final topology provenance still pending |
| Fail-closed contract runner | CI-VERIFIED in run #42 |
| DGAF/TGL adapter | IMPLEMENTED / CI-VERIFIED |
| Retry/recovery state engine | CI-VERIFIED in run #42 |
| True wall-clock timeout/isolation characterization | IMPLEMENTED; final freeze characterization pending |
| Experimental task adapter | NOT YET IMPLEMENTED |
| Paired-seed FFCR execution | NOT YET IMPLEMENTED |
| Sample-size planning utility | IMPLEMENTED; dedicated protocol-equivalence verification pending |
| Canonical experimental artifact validator | PARTIALLY IMPLEMENTED / contract-validated |
| Protected mapping custody | NOT YET VERIFIED |
| Protocol deviation register | IMPLEMENTED / contract-validated |
| 300-second runtime characterization | NOT YET VERIFIED |
| Dedicated pre-freeze CI execution | **VERIFIED — run #42** |
| Empirical 50-seed pilot | NOT AUTHORIZED / NOT RUN |

## Evidence boundary

Run #42 establishes that the covered software controls execute successfully in the tested CI environment. It does **not** establish PDMAL efficacy, topology superiority, convergence, robustness, or real-world benefit.

The following must remain false until the corresponding evidence and authorization exist:

```text
PDMAL empirical efficacy = VERIFIED
PDMAL superiority = VERIFIED
PDMAL real-world benefit = VERIFIED
Pilot authorized = TRUE
```

## Freeze criterion

Protocol freeze remains prohibited until the remaining controls marked `NOT YET IMPLEMENTED`, `NOT YET VERIFIED`, or otherwise requiring explicit freeze-time provenance are resolved and independently recorded, including:

- real experimental task adapter;
- complete artifact/provenance validation;
- protected mapping custody and separation of duties;
- full resolver/hash-locked or equivalently reproducible environment record;
- exact timeout/retry/runtime values and required characterization;
- exact implementation identifiers and topology provenance;
- final analysis/sample-size implementation evidence;
- canonical artifact schema and retention/custody record;
- explicit freeze commit and timestamp.

## No-data-collection invariant

Until the protocol is explicitly frozen and pilot authorization is recorded, no command in this pre-freeze implementation is permitted to generate the 50-seed pilot dataset. Contract and validation execution paths remain non-empirical.
