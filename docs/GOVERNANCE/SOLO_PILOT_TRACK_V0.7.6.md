# DGAF/PDMAL v0.7.6 Solo Pilot Track

**Status:** TRACK AVAILABLE AFTER MERGE; NOT YET EXECUTED  
**Empirical N:** 0 at definition  
**Purpose:** permit a developer-run empirical pilot without falsely satisfying the separate High-Assurance Track.

## Why this track exists

The existing High-Assurance Track intentionally depends on external or independently controlled facts: independent security review, real Confidential Space qualification, independently retained production authority/custody, protected continuity acceptance, final independent verification, and repository-administration enforcement.

Those requirements remain valid for **high-assurance / independently validated** claims. They are no longer prerequisites for the narrower question the Solo Pilot is intended to answer:

> Does the frozen v0.7.6 PDMAL/DGAF apparatus produce useful empirical behavior worth further validation?

The Solo Pilot changes the **scope of permissible claims**, not the underlying evidence.

## Two-track model

| Track | Can one developer complete it? | Empirical execution | Permitted claim ceiling |
|---|---:|---:|---|
| Solo Pilot | Yes | Yes, after explicit self-freeze and self-authorization | Developer-run empirical pilot; self-validated; not independently verified |
| High-Assurance | No by design | Yes, only after its original gates | Independently reviewed / high-assurance claims supported only by evidence actually obtained |

The tracks do not collapse into one another. Solo evidence may later be retained as exploratory/pilot evidence, but it does not satisfy #277, #295, #310, #316, or #320 and does not establish High-Assurance P4/P8/P9 closure.

## Solo Pilot prerequisites

Before setting `PDMAL_MODE=solo_pilot`, all of the following must be true:

1. **Exact code freeze:** choose one exact clean repository commit and set its full 40-character SHA in `PDMAL_FROZEN_COMMIT_SHA`.
2. **Self-freeze assertion:** set `PDMAL_PROTOCOL_FROZEN=1` only after deciding not to change protocol/executor/analysis-relevant behavior during the bounded run.
3. **Explicit Solo authorization:** set `PDMAL_SOLO_PILOT_AUTHORIZED=1` deliberately for the bounded run.
4. **Limitations acknowledgement:** set `PDMAL_SOLO_LIMITATIONS_ACKNOWLEDGED=1` to acknowledge that Solo output is not independent review, Confidential Space evidence, independently retained custody evidence, or High-Assurance authorization.
5. **No false High-Assurance assertion:** `PDMAL_PILOT_AUTHORIZED` must remain absent/not `1` in Solo mode.
6. **Protected blinding:** provide a blinding key of at least 32 characters through `PDMAL_BLINDING_KEY`; do not commit the key.
7. **Durable local retention:** configure `PDMAL_ARCHIVE_ROOT` to a durable location separate from the working output directory.
8. **No outcome-dependent protocol edits:** after the Solo freeze, any protocol-affecting change invalidates that frozen Solo run identity and requires a new freeze before additional confirmatory data.

The runner still verifies that the actual checked-out `HEAD` exactly matches `PDMAL_FROZEN_COMMIT_SHA` before empirical collection.

## Execution identity

Solo artifacts use the distinct experiment identity:

`PDMAL-SOLO-PILOT-V1`

High-Assurance artifacts continue to use:

`PDMAL-PILOT-V1`

This difference is deliberate and machine-visible. Solo mode reuses the same blinded matrix, artifact schema, sidecar verification, exact commit binding, runtime ceiling, and durable-retention primitives.

## What Solo evidence may support

After a successful run, accurate language includes:

- "Developer-run empirical pilot executed on exact frozen commit `<sha>`."
- "The Solo Pilot produced `<N>` empirical trial observations under the preregistered/frozen apparatus."
- "Results are self-validated and provenance-bound, not independently verified."
- "Independent security review and Confidential Space/high-assurance custody remain future validation work."

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

## Empirical-status semantics

Before the first successful Solo artifact is written and retained:

**SOLO TRACK AVAILABLE · SOLO NOT YET AUTHORIZED/EXECUTED · N=0**

After a successful retained Solo run, it is valid to increase the **Solo empirical N** by the actual number of completed empirical trial observations. This does not change the High-Assurance track's acceptance state.

Recommended status wording after execution:

**SOLO PILOT EXECUTED · DEVELOPER-RUN · SELF-VALIDATED · NOT INDEPENDENTLY VERIFIED · HIGH-ASSURANCE GATES OPEN**

## High-Assurance Track preservation

Issues #277, #295, #310, #316, #320 and the final-candidate/high-assurance sequence remain open unless their original acceptance facts are genuinely established. Nothing in this document retroactively weakens those issue contracts.

A future high-assurance experiment may use the Solo run as exploratory context, but confirmatory claims should be based on the separately authorized high-assurance run and its own candidate/freeze/evidence chain.
