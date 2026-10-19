# SBCF calibration receiver candidate v0

Status: CANDIDATE / EXECUTABLE INSTRUMENT / NOT FROZEN.

This child of the negative-observation protocol adds an executable receiver-side
instrument for **positive-control timing calibration only**. It does not choose
a calibration sample count, margin, maximum start lag, or negative-observation
bound.

The candidate contract is bound to exact parent artifacts:

- matched HTTP v1 effect contract:
  `sha256:0540ca3b11e82da563208afb4164da9b00c260779832b462dc6824e7dfebadff`;
- receiver custody candidate:
  `sha256:14aeacd65dcc0c33b6f5d465e486560fed32c7e542df8c3b1827fb0ef7df07c5`;
- negative-observation protocol:
  `sha256:d01d33de9f14d9bdace222528325d5766f5422088c8a4fa4c109adc1465e55cf`.

Current calibration-receiver contract digest:

`sha256:3d05f5c94a0aca51fd8b80fe20e4acb84330e649b5e7a1251064fd9721aa0cd5`

## Receiver-monotonic measurement path

The receiver records three events from one injected monotonic clock:

1. receiver armed for a calibration trial;
2. system attempt started;
3. exact effect identity received.

A receipt exposes:

- receiver arm → attempt-start lag;
- attempt-start → receive latency;
- exact system identity;
- exact receiver build identity;
- exact runtime-mapping digest;
- exact effect-identity SHA-256;
- canonical raw bytes and SHA-256.

Cross-host wall-clock comparison is not used.

The instrument rejects:

- matched-trial outcomes presented as calibration input;
- an attempt that starts before receiver arming;
- receipt before attempt-start recording;
- effect-identity mismatch;
- duplicate trial arming;
- duplicate attempt-start recording;
- backward monotonic-clock movement;
- invalid effect SHA-256 identifiers.

## Custody compatibility

Calibration receipts are wrapped in the already-defined receiver-custody shape:

- `trial_id`;
- `effect_identity_sha256`;
- `observed_effect`;
- `raw_record_sha256`;
- `byte_count`.

The canonical calibration receipt remains the retained raw record. The wrapper
adds no analysis or scoring fields.

This makes the timing instrument structurally compatible with the receiver
custody contract, but it does **not** satisfy the custody gate. The receiver
operator remains unassigned and durable retention remains unresolved.

## Calibration aggregation

The aggregation helper requires:

- an exact preregistered sample count;
- one system identity;
- one receiver build identity;
- one runtime-mapping digest;
- unique trial IDs;
- positive-control source only;
- receiver-monotonic clock only.

It reports only:

- sample count;
- maximum arm → attempt-start lag;
- maximum attempt → receive latency;
- raw-receipt hashes.

It does not select a margin or derive/freeze the final negative-observation
bound.

## Closed receiver contract

The receiver contract is deliberately `CANDIDATE_NOT_FROZEN`.

Current blockers:

- calibration receiver contract not frozen;
- receiver build identity not frozen;
- SBCF runtime mapping not frozen;
- ACS runtime mapping not frozen;
- OpenShell runtime mapping not frozen.

A future structural READY state requires an exact receiver build ID + source
SHA-256 and exact runtime-mapping digests for all three systems. READY would
still not freeze the observation protocol's sample count, margin, timing bound,
custody operator, or retention archive.

## QA

First focused execution preserved:

- **13 passed / 3 failed**.
- One failure was an exhausted injected-clock fixture in the duplicate-attempt
  test.
- Two failures were assertion-message mismatches where stricter generic
  validation ran before the SHA-specific message.

Smallest remediation:

- added one clock value only to the affected duplicate-attempt fixture;
- moved effect-SHA validation out of the generic string-field loop so all
  malformed effect identities share the same explicit contract error.

Post-remediation:

- calibration receiver focused tests: **17 passed**;
- receiver + receiver-contract + negative-observation + custody focused slice:
  **60 passed**;
- complete SBCF group: **260 passed / 7 strict xfailed / 37 subtests**;
- Black, isort, flake8 and mypy pass for the changed Python surface;
- Bandit blocking threshold passes;
- `git diff --check` passes.

The seven existing strict xfails are unchanged. This candidate introduces no new
efficacy or containment result.

## Authority boundary

No calibration has been run against SBCF, ACS, or OpenShell. No sample count,
margin, receiver build, runtime mapping, operator, archive, or observation bound
is frozen. No matched trial is authorized.

This instrument is same-system research code and cannot satisfy the independent
receiver-operator requirement by itself.

No merge, trial, freeze, analysis, adjudication, scientific-N increment, or
authority expansion is authorized.

`SCIENTIFIC_N_INCREMENT=0`

`INDEPENDENT_VALIDATION=NOT_ESTABLISHED`

`CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED`

`HIGH_ASSURANCE=NOT_AUTHORIZED`
