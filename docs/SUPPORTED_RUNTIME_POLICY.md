# Supported Runtime Policy

**Status:** CI validation policy — not a blanket compatibility guarantee  
**Effective:** 2026-08-16

## Current CI validation matrix

The repository currently executes its Python test workflow on:

- Python 3.9
- Python 3.10
- Python 3.11
- Python 3.12

The latest successful run is `31976717339` on main commit `810caa34fff606f3b60b585560687f1cd01b70af`.

## Interpretation

A green CI job establishes that the current tested suite completed under that runner/runtime combination. It does **not**, by itself, establish a product-level promise of full support for every use case on that interpreter version.

Until a maintainer explicitly narrows or expands the policy, repository documentation should describe these versions as **CI-validated runtimes**, not as an unconditional compatibility guarantee.

## Release/support decision

A future release-level support policy should identify:

1. officially supported Python versions;
2. minimum and maximum dependency/runtime constraints;
3. versions treated as informational compatibility checks;
4. end-of-support/deprecation dates; and
5. whether security and quality gates are release-blocking for each supported version.

Until those decisions are recorded, issue `#51` remains open.
