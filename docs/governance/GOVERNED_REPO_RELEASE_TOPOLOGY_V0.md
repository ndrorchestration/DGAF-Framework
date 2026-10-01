# Governed Repo v0 release topology and canonical source

Status: draft productization contract. This document defines ownership and release boundaries; it does not authorize publication, merge, deployment, or repository mutation.

## Canonical semantic source

The single semantic implementation of the Governed Repo evaluator is:

`packages/governed-repo/src/governed_repo/core.py`

The historical module:

`components/governed_repo.py`

is a temporary compatibility surface only. It may import and re-export canonical package objects, but it must not contain independent promotion semantics.

## Compatibility invariant

For the v0 public evaluator surface, legacy imports and package-core imports must resolve to the same Python objects for:

- `ChangeIdentity`
- `GateReceipt`
- `GateRequirement`
- `PromotionPolicy`
- `PromotionReason`
- `PromotionReceipt`
- `UpstreamDecision`
- `assess_promotion`

A compatibility test must fail if the legacy surface becomes a semantic fork.

## Repository topology

The first bounded release candidate remains in the DGAF monorepo:

- package: `packages/governed-repo/`
- GitHub adapter: package module
- composite Action: `actions/governed-repo/`
- DGAF compatibility surface: `components/governed_repo.py`

A standalone repository is deferred until evidence shows materially different ownership, release cadence, contributor boundary, or distribution requirements.

## Versioning baseline

Current experimental version: `0.0.0.dev0`.

Before public package or Action release:

1. designate one package version source;
2. define the first intentional public version;
3. document supported Python versions from tested evidence;
4. treat stable reason-code strings as compatibility surface;
5. document receipt-field compatibility and deprecation rules;
6. publish release notes tied to exact source identity.

The currently tested Python matrix is 3.10 through 3.14. This is observed compatibility evidence, not a perpetual support guarantee.

## Release provenance record

A release candidate should bind:

- exact source commit SHA;
- package version;
- wheel SHA-256;
- sdist SHA-256;
- composite Action source SHA;
- relevant exact-head CI run identities;
- compatibility matrix;
- release notes/changelog;
- non-effect invariants.

This is a release-provenance contract only. It does not imply SLSA, in-toto, certification, or independent validation.

## Action pinning

Until an intentional tag/release policy is established, external consumers should pin the composite Action by immutable commit SHA.

## Non-effects

Governed Repo remains a decision/evidence layer. Release topology does not change these invariants:

- `merge_executed = false`
- `mutation_executed = false`
- `authorization_effect = NONE`

## Deferred work

The following remain outside this tranche:

- package publication;
- Marketplace publication;
- GitHub App or hosted service;
- live GitHub API client;
- organization-wide installation lifecycle;
- repository write permissions;
- merge execution;
- automatic promotion.

## Next usability gate

Before stronger product-readiness language, require at least one outside operator who is not relying on NDR ecosystem context to:

1. follow the installation or Action invocation documentation;
2. run one eligible case;
3. run one denial case;
4. explain the receipt/non-effect semantics correctly;
5. report setup friction and hidden assumptions.

Same-owner second repositories remain portability evidence, not independent outside-operator validation.
