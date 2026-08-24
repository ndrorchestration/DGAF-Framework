# PDMAL Topology Fingerprint Manifest

**Status:** CURRENT SOURCE MANIFEST / PRE-FREEZE
**Applies to:** current `main` source at the time of generation; must be revalidated for the final freeze candidate.
**Master seed:** `20260817`
**Topology stream seed:** `3575256538061230469`
**Seed derivation:** `sha256("pdmal-v1|20260817|topology")[:8]` interpreted as big-endian unsigned integer.
**Fingerprint function:** SHA-256 of the sorted normalized edge list, using `u,v` pairs joined by `|`, as implemented by `experiments/pdmal_pilot/topology_utils.py`.

## Deterministic fingerprints

| Topology | Generator | Fingerprint |
|---|---|---|
| ring | `nx.cycle_graph(20)` | `d14d1a70fe4401e72301e72a05d0f8024234e2a45a75e989e1fd77d263d4edaf` |
| pdmal | `nx.dodecahedral_graph()` | `cdb82b316016def43c7d9c3c4c0d5ee1c3aaad818ea9c229f921eb632ae952d0` |
| random_regular | `nx.random_regular_graph(3, 20, seed=3575256538061230469)` | `0eb80c5de13e687bb9d64deee7e7a132b097ae9108a8ab5d774e5995281854c4` |
| small_world | `nx.watts_strogatz_graph(20, 4, 0.3, seed=3575256538061230469)` | `8cbfb24f34ae38b795878ce4a9ed8863e3a00c8c15ae463289d88d5e50284ea2` |
| complete | `nx.complete_graph(20)` | `f922f507f58e4d6cf53d142a5fd5de8b37b5eb10d299c33c1df6ff3afe66ebf8` |

## Source identity

- `experiments/pdmal_topology/seeds.py` — ASCII `pdmal-v1` seed derivation.
- `experiments/pdmal_topology/graph_harness.py` — preregistered topology generators.
- `experiments/pdmal_pilot/topology_utils.py` — normalized edge-list fingerprinting.

## Verification boundary

These values are deterministic source-derived provenance for the current repository. They are not pilot results. The final freeze candidate must record the exact blob SHAs of the generator/fingerprint source files and independently re-compute the fingerprints against that exact candidate tree.

## Historical note

Earlier working-tree agents reported a different seed/fingerprint family caused by an older source-state ambiguity. This manifest intentionally derives values from the current committed `seeds.py` source and must not be back-projected into the historical `3510b868...` apparatus.
