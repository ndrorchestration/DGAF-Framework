# Track A Topology Robustness — Epoch 002 Prospective Preregistration

Status: **PROPOSAL ONLY / NOT AUTHORIZED / N=0**  
Controller: **#523**  
Protocol: **`PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-002`**

## Purpose

Epoch 002 is the prospective successor to the unrecoverable Track A Epoch 001 custody path. It creates a new protocol identity and fresh seed panel while preserving the scientific design that was fixed before Epoch 001 outcomes could be analyzed.

Epoch 001 remains historical blinded evidence with primary analysis **UNANALYZABLE / NOT RUN**. Its 2,250 blinded observations are not pooled, inspected for topology outcomes, or used to tune this successor.

The machine-readable authority for this proposal is:

`docs/experiment/TRACK_A_TOPOLOGY_ROBUSTNESS_EPOCH_002_PREREGISTRATION.json`

## What changes from Epoch 001

Only successor-specific prospective identities change here:

- protocol identity: `...EPOCH-002` rather than `...EPOCH-001`;
- seed panel: `20270201..20270250`;
- bootstrap seed: `20270251`;
- custody contract: real precollection recovery drill and non-secret recovery receipt are mandatory under #523.

The new seed panel is machine-checked against the Epoch 001 panel, historical excluded ranges, and diagnostic seeds.

## What does not change

The validator requires exact continuity for the load-bearing scientific design:

- research question and directional hypothesis;
- reference neighbor-mean algorithm, `alpha = 0.5`;
- five-topology panel;
- failure counts `0,1,2,3,4,5,6,8,10`;
- boolean `ffcr_success` endpoint and fixed success definition;
- PDMAL vs random-regular primary contrast;
- paired-seed estimand;
- 10,000-resample percentile bootstrap method;
- two-sided 95% interval and directional interpretation rules;
- single confirmatory family and exploratory-only secondary comparisons;
- 50 paired seed units / 2,250 expected observations;
- prospective QC and fail-closed missing-cell policy;
- analysis-label blinding, structural-lock-before-unblinding, and separate unblinding authorization;
- claim ceiling: canonical DGAF efficacy remains `NOT_ESTABLISHED`.

Any later scientific change requires a separate prospective justification and new governed identity; it must not be silently folded into this record.

## Custody prerequisite

This preregistration does **not** create the real successor key and does not satisfy custody.

Before collection authorization, the real user-controlled process remains:

`fresh local keypair → encrypted PKCS#8 private key → two durable encrypted recovery copies in distinct storage classes → recovery drill → exact public-key/certificate match → non-secret receipt → receipt validator PASS`

The real private key, passphrase, and recoverable secret material must remain outside GitHub, Notion, chat, workflows, logs, and CI artifacts. Solo custody is classified as **`SAME_SYSTEM_NONINDEPENDENT`**; recoverability is not independence.

See `TRACK_A_SUCCESSOR_LOCAL_SETUP.md` and `TRACK_A_SUCCESSOR_SOLO_CUSTODY_CONTRACT.md`.

## Remaining gates after this proposal

Even if this preregistration validates and merges, all of the following remain separate gates:

1. real local successor custody establishment and recovery receipt;
2. analysis implementation revalidation on the successor identity;
3. runner/candidate binding and precollection preflight;
4. exact candidate freeze;
5. separate immutable successor collection authorization;
6. fresh blinded collection;
7. dataset lock;
8. separate unblinding authorization and controlled materialization;
9. separate primary-analysis authorization;
10. locked analysis and bounded interpretation.

## Non-effects

This proposal does not:

- authorize empirical collection;
- create or store a real private key;
- establish independent custody;
- increase scientific N;
- rescue or analyze Epoch 001;
- establish canonical DGAF efficacy;
- establish High-Assurance status.

Current boundary: **EPOCH 001 HISTORICAL / UNANALYZABLE · EPOCH 002 PROPOSAL ONLY · SUCCESSOR COLLECTION NOT AUTHORIZED · CANONICAL DGAF EFFICACY NOT ESTABLISHED · HIGH-ASSURANCE NOT AUTHORIZED / N=0**.
