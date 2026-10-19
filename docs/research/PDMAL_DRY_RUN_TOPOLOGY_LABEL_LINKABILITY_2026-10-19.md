# PDMAL structural dry-run topology-label linkability — 2026-10-19

**Status: REPRODUCED IN SAME-SYSTEM SYNTHETIC TEST / TOPOLOGY CONFIDENTIALITY NOT ESTABLISHED.**

**Scope:** [#1399](https://github.com/ndrorchestration/DGAF-Framework/issues/1399), the `experiments/pdmal_topology` structural-instrumentation dry-run only, on protected `main` `1a95b94332dffb404c5a3ce026d70781a8c10b90`. This note is *not* a modification to the canonical preregistered empirical protocol, a repair to retained data, a new freeze artifact, or an independent security assessment. Scientific N remains 0.

## Observed source mechanism

- `artifacts.blind_label` uses a keyed HMAC-SHA256-prefix pseudonym, which prevents disclosure of the original topology string through the label **by direct visual inspection alone**.
- `artifacts.blind_rows` changes only the `topology` field; seed, failure count, failure-node list, and six structural measurements remain available in the candidate dry-run CSV.
- The simulator is deterministic for disclosed seeds. A source-aware observer can independently reconstruct named candidate rows, match the remaining public field values, and aggregate candidate sets across records that share a pseudonym. **This need not recover, predict, or brute-force the HMAC key.**

## Bounded non-secret reproduction

`tests/test_pdmal_structural_masking_linkability.py` runs two separate, five-seed synthetic generator invocations. It uses two unrelated **disposable dummy keys** and shuffles published masked rows, so source-row index correspondence is not part of the attack. For each pseudonym, the test intersects topology candidates from matching source-known reference rows. The code deliberately does not read any GitHub secret, protected artifact, recorded scientific result, or retained custody file.

| Accessible fields | Classes attributed out of 5 | Masked rows attributed out of 225 |
| --- | ---: | ---: |
| Seed, failure count | 0 | 0 |
| Seed, failure count, failure-node list | 0 | 0 |
| Six structural metrics alone | 4 | 180 |
| Seed, failure count, metrics | **5** | **225** |
| All retained non-topology fields | **5** | **225** |

Results matched with either dummy key. Individual row fingerprints were unique in 65/225 cases with the seed/failure/metric combination; pseudonym-class aggregation extended attribution to all 225 rows. **A passed characterization test is affirmative evidence of a limitation, not evidence that concealment is effective.**

## Epistemic limits and relationships

- The result demonstrates a **source-known, deterministic structural reconstruction side channel** in the simulated dry-run data representation. It does not demonstrate a cryptographic failure of HMAC-SHA256, an attack on independently held secrets, or a release of real protected experiment rows.
- It is separate from historical [#307](https://github.com/ndrorchestration/DGAF-Framework/issues/307), a different *treatment identity* leak via order/trace in v0.7.5 pilot artifacts, repaired by #308. This dry-run finding **does not assert that the v0.7.6 canonical condition-blinding repair regressed**.
- It is separate from [#1375](https://github.com/ndrorchestration/DGAF-Framework/issues/1375), which controls expiring **Epoch 004 dataset and recoverable-key custody**. Do not fetch, reclassify, unblind, mirror, or replace those protected artifacts as part of this check.
- `pdmal-instrumentation-dry-run.yml` remains formally unclassified under [audit #777](https://github.com/ndrorchestration/DGAF-Framework/issues/777). It is secret-bearing and emits masked CSV and 14-day retained evidence, so its research-rehearsal purpose and artifact-confidentiality claims need a dedicated gate.

## Decision hold

Before accepting a stronger blinding/confidentiality claim, formally establish whether the dry-run intends **stable label pseudonymization** (which the code does) or **concealment of topology identity from someone who knows the simulator source, seeds and structural outputs** (not established and defeated in these synthetic cases). If confidentiality is required, propose a prospective, pre-authorized mitigation such as reducing the pre-release observation surface or separating protected metrics from public structural receipts. Preserve analytical relevance; do not remove outcomes or change frozen evidence solely to make this synthetic inference test fail. Independently re-run the adversarial test, enumerate what observers genuinely know, and predeclare accept/reject criteria.

**Ceilings unchanged:** `SCIENTIFIC_N_INCREMENT=0`, `INDEPENDENT_VALIDATION=NOT_ESTABLISHED`, `CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED`, `HIGH_ASSURANCE=NOT_AUTHORIZED`.

**Important: Reproducibility is local/technical; same-system test authoring, source inspection, and provider CI cannot be substituted for non-author technical acceptance.**
