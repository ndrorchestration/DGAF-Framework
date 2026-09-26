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
- GB-008: compromised delegated sub-agent;
- GB-009: valid independently verified claim;
- GB-010: explicitly authorized sensitive-data composition;
- GB-011: valid delegated requester;
- GB-012: valid intent-bound model action;
- GB-013: attested non-widening delegated sub-agent.

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
classes, false blocks, and decision-step counts. The report also records the
incremental decision-step cost of DGAF relative to the hardened policy baseline.

## Evidence boundary

A passing run establishes only that this exact synthetic harness behaves as
specified. It does not establish general DGAF efficacy, external validity,
independent validation, production safety, standards compliance, or
state-of-the-art status.


## Metamorphic mutation suite

`run_mutations.py` starts from legitimate seed cases and flips one governance
predicate at a time. The current bounded suite generates 10 mutations:

- five authority-context mutations from a valid delegated-action seed;
- three epistemic mutations from a valid independently supported claim;
- two flow mutations from an explicitly authorized sensitive-data composition.

This produces 30 baseline decisions across C1, C2, and DGAF. The expected
property is structural: C2 and DGAF should catch authority-context violations,
while only DGAF should catch the current epistemic and composed-flow violations.

Run:

```bash
python experiments/governance_benchmark/run_mutations.py
python -m pytest tests/test_governance_benchmark_mutations.py
```

The suite is deterministic and intentionally small. It is not randomized fuzzing
and does not establish robustness outside the enumerated mutation dimensions.


## Two-factor interaction suite

`run_interactions.py` combines two previously isolated governance degradations
in a single case. The current bounded suite contains seven interactions:

- three authority interactions;
- three epistemic interactions;
- one composed-flow interaction.

These tests ask whether the control behavior remains stable when more than one
condition degrades at once. They do not establish emergent robustness or broad
adversarial generalization.

Run:

```bash
python experiments/governance_benchmark/run_interactions.py
python -m pytest tests/test_governance_benchmark_interactions.py
```

Authority-only interactions remain creditable to hardened runtime policy as well
as DGAF. Epistemic and composed-flow interactions count as DGAF incremental
scope only within this synthetic model.
