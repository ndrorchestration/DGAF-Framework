# Brainstorm Artifact Recovery Adjudication — 2026-09-09

**Purpose:** follow-up to the three-batch historical brainstorm-corpus reconciliation. This record checks whether high-value historical concepts resolve to current implementation evidence, current scoped analogues, or unresolved artifact-discovery targets.

**Source boundary:** historical brainstorm/generated synthesis is discovery/provenance input only. Current GitHub source is implementation truth within repository scope.

**Scientific state effect:** NONE  
**Empirical authorization effect:** NONE  
**Canonical DGAF efficacy:** NOT_ESTABLISHED

## Current-main anchor

This recovery pass starts from post-#531 `main` at:

`f3e40527a32f2b9ea9efe625c47d14f95c33bcf9`

PR #531 incorporated the final three-batch vocabulary/evidence reconciliation after all exact-head checks passed.

## Recovery table

| Historical concept / target | Current finding | Evidence class | Disposition |
|---|---|---|---|
| NDR-78 — Axiomatic Authorization Gate | No current `NDR-78` implementation identifier was found. The narrower safety property already exists in `pptl/commit_gate.py`: consequential commit requests require explicit proposal + authorization before commit, duplicate authorization is denied, and committed requests cannot be replayed. `pptl/tests/test_v1_control_plane.py` exercises these fail-closed properties. | `IMPLEMENTED` / `VERIFIED` for `CommitGate`; `HISTORICAL` for the NDR-78 name | **MAP, DO NOT DUPLICATE.** Treat NDR-78 as historical lineage / closest analogue to the current CommitGate authorization barrier, not as a separate active gate. |
| NDR-69 — Master State Anchoring | No current `NDR-69` implementation identifier was found. Current implementation already provides canonical state serialization + SHA-256 state identity through `pptl/state_identity.py`; tests verify deterministic identity. Current governance/experiment docs separately bind candidate/control state to exact manifests, provenance anchors, and fail-closed authority. | `IMPLEMENTED` / `VERIFIED` for exact state identity; broader manifest/provenance anchoring is source-specific | **MAP, DO NOT DUPLICATE.** Preserve NDR-69 as lineage for exact-state/provenance anchoring. |
| NDR-68 — Gated Crystallization | No source implementation under the historical identifier was found. The general idea overlaps existing governed promotion/authorization/evidence-state controls, but no distinct calibrated `m > 0.98` mechanism was located. | `DEFINED` / `HISTORICAL`; threshold `UNSUPPORTED` | **NO NEW COMPONENT.** Reuse current gate/evidence-transition controls unless a distinct predicate and lifecycle are later implemented. |
| NDR-73 — Pillar-Driven Telemetry | No source implementation under the historical identifier was found. Historical source definitions conflict about pillar semantics. | `HISTORICAL` / `CONFLICT_PRESERVE` | **REQUIRES OWNING SOURCE** before any operational mapping. |
| NDR-82 — Proximity-Gated Luminance | No implementation was found in current repo or organization code search. Searches for `NDR-82`, `RK4-Lite`, GPGPU/proximity-luminance language produced no implementation evidence. | `HISTORICAL` / `HYPOTHESIS` | **KEEP AS VISUALIZATION CANDIDATE ONLY.** |
| Demicog Stress Suite | Current source search found `Demicog` only in a historical terminology-correction table mapping `Demicog → DemiJoule`; no stress-suite harness, 2,100-run telemetry, or reproducibility artifact was found. | `HISTORICAL`; stress-suite result claims `UNSUPPORTED` | **DO NOT TREAT AS RECOVERED HARNESS.** Continue only if an owning artifact is found outside the current repository. |
| A.P.O.G.E.E. v49.2 / `v49_master_manifest.json` | No current repository/organization source hit for the named master manifest or `v49.2 Master Build`. | `HISTORICAL` / `REQUIRES_OWNING_SOURCE` | Preserve lineage; do not reconstruct from generated descriptions. |
| `CITATION.cff` | A real current root `CITATION.cff` exists. It identifies DGAF as **Dynamic Governance Agentic Formation**, provides citation metadata, and explicitly says repository publication does not itself establish empirical validation, certification, or production readiness. | `IMPLEMENTED` citation metadata | **RECOVERED, SCOPED.** Citation metadata is real; legal priority, empirical validation, and certification claims remain outside its evidentiary scope. |
| Rose Gold Capture → Cluster → Synthesize → Critique → Decision | No distinct executable component recovered under this name. The sequence remains useful as a documentation/artifact-graduation workflow and overlaps current reconciliation/review practice. | `DEFINED` / pattern candidate | **PROCESS PATTERN, NOT MATURITY GATE.** |
| Hamiltonian cognitive coverage | No evidence found that Hamiltonian traversal is a current causal mechanism guaranteeing exhaustive cognition or role separation. | `HYPOTHESIS` | **TESTABLE ROUTING/EVALUATION HYPOTHESIS ONLY.** |

## Verified current analogues

### 1. Explicit consequential-action authorization

`pptl/commit_gate.py` implements a proposal/authorization/commit barrier:

- request identity and action fields are required;
- request IDs cannot be proposed twice;
- authorization requires both an authorizing identity and authorization reference;
- authorization cannot occur for an unknown proposal;
- reauthorization and replay are denied;
- commit fails closed if explicit authorization is absent.

This is a stronger current anchor than the generated NDR-78 label because it is inspectable code with tests. The historical identifier should therefore point to this implementation family rather than create a second gate.

### 2. Exact orchestration-state identity

`pptl/state_identity.py` canonicalizes state through stable JSON ordering and computes SHA-256 state IDs. `StateRegistry` records observed identities and supports exact cycle/state detection. Tests confirm that semantically identical dictionaries with different key ordering produce the same canonical form and state ID.

This supplies a concrete implementation component for the state-anchoring idea recovered under NDR-69, while experiment/candidate authority remains governed by the repository's dedicated control-state and manifest documents.

### 3. Citation metadata boundary

The current `CITATION.cff` is genuine source metadata. It is not proof of:

- patent rights or inventorship priority;
- empirical efficacy;
- certification;
- production readiness;
- institutional or regulatory compliance.

Its own abstract preserves that boundary.

## Negative findings preserved

The following searches produced no current implementation evidence and must remain negative findings rather than being reconstructed from generated prose:

- exact NDR-68 / NDR-69 / NDR-73 / NDR-78 / NDR-82 implementation identifiers;
- `v49_master_manifest.json`;
- `v49.2 Master Build`;
- `RK4-Lite`;
- GPGPU/proximity-luminance implementation matching the historical description;
- a Demicog Stress Suite harness or retained 2,100-run telemetry.

A negative search is not proof that an artifact never existed; it establishes only that it was not located in the currently searched GitHub sources.

## Architecture decision

Do **not** resurrect historical pattern identifiers as new runtime components merely because useful ideas survived corpus reconciliation.

Prefer:

`historical concept → current canonical mechanism/owner → exact implementation/evidence → remaining gap`

instead of:

`historical concept → new parallel subsystem`

This keeps the present architecture centered on DGAF governance/evidence authority, the existing PPTL/control-plane mechanisms, PDMAL's scoped empirical work, and the current provenance/control-state surfaces.

## Next evidence targets

1. Search non-GitHub connected sources for the specifically named historical A.P.O.G.E.E./v49.2 manifest or source bundle before declaring it lost.
2. Search saved files/Drive/Notion for any real Demicog harness, 2,100-run telemetry, result tables, or scripts.
3. If NDR-73 is retained, resolve its conflicting pillar definitions from an owning source before implementation.
4. If NDR-82 remains interesting, specify it from scratch as a visualization experiment with measurable inputs/outputs rather than inheriting historical implementation claims.
5. If Hamiltonian coverage is pursued, compare it prospectively against simpler routing baselines on pre-specified coverage, latency, cost, disagreement-detection, and failure-recovery metrics.

## Invariants

`documentation reconciliation ≠ scientific evidence`  
`current implementation analogue ≠ historical-name equivalence`  
`negative search ≠ proof of nonexistence`  
`CI success ≠ DGAF efficacy`  
`canonical_dgaf_efficacy = NOT_ESTABLISHED`
