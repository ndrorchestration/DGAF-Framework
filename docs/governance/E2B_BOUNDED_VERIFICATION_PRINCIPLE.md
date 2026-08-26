# E2b Bounded Verification Principle

**Status:** Governance control
**Scope:** DGAF freeze-admissibility verification
**Epistemic state:** PRE-FREEZE / N=0 / pilot NOT GRANTED

## Purpose

E2b establishes reproducibility and integrity of the designated verification environment and its target apparatus without recursively requiring E2b to verify the complete provenance of the tooling used to bootstrap E2b.

## Bounded trust model

Verification SHALL terminate at an explicitly declared bootstrap trust boundary. Bootstrap tooling and infrastructure are recorded as external trust inputs; they are not recursively subjected to the same E2b predicate.

The control therefore distinguishes:

1. **Bootstrap integrity** — the declared verifier can be instantiated from its trusted bootstrap boundary.
2. **Verifier reproducibility** — the declared verifier dependency environment can be recreated with the same dependency identity.
3. **Verifier correctness** — the verifier's implementation correctly expresses the intended governance predicates. This is controlled by code review, tests, independent verification, and P9 rather than recursive E2b self-verification.

## Evolution rule

Immutability applies to an evidence instance, not to DGAF as a permanently immutable system.

A substantive change to the verifier, its lock, its bootstrap boundary, or relevant verification semantics INVALIDATES affected E2b evidence and requires a new verification cycle. It does not create a recursive verification obligation.

## Fail-closed states

- **PASS:** the declared verifier environment satisfies the E2b reproducibility contract.
- **NOT PASS:** required dependency/provenance evidence is incomplete.
- **INVALIDATED:** previously valid E2b evidence was affected by a substantive change.
- **BLOCKED:** E2b cannot execute because an external prerequisite is unavailable.

No state requires indefinite self-verification.

## Non-recursion invariant

> No DGAF governance predicate SHALL require recursive verification of itself or its entire bootstrap chain. Every verification layer SHALL terminate at an explicitly declared trust boundary.

## Advancement invariant

> Controls SHALL be fail-closed while remaining evolution-permitting. A failed or invalidated control initiates a bounded re-verification cycle; it SHALL NOT create an unbounded dependency loop that makes legitimate system evolution impossible.

## Current E2b boundary

The PDMAL apparatus full lock is the designated hash-pinned verifier input. The separate `requirements-epistemic.txt` surface is not currently a complete immutable transitive hash lock, so E2b remains OPEN for that surface. This is an evidence-closure condition, not a requirement to recursively lock the tooling that creates or verifies the lock.

## Authorization boundary

This control does not authorize pilot execution, unblinding, freeze creation, or empirical claims. Current empirical N remains 0 until the independently verified authorization sequence is completed.
