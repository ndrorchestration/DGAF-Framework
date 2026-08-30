# Public Surface Refactor — 2026-08-29

## Purpose

This record documents the repository-wide editorial pass initiated after review of the root README. The objective is to preserve DGAF's unusually strong transparency while improving audience fit, hierarchy, scanability, and professional presentation.

## Finding

The repository's documentation was generally rigorous but had accumulated a recurring pattern: internal governance, evidence, and coordination detail was sometimes presented at a level intended for landing pages or broad project communication.

The principal correction is **not to remove evidence**. It is to place information at the level where it is most useful.

## Repository-wide editorial model

Documentation now follows this hierarchy:

### Information hierarchy

`landing → project → technical → research → evidence → historical`

Higher-level surfaces summarize and route. Lower-level surfaces preserve detail.

The canonical editorial rules are in [`DOCUMENTATION_STYLE_GUIDE.md`](DOCUMENTATION_STYLE_GUIDE.md). Publication controls remain in [`PUBLIC_SURFACE_QA_STANDARD.md`](PUBLIC_SURFACE_QA_STANDARD.md).

## Changes in this pass

- Root README refocused as a project entry point rather than an internal evidence ledger.
- Documentation map reduced to reader tasks instead of an exhaustive document inventory.
- Current engineering and experimental tracks are explicitly separated.
- Current engineering narrative references PR #139 as the active engineering lane; PRs #132/#133 are historical remediation records unless a deeper record requires their history.
- Contribution guidance now follows the same audience, claim-boundary, and documentation principles.
- Public-surface QA now explicitly identifies audit-ledger overload, repeated prohibitions, stale status references, unexplained acronym density, and caveat-driven loss of project identity as editorial risks.
- A repository-wide style guide establishes rules for audience, hierarchy, claim presentation, temporal scope, navigation, and public social quality.

## What remains intentionally detailed

Technical specifications, experiment protocols, evidence indexes, audit records, mathematical policies, provenance records, and historical reconciliations should remain detailed where that detail serves reproducibility or governance.

The refactor does **not** flatten technical documentation into marketing copy. It separates technical depth from public orientation.

## Required ongoing behavior

When changing documentation:

1. Identify the document's audience and primary job.
2. Put the highest-value information first.
3. Use bounded claims tied to evidence.
4. Avoid repeating caveats that belong in a canonical policy.
5. Mark historical material clearly at the point of encounter.
6. Update living status references when current state changes.
7. Keep internal coordination out of public navigation unless deliberately designated.
8. Prefer links to authoritative records over duplicated audit detail.

## Verification boundary

This editorial pass changes documentation only. It does not modify implementation, experimental apparatus identity, freeze state, pilot authorization, empirical N, or scientific results.

The current experimental state remains governed by the authoritative project/current-state and evidence records.
