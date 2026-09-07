# Solo P-30 Remediation Diagnostic Epoch 002 — Preregistration

## Status

`PREREGISTERED / NON_EMPIRICAL_ENGINEERING_DIAGNOSTIC / SCIENTIFIC_N_INCREMENT=0`

This record is prospective with respect to remediation diagnostic epoch 002. It does not alter, erase, reinterpret, or pool Solo final experiment 001.

## Why a new epoch is required

Solo final experiment 001 retained and analyzed 50 seeds / 9,000 observations, but all 2,250 DGAF-condition cells failed closed. Source tracing established that the PDMAL adapter did not populate the required P-30 Apogee confidence substrate. The default `confidence=0.0` therefore produced grade `D`; the designated P-30 semantics map `D -> KILL`, causing deterministic fail-closed termination before the intended DGAF consensus behavior could be tested.

Experiment 001 remains permanent apparatus-falsification evidence. It is not eligible for deletion, positive relabeling, or pooling with this remediation epoch.

## Diagnostic question

> If the missing P-30 interface is populated with the lowest passing value already defined by the designated P-30 grade ladder, can the remainder of the DGAF treatment execute, or does another deterministic treatment-binding defect become visible?

This is an engineering-diagnostic question, not an efficacy hypothesis.

## Fixed P-30 diagnostic fixture

- Binding ID: `SYNTHETIC_MINIMUM_PASSING_P30_FIXTURE_V1`
- Confidence: exactly `0.45`
- Expected designated grade: `C`
- Expected P-30 gate result: `PASS`
- Real/calibrated Apogee confidence: **NO**
- Proxy for real confidence: **NO**
- Efficacy interpretation allowed: **NO**

The value `0.45` is chosen only because it is the lowest passing threshold in the already-designated P-30 S/A/B/C/D ladder. It was not selected from experiment 001 outcomes and must not be tuned after this record.

## Diagnostic matrix

- Conditions: DGAF only
- Seeds: `20260819`, `20260820`
- Topologies: canonical five
- Failure counts: canonical nine (`0,1,2,3,4,5,6,8,10`)
- Total diagnostic trials: `2 × 5 × 9 = 90`
- Scientific empirical N increment: `0`

The diagnostic intentionally excludes null/simple/static comparisons, blinding, bootstrap inference, and directional-support analysis. It may inspect execution status, iteration count, deviation, gate failures, and final consensus state solely to identify engineering defects.

## Decision rule

1. If P-30 itself still emits KILL under the fixed fixture, epoch 002 FAILS and no empirical rerun is authorized.
2. If another required gate produces systematic fail-closed behavior, record that gate/binding defect and stop. No empirical rerun is authorized.
3. If the DGAF diagnostic executes substantively across the matrix without a new deterministic binding defect, epoch 002 may support a separate proposal for a fresh blinded Solo empirical epoch.
4. No diagnostic outcome can retroactively validate experiment 001 or count toward an efficacy sample.

## Non-promotion boundary

This diagnostic cannot establish canonical DGAF efficacy, real P-30 calibration, independent validation, High-Assurance acceptance, production readiness, or external certification. Any later empirical epoch must declare its P-30 binding explicitly and remain distinct from experiment 001 and this engineering diagnostic.
