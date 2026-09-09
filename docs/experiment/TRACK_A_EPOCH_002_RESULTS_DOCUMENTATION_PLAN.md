# Track A Epoch 002 — Results Documentation, QC, and Release Plan

Status: **PROSPECTIVE PLAN ONLY / NOT AUTHORIZED / N=0**  
Controller: **#523**  
Companion scientific authority: `TRACK_A_TOPOLOGY_ROBUSTNESS_EPOCH_002_PREREGISTRATION.json`

## Purpose

This plan specifies the evidence that must be produced, checked, retained, and documented if—and only if—Epoch 002 is separately authorized. It does not alter the preregistered endpoint, estimand, seed panel, collection authorization status, or claim ceiling.

A completed row in this plan is operational evidence for its named scope only. No row alone authorizes collection, unblinding, analysis, or a scientific claim.

## Ordered evidence ledger

| Order | Result/document | Required contents | Authority and effect |
|---:|---|---|---|
| 0 | Precollection gate checklist | exact candidate SHA/tree; preregistration identity; local custody receipt validation; runner/analysis lock checks | GitHub and controller; blocks collection if incomplete |
| 1 | Collection-start receipt | authorization identity; UTC start; candidate and environment fingerprints; no outcomes | collection evidence only |
| 2 | Per-seed execution record | seed; topology/failure cell counts; runner/environment fingerprints; per-seed integrity sidecar | bounded operational record |
| 3 | QC ledger | expected 50 seeds × 45 cells = 2,250 observations; duplicates; missing-cell checks; schema checks | `FAIL_CLOSED_NO_CONFIRMATORY_ANALYSIS` on any required defect |
| 4 | Dataset-lock receipt | dataset digest; manifest digest; sidecar inventory; candidate binding; structural lock time | required before unblinding |
| 5 | Blinding/unblinding decision record | dataset-lock reference; custody/recovery status; explicit unblinding decision; no plaintext secret material | separate authorization only |
| 6 | Materialization receipt | exact public-key/certificate match; input digest; mapping-materialization status; no key/passphrase | required before primary analysis |
| 7 | Primary-analysis authorization record | locked-input receipt; locked analysis identity; explicit authorization identity | separate authorization only |
| 8 | Locked analysis result record | point estimate; interval; bootstrap identity; all prespecified classifications; exact input and code identities | bounded Epoch 002 result only |
| 9 | Interpretation note | confirms claim ceiling, limitation statements, independent/nonindependent status, and no cross-epoch pooling | communication layer, not new evidence |

## Required fields in every retained result record

- `record_type` and schema version;
- protocol ID and epoch;
- immutable subject identity: commit/tree, workflow run ID, artifact ID, or SHA-256;
- generation time in UTC;
- producing system and tool version/commit;
- evidence scope and explicit non-effects;
- status: `PASS`, `FAIL`, `BLOCKED`, `STALE`, `UNVERIFIED`, `NOT_RUN`, or `NOT_APPLICABLE`;
- references to predecessor records required by the ordered ledger;
- `authorization_effect` and `scientific_state_effect`.

Records MUST NOT contain a private key, passphrase, API token, unencrypted topology-mapping material, or other recoverable secret.

## QC and stop rules

Before dataset lock, the QC ledger must prove:

1. exactly 50 permitted successor seeds;
2. exactly five preregistered topologies and nine preregistered failure counts;
3. exactly one record per seed/topology/failure cell;
4. exactly 2,250 observations;
5. no duplicate cells;
6. strict boolean `ffcr_success`;
7. bound algorithm and environment fingerprints;
8. one integrity sidecar per seed.

Any missing, duplicate, malformed, unbound, or unverifiable required item produces **BLOCKED/FAIL-CLOSED** status. It must not be repaired by outcome-based exclusion, replacement sampling, silent reruns, or post-hoc changes to the analysis plan.

## Analysis and interpretation boundary

The only confirmatory comparison is the preregistered PDMAL versus random-regular paired-seed estimand. The result record must retain:

- 50 paired seed effects;
- the locked 10,000-resample paired percentile bootstrap;
- the fixed bootstrap seed `20270251`;
- two-sided 95% interval;
- directional support, directional-negative, or inconclusive classification using the preregistered rules.

Other topology comparisons, failure-specific effects, and subgroup views are exploratory only. Epoch 001 outcomes are never pooled, inspected to tune Epoch 002, or used to relabel exploratory findings as confirmatory.

## Publication/release sequence

1. Release the preregistration and collection/QC receipts before any result interpretation.
2. Release the dataset-lock and authorization records before any unblinded result.
3. Release the locked analysis result with its exact code/input bindings.
4. Release the interpretation note with the limitations and claim ceiling alongside—not after—the result.
5. Never describe this lane as canonical DGAF efficacy, independent validation, production readiness, or High-Assurance evidence.

## Current gate

This plan is ready to govern documentation once the separate successor gates are met. Current state remains:

**Epoch 001 historical / unanalyzable · Epoch 002 proposal only · successor collection not authorized · canonical DGAF efficacy not established · High-Assurance not authorized / N=0.**
