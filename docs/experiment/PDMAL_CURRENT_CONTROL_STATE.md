---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-23
applies_to_sha: CURRENT_MAIN_AT_VERIFICATION
---

# PDMAL Current Control State

This is the current pre-authorization gate record. GitHub is authoritative for implementation and CI; Notion is authoritative for governance decisions. Historical evidence remains scoped to its exact tested SHA. This document describes the moving pre-freeze state and therefore does not pin a mutable main SHA.

## Current state

| Control | State | Evidence / blocker |
|---|---|---|
| Historical freeze | HISTORICAL / SUPERSEDED | `3510b86889cd341f7a7cf9ab684fd37b2fafd758` |
| Corrected runner | CANDIDATE | Exact-SHA gating and pilot artifact validation are present; runner now emits explicit `ffcr_success`; fresh candidate verification required |
| Environment lock | VERIFY | Target Python 3.12.0, NumPy 2.5.1, NetworkX 3.6.1 |
| Executor contract | PARTIAL | Stale test reconciled; fresh CI required |
| Artifact contract | PARTIAL | Pilot schema and inline validator/sidecar checks present; `ffcr_success` is an additional explicit outcome field; fresh candidate verification required |
| Topology provenance | VERIFY | Current-source fingerprint manifest restored; final candidate re-computation required |
| Runtime characterization | CLOSED FOR CHARACTERIZATION | Historical Run #14; non-empirical |
| Blinding custody | CLOSED FOR SYNTHETIC VERIFICATION | Historical synthetic custody evidence; production key custody still requires operational evidence |
| Security controls | VERIFY | Pre-authorization workflow/tests present; fresh CI required |
| Durable retention | OPEN | Archive destination and direct retrieval/hash proof not established |
| Primary contrast | ADOPTED / P7 | Full `dgaf` vs `null`; FFCR; seed-paired primary analysis |
| Analysis implementation | CANDIDATE / P8 | `experiments/pdmal_pilot/analysis.py`; paired percentile bootstrap and decision bindings specified; candidate SHA and independent verification still required |
| Analysis configuration | CANDIDATE / P8 | Canonical configuration SHA: `6cab3f1ed6d4e040141598d293628dbab52442234c519b3e231b76a2896f09a8`; final binding still required |
| Protocol identity | OPEN / P8 | Protocol reconciled to explicit `ffcr_success` and P8 boundary; exact post-commit blob SHA must be bound |
| New freeze | NOT CREATED | Historical freeze cannot be reused |
| Pilot authorization | NOT GRANTED | Separate governance decision |
| Empirical data | ZERO | No authorized pilot execution |

## Canonical predicate taxonomy

P1 Candidate integrity; P2 Execution contract; P3 Artifact contract; P4 Security/blinding integrity; P5 Provenance/reproducibility; P6 Durable evidence custody; P7 Scientific target specification; P8 Analysis lock; P9 Independent verification.

Experimental-design integrity is covered by P5 + P7 and is not a tenth predicate. Authorization is a separate governance transition after freeze verification.

## P7 closure boundary

P7 is adopted. The primary contrast is the full `dgaf` condition versus the `null` condition, using FFCR and a seed-level paired difference. The adopted P7 decision defines the treatment/reference boundary, aggregation concept, direction, exclusion/missing-data boundary, and secondary/exploratory family.

P7 adoption does not authorize execution and does not create a freeze.

## P8 progress

P8 implementation work has begun. The canonical analysis path is `experiments/pdmal_pilot/analysis.py`. It consumes validated seed artifacts only, preserves the blinded-condition boundary until explicit unblinding, rejects incomplete/duplicate matrix cells, and performs paired bootstrap over complete seed effects.

The pilot runner was amended to emit explicit `ffcr_success`, because the previous artifact recorded `final_std` but did not expose the protocol's failure-free completion outcome directly. The runner protocol version was also reconciled from `0.7.4` to `0.7.5` to match the governing matrix amendment. These are candidate apparatus changes and therefore require fresh verification before they can participate in a freeze.

The initial P8 implementation constants are now explicit: 10,000 percentile-bootstrap resamples, RNG seed `20260823`, two-sided 95% interval, alpha `0.05`, and positive-estimate/positive-CI primary support criterion. Secondary confirmatory claims use Holm if such claims are made; otherwise secondary results remain exploratory/descriptive.

Adversarial analysis tests have been added for incomplete matrices, duplicates, malformed outcome values, missing unblinding mappings, deterministic bootstrap behavior, and decision logic.

## Historical freeze boundary

`3510b86889cd341f7a7cf9ab684fd37b2fafd758` is historical evidence only. It must not be described as the current freeze of the corrected runner. If verification identifies a defect requiring an apparatus change, a new freeze must be established after repair and re-verification.

## Required next evidence events

1. Run fresh candidate CI and analysis tests on the exact current candidate.
2. Verify canonical artifact serialization and runtime validation, including the new `ffcr_success` field.
3. Bind the exact analysis implementation SHA and configuration SHA.
4. Bind the exact protocol blob SHA after the current protocol reconciliation commit.
5. Establish durable evidence custody and direct retrieval/hash evidence.
6. Reconcile topology fingerprints and environment identity on the exact candidate.
7. Derive P1–P8 from candidate-scoped evidence.
8. Execute P9 independent verification.
9. Create and verify a new freeze.
10. Obtain separate pilot authorization.

**No empirical execution is authorized by this record. N = 0.**
