# DGAF-Framework — Repository Quality Baseline

**Audit date:** 2026-08-15  
**Scope:** engineering quality, evidence, reproducibility, CI, security/provenance  
**Epistemic status:** audit record; not repository-wide validation

## Current disposition

DGAF is the canonical governance/evaluation vocabulary and research/implementation repository. Its README now correctly separates repository scope from validation and certification claims.

## Verified observations

- The repository has an explicit epistemic classification standard.
- `.github/workflows/python-tests.yml` runs deterministic staging evidence, a Python test matrix, integration tests, and security scans.
- The staging circuit-breaker harness produces an uploaded evidence artifact.
- The workflow runs Bandit and Safety checks, but both security stages are configured as non-blocking.

## Critical audit finding

Several CI stages currently use `continue-on-error: true` or equivalent non-failing behavior:

- flake8 extended checks;
- Black formatting;
- isort;
- mypy;
- integration tests;
- Bandit;
- Safety;
- Codecov reporting.

This means the workflow provides substantial diagnostic coverage but should not be described as a strict quality/security gate. The deterministic staging harness is materially stronger because its pytest invocation is not marked non-blocking.

## Evidence implications

The existence of a test or security scan is not equivalent to a passing mandatory gate. Future repository claims should distinguish:

- executed;
- passed;
- advisory/non-blocking;
- blocking;
- artifact-produced;
- independently validated.

## P0/P1 actions

1. Preserve current non-blocking jobs where they are intentionally advisory, but label them explicitly as advisory.
2. Establish a minimal blocking quality gate for syntax/type/test failures appropriate to the repository's supported components.
3. Establish a blocking security policy only after false-positive handling and dependency scope are defined.
4. Keep research/evidence harnesses separate from production-readiness claims.
5. Continue the TLA+ containment reconstruction under issue #44 rather than treating prose or historical references as an executable specification.

## Promotion rule

A green workflow alone does not validate DGAF's mathematical models, governance efficacy, or cross-repository claims. Evidence remains artifact- and experiment-specific.
