# DGAF/PDMAL v0.7.6 Solo Pilot Track

> **Current-authority overlay — 2026-09-07:** The original Solo-track definition below is historical design authority, not reusable execution authorization. A 2-seed blinded Solo QC collection was completed, followed by Solo final experiment 001 (50 seeds / 9,000 observations). Experiment 001 exposed a deterministic missing P-30 treatment binding before the intended DGAF treatment behavior could be evaluated and is retained as **apparatus-falsification evidence, not efficacy evidence**. The experiment-001 authorization is consumed. The epoch-002 P-30 engineering diagnostic passed at scientific N increment 0. **No fresh Solo empirical epoch is authorized. Issue #369 controls the unresolved empirical P-30 binding.** Current machine authority is recorded in `docs/GOVERNANCE/SOLO_EPOCH_AUTHORITY_V1.json` and is fail-closed at `NOT_AUTHORIZED`.

**Original definition status:** TRACK DEFINED  
**Current execution status:** EXPERIMENT 001 EXECUTED / APPARATUS-FALSIFICATION EVIDENCE / EXECUTION AUTHORITY RETIRED  
**Fresh Solo empirical epoch:** NOT AUTHORIZED  
**Canonical High-Assurance empirical N:** 0  
**Purpose:** preserve a bounded developer-run empirical path without falsely satisfying the separate High-Assurance Track, while keeping each empirical epoch bound to its own valid apparatus and authorization.

## Why this track exists

The High-Assurance Track intentionally depends on external or independently controlled facts: independent security review, real Confidential Space qualification, independently retained production authority/custody, protected continuity acceptance, final independent verification, and repository-administration enforcement.

Those requirements remain valid for **high-assurance / independently validated** claims. The narrower Solo question was intended to ask whether a frozen PDMAL/DGAF apparatus produced useful behavior worth further validation without claiming independent assurance.

The Solo Pilot changes the **scope of permissible claims**, not the underlying evidence standards. A developer-run execution can still falsify its apparatus. Execution alone does not make the resulting observations valid efficacy evidence.

## Two-track model

| Track | Can one developer complete it? | Empirical execution | Permitted claim ceiling |
|---|---:|---:|---|
| Solo Pilot | Potentially, after a separately valid freeze/authorization for that epoch | Yes, only under the exact epoch contract | Developer-run empirical evidence whose validity is limited by the actual apparatus and verification obtained |
| High-Assurance | No by design | Yes, only after its original gates | Independently reviewed / high-assurance claims supported only by evidence actually obtained |

The tracks do not collapse into one another. Solo evidence does not satisfy #277, #295, #310, #316, or #320 and does not establish High-Assurance P4/P8/P9 closure.

## Historical Solo Pilot prerequisites

The following requirements governed the original Solo execution sequence. They remain useful design constraints but **do not themselves authorize a successor epoch**:

1. **Exact code freeze:** choose one exact clean repository commit and bind the full 40-character SHA in `PDMAL_FROZEN_COMMIT_SHA`.
2. **Self-freeze assertion:** set `PDMAL_PROTOCOL_FROZEN=1` only after deciding not to change protocol/executor/analysis-relevant behavior during the bounded run.
3. **Explicit epoch authorization:** authorization must be deliberate and specific to the exact bounded run; experiment-001 authorization may not be reused.
4. **Limitations acknowledgement:** acknowledge that Solo output is not independent review, Confidential Space evidence, independently retained custody evidence, or High-Assurance authorization.
5. **No false High-Assurance assertion:** `PDMAL_PILOT_AUTHORIZED` must remain absent/not `1` in Solo mode unless the separate High-Assurance contract is actually satisfied.
6. **Protected blinding:** provide a blinding key of at least 32 characters through the accepted epoch custody mechanism; do not commit the key.
7. **Durable retention:** retain evidence outside the transient working output directory under the epoch-specific custody contract.
8. **No outcome-dependent protocol edits:** any protocol-affecting change after freeze invalidates that frozen run identity and requires a new candidate/freeze/authorization cycle.
9. **Constitutive treatment bindings must be explicit:** every required DGAF gate must receive its designated substrate. Missing evidence must fail closed rather than silently receiving a proxy.

For a successor Solo epoch, a commit cannot truthfully contain its own Git SHA in an authority record because adding that SHA changes the commit. The current runner therefore uses a non-circular **two-identity contract**: first freeze the exact apparatus commit; then create one direct-child authorization-envelope commit that changes only `docs/GOVERNANCE/SOLO_EPOCH_AUTHORITY_V1.json` and names the parent apparatus SHA. The runner verifies the direct-parent relationship and one-file diff before empirical collection. The empirical artifact remains bound to the apparatus SHA; the run summary retains the authorization-envelope SHA and authority-record digest.

## Experiment-001 finding and consequence

Solo final experiment 001 satisfied the mechanics needed to collect and retain 50 seeds / 9,000 observations, but the DGAF treatment path had a constitutive P-30 defect: the adapter did not populate Apogee confidence, leaving the restored default `confidence=0.0`, which grades `D` and maps to `KILL`.

Therefore:

- the collected experiment-001 records remain real retained observations of the faulty apparatus;
- they are **not eligible for positive or negative DGAF efficacy inference**;
- they must not be repaired in place, positively relabeled, deleted, or pooled into a successor empirical epoch;
- a later N=0 diagnostic using synthetic confidence `0.45` established only that the remainder of the DGAF path can execute when the missing substrate is populated;
- the synthetic diagnostic fixture is not an empirical P-30 source;
- Issue #369 must be resolved before a fresh Solo empirical proposal can be considered.

## Execution identity

Historical Solo artifacts use the distinct experiment identity:

`PDMAL-SOLO-PILOT-V1`

High-Assurance artifacts use:

`PDMAL-PILOT-V1`

This difference is deliberate and machine-visible. A successor Solo epoch must also carry a new explicit epoch identity and must not masquerade as experiment 001. The runner obtains that successor identity from the committed repository authority record rather than from the historical experiment constant.

A successor Solo execution has two Git identities with different meanings:

- **apparatus commit SHA** — the frozen protocol/executor/analysis-relevant code identity and the `frozen_commit_sha` recorded in empirical artifacts;
- **authorization-envelope commit SHA** — the direct child that changes only the authority record from fail-closed state to the explicit epoch grant. This SHA and the authority-record SHA-256 are retained in the summary/provenance record.

## What valid Solo evidence may support

If a future epoch is separately preregistered, authorized, executed, and its apparatus remains valid, accurate language may include:

- "Developer-run empirical experiment executed against exact frozen apparatus commit `<sha>`."
- "The Solo epoch produced `<N>` retained observations under its preregistered/frozen apparatus."
- "The authorization envelope was separately provenance-bound and changed no apparatus file."
- "Results are developer-run and provenance-bound, not independently verified."
- "Independent security review and Confidential Space/high-assurance custody remain future validation work."

Those statements are conditional on the apparatus actually being valid for the claim. Experiment 001 currently supports apparatus-falsification claims, not DGAF efficacy claims.

## Claims Solo evidence must not support

A Solo run does **not** establish any of the following unless separately evidenced:

- independent security review;
- independent verification;
- real Google Confidential Space qualification;
- production Mode-T custody/admission acceptance;
- independently retained R/A/C authority;
- High-Assurance P4 closure;
- High-Assurance P8/P9 completion;
- repository preventive enforcement;
- production readiness or external certification.

A Solo run also does not establish efficacy when a constitutive treatment-binding defect prevents the intended treatment from being exercised.

## Empirical-status semantics

Keep three quantities distinct:

1. **Retained observations** — records physically collected under a run, including records from a later-falsified apparatus.
2. **Efficacy-eligible evidence** — observations whose apparatus/treatment binding remains valid for the intended comparison.
3. **Canonical High-Assurance empirical N** — observations collected only under the separately authorized High-Assurance sequence.

For experiment 001, retained observations exist, but its DGAF-condition results are not efficacy-eligible because the intended treatment was not exercised. Canonical High-Assurance empirical N remains `0`.

Current recommended wording:

> SOLO EXPERIMENT 001 EXECUTED · APPARATUS-FALSIFICATION EVIDENCE · NOT EFFICACY EVIDENCE · EXECUTION AUTHORITY RETIRED · FRESH SOLO EPOCH NOT AUTHORIZED

## Successor-epoch gate

A successor Solo epoch must not be started merely by setting the historical Solo environment variables. The current committed authority record is `docs/GOVERNANCE/SOLO_EPOCH_AUTHORITY_V1.json`; while it says `NOT_AUTHORIZED`, the runner must reject empirical Solo execution regardless of environment-variable values.

A future authorization requires a new prospective repository state that, at minimum:

1. resolves Issue #369 with an explicit, reproducible, non-circular empirical P-30 confidence binding;
2. validates that binding at scientific N increment 0;
3. declares the exact apparatus dependencies, analysis-relevant configuration, successor epoch identity, blinding/custody model, and schedule;
4. preserves non-pooling from experiment 001;
5. freezes the exact apparatus commit before authorization;
6. creates a single direct-child authorization-envelope commit that changes only `SOLO_EPOCH_AUTHORITY_V1.json`, names the exact parent apparatus SHA and successor epoch ID, and records `GRANTED` only after the prior checks pass;
7. passes the fail-closed authority/envelope tests before any empirical execution trigger is introduced.

Until then: `FRESH_SOLO_EMPIRICAL_EPOCH_NOT_AUTHORIZED`.
