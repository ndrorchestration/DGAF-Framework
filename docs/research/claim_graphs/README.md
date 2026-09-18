# Structural Epistemics Claim Graph Records

This directory is the canonical repository intake surface for machine-readable
Structural Epistemics claim/evidence graph records.

Every `.json` file placed here is validated by
`tests/test_structural_epistemics_claim_graph_registry.py` using:

- `docs/research/STRUCTURAL_EPISTEMICS_CLAIM_RECORD_SCHEMA.json`;
- `docs/research/STRUCTURAL_EPISTEMICS_EVIDENCE_GRAPH_SCHEMA.json`;
- `scripts/validate_structural_epistemics_claim_graph.py`.

The validator is deliberately structural and fail-closed. It checks machine-
decidable epistemic invariants such as reference integrity, typed
support/contradiction relations, explicit dependence when evidence shares roots,
retraction/supersession consistency, stale-support handling, causal-claim
discipline, and triggered defeaters.

A passing record does **not** establish truth, independence, empirical efficacy,
authorization, execution, or scientific state. It establishes only that the
record satisfies the declared machine-readable Structural Epistemics contract.

Reference/adversarial test material belongs under
`docs/research/fixtures/`, not in this directory.
