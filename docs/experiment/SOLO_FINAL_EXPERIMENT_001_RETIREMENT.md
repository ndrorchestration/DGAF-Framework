# Solo Final Experiment 001 — Execution-Lane Retirement

## Status

`EXPERIMENT_001_RETIRED / APPARATUS_FALSIFICATION_EVIDENCE / FRESH_SOLO_EMPIRICAL_EPOCH_NOT_AUTHORIZED`

This record retires the **execution authority** for Solo final experiment 001. It does not delete, rewrite, invalidate, or conceal the historical experiment, its branch, its workflow run, its blinded artifacts, or its apparatus-falsification result.

## Historical execution identity

- Historical execution branch: `solo-experiment/run-20260907-001`
- Historical run-request commit: `9db20dd2af4ec6a7e23bb8c078e744862109ac4e`
- Parent containing the original execution workflow: `0eb0c76f8f4ca49c87ecd0286a06d8b6930ae0ed`
- Historical authorization string embedded in the original lane: `GRANTED_BY_DEVELOPER_AFTER_BLINDED_QC`
- Historical QC authority record: `docs/experiment/SOLO_PILOT_QC_ADJUDICATION_2026-09-07.md`

These identities remain historical provenance. The branch is not re-pointed by this retirement record.

## Why retirement is required

The original `.github/workflows/pdmal-solo-final-experiment.yml` treated a push to `solo-experiment/run-*` containing the exact experiment-001 request as sufficient to start the 50-seed Solo execution.

That authorization was valid only for the experiment-001 decision sequence then in force. The resulting experiment subsequently exposed a deterministic P-30 treatment-binding defect: the required Apogee confidence substrate was absent, defaulted to `0.0`, graded `D`, and caused `D -> KILL` before the intended DGAF consensus treatment behavior could be tested.

Experiment 001 is therefore retained as apparatus-falsification evidence rather than efficacy evidence. PR #366 then ran the separate N=0 P-30 remediation diagnostic; PR #367 retained its adjudication. The diagnostic PASS does not revive the old experiment-001 authorization.

## Retirement action

On current mainline, `.github/workflows/pdmal-solo-final-experiment.yml` is converted to a **validation-only retirement guard**:

- no `push` trigger;
- no `solo-experiment/run-*` execution trigger;
- no empirical runner invocation;
- no `PDMAL_SOLO_PILOT_AUTHORIZED=1` injection;
- no reuse of `GRANTED_BY_DEVELOPER_AFTER_BLINDED_QC` as current authority;
- no data collection or scientific N advancement.

This prevents the current lineage from treating experiment-001 authorization as a reusable token for a later epoch.

## P-30 blocker for any successor epoch

Issue #369 is the controlling blocker for a possible Solo epoch 003. A successor empirical proposal must first define and verify a prospectively bound, reproducible, non-circular P-30 confidence source. The following are explicitly insufficient without new authoritative evidence:

- the synthetic epoch-002 fixture at `0.45`;
- the legacy `/api/triad` `PHI_STAR` default;
- consensus-derived or outcome-derived proxies;
- a historical Apogee/11Q score from an unrelated artifact/session;
- post-hoc tuning against experiment-001 results.

Only after the P-30 source is semantically reconciled, candidate-bound, and validated at scientific N increment 0 may a new blinded empirical epoch be separately preregistered and considered for authorization.

## Evidence and preservation boundary

This retirement changes future execution authority only.

It does **not**:

- delete the historical run branch or commit;
- erase the 50-seed / 9,000-observation experiment-001 record;
- convert experiment 001 into efficacy evidence;
- change the epoch-002 diagnostic into empirical evidence;
- authorize unblinding or a successor empirical run;
- affect canonical High-Assurance P4/P7/P8/P9, freeze, authorization, or empirical N.

## Current decision

- Solo final experiment 001: `EXECUTED / APPARATUS_FALSIFICATION_EVIDENCE / EXECUTION AUTHORITY CONSUMED`
- P-30 remediation diagnostic epoch 002: `PASS / NON_EMPIRICAL / SCIENTIFIC_N_INCREMENT=0`
- Issue #369: `OPEN / P-30 EMPIRICAL BINDING BLOCKER`
- Fresh Solo empirical epoch: `NOT AUTHORIZED`
- Canonical High-Assurance PDMAL: `PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0`
