# Governance Benchmark External Review Handoff

This handoff describes how to reproduce the bounded DGAF governance benchmark
without relying on an operator-created archive.

## Build the review bundle

From the exact commit under review:

```bash
python experiments/governance_benchmark/package_review_bundle.py \
  --output DGAF-governance-benchmark-review.zip
```

The generated ZIP contains fixed benchmark output, mutation results,
same-domain interactions, cross-domain interactions, the canonical evidence
manifest, the evidence envelope, and all currently admitted falsification
layers:

- strong-policy fixed-fixture parity;
- exhaustive bounded semantic equivalence;
- neutral reusable-abstraction configuration scaling.

It also contains a reviewer note and `SHA256SUMS.txt`.

The ZIP writer uses fixed metadata and sorted filenames so two unchanged runs
produce the same archive digest.

## Verify

Run:

```bash
python -m pytest \
  tests/test_comparative_governance_benchmark.py \
  tests/test_governance_benchmark_mutations.py \
  tests/test_governance_benchmark_interactions.py \
  tests/test_governance_benchmark_cross_domain.py \
  tests/test_governance_benchmark_evidence_manifest.py \
  tests/test_governance_benchmark_evidence_envelope.py \
  tests/test_governance_benchmark_review_bundle.py \
  tests/test_governance_benchmark_strong_policy.py \
  tests/test_governance_benchmark_semantic_equivalence.py \
  tests/test_governance_benchmark_configuration_scaling.py \
  tests/test_standards_risk_crosswalk.py
```

## Independent review boundary

An external reviewer should clone the repository independently, check out the
exact commit, regenerate the bundle, run the tests, and report the result from
their own environment.

The negative/parity layers are part of the evidence and must not be omitted or
reinterpreted as failures to be tuned away. In particular, decision parity or
configuration-scaling parity does not establish architectural equivalence, and
it does not establish DGAF superiority.

A matching bundle or passing test run is engineering verification. It does not,
by itself, establish independent validation, canonical efficacy, scientific-N
increment, regulatory compliance, production certification, SOTA status, or
High-Assurance authorization.
