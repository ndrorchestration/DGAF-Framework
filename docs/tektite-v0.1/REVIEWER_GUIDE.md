# Tektite v0.1 Public Reviewer Guide

Tektite v0.1 is a static public governance-console projection. This guide explains how to read it without over-interpreting what it proves.

## What the shell is

The public shell is a curated display layer for evidence-bound AI-assisted systems. It is meant to help reviewers answer three questions:

1. What happened?
2. What evidence supports that statement?
3. What is the system authorized to do next?

The shell is intentionally useful even when the answer is negative, blocked, not established, or not authorized.

## What the shell is not

The shell is not:

- an execution surface;
- a deployment artifact;
- a live repository controller;
- a rollback mechanism;
- an independent validation result;
- a certification or compliance claim;
- a High-Assurance assertion;
- evidence of canonical DGAF efficacy.

A green CI run, merged documentation PR, or static preview page may improve reviewability, but it does not change those claim ceilings by itself.

## How to read status labels

Use the labels conservatively:

- `ACTIVE` means a documented discipline or process is present in the public representation.
- `ESTABLISHED` means the represented documentation or boundary has been created and reconciled within the repository context.
- `MERGED` means the relevant documentation or static artifact reached `main`.
- `NOT_ESTABLISHED` means the system does not claim the condition has been shown.
- `NOT_AUTHORIZED` means the evidence does not permit the transition or action.
- `BLOCKED` means there is an explicit unresolved dependency or boundary preventing advancement.

Negative status is part of the product. It is not a visual blemish or copy problem.

## How to evaluate an evidence row

For each evidence row, review four separate fields:

1. **Supports** — what the evidence is allowed to show.
2. **Does not support** — what the same evidence must not be used to claim.
3. **Authorization effect** — what can or cannot happen next.
4. **Source context** — which public PR, issue, or document backs the row.

Do not collapse these into a single pass/fail impression. A row can be valuable precisely because it blocks over-interpretation.

## Current preserved ceiling

```text
SCIENTIFIC_N_INCREMENT=0
INDEPENDENT_VALIDATION=NOT_ESTABLISHED
CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED
HIGH_ASSURANCE=NOT_AUTHORIZED
LIVE_REPOSITORY_MUTATION=NOT_AUTHORIZED
ROLLBACK_EXECUTION=NOT_AUTHORIZED
PRODUCTION_EXECUTOR=NOT_ESTABLISHED
```

## Public review checklist

A reviewer should be able to confirm:

- the page makes the core question visible;
- negative statuses are easy to find;
- evidence rows distinguish supported and unsupported claims;
- case studies do not promote blocked authority;
- public links identify source artifacts;
- private systems, credentials, filesystem paths, and personal logistics are absent;
- the shell remains understandable without JavaScript, private APIs, or a live service.

## Allowed next steps from the reviewer guide

This guide can support:

- static copy review;
- accessibility review;
- evidence-link curation;
- additional static case-study detail pages;
- reviewer onboarding.

It does not authorize:

- public deployment as a production claim;
- live executor attachment;
- repository mutation;
- rollback execution;
- independent validation claims;
- High-Assurance claims;
- certification or compliance claims.
