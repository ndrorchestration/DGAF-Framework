# Canonical Solo Epoch 004 — Exploratory Diagnostics

**Classification:** `POST_PRIMARY_EXPLORATORY_DESCRIPTIVE_ONLY`  
**Primary result:** unchanged — `EVIDENCE_AGAINST_DIRECTIONAL_DGAF`

These diagnostics were computed only after the locked primary result had been recorded. They are intended to locate candidate failure modes and generate future hypotheses. They are not confirmatory tests and cannot replace, weaken, or rescue the Epoch 004 primary result.

## Seed-level pattern

Across the 50 paired seed effects, 40 were negative, 10 were exactly zero, and none were positive. The median DGAF-minus-null seed effect was approximately `-0.06667`; the observed range was `[-0.31111, 0.0]`.

## Aggregate condition descriptives

- DGAF: `0.73378`
- null: `0.82756`
- simple: `0.73911`
- static: `0.89289`

DGAF and `simple` are descriptively very close overall: DGAF minus simple is approximately `-0.00533`. That does not establish equivalence, but it suggests that the canonical governance treatment did not produce a broad aggregate advantage over the simpler comparator in this apparatus.

## Where the DGAF-minus-null deficit appears

Topology-level descriptive differences:

- random_regular: `-0.27111`
- ring: `-0.16444`
- small_world: `-0.02222`
- pdmal: `-0.01111`
- complete: `0.0`

The strongest descriptive deficits are therefore concentrated in random-regular and ring topologies. Complete is tied, and PDMAL/small-world are much closer to null.

By failure count, the DGAF-minus-null difference remains negative at every tested level. The largest failure-count aggregate deficit occurs at failure count 10 (`-0.144`), but the topology decomposition shows that topology structure is a major contributor to the observed pattern.

The five largest topology × failure-count descriptive deficits are:

1. random_regular, failure 10: `-0.44`
2. ring, failure 0: `-0.34`
3. random_regular, failure 8: `-0.30`
4. random_regular, failure 5: `-0.30`
5. random_regular, failure 6: `-0.28`

## What can and cannot be inferred

The data support a descriptive statement that the negative primary effect is concentrated in particular topology regimes rather than being uniformly large across every topology. They also support the observation that DGAF and the simple condition have nearly the same aggregate FFCR in this epoch.

They do **not** establish why those topology-specific deficits occur, which governance component is responsible, whether changing a component would improve performance, statistical significance of secondary contrasts, or any revised efficacy claim.

## Next scientific move

Treat the topology pattern as a hypothesis generator. Any mechanism-specific change should be specified without using Epoch 004 outcomes to tune thresholds or acceptance rules, then tested under a **new prospective protocol and fresh epoch**. Epoch 004 remains immutable negative primary evidence.

High-Assurance remains `NOT AUTHORIZED / N=0`.
