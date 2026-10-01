# Governed Repo package candidate

Status: **package-canonical productization candidate / non-mutating / not released**

Governed Repo evaluates whether an exact repository change is eligible for
promotion under caller-supplied policy and observed gate receipts. It does
not merge, push, deploy, release, mutate repository state, or grant
authorization.

Project distribution name:

```text
ndrorchestration-governed-repo
```

Python import name:

```python
import governed_repo
```

## Canonical source

The single semantic implementation of the evaluator is:

```text
packages/governed-repo/src/governed_repo/core.py
```

`components/governed_repo.py` is a compatibility re-export surface for the
historical DGAF import path. It must not contain an independent evaluator
implementation. CI checks object identity between the compatibility surface
and the canonical package objects.

## Tested package boundary

Canonical merged source for outside-operator testing:

```text
c90c74c04583c5a3f23f6a261cf38cd6922c781c
```

The merged commit has the same Git tree as fully tested PR head
`77c818ecc5d57e5dd354bc86396dc9e7c5c6be9e`. That PR head completed the
Governed Repo package workflow successfully on Python 3.10, 3.11, 3.12,
3.13, and 3.14. The merged commit then completed the observed post-merge
mainline suite successfully, including Main Push Provenance Audit and live
regression.

This preserves the distinction between package-matrix evidence on the PR head
and canonical repository identity on protected `main`.

That is bounded compatibility evidence for the tested environments, not a
perpetual support guarantee.

## Install from the validated source

The package is not published. For the bounded validation path, clone the
repository and check out the exact validated commit:

```bash
git clone https://github.com/ndrorchestration/DGAF-Framework.git
cd DGAF-Framework
git checkout c90c74c04583c5a3f23f6a261cf38cd6922c781c
python -m pip install ./packages/governed-repo
```

Then verify the import:

```bash
python -c "import governed_repo; print(governed_repo.PromotionReason.ELIGIBLE_FOR_PROMOTION.value)"
```

Expected output:

```text
ELIGIBLE_FOR_PROMOTION
```

For the controlled outside-operator usability exercise, follow
`docs/governance/GOVERNED_REPO_OUTSIDE_OPERATOR_TRIAL_V0.md`.

## Non-effects

Every Governed Repo v0 receipt preserves:

- `merge_executed = False`
- `mutation_executed = False`
- `authorization_effect = "NONE"`

An `ELIGIBLE_FOR_PROMOTION` result means the supplied observations satisfy
the supplied policy. It is not a merge, deployment, authorization grant, or
claim that the repository is safe in every respect.

## Claim ceiling

A successful package build/install or bounded operator trial does not
establish:

- merge or repository-mutation authority;
- production security;
- generalized GitHub correctness;
- independent validation;
- compliance or certification;
- High-Assurance authorization;
- publication readiness;
- product-market fit.

See `docs/governance/GOVERNED_REPO_RELEASE_TOPOLOGY_V0.md` for the current
source-ownership, versioning, and release-provenance boundary.
