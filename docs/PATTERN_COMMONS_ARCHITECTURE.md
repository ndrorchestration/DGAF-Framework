# Pattern Commons Architecture

**Status:** Proposed / audit phase
**Date:** 2026-08-25

## Purpose

Pattern definitions and pattern registries are ecosystem-level knowledge artifacts. They are not inherently owned by DGAF merely because DGAF implements or references them.

## Separation of concerns

- **Pattern Commons:** canonical identity, provenance, aliases, semantic equivalence, epistemic status, and evidence relationships across repositories.
- **NDR:** a pattern namespace/family within the Pattern Commons.
- **DGAF:** framework implementation, governance mechanisms, enforcement, and references to applicable patterns.
- **Notion:** governance/index layer linking patterns to repositories, claims, decisions, implementations, and evidence.

## Registry classification

The census distinguishes at least:

1. pattern registries;
2. taxonomy/vocabulary registries;
3. template registries;
4. agent registries;
5. evidence/claim registries;
6. ecosystem registries;
7. service/runtime registries;
8. historical/deprecated registries.

These must not be merged merely because they share the term `registry`.

## Equivalence rule

Same identifier, filename, or terminology is insufficient evidence of pattern equivalence. Equivalence requires comparison of definition, mechanism, scope, provenance, and claimed function.

## Epistemic rule

Registry membership does not establish truth, novelty, empirical support, completeness, or independent verification. Pattern claims must carry explicit epistemic status and evidence boundaries.

## Current NDR candidates

The current audit has identified candidate concepts for the next NDR wave:

- P-35 Epistemic Overreach
- P-36 Mutual Reference Instability
- P-37 Semantic Convergence Failure
- P-38 Observational Perturbation

These remain candidate definitions until formalization and evidence are completed.

## Migration policy

No existing pattern artifacts should be moved, deleted, or consolidated until provenance, ownership, aliases, and epistemic status have been reconciled. The dedicated Pattern Commons repository decision is deferred until the census and audit provide sufficient evidence.
