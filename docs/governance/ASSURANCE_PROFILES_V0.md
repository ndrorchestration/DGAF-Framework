# Assurance Profiles v0 — extraction boundary

Status: **generic core accepted / bounded same-owner cross-repository API/conformance portability accepted for one consumer / non-authorizing / repository-local exact-SHA distribution selected**

Extraction controller: #1242 (completed). Distribution-boundary controller: #1271.

## Purpose

Assurance Profiles v0 extracts reusable assurance mechanics already present in
AOSS without promoting AOSS Stage-A research semantics into a general-purpose
product claim.

The generic layer answers five bounded questions:

1. What exact source/system is being observed?
2. What was measured directly, derived, unmeasured, or not established?
3. Which source/runtime/environment/artifact identities are bound?
4. Can retained evidence be replayed and integrity-checked under an explicit contract?
5. Are the declared readiness/review predicates satisfied for the stated scope?

A positive result is an assurance result only. It is not execution authority,
scientific validation, efficacy evidence, certification, or High-Assurance
acceptance.

## Generic records

The initial core exposes:

- `SourceBinding`
- `MeasurementField`
- `MeasurementContract`
- `ReplayContract`
- `ReplayReceipt`
- `ReadinessPredicate`
- `ExternalReviewDisclosure`
- `ExternalReviewReceipt`
- `AssuranceProfile`
- `AssuranceDecision`

The corresponding machine-readable profile shape is defined in
`schemas/assurance_profile_v0.schema.json`.

## Required invariants

- observation != validation;
- validation != authorization;
- readiness != execution permission;
- replay match != independent replication;
- positive external review != local acceptance;
- source-origin labels do not create authority;
- consequential missing evidence fails closed;
- unsupported state remains `UNMEASURED` or `NOT_ESTABLISHED`;
- receipts remain bound to exact source/artifact identities;
- assurance decisions have no scientific-N or efficacy effect.

Every `AssuranceDecision` therefore carries:

```text
authorization_effect=NONE
execution_effect=NONE
scientific_n_increment=0
efficacy_effect=NONE
```

## Extracted from AOSS concepts

Reusable concepts are derived from the existing AOSS profile bundle:

- measurement manifest and observer boundary;
- source/runtime/environment identity binding;
- artifact digest and replay receipt rules;
- readiness predicates and explicit blockers;
- reviewer independence disclosure;
- external evidence retention;
- separation between external positive review and local acceptance.

This extraction does not change or replace the original AOSS contracts.

## Explicit exclusions

The generic core does not contain:

- Stage-A comparator semantics;
- historical O/M/R meanings;
- ACP-specific event classes;
- the frozen 16-class corpus;
- repetition or seed plans;
- failure-injection ground truth;
- primary or secondary endpoints;
- multiplicity/statistical analysis rules;
- practical-effect/adoption thresholds;
- collection authorization;
- scientific-N transition logic;
- DGAF/PDMAL efficacy semantics;
- High-Assurance authorization.

Those remain profile/research-specific.

## Bounded portability evidence

The second-system gate has been exercised for one materially different
non-AOSS consumer. This is same-owner API/conformance evidence only.

Accepted identities now include:

- generic core: DGAF PR #1244, protected-main merge
  `86120d604d9eb747a722c33a299898f79808f6ef`;
- core module Git blob at that merge:
  `14df8c2bfdb46f49ac6b9f20fcd0a699a131e82d`;
- schema Git blob at that merge:
  `68ecf07d20d02709960277f7d72e27dab396c94f`;
- canonical second-system consumer:
  [ai-prompt-systems-portfolio PR #13](https://github.com/ndrorchestration/ai-prompt-systems-portfolio/pull/13),
  reviewed head `0622114945abddde7a2a2a6f4c562797d2f3f503`,
  merged as `56d3da4106e50632f16a8a263e61f16a06190423`;
- refreshed consumer exact-head workflows before merge:
  Assurance Profiles portability probe, Common Evaluation Object Model, and
  Public portfolio integrity: all SUCCESS.

Historical portability runs remain valid only for their listed identities.
The accepted consumer merge does not convert same-owner conformance evidence
into independent validation.

The consumer uses its real prompt/evaluation mapping and fetches the upstream
core from the immutable source SHA rather than vendoring a separate copy.
The probe covers direct, derived, and explicitly unmeasured fields; exact
source binding; replay/integrity; missing-evidence rejection; blocked
readiness; and positive review that remains non-authorizing.

These results remain bound to the listed revisions. Refreshing this
candidate onto current main does not transfer historical CI or consumer
results to the new head. A refreshed consumer pin requires its own exact-head
probe; source equivalence alone is not a fresh execution result.

## Distribution boundary

Controller #1271 selects the smallest currently justified distribution shape:

**repository-local canonical source + exact accepted commit pinning**.

For v0:

- canonical implementation remains `components/assurance_profiles.py` in DGAF;
- canonical schema remains `schemas/assurance_profile_v0.schema.json`;
- consumers pin an immutable accepted DGAF commit rather than `main`;
- consumers fetch or vendor only under an explicit provenance record and must
  preserve the source commit identity used for their conformance run;
- source equivalence, a matching Git blob, or package availability does not
  transfer CI, validation, or authority from another revision;
- schema and implementation are treated as one reviewed v0 boundary; a
  consumer must not silently mix a schema from one accepted revision with
  implementation from another;
- superseding the v0 source requires a new accepted DGAF source identity and
  a fresh consumer conformance run before the new pin is called exercised.

No PyPI package, standalone repository, service, dependency admission, or
release channel is justified by current consumer needs. A future installation
or multi-consumer maintenance need may reopen that decision under a separate
controller.

This choice is intentionally a **distribution constraint**, not a maturity
promotion. Exact-SHA availability does not establish production readiness,
certification, independent validation, or support guarantees.

## Claim ceiling

This core candidate does not establish:

- AOSS superiority;
- generalized correctness;
- independent validation;
- production safety/security;
- certification or compliance;
- High-Assurance authorization;
- scientific efficacy;
- commercial demand;
- product-market fit.

Repository-local exact-SHA distribution is the accepted v0 boundary. Package
publication and standalone extraction remain deferred. The bounded
same-owner portability result does not establish independent validation or
authorize execution.
