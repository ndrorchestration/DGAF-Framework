# DGAF Documentation Gap Audit

## Status

Audit performed before empirical execution and updated after expert-panel adjudication and subsequent CI troubleshooting. The substantive scientific and methodological protocol choices are resolved. Remaining work is limited to implementation/provenance verification required before the protocol can legitimately enter `FROZEN` status.

## Findings

| Area | Status | Required action |
|---|---|---|
| P6a CORS verification | CLOSED | Verified run `32092041579`, artifact `9308650112`; no further P6a work required. |
| PDMAL experiment protocol | PRE-FREEZE / PANEL-ADJUDICATED | Decisions are recorded in `PDMAL_EXPERIMENT_PROTOCOL.md`; freeze only after the remaining implementation controls and approved experimental commit are established. |
| Topology/baseline matrix | PANEL-ADJUDICATED / PROVENANCE PENDING | Record exact implementation SHAs, generation parameters, dependency/version identifiers, graph validation results, and canonical graph fingerprints for every topology. |
| Primary endpoint | RESOLVED | FFCR: completed trials without unrecovered failure / eligible trials; higher is better; primary estimand is the mean paired seed-level FFCR difference. |
| Secondary endpoints | RESOLVED | Recovery success, recovery latency, unrecovered failures, runtime, variance, connectivity/surviving component size, protocol compliance, missing/invalid rate, gate-block frequency; `D_a`/phi/topology diagnostics exploratory. |
| RNG specification | RESOLVED / VERSION RECORD PENDING | NumPy `Generator(PCG64)` using a root `SeedSequence` with domain-separated `spawn()` child streams. Record exact Python/NumPy versions, stream manifest, and checkpoint-state requirements. |
| Trial ordering/randomization | RESOLVED | Block-randomized within seed using dedicated ordering stream; realized order retained in auditable provenance without exposing analytical mapping. |
| Failure/recovery semantics | RESOLVED / RUNNER VERIFICATION PENDING | Candidate fixed values: 60s per-attempt timeout, 3 attempts, 30s recovery window; verify semantics against the pinned runner. |
| Exclusion rules | RESOLVED | Objective protocol violations only; retain exclusions with reasons; no outcome-based exclusion. |
| Stopping rules | RESOLVED | No efficacy stopping; only predefined safety, provenance, blinding, protocol-integrity, secret-exposure, catastrophic execution, or comparability halts. |
| Statistical analysis plan | RESOLVED / IMPLEMENTATION PENDING | One seed = one paired block; raw FFCR differences are the primary estimand; mean paired difference with 95% paired bootstrap CI; paired t-test is sensitivity/reference only. Implement and test the frozen analysis. |
| Sample-size rule | RESOLVED / IMPLEMENTATION PENDING | Target power 0.80, two-sided alpha 0.05, MDD 0.15; pilot estimates within-seed SD of paired FFCR difference; fixed paired-difference power approximation; round upward with `math.ceil`. Verify implementation and consistency with the primary estimand. |
| Blinding/unblinding | RESOLVED / CUSTODY VERIFICATION PENDING | Owner holds secret and does not analyze; executor/analyst see blinded IDs; panel chair unblinds after dataset/preprocessing/exclusion/integrity freeze; mapping stored separately as protected object. |
| Pilot acceptance criteria | RESOLVED / RUNTIME CEILING PENDING | 100% attempted, 0 blinding breaches, missing/invalid <=5%, all conditions execute, no comparability-affecting deviation, artifact/provenance checks pass, runtime <= frozen ceiling. |
| Data/artifact schema | RESOLVED / IMPLEMENTATION PENDING | One JSON artifact per seed; GitHub Actions artifact or approved durable storage; retain artifact ID, SHA-256, protocol/runner SHA, environment fingerprint, workflow/run ID, and attestation where supported. |
| Environment reproducibility | RESOLVED / VERSION RECORD PENDING | Pin exact Python/NumPy/dependencies/runner image and retain environment fingerprint/lock hash. |
| Protocol deviation register | RESOLVED / IMPLEMENTATION PENDING | Operationalize deviation ID, seed/trial, cause, impact, include/exclude decision, and authorization record. |
| Evidence classification | PRESENT | Maintain VERIFIED / VALIDATED / EMPIRICALLY SUPPORTED separation and condition-specific claims. |
| CI dependency boundary | DOCUMENTED / CORRECTED | Workflow now installs the PDMAL direct-pin manifest plus `pptl/requirements.txt`; `pandas` is declared by PPTL and is no longer treated as an undocumented direct PDMAL dependency. |
| PPTL import boundary | DOCUMENTED / CORRECTED / CI PENDING | `pptl/__init__.py` no longer imports the inconsistent legacy `IntegratedOrchestrator` path for adapter loading. Fresh current-head CI is still required. |
| CI evidence log | ADDED | `docs/experiment/PDMAL_CI_EVIDENCE_LOG_2026-08-18.md` records observed failures, corrections, evidence boundaries, and the next verification gate. |
| Metrics provenance registry | LEGACY GAP | `docs/qa/METRICS_PROVENANCE.md` remains separate technical debt and is not a pilot blocker when new pilot metrics are explicitly registered. |
| Issue #76 | UNVERIFIED | GitHub returned 404; do not infer state until repository identity/reference is resolved. |

## CI evidence now documented

The current troubleshooting sequence establishes the following without promoting it to functional verification:

1. `ModuleNotFoundError: pandas` was observed during adapter-test collection.
2. `pptl/requirements.txt` was verified to declare `pandas>=2.0.0`.
3. Commit `067f8706...` corrected CI dependency installation to include both dependency manifests.
4. The subsequent collection failure moved to `ImportError: cannot import name 'TGLConfig'`, demonstrating that the dependency boundary had advanced and exposing the inconsistent legacy orchestrator import path.
5. Repository inspection confirmed the adapter directly uses `TriadicGovernanceLoop`, `TGLHooks`, and `run_turn()` and does not require `IntegratedOrchestrator`.
6. Commit `ffde0b9a...` removed the unrelated orchestrator import/export from `pptl/__init__.py`.
7. A fresh CI result for the corrected head remains pending.

These findings are implementation/provenance evidence only. They do not establish PDMAL efficacy.

## Remaining pre-freeze verification blockers

Only these implementation/provenance controls remain before the protocol can legitimately enter `FROZEN` status:

1. Fresh current-head CI verification after the dependency and import-boundary corrections, including `test_dgaf_tgl_adapter.py`.
2. Exact topology implementation/source SHAs, parameters, graph validation, and fingerprints.
3. Exact Python/NumPy/environment versions and RNG manifest.
4. Verification of 60s timeout / 3 attempts / 30s recovery semantics in the pinned runner.
5. Verification of the paired-analysis implementation, bootstrap CI, and paired-difference sample-size implementation.
6. Canonical artifact schema validator, retention path, integrity manifest, and attestation path.
7. Blinded-label custody and protected mapping/unblinding mechanism.
8. Characterization and freeze of the numeric 300s seed-runtime ceiling in the pinned execution environment.
9. Operational protocol deviation register.

These are control/provenance requirements, not empirical results.

## Gate rule

No empirical seed generation is authorized until the remaining blockers above are resolved, the protocol is frozen with a commit SHA and timestamp, and pilot authorization is explicitly recorded.

## Evidence boundary

This audit identifies documentation completeness and protocol controls. It does not constitute evidence that PDMAL is effective.
