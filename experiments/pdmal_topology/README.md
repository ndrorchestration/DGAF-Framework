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
- Final sample size: determined after the preregistered power analysis; no post-hoc target may be selected from observed significance.
- Small-world control: Watts-Strogatz `n=20, k=4, p=0.3`; `k=3` is not used because the generator requires an even `k`.

## Pilot stopping criteria

The pilot is adequate only when the predeclared criteria are evaluated on masked labels:

- runtime per seed <= 300 seconds;
- primary-metric SD <= 0.15 for at least 4 of 5 masked topology labels;
- maximum masked paired-comparison 95% CI width <= 0.40.

Failure requires the predeclared action in `manifest.yaml`; criteria cannot be changed after inspecting unmasked topology identities.

## Reproducibility and storage

Each pilot execution must preserve:

1. frozen manifest;
2. repository commit;
3. exact experiment dependency versions;
4. separate seed families for topology, failure, workload, and initialization where applicable;
5. raw per-trial observations;
6. analysis code;
7. generated summary;
8. deviations and exclusions;
9. SHA-256 checksum of the raw artifact;
10. persistent CI artifact before analysis begins.

Pilot raw data use the filename pattern `raw_pilot_<commit_short>_<utc_timestamp>.csv` plus a `.sha256` sidecar.

## Blinding

Pilot precision/power preparation uses topology-masked labels generated from an HMAC-SHA256 mapping that requires the external `PDMAL_BLINDING_KEY`. The key is not stored in this repository. The repository therefore cannot reveal which masked label corresponds to PDMAL without the external unblinding key.

## Comparison rule

Topology generation, failure selection, initial states, workload, protocol, compute budget, and stopping condition must be held constant wherever applicable. Randomized topology families receive deterministic per-seed generation from the manifest. The largest-component fraction uses the original population denominator N, not the number of surviving nodes.

## Claims prohibited before analysis

Do not state that PDMAL is superior, optimal, more resilient, or Pareto-efficient before the corresponding preregistered analysis has been executed.

## Execution status

The structural harness, post-failure semantic tests, persistence layer, masking layer, and deterministic case runner are implemented. The mandatory CI dry-run workflow is present, but the current branch head does not yet expose a completed GitHub Actions run. Therefore instrumentation remains **NOT VERIFIED** and no pilot dataset has been promoted to evidence.
