# AOSS v0.6 Stage A — Observer and Measurement Boundary

**Controller:** #810  
**Status:** FROZEN PRE-DATA CONTRACT · NO OUTCOMES  
**Scientific effect:** NONE

This contract closes two apparatus-definition predicates without selecting any empirical result, freshness threshold, statistical method, or AOSS decision policy.

## Observer deployment boundary

The Stage-A observer is external, post-export, and read-only. It consumes only the frozen ACP provenance manifest exported by the unchanged target commit.

It may not:

- mutate the ACP process;
- call back into ACP;
- inject environment/configuration;
- influence scheduling or policy;
- patch ACP instrumentation for the study.

ACP-origin events are classified by the adapter as trust domain `SYSTEM`. That classification describes origin only. It does not imply validator or authority status.

Adapter-generated metadata belongs to the `OBSERVER` domain. Validator and authority evidence are absent in the frozen ACP source and therefore remain `UNMEASURED`.

## Extraction identity

Every consequential normalized field now has a versioned extraction-function identifier in:

`registry/aoss_v0_6_stage_a_observer_measurement_boundary_v1.json`

The contract distinguishes:

- exact direct copies;
- deterministic adapter-derived values;
- explicit absent-to-`UNMEASURED` mappings;
- exact list-index extraction;
- timezone-aware timestamp parsing with exact source-string preservation.

There are no floating numeric measurements in this adapter contract. The only numeric extracted field is the zero-based source-order index, which has zero tolerance.

Timestamp extraction tolerance is also exact: parsing validates that the source timestamp is timezone-aware and the adapter preserves the original source string. **This does not define freshness.** The acceptable age of an observation and clock-calibration semantics remain a separate unresolved predicate.

## Non-effects

Acceptance of this boundary does not:

- define or recover the missing AOSS decision policy;
- select a freshness threshold;
- define episode eligibility or repetitions;
- assign ground-truth outcome labels;
- choose a statistical estimator or multiplicity policy;
- authorize Stage-A outcome collection;
- establish external validation;
- increment scientific N.
