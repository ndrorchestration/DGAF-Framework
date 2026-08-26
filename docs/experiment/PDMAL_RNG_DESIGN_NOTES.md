---
status: CURRENT SOURCE DOCUMENT / PRE-FREEZE
state: DESIGN_NOTES
author: coherence-review
last_updated: 2026-08-20
---

# PDMAL RNG Design Notes (F2, F3)

## Overview

These notes document intentional design distinctions in the PDMAL codebase that may appear as inconsistencies but are deliberate architectural choices.

## F2: Dual Seed-Derivation Systems

### System 1: numpy SeedSequence (pdmal_pilot)

**Location:** `experiments/pdmal_pilot/task_engine.py`

**Mechanism:** Uses `numpy.random.SeedSequence.spawn(N)` to derive N independent PCG64 streams.

```python
seed_seq = np.random.SeedSequence(seed)
child_streams = seed_seq.spawn(5)  # 5 independent streams
```

**Purpose:** Provides cryptographically sound, independent RNG streams for the pilot execution context. All streams are fully parallelizable and have strong guarantees of non-overlap.

### System 2: hashlib + Python random (pdmal_topology)

**Location:** `experiments/pdmal_topology/seeds.py`

**Mechanism:** Uses `hashlib.sha256` to derive integer seeds, then feeds them to Python's `random.Random`.

```python
payload = f"pdmal-v1|{master_seed}|{stream}".encode("utf-8")
seed_int = int.from_bytes(hashlib.sha256(payload).digest()[:8], "big")
rng = random.Random(seed_int)
```

**Purpose:** Provides deterministic seed derivation with external auditability. The hash-based derivation makes it possible to verify seed derivation without needing the original Python environment.

### Design Rationale

These systems serve different purposes:

1. **pdmal_pilot/task_engine.py** (numpy SeedSequence): Optimized for high-performance parallel simulation where multiple threads need independent random streams. The PCG64 generator provides excellent statistical properties and the spawn() mechanism guarantees no correlation between streams.

2. **pdmal_topology/graph_harness.py** (hashlib+random): Optimized for auditability and verification. The seed derivation is externally verifiable via the hash input, and the resulting integer can be independently reproduced in any environment with SHA-256.

### Cross-Track Consistency

Each track maintains internal consistency:
- pdmal_pilot: ALL seeds derived via numpy SeedSequence stream spawning
- pdmal_topology: seed derivation uses hashlib, failure injection if needed uses the derived Python random.Random instances

## F3: Dual Failure-Injection Mechanisms

### Mechanism 1: numpy Generator.choice (ConsensusTask)

**Location:** `experiments/pdmal_pilot/task_engine.py`

```python
failure_nodes = np.random.default_rng(failure_seed).choice(
    20, size=failure_count, replace=False
)
```

**Properties:**
- Uses numpy's PCG64 generator
- Selection is without replacement
- Fully deterministic given the seed
- High-performance for repeated selections

### Mechanism 2: Python random.sample (graph_harness)

**Location:** `experiments/pdmal_topology/graph_harness.py`

```python
failure_nodes = random.Random(failure_seed).sample(range(n), failure_count)
```

**Properties:**
- Uses Python's Mersenne Twister
- Selection is without replacement
- Fully deterministic given the seed
- Pure-Py implementation, no numpy dependency required

### Design Rationale

Neither mechanism is a bug—they serve different contexts:

1. **ConsensusTask (numpy choice):** Used in the main simulation loop where numpy is already loaded for the task engine. Provides optimal performance when executing thousands of trials.

2. **graph_harness (random.sample):** Used for topology-level utilities where the simulation may not need numpy loaded. Maintains compatibility with environments where only standard library is available.

### Important: Different Seeds, Same Property

Both mechanisms use separate seed streams that derive from their respective seed derivation systems. When comparing failure injection behavior across tracks, the different RNG families do NOT produce the same sequence—but this is intentional. Each system only needs deterministic failure injection within its own track, not cross-track correspondence.

## F5: External Dependency Note (pptl)

The `pdmal_pilot/run_pilot.py` imports from an external module `pptl.triadic_governance_loop`:

```python
from pptl.triadic_governance_loop import TriadicGovernanceLoop
```

This dependency is deliberately external because:
1. The triadic governance loop is a separate governance module
2. Different projects may evolve their TGL implementations independently
3. The PDMAL adapter tests `dgaf_tgl_adapter.py` in isolation, mocking the TGL dependency

The adapter's `decision_from_audit()` function is well-tested without the external dependency. Integration testing with the actual pptl module is a deployment-time concern.

## References

- PDMAL_EXPERIMENT_PROTOCOL.md for the overall experimental design
- PDMAL_TASK_SPEC_V0.7.4.md for consensus dynamics
- experiments/pdmal_pilot/task_engine.py for numpy-based RNG usage
- experiments/pdmal_topology/seeds.py for hash-based seed derivation
- experiments/pdmal_topology/graph_harness.py for failure injection in topology utilities