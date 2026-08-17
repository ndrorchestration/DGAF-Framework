# DGAF Evidence Card Schema

**Version:** 1.0
**Status:** Draft

An Evidence Card is the minimum structured record for a consequential DGAF claim.

## Required fields

```yaml
id: DGAF-CLAIM-EXAMPLE-001
claim:
  statement: "Exact claim text"
  class: HYPOTHESIS
  scope: "Explicit tested context"
construct:
  name: "What is being measured"
  definition: "Operational definition"
measurement:
  metric: "Metric name"
  unit: "unit or binary"
  baseline: "Defined comparison/baseline"
  direction: "higher_is_better | lower_is_better | target_range"
test:
  method: "Protocol or test name"
  version: "Protocol version"
  inputs: "Dataset/fixture/workload identifier"
  seeds: "Seed policy"
  controls: "Controlled variables"
ground_truth:
  source: "Ground-truth source or generation method"
  known: true
results:
  summary: "Observed result"
  artifact: "Path, CI run, report, or archive identifier"
uncertainty:
  method: "CI/bootstrap/measurement uncertainty/etc."
  value: "If applicable"
provenance:
  repository: "owner/repo"
  commit: "commit SHA"
  date: "YYYY-MM-DD"
external_references:
  - source: "Reference"
    role: "methodology | benchmark | context | independent_evidence"
    scope: "What the reference actually establishes"
evidence:
  maturity: SPECIFIED
  limitations:
    - "Known limitation"
validation:
  intended_use: "Use for which validation is claimed"
  status: NOT_VALIDATED
```

## Controlled vocabulary

`claim.class` uses the canonical DGAF taxonomy: `DEFINED`, `IMPLEMENTED`, `COMPUTED`, `VERIFIED`, `ATTESTED`, `HISTORICAL`, `HYPOTHESIS`, `METAPHOR`, `UNSUPPORTED`, `DEPRECATED`.

`evidence.maturity` uses: `SPECIFIED`, `TESTED`, `REPRODUCIBLE`, `VERIFIED`, `VALIDATED`, `EMPIRICALLY_SUPPORTED`.

`validation.status` uses: `NOT_VALIDATED`, `CONTEXT_VALIDATED`, `INDEPENDENTLY_REPLICATED`, `REAL_WORLD_VALIDATED`.

These fields are intentionally separate. A claim classified as `HYPOTHESIS` may have a fully reproducible test without becoming a validated result.

## Minimum review requirements

1. Claim text is exact and bounded.
2. Construct is operationally defined.
3. Metric and baseline are explicit.
4. Test procedure and inputs are identifiable.
5. Ground truth is stated or explicitly unavailable.
6. Results point to an artifact or reproducible record.
7. Limitations are recorded.
8. External sources are scoped and do not silently become DGAF evidence.
9. Provenance identifies the code/data state.
10. Validation status is explicit.
