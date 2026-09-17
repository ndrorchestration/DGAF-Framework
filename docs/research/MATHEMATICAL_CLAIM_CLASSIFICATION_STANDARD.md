# Mathematical Claim Classification Standard

> **Status:** ACTIVE RESEARCH/DOCUMENTATION METHOD / NON-AUTHORIZING  
> **Scientific-state effect:** NONE  
> **Established:** 2026-09-17

## Purpose

Mathematical elegance can generate useful hypotheses while also creating a risk of overclaiming. This standard requires mathematically framed statements to be classified according to what the evidence actually establishes.

It applies to DGAF/PDMAL research documentation and is recommended for related NDR projects when mathematical motifs, spectral structure, topology, harmonic language, phi-derived structure, dynamical analogies, or formal invariants are used.

## Classification set

### `ANALOGY`

A conceptual comparison used to reason or communicate.

Requirements:

- the mapped concepts are named;
- the document explicitly states that the systems are not claimed to obey the same equations/mechanism;
- no empirical or mechanistic conclusion is inferred from the analogy alone.

Example: describing correlated multi-agent reinforcement as “resonance” while clearly stating that the agent system has not been shown to obey a harmonic-oscillator model.

### `DESIGN_HEURISTIC`

A rule or architectural idea motivated by theory, prior work, analogy, engineering practice, or expected behavior, but not established as an empirical advantage in the target system.

Example: hiding peer outputs until each verifier completes an independent first pass to reduce anchoring/correlation risk.

### `MATHEMATICAL_PROPERTY`

A statement established for an exact mathematical object by proof, derivation, exhaustive computation, or validated numerical calculation appropriate to the claim.

Requirements:

- exact object identity/definition;
- exact quantity/definition;
- calculation/proof method;
- numerical tolerance where relevant;
- reproducible implementation or derivation when computational.

Example: an exact graph has a specified vertex connectivity under a declared graph definition.

**Boundary:** a graph property is not evidence that an agent system using that graph has superior empirical performance.

### `EMPIRICAL_HYPOTHESIS`

A falsifiable statement about observed behavior that has not yet met the evidence threshold for support.

Requirements:

- population/system scope;
- measurable outcome;
- comparison or falsification criterion;
- prospective protocol for confirmatory use.

Example: higher path redundancy reduces false-consensus persistence under controlled node failures.

### `EMPIRICALLY_SUPPORTED`

A scoped empirical statement supported by completed, admissible evidence under a declared method.

Requirements:

- exact experiment/data identity;
- endpoint/estimand;
- analysis identity;
- uncertainty/effect estimate where applicable;
- deviations and negative findings retained;
- verification class stated;
- scope limited to what the evidence supports.

`EMPIRICALLY_SUPPORTED` does not imply external replication or universal generalization.

## Optional evidence qualifiers

A classified claim MAY add qualifiers without replacing the primary class:

- `INTERNALLY_VERIFIED`
- `INDEPENDENTLY_VERIFIED`
- `REPLICATED_INTERNAL`
- `REPLICATED_EXTERNAL`
- `PROSPECTIVE`
- `EXPLORATORY`
- `HISTORICAL_EXACT_SCOPE`

A qualifier must be supported by an explicit evidence record. `INDEPENDENTLY_VERIFIED` must not be assigned to same-system developer self-verification.

## Promotion ladder

Typical promotion paths include:

```text
ANALOGY
  -> DESIGN_HEURISTIC
  -> EMPIRICAL_HYPOTHESIS
  -> EMPIRICALLY_SUPPORTED
```

or:

```text
mathematical statement
  -> MATHEMATICAL_PROPERTY
  -> EMPIRICAL_HYPOTHESIS about system consequences
  -> EMPIRICALLY_SUPPORTED consequence
```

A `MATHEMATICAL_PROPERTY` does not automatically promote to `EMPIRICALLY_SUPPORTED`; the two refer to different claim types.

## Required claim record

A material mathematical claim SHOULD record:

```text
claim_id
project
statement
classification
scope
object_or_system_identity
definition_or_equation
mechanism_claimed: true|false
prospective_or_posthoc
evidence_refs
counterfactual_or_baseline
verification_class
known_conflicts_or_negative_findings
promotion_requirement
last_reviewed
```

Unknown values remain `UNKNOWN`.

## Baseline requirement

A special mathematical structure must be tested against simpler or matched alternatives before being credited for empirical advantage.

Examples:

- phi-derived schedule vs matched non-phi schedules;
- harmonic/periodic schedule vs randomized or equal-cost schedules;
- spectral predictor vs simpler degree/connectivity/path-length predictors;
- special topology vs density/degree-matched graph baselines.

Without an appropriate baseline, the stronger mechanism or superiority claim remains unsupported.

## Post-hoc rule

A relationship noticed after observing outcomes is exploratory unless a valid pre-existing preregistration independently fixed the same hypothesis, direction, endpoint, and analysis.

Post-hoc mathematical pattern discovery must not be rewritten as prospective confirmation.

## Multiple-search rule

Searching many constants, ratios, graph statistics, transforms, frequencies, or geometric constructions increases the probability of apparently striking coincidences.

When many candidates were searched:

- record the search space when feasible;
- treat selected patterns as exploratory;
- use fresh/held-out data for confirmation;
- account for multiplicity where statistical inference is attempted.

## Mechanism rule

A numerical fit, correlation, visual resemblance, or matching ratio is not a mechanism.

A mechanism claim requires a model explaining how the proposed quantity enters the causal/operational process and a test capable of distinguishing that mechanism from plausible alternatives.

## Cross-project examples

| Statement | Required classification absent stronger evidence |
|---|---|
| “Agent errors can resonate.” | `ANALOGY` |
| “Independent first-pass verification may reduce correlated consensus.” | `DESIGN_HEURISTIC` or `EMPIRICAL_HYPOTHESIS`, depending on wording |
| “This exact graph has vertex connectivity 3.” | `MATHEMATICAL_PROPERTY` if exact-scope derivation/computation is verified |
| “PDMAL is more robust because its graph has high expansion.” | `EMPIRICAL_HYPOTHESIS`; the causal wording is unsupported until tested |
| “FFT is appropriate for decomposing an ASIS acoustic signal into frequency components.” | `DESIGN_HEURISTIC` grounded in signal-processing mathematics; measured benefit still empirical |
| “A phi-derived trigger improves orchestration stability.” | `EMPIRICAL_HYPOTHESIS` until a prospective matched-baseline test supports it |
| “A 32-pass recurrence is evidence of a harmonic mechanism.” | `ANALOGY` or unsupported mechanism claim unless a dynamical model and test establish more |

## Prohibited inference shortcuts

Do not infer:

```text
beautiful mathematics -> correct mechanism
mathematical property -> empirical efficacy
agent agreement -> independent verification
implementation -> validated scientific result
external literature -> target-system result
correlation -> causation
post-hoc fit -> prospective confirmation
```

## Negative findings

Negative or null findings remain part of the claim record. They must not be deleted because a later alternative formulation is more appealing.

A disproven empirical hypothesis may remain historically useful, but it must be labeled accordingly and cannot silently revert to `DESIGN_HEURISTIC` as though the test never occurred.

## Current DGAF/PDMAL boundary

This classification method does not alter any current gate or scientific state. In particular, it does not authorize Track A Epoch 002 materialization or primary analysis, increment scientific N, establish canonical DGAF efficacy, or establish independent validation.

## Relationship to Structural Epistemics

This standard governs claim language for `STRUCTURAL_EPISTEMICS_RESEARCH_PROGRAM.md` and its linked threat-model, topology-predictor, and ablation work.
