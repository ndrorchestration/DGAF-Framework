# P4 Mode T Admission-Policy Binding — Synthetic Contract

**Date:** 2026-09-06  
**Tracker:** #316  
**State:** PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · empirical N=0  
**Evidence class:** engineering/synthetic contract only

## Purpose

The authenticated Confidential Space token path proves that Google signed a token and that its claims match an `AttestationExpectation`. That is necessary but not sufficient for P4 admission: the execution principal must also be unable to substitute a different otherwise-valid expectation after authorization.

This tranche defines the synthetic contract for binding one canonical security-critical admission policy into the pre-execution authorization lineage.

It does **not** implement or claim independently retained production authorization evidence.

## Static policy identity

`mode_t_admission_policy.py` defines a canonical static policy identity and SHA-256 digest. The identity includes the reviewed security-sensitive fields that must remain fixed across PRE and POST:

- Google Cloud Attestation issuer and OEM identity;
- exact audience;
- exact Confidential Space VM subject/selfLink;
- exact service-account set;
- Confidential Space software identity;
- TDX hardware identity and Intel attester TCB requirement;
- Secure Boot required;
- debug disabled and STABLE support attribute;
- memory monitoring disabled;
- exact digest-pinned workload image;
- exact container argv;
- exact command override expectation;
- exact explicit non-secret environment;
- environment override prohibition;
- restart policy;
- maximum accepted clock skew.

The policy identity deliberately excludes the attestation phase and phase nonce/binding digest. PRE binds the single-use authorization-consumption record C; POST binds the output-manifest digest. Both phases must nevertheless resolve to the same static policy identity.

## Explicitly incomplete policy field

The signed-token lifetime upper-bound policy remains **OPEN REVIEW**. The v1 policy identity therefore carries:

- `token_lifetime_upper_bound_seconds = null`;
- `token_lifetime_policy = OPEN_REVIEW_NOT_PRODUCTION_COMPLETE`;
- `production_policy_complete = false`.

This is intentional. The repository must not silently convert a documented provider token lifetime into a local authorization policy without explicit review.

## Synthetic R → A → C binding

The integrated synthetic lifecycle now requires `admission_policy_sha256` when reservation R is constructed.

The exact digest is then carried through:

`R → A → C → PRE policy check → output manifest → POST/final lineage`

The synthetic C record remains labeled:

`SYNTHETIC_MODEL_ONLY_NOT_INDEPENDENTLY_RETAINED`

A matching digest in this record is therefore not equivalent to independently retained authorization evidence.

## Fail-closed anti-substitution control

Before synthetic key acquisition, `verify_synthetic_consumption_policy_binding(...)` recomputes the canonical policy digest from the supplied expectation and requires exact equality with the digest carried by C.

Deterministic negative controls reject:

- a C record bound to policy P1 when a different otherwise-valid expectation P2 is supplied;
- mutations of individual security-sensitive expectation fields;
- duplicate service-account entries;
- unknown or promotable synthetic-retention states;
- attempts to treat the synthetic record as independently retained or production-complete.

The integrated lifecycle tests also require the same policy digest in R, A, C, the output manifest, and the final synthetic lineage result.

## Production boundary still open

This tranche does **not** satisfy #316's production requirement.

Production P4 admission still requires a source of authenticated, independently retained and re-verifiable R/A/C evidence (or an equivalent authorization capability) whose policy digest was fixed before execution. Production key generation must consume that evidence and require exact policy equality before token admission and entropy generation.

The current synthetic ledger cannot be promoted to that role.

The exact real VM subject/selfLink also remains unresolved until an authenticated Confidential Space launch instance exists. The launch-contract digest in #317 is not the final admission-policy digest and must not be promoted as one.

## Evidence interpretation

Passing unit tests or GitHub Actions for this tranche can establish only that the synthetic contract is implemented and its negative controls pass at the tested commit.

It cannot establish:

- real Google Confidential Space admission;
- independent retention;
- real P4 custody;
- protocol freeze;
- pilot authorization;
- empirical execution;
- empirical efficacy.

**Controlling state remains P4 OPEN · PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · empirical N=0.**
