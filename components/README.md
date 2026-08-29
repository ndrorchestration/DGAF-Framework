# Components — Runtime Index

This directory contains implementation components used by DGAF experiments and governance tooling. A component's presence in the repository establishes that an implementation artifact exists; capability, production readiness, and efficacy depend on evidence appropriate to the specific claim.

## Components

| Component | Path | Purpose |
|---|---|---|
| KAPPA Dynamic Confidence Router | `KAPPA/dynamic_weight_router.py` | Confidence-gated routing and category-sensitive weight selection |
| KAPPA Calibration | `KAPPA/calibration_v3_6.json` | Project threshold configuration |
| KAPPA Component Card | `KAPPA/DGAF_GATE_KAPPA_v3_5_component_card.json` | Component metadata and registry information |
| Evaluate Router | `evaluate_router.py` | Batch pipeline composition |
| Evaluate Router v1.1 | `evaluate_router_v1_1.py` | Extended routing hooks and per-record audit support |
| Normative Constraint | `normative_constraint.py` | Deontic and epistemic constraint implementation |

## Using the components

Read the implementation and its tests together. Component-level results should not be generalized into repository-wide validation or experimental evidence.

For example, the normative constraint module can be imported directly by an evaluation pipeline:

```python
from components.normative_constraint import run_normative_pass

constrained = run_normative_pass(batch)
```

The applicable input/output contract is defined by the implementation and its associated tests and specifications.

## Evidence and historical records

The repository retains historical Apogee attestation artifacts and project-local quality records in `docs/qa/`. Those records document the procedures and artifacts to which they apply; they are not independent certifications and should not be read as current verification of every component.

Canonical promotion and governance requirements are defined in the relevant current specifications. See [`README.technical.md`](../README.technical.md), the pattern registry, and [`docs/CURRENT_STATE.md`](../docs/CURRENT_STATE.md) for project-level navigation.

## Status conventions

When reading older component documentation, distinguish current implementation from historical evaluation records. See [`docs/governance/LEGACY_DOCUMENTATION_STATUS_POLICY.md`](../docs/governance/LEGACY_DOCUMENTATION_STATUS_POLICY.md) for the repository policy on retained historical material.
