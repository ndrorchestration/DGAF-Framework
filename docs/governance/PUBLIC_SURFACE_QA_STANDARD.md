# Public Surface QA Standard

## Purpose

This standard governs any DGAF artifact that is visible to a GitHub visitor, contributor, evaluator, recruiter, collaborator, customer, or other external reader. Public-facing repository material represents both the project and its maintainer; internal correctness alone is not sufficient for publication.

GitHub's repository guidance treats the README as a primary visitor entry point and recommends clear project purpose, usefulness, getting-started guidance, support paths, and maintainer/contributor information. DGAF applies that expectation as a publication-quality control, not merely as a documentation suggestion.

## Publication principle

> **A public artifact must be true, appropriately scoped, useful to its intended audience, professionally presented, correctly placed, safely disclosed, and maintainable.**

An internal artifact does not become public-facing merely because it is accurate or authoritative internally.

## Public-surface lens

Before merging a GitHub-visible change, review it through all of these lenses:

1. **Truth** — Are factual, technical, mathematical, and status claims supported by the appropriate evidence?
2. **Authority** — Is the cited artifact actually authoritative for the claim being made?
3. **Audience** — Is the material written for the people who will encounter it?
4. **Utility** — Does it help a visitor understand, evaluate, use, reproduce, contribute to, or appropriately interpret the project?
5. **Placement** — Is it located where a reasonable GitHub user would expect to find it?
6. **Navigation** — Do links lead to stable, intentional, audience-appropriate destinations?
7. **Professional representation** — Does the surface represent the maintainer's work at the expected engineering/open-source quality bar?
8. **Disclosure** — Does it avoid unnecessary personal information, private workspace material, credentials, internal deliberation, operational clutter, or unfinished work?
9. **Community fit** — Is it consistent with normal open-source expectations for clarity, accessibility, contribution, attribution, licensing, and respectful project maintenance?
10. **Maintenance** — Can the information and its destinations remain coherent as the repository evolves?
11. **Identity integrity** — Does the artifact accurately represent the project and the maintainer rather than overstating capability, validation, status, or maturity?
12. **Friction** — Does it reduce the reader's next-step uncertainty rather than forcing them through internal process or irrelevant detail?

## Internal versus public authority

DGAF distinguishes internal operational authority from public project navigation.

- Personal Notion pages, private working records, internal control notes, and temporary coordination artifacts are **not public navigation targets by default**.
- A GitHub landing page should preferentially resolve to repository-local documentation, stable public project resources, or an intentionally designated public project surface.
- An internal control record may inform public documentation without being exposed as the public destination.
- If an external service is linked, the destination must be intentionally designated for public consumption and must not expose private workspace context merely because the internal team uses it.

## Evidence and presentation boundary

Public documentation must preserve DGAF's epistemic distinctions. In particular:

`defined → implemented → computed → verified → attested → historical`

must not collapse into a generic claim of "validated" or "production-ready."

A mathematical correction can establish a mathematical result without establishing a system-level claim. A passing component test can establish the tested component result without establishing repository-wide validation. A deployment can establish deployment state without establishing experimental authorization or efficacy.

## Historical material

Incorrect or superseded values should normally be **retired, classified, superseded, and prevented from downstream use**, not silently erased when their historical presence is relevant to provenance. Historical material must be visibly scoped so a normal visitor cannot mistake it for current project truth.

## Required pre-merge review

For every externally visible documentation or navigation change, answer:

- What will a first-time visitor believe after reading this?
- Is that belief exactly supported by the evidence?
- Is this the right information for this surface?
- Is the destination public, stable, and intentionally maintained?
- Does anything internal or personal become visible unnecessarily?
- Does the change improve comprehension and next-step usability?
- Does it remain coherent with the current README, project status, evidence index, governance records, and terminology?

If any answer is materially uncertain, the change should remain internal or be revised before publication.

## Relationship to DGAF governance

This standard is a **publication-surface control**. It does not grant experimental authorization, create a freeze, upgrade evidence, or change empirical N. It operates as a lens over changes that represent DGAF externally.

Current experimental state remains independently governed by the authoritative gate/evidence records.
