# AOSS v0.6 Stage A — Primary Comparator Protocol Amendment

**Controller:** #810  
**Status:** FROZEN PRE-DATA AMENDMENT CANDIDATE / NON-AUTHORIZING  
**Amendment:** `AOSS_V0_6_STAGE_A_PRIMARY_COMPARATOR_AMENDMENT_V1`

## Why this amendment exists

The historical `AOSS_V0_5_OMR_FROZEN` decision rule is documented, but the semantic definitions and machine derivation of `O`, `M`, and `R` could not be recovered from GitHub or the canonical AOSS/Structural Epistemics records before Stage-A outcome collection. The historical reference projection `(3,1,1.0)` is not an extraction rule.

Stage A therefore must not invent O/M/R semantics. This amendment prospectively replaces that unusable confirmatory comparator with a source-native baseline whose inputs and decision rules are fully executable and frozen before any Stage-A outcomes exist.

## Replacement comparator

`AOSS_V0_6_ACP_DIRECT_EVENT_BASELINE_V1` reads only:

- manifest schema;
- manifest/run event identity;
- exact event count;
- source-native event kind.

It deliberately ignores timestamps, ordering semantics, lineage, authority, validation, provenance richness, state/detail/capability payloads, observer-derived identifiers, and all historical O/M/R variables.

Rules:

1. invalid structural identity → `HOLD`;
2. no terminal event → `HOLD`;
3. multiple terminal events → `HOLD`;
4. exactly one `task.completed` → `RECORD_OUTCOME`;
5. exactly one `task.denied`, `task.rejected`, `task.failed`, `task.cancelled`, or `task.budget_exhausted` → `ESCALATE_BLOCK`.

All categorical and identity comparisons use exact equality with zero tolerance.

Executable:

- `scripts/aoss_v0_6_stage_a_acp_direct_baseline.py`
- Git blob: `f1846d00084b9e0a1b1ddbd21999f1ce9627c4f5`

## Primary endpoint amendment

The prior endpoint `AOSS_DECISION_DIFFERS_FROM_FROZEN_OMR` is replaced prospectively by:

`AOSS_DECISION_DIFFERS_FROM_ACP_DIRECT_EVENT_BASELINE`

The estimator remains the exact finite-corpus fraction over the already frozen eligible canonical episodes. Divergence remains descriptive; it is not correctness, superiority, causal value, or a population effect.

## Epistemic boundary

This amendment occurs after the apparatus/fixture classes were designed but before any Stage-A outcome collection. It does not use injected ground-truth labels as comparator inputs and does not inspect Stage-A results. It is therefore a transparent pre-data repair to an unusable comparator definition, not a result-conditioned rewrite.

The original OMR gap record remains historical evidence that O/M/R were never recovered. It is not rewritten as though the missing derivation had been found.

## Non-effects

This amendment does not authorize Stage-A collection, establish external validation, establish AOSS/DGAF/PDMAL efficacy, increment scientific N, or alter the separately closed Track A Epoch 002 lane. If every pre-data predicate becomes bound, the only automatic state is `READY_FOR_SEPARATE_AUTHORIZATION_REVIEW`.
