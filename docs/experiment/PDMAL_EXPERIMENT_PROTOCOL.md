# PDMAL Experiment Protocol

## Status

**PRE-FREEZE / NO DATA COLLECTION AUTHORIZED**

This document is the consolidated control document for the planned PDMAL empirical evaluation. It is intentionally **not frozen** until the listed protocol fields are reviewed, explicitly resolved, and committed as the authoritative experimental contract.

No pilot or final experimental seed may be generated while this document remains in `PRE-FREEZE` status.

## Evidence boundary

Passing software verification, instrumentation verification, deployment verification, and P6a CORS verification establish that the relevant software/evidence machinery operates under the tested conditions. They do **not** establish PDMAL efficacy or real-world benefit.

The empirical experiment is a separate evidence track.

## Transition rule

The experimental phase may begin only after all of the following are true:

1. PR #65 is merged or an equivalent approved experimental commit is established.
2. This protocol is explicitly frozen with a commit SHA and freeze timestamp.
3. The topology set and baseline matrix are frozen.
4. The primary endpoint and secondary endpoints are frozen.
5. Failure, recovery, and rerouting semantics are frozen.
6. RNG/seed generation and stream separation rules are frozen.
7. Trial ordering is frozen.
8. Exclusion and stopping rules are frozen.
9. The blinding mechanism is confirmed operational without exposing the secret.
10. The unblinding procedure is frozen.
11. The statistical analysis plan is frozen.
12. Pilot execution authorization is recorded in the evidence log.

## Protocol fields requiring freeze

| Field | Pre-freeze status |
|---|---|
| Topology set | Review/freeze required |
| Baseline matrix | Review/freeze required |
| Primary endpoint | Review/freeze required |
| Secondary endpoints | Review/freeze required |
| Failure model | Review/freeze required |
| Recovery/rerouting semantics | Review/freeze required |
| RNG/seed generation | Review/freeze required |
| RNG stream separation | Review/freeze required |
| Trial ordering | Review/freeze required |
| Exclusion rules | Review/freeze required |
| Stopping rules | Review/freeze required |
| Blinding mechanism | Confirm before freeze |
| Unblinding procedure | Review/freeze required |
| Statistical analysis plan | Review/freeze required |
| Pilot acceptance criteria | Review/freeze required |
| Final sample-size rule | Review/freeze required |

## Planned pilot

The first empirical event is a **50-seed blinded pilot**.

The pilot is a feasibility/QC stage and is not itself a claim of efficacy.

Pilot checks include:

- execution completeness;
- missing and invalid trial rate;
- runtime distribution;
- outcome variance;
- endpoint stability;
- reproducibility;
- artifact/provenance integrity;
- protocol-compliance failures.

Pilot observations must not be used to retroactively alter the primary endpoint, exclusion rules, or stopping criteria.

## Final experiment

A final controlled experiment follows the pilot only after the pilot QC decision and the predetermined sample-size rule are satisfied.

Before unblinding:

1. raw observations are frozen;
2. preprocessing rules are frozen;
3. exclusions are frozen and recorded;
4. the analysis dataset is retained with provenance/integrity metadata;
5. unblinding authorization is recorded.

## Planned comparative matrix

The working baseline matrix is:

1. Null / no-op control
2. Simple agent/control topology
3. Static rules/control
4. DGAF
5. DGAF + PDMAL

The final matrix must be explicitly frozen before data collection. Any deviation requires documented protocol amendment rather than silent post-hoc substitution.

## Analysis requirements

The analysis must report, at minimum:

- sample size;
- primary endpoint result;
- effect size;
- uncertainty/confidence interval as appropriate;
- variance;
- missingness/failure rate;
- runtime cost;
- baseline comparisons;
- protocol deviations;
- limitations.

The analysis must distinguish implementation behavior from empirical efficacy and must not promote unsupported causal or generalization claims.

## Blinding controls

`PDMAL_BLINDING_KEY` is an operational secret used by the instrumentation layer. It must never be committed, printed, or included in retained artifacts.

Blinded topology labels must remain blinded throughout collection and through the pre-unblinding dataset freeze.

Unblinding must occur only after the collection dataset and preprocessing/exclusion decisions are frozen.

## RNG controls

The protocol must explicitly separate:

- seed generation;
- trial/failure sampling;
- topology construction where randomness is used;
- trial ordering/randomization;
- any analysis resampling or bootstrap streams.

Exact RNG libraries, algorithms, seeds/seed lists, and stream derivation rules must be frozen before pilot execution.

## Evidence classification

The experiment may support increasingly strong evidence only to the extent justified by the retained data:

`VERIFIED` → `VALIDATED` → `EMPIRICALLY SUPPORTED`

These classes are not interchangeable.

A passing pilot or final experiment does not automatically establish broader real-world effectiveness.

## Freeze record

This section is intentionally blank until the protocol is reviewed and frozen.

```text
Protocol status:       PRE-FREEZE
Freeze commit SHA:     NOT YET ASSIGNED
Freeze timestamp:      NOT YET ASSIGNED
Pilot authorization:   NOT YET GRANTED
```

## Change control

Any change after freeze requires:

1. a new protocol version;
2. explicit description of the change;
3. reason for the change;
4. determination of whether previously collected data remain valid;
5. a new commit SHA;
6. updated evidence/provenance documentation.
