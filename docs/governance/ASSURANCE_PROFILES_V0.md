# Assurance Profiles v0 — extraction boundary

Status: **generic core candidate / bounded same-owner API/conformance portability evidenced at pinned revisions / non-authorizing / distribution not established**

Controller: #1242.

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

Exact tested identities:

- upstream core: DGAF PR #1244 at
  `8cfea9a073476eae1f4eb964ba9b9c0df704f9b5`;
- consumer: [ai-prompt-systems-portfolio PR #13](https://github.com/ndrorchestration/ai-prompt-systems-portfolio/pull/13)
  at `97e2102a0c0c15f11979f60d4f22fddc7f781dd1`;
- [portability probe run 36940089142](https://github.com/ndrorchestration/ai-prompt-systems-portfolio/actions/runs/36940089142):
  completed/success;
- consumer Common Evaluation Object Model run `36940088848` and Public
  portfolio integrity run `36940088847`: completed/success.

The consumer uses its real prompt/evaluation mapping and fetches the upstream
core from the immutable source SHA rather than vendoring a separate copy.
The probe covers direct, derived, and explicitly unmeasured fields; exact
source binding; replay/integrity; missing-evidence rejection; blocked
readiness; and positive review that remains non-authorizing.

These results remain bound to the listed revisions. Refreshing this
candidate onto current main does not transfer historical CI or consumer
results to the new head. A refreshed consumer pin requires its own exact-head
probe; source equivalence alone is not a fresh execution result.

## Next integration decision

Choose the smallest distribution boundary supported by consumer needs:

- keep the module internal to DGAF;
- distribute the schema/spec with a reference library;
- introduce an isolated Python package only if installation needs justify it.

No packaging or distribution was established by this tranche. Do not create
a separate repository or service merely because bounded portability passed.

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

Packaging/distribution remains deferred until the integration decision is
explicitly reviewed. The bounded historical portability result does not
establish independent validation or authorize execution.
