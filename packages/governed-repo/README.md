# Governed Repo package candidate

Status: **P0 packaging experiment / non-mutating / not released**

This subproject tests whether Governed Repo v0 can be built, installed, and
imported as an isolated Python package without reusing DGAF's root
`pyproject.toml` and without changing the evaluator's semantics.

Project distribution name:

```text
ndrorchestration-governed-repo
```

Python import name:

```python
import governed_repo
```

## Boundaries

A successful package build/install demonstrates only bounded package and
import portability for the tested Python environments.

It does not establish merge authority, repository mutation authority,
production security, generalized GitHub correctness, independent
validation, compliance/certification, High-Assurance authorization, or
product-market fit.

The package remains deliberately non-mutating:

- `merge_executed = False`
- `mutation_executed = False`
- `authorization_effect = "NONE"`

## Temporary source-mirroring rule

During P0, `src/governed_repo/core.py` is an exact mirror of
`components/governed_repo.py`.

CI must fail if those files differ byte-for-byte. This prevents the package
candidate from becoming a silent semantic fork while the canonical source
location is still under review.

A later promotion may choose one canonical source location and replace this
temporary mirror arrangement.
