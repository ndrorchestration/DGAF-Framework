# DGAF/PDMAL Execution Readiness — Refined 2026-08-21

## Executive state

**Repository state:** PRE-FREEZE / BLOCKED
**Historical freeze:** `3510b86889cd341f7a7cf9ab684fd37b2fafd758` — historical / superseded for corrected pilot apparatus
**Current main at this synthesis:** `5efd1dc52e5f986baa966cfb62e5941ad7620a39`
**Corrected candidate:** PR #77 lineage; candidate must be refreshed against current main before verification
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

## Engineering closure

### Test contract

`test_execution_contract.py` no longer asserts that the executor is unimplemented. It now preserves fail-closed mode/authorization testing and explicitly identifies the `ConsensusTask` executor path.

### Pilot artifact contract

PR #77 adds `pilot_artifact_schema.py`. The corrected runner now uses the schema module's `canonical_json_bytes()` for record hashing and calls `validate_artifact()` plus `verify_sidecar()` on each written seed artifact. This establishes runtime enforcement in addition to CI tests.

The remaining candidate-level verification is to run the full test suite against the refreshed candidate.

### Security workflow

The PR #77 pre-authorization workflow now declares `permissions: contents: read`, addressing the GitHub Advanced Security finding that the workflow lacked an explicit permissions block.

### Durable retention

Retention remains an open gate on current main. The repository currently has the retention policy but does not have a committed/operational archive destination proven by an actual write/retrieval/hash cycle. A previously observed local implementation is not treated as repository evidence until committed and independently verified.

## Scientific closure

The construct is FFCR. The statistical unit is seed. The primary contrast remains OPEN. Candidate contrasts include `dgaf` vs `null`, historical topology comparisons under an explicitly defined current estimand, and other prespecified contrasts with explicit multiplicity treatment.

The historical PDMAL-vs-Ring contrast must not be silently inherited from a different protocol/end-point framework.

The repository now contains `docs/experiment/PDMAL_ANALYSIS_CONTROL_PLAN.md`, which records the required analysis-lock fields but does not select the scientific contrast.

## Provenance reconciliation

The repository previously contained conflicting recorded SHA-256 values for the runtime-characterization inner artifact. The latest status reconciliation records:

- ZIP: `ba2d44016a9ef7f76546746bd03cd2964776e735ce4bbd5034d28f8cebee6f20`
- Inner artifact: `42da11122cf4bca517d93888c946d26b31a8ae6b304433e56ae9c2f4c155f6ea`

These values are the latest recorded reconciliation values, but a byte-level recomputation from the release asset should be performed when the asset is available before the final freeze packet is sealed.

## Topology provenance

The repository now contains a current-source fingerprint manifest derived from the committed `seeds.py` (`pdmal-v1` ASCII seed derivation) and the current topology generators. The manifest is candidate-source provenance, not pilot evidence, and must be recomputed against the exact future freeze tree.

## State/provenance rules

- Historical evidence never silently transfers to a corrected apparatus.
- `main`, PR candidate, historical freeze, deployment, and governance identities remain separately scoped.
- Status documents cannot create closure by assertion.
- A candidate must be refreshed against current main before fresh verification.
- A freeze is a new immutable state transition; it is not a repaired historical freeze.
- Merge is not freeze. Freeze is not authorization. Execution is not empirical validation.

## Anti-yellow-tape rule

A new blocking control is justified only when it addresses a concrete material failure mode or uncertainty that is not already covered and provides new protective or evidentiary information. Evidence should become stronger, not merely larger.

## Required next sequence

1. Refresh/rebase PR #77 against the current mainline.
2. Run fresh candidate CI and contract/security/schema checks.
3. Verify the runtime artifact serializer/validator path on the refreshed candidate.
4. Establish durable evidence custody and direct retrieval/hash verification.
5. Reconcile candidate topology fingerprints and environment identity.
6. Adjudicate the primary contrast and lock the analysis implementation/configuration.
7. Derive P1–P8 from candidate-scoped evidence.
8. Execute P9 independent verification.
9. Create a new freeze and independently verify that exact freeze.
10. Obtain explicit authorization.
11. Execute the 50-seed blinded pilot.

## Final epistemic boundary

**No empirical efficacy claim is established.** Historical acceptance/characterization evidence remains non-empirical. Pilot authorization remains NOT GRANTED. Empirical N remains 0.
