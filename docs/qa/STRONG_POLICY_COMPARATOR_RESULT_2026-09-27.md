# Strong Policy Comparator — Fixed-Fixture Falsification Result

> **Evidence class:** SYNTHETIC FALSIFICATION ENGINEERING EVIDENCE  
> **Comparator:** C3_STRONG_POLICY_AS_CODE_V1  
> **Scope:** Current 13 fixed governance fixtures only  
> **Scientific effect:** NONE

## Question

Does the current fixed benchmark still show a unique DGAF decision advantage when
a conventional policy-as-code comparator is allowed the same declared action,
delegation, claim, provenance, and composition inputs wherever those rules are
reasonably expressible as ordinary policy?

## Frozen comparator

The comparator rules are machine-readable in
`experiments/governance_benchmark/strong_policy_rules_v1.json`.

The ruleset is frozen before result inspection and identified by its canonical
SHA-256. It contains 12 explicit rule clauses spanning:

- action authorization, tool, and target checks;
- delegated requester, replay, intent, attestation, and non-widening scope;
- claim evidence presence/freshness and verification class;
- flow provenance and protected-egress composition authorization.

## Result

On the current 13 fixed fixtures:

| Measure | C3 strong policy | DGAF |
|---|---:|---:|
| Task-correct decisions | 13/13 | 13/13 |
| False blocks | 0 | 0 |
| Decision parity | 13/13 | — |

Observed falsification outcome:

`PARITY_ON_CURRENT_FIXED_FIXTURES`

This means the current fixed fixtures do **not** demonstrate unique DGAF
protection once the conventional comparator is given equivalent expressible
rules over the same declared inputs.

## What this weakens

The result weakens any interpretation that the existing fixed-fixture advantage
over C1/C2, by itself, demonstrates that DGAF's protection cannot be reproduced
by a sufficiently strong conventional policy engine.

## What this does not establish

Parity does not establish that:

- the architectures are equivalent;
- configuration or maintenance burden is equal;
- policy composition remains equally safe at larger scale;
- recovery, provenance custody, epistemic state transitions, or operator
  oversight are equivalent;
- either system is production-safe;
- DGAF efficacy is established;
- DGAF is or is not state of the art.

## Next falsification target

The next useful comparison should move beyond fixed decision parity and measure
where architectural differences can actually appear:

1. policy/configuration growth as cases and authority domains scale;
2. update burden when claim/evidence semantics change;
3. cross-workflow composition and authority laundering;
4. stale/conflicting evidence and UNDETERMINED handling;
5. recovery/reconciliation after partial execution;
6. operator intervention burden.

Parity remains an acceptable result at every stage.

## Claim ceiling

Unchanged:

- `SCIENTIFIC_N_INCREMENT=0`
- `INDEPENDENT_VALIDATION=NOT_ESTABLISHED`
- `CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED`
- `STATE_OF_THE_ART=NOT_ESTABLISHED`
- `HIGH_ASSURANCE=NOT_AUTHORIZED`
