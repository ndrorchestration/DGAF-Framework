# DGAF/PDMAL Execution Readiness — Refined 2026-08-21

## Executive state

**Repository state:** PRE-FREEZE / BLOCKED
**Historical freeze:** `3510b86889cd341f7a7cf9ab684fd37b2fafd758` — historical / superseded for corrected pilot apparatus
**Current main:** resolve from GitHub `main` at verification time
**Corrected apparatus:** present on current mainline, candidate-scoped verification pending
**New freeze:** NOT CREATED
**Pilot authorization:** NOT GRANTED
**Empirical N:** 0

## Closure model

Engineering closure, scientific closure, and operational evidence proceed in parallel and converge into predicate evaluation. Predicate status is derived from underlying evidence and is not self-authorizing.

```text
Engineering ─┐
Scientific  ─┼─> P1–P8 evaluation ─> P9 independent verification
Operations  ─┘                              │
                                           v
                                      NEW FREEZE
                                           │
                                           v
                                  FREEZE VERIFICATION
                                           │
                                           v
                                      AUTHORIZATION
                                           │
                                           v
                                     50-SEED PILOT
```

## Canonical predicates

| ID | Predicate | Current state |
|---|---|---|
| P1 | Candidate integrity | PARTIAL |
| P2 | Execution contract | PARTIAL |
| P3 | Artifact contract | PARTIAL |
| P4 | Security / blinding integrity | PARTIAL |
| P5 | Provenance / reproducibility | PARTIAL |
| P6 | Durable evidence custody | OPEN |
| P7 | Scientific target specification | PARTIAL / contrast OPEN |
| P8 | Analysis lock | OPEN |
| P9 | Independent verification | NOT EXECUTED |

Experimental-design integrity is folded into P5 + P7. Authorization is a separate governance transition.

## Engineering closure completed in mainline

### Test contract

`test_execution_contract.py` no longer asserts that the executor is unimplemented. It preserves fail-closed mode/authorization testing and explicitly verifies the `ConsensusTask` executor path.

### Pilot artifact contract

`pilot_artifact_schema.py` is present on mainline. The runner uses the schema's `canonical_json_bytes()` for record hashing and calls `validate_artifact()` plus `verify_sidecar()` on each written seed artifact. This establishes runtime enforcement in addition to CI tests.

### Security workflow

The pre-authorization security workflow is present with explicit `permissions: contents: read` and includes adversarial controls, schema tests, execution-contract tests, and contract-mode non-empirical verification.

### Remaining engineering evidence

The implementation changes are present, but fresh CI and candidate-scoped artifact/smoke verification have not yet been established as VERIFIED evidence.

### Durable retention

Retention remains an open gate on current main. The policy is present, but an operational archive destination and actual write/retrieval/hash evidence are not yet established on the mainline candidate.

## Scientific closure

The construct is FFCR. The statistical unit is seed. The primary contrast remains OPEN. Candidate contrasts include `dgaf` vs `null`, historical topology comparisons under an explicitly defined current estimand, and other prespecified contrasts with explicit multiplicity treatment.

The historical PDMAL-vs-Ring contrast must not be silently inherited from a different protocol/endpoint framework.

The repository contains `docs/experiment/PDMAL_ANALYSIS_CONTROL_PLAN.md`, which records the analysis-lock requirements but does not select the scientific contrast.

## Provenance reconciliation

The latest recorded runtime-characterization reconciliation is:

- ZIP: `ba2d44016a9ef7f76546746bd03cd2964776e735ce4bbd5034d28f8cebee6f20`
- Inner artifact: `42da11122cf4bca517d93888c946d26b31a8ae6b304433e56ae9c2f4c155f6ea`

A fresh byte-level recomputation from the release asset should be performed before the final freeze packet is sealed.

## Topology provenance

`docs/experiment/PDMAL_TOPOLOGY_FINGERPRINT_MANIFEST.md` records current-source deterministic fingerprints. The final freeze packet must recompute them against the exact immutable candidate tree.

## State/provenance rules

- Historical evidence never silently transfers to a corrected apparatus.
- Mainline, historical freeze, deployment, and governance identities remain separately scoped.
- Status documents cannot create closure by assertion.
- A freeze is a new immutable state transition; it is not a repaired historical freeze.
- Merge is not freeze. Freeze is not authorization. Execution is not empirical validation.

## Anti-yellow-tape rule

A new blocking control is justified only when it addresses a concrete material failure mode or uncertainty that is not already covered and provides new protective or evidentiary information. Evidence should become stronger, not merely larger.

## Required next sequence

1. Run fresh CI on the corrected mainline candidate.
2. Execute candidate-scoped smoke and artifact validation checks.
3. Establish durable evidence custody and direct retrieval/hash verification.
4. Reconcile topology fingerprints and environment identity on the exact candidate.
5. Adjudicate the primary contrast and lock the analysis implementation/configuration.
6. Derive P1–P8 from candidate-scoped evidence.
7. Execute P9 independent verification.
8. Create a new freeze and independently verify that exact freeze.
9. Obtain explicit authorization.
10. Execute the 50-seed blinded pilot.

## Final epistemic boundary

**No empirical efficacy claim is established.** Historical acceptance/characterization evidence remains non-empirical. Pilot authorization remains NOT GRANTED. Empirical N remains 0.
