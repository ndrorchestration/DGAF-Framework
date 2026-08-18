---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL experimental-design control
last_verified: 2026-08-18
applies_to_sha: 2dc0ce49c30b06807f3d57ce3eac775620b31eb5
---

# PDMAL Experimental Task Specification v0.7.4

**Status:** Approved for implementation by the expert panel.

## Scope

The pre-registered pilot workload is endogenous consensus formation over each generated 20-node topology. The pilot uses four conditions: `null`, `simple`, `static`, and `dgaf`. The repository recognizes `dgaf_pdmal`, but that condition is explicitly out of scope for this pilot.

## Deterministic trial identity

A trial is identified by:

```text
(seed, topology, condition, failure_count)
```

The attempt number is not part of trial identity and must not alter topology, initial values, failure selection, or any other workload state. Retries reproduce the same deterministic trial from scratch.

## Consensus dynamics

- Nodes: 20.
- Initial values: Uniform(-1, 1), generated from the dedicated `task_initialization` RNG child stream.
- Iterations: exactly 100; no convergence-based early stopping.
- `null`: active-neighbor averaging with alpha = 0.5.
- `simple`: active-neighbor averaging with alpha = 0.2.
- `static`: fixed edge weights `1 / max(deg_original(i), deg_original(j))`; surviving weights are not renormalized.
- `dgaf`: the verified `DGAF_TGLAdapter` is invoked each iteration without modification.

## DGAF integration

The existing verified adapter contract is authoritative:

```text
TriadicGovernanceLoop.run_turn(input_text, context=context)
```

The adapter's canonical structured-text serialization and structured context payload are reused as-is. Decision vocabulary is:

```text
NO_CHANGE
CONSERVATIVE_MIX
ISOLATE_FAILED_NEIGHBORS
FAIL_CLOSED
```

`NO_CHANGE` applies the `null` update; `CONSERVATIVE_MIX` applies the `simple` update; `ISOLATE_FAILED_NEIGHBORS` applies the `null` update over the already-filtered active-neighbor set; `FAIL_CLOSED` terminates the current attempt as `FAILURE`.

Malformed or missing governance output is an attempt failure, not a silent `null` fallback.

## Failure schedule

- Inject selected failure nodes at the start of iteration 33.
- Failed nodes remain failed for iterations 33 through 65 inclusive.
- Restore all failed nodes at the start of iteration 66.
- Failed nodes retain their last value and are excluded from active-neighbor sets while failed.
- Restored nodes resume updating with their retained value.
- Final consensus quality includes all 20 nodes.

Failure nodes are selected without replacement from the deterministic `failure_injection` stream and do not depend on attempt number.

## Retry semantics

Workload node failures are independent of execution-level retry behavior. The frozen retry policy is:

- attempt timeout: 60 seconds
- recovery window: 30 seconds
- maximum attempts: 3
- seed runtime ceiling: 300 seconds

A governance `FAIL_CLOSED` is an attempt-level `FAILURE`. A later successful attempt is `RECOVERED`; exhausting attempts is `UNRECOVERED_FAILURE` and counts as FFCR failure.

## Endpoints

**Primary endpoint:** FFCR (Failure-Free Completion Rate).

**Secondary endpoint:** `final_std = stddev(X_i(100))` across all 20 nodes, with consensus-quality threshold:

```text
final_std < 0.01
```

FFCR success and consensus-quality success are recorded separately.

## RNG stream preservation

The existing four child streams remain in their original order:

```text
trial_order
failure_injection
topology_construction
analysis_resampling
```

The new `task_initialization` stream is appended so existing stream identities remain stable.

## Verification requirements

Before protocol freeze and pilot authorization:

1. `ConsensusTask` contract tests must cover all four pilot conditions.
2. Retry tests must demonstrate identical deterministic trial state across attempts.
3. DGAF `FAIL_CLOSED` and malformed-output behavior must be covered.
4. Fresh current-head CI must pass.
5. Runtime characterization must establish the operational suitability of the 300-second seed ceiling.
6. Blinding, retention, freeze-packet, protocol-freeze, and pilot-authorization gates must remain closed until independently verified.

Empirical execution remains prohibited until protocol freeze and explicit pilot authorization.
