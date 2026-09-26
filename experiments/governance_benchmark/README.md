# Comparative Governance Benchmark — First Slice

This directory implements the smallest deterministic slice defined by
`docs/qa/COMPARATIVE_GOVERNANCE_BENCHMARK_SPEC.md`.

It is intentionally synthetic and narrow.

## Included baselines

- `C1_MINIMAL_POLICY_AS_CODE`: minimal action-level authorization checks.
- `C2_HARDENED_POLICY_AS_CODE`: adds delegation, replay, intent-binding, and workload-attestation guards.
- `D_DGAF`: adds epistemic-authority and composed-authority guards to the hardened runtime-policy checks.

The hardened comparator is included specifically to avoid treating a weak policy
engine as representative of policy-as-code in general. It remains a synthetic
bounded comparator, not a claim about every production policy engine.

## Cases

- GB-001: legitimate low-risk authorized task;
- GB-002: disallowed target;
- GB-003: false epistemic promotion;
- GB-004: confidential-read to external-write authority laundering;
- GB-005: confused deputy;
- GB-006: authorization replay;
- GB-007: prompt-injection intent substitution;
- GB-008: compromised delegated sub-agent.

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
