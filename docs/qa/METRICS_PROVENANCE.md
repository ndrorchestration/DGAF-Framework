---
status: ACTIVE_FAIL_CLOSED
authority: Both
owner: DGAF PMO
last_verified: 2026-09-04
machine_registry: docs/qa/METRICS_PROVENANCE.json
validator: scripts/lint_provenance.py
---

# Metrics Provenance Registry

This record is the human-readable companion to `docs/qa/METRICS_PROVENANCE.json`. The machine registry is the promotion source of truth.

## Control rule

A historical value may remain in the repository without being treated as current verified evidence. A metric may be promoted to **VERIFIED** only when:

1. its definition, calculation, unit/range, corpus, baseline, configuration, and source commit are identified;
2. an exact workflow run, retained artifact, and timestamp are bound to the metric;
3. a runnable reproduction command is present;
4. every declared upstream instrument dependency is itself **VERIFIED**; and
5. `scripts/lint_provenance.py` accepts the registry.

If any upstream dependency is unresolved, deprecated, shadow-only, or contradictory, the derived metric is fail-closed and cannot be promoted to VERIFIED.

## Current disposition

| Metric ID | Pattern | Historical value | Current epistemic status | Blocking condition |
|---|---|---:|---|---|
| `M-P10-SPEED` | P-10 | +340% | HISTORICAL_UNVERIFIED | timing/decision-speed instrument unresolved |
| `M-P11-HUMAN-REVIEW` | P-11 | -21% | HISTORICAL_UNVERIFIED | P-11 instrument deprecated |
| `M-P29-LATENCY` | P-29 | -62% | HISTORICAL_UNVERIFIED | benchmark/run identity unresolved |
| `M-P29-TOKENS` | P-29 | -42% | HISTORICAL_UNVERIFIED | benchmark/run identity unresolved |
| `M-P34-945` | P-34 | 94.5% | DEPENDENCY_BLOCKED | P-11 deprecated; P-11Q shadow; value semantics differ across legacy surfaces |
| `M-P36-MTTE` | P-36 | -58.3% | HISTORICAL_UNVERIFIED | MTTE benchmark identity unresolved |
| `M-P37-PRECISION` | P-37 | 96% | HISTORICAL_UNVERIFIED | evaluation identity unresolved |
| `M-P39-TRANSFER` | P-39 | 95% | HISTORICAL_UNVERIFIED | transfer evaluation identity unresolved |
| `M-P40-F1` | P-40 | 82.6% | HISTORICAL_UNVERIFIED | cross-model evaluation identity unresolved |

The P-34 94.5% value is intentionally preserved as a historical attestation/metric claim. This registry does **not** assert that the value is false; it records that the current repository does not provide a dependency-clean, independently reproducible evidence chain sufficient for VERIFIED status.

## Required machine fields

Each metric record carries or explicitly leaves unresolved:

- stable metric and pattern identifiers;
- precise definition and calculation method;
- unit and score range;
- dataset/corpus and baseline;
- parameter/configuration identity;
- source commit;
- workflow run, retained artifact, and timestamp;
- reproduction status and command;
- upstream dependencies;
- epistemic status; and
- source surfaces where the historical claim appears.

Null evidence fields are deliberate fail-closed markers. They are not placeholders that permit promotion.

## Enforcement

Run:

```bash
python scripts/lint_provenance.py
python -m unittest discover -s tests -p 'test_lint_provenance.py' -v
```

`PPTL CI` runs both checks. The validator exits non-zero for schema violations, duplicate identities, unknown dependencies, missing known metric records, or any attempt to mark a metric VERIFIED without complete reproducibility evidence and VERIFIED upstream dependencies. It may emit warnings when active prose uses current-looking promotion language around an unresolved historical value; those warnings do not rewrite historical records.

## Scientific boundary

This provenance repair changes evidence classification and enforcement only. It does not create new measurements, validate historical headline values, establish PDMAL freeze, grant pilot authorization, unblind conditions, or increase empirical N.
