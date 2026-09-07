# Legacy Apogee Runtime Identity Migration — 2026-09-07

## Status

`NONCANONICAL_ID_ASSIGNED / RETIRED_FROM_CANONICAL_DGAF_TREATMENT / HISTORICAL_COMPATIBILITY_PRESERVED / NEW_CANONICAL_EMPIRICAL_EPOCH_STILL_NOT_AUTHORIZED`

This is the follow-up semantic migration required by issue #374 and the merged P-30 authority reconciliation in PR #375 (`3a0bf4f864b7ff43af390daec65ead8c76588d1e`). It is non-empirical.

## Decision

The historical scalar-confidence `ApogeeReviewer` mechanism is assigned the explicit non-canonical identity:

`LEGACY_APOGEE_RUNTIME_CONFIDENCE_GATE_V1`

It is **not P-30** and is **retired from any future canonical DGAF PDMAL treatment**.

Canonical **P-30 — Apogee-Attestation-Gate** remains:

`S035_P11_11Q_ATTESTATION`

The canonical P-30/11Q gate is a governance-ready/canonical-promotion attestation. It remains **outside per-turn PDMAL consensus dynamics** unless a future change separately specifies and validates a non-circular runtime 11Q measurement contract.

## Why this migration is non-destructive

Historical code, issue #165, and experiment records used the P-30 label for the restored scalar ladder. Those records are preserved as provenance. They are not rewritten or deleted.

A new dependency-free identity map, `experiments/pdmal_pilot/legacy_apogee_runtime_gate.py`, assigns the distinct identity and records symbolic references to the historical state/hook implementation. It deliberately does **not** import, wrap, or execute the historical pilot stack. This makes future references able to distinguish the runtime mechanism without altering experiment 001, diagnostic Epoch 002, Epoch 003, or their dependency surfaces.

## Historical compatibility surfaces audited

| Surface | Current role | Migration treatment |
|---|---|---|
| `components/ensemble_v17.py::ApogeeReviewer` | historical scalar S/A/B/C/D reviewer | preserved historical implementation |
| `experiments/pdmal_pilot/pdmaltgl_gate_binding.py::ApogeeAttestationState` | restored scalar substrate | preserved compatibility symbol; not canonical P-30 authority |
| `experiments/pdmal_pilot/pdmaltgl_gate_binding.py::build_apogee_hook` | restored scalar hook, D→KILL under #165 | preserved compatibility symbol; not permitted in future canonical treatment under P-30 identity |
| `experiments/pdmal_pilot/dgaf_tgl_adapter.py` | historical seven-gate apparatus wiring | historical apparatus lineage; future canonical treatment requires a separately identified profile |
| `experiments/pdmal_pilot/p30_remediation_diagnostic.py` | Epoch 002 diagnostic | immutable historical diagnostic semantics |
| `experiments/pdmal_pilot/run_p30_variant.py` | Epoch 003 synthetic variant runner | immutable historical experimental identity |
| `.github/workflows/pdmal-solo-p30-variant-execution.yml` | Epoch 003 execution lane | historical synthetic-variant lane; not reusable as canonical-DGAF authorization |
| `experiments/pdmal_pilot/test_p30_variant_track.py` | Epoch 003 fail-closed controls | retained historical tests |
| `experiments/pdmal_pilot/test_restore_five_gates_parity.py` | restoration parity evidence | retained historical parity evidence |

## Issue #165 interpretation

Issue #165 remains valid evidence that, on 2026-08-31, the operator designated the scalar runtime semantics `S/A/B/C/D`, historical S-grade gold-star behavior, and `D → KILL` for the restoration work.

After PR #375, #165 is **not** evidence that this scalar mechanism supersedes the S035 canonical P-30/11Q contract. A clarification comment was appended to #165 rather than rewriting the historical decision.

## Canonical-treatment consequence

A future canonical DGAF PDMAL apparatus must not silently reuse `LEGACY_APOGEE_RUNTIME_CONFIDENCE_GATE_V1` as P-30.

For canonical-treatment design:

1. canonical P-30/11Q is treated as an external qualification/promotion gate, not a per-turn experimental state variable;
2. the legacy scalar runtime gate is excluded from the canonical treatment profile unless explicitly studied as a named non-canonical variant;
3. no 11Q percentage is converted into runtime confidence without a separate normative bridge and disjoint calibration evidence;
4. no `agent_values`, FFCR outcome, topology, default constant, phi constant, or synthetic fixture may supply a value labeled calibrated P-30 confidence;
5. historical seven-gate experiments remain historical and unpooled with any future canonical-treatment experiment.

## What this does not authorize

This migration does not itself define the replacement canonical experimental profile. It therefore does **not** authorize a new empirical run.

The next required work is a **non-empirical canonical-treatment profile** that makes the P-30 external-attestation boundary explicit, proves the remaining runtime gates execute under that profile, and passes failure-mode/parity testing before any new preregistration.

## Decision boundary

`CANONICAL_P30_AUTHORITY = S035_P11_11Q_ATTESTATION`

`CANONICAL_P30_LOCATION = EXTERNAL_GOVERNANCE_PROMOTION_ATTESTATION`

`LEGACY_RUNTIME_SCALAR_GATE_ID = LEGACY_APOGEE_RUNTIME_CONFIDENCE_GATE_V1`

`LEGACY_RUNTIME_SCALAR_GATE_CANONICAL_TREATMENT_STATUS = RETIRED_FROM_CANONICAL_DGAF_TREATMENT`

`NORMATIVE_11Q_TO_RUNTIME_CONFIDENCE_BRIDGE = NOT_ESTABLISHED`

`NEW_CANONICAL_DGAF_EMPIRICAL_EPOCH = NOT_AUTHORIZED_PENDING_NONEMPIRICAL_CANONICAL_TREATMENT_PROFILE`
