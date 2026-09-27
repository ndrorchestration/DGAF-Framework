# Governance Benchmark External Review Handoff

This handoff describes how to reproduce the bounded DGAF governance benchmark
without relying on an operator-created archive.


## One-command reviewer helper

The manual commands below remain the review contract. A reviewer may execute the
same contract through the fail-closed helper:

```bash
python scripts/run_governance_benchmark_independent_review.py \
  --expected-commit <commit-from-issue-1067> \
  --expected-bundle-sha256 <bundle-sha256-from-issue-1067> \
  --reviewer-identity "<name-or-reviewer-id>" \
  --affiliation "<affiliation>" \
  --relationship-disclosure "<relationship/conflict disclosure>" \
  --output-dir review-reproduction
```

The helper:

- refuses a checked-out HEAD that differs from the frozen controller target;
- runs the exact bounded reviewer test list;
- regenerates the deterministic review bundle;
- verifies the expected ZIP digest and complete `SHA256SUMS.txt`;
- verifies handoff/envelope commit binding;
- recomputes all Envelope V2 canonical layer digests from archived payloads;
- writes `review-reproduction/review_receipt.json`;
- records the first result as `REPRODUCED`, `MISMATCH`, or `BLOCKED`.

The receipt is local reviewer evidence and is not automatically trusted,
uploaded, or admitted. The helper does **not** prove reviewer independence; the
identity, affiliation, relationship/conflict disclosure, execution environment,
and separately retained evidence still require review under issue #1067.

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
- neutral reusable-abstraction configuration scaling;
- matched recovery/composition parity;
- matched provenance-custody parity.

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
  tests/test_governance_benchmark_recovery_composition.py \
  tests/test_governance_benchmark_provenance_custody.py \
  tests/test_standards_risk_crosswalk.py
```

## Independent review boundary

An external reviewer should clone the repository independently, check out the
exact commit, regenerate the bundle, run the tests, and report the result from
their own environment.

The negative/parity layers are part of the evidence and must not be omitted or
reinterpreted as failures to be tuned away. In particular, decision parity or
configuration-scaling, recovery/composition, or provenance-custody parity does
not establish architectural equivalence, and none establishes DGAF superiority.

A matching bundle or passing test run is engineering verification. It does not,
by itself, establish independent validation, canonical efficacy, scientific-N
increment, regulatory compliance, production certification, SOTA status, or
High-Assurance authorization.
