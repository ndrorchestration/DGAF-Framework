# DGAF Documentation Gap Audit

## Status

Audit performed before empirical execution and updated after expert-panel adjudication. The panel has resolved the substantive protocol choices; remaining items are implementation/provenance fields required before freeze.

## Findings

| Area | Status | Required action |
|---|---|---|
| P6a CORS verification | CLOSED | Verified run `32092041579`, artifact `9308650112`; no further P6a work required. |
| PDMAL experiment protocol | PRE-FREEZE / PANEL-ADJUDICATED | Decisions are recorded in `PDMAL_EXPERIMENT_PROTOCOL.md`; freeze only after remaining operational fields and approved experimental commit are established. |
| Topology/baseline matrix | PANEL-ADJUDICATED / PROVENANCE PENDING | Candidate matrix accepted. Record exact implementation SHAs, dependency/version identifiers, generation parameters, and graph validation results for every topology. |
| Primary endpoint | RESOLVED | FFCR: completed trials without unrecovered failure / eligible trials; higher is better; prespecified contrasts with 95% CI. |
| Secondary endpoints | RESOLVED | Recovery success, recovery latency, unrecovered failures, runtime, variance, connectivity/surviving component size, protocol compliance, missing/invalid rate, gate-block frequency; `D_a`/phi/topology diagnostics exploratory. |
| RNG specification | RESOLVED / VERSION RECORD PENDING | NumPy `Generator(PCG64)` with domain-separated streams and SHA-256 seed+stream derivation. Record exact NumPy version and serialization details. |
| Trial ordering/randomization | RESOLVED | Block-randomized within seed using dedicated ordering stream; retain reproducible ordering in provenance. |
| Failure/recovery semantics | RESOLVED / TIMEOUT VALUES PENDING | Failure definition and recovery/reroute semantics fixed; exact timeout, retry count, and recovery window must be frozen from the pinned runner. |
| Exclusion rules | RESOLVED | Objective protocol violations only; retain exclusions with reasons; no outcome-based exclusion. |
| Stopping rules | RESOLVED | No efficacy stopping; only predefined safety, provenance, blinding, protocol-integrity, or catastrophic execution halts. |
| Statistical analysis plan | RESOLVED / IMPLEMENTATION PENDING | Paired FFCR comparisons, risk difference, 95% CI, prespecified primary contrast, exploratory secondary contrasts with correction. Implement exact analysis formula before freeze. |
| Sample-size rule | RESOLVED / FORMULA IMPLEMENTATION PENDING | Target power 0.80, alpha 0.05, minimum detectable risk difference 0.15; final N from pilot estimate using fixed formula/rounding rule. |
| Blinding/unblinding | RESOLVED / CUSTODY PROCEDURE PENDING | `PDMAL_BLINDING_KEY` remains secret; mapping external to analytical dataset; freeze custody and authorization procedure. |
| Pilot acceptance criteria | RESOLVED / RUNTIME CEILING PENDING | 100% attempted, 0 blinding breaches, missing/invalid <=5%, all conditions execute, no comparability-affecting deviation, runtime <= frozen ceiling. Numeric ceiling still needs characterization and freeze. |
| Data/artifact schema | RESOLVED / IMPLEMENTATION PENDING | One JSON artifact per seed with trial records + provenance; verify exact schema, naming, hashes, environment fingerprint, and retention path. |
| Evidence classification | PRESENT | Maintain VERIFIED / VALIDATED / EMPIRICALLY SUPPORTED separation and condition-specific claims. |
| Metrics provenance registry | LEGACY GAP | `docs/qa/METRICS_PROVENANCE.md` remains a separate technical-debt item and is not a pilot blocker when new pilot metrics are explicitly registered. |
| Issue #76 | UNVERIFIED | GitHub returned 404; do not infer state until repository identity/reference is resolved. |

## Remaining pre-freeze blockers

Only these implementation-dependent items remain before the protocol can legitimately enter `FROZEN` status:

1. Exact topology implementation/source SHAs and graph validation records.
2. Exact NumPy version and RNG serialization/derivation details.
3. Exact failure timeout/retry/recovery-window values from the pinned runner.
4. Final sample-size formula implementation and fixed rounding rule.
5. Final artifact schema implementation/validation and retention location.
6. Exact blinded-label custody/unblinding authorization procedure.
7. Numeric runtime ceiling based on the pinned execution environment.

These are not empirical results; they are protocol implementation/provenance controls.

## Gate rule

No empirical seed generation is authorized until the remaining blockers above are resolved, the protocol is frozen with a commit SHA and timestamp, and pilot authorization is explicitly recorded.

## Evidence boundary

This audit identifies documentation completeness and protocol controls. It does not constitute evidence that PDMAL is effective.
