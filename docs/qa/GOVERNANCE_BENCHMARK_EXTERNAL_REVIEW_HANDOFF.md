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

It also contains a reviewer note, `SHA256SUMS.txt`, `DGAF_SMOKE_CONTRACT_V1.md`, and `run_dgaf_smoke_v1.py`. The smoke files are included as reproducibility inputs only; the review bundle does not embed or assert a smoke PASS.

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

## Operational smoke verification

The governance benchmark bundle and the DGAF smoke contract answer different questions.

- The benchmark bundle evaluates the bounded governance benchmark and admitted falsification layers.
- DGAF Smoke Contract v1 checks whether the exact revision can execute a minimal governed control path, preserve provenance, reject an authority-widening attempt, and block ambiguous promotion.

To reproduce the smoke check from the exact commit under review, use the canonical control-plane dependency lock:

```bash
python -m pip install --require-hashes -r requirements-ci-control-plane-py312-ubuntu2404-x64.lock
python -m pytest -q tests/test_dgaf_smoke_v1.py
python scripts/run_dgaf_smoke_v1.py --output artifacts/dgaf-smoke-v1/result.json
```

A valid smoke result must remain revision-bound and preserve:

```text
SCIENTIFIC_N_INCREMENT=0
AUTHORIZATION_EFFECT=NONE
INDEPENDENT_VALIDATION=NOT_ESTABLISHED
CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED
HIGH_ASSURANCE=NOT_AUTHORIZED
```

Smoke `PASS` means the bounded engineering contract executed successfully. `FAIL` or `NOT_OBSERVED` remains promotion-blocking. None of these outcomes establishes empirical efficacy, independent validation, SOTA status, production certification, or High-Assurance authorization.

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
