# PDMAL Topology Comparison — Pilot

This directory contains the preregistered computational experiment for comparing the 20-node dodecahedral PDMAL topology against ring, 3-regular random, Watts-Strogatz, and complete graphs.

## Epistemic boundary

This pilot is evidence-producing infrastructure. It does not establish PDMAL superiority. Hypotheses remain hypotheses until the frozen protocol is executed and analyzed.

## Frozen primary design

- Paired computational design by seed.
- N = 20 agents/nodes.
- Primary failure mode: uniform random node failure.
- Failure counts: 0, 1, 2, 3, 4, 5, 6, 8, 10.
- Primary structural outcomes: largest-component fraction and connectivity probability.
- Application outcome: scalar-consensus task success.
- Pilot: 50 seeds.
- Final sample size: determined after pilot/power analysis; no post-hoc target chosen from observed significance.

## Required artifacts

Each execution must preserve:

1. frozen manifest;
2. repository commit;
3. Python/dependency environment;
4. seed family;
5. raw per-trial observations;
6. analysis code;
7. generated summary;
8. deviations and exclusions;
9. artifact hashes.

## Comparison rule

Topology generation, failure selection, initial states, workload, protocol, compute budget, and stopping condition must be held constant wherever applicable. Randomized topology families receive deterministic per-seed generation from the manifest.

## Claims prohibited before analysis

Do not state that PDMAL is superior, optimal, more resilient, or Pareto-efficient before the corresponding preregistered analysis has been executed.
