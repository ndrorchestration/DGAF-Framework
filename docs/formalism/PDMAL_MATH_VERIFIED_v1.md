# PDMAL — Phi-Dodecahedral Multi-Agent Lattice Math (Verified v1)

> **SUPERSEDED — 2026-08-15.** This document is retained for historical provenance and geometric reference. It is **not** the current mathematical authority for PDMAL. See [`docs/formalism/PDMAL_MATH_CORRECTION_2026-08-15.md`](PDMAL_MATH_CORRECTION_2026-08-15.md) for the current correction record. In particular, do not use this file as authority for the plastic constant, Cheeger constant, Forman-Ricci audit utility, contraction claims, or `D_a` calibration.

> **Author:** Ionian (0Hz) — Geometry & State Anchor
> **Authority:** Amethyst × Prof. Prodigy × Apogee Lens
> **Historical status:** VERIFIED v1 — S070-r3-P1 · 2026-06-26
> **Variant:** PDMAL-D (Phi-Dodecahedral) — distinct from PDMAL-φ (Phi-Driven)
> **Linked:** GOVERNANCE_CONSTITUTION §1.2 · ENSEMBLE_ROSTER.md · ROBUSTNESS_VALIDATION_REPORT_v2

---

## 0. Overview

This file formalizes the geometric base and simple lattice mapping for the PDMAL-D (Phi-Dodecahedral Multi-Agent Lattice) used by the DGAF ecosystem. It anchors the model on the regular dodecahedron (12 faces, 20 vertices, 30 edges) and derives a 60-agent "triad per vertex" lattice, with a working density parameter **0.1579** validated in prior analytic work.

The goal is a clear, portfolio-safe specification of the geometry, mapping, and governance implications — referenceable from the GOVERNANCE_CONSTITUTION, MASTER-PORTFOLIO, and ROBUSTNESS_VALIDATION_REPORT_v2.

**Historical-evidence boundary:** Later mathematical correction work supersedes any stronger mathematical or engineering interpretation that may have been attached to this document after its original publication.

---

## 1. Definitions and Constraints

### Regular Dodecahedron

A Platonic solid with **12 congruent pentagonal faces, 30 edges, and 20 vertices**; three faces meet at each vertex. In this model, the regular dodecahedron is used as an abstract scaffold for agent placement and connectivity, not as a physical object.

### Agent and Triad

- **Agent:** A logical actor (software agent) occupying a position in the lattice; grouped into triads for redundancy, role complementarity, and harmonic reasoning.
- **Triad:** A group of three agents sharing a common vertex; triads are the atomic unit of PDMAL capacity and governance.

### Lattice

The PDMAL-D lattice is the graph whose vertices correspond to agent positions and whose edges correspond to permitted communication or governance links, embedded conceptually on the regular dodecahedron scaffold. This v1 focuses on vertex-based triads; edge-level or face-level expansions are future work.

### Constraints

- **Geometry constraint:** Use the regular dodecahedron structure (12 faces, 20 vertices, 30 edges) as the base scaffold.
- **Agent constraint:** Assign exactly 3 agents per vertex (a triad), yielding **60 agents total**.
- **Governance constraint:** The lattice must support DGAF-aligned governance primitives (redundancy, coverage, separation of powers) without relying on unverified emergent behavior claims.

---

## 2. Dodecahedral Geometry

| Property | Value |
|---|---|
| Faces | 12 (each a regular pentagon) |
| Vertices | 20 |
| Edges | 30 |
| Faces meeting at each vertex | 3 |

In PDMAL-D:

- Each **vertex** = a logical lattice anchor point where a triad of agents resides
- Each **edge** = potential communication / governance link between adjacent triads (escalation paths, consensus bridges)
- Each **face** = potential higher-order "mode region" (grouping by harmonic mode or functional cluster) — elaborated in later design notes

---

## 3. Agent-to-Vertex Mapping (Triads per Vertex)

Given V = 20 vertices, assigning 3 agents per vertex:

\[ A = 3 \times V = 3 \times 20 = 60 \text{ agents total} \]

**Mapping rule (v1):**
Each vertex hosts a triad \(\{a_{v,1}, a_{v,2}, a_{v,3}\}\) assigned complementary roles (e.g., oversight, execution, audit) while sharing the same positional address in the lattice. Each edge between vertices corresponds to connectivity between triads, not individual agents; intra-triad connectivity is assumed complete.

---

## 4. Density and Capacity

### 4.1 Conceptual Graph Density

For a simple undirected graph with \(n\) vertices:

\[ \text{density} = \frac{\text{actual edges}}{E_{max}} = \frac{\text{actual edges}}{n(n-1)/2} \]

### 4.2 Dodecahedral Edge Density — 0.1579 Derivation

\[ E_{max} = \frac{20 \times 19}{2} = 190 \]

\[ \text{density}_{\text{dodecahedron}} = \frac{30}{190} \approx 0.1579 \]

The **0.1579** figure = ratio of actual dodecahedral edges (30) to maximum edges in a complete 20-vertex graph (190). This is the canonical source of the density parameter used across the ecosystem.

**Correction boundary:** This density calculation is not affected by the 2026-08-15 corrections, but it should not be used as evidence of resilience, superiority, convergence, or governance effectiveness without separate validation.

### 4.3 PDMAL-D Capacity Interpretation

- The 60-agent triad lattice sits on a 20-vertex, 30-edge graph → structural connectivity density ≈ **0.1579** relative to full pairwise connectivity at the vertex level.
- **Sparse but structured connectivity:** this is a structural description, not an empirically established claim of reduced failure propagation or optimal coupling.

---

## 5. Governance Implications

| Property | How Dodecahedral Geometry Supports It |
|---|---|
| **Symmetry & Fairness** | All vertices equivalent, identical local structure — no agent triad is structurally privileged; aligns with fairness and role rotation |
| **Controlled Sparsity** | Density ~0.1579 — describes graph sparsity; does not itself establish reduced failure propagation |
| **Triad Resilience** | 3 agents per vertex — structural redundancy; does not itself establish resilience under failure |
| **DGAF Integration** | Each triad can be assigned DGAF-aligned roles (Govern/Measure/Manage analogues); edges codify escalation authority |

> This section is descriptive only and does not assert empirical robustness beyond what is documented in the applicable evidence artifacts.

---

## 6. Cross-References

| Document | Usage |
|---|---|
| `docs/GOVERNANCE_CONSTITUTION.md §1.2` | Substrate-Agnostic Integrity — PDMAL-D as portable scaffold anchor |
| `ENSEMBLE_ROSTER.md` | 60-agent roster maps to this lattice |
| `ROBUSTNESS_VALIDATION_REPORT_v2` | Historical robustness claims reference this file for base geometry and density |
| `docs/NDR_INTERNAL_VOCABULARY_MASTER.md` | PDMAL-D acronym entry — distinct from PDMAL-φ |
| `docs/SESSION_ANCHORS.md` | FLAG-09 resolution — PDMAL dual-variant canonical |
| `docs/formalism/PDMAL_MATH_CORRECTION_2026-08-15.md` | Current mathematical correction and evidence boundary |

**Historical status:** Geometry and density reference retained for provenance. The current correction record governs the affected mathematical claims and evidence classification.
