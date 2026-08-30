# Epistemic Claim Classification Standard

**Effective for:** N=1 operational characterization and subsequent PDMAL study records

## Rule

No project statement may compress implementation, verification, and empirical validation into a single claim.

**Implementation != Verification != Empirical Validation.**

## Classifications

| Class | Meaning | Permitted evidence basis |
|---|---|---|
| Observed | Directly present in an artifact, log, trace, or execution record | Primary observation |
| Verified | A defined predicate was checked and passed | Reproducible verification evidence |
| Operationally Characterized | The apparatus was exercised end-to-end sufficiently to characterize operation | Bounded execution evidence |
| Inferred | Interpretation derived from established observations | Explicit reasoning from evidence |
| Hypothesized | Proposed mechanism, explanation, or expected result | Theory/design rationale |
| Planned | Intended future activity | Approved plan/protocol |
| Not Established | Evidence is currently insufficient | Explicit absence/uncertainty |

## Prohibited compression

The following substitutions are not permitted:

- `implemented` -> `proven`
- `CI passed` -> `efficacy established`
- `N=1` -> `generalizable effect`
- `deployment ready` -> `scientifically validated`
- `verification passed` -> `hypothesis confirmed`

## N=1 rule

The first successful run may establish **Operationally Characterized** status. It may generate observations relevant to later hypotheses, but it cannot establish a population-level efficacy claim or replace the planned multi-seed experiment.

## Reporting rule

When evidence levels differ within one paragraph or table row, state the classification next to each substantive claim rather than allowing the strongest classification to implicitly cover weaker claims.
