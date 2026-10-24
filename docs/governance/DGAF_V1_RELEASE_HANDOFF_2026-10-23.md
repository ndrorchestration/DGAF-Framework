# DGAF v1 — Dated Release and Review Handoff (2026-10-23)

**Document class:** operational status / G3 reconciliation candidate; **NOT an admitted gate, frozen preregistration, approval, or scientific result**.

## Release boundary

- `DGAF_V1_RELEASE=HOLD`. Last verified protected-main baseline for this handoff: `1a95b94332dffb404c5a3ce026d70781a8c10b90`. Recheck repository settings and protected main before relying on these dated facts.
- No final v1 release SHA/tree, independent Gate 5 disposition, or G1–G6 acceptance has been established.
- `SCIENTIFIC_N_INCREMENT=0`, `INDEPENDENT_VALIDATION=NOT_ESTABLISHED`, `CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED`, `HIGH_ASSURANCE=NOT_AUTHORIZED`.

## Protected-main approval and signing — last recorded policy readback

Protected main required **one approval from an eligible non-author**, approval of the latest push by someone other than its pusher, stale review dismissal, verified signed commits, linear history, admin enforcement, no force push, and no branch deletion. Strict required status contexts recorded:

1. `PPTL CI`
2. `Governance CI`
3. `PR Issue-State Keyword Guard`
4. `security-scan`
5. `test (3.10)`
6. `test (3.11)`
7. `test (3.12)`

The four Python contexts are **jobs** emitted by `Python Tests & Quality Checks`; `staging-evidence` and `integration-tests` are not thereby globally required. Production/Preview environments were recorded as protected-branch-restricted; environment-admin bypass remained available and required environment reviewers were not configured. These are dated settings observations, not a live readback or authorization to change settings.

**Review separation:** Role A must be outside implementation with no repository write/admin access during review, disclose conflicts, reproduce the exact SHA/tree from a clean checkout, hash retained evidence and issue a written disposition. Role B must be a separate authorized write-capable GitHub approver eligible under branch protection and latest-push rules. Automated review does not replace either role. See issues #1452 and #1459. No review approval is inferred from CI.

## Signed release ancestry — all unadmitted

- [#1472](https://github.com/ndrorchestration/DGAF-Framework/pull/1472), dependency + Track A bootstrap, exact signed head `9021817faa6ba66c8e603de73d04f4a44821e36a`. Canonical remediations include Black 26.10.1 and certifi 2026.10.19. Independent Role A/B admission outstanding.
- [#1492](https://github.com/ndrorchestration/DGAF-Framework/pull/1492), Gate 0 documentation, signed stacked head `7f5fa18b3f8208b06c8d22e70dede4cfd04b8c91`.
- [#1493](https://github.com/ndrorchestration/DGAF-Framework/pull/1493), PDMAL publication guard, signed stacked head `0b3d353b3ef6cb5e59ed0624aaabd130614e9afa`.
- [#1495](https://github.com/ndrorchestration/DGAF-Framework/pull/1495), six-lane phase-three candidate, signed head `57ef6472c5d4493c652683f539533d90e4efd8e0`. Later credential argv hardening in unsigned [#1500](https://github.com/ndrorchestration/DGAF-Framework/pull/1500) is absent from this signed source. Its acceptance requires signed reconstruction and full checks.
- Track A/PDMAL denial workflow results remain **fail-closed policy evidence**, not globally green admission; never weaken these guards to manufacture a passing release.

## Bounded test and documentation progress

| Candidate | Exact last inspected head | Evidence and scope | Admission |
| --- | --- | --- | --- |
| [#1502 G2 Tektite](https://github.com/ndrorchestration/DGAF-Framework/pull/1502) | `6390fb7c07780a2b0245f1a6e6c39251ca83d25e` | Two 503-denial/no-fetch cases explicitly pass in hosted UI run 39922003125; 119/119 UI tests. Main-based security scan fails on old Black/certifi baseline. | DRAFT / HOLD |
| [#1503 G4 AAR](https://github.com/ndrorchestration/DGAF-Framework/pull/1503) | `41be96c0418db0a11bd02ecf24aefdbceea7536b` | Non-object and malformed denial/no receipt tests; seven exact-reason validator cases pass hosted UI run 40019939879; 120/120 UI tests. | DRAFT / HOLD |
| [#1504 G3 Herald docs](https://github.com/ndrorchestration/DGAF-Framework/pull/1504) | `081202fd1ff867f1372a96689db36b8c6e2794ad` | Module header reconciles explicit local auth opt-in. One file, documentation-only; 9 associated workflows success, not full protected-main checks. | DRAFT / HOLD |

## Bounded technical claims

G1 registers only `AUDIT_COUNTER_UPDATE_V1 -> POST /api/audit`, an in-memory, non-scientific action. No durable cross-instance replay prevention, authoritative post-issuance revocation, general production AAR issuer/trust-anchor lifecycle or other action-class coverage is established. G4 tests show named route/validator denial behaviors; a postcondition failure can follow state writes and cannot be generalized to rollback or exactly-once semantics. G2 remains blocked by unadmitted Herald and PDMAL publication/custody boundaries despite Tektite's successful negative tests.

## Ordered next admission tasks

1. Obtain a genuinely eligible independent Role A review of exact #1472 SHA/tree and a distinct authorized Role B approver. Neither has been recorded.
2. Admit prerequisite signed ancestry **only** through protected-main policy with all exact required checks, signatures and human approvals.
3. Reconstruct reviewed #1500 credential-hardening and G2/G3/G4 test/documentation deltas without changing content, under authorized signed integration ancestry. Rerun all required checks on each final admitted source SHA.
4. Bind G1–G6 evidence, Production/Preview settings readback, SBOM manifest and custody, exclusions, residual risks, and adjudications to the *final* release candidate SHA. Do not claim readiness from a predecessor branch's successful tests.
5. Preserve historical status, original preregistration and frozen gate maps, as well as research N=0. No automatic merges, publication or production deployment.

## Source of truth

- [Release controller #1453](https://github.com/ndrorchestration/DGAF-Framework/issues/1453)
- [G3 document reconciliation #1450](https://github.com/ndrorchestration/DGAF-Framework/issues/1450)
- [External reviewer coordination #1459](https://github.com/ndrorchestration/DGAF-Framework/issues/1459)
- [Role separation #1452](https://github.com/ndrorchestration/DGAF-Framework/issues/1452)
- [G2 exclusion matrix #1448](https://github.com/ndrorchestration/DGAF-Framework/issues/1448)
- [G4 fault matrix #1446](https://github.com/ndrorchestration/DGAF-Framework/issues/1446)

This dated handoff is not a claim that a final source is accepted. Re-read live GitHub source and settings before changing any release state.
