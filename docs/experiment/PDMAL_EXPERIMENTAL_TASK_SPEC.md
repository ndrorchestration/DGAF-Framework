# PDMAL Genuine Experimental Task Specification

**Status:** PRE-FREEZE (executor implementation, not protocol freeze)
**Author:** ndrorchestration
**Date:** 2026-08-20
**Freeze target:** Not yet frozen — this document describes what the executor must do *before* freeze, not after.

---

## 1. What is the genuine experimental task?

The PDMAL experiment asks whether a dodecahedral network topology (`pdmal`) produces measurably different consensus outcomes compared to baseline topologies (ring, random-regular, small-world, complete) under endogenous node failure.

A **single experimental observation** is one complete `ConsensusTask` trial:

```
(seed, topology, condition, failure_count) → ConsensusTrialResult
```

Where:

- `seed` — root entropy seed (deterministic stream spawning)
- `topology` — one of: `ring`, `pdmal`, `random_regular`, `small_world`, `complete`
- `condition` — one of: `null`, `simple`, `static`, `dgaf`
- `failure_count` — one of: 0, 1, 2, 3, 4, 5, 6, 8, 10 (uniform without replacement from 20 nodes)

The trial runs 100 consensus iterations on 20 agents:

- Iteration 33: inject `failure_count` node failures
- Iteration 66: recover (remove failures)
- Iterations 67-99: post-recovery convergence

## 2. Protocol matrix

| Dimension | Values | Count |
|-----------|--------|-------|
| Topology | ring, pdmal, random_regular, small_world, complete | 5 |
| Condition | null, simple, static, dgaf | 4 |
| Failure count | 0, 1, 2, 3, 4, 5, 6, 8, 10 | 9 |
| **Trials per seed** | 5 × 4 × 9 | **180** |
| **Seeds (pilot)** | 50 (post-freeze) | **50** |
| **Total observations** | 180 × 50 | **9,000** |

## 3. What the executor must produce

For each trial, the executor must produce a `ConsensusTrialResult` containing:

| Field | Type | Description |
|-------|------|-------------|
| `trial_key` | str | SHA-256 of `seed\|topology\|condition\|failure_count` |
| `condition` | str | The protocol condition (`null`/`simple`/`static`/`dgaf`) |
| `topology` | str | The topology name |
| `failure_count` | int | Number of failed nodes |
| `failure_nodes` | tuple | Which nodes failed |
| `initial_values` | tuple | Agent values at t=0 |
| `final_values` | tuple | Agent values at t=100 |
| `final_std` | float | Standard deviation of final values |
| `topology_fingerprint` | str | Graph fingerprint for provenance |
| `iterations_completed` | int | Always 100 if SUCCESS |
| `attempt_status` | AttemptStatus | SUCCESS / FAILURE / TIMEOUT |
| `deviation` | str \| None | Deviation reason if any |

## 4. What the executor must NOT do

- **Must not substitute ScriptedTask.** ScriptedTask is a contract-testing stub, not the experimental workload.
- **Must not substitute dry-run path.** The executor must actually run consensus iterations.
- **Must not skip conditions/topologies/failure counts.** All 180 trials per seed must be executed.
- **Must not produce results without provenance.** Each result must include topology fingerprint, trial key, failure nodes, and all fields above.
- **Must not authorize empirical collection before freeze.** Results are pre-freeze artifacts until the freeze commit.

## 5. Evidence classification

| Activity | Classification |
|----------|---------------|
| Running `ConsensusTask.run_detailed()` for all 180 trials × N seeds | **Executor acceptance evidence** (proves apparatus works) |
| Post-freeze, authorized 50-seed run | **Pilot observation** (empirical sample) |
| Statistical analysis of 9,000 observations | **Empirical efficacy evidence** (only after unblinding) |

**Current N = 0.** No seed has been executed end-to-end with the real workload.

## 6. Acceptance predicates

The executor is accepted when it demonstrably:

1. **Task fidelity** — invokes `ConsensusTask.run_detailed()` for all 180 trials per seed, across all 4 conditions and 5 topologies with the correct failure counts
2. **Failure fidelity** — injects failures at iteration 33 and recovers at iteration 66 for the correct failure counts
3. **Observation production** — produces `ConsensusTrialResult` with all required fields, not a status/characterization artifact
4. **Provenance completeness** — includes seed, condition, topology, failure nodes, topology fingerprint, exact iteration count
5. **Artifact integrity** — results validate against `artifact_schema.py` (16 required fields + SHA-256 sidecar)

And one mandatory negative property:

> The executor must demonstrably reject or fail when any required experimental component (topology, condition, failure schedule, consensus iteration count, seed entropy) is substituted by a characterization/placeholder path.

---

*This specification is pre-freeze. Post-freeze, the executor must run exactly as specified here, with no modifications to the workload definition, failure schedule, topology set, or iteration count.*
