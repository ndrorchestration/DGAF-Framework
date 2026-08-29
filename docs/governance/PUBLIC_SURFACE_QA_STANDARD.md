# Public Surface QA Standard

## Purpose

This standard governs material visible to a GitHub visitor, contributor, evaluator, recruiter, collaborator, customer, funder, or other external reader. Public material represents both the project and its maintainer; technical correctness alone is not enough.

The companion [Documentation Style Guide](DOCUMENTATION_STYLE_GUIDE.md) defines the editorial rules. This document defines the publication-quality control.

## Publication principle

> **A public artifact must be true, appropriately scoped, useful to its audience, professionally presented, correctly placed, safely disclosed, and maintainable.**

Public quality has two independent dimensions:

- **Epistemic quality:** the claims are accurate and properly evidenced.
- **Communication quality:** the reader can understand what matters, why it matters, and what to do next.

A document can satisfy one without satisfying the other.

## Public-surface tiers

| Tier | Examples | Expected treatment |
|---|---|---|
| **Landing** | README, repository description, top-level navigation | value, orientation, quick paths; minimal internal process |
| **Project** | current state, project status, architecture overview | precise status and useful context |
| **Technical** | specifications, contracts, implementation notes | technical depth and explicit semantics |
| **Research** | protocols, analysis plans, experiment records | reproducibility, scope, methodological precision |
| **Evidence** | run records, audit reports, evidence indexes | exact identity, provenance, forensic detail |
| **Historical** | superseded records, reconciliation logs | preserved detail with clear temporal scope |

A lower-level document may contain more detail than a higher-level document. Do not copy lower-level detail upward merely for completeness.

## Public-surface lens

Before merging a GitHub-visible change, review:

1. **Truth** — Are factual, technical, mathematical, and status claims supported?
2. **Authority** — Is the cited source authoritative for the claim?
3. **Audience** — Is the document written for the people who will encounter it?
4. **Utility** — Does it help readers understand, use, evaluate, reproduce, or contribute?
5. **Hierarchy** — Does the most important information appear before supporting detail?
6. **Placement** — Is the information where a reasonable GitHub user expects it?
7. **Navigation** — Are links stable, public, intentional, and useful?
8. **Professional representation** — Does the surface meet a credible engineering/open-source quality bar?
9. **Disclosure** — Does it avoid unnecessary personal, private, credential, or internal-deliberation exposure?
10. **Community fit** — Is it readable, accessible, maintainable, and consistent with open-source norms?
11. **Identity integrity** — Does it accurately represent capability, maturity, evidence, and project boundaries?
12. **Friction** — Does it reduce uncertainty about the reader's next step?

## Claim presentation

Use the repository's evidence vocabulary consistently:

`DEFINED → IMPLEMENTED → COMPUTED → VERIFIED → ATTESTED → HISTORICAL → HYPOTHESIS → METAPHOR → UNSUPPORTED → DEPRECATED`

Do not collapse these states into generic terms such as `validated`, `proven`, `production-ready`, `certified`, or `safe` unless the precise scope and supporting evidence establish that language.

For public-facing documents, prefer bounded positive statements over repeated prohibitions. State what was measured, what it supports, and where the boundary ends. Use explicit warnings when a reasonable reader could otherwise form a materially false conclusion.

## Historical material

Historical material may be retained when it has provenance value. It should be visibly dated, labeled, superseded, or otherwise scoped so a normal reader cannot mistake it for current project truth.

Do not silently rewrite historical evidence to match current state. Do not allow historical claims to remain visually indistinguishable from current claims.

## Internal versus public authority

- Personal Notion pages, private working records, internal control notes, and temporary coordination artifacts are not public navigation targets by default.
- Public landing surfaces should resolve to repository-local documentation, stable public resources, or intentionally designated public project surfaces.
- Internal records may inform public documentation without becoming the public destination.
- External services should be linked only when their destination is intentionally public and appropriately maintained.

## Documentation anti-patterns

The following are publication-quality risks:

- audit-ledger content placed on a landing page;
- long lists of internal predicates where a status summary would suffice;
- repeated `must not` / `do not infer` warnings that duplicate one canonical policy;
- closed PRs presented as current engineering work;
- stale SHAs, dates, branch names, or candidate identifiers;
- unexplained acronyms introduced faster than they can be understood;
- agent/persona names used as though they were external authorities;
- marketing language that outruns evidence;
- technical caveats that obscure the project's actual purpose;
- private workspace links or internal deliberation presented as public documentation.

## Pre-merge reader test

Ask:

- What will a first-time visitor believe after the first minute?
- Is that belief accurate?
- Can the reader find the architecture, current status, evidence, and contribution path without knowing internal project vocabulary?
- Are the important caveats present without overwhelming the primary purpose?
- Are historical and current states distinguishable?
- Is every public link intentional and maintainable?

If a detailed caveat is important but not appropriate for the current surface, move it to the canonical lower-level record and link to it.

## Governance boundary

This is a publication-surface control. It does not grant experimental authorization, create a freeze, upgrade evidence, change empirical N, or alter technical authority. Technical and experimental state remain governed by their authoritative records.
