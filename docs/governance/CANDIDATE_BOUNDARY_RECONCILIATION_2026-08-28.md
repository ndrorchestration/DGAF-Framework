# DGAF/PDMAL Candidate Boundary Reconciliation — 2026-08-28

**Evidence class:** INTERNAL GOVERNANCE / PROVENANCE
**Lifecycle:** PRE-FREEZE / FAIL-CLOSED
**Experimental apparatus identity:** `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a`
**Current `main`:** authoritative for living implementation/documentation lineage
**Freeze:** NOT CREATED
**Authorization:** NOT GRANTED
**Empirical N:** 0

## Purpose

This record reconciles candidate identity, component fingerprints, deployment provenance, and evidence-surface boundaries. It does not create a new experimental apparatus candidate and does not constitute a freeze manifest.

## Candidate-bound component fingerprints

The following components were directly observed on the exact experimental candidate `ac8ea267…`:

- Runner — `experiments/pdmal_pilot/run_pilot.py` — `6b604d4eabaaf42b1dc9bd46099c8a09893ba1e9`
- Analysis — `experiments/pdmal_pilot/analysis.py` — `a269ed226b1d261663994fc3ef0e8a1a96da6cd3`
- Pilot artifact schema — `experiments/pdmal_pilot/pilot_artifact_schema.py` — `c620d3755a645c5f2ad14124f42ce07a1c670c5f`
- Durable retention — `experiments/pdmal_pilot/durable_retention.py` — `b2d889838b29ef74e1a6774db191c7a1b3c9e0ba`
- Harness contract — `experiments/pdmal_pilot/harness_contract.py` — `bb97c54ddf087fef568b1b3c8f8df72c30dad11e`
- Task engine — `experiments/pdmal_pilot/task_engine.py` — `4afb49ffbcbdfea2929c8c899b43568a8c42a300`
- Topology utilities — `experiments/pdmal_pilot/topology_utils.py` — `7ae92ba8a9ab964537e5dafa5e12de36b841391e`
- Topology manifest — `experiments/pdmal_topology/manifest.yaml` — `3abeeabc71fc0921cd9af6c53cfad1e6118bb2d1`
- Task specification — `docs/experiment/PDMAL_TASK_SPEC_V0.7.4.md` — `06a8386979fc8f1e3483d8ea76a5754b4a6ce487`
- Protocol amendment — `docs/experiment/PDMAL_PROTOCOL_MATRIX_AMENDMENT_V0.7.5.md` — `a686366c4754c3532d46118f55739ddd0685c558`
- P7 adjudication — `docs/experiment/PRIMARY_CONTRAST_ADJUDICATION.md` — `db728dbd8e34426bbf2d3c20d01116883d6f3a19`
- Governance CI — `.github/workflows/governance-ci.yml` — `fd4d29b79d8d31ca42c11660ce8efa4b6678dfbd`
- P2 workflow — `.github/workflows/p2-runtime-verification.yml` — `76e0a3014127ec1ebe164a0c1c5b45b8388eef02`
- Dependency lock — `experiments/pdmal_pilot/requirements-full-lock.txt` — `00c1f779e97030f9b25ae494642edb31b5b09de5`

## Protocol binding

The current canonical protocol text on `main` is a living specification and is not itself a freeze. Its final blob identity and applicability are to be captured in the eventual freeze/P8 packet. The historical candidate manifest from 2026-08-21 remains provenance only.

## Deployment boundary

READY deployment `dpl_DND15HJ45s1d5eFcGmVr4SWNpGaC` is source-bound to `ac8ea267…`. Deployment readiness and `/api/health` are deployment evidence only. P2/P6a remain authenticated runtime predicates requiring the same exact candidate/deployment identity.

## Scientific binding

The adopted scientific target is `dgaf` versus `null`, with FFCR as the primary endpoint, paired by root seed, equal-weight mean paired seed effect, two-sided 95% percentile paired bootstrap, 10,000 resamples, bootstrap seed `20260823`, and alpha `0.05`. Exact freeze binding remains open.

## Evidence surfaces

**PUBLIC-FACING:** stable, audience-appropriate, traceable implementation/methodology/scoped-verification claims. No private custody mechanics or efficacy implication from readiness/verification.

**INTERNAL GOVERNANCE:** complete dependencies, candidate/run/deployment identity, provenance, custody, panel decisions, blockers, and audit detail.

**EMPIRICAL/EFFICACY:** only authorized experimental observations tied to the frozen protocol, admissible retained data, and locked analysis. CI, deployment readiness, formal verification, synthetic fixtures, expert review, and documentation quality are not efficacy evidence by themselves.

## Non-authorizing limitations

This document is a governance reconciliation record only. It does not authorize execution, create a freeze, expose or establish a blinding key, establish P2/P6a execution, close P8/P9, or increase empirical N.

**Current state: PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · empirical N=0.**
