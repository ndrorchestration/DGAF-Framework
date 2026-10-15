# AOSS v0.6 Stage-A independent-validation identity refresh — 2026-10-15

Status: **PRE-VALIDATION IDENTITY ADDENDUM — NON-AUTHORIZING — CANDIDATE UNTIL ACCEPTED**

Controllers: #929 (external reviewer engagement/evidence return), #901 (Stage-A execution readiness)

Historical accepted handoff:
`docs/research/AOSS_V0_6_STAGE_A_INDEPENDENT_VALIDATION_HANDOFF.md`

Accepted handoff commit:
`92bc930bdd84f6c4258852e764d3e42019e41342`

Historical handoff preparation identity:
`054a300447627f3e87e92b24f16d261abc7d8d77`

Evaluated current DGAF implementation identity:
`9054fc14f4cb8ef7a1b627338b363ee3d9987bd1`

Frozen ACP target remains:
`ndrorchestration/agent-control-plane@dbab7c1afafec524ce7c18157de2089cafe79c87`

This document does **not** rewrite or supersede the historical facts recorded by
the accepted #928 handoff. It is a scoped identity refresh for a reviewer
evaluating the later protected-main implementation after PRs `#1350`, `#1353`,
`#1352`, and `#1356` were admitted.

The original handoff and this addendum must be read together for that current
implementation target. Neither document establishes reviewer independence,
installed-environment acceptance, executable/source-driver acceptance,
destination/attempt acceptance, collection-execution readiness, scientific N,
canonical DGAF efficacy, or High-Assurance authorization.

## 1. Why a refresh is required

The accepted handoff bound an earlier protected-main source identity and a
historical source-driver recipe-catalog Git blob. Subsequent bounded engineering
work:

- corrected the suppressed-budget terminal mapping via #1350;
- added LF checkout policy for hash/blob-bound Stage-A artifacts via #1353;
- admitted a real non-collecting source-driver implementation and hardened exact
  execution identity via #1352;
- added exact recipe-catalog byte re-verification and LF policy before #1352
  admission;
- reconciled the catalog execution-status field after driver admission and added
  the catalog regression to the focused AOSS lane via #1356.

The historical handoff remains valid evidence for what was accepted at that
time. It must not be silently interpreted as binding later source bytes.

## 2. Reconciliation of the original handoff artifact table

All 19 registry paths listed in the original handoff were re-read at evaluated
DGAF commit `9054fc14f4cb8ef7a1b627338b363ee3d9987bd1`.

**18 of 19 Git blob identities are unchanged.**

The only changed original-table artifact is:

| Artifact | Historical handoff blob | Current evaluated blob | Current raw SHA-256 |
|---|---|---|---|
| source-driver recipe catalog | `178471a6a871fec5d5a7a6349f6f439af8667284` | `08271a57063177895df63bfe4c19971398ab26b0` | `0ea0de6a88285c3bf34f50a6924c7e99288d4d3b00b90cfd1855a566d76d583f` |

Current catalog execution status at the evaluated target is
`SOURCE_DRIVER_IMPLEMENTATION_CANDIDATE_NOT_ACCEPTED`. This records that the
implementation candidate exists while preserving non-acceptance and does not
authorize import, ACP execution, or collection.

A reviewer should independently retrieve and verify the unchanged rows from the
historical handoff rather than trusting this reconciliation statement alone.

## 3. Newly admitted executable-identity artifacts

A current review must additionally bind the executable-identity implementation
that did not exist in the historical handoff:

| Artifact | Repository path | Git blob identity |
|---|---|---|
| Stage-A source driver | `scripts/aoss_stage_a/source_driver.py` | `7fb24863ed831acdb15a9915799286a64a268fd1` |
| execution-identity candidate/validator | `scripts/aoss_stage_a/execution_identity_candidate.py` | `0626347a1491590ea67e6105160e0e57854086d9` |
| Stage-A dependency lock | `requirements-aoss-stage-a.lock` | `196d67a51e687f50e1316b95af8af16374407017` |
| checkout byte policy | `.gitattributes` | `0a35353fca4f82e50e480b657886c8f97d29076b` |

The frozen Stage-A dependency-lock SHA-256 remains:

`81c1ade0b76ff38cbdcbe4ddbc615c273f02dc97a9ff055c8c2889940a2ca6bd`

The source-driver implementation binds the frozen ACP repository/commit/core
blob, one frozen recipe class per invocation, the actual recipe-catalog bytes,
the exact source-driver bytes, process argv, working-directory resolution, and
non-promoting execution-identity candidate fields.

The reviewer must recompute content SHA-256 values from independently retrieved
bytes. Repository Git blob identities and owner-reported SHA-256 values are
reference identities, not substitutes for independent recomputation.

## 4. Current evidence that must be freshly supplied

The following are **not established by this addendum** and must not be inferred
from implementation admission or internal operator testing:

- a fresh installed-environment evidence candidate captured after the current
  protected-main implementation was admitted;
- accepted installed-environment evidence for the exact CPython 3.12.3 runtime,
  executable identity and dependency-lock bytes;
- an accepted exact source-driver/executable identity;
- an accepted non-fixture destination and prospective-attempt identity;
- verified reviewer attribution;
- verified reviewer independence;
- an explicit local trust/execution-admission promotion.

Earlier Windows environment candidates captured from unadmitted branches remain
historical engineering evidence only and must not be reused as accepted
post-admission host evidence.

If any required current evidence is unavailable, the reviewer should return
**BLOCKED** for the affected finding rather than substitute an older candidate,
fixture, CI result, operator self-test, or inferred identity.

## 5. Reviewer procedure for the current implementation

For a review targeting evaluated DGAF commit
`9054fc14f4cb8ef7a1b627338b363ee3d9987bd1`:

1. Read the accepted historical handoff first.
2. Read this identity addendum before relying on any handoff source identity.
3. Independently retrieve DGAF at the evaluated commit and ACP at frozen commit
   `dbab7c1afafec524ce7c18157de2089cafe79c87`.
4. Verify the 18 unchanged historical registry blobs and the refreshed recipe
   catalog blob independently.
5. Verify the newly admitted source-driver, execution-identity, dependency-lock,
   and checkout-policy Git objects above.
6. Recompute required SHA-256 identities independently.
7. Compare any later supplied real installed-environment, executable and
   destination/attempt evidence against these exact source identities.
8. Preserve conflict/relationship disclosure before substantive result review.
9. Continue the original handoff procedure without changing frozen contracts
   after outcome inspection.
10. Return ACCEPT, REJECT, BLOCKED, or a stricter equivalent based on the
    independently retained evidence. No positive conclusion is required.

## 6. Non-effects and claim ceiling

This addendum is an identity/navigation artifact only.

It does not authorize source-driver execution or ACP outcome collection. No
study attempt or empirical outcome is created by preparing or accepting this
document.

Current controlling state remains:

```text
trust_promotion=NOT_EXECUTED
reviewer_attribution_verified=false
independence_verified=false
INSTALLED_ENVIRONMENT_ACCEPTANCE=NOT_ESTABLISHED
SOURCE_DRIVER_BINDING=NOT_ESTABLISHED
EXECUTABLE_ACCEPTANCE=NOT_ESTABLISHED
DESTINATION_ACCEPTANCE=NOT_ESTABLISHED
execution_allowed=false
COLLECTION_EXECUTION_READINESS=NOT_ESTABLISHED
SCIENTIFIC_N_INCREMENT=0
EXTERNAL_VALIDATION_ESTABLISHED=FALSE
CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED
INDEPENDENT_VALIDATION=NOT_ESTABLISHED
HIGH_ASSURANCE=NOT_AUTHORIZED
```

## 7. Acceptance semantics

Until this addendum is separately accepted on protected main, it is only a
candidate identity refresh.

If accepted, it supplements the historical #928 handoff for reviews of the
evaluated current implementation identity above. It does not retroactively
alter the historical handoff, does not classify any reviewer as independent,
and does not itself satisfy any #901 acceptance predicate.
