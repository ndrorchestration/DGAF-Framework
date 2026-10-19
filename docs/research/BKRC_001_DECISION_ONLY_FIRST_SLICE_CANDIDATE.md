# BKRC-001 — decision-only evidence-boundary first slice

Status: OPERATOR-LOCAL ENGINEERING CANDIDATE, NO SCIENTIFIC OR RUNTIME AUTHORITY.
Research protocol: [BKRC-001 candidate](https://app.notion.com/p/3fef5bad238b8125b897ff011009ed2f)
Canonical prospective comparative study: docs/qa/COMPARATIVE_GOVERNANCE_BENCHMARK_SPEC.md
Existing engineering controller: DGAF issue #1022; evaluation-integrity owner: issue #64.

## Scope

Four source-bound scenarios use the unchanged historical synthetic D model and
strong conventional C3 comparator: legitimate documentation action (GB-001),
disallowed target (GB-002), improper independent-status promotion (GB-003),
and a single-field positive control for GB-003 with claim status kept at
SAME_SYSTEM_NONINDEPENDENT.

The signed fixture and C3 rules source identities are retained in the report.
No baseline implementation, frozen input file or protected claim artifact is
modified. This adds a *classification and non-inference test* to the already
existing comparator results. It is not a new scientific dataset.

## Critical distinction

A model's ALLOW or DENY is *decision evidence*, not observed real-world
enforcement. Every output record declares dispatch/effect NOT_INSTRUMENTED,
enforcement receipt null, independent truth oracle NOT_ESTABLISHED and
non-dispatch not proven. Synthetic D and strong C3 decision parity weakens
any attribution of incremental decision value to DGAF on these cases.

A protected executor and its effect ledger are not connected by this code;
providing a forged synthetic "effect prevented" receipt would be misleading.
Future BKRC tests of concurrency, revocation, conflicting claim graphs,
lost acknowledgements or effect uncertainty require separate accepted owners
and evidence instruments.

## Reproduction

From an exact-source full-history checkout, Python 3.12 with the repository
hash-locked CI dependency set:

    python -m pytest tests/test_governance_benchmark_bkrc_first_slice.py -q
    python -m experiments.governance_benchmark.bkrc_first_slice --output /tmp/bkrc-first-slice.json
    sha256sum /tmp/bkrc-first-slice.json

The report records Git HEAD, SHA-256 of original fixtures, C3 rules source,
canonical rules representation and each exact case. Unit tests check no
mutation of the source fixtures, a one-field control difference, decision
parity, and that the synthetic outputs do not assert actual non-effects.

## Non-effects, methodological and authorization gates

This first slice is synthetic, deterministic and author-operated. It measures
neither real protected effect nor independent truth, false production blocking,
runtime costs, live network access nor valid outside-operator behavior.
The four decision observations do NOT increment scientific N. No live ACP
driver, credentials, provider, AOSS collector, public Tektite surface,
independent custodian or repository protected-main mutation is exercised.

Use a non-author review of the case/source identity, expected-output oracle,
trace reliability and assertion limits before any admission. Follow existing
DGAF #1022 and #64 controllers for next engineering measurements. Reconcile
with the canonical comparator and resource parity specification before
expansion; no new benchmark program or effect admission is created.

SCIENTIFIC_N_INCREMENT=0
INDEPENDENT_VALIDATION=NOT_ESTABLISHED
CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED
HIGH_ASSURANCE=NOT_AUTHORIZED
