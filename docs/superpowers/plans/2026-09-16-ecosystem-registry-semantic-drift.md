# Ecosystem Registry Semantic-Drift Hardening Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Make `registry/ecosystem_registry.json` an explicitly bounded projection and make `registry/ecosystem_audit.py` fail closed on material semantic drift instead of reporting structural inventory only.

**Architecture:** Keep the registry as a repository-local projection, not an SSoT. Add explicit root projection metadata and structured current-vs-historical authority/deployment semantics; refactor the auditor into deterministic pure validation functions plus the existing GitHub inventory fetch so tests can exercise semantic drift without network access. The CLI exits nonzero when fail-closed semantic violations are present while retaining informational lifecycle/pattern reporting.

**Tech Stack:** Python 3.11 stdlib + existing `requests`, JSON registry data, pytest, GitHub Actions YAML.

**Spec:** GitHub issue #694 (`Harden ecosystem registry projection semantics and semantic-drift audit`), rebased to protected `main` `0083d64aa5f9395a9aa38ff0ca01ccd9e528fd44`.

## Global Constraints

- Preserve `PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0` scientific semantics.
- Do not establish materialization, a materialization receipt, primary-analysis authorization, efficacy, independent validation, certification, compliance, or production readiness.
- Registry is a projection only; repository/project-local canonical sources remain authoritative.
- Preserve historical persona/governance propagation as explicit lineage; do not erase history.
- Negative/historical statements containing risky phrases must not be rejected as current positive claims.
- Deployment runtime truth requires dated/bound observation evidence; declaration/configuration is separate from observation.
- TDD RED must precede implementation GREEN for semantic validators.

---

### Task 1: Reproduce the semantic-audit blind spot with focused RED tests

**Files:**
- Create: `tests/test_ecosystem_registry_projection_hygiene.py`
- Read: `registry/ecosystem_audit.py`
- Read: `registry/ecosystem_registry.json`

**Interfaces:**
- Consumes: current `load_registry()` and module import surface.
- Produces: executable requirements for `collect_semantic_violations(registry, github_repos, *, now)` and `audit_exit_code(violations)`.

- [ ] **Step 1: Write failing tests for projection metadata and current-authority semantics**

```python
from datetime import datetime, timezone

from registry.ecosystem_audit import collect_semantic_violations


def _repo(full_name="ndrorchestration/example", **overrides):
    base = {
        "full_name": full_name,
        "private": False,
        "archived": False,
        "default_branch": "main",
    }
    base.update(overrides)
    return base


def _registry(project):
    return {
        "registry_version": "0.5.0",
        "projection": {
            "authority_scope": "projection_only",
            "canonical_source": "project-local repository governance/evidence",
            "canonical_source_revision": "0083d64aa5f9395a9aa38ff0ca01ccd9e528fd44",
            "projection_checked_at": "2026-09-16T12:00:00Z",
            "projection_status": "CURRENT",
            "staleness_class": None,
        },
        "projects": [project],
    }


def test_rejects_current_persona_authority_without_functional_role():
    project = {
        "id": "example",
        "github": {"owner": "ndrorchestration", "repo": "example", "private": False, "archived": False, "default_branch": "main"},
        "authority": {"current_owner": "Amethyst"},
        "deployments": [],
        "summary": "Example project.",
    }
    violations = collect_semantic_violations(
        _registry(project), [_repo()], now=datetime(2026, 9, 16, 12, tzinfo=timezone.utc)
    )
    assert any(v["code"] == "CURRENT_PERSONA_AUTHORITY" for v in violations)
```

- [ ] **Step 2: Add RED tests for GitHub metadata mismatch, deployment evidence, claim scope, and historical negative controls**

Test these independent behaviors:

```text
GITHUB_METADATA_MISMATCH      private/archived/default_branch mismatch
ACTIVE_DEPLOYMENT_UNVERIFIED  active runtime + TODO identity or no observed_at/evidence
UNSCOPED_CURRENT_CLAIM         positive inherited authority/certification/compliance wording
PROJECTION_METADATA_MISSING    absent/stale required projection metadata
```

Also assert that explicit `historical_lineage` and phrases such as `security compliance NOT established` do not trigger current-claim violations.

- [ ] **Step 3: Run the focused test file and record RED**

Run: `pytest -q tests/test_ecosystem_registry_projection_hygiene.py`
Expected: collection/import failure because `collect_semantic_violations` does not exist, or assertion failures proving the current auditor does not enforce the semantics.

- [ ] **Step 4: Commit RED tests only**

Commit message: `test(registry): expose semantic projection drift`

---

### Task 2: Add the deterministic fail-closed semantic validator

**Files:**
- Modify: `registry/ecosystem_audit.py`
- Test: `tests/test_ecosystem_registry_projection_hygiene.py`

**Interfaces:**
- Produces: `collect_semantic_violations(registry: dict, github_repos: list[dict], *, now: datetime) -> list[dict]`
- Produces: `audit_exit_code(violations: list[dict]) -> int`
- `run_audit()` prints structural + semantic sections and returns the exit code.

- [ ] **Step 1: Implement minimum root projection validation**

Require:

```text
authority_scope == projection_only
canonical_source non-empty
canonical_source_revision non-empty
projection_checked_at parseable ISO-8601
projection_status in CURRENT|STALE|HISTORICAL
staleness_class null or METADATA|SOURCE_SEMANTIC|RUNTIME_IDENTITY|HISTORICAL_SCOPE|GENERATOR
```

A `CURRENT` projection older than the policy window (default 7 days) produces `PROJECTION_METADATA_STALE`.

- [ ] **Step 2: Implement live GitHub metadata comparison**

For every current project with a GitHub binding, compare `private`, `archived`, and `default_branch` to the fetched repository record. Emit `GITHUB_METADATA_MISMATCH` with project id, field, registry value, and observed value.

- [ ] **Step 3: Implement authority and claim-scope checks**

Current authority must use `role.*` / `capability.*` identifiers. Persona labels (`Amethyst`, bare `Sentinel`, `COLLEEN`) are permitted only in structured historical lineage fields. Current positive summary/authority text matching bounded high-risk patterns (`DGAF-governed`, `DGAF-certified`, external certification, guaranteed compliance, `security compliance`) emits `UNSCOPED_CURRENT_CLAIM`; explicit negation/historical scope is exempt.

- [ ] **Step 4: Implement deployment evidence checks**

For a deployment whose runtime `status` is `active`, require non-TODO deployment identity plus `observed_at` and an `evidence` binding. Otherwise emit `ACTIVE_DEPLOYMENT_UNVERIFIED`. Declared configuration may remain present under `declared_status` without implying runtime observation.

- [ ] **Step 5: Make the CLI fail closed**

`run_audit()` returns `1` whenever semantic violations are present, `0` otherwise. The module entry point calls `sys.exit(run_audit())`.

- [ ] **Step 6: Run focused tests GREEN**

Run: `pytest -q tests/test_ecosystem_registry_projection_hygiene.py`
Expected: all tests pass.

- [ ] **Step 7: Commit validator**

Commit message: `fix(registry): fail closed on semantic projection drift`

---

### Task 3: Reconcile the machine registry as an explicit projection

**Files:**
- Modify: `registry/ecosystem_registry.json`
- Test: `tests/test_ecosystem_registry_projection_hygiene.py`

**Interfaces:**
- Consumes validator semantics from Task 2.
- Produces a registry that passes semantic validation against the exact bounded GitHub observations used for reconciliation.

- [ ] **Step 1: Upgrade root projection metadata**

Set `registry_version` to `0.5.0` and add a `projection` object identifying projection-only authority, the bounded audit revision `0083d64aa5f9395a9aa38ff0ca01ccd9e528fd44`, checked timestamp, `CURRENT` status, and null staleness class.

- [ ] **Step 2: Replace current persona authority with functional roles while preserving history**

Use functional role identifiers where current governance function is actually established; preserve former Amethyst/Sentinel/COLLEEN ownership under `historical_lineage` rather than deleting it. Do not infer a role where current evidence is absent; use an explicit non-authoritative/unknown projection state instead.

- [ ] **Step 3: Correct the verified high-risk project entries**

At minimum reconcile AOGA, Sentinel Governance, Phi-Calculus App, and Acoustic Mesh so current summaries/authority no longer assert inherited DGAF authority, certification/compliance, or incorrect visibility. Preserve historical wording in lineage fields where useful.

- [ ] **Step 4: Make deployment objects evidence-aware**

Replace unsupported `status: active` records with separate declared configuration and observed runtime semantics. No TODO project id may coexist with a current observed-active claim.

- [ ] **Step 5: Add regression assertions for the real registry**

Load `registry/ecosystem_registry.json` in the focused test and assert no semantic violations when supplied the bounded GitHub metadata fixtures for the specifically reconciled projects.

- [ ] **Step 6: Run focused tests**

Run: `pytest -q tests/test_ecosystem_registry_projection_hygiene.py`
Expected: PASS.

- [ ] **Step 7: Commit registry reconciliation**

Commit message: `docs(registry): reconcile projection semantics`

---

### Task 4: Preserve historical propagation boundary and harden CI execution

**Files:**
- Create: `repos/README.md`
- Modify: `.github/workflows/ecosystem-audit.yml`
- Modify: `docs/ECOSYSTEM_AUDIT_STATUS.md`

**Interfaces:**
- The README marks `repos/*/GOVERNANCE.md` mirrors as historical propagation evidence and points to current external repository governance.
- Workflow executes focused tests before the live audit and fails when the auditor returns nonzero.

- [ ] **Step 1: Add historical/supersession boundary**

Document that `repos/*` mirrors are retained historical evidence of the July 2026 rollout and are not current cross-repository authority sources.

- [ ] **Step 2: Update audit status**

Record issue #694 remediation scope, projection-only semantics, and the distinction between source semantics and runtime observation.

- [ ] **Step 3: Update workflow**

Install `pytest requests`; run `pytest -q tests/test_ecosystem_registry_projection_hygiene.py`; then run `python registry/ecosystem_audit.py`. Add `push`/`pull_request` path triggers for registry, focused tests, and the workflow itself while preserving hourly/manual execution.

- [ ] **Step 4: Validate YAML and targeted tests locally**

Run focused pytest plus a Python import/compile check.

- [ ] **Step 5: Commit CI/docs boundary**

Commit message: `ci(registry): enforce semantic projection hygiene`

---

### Task 5: Rebase issue #694 and validate the exact branch head

**Files:**
- GitHub issue #694 metadata/body
- No scientific-state files unless a test requires an exact non-effect assertion.

- [ ] **Step 1: Update issue #694 sequencing boundary**

Replace the obsolete #679 blocker with the accepted base `0083d64aa5f9395a9aa38ff0ca01ccd9e528fd44`; record dataset lock `ESTABLISHED`, bounded unblinding `AUTHORIZED`, and primary-analysis authorization `NOT AUTHORIZED / NOT RUN` with scientific N increment `0`.

- [ ] **Step 2: Run targeted verification**

Run:

```bash
pytest -q tests/test_ecosystem_registry_projection_hygiene.py
python -m py_compile registry/ecosystem_audit.py
```

Run broader repository Python tests if the full checkout is available. If the harness cannot materialize the full repository, rely on exact-head GitHub Actions for the repository-wide suite and state that limitation explicitly.

- [ ] **Step 3: Open PR against current protected `main`**

PR body must document RED evidence, GREEN evidence, exact base/head, semantic scope, historical preservation, and scientific/control non-effects.

- [ ] **Step 4: Require exact-head CI before merge**

Do not claim completion until returned PR workflow families are terminal and required governance/claim/truth-layer checks pass.
