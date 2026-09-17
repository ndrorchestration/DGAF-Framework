# Provider-Neutral External Runtime Adapter Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Implement a deterministic, provider-neutral ingress validator that accepts external runtime events only as non-authoritative DGAF input records and fails closed on missing, malformed, stale, replayed, unsupported, or authority-upgrading inputs.

**Architecture:** Add a versioned machine-readable contract, a small pure-Python validator/canonicalizer, and focused fixtures/tests. Provider-specific integrations remain out of scope; all named runtimes terminate at the neutral `ExternalRuntimeEnvelope V1` boundary. Admission means only that an external input record is structurally and semantically acceptable for DGAF-owned downstream evaluation; it never grants execution authority.

**Tech Stack:** Python 3, stdlib `json`/`hashlib`/`datetime`, pytest, JSON fixtures.

**Spec:** `docs/superpowers/specs/2026-09-17-provider-neutral-external-runtime-adapter-design.md`

## Global Constraints

- Preserve `PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0` and all current Track A boundaries.
- No named provider adapter or provider-specific trust rule in this tranche.
- External verification and authorization assertions are metadata only; they cannot directly establish DGAF verification or authorization.
- Record identity and effect identity remain distinct; replay protection is keyed to effect identity.
- Exactly-once execution remains `NOT_ESTABLISHED`.
- Unknown or missing required consequence/reversibility fields fail closed when the requested action class requires them.
- Use only Python standard-library dependencies.

---

### Task 1: Machine-readable ingress contract

**Files:**
- Create: `registry/external_runtime_adapter_contract_v1.json`
- Test: `tests/test_external_runtime_adapter_contract.py`

**Interfaces:**
- Consumes: design spec constants and existing Action Admission record/effect identity semantics.
- Produces: versioned field sets, allowed statuses, rejection codes, validation order, and non-effect declarations consumed by the validator/tests.

- [ ] **Step 1: Write the failing contract test**

Create `tests/test_external_runtime_adapter_contract.py` asserting:

```python
contract["version"] == "EXTERNAL_RUNTIME_ENVELOPE_V1"
contract["status"] == "NON_AUTHORITATIVE_INGRESS_CONTRACT"
contract["authority_semantics"] == "PRESENTED_NOT_GRANTED"
contract["exactly_once"] == "NOT_ESTABLISHED"
"record_id" not in contract["effect_identity_fields"]
contract["provider_specific_trust"] == "PROHIBITED"
```

Also assert the stable rejection taxonomy includes `MALFORMED_IDENTITY`, `STALE_EVIDENCE`, `DUPLICATE_EFFECT`, `AUTHORITY_MISMATCH`, `UNSUPPORTED_ACTION_CLASS`, `PROVIDER_SUBSTITUTION`, `MISSING_REQUIRED_FIELD`, and `UNKNOWN_REQUIRED_DIMENSION`.

- [ ] **Step 2: Run the focused test and verify RED**

Run: `pytest -q tests/test_external_runtime_adapter_contract.py`
Expected: FAIL because `registry/external_runtime_adapter_contract_v1.json` does not exist.

- [ ] **Step 3: Add the minimal contract JSON**

Define the exact V1 required fields, record/effect identity fields, validation order, rejection codes, non-authority semantics, and scientific/governance non-effects required by the spec.

- [ ] **Step 4: Re-run the focused test**

Run: `pytest -q tests/test_external_runtime_adapter_contract.py`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add registry/external_runtime_adapter_contract_v1.json tests/test_external_runtime_adapter_contract.py
git commit -m "test: define external runtime ingress contract"
```

### Task 2: Deterministic envelope validator

**Files:**
- Create: `dgaf/external_runtime_adapter.py`
- Modify: `tests/test_external_runtime_adapter_contract.py`

**Interfaces:**
- Consumes: `validate_external_runtime_envelope(envelope: dict, *, seen_effect_ids: set[str] | None = None, now: datetime | None = None) -> dict`.
- Produces: a deterministic result with `decision`, `rejection_code`, `record_identity`, `effect_identity`, `normalized_envelope`, and `authority_effect`.

- [ ] **Step 1: Add failing behavior tests**

Cover one accepted envelope plus each required fail-closed case: malformed identity, stale evidence, duplicate effect, authority mismatch, unsupported action class, provider-name substitution, missing field, and required consequence/reversibility set to `UNKNOWN`.

The accepted result must satisfy:

```python
assert result["decision"] == "ADMITTED_AS_NON_AUTHORITATIVE_INPUT"
assert result["authority_effect"] == "NONE"
assert result["record_identity"].startswith("sha256:")
assert result["effect_identity"].startswith("sha256:")
```

- [ ] **Step 2: Run the focused tests and verify RED**

Run: `pytest -q tests/test_external_runtime_adapter_contract.py`
Expected: FAIL because `dgaf.external_runtime_adapter` is absent.

- [ ] **Step 3: Implement minimal deterministic validation**

Use only stdlib modules. Validation order must be stable and stop at the first rejection. Canonical identities use UTF-8 JSON with `sort_keys=True`, compact separators, and SHA-256. External `verification_assertion` and `authority_presented` values are retained in the normalized record but never transformed into DGAF-granted authority.

- [ ] **Step 4: Re-run focused tests**

Run: `pytest -q tests/test_external_runtime_adapter_contract.py`
Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add dgaf/external_runtime_adapter.py tests/test_external_runtime_adapter_contract.py
git commit -m "feat: add fail-closed external runtime ingress validator"
```

### Task 3: Fixtures and regression boundary

**Files:**
- Create: `tests/resources/external_runtime_adapter/valid_envelope.json`
- Create: `tests/resources/external_runtime_adapter/provider_substitution.json`
- Modify: `tests/test_external_runtime_adapter_contract.py`

**Interfaces:**
- Consumes: `validate_external_runtime_envelope` from Task 2.
- Produces: stable provider-neutral regression fixtures demonstrating that provider labels cannot alter semantic admission.

- [ ] **Step 1: Add failing fixture-driven tests**

Assert the valid fixture is admitted and the provider-substitution fixture returns `PROVIDER_SUBSTITUTION`; assert changing only an untrusted provider display label never changes evidence or authority class.

- [ ] **Step 2: Run and verify RED until fixtures exist**

Run: `pytest -q tests/test_external_runtime_adapter_contract.py`
Expected: FAIL due to missing fixtures.

- [ ] **Step 3: Add the two minimal fixtures**

Use synthetic provider names only; do not encode special cases for ECC, LangGraph, OpenAI, Microsoft, or other named runtimes.

- [ ] **Step 4: Run focused and adjacent tests**

Run:

```bash
pytest -q tests/test_external_runtime_adapter_contract.py tests/test_action_admission_authority_contract.py
```

Expected: PASS.

- [ ] **Step 5: Commit**

```bash
git add tests/resources/external_runtime_adapter tests/test_external_runtime_adapter_contract.py
git commit -m "test: add provider-neutral ingress fixtures"
```

### Task 4: Repository verification and PR readiness

**Files:**
- Modify only if required by existing project conventions after test evidence identifies a real need.

**Interfaces:**
- Consumes: all Task 1-3 artifacts.
- Produces: exact-head CI evidence and a PR state suitable for review without claiming runtime authority or scientific advancement.

- [ ] **Step 1: Run focused local suite**

```bash
pytest -q tests/test_external_runtime_adapter_contract.py tests/test_action_admission_authority_contract.py
```

Expected: PASS.

- [ ] **Step 2: Run repository quality commands used by CI**

Use the repository's existing Python quality/test entrypoints; do not alter unrelated failures.

- [ ] **Step 3: Update PR #774 description if implementation scope changed**

Explicitly preserve: no provider integration, no runtime authority, no new action class, no scientific transition, no efficacy claim, and no High-Assurance promotion.

- [ ] **Step 4: Verify exact-head GitHub workflow results**

Require all returned workflow families for the implementation head to complete successfully before describing the branch as verified.

- [ ] **Step 5: Stop at protected-branch gate**

Do not bypass required checks, signed-commit rules, review requirements, or branch protection.