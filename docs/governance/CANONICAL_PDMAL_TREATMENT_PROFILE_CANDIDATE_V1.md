# Canonical PDMAL Treatment Profile Candidate V1

Status: `NONEMPIRICAL_CANDIDATE_PROFILE / EMPIRICAL_AUTHORIZATION_FALSE / SCIENTIFIC_N_INCREMENT_0`

This candidate resolves issue #377 at the treatment-profile level without creating a new empirical lane.

## Profile identity

`DGAF_CANONICAL_PDMAL_PROFILE_CANDIDATE_V1`

Canonical P-30 remains `S035_P11_11Q_ATTESTATION` and remains external to per-turn consensus scoring. The historical scalar gate `LEGACY_APOGEE_RUNTIME_CONFIDENCE_GATE_V1` is prohibited from this profile.

## TGL step 8

TGL step 8 remains required, but its canonical-profile meaning is narrowed to **verification of a previously produced external P-30/P-11 11Q qualification artifact** bound to the exact treatment-profile source identity.

The step-8 verifier does not score 11Q, estimate confidence, or inspect scientific outcomes. It verifies:

- record type and schema;
- P-30 gate and P-11 11Q rubric identity;
- exact profile ID;
- exact frozen profile-source SHA;
- exact externally supplied SHA-256 of the qualification artifact;
- qualifying tier/result semantics;
- declared verification class.

It fails closed on missing, malformed, stale, wrong-profile, wrong-source, digest-mismatched, or nonqualifying evidence.

## Forbidden inputs

Step 8 may not use empirical outcomes, FFCR, `agent_values`, topology, failure count, a runtime confidence scalar, default constants, phi-derived constants, or synthetic confidence fixtures.

## Qualification semantics

A future qualification artifact may satisfy this candidate contract only if either:

- S-TIER: percentage >=95, Q11 >=9, result `GRANTED`; or
- A-TIER: percentage >=85, result `CONDITIONAL`, with one or more explicitly tracked open BLGs.

A developer-run artifact must identify itself as `DEVELOPER_SELF_ATTESTED_NONINDEPENDENT`. That class is sufficient only for the Solo non-empirical diagnostic gate and must never be presented as independent verification.

## Sequencing

1. Merge/freeze this candidate profile only after exact-head CI.
2. Produce a separate developer/self-attested 11Q qualification bound to the exact merged profile source.
3. Run a non-empirical matrix diagnostic proving required TGL gates execute and step 8 verifies the bound artifact. Scientific N increment remains 0.
4. Only after those gates pass may a fresh empirical epoch be proposed under a new preregistration and authorization.

No experiment 001, Epoch 002, or Epoch 003 evidence is rewritten or pooled.

`NEW_CANONICAL_DGAF_EMPIRICAL_EPOCH = NOT_AUTHORIZED`

`HIGH_ASSURANCE = UNCHANGED / NOT_AUTHORIZED / N=0`
