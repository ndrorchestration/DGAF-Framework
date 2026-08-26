# Publication Experiment Mapping: H1–H3

> **Control status:** PRE-AUTHORIZATION / N=0
> **Executable candidate:** `e6beeb66335e1b50a239697badab22dab50eb5ba`
> **Freeze:** NOT CREATED
> **Authorization:** NOT GRANTED

## Purpose

Map publication hypotheses H1–H3 to the apparatus, protocol, baselines, negative controls, endpoints, statistical analysis, reproducibility requirements, and authorization predicates required before confirmatory execution.

## Boundary

No pilot execution, unblinding, efficacy claim, or post-hoc protocol change is permitted before explicit authorization. Empirical N remains **0**.

## Apparatus identity

`e6beeb66335e1b50a239697badab22dab50eb5ba` remains the executable verification candidate. Documentation-only successors do not redefine the executable apparatus.

A future immutable freeze must bind the final executable SHA, tree identity, canonical protocol, artifact schema, analysis configuration, runner, environment fingerprint, deployment identity, and evidence registry.

## H1 — Primary DGAF contrast

- Treatment: `dgaf`
- Reference: `null`
- Primary endpoint: FFCR
- Unit of inference: root seed
- Estimand: mean paired seed-level `FFCR_dgaf - FFCR_null`
- Direction: higher FFCR favors treatment

The P7 statistical analysis is a two-sided 95% percentile paired bootstrap with 10,000 resamples, RNG seed `20260823`, and α=`0.05`. Directional support requires a positive estimate with an interval wholly above zero.

## H2 — Governance/control comparison

The preregistered comparison matrix includes `NULL`, `SIMPLE_AGENT`, `STATIC_RULES`, `DGAF`, and `DGAF_PDMAL`. Comparison controls require a frozen task corpus, identical prompts where applicable, matched model versions where applicable, matched or explicitly reported compute budget, paired seeds where semantically valid, and a fixed evaluator.

## H3 — Evidence-coupling / topology comparison

H3 remains comparative/exploratory until its exact endpoint and confirmatory status are explicitly frozen. Topology and interaction diagnostics must not silently become primary efficacy evidence.

## Negative controls

The preauthorization control surface includes:

1. **NC-01 Null decision** — no-op/random governance output; reported separately from efficacy.
2. **NC-02 Evidence-decoupled** — same nominal task input without the DGAF evidence-coupling path.
3. **NC-03 Governance-signal falsification** — synthetic/invalid governance signal; expected fail-closed.
4. **NC-04 Provenance falsification** — altered/mismatched provenance identity; expected fail-closed.
5. **NC-05 Semantic-boundary** — unsupported ontology/entity assertion; must not alter canonical semantic state.
6. **NC-06 Recovery-state** — invalid recovery transition; expected fail-closed.

Negative controls are diagnostic unless explicitly promoted into the frozen experimental design. They are analyzed separately from the primary efficacy estimate.

## Reproducibility requirements

The final freeze must capture:

- Git SHA and tree identity;
- protocol hash;
- artifact-schema hash;
- analysis hash;
- runner identity/hash;
- Python/Node/OS/runtime/dependency-lock versions;
- exact Vercel deployment ID and URL;
- workflow run IDs and evidence artifact IDs;
- durable-retention/retrieval hashes;
- blinding/custody control identifier.

## Authorization predicates

Before authorization, all of the following must be evidenced:

- canonical protocol frozen;
- canonical artifact schema frozen;
- P7 authority adoption and exact binding complete;
- P8 candidate verification complete;
- authenticated P2 runtime verification complete;
- P6a CORS verification complete against the same deployment identity;
- P4 blinding custody/unblinding procedure verified;
- baselines frozen;
- negative controls frozen;
- endpoints and statistical analysis plan frozen;
- environment fingerprint established;
- durable evidence custody verified;
- independent P9 verification complete;
- immutable freeze created and verified;
- explicit authorization decision recorded.

Only after these predicates are satisfied may empirical N transition from 0.

## Claim boundary

Pre-execution statements remain hypotheses/specifications. Post-execution claims remain bound to measured outcomes, uncertainty, tested scope, deviations, and the exact frozen apparatus. A result against one baseline does not establish general superiority over all governance approaches.
