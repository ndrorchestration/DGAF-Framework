# AOSS v0.6 Stage-A ingest-reference and freshness boundary

This tranche implements a **synthetic-only, non-collecting** ingest-reference contract for Issue #901.

It provides:

- an explicit same-process ingest timestamp for a supplied synthetic event;
- enforcement of the frozen Stage-A freshness bounds: maximum age **30 seconds** and maximum future skew **2 seconds**;
- deterministic canonical receipt bytes and SHA-256 identity for exact-byte replay;
- fail-closed validation against freshness relabeling, timestamp ambiguity, and boundary drift.

It does **not** import or execute the frozen ACP target, generate Stage-A outcomes, accept a collector executable or destination, perform the five-pass study replay, or establish collection execution readiness.

The retained receipt is apparatus evidence only. It demonstrates that ingest-time capture and replay mechanics can preserve the frozen timing semantics before any empirical collection path is enabled.

State boundary:

- `OUTCOME_COLLECTION_AUTHORIZED=TRUE` remains bounded and unchanged;
- `COLLECTION_EXECUTION_READINESS=NOT_ESTABLISHED`;
- `SCIENTIFIC_N_INCREMENT=0`;
- `CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED`;
- `INDEPENDENT_VALIDATION=NOT_ESTABLISHED`;
- `HIGH_ASSURANCE=NOT_AUTHORIZED`.

The next gate remains accepted executable/destination binding plus full five-bundle custody, five exact-byte replay passes, attempt invalidation, and no-retry-after-outcome-inspection enforcement before collection can be considered executable.
