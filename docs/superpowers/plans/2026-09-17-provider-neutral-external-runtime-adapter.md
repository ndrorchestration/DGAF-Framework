# Provider-Neutral External Runtime Adapter Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox syntax for tracking.

**Goal:** Implement a deterministic, provider-neutral ingress validator that admits external runtime submissions only as non-authoritative DGAF input records and fails closed on malformed, stale, replayed, unsupported, ambiguous, or authority-upgrading inputs.

**Architecture:** Follow the repository's established `scripts/validate_*.py` pattern. Add one versioned registry contract, one pure-stdlib validator/canonicalizer, two synthetic fixtures, and one focused pytest module. No named-provider adapter or runtime execution path is introduced.

**Tech Stack:** Python 3 stdlib (`json`, `hashlib`, `datetime`, `re`), pytest, JSON fixtures.

**Spec:** `docs/superpowers/specs/2026-09-17-provider-neutral-external-runtime-adapter-design.md`

## Global Constraints

- Preserve `PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · N=0` and current Track A boundaries.
- External verification/authorization assertions remain untrusted metadata and cannot promote DGAF state.
- `event_id`, `effect_id`, and `source_id` remain distinct; replay protection is effect-bound.
- Exactly-once execution remains `NOT_ESTABLISHED`.
- Consequential requests with missing or `UNKNOWN` required risk metadata fail closed.
- No provider-specific trust rules, network calls, SDK dependencies, durable stores, or new action classes.

---

### Task 1: Contract RED → GREEN

**Files:**
- Create: `registry/external_runtime_adapter_contract_v1.json`
- Test: `tests/test_external_runtime_adapter_contract.py`

- [ ] Add contract tests for schema version, non-authoritative status, `PRESENTED_NOT_GRANTED`, effect-vs-record identity, provider-specific trust prohibition, exactly-once non-claim, validation order, and the spec's stable `DGAF_EXT_*` rejection taxonomy.
- [ ] Run `pytest -q tests/test_external_runtime_adapter_contract.py`; verify RED because the contract artifact is absent.
- [ ] Add the minimal registry JSON matching the approved spec.
- [ ] Re-run the focused test; contract-only assertions must pass while validator/fixture assertions remain RED until their tasks are implemented.

### Task 2: Validator RED → GREEN

**Files:**
- Create: `scripts/validate_external_runtime_adapter.py`
- Modify: `tests/test_external_runtime_adapter_contract.py`

**Interface:**

```python
validate_external_runtime_envelope(
    envelope: dict,
    *,
    seen_effect_ids: set[str] | None = None,
    seen_events: dict[str, str] | None = None,
    now: datetime | None = None,
) -> dict
```

- [ ] Tests import `validate_external_runtime_envelope` from `scripts.validate_external_runtime_adapter` and cover deterministic valid admission plus missing field, malformed identity, digest mismatch, provenance failure, stale evidence, unsupported action/transition, authority mismatch, required risk metadata, duplicate effect, event collision, provider substitution, and external verification/authorization non-promotion.
- [ ] Verify RED because the script is absent.
- [ ] Implement deterministic first-failure validation in the exact spec order. Canonical JSON uses `sort_keys=True`, compact separators, UTF-8, and SHA-256.
- [ ] Accepted output uses `DGAF_EXTERNAL_RUNTIME_ADMISSION_V1`, `EXTERNAL_NON_AUTHORITATIVE_UNTIL_VALIDATED`, `PRESENTED_NOT_GRANTED`, and a content-addressed `record_id`; admission does not authorize the requested transition.
- [ ] Re-run focused tests to GREEN.

### Task 3: Fixture regressions

**Files:**
- Create: `tests/resources/external_runtime_adapter/valid_envelope.json`
- Create: `tests/resources/external_runtime_adapter/provider_substitution.json`
- Modify: `tests/test_external_runtime_adapter_contract.py`

- [ ] Add fixture-driven tests first and verify RED due to missing fixtures.
- [ ] Add only synthetic provider/runtime identities; no ECC, LangGraph, OpenAI, Microsoft, or other named provider is privileged or encoded.
- [ ] Verify `pytest -q tests/test_external_runtime_adapter_contract.py tests/test_action_admission_authority_contract.py` passes.

### Task 4: Exact-head verification

- [ ] Run/observe the repository's existing Python quality/test and governance workflow families on the implementation head.
- [ ] Fix only failures caused by this tranche.
- [ ] Update PR #774 from design-only wording to design+implementation wording while preserving all non-effects.
- [ ] Describe the branch as verified only if every returned exact-head workflow family completes successfully.
- [ ] Do not bypass protected-branch required checks, signature rules, or review gates.
