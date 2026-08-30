# ORBIT-N1 — Bounded Evidence-Driven Orchestration Pattern

**Purpose:** Move DGAF/PDMAL from engineering-heavy pre-freeze work to valid empirical observation without allowing governance, verification, or provenance work to become an infinite prerequisite chain.

## Core principle

> Do the smallest amount of work necessary to make the next observation interpretable.

A desirable improvement is not a blocker merely because it is possible. A pre-N=1 blocker must demonstrably affect treatment identity, execution validity, or interpretation of the planned observation.

## State machine

`UNKNOWN/HISTORICAL → CURRENT CANDIDATE → APPARATUS BOUNDED → REQUIRED CONTROLS VERIFIED → SCIENTIFIC TARGET BOUND → FREEZE → AUTHORIZATION → N=1 → CLASSIFY → FULL PILOT / REPAIR`

One state transition is the unit of orchestration. Later states are never inferred from earlier green status.

## ORBIT cycle

### O — Observe

Read the current machine-verifiable state before changing anything: HEAD, candidate identity, workflow state, artifact state, open issues/PRs, and known boundaries.

### R — Reconcile

For every completion claim, identify the exact predicate, evidence, candidate/tree/runtime identity, and whether the evidence is current or historical. Classify it as current, historical, superseded, unverified, blocking, or non-blocking.

### B — Bound

Define only the minimum boundary necessary for the next state transition. For the current DGAF study, the tested treatment includes the seven canonical TGL required gates; non-required historical governance remains outside scope.

### I — Instrument

Every transition must produce identity-bound evidence where applicable: candidate SHA, tree SHA, action/run ID, artifact ID/hash, result, claim classification, and limitations.

### T — Transition

Advance exactly one state when its acceptance predicates have evidence. Do not collapse candidate designation, freeze, authorization, and experimental execution into one opaque action.

## Blocking-defect classes

**Interpretability blocker:** changes what the experiment would mean.

**Evidence blocker:** the observation may occur, but its identity or result cannot be established.

**Quality defect:** does not change interpretation; defer.

**Research enhancement:** useful future work but not required for the current observation; defer.

## Evidence inheritance

Evidence does not transfer across apparatus identity changes by default. Historical evidence remains historical unless an explicit inheritance rule demonstrates same apparatus, relevant configuration, execution semantics, evidence predicate, and provenance continuity.

## Candidate identity

A material change to treatment semantics, control behavior, execution semantics, or artifact generation creates a new experimental candidate cycle. Documentation-only changes do not automatically create a new candidate.

## Epistemic claims

Use: `OBSERVED`, `VERIFIED`, `OPERATIONALLY CHARACTERIZED`, `INFERRED`, `HYPOTHESIZED`, `PLANNED`, `NOT ESTABLISHED`.

Never compress:

- implementation into proof;
- CI success into efficacy;
- deployment readiness into validation;
- N=1 into generalizable effect;
- verification into empirical support.

## N=1 execution mode

After the apparatus satisfies the bounded N=1 predicates, new work is admitted only when it affects interpretability of the planned observation. Peripheral engineering is deferred.

## N=1 acceptance packet

A valid N=1 record must identify the candidate/apparatus, scientific target, treatment/reference conditions, seed, execution identity, runtime/deployment identity, outcomes, artifact IDs and hashes, authorization state, blinding/custody state, and required reproducibility metadata.

A successful first run establishes **Operationally Characterized**, not proven efficacy.

A failed first run is classified by cause: apparatus defect, protocol defect, environment defect, or genuine behavioral result.

## Anti-infinite-project guard

For every new prerequisite:

`NEW TASK → affects current experiment? → affects interpretability? → if no: DEFER; if yes: MINIMAL FIX → VERIFY → TRANSITION`

The existence of further desirable rigor is not sufficient to stop a valid state transition.

## Current DGAF application

For the present study:

`F1–F3 remediation → semantic recovery of seven constitutive gates → new candidate → candidate-scoped verification → freeze → authorization → N=1`

HPG, Herald, and unrelated historical governance capabilities remain out of the minimal treatment unless separately adopted by a future governed construct.
