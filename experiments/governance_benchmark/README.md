# Comparative Governance Benchmark — First Slice

This directory implements the smallest deterministic slice defined by
`docs/qa/COMPARATIVE_GOVERNANCE_BENCHMARK_SPEC.md`.

It is intentionally synthetic and narrow.

## Included baselines

- `C_POLICY_AS_CODE`: action-level authorization checks.
- `D_DGAF`: the same checks plus bounded epistemic and composed-authority guards.

This is not intended to represent every production policy engine. Baseline C is
a deliberately explicit minimal comparator for the first slice.

## Cases

- GB-001: legitimate low-risk authorized task;
- GB-002: disallowed target;
- GB-003: false epistemic promotion from same-system verification to independent validation;
- GB-004: confidential-read to external-write authority laundering.

## Run

```bash
python experiments/governance_benchmark/run_benchmark.py
python -m pytest tests/test_comparative_governance_benchmark.py
```

Optional retained report:

```bash
python experiments/governance_benchmark/run_benchmark.py \
  --output artifacts/governance-benchmark-first-slice.json
```

Runtime nanoseconds are informational only and must not be treated as stable
performance evidence. The deterministic comparison uses decisions, error
classes, false blocks, and decision-step counts.

## Evidence boundary

A passing run establishes only that this exact synthetic harness behaves as
specified. It does not establish general DGAF efficacy, external validity,
independent validation, production safety, standards compliance, or
state-of-the-art status.
