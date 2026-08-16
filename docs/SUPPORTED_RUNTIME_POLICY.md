# Supported Runtime Policy

**Status:** Release/support policy
**Effective:** 2026-08-16

## Officially supported Python versions

The current supported Python runtime range for DGAF-Framework is:

- Python 3.10
- Python 3.11
- Python 3.12

These versions are the release/evidence-gate matrix. Required functional, quality, and security checks are expected to execute successfully on all three versions.

## Python 3.9 disposition

Python 3.9 is **legacy / not release-supported**.

The prior CI matrix included Python 3.9, but the pinned evidence-gate toolchain requires Python 3.10 or newer. Rather than weaken the reproducibility controls or silently retain an unsupported runtime claim, Python 3.9 has been removed from the supported evidence matrix.

Python 3.9 compatibility is not claimed, tested as a release gate, or used as evidence for current support.

## Interpretation

A green CI job establishes that the current tested suite completed under that runner/runtime combination. It does not, by itself, establish product-level efficacy or unrestricted compatibility outside the documented scope.

The supported-runtime claim is limited to the versions listed above and the dependency/configuration state exercised by the current evidence gates.

## Release-gate policy

For the supported Python versions:

1. Functional pytest execution is release-blocking.
2. Required integration/security evidence must complete successfully.
3. Quality checks are retained as explicit evidence and remain subject to the repository quality policy.
4. Toolchain versions used by evidence gates are pinned and reported.
5. Any change to the supported runtime range requires a documented policy update and a corresponding CI/evidence review.

## Deprecation and expansion

This policy can be revised when a supported runtime reaches end-of-life, dependency constraints require a change, or a new Python version is deliberately adopted. Such a revision must update the CI matrix, toolchain policy, claim/evidence index, and release documentation together.
