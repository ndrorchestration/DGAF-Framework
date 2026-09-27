# DGAF Governance Benchmark — External Review Return Template

Use this template only for independent reproduction controller #1067.

The reviewer should retain their evidence independently before the project owner
performs local cryptographic reverification or adjudication.

A negative result is valid. Do not discard a first FAIL / MISMATCH / BLOCKED
result and rerun silently after inspecting outcomes.

Required machine-readable record schema:

`registry/governance_benchmark_external_review_return_v1.schema.json`

Validator:

```bash
python scripts/validate_governance_benchmark_external_review_return.py review-return.json
```

Required fields cover:

- durable reviewer identity, affiliation, and role;
- relationship/conflict disclosure;
- prior artifact authorship/modification and outcome access;
- commercial relationship and reviewer-stated independence;
- operating system, Python, Git, and environment notes;
- exact frozen commit and expected bundle digest;
- first-attempt preservation;
- contract-test result;
- regenerated bundle SHA-256;
- canonical layer digests;
- independently retained evidence location and digest;
- REPRODUCED / MISMATCH / BLOCKED disposition;
- explicit non-promoting claim boundary.

A validator PASS means only that the return record is structurally admissible for
later adjudication. It does not establish reviewer independence or independent
validation by itself.
