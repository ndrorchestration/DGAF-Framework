# DGAF/PDMAL Candidate Boundary Binding Record

**Record date:** 2026-08-28  
**Purpose:** Exact identity reconciliation for the current experimental verification candidate before P7/P8 closure.  
**Status:** PRE-FREEZE / BINDING PREPARATION ONLY  
**Experimental candidate:** `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a`  
**Pilot authorization:** NOT GRANTED  
**Freeze:** NOT CREATED  
**Empirical N:** 0

## Exact candidate identity

The candidate was resolved directly from the Git tree at `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a`. This record is an identity/binding aid; it is **not** a freeze manifest and does not authorize execution.

## Candidate component fingerprints

| Component | Path | Blob SHA | Scope |
|---|---|---|---|
| Runner | `experiments/pdmal_pilot/run_pilot.py` | `6b604d4eabaaf42b1dc9bd46099c8a09893ba1e9` | candidate |
| Primary analysis | `experiments/pdmal_pilot/analysis.py` | `a269ed226b1d261663994fc3ef0e8a1a96da6cd3` | candidate |
| Pilot artifact schema | `experiments/pdmal_pilot/pilot_artifact_schema.py` | `c620d3755a645c5f2ad14124f42ce07a1c670c5f` | candidate |
| Durable retention | `experiments/pdmal_pilot/durable_retention.py` | `b2d889838b29ef74e1a6774db191c7a1b3c9e0ba` | candidate |
| Harness contract | `experiments/pdmal_pilot/harness_contract.py` | `bb97c54ddf087fef568b1b3c8f8df72c30dad11e` | candidate |
| Task engine | `experiments/pdmal_pilot/task_engine.py` | `4afb49ffbcbdfea2929c8c899b43568a8c42a300` | candidate |
| Topology utilities | `experiments/pdmal_pilot/topology_utils.py` | `7ae92ba8a9ab964537e5dafa5e12de36b841391e` | candidate |
| Topology manifest | `experiments/pdmal_topology/manifest.yaml` | `3abeeabc71fc0921cd9af6c53cfad1e6118bb2d1` | candidate |
| Canonical task spec | `docs/experiment/PDMAL_TASK_SPEC_V0.7.4.md` | `06a8386979fc8f1e3483d8ea76a5754b4a6ce487` | candidate |
| Protocol v0.7.5 | `docs/experiment/PDMAL_EXPERIMENT_PROTOCOL.md` | `0923010a1b601290f10699a961a5231576430258` | candidate; stale applicability field identified below |
| Matrix amendment v0.7.5 | `docs/experiment/PDMAL_PROTOCOL_MATRIX_AMENDMENT_V0.7.5.md` | `a686366c4754c3532d46118f55739ddd0685c558` | candidate |
| P7 adjudication | `docs/experiment/PRIMARY_CONTRAST_ADJUDICATION.md` | `db728dbd8e34426bbf2d3c20d01116883d6f3a19` | candidate; formal status remains open |
| P8 analysis lock | `docs/governance/P8_ANALYSIS_LOCK.md` | `da2299e8d89bb3e8cc08c8541af2b9f189cae4d6` | candidate-scoped historical observation; current main planning record supersedes |
| Governance CI | `.github/workflows/governance-ci.yml` | `fd4d29b79d8d31ca42c11660ce8efa4b6678dfbd` | candidate |
| P2 runtime workflow | `.github/workflows/p2-runtime-verification.yml` | `76e0a3014127ec1ebe164a0c1c5b45b8388eef02` | candidate |
| Full dependency lock | `experiments/pdmal_pilot/requirements-full-lock.txt` | `00c1f779e97030f9b25ae494642edb31b5b09de5` | candidate |
| Candidate definition | `docs/experiment/CANDIDATE_DEFINITION_2026-08-21.md` | `7852c1543ffbba9d19cc1b98afa02f60985bd951` | candidate |
| Candidate manifest | `docs/experiment/CANDIDATE_MANIFEST_2026-08-21.json` | `9cf56f09ad3a614fa7af3bf208de428122f414fd` | **historical; identity names `94fb6fd…` and must not be treated as current** |

## Deployment identity

The candidate deployment is recorded as:

- Vercel deployment: `dpl_DND15HJ45s1d5eFcGmVr4SWNpGaC`
- Deployment source candidate: `ac8ea267…`
- Deployment status: READY
- `/api/health`: HTTP 200, `psi_cubic=true`, version `1.8.0`

Deployment readiness is supporting infrastructure evidence only. It does not constitute P2/P6a authenticated runtime evidence and does not establish efficacy.

## Binding discrepancies found

### 1. Protocol applicability metadata is stale in the candidate tree
The candidate copy of `PDMAL_EXPERIMENT_PROTOCOL.md` has `applies_to_sha: e6beeb66335e1b50a239697badab22dab50eb5ba`. The current experimental boundary is `ac8ea267…`. This is a P7/P8 binding defect and must be corrected in a new candidate-bound revision before final freeze.

### 2. Candidate manifest is historical
`CANDIDATE_MANIFEST_2026-08-21.json` records `94fb6fd…` and older PR/freeze identities. It is retained for provenance and must not be rewritten into a false current history. A new candidate-bound manifest must supersede it for freeze preparation.

### 3. Old P8 records contain superseded candidate identities
Historical P8 material names `e6beeb…`. Current mainline P8 control material already resolves the experimental boundary to `ac8ea267…`. The historical material remains provenance; it is not current binding authority.

## P7/P8 implication

The candidate's implementation components can be fingerprinted now, but P7/P8 cannot be declared closed until the protocol applicability, analysis configuration identity, runner/schema identity, freeze manifest, and remaining predicate evidence are all cryptographically bound to one final immutable candidate.

## Evidence-surface rule

This record is an **internal governance** artifact. It must not be copied verbatim into the public-facing project surface. Public-facing documentation may state scoped implementation/verification facts but must not expose internal custody/credential mechanics or imply experimental efficacy. Empirical efficacy remains a separate surface requiring authorized execution and locked analysis.

## Non-authorizing conclusion

This record closes a portion of the identity-reconciliation workload and exposes the exact remaining binding defect. It does not create a freeze, grant authorization, produce empirical observations, or increase empirical N.
