# PDMAL Implementation Provenance

## Status

PRE-FREEZE / TOPOLOGY FINGERPRINTS IMPLEMENTED / PILOT NOT AUTHORIZED

This record distinguishes implementation existence from implementation verification. The pre-freeze contract path remains separate from empirical execution.

## Topology provenance record

The topology generation code is implemented in:

```text
experiments/pdmal_pilot/harness_contract.py
```

The topology fingerprint helper is implemented in:

```text
experiments/pdmal_pilot/topology_utils.py
```

Authoritative source commits for this topology-provenance change are:

```text
Topology generation + HarnessResult fingerprint field:
efB5d318d95a0714c328f60d5a3157956f4f1965

Fingerprint helper:
123289688583ea9cbdab3cd5b678df7958eed6f1

Reproducibility tests:
ef29c90242923cfe6c1d2276e88e0f3cca89763e
```

### Topology matrix

| Topology | Generator | Parameters / invariants | Source code | Fingerprint |
|---|---|---|---|---|
| Ring | `nx.cycle_graph(20)` | 20 nodes, 20 edges, degree 2, connected | `harness_contract.py` @ `efb5d318d95a0714c328f60d5a3157956f4f1965` | SHA-256 of normalized undirected edge list |
| PDMAL | `nx.dodecahedral_graph()` | 20 nodes, 30 edges, degree 3, connected, node connectivity >= 3 | `harness_contract.py` @ `efb5d318d95a0714c328f60d5a3157956f4f1965` | SHA-256 of normalized undirected edge list |
| Random regular | `nx.random_regular_graph(3, 20, seed=rng)` | 20 nodes, 30 edges, degree 3, connected | `harness_contract.py` @ `efb5d318d95a0714c328f60d5a3157956f4f1965` | SHA-256 of normalized undirected edge list |
| Small-world | `nx.watts_strogatz_graph(20, 4, 0.3, seed=rng)` | 20 nodes, 40 edges, connected | `harness_contract.py` @ `efb5d318d95a0714c328f60d5a3157956f4f1965` | SHA-256 of normalized undirected edge list |
| Complete K20 | `nx.complete_graph(20)` | 20 nodes, 190 edges, degree 19, connected | `harness_contract.py` @ `efb5d318d95a0714c328f60d5a3157956f4f1965` | SHA-256 of normalized undirected edge list |

The random regular and small-world generators consume the dedicated `topology_construction` NumPy stream. Ring, PDMAL dodecahedral, and Complete K20 are deterministic constructors without RNG input.

## Fingerprint algorithm

`experiments/pdmal_pilot/topology_utils.py` defines `graph_fingerprint(graph)`.

For an undirected graph, each edge is normalized to `(min(u, v), max(u, v))`, sorted lexicographically, serialized as `u,v|u,v|...`, encoded as UTF-8, and hashed with SHA-256.

The fingerprint is emitted in each `HarnessResult` as:

```text
 topology_fingerprint
```

Contract artifacts therefore carry a deterministic topology fingerprint for every validated topology result.

## Reproducibility verification

`experiments/pdmal_pilot/test_harness_contract.py` now verifies:

1. identical topology fingerprints for repeated generation from the same root seed and topology stream;
2. fingerprint format is a 64-character hexadecimal SHA-256 digest;
3. contract results contain a fingerprint for every topology.

The new reproducibility test is included automatically in the existing `test_harness_contract.py` invocation in `.github/workflows/pdmal-pre-freeze-runner.yml`.

## Remaining topology freeze boundary

This change establishes the source identifiers, generation parameters, fingerprint method, and reproducibility test. A topology may still not enter the empirical pilot until the final topology set is explicitly frozen and the corresponding CI evidence is observed on the final pre-freeze head.

No topology fingerprint constitutes evidence of empirical superiority or efficacy. It is an implementation/provenance integrity identifier only.
