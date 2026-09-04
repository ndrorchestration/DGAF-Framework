# DGAF Evidence Operating Principles

**Status:** ACTIVE OPERATING PRACTICE
**Date:** 2026-09-04
**Scientific boundary:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / empirical N = 0

## Purpose

This document records the established engineering and research practices used to keep DGAF evidence traceable, reproducible, independently challengeable, and epistemically honest. It is an operating guide for the existing P1–P9 process, not a new governance gate.

## Five governing principles

### 1. Identity before inference

No claim-bearing evidence is interpreted until its exact producing identity is established.

At minimum, candidate SHA, executed tree SHA, apparatus identity, protocol identity, producing workflow/run, and artifact identity must agree. A later documentation commit, matching filename, deployment URL, or behavioral similarity is not an identity substitute.

### 2. Evidence before status

A status is a conclusion derived from evidence. The status must never substitute for the evidence that supports it.

Every material evidence item should therefore retain both:

- the evidence object or retrieval reference; and
- the predicate decision made from that evidence.

### 3. Unknown stays unknown

Missing retrieval, incomplete provenance, unresolved dependency, or unavailable independent verification must remain explicitly represented.

Use the repository's existing distinctions rather than collapsing them:

- `VERIFIED` — predicate satisfied by the required evidence;
- `RECORDED` — historically recorded, but not presently re-verified;
- `UNCONFIRMED` — expected evidence cannot currently be independently retrieved;
- `SUPERSEDED` — valid historical record that no longer governs current state;
- `BLOCKED` — required evidence cannot yet be produced;
- `NOT_EXECUTED` — the event has not occurred;
- `INVALIDATED` — evidence was shown to be unusable or contradicted.

Do not promote an item merely because a related artifact exists.

### 4. Verification is not efficacy

Engineering, governance, CI, deterministic, synthetic, dry-run, and artifact-integrity results establish properties of the apparatus or evidence process. They do not establish that DGAF outperforms its null condition.

Accordingly:

- CI success does not increase empirical N;
- dry-run observations are not pilot observations;
- artifact integrity does not establish scientific validity;
- P3–P8 closure does not establish an effect;
- only authorized empirical execution creates empirical observations.

### 5. Independent challenge precedes irreversible transition

The actor or workflow producing evidence should not be the sole authority declaring that the evidence proves the transition it enables.

Freeze, authorization, and empirical execution therefore require an independently challengeable evidence chain. Independent verification must inspect the bound evidence itself, not merely accept the producer's summary.

## Configuration and provenance practice

DGAF treats an experimental candidate as a configuration-controlled object. Claim-bearing evidence should be bound to the immutable source tuple defined by `CURRENT_CANDIDATE_EVIDENCE_REGISTRY_CONTRACT_v1.md`.

The practical chain is:

`candidate → tree → apparatus → protocol → analysis/configuration → workflow/run → artifact → digest`

Where technically feasible, artifact content must also be independently hashed after retrieval. No historical artifact is transferred to a later candidate merely by ancestry or apparent equivalence.

## Reproducibility practice

Reproducibility is tested rather than asserted.

### Level A — deterministic self-reproduction

The same candidate and inputs reproduce the same expected artifact/result.

### Level B — independent reproduction

A separate execution context or verifier can reproduce or independently validate the expected artifact/result from the retained identity and instructions.

Level A does not automatically imply Level B.

## Freeze practice

A freeze is a configuration-management event, not a documentation event.

The eventual freeze identity must bind the exact executable candidate and the complete scientific/control configuration, including the analysis lock and prerequisite evidence. The existence of a document stating that a system is frozen does not itself establish a freeze.

## Retrieval test

A documentation and evidence package is considered operationally adequate only if an unfamiliar verifier can reconstruct:

1. what exact candidate was evaluated;
2. what evidence was produced;
3. which evidence is current versus historical;
4. why each predicate is open, blocked, verified, or not executed;
5. what remains required before the next irreversible transition.

If that reconstruction requires undocumented knowledge from the original operator, the package has a retrieval gap.

## Relationship to P1–P9

These practices support the existing process without adding new gates:

| Practice | Primary support |
|---|---|
| Identity before inference | P1, P5, P7, P8 |
| Evidence before status | P1–P9 |
| Unknown stays unknown | P2, P6, P8, P9 |
| Verification ≠ efficacy | P3–P9 and N accounting |
| Independent challenge | P9, freeze, authorization |
| Configuration control | P1, P5, P7, P8 |
| Reproducibility levels | P5, P9 |
| Freeze as configuration event | P8, freeze |
| Retrieval test | P3–P6, P9 |

## Current disposition

These principles refine execution of the existing DGAF closure path. They do not close any predicate, create a freeze, grant authorization, permit unblinding, or change empirical N.

**Current experimental state remains: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
