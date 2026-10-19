# Governance V3 — shared input envelope (candidate)

**PRE-ADMISSION DESIGN / SAME-SYSTEM ENGINEERING / NO SCIENTIFIC-N INCREMENT.**

This isolated characterization responds to issue #1394. It **does not
edit** frozen C1/C2/D/C3 implementations, original 13 fixtures, pinned
OPA experiment, or any admitted runtime permission gate.

## Typed input acceptance is not a policy decision

A single input_envelope_v1.json contract and input_envelope.py validator
run **before** each candidate comparator. INPUT_REJECTED is a separate
invalid-input result; all policy columns read NOT_EVALUATED. Never
reinterpret it as a policy DENY or include it in historical efficacy
denominators. A real Boolean False is structurally valid and then the
historical policy denies it.

- Root must be a plain mapping with action as an object with exactly the
  three Boolean authorized, tool_allowed, target_allowed fields.
- authority_context, claim, and flow can be omitted or null. If nonnull,
  each must be a complete typed object matching every listed field.
  Partial/sparse domains are rejected even if C3 would skip missing keys.
- Known historical fixture metadata may be supplied for bookkeeping only.
  Reject all unexpected fields and types; never coerce truthy values.
- The contract is deliberately STRICTER than historical conditionals.
  It is a **proposal**, not established production JSON Schema or
  evidence that missing optional domains are safe live permissions.
- Admitted input is copied and evaluated with unchanged historical rules.

## Reproduction from the pinned Python 3.12 Ubuntu 24.04 CI environment

~~~bash
python -m pytest tests/test_governance_benchmark_v3_input_envelope.py -q -rs
python -m experiments.governance_benchmark.v3.characterize \
  --output /tmp/dgaf-v3-characterization.json
~~~

The original 13 well-formed fixture cases should be admitted. Synthetic
D vs C3 retains original decisions; four-way equality may be less because
C1 and C2 intentionally implement less complete policies.

Optional actual-engine verification uses both --opa-bin and --opa-policy,
with OPA v1.21.2 exact static binary SHA-256 validation. Policy must
be explicitly supplied from the separate review-controlled Rego source.
No engine supplied means real_opa_executed=false, not a hidden skip
reported as external-engine success.

~~~bash
python -m experiments.governance_benchmark.v3.characterize \
  --opa-bin /approved/location/opa \
  --opa-policy /approved/source/opa_c3_v1.rego \
  --output /tmp/dgaf-v3-opa-characterization.json
~~~

Policy source digest is recorded. No versioned C3 or DGAF comparator was
replaced or quietly normalized; comparators receive the same valid data.
Reject invalid cases before calling any policy. Explicitly account for
admitted, input-rejected and policy outcomes in separate denominators.

## Review gates and epistemic limits

Technical non-author review is required for root/optional-domain typing,
unknown keys, null semantics, provenance, implementation and exceptions.
Methodological review is required for fairness and prospective oracle,
and independent authorized operator/custodian requirements remain separate.
Retain first failures and exact source identities. No historical metrics
or scientific data may be rewritten, pooled or upgraded.

This does NOT authorize live providers, execution drivers, high assurance,
independent validation, state-of-the-art or canonical DGAF efficacy.
SCIENTIFIC_N_INCREMENT=0.
INDEPENDENT_VALIDATION=NOT_ESTABLISHED.
CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED.
HIGH_ASSURANCE=NOT_AUTHORIZED.
