# DGAF Documentation Gap Audit

## Status

Audit performed before empirical execution. This document records documentation gaps that must be resolved or explicitly accepted before protocol freeze and pilot authorization.

## Findings

| Area | Status | Required action |
|---|---|---|
| P6a CORS verification | CLOSED | Verified run `32092041579`, artifact `9308650112`; no further P6a work required. |
| PDMAL experiment protocol | PRE-FREEZE | Resolve all protocol fields with concrete values and freeze with commit SHA/timestamp before any seed generation. |
| Topology/baseline matrix | PARTIALLY SPECIFIED | Freeze exact implementation identifiers/versions for Null, Simple, Static, DGAF, DGAF+PDMAL conditions and mapping to blinded labels. |
| Primary endpoint | OPEN | Name the exact metric, formula, denominator, directionality, aggregation rule, and decision rule. |
| Secondary endpoints | OPEN | Define exact metrics, formulas, aggregation, and multiplicity treatment where applicable. |
| RNG specification | OPEN | Freeze exact RNG libraries/algorithms, stream derivation, seed list generation, and separation between trial/failure/order/analysis streams. |
| Trial ordering/randomization | OPEN | Freeze deterministic ordering/randomization procedure and reproducibility command. |
| Failure/recovery semantics | OPEN | Freeze exact injected failure model, recovery/rerouting behavior, and what counts as a failure/recovery event. |
| Exclusion rules | OPEN | Enumerate objective exclusion criteria and handling of invalid/missing trials. |
| Stopping rules | OPEN | Define pilot/final stopping boundaries and who/what can authorize termination. |
| Statistical analysis plan | OPEN | Specify primary test/model, effect size, uncertainty interval, multiple-comparison handling, missing-data treatment, and sensitivity analyses. |
| Sample-size rule | OPEN | Define how pilot variance maps to the final sample size; prevent post-hoc favorable target selection. |
| Blinding/unblinding | PARTIALLY VERIFIED | Secret is operational; freeze exact blinded-label mapping, custody, dataset-freeze gate, and authorization procedure for unblinding. |
| Pilot acceptance criteria | OPEN | Convert feasibility checks into explicit pass/fail thresholds before the 50-seed pilot. |
| Data/artifact schema | PARTIALLY SPECIFIED | Freeze canonical raw-result schema, provenance fields, hashes, artifact naming, and retention location. |
| Evidence classification | PRESENT | Maintain separation of VERIFIED / VALIDATED / EMPIRICALLY SUPPORTED and tie any promoted claim to exact tested conditions. |
| Metrics provenance registry | LEGACY GAP | `docs/qa/METRICS_PROVENANCE.md` remains an active skeleton with unverified legacy metrics and a planned-but-not-created linter. This is not a pilot blocker if the pilot uses newly registered metrics, but it remains technical documentation debt. |
| Issue #76 | UNVERIFIED | GitHub returned 404; do not infer state until repository identity/reference is resolved. |

## Gate rule

No empirical seed generation is authorized until all rows marked OPEN or PARTIALLY SPECIFIED that affect the pilot are resolved and the protocol is frozen with a commit SHA and timestamp.

## Evidence boundary

This audit identifies documentation completeness requirements. It does not constitute evidence that PDMAL is effective.
