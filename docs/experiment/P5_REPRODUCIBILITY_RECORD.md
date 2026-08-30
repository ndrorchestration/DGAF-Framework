# Reproducibility Record: Candidate c6157158

## 1. Topology Fingerprint
- **Candidate SHA**: `c6157158bf0ee4840e99a381a4b99bd2febe2302`
- **Tree SHA**: `6195063e2e6e01069ddef8a25e90bfe9d8a3283c`
- **Parent SHA**: `9f09a7932d7a21ecd4f57a9a7e7fc65417fe8631`
- **Binding**: Bound to the exact candidate tree.

## 2. Reproducibility Apparatus Verification
The reproducibility apparatus was examined on the candidate tree (`c6157158`).

### Seed/RNG Separation
- **Mechanism**: `experiments/pdmal_topology/seeds.py` implements `derive_seed(master_seed, stream)`.
- **Separation Logic**: Uses SHA256 hash of `pdmal-v1|<master_seed>|<stream>` to derive independent integer seeds for different RNG streams.
- **Verification**:
    - `build_topologies` in `graph_harness.py` uses `derive_seed(seed, "topology")`.
    - `random_node_failures` in `graph_harness.py` uses `derive_seed(seed, "failure")`.
- **Verdict**: **VERIFIED**. RNG streams for topology generation and node failure selection are cryptographically separated, preventing correlation between the generated graph structure and the failure set.

### Determinism Contract
- **Verification**: `experiments/pdmal_topology/determinism.py` implements a canonical serialization of the experiment case (JSON with sorted keys and strict separators) and computes a SHA256 digest of the resulting bytes.
- **Verdict**: **VERIFIED**. The apparatus ensures that identical inputs (seed, topology, failure count) produce identical, verifiable digests.

## 3. Gate Closure
- **P5 Gate**: Reproducibility / Provenance.
- **Status**: **CLOSED**.
- **Evidence**: Mapping of exact candidate tree and verification of the seed separation logic implemented on that tree.
