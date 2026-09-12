# DGAF Discovery Harness v1

## Status

ENGINEERING DISCOVERY ONLY · NON-AUTHORIZING · SCIENTIFIC N=0 EFFECT

This harness is a second-order assurance layer. It searches for weaknesses in DGAF controls, weaknesses in the detectors that inspect those controls, and weaknesses shared by the discovery methods themselves.

It does not alter Track A or Mode T governance state, authorize collection, materialize empirical inputs, unblind results, promote evidence independence, or increment scientific N.

## Authority firewall

Every harness output must satisfy:

- repository mutation by an experiment: `false`;
- authorization effect: `false`;
- scientific state effect: `NONE`;
- scientific N increment: `0`;
- production execution: `false`;
- mutation scope: `EPHEMERAL_COPY_ONLY`.

Harness failure, timeout, missing evidence, malformed input, or unknown classification can never increase authority.

## v1 scope

The implementation provides a fail-closed output envelope, curated governance-semantic mutation operators, explicit legal/forbidden transition coverage metrics, pairwise control-interaction analysis, assumption-expiry modeling, a blind-spot ledger contract, executable metamorphic relation checks, bounded detector/property mutation campaigns, and candidate blind-spot retention for surviving detector mutants.

Critical mutant families begin with authorization promotion, evidence-independence promotion, predecessor/provenance removal, scientific-N increment, and fail-open decision promotion.

### Assumption validity and expiry

Assumptions are classified by evidence validity mode:

- `IMMUTABLE` — content-addressed or otherwise immutable evidence does not decay merely because time passes;
- `VERSION_BOUND` — revalidation is triggered by a relevant version change;
- `CONFIGURATION_BOUND` — revalidation is triggered by a relevant configuration change;
- `ENVIRONMENT_BOUND` — revalidation is triggered by a relevant environment change;
- `TEMPORAL` — a timezone-aware revalidation deadline is required.

Expiry is trigger-based first. The registry is seeded empty and carries `completeness_claim: false`; an empty registry therefore does not claim that no unregistered assumptions exist.

### Blind-spot ledger

A blind-spot record separates methods that discovered a finding from methods that missed it, binds reproduction evidence, may point to a candidate generated detector, and is always `authoritative_effect: NONE`.

The seed ledger is deliberately empty with `completeness_claim: false`. Findings may be marked only `CANDIDATE`, `REVIEWED`, or `REJECTED`; the ledger itself cannot promote a finding into governance truth.

Surviving detector mutants may be converted into candidate blind-spot records. The conversion records `detector-mutation` as the discovery method, the evaluated detector or property suite as the method that missed the mutant, binds reproduction evidence to the mutant identifier, and keeps the record at `CANDIDATE` with `authoritative_effect: NONE`. Killed mutants do not create blind-spot records.

### Metamorphic relations

The initial executable relations cover two failure classes that ordinary example-based testing can miss:

- changes outside governance semantics, such as presentation-only changes, must preserve protected authority fields;
- removing required predecessor/provenance evidence cannot leave a `PASS` decision intact.

Metamorphic failures are candidate engineering findings only. They do not themselves reject or authorize an experiment record unless an independent authoritative validator already defines that consequence.

### Detector and property mutation

Detector mutation evaluates intentionally weakened detector behavior against explicit property cases whose expected validity is specified independently of the mutant. The canonical detector must agree with every property case before a campaign is scored; disagreement fails closed instead of allowing a misleading mutation score.

A mutant is killed when at least one property case distinguishes the weakened detector from the stated property oracle. Surviving mutants are retained as evidence of an inadequate distinguishing corpus, not evidence that the detector is correct. Scores are reported both overall and by semantic family to reduce the value of a single gameable aggregate. Empty mutation campaigns are rejected rather than receiving a vacuous perfect score.

Detector mutation operates on in-memory behavior only. Campaign results are always `authoritative_effect: NONE`, `scientific_state_effect: NONE`, `scientific_n_increment: 0`, and `mutation_scope: EPHEMERAL_COPY_ONLY`.

## Recursive assurance roadmap

Later layers add a machine-readable metamorphic relation registry, stateful search, formal lifecycle models, bounded agent/API chaos, versioned external-framework crosswalks, and cross-method blind-spot synthesis across mutation, metamorphic, transition, interaction, and chaos detectors.

A discovery method may generate a candidate finding or test. It may never promote itself into authoritative governance truth.

## Research alignment

The design follows a measurement-oriented rather than certification-oriented interpretation of current AI TEVV work: assumptions and measurement objectives must be explicit, evidence validity can change with context, monitoring methods themselves can have blind spots, and machine-readable audit records improve reproducibility. External framework mappings remain informational and never imply compliance or certification.

## Verification boundary

Passing these tests demonstrates only that the harness kernel obeys its non-authorizing contract and that its basic analyzers behave as specified. It is not evidence of DGAF efficacy, experiment authorization, production validation, or scientific findings.
