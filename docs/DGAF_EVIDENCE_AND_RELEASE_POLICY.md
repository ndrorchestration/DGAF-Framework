# DGAF Evidence and Release Policy

## Scope

DGAF is the canonical governance/evaluation vocabulary and implementation track for Dynamic Governance Agentic Formation. It contains artifacts at different maturity levels; repository-level presence does not imply repository-level validation.

## Evidence progression

`DEFINED → IMPLEMENTED → COMPUTED → TESTED → EVALUATED → REPRODUCED`

Governance effectiveness claims require evaluation evidence appropriate to the specific control or gate. A policy document establishes intended behavior; it does not demonstrate that agents comply with the policy under adversarial or operational conditions.

## Governance claim gates

For a claim such as "prevents," "detects," "enforces," "stabilizes," or "improves," the evidence should identify:

1. the precise behavior being claimed;
2. baseline/control condition;
3. threat or failure model where applicable;
4. measurement metric and denominator;
5. test/evaluation procedure;
6. results and uncertainty/limitations;
7. reproducible artifact or run identifier.

## Cross-project boundaries

DGAF may provide governance specifications or evaluation mechanisms to other repositories. Such integration does not establish the effectiveness of those mechanisms in the receiving repository unless the integration itself is tested and evaluated.

PDMAL, AHG, ACP, Driftwatch, Acoustic-Mesh, and Phi-Calculus remain separate evidence tracks.

## Versioning

Use software/research versions to describe artifact evolution. Version numbers do not indicate governance effectiveness, security certification, mathematical validity, or production readiness.

## Historical claims

Historical benchmarks and attestations remain preserved as provenance when useful, but must be labeled as historical unless reproduced under a documented current procedure.
