# AKDC Gate 4 — local transactional replay-admission research

**Status:** DRAFT / SYNTHETIC ENGINEERING / NON-AUTHORIZING / NOT MERGE-READY / SCIENTIFIC N=0.

**Dependency:** Gate 3 [draft PR #1520](https://github.com/ndrorchestration/DGAF-Framework/pull/1520) must be independently reviewed before this stacked research proposal can be considered. The candidate files are `experiments/akdc/replay_store_research.py` and `tests/test_akdc_replay_store.py`. This branch is based on Gate 3, not protected main.

## Scope and local evidence

This Python reference experiment uses a **single local file-backed SQLite database** to atomically admit **untrusted external observation records** after the existing DGAF `validate_external_runtime_envelope` contract accepts them. It neither executes tools nor grants authorization.

The local combined test suite passed **42/42, zero skipped** on 2026-10-26: 14 pinned-source Gate 3 ingress tests and 28 Gate 4 replay tests. Pinned reference DGAF validator Git blob: `fab53669c69ea0b26bc9a55bce2ab157ac8f5348` from protected-main `1a95b94332dffb404c5a3ce026d70781a8c10b90`. The tests use synthetic fixtures and fixed observed times; this is not independent external validation or an empirical experiment.

Commands for the PR checkout:

```bash
python -W error::ResourceWarning -m unittest discover -s tests -p 'test_akdc_*.py' -v
```

Coverage includes event/effect deduplication, terminal task transitions, monotonic task sequence/context, validator rollback, stored-result integrity checks, persistence across restart, eight-thread and four-spawn-process single-file contention, refusal of unsupported schema, abrupt termination of an **uncommitted SQL writer** (not physical power loss), an injected post-validation SQL failure, restart-time missing-table refusal, weakened-primary-key refusal, unversioned-partial-store refusal, and the negative controls showing separate databases and untrusted runtime-id rotation do not share replay protection. All observed admissions remain `RECORD_ONLY` and `PRESENTED_NOT_GRANTED`.

**Gate 5 adversarial red/green:** three new startup tests first **FAILED** against the prior `CREATE TABLE IF NOT EXISTS` initialization, demonstrating silent table recreation and missing PK checks. The corrected initializer creates the three tables atomically with the version marker, checks declared column/primary-key shape on every reopen and fails closed on partial unversioned ledgers. A fourth negative control intentionally demonstrates that self-asserted runtime-id rotation can create a distinct replay namespace. Local TDD regression, not a security certification.\n\n**Nonrelease Python CI:** `.github/workflows/akdc-research-python-quality.yml` was added as a branch-scoped matrix for Black, isort, flake8, mypy, Python 3.10–3.12 and a non-waived dependency audit. CI evidence is pending and distinct from the local test result.\n\n## Hard boundaries

- Provider/runtime/source identifiers are **self-asserted and unauthenticated**, without signed identity, delegation validation, revocation or trusted namespace binding.
- Database transaction atomicity is not distributed exactly-once delivery, external-effect idempotency, authorization, network consensus, or durability across filesystems.
- Local process termination and rollback tests do not establish power-loss or file-corruption recovery.
- No real official SDK traces, A2A or MCP servers, streaming, task negotiation, reauthentication, offline transport or consequential outputs were exercised.
- Do not wire the store into `CommitGate`, execution, local MCP, GitHub actions, custody materialization, scientific state, or protected-main policy.
- Test inputs must not be equated to the unfrozen `SYN-AUTH-01` benchmark in [issue #1508](https://github.com/ndrorchestration/DGAF-Framework/issues/1508).

## Gates remaining

1. Review exact-head CI for both stacked PRs; **do not** regard a passing subset as full validation. Gate 3's existing CI security audit is blocked by locked dependency vulnerabilities tracked separately, including [#1477](https://github.com/ndrorchestration/DGAF-Framework/issues/1477).
2. Obtain independent code review and explicit versioned ledger schema / failure-mode policy.
3. Run an external process-kill, disk-full, restore and crash-consistency evaluation before considering durability claims.
4. Freeze official A2A/MCP protocol trace fixtures and compare an ordinary direct adapter against this stateful replay approach.
5. Separately design authenticated principal binding, revocation, event retention and atomic outbox protocol before any production candidate.

Tracking: [issue #1523](https://github.com/ndrorchestration/DGAF-Framework/issues/1523). Claim ceiling: `DGAF_V1_RELEASE=HOLD`; `SCIENTIFIC_N_INCREMENT=0`; `INDEPENDENT_VALIDATION=NOT_ESTABLISHED`; `HIGH_ASSURANCE=NOT_AUTHORIZED`.

**This PR is research-only. Do not merge without separate review and all applicable approval gates.**
