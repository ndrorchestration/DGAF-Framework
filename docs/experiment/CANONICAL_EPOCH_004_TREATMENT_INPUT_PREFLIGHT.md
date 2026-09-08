# Canonical Solo Empirical Epoch 004 — Treatment-Input Preflight

## Status

`NONEMPIRICAL PREFLIGHT / EMPIRICAL EXECUTION NOT AUTHORIZED / SCIENTIFIC N INCREMENT = 0`

This gate follows the merged proposal-level preregistration for `PDMAL-SOLO-CANONICAL-EPOCH-004`. It does not collect observations, create a blinding key, expose a workflow-dispatch surface, authorize a runner, or inspect any empirical outcome.

## Purpose

The purpose is to prevent a recurrence of experiment 001's treatment-binding failure by requiring every constitutive treatment input and exact source identity to be verified before an empirical runner can even be proposed for authorization.

The preflight binds and verifies:

- frozen Epoch 004 preregistration merge `ae854edf565c903bf799f243841799819333d920`;
- canonical profile `DGAF_CANONICAL_PDMAL_PROFILE_CANDIDATE_V1` and exact profile blob `133d7b71c9e829d5461e7c911527c6b2b10ba9ae`;
- canonical external P-30 authority `S035_P11_11Q_ATTESTATION` at TGL step 8;
- retirement/prohibition of `LEGACY_APOGEE_RUNTIME_CONFIDENCE_GATE_V1` from the canonical profile;
- developer self-attested/non-independent 11Q qualification SHA-256 `4d0346f6a05046f03ce5a399d1dd4de2d31b69f683988fe9af20802d2c062d78`;
- canonical required TGL step set `{1,2,3,4,5,6,8}` directly from current source;
- successful canonical treatment-reachability evidence from PR #380 / run `34176977560` / artifact `10037645166`;
- unchanged locked primary statistical source blob `a269ed226b1d261663994fc3ef0e8a1a96da6cd3` and analysis-config SHA-256 `6cab3f1ed6d4e040141598d293628dbab52442234c519b3e231b76a2896f09a8`;
- fresh seed panel `20261001..20261050`, collision-free against experiment 001 and Epoch 003;
- 9,000-observation matrix identity if a later, separately authorized collection occurs.

## Fail-closed rule

Any mismatch in profile identity/blob, qualification bytes/class, required TGL steps, analysis identity, reachability evidence identity, seed panel, or collection-control boundary fails the preflight. Existing governed profile, qualification, and preregistration validators are re-run rather than reimplemented.

A passing result is classified only as:

`PASS_NONEMPIRICAL_TREATMENT_INPUT_PREFLIGHT_ONLY`

It establishes that the preregistered canonical treatment inputs are internally consistent and present on the tested source. It does not establish efficacy, independent verification, production readiness, High-Assurance acceptance, or empirical authorization.

## Next gate after a successful merge

Only after exact-head CI and merge of this preflight may work proceed to a separately governed empirical runner/collection contract. That later work must still preserve fresh blinding, exact frozen execution identity, structural dataset locking before unblinding, separate post-lock unblinding authorization, no historical pooling, and the Solo/non-independent claim ceiling.

`EMPIRICAL_EXECUTION = NOT_AUTHORIZED`

`SCIENTIFIC_N_INCREMENT = 0`

`HIGH_ASSURANCE = UNCHANGED / NOT_AUTHORIZED / N=0`
