# PDMAL Mathematical Correction — 2026-08-15

> **Status:** CURRENT CORRECTION RECORD
> **Scope:** Evidence correction for the PDMAL lattice/topology work.
> **Authority boundary:** This document records corrected computations and evidence classification. It does not claim empirical superiority, convergence proof, or production validity.

## Corrections

### Plastic constant
The plastic constant used in the affected lattice analysis is:

`1.3247179572447454`

A prior value of approximately `1.7747` was incorrect and must not be retained as the plastic constant.

### Dodecahedral graph Cheeger constant
For the dodecahedral graph used by the PDMAL topology, the corrected Cheeger constant is:

`0.6`

A prior value of `0.89` was incorrect.

## Forman-Ricci curvature

The unweighted Forman-Ricci calculation on the current dodecahedral topology is computationally valid, but every edge evaluates to curvature `-2`. Because the result is constant across the topology, it is not currently a useful discriminating audit signal.

Therefore:

- the computation may be retained as a reproducibility check;
- it must not be presented as evidence of useful curvature-based auditing;
- a weighted Forman-Ricci treatment remains an open research item;
- any weighted formulation must first define the edge-weight semantics and calibration procedure.

## PDMAL interpretation boundary

The current evidence supports the following mapping:

- dodecahedral graph → PDMAL core topology;
- three colocated services/agents per vertex → 60-service interpretation;
- `φ` → convergence target only where a project-local specification explicitly defines it as such;
- corrected plastic constant → contextual value for the specified evaluation methods;
- `ContractionMonitor` → empirical runtime proxy, not proof of contraction;
- Forman-Ricci → open research signal until weighted edges are defined and shown to provide useful discrimination.

Topology, computation, and empirical performance remain separate evidence classes.

## `D_a` admission invariant

The `D_a` admission invariant belongs conceptually to the DGAF Quintet's calibration discipline. It should not be represented as an arbitrary universal hard-coded threshold unless a calibration artifact establishes that threshold for a defined operating regime.

## Evidence rule

A mathematically correct computation is not automatically a useful engineering signal. Each metric must be evaluated on two separate questions:

1. **Is the calculation correct?**
2. **Does the resulting quantity provide the claimed engineering discrimination or control value?**

The current Forman-Ricci result demonstrates why those questions must remain separate.

## Supersession

`docs/formalism/PDMAL_MATH_VERIFIED_v1.md` is retained for provenance but is superseded as a current mathematical authority by this correction record. Any portfolio, governance, or cross-reference document using the older authority label must be updated to point to this correction.

## Open validation gates

- empirical PDMAL comparative validation;
- real-trace calibration of `D_a`;
- definition and validation of weighted Forman-Ricci edge weights;
- reproducible evaluation of whether weighted curvature adds useful signal;
- any stronger convergence, robustness, superiority, or production claim requiring independent evidence.
