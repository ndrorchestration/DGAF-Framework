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


## One-command reviewer protocol

A reviewer may use the creation-only protocol below instead of manually
assembling a return record. Read the frozen commit and bundle SHA-256 from
controller #1067, then run from that exact checked-out commit:

```bash
python experiments/governance_benchmark/run_independent_reviewer_protocol.py \
  --expected-commit <FROZEN_COMMIT_FROM_ISSUE_1067> \
  --expected-bundle-sha256 <FROZEN_SHA256_FROM_ISSUE_1067> \
  --output-dir reviewer-result-first \
  --reviewer-id "<durable reviewer identity>" \
  --affiliation "<affiliation>" \
  --relationship-disclosure "<relationship/conflict disclosure>" \
  --environment-note "<environment and relevant limitations>"
```

The protocol independently checks the checked-out commit, runs the bounded
handoff test set, regenerates the deterministic review bundle, compares its
SHA-256 to the frozen controller value, and writes
`independent-review-record.json`.

The first record is creation-only and MUST be preserved. The protocol refuses
to overwrite it. Any diagnostic rerun must use a different output directory and
retain the first result.

Possible protocol dispositions are:

- `REPRODUCED`: frozen commit, tests, and bundle digest matched;
- `MISMATCH`: the exact target was reached but tests or bundle digest differed;
- `BLOCKED`: the frozen commit was not reached or execution encountered a
  prerequisite/tooling blocker.

These dispositions are reproduction findings only. The script does not
adjudicate reviewer independence and cannot promote
`INDEPENDENT_VALIDATION`, scientific N, efficacy, SOTA status, or
High-Assurance authorization.

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
