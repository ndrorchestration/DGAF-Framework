# docs/drafts — DGAF Staging Layer

**Status:** Project-local staging/documentation area. Contents are drafts unless independently promoted and evidenced.

**Pattern:** P-03 (BLG-Surface-and-Defer) | P-18 (Open-Issue-Triage) | P-11 (11Q Terminal Gate)  
**Historical project roles:** Agent COLLEEN (triage queue) | Agent Apogee (promotion gate)  
**Historical/project-local conductor role:** Agent Amethyst

---

## Purpose

This directory is a staging area for DGAF governance artifacts that have been created but not yet promoted into the project's current documentation set.

Presence here signals **draft/in-review status**. Promotion to a named `docs/` location is a project workflow action; it does not by itself establish external certification, independent validation, or governance authority.

Anything in `drafts/` is:

- Visible to repository collaborators
- NOT automatically part of the current public specification
- NOT externally certified merely by passing a project-local gate
- Subject to the repository's current review process

## Promotion Criteria

A draft artifact may be considered for promotion when the project-local review criteria are satisfied:

| Criterion | Project-local gate |
|-----------|--------------------|
| Required P-24 fields present | `gate_compliance_check.py` passes |
| P-10 (1-1-1-1) criteria satisfied | Project-local review score |
| P-11 (11Q) criteria satisfied | Project-local review runs |
| No unresolved tension in reasoning chain | Review evidence |
| CROSS_REF entry drafted | Ready for registration |

These gates are **internal workflow criteria**, not independent certification standards.

**Promotion action:** move the file to the appropriate documentation location, update the relevant cross-reference, and record the change in the project log.

## Staleness Rule

Any file that remains in `drafts/` for **≥ 2 consecutive sweep sessions** without promotion is eligible for escalation:

1. Surface it in the next priority queue.
2. Review: promote, rework, or formally defer with rationale in the project log.
3. Files deferred > 5 sessions with no action may be archived with a `DEFERRED.md` explaining the disposition.

## Current Drafts

*None — staging area initialized S026.*

## Evidence boundary

Use the ecosystem evidence ladder:

**DEFINED → IMPLEMENTED → COMPUTED → VERIFIED → ATTESTED → HISTORICAL → HYPOTHESIS → METAPHOR → UNSUPPORTED → DEPRECATED**

A project-local gate can establish that a workflow criterion was met; it cannot, by itself, upgrade an artifact to external certification or independent verification.

---

*Project-local workflow roles and historical terminology are retained for provenance. Current status is governed by repository evidence, not role names.*
