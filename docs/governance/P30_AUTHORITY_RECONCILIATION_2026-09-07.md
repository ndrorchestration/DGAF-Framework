# P-30 Authority Reconciliation — 2026-09-07

## Status

`EVIDENCE_REVIEW_COMPLETE / SEPARATION_RECOMMENDED / CANONICAL_RUNTIME_REBINDING_NOT_YET_EXECUTED / NEW_CANONICAL_EMPIRICAL_EPOCH_PROHIBITED`

This record addresses GitHub issue #374 after Solo P-30 Explicit Variant Epoch 003. It is non-empirical and does not alter the retained results of any prior epoch.

## Question

Which in-repository semantic lineage is authoritative for **P-30 — Apogee-Attestation-Gate**, and what follows for the historical scalar-confidence `ApogeeReviewer` mechanism used by the restored PDMAL experimental path?

## Source authority matrix

| Source | Recorded lineage | Input | Threshold / decision semantics | Purpose | Authority signal |
|---|---|---|---|---|---|
| `docs/patterns/NDR_PATTERN_REGISTRY.md` | P-30 Apogee-Attestation-Gate | P-11 11Q attestation | S-TIER >=95%, or A-TIER >=85% with open BLGs; Q11 >=9/10 for S-TIER | governance-ready/canonical promotion | P-30 explicitly registered S035; canonical registry |
| `docs/qa/APOGEE_11Q_S035.json` | first live P-30 run | P-11 11Q component scoring | 97.3% and 95.5%, S-TIER, attestation GRANTED | canonical quality attestation | dated S035 evidence artifact |
| `docs/qa/APOGEE_11Q_P34.json` | later P-30 attestation | 11Q per-dimension evidence scores | 94.5%, A-TIER, Q11=9, CONDITIONAL with BLGs | pattern promotion | explicit `attestation_gate=P-30`, `rubric=P-11 11Q Attestation Scoring` |
| `docs/agents/apogee/APOGEE_KB.md` | evidence-governance Apogee | evidence/provenance-based 11Q composite | primary scoring instrument; calibration is a Layer-0 requirement | final verification / governance | agent KB, aligned to attestation lineage |
| `components/ensemble_v17.py` | historical runtime `ApogeeReviewer` | caller-supplied `confidence`, optionally transformed by HPG to `eff_conf` | S>=0.90, A>=0.75, B>=0.60, C>=0.45, else D | per-turn runtime grading / gold star | executable historical mechanism, but not an internal confidence estimator |
| `pages/api/triad.ts` | web/runtime confidence path | request `confidence`, with default when absent | HPG-style snap then downstream use | runtime API | confirms externally supplied/default confidence contract, not calibration |
| `experiments/pdmal_pilot/pdmaltgl_gate_binding.py` | restored experiment mechanism | `ApogeeAttestationState.confidence` | historical scalar ladder; #165 adds D -> KILL | PDMAL gate restoration | explicitly says confidence is required input and is **not derivable from `agent_values`** |
| GitHub #165 | restoration designation | historical scalar confidence substrate | S/A/B/C/D; gold-star predicate; D -> KILL | semantic restoration | did not designate confidence provenance or state that S035 11Q registration was superseded |

## Chronology

1. P-30 is registered as **S035 — Apogee-Attestation-Gate**, Layer 5 Quality Gate, BLOCKING, CANONICAL.
2. The S035 evidence artifact records the first live P-30 run as 11Q attestation, with S-TIER scores and `GRANTED` decisions.
3. Subsequent P-30 attestations continue to explicitly bind `P-30` to the `P-11 11Q Attestation Scoring` rubric.
4. The historical ensemble implementation contains a different per-turn scalar-confidence reviewer named `ApogeeReviewer`.
5. Issue #165 later designated restoration semantics for that historical runtime reviewer inside the PDMAL experimental gate path, including `D -> KILL`, but did not designate a source/calibration for its confidence input and did not explicitly supersede the S035 canonical registry definition.
6. Experiment 001 exposed the missing scalar-confidence input; Epoch 002 showed the remainder of the path executes with a synthetic minimum-passing fixture; Epoch 003 then tested that explicitly synthetic-bound variant and obtained a negative directional result.

## Evidence-based reconciliation

### Recommended authority decision: separate the contracts

The least-assumptive reconciliation is:

1. **Retain P-30 as the canonical S035 Apogee-Attestation-Gate**, whose governance semantics are the P-11 11Q attestation contract recorded in the canonical pattern registry and demonstrated by signed/durable QA artifacts.
2. **Do not treat the historical scalar-confidence `ApogeeReviewer` ladder as equivalent to canonical P-30.** It is a distinct runtime grading mechanism whose present pattern identity is **UNASSIGNED** by this packet.
3. Treat issue #165 as evidence that the historical scalar ladder was deliberately restored for the experimental runtime path, including `D -> KILL`, but **not** as evidence that the canonical S035 P-30/11Q contract was superseded.
4. Do not invent a numeric bridge from 11Q percentage to runtime confidence. The two scores have different provenance, purposes, and thresholds; no normative bridge is currently designated.
5. Do not derive runtime confidence from PDMAL `agent_values`, `final_std`, FFCR outcomes, topology, or any post-treatment variable. The restored binding explicitly prohibits an `agent_values` proxy, and outcome-derived calibration would contaminate confirmatory interpretation.

## Why separation dominates the alternatives

### Against an implicit 11Q -> runtime-confidence bridge

A numeric 11Q percentage is evidence-governance attestation of a component/artifact. The historical runtime scalar is a caller-supplied turn confidence after optional HPG transformation. Treating one as the other would silently introduce a new measurement model and change the treatment.

A bridge could be researched later, but it would require its own specification, calibration evidence, non-circularity tests, and disjoint calibration/test data. It cannot be inferred from shared 0–1 ranges.

### Against making the historical scalar ladder canonical P-30 by default

The canonical registry explicitly identifies P-30 with S035 and 11Q-based governance-ready promotion, and S035 itself contains the first live P-30 attestation evidence. No located later authority record explicitly supersedes that definition. The scalar runtime implementation is therefore insufficient on its own to displace the registry lineage.

## Immediate governance consequences

Until a follow-up semantic migration is explicitly designated and merged:

- canonical P-30 remains the S035/P-11 11Q attestation meaning for governance claims;
- the restored PDMAL scalar ladder remains a **legacy/runtime experimental mechanism with unresolved independent pattern identity**;
- `DGAF-P30-EXPLICIT-0.45` remains exactly what Epoch 003 called it: a synthetic-bound experimental variant, not canonical DGAF;
- no new empirical run may be called **canonical DGAF** merely by selecting another scalar confidence;
- no default, phi constant, synthetic fixture, request default, or PDMAL state proxy may be relabeled as calibrated confidence;
- High-Assurance state is unchanged.

## Required follow-up before any new canonical DGAF epoch

A separate semantic-migration change must:

1. assign an explicit identity/name to the historical scalar runtime mechanism or explicitly retire it from the canonical treatment path;
2. update #165 references so historical restoration evidence remains preserved without overloading canonical P-30;
3. audit every PDMAL/TGL reference that currently labels the scalar ladder `P-30`;
4. decide whether canonical P-30/11Q belongs inside the per-turn PDMAL treatment at all, or instead remains a promotion/attestation gate outside the consensus dynamics;
5. if 11Q is proposed inside the treatment, define the object being scored per turn and establish a deterministic, non-circular scoring implementation before any empirical run;
6. run non-empirical parity/failure-mode tests on the exact proposed treatment;
7. preregister any later empirical epoch with fresh identity, seeds, blinding, analysis lock, and authorization.

## Current decision boundary

`P30_CANONICAL_AUTHORITY = S035_P11_11Q_ATTESTATION`

`LEGACY_RUNTIME_SCALAR_GATE_IDENTITY = UNASSIGNED_PENDING_SEMANTIC_MIGRATION`

`NORMATIVE_11Q_TO_RUNTIME_CONFIDENCE_BRIDGE = NOT_ESTABLISHED`

`NEW_CANONICAL_DGAF_EMPIRICAL_EPOCH = PROHIBITED_PENDING_SEMANTIC_MIGRATION`

This packet is an evidence-based reconciliation record. It does not itself rename executable classes or pattern IDs and does not authorize empirical execution.
