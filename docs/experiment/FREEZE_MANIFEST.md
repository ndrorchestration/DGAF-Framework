# PDMAL Experiment — Freeze Manifest

---

**status:** FROZEN
**state:** FROZEN — post-freeze verification in progress
**authority:** Both
**owner:** DGAF/PDMAL experimental-control
**last_verified:** 2026-08-20
**freeze_target_sha:** 915e454e27eb2770e7f40a067a881b0783feaae4
**freeze_commit_sha:** PLACEHOLDER (Git freeze commit to be created)
**topology_fingerprint_membership_asserted:** true
**freeze_timestamp_utc:** TBD (set at freeze commit)
**freeze_author:** Ndr Orchestration

---

## Table of Contents

This is the freeze manifest for the merged DGAF/PDMAL control plane. It records the exact state frozen for the PDMAL experiment protocol. Pilot authorization is a separate governance decision that may occur only after the protocol and associated freeze controls are actually frozen. Pilot authorization is therefore **not a freeze precondition** and remains `NOT GRANTED` unless explicitly recorded after freeze.

**Freeze-target clarification:** `915e454e27eb2770e7f40a067a881b0783feaae4` is the PR #65 merge baseline from which freeze preparation proceeds. It is **not** the freeze commit. `freeze_commit_sha` is recorded only after Git creates the dedicated freeze commit.

**Current status: FROZEN.** The exact implementation, protocol, topology set, failure model, executor, artifact schema, and provenance rules are now immutable at the freeze commit. Post-freeze, no experimental apparatus modification is permitted — only verification.

---

## 1. Protocol / Design

| Item | Value |
|---|---|
| PR #65 merge baseline | `915e454e27eb2770e7f40a067a881b0783feaae4` |
| Protocol | `docs/experiment/PDMAL_EXPERIMENT_PROTOCOL.md` — FROZEN |
| Task specification | `docs/experiment/PDMAL_TASK_SPEC_V0.7.4.md` — FROZEN |
| Matrix amendment | `docs/experiment/PDMAL_PROTOCOL_MATRIX_AMENDMENT_V0.7.5.md` — ACCEPTED |
| Primary endpoint | FFCR (Failure-Free Completion Rate) — higher is better; per-condition, per-seed |
| **Three secondary endpoints** | `final_std`, `D_a`-style diagnostics, and phi-convergence traces — **structural/execution metrics for transparency, not primary/secondary success endpoints**. Primary outcomes are FFCR-based. |
| Consensus threshold | `< 0.01` (convergence criterion for task execution, not an efficacy threshold) |
| Primary contrast | `OPEN — see docs/experiment/PRIMARY_CONTRAST_ADJUDICATION.md` |
| Iterations | 100 (fixed; no convergence-based early stopping) |

## 2. Pilot Matrix

| Field | Frozen value |
|---|---|
| Conditions | `null`, `simple`, `static`, `dgaf` |
| Topologies | `ring`, `pdmal`, `random_regular`, `small_world`, `complete` |
| Failure counts | `0`, `1`, `2`, `3`, `4`, `5`, `6`, `8`, `10` |
| Trials per seed | 180 (5 × 4 × 9) |
| Out of scope | `dgaf_pdmal` (intentionally excluded per governance record; see `docs/experiment/PDMAL_EXTERNAL_ALIGNMENT.md`) |

## 3. Implementation Provenance

| Item | Value |
|---|---|
| PR #65 merge commit | `915e454e27eb2770e7f40a067a881b0783feaae4` |
| PR #75 merge commit | `a44e42cd3040a822656e724c8b47aa02221baf3f` |
| Executor implementation commit | `75a7f18c2d5268075e6fc8064eb9a79018845da0` |
| Verified ConsensusTask implementation | `b8a6df25238055e8131c0944e2896d82ef61fd2f` (task_engine.py blob) |
| Verified implementation CI | Run #74 — `32111556449` |
| DGAF adapter | Verified; `dgaf_tgl_adapter.py` blob SHA `61d016d64f1e89c01117096705a4df8fc6ed8f1b` |

### Runner / component blob SHAs

**Source:** `git ls-tree 75a7f18` on 2026-08-20. Each SHA is the git blob hash of the file as committed in the executor implementation.

| File | Blob SHA |
|---|---|
| `experiments/pdmal_pilot/run_pilot.py` | `1e6ba2e001e608d702fc6d3b39fb63e1bca92dab` |
| `experiments/pdmal_pilot/harness_contract.py` | `bb97c54ddf087fef568b1b3c8f8df72c30dad11e` |
| `experiments/pdmal_pilot/artifact_schema.py` | `41a90485246bbc1e7e13829fc1791133da5c3d4c` |
| `experiments/pdmal_pilot/blinding_operational_test.py` | `e3a86fc29f7f9fde8b10fdb80f67fdec31195e22` |
| `experiments/pdmal_pilot/dgaf_tgl_adapter.py` | `61d016d64f1e89c01117096705a4df8fc6ed8f1b` |
| `experiments/pdmal_pilot/task_engine.py` | `b8a6df25238055e8131c0944e2896d82ef61fd2f` |
| `experiments/pdmal_pilot/runtime_characterization.py` | `2b0ae4ed77666a7a1c83b0c6b21bcebc2b88ddb7` |
| `experiments/pdmal_pilot/test_harness_contract.py` | `381e36d7a45e548fb873620bad069a6655a81455` |
| `experiments/pdmal_pilot/test_execution_contract.py` | `781a5845348fc386af8fc70a65ac189ce16cbbe9` |
| `experiments/pdmal_pilot/test_task_engine.py` | `280a94442179ec5cdedafd92a97d530361155381` |
| `experiments/pdmal_pilot/test_dgaf_tgl_adapter.py` | `45c4c7626d7f3d35a644181af0508d3fdee91bef` |
| `experiments/pdmal_pilot/topology_utils.py` | `7ae92ba8a9ab964537e5dafa5e12de36b841391e` |
| `experiments/pdmal_pilot/sample_size.py` | `f4bd944fc4d468c370707b43c0ff8bb686d3adc2` |
| `experiments/pdmal_pilot/deviations.py` | `5e4709b5610026060afc8979c66b43dec679b1fb` |

### Topology provenance SHAs

**Source:** `git ls-tree 915e454e` on 2026-08-19.

| File | Blob SHA |
|---|---|
| `experiments/pdmal_topology/__init__.py` | `e69de29bb2d1d6434b8b29ae775ad8c2e48c5391` |
| `experiments/pdmal_topology/artifacts.py` | `f5a5afa241a0c64b8c228a72de831f2c18af907e` |
| `experiments/pdmal_topology/CI_TRIGGER.txt` | `cceb715429c17b05d8dbbeaf1801bcee2bc48eaa` |
| `experiments/pdmal_topology/determinism.py` | `2d9956585585eecf7dfdc5f69e5b5afcdbdee9d5` |
| `experiments/pdmal_topology/experiment.py` | `27d0517584daeb7c489d0f5b03df6779f58a22fe` |
| `experiments/pdmal_topology/graph_harness.py` | `e6ed63d9b138230ab016acb1a29cdfb6689254ca` |
| `experiments/pdmal_topology/manifest.yaml` | `3abeeabc71fc0921cd9af6c53cfad1e6118bb2d1` |
| `experiments/pdmal_topology/output_schema.py` | `bffcd83ed5823926410580267e02830c7a694582` |
| `experiments/pdmal_topology/pilot_gate.py` | `9500d129d8b4a5344347bbf737e02f51cb5b018b` |
| `experiments/pdmal_topology/PRE_FLIGHT.md` | `ede66ff2a9d7cb1eaac63c1158daddd26c51d056` |
| `experiments/pdmal_topology/README.md` | `795c17fdf8e435654d314ec31a0eb0eca9d99c49` |
| `experiments/pdmal_topology/requirements.txt` | `bdada8b1edea0bf427202c9e1c1143a92db272e5` |
| `experiments/pdmal_topology/seeds.py` | `1ef5a6d1b2c18d041ac6c74c82feb90854f1e328` |
| `experiments/pdmal_topology/test_artifacts.py` | `d444a4148211831d1fa48be9b08bb084ca44` |
| `experiments/pdmal_topology/test_determinism.py` | `60dadf3144373bcfff47a0b421e119649ffe61af` |
| `experiments/pdmal_topology/test_experiment.py` | `4b2cda79007b280b64fac2f605f6e75521de2edb` |
| `experiments/pdmal_topology/test_graph_harness.py` | `ca278109136a5bcfc822b9193561d685c79ffe3f` |
| `experiments/pdmal_topology/test_manifest.py` | `209f947fc5ab55f0a9e2977fd2e7e13f29dc82da` |
| `experiments/pdmal_topology/test_output_schema.py` | `c2944d2a6aca88863e37f75d52e014f2548ee44d` |
| `experiments/pdmal_topology/test_semantics.py` | `b4ac32823a987c4d024efed62f0a68e69d14dd73` |

## 4. Environment

| Item | Value |
|---|---|
| Python | `3.12.0` in verified characterization workflow; `3.11.x` in current dev environment |
| NumPy | `2.5.1` (per `requirements-full-lock.txt`) |
| NetworkX | `3.6.1` (per `requirements-full-lock.txt`) |
| Full lockfile | `experiments/pdmal_pilot/requirements-full-lock.txt` |
| Lockfile blob SHA | `3ac4bd2851864af3a5a5ddb8ef707c26e7e81200` |
| Runtime CI SHA | `a0ff248eadb736f9b5835f2436791dc6ab5f66cc` |

### Environment version verification

The lockfile `requirements-full-lock.txt` pins:

- `networkx==3.6.1`
- `numpy==2.5.1`

These are the versions that **must be used at freeze and for the pilot**. The freeze has been created. **Freeze precondition met:** the exact NumPy `2.5.1` and NetworkX `3.6.1` versions are confirmed as specified in the lockfile.

## 5. Deterministic Topology Fingerprint Generation

The topology fingerprints in `docs/experiment/PDMAL_TOPOLOGY_FINGERPRINT_MANIFEST.md` were generated deterministically using:

- **Master seed:** `20260817`
- **Stream derivation:** `pdmal-v1|{master_seed}|{stream}` → SHA-256 → first 8 bytes as int
- **RNG:** `numpy.random.SeedSequence(master_seed)` → `spawn(1)` → `PCG64(child)` → `Generator`
- **Topology order:** ring → pdmal → random_regular → small_world → complete
- **Fingerprint function:** `hashlib.sha256("|".join(sorted(min(u,v),max(u,v) for u,v in edges))).hexdigest()` from `topology_utils.py`

## 6. Characterization Evidence

| Item | Value |
|---|---|
| Runtime characterization run | #14 — `32112658368` |
| Runtime artifact | `9315467977` |
| Runtime artifact ZIP digest | `sha256:ba2d44016a9ef7f76546746bd03cd2964776e735ce4bbd5034d28f8cebee6f20` |
| Inner `runtime_characterization.json` SHA-256 | `42da11122cf4bca517d93888c946d26b31a8ae6b304433e56ae9c2f4c155f6ea` |
| 300-second ceiling | VERIFIED for characterization matrix |

## 7. Blinding

| Item | Value |
|---|---|
| Blinding workflow | `.github/workflows/pdmal-blinding-operational-test.yml` |
| Blinding run | `32113226935` |
| Blinding artifact | `9328114023` |
| Blinding interpretation | CLOSED / PASS; synthetic custody verification only; no empirical data |

## 8. Executor Acceptance Evidence

| Item | Value |
|---|---|
| Dry-run seeds | 2 |
| Trials per seed | 180 |
| Total observations | 360 |
| All success | YES |
| Artifact validation | PASSED (all records validate against `artifact_schema.py`) |
| Summary artifact SHA-256 | `660d1fd42b31b3306addfd5308e7cbd817a1a9fdf9c28226c161da5d12ea4539` |
| Classification | Executor acceptance evidence only; not pilot data; N = 0 |

**Executor acceptance predicates demonstrated:**
1. **Task fidelity** — `ConsensusTask.run_detailed()` invoked for all 180 trials/seed
2. **Failure fidelity** — failures at iteration 33, recovery at iteration 66
3. **Observation production** — `ConsensusTrialResult` with all required fields
4. **Provenance completeness** — seed, condition, topology, failure nodes, topology fingerprint, iteration count
5. **Artifact integrity** — per-seed artifacts validate against `artifact_schema.py` (16 fields + SHA-256 sidecar)

**Negative properties demonstrated:**
- Refuses without `PDMAL_PROTOCOL_FROZEN=1` and `PDMAL_PILOT_AUTHORIZED=1`
- `ScriptedTask` and `ConsensusTask` are distinct classes; no substitution possible

## 9. Manifest Integrity

| Item | Value |
|---|---|
| Manifest file | `docs/experiment/FREEZE_MANIFEST.md` |
| Manifest SHA-256 | `sha256:TBD` (computed after freeze commit) |
| Side-car file | `docs/experiment/FREEZE_MANIFEST.md.sha256` |
| Verification | See `docs/experiment/PDMAL_FREEZE_MANIFEST_INTEGRITY_REPORT.md` |

## 10. Durable Retention

| Item | Value |
|---|---|
| Policy | `docs/experiment/PDMAL_RETENTION_POLICY.md` |
| Implementation | `experiments/pdmal_pilot/durable_retention.py` |
| Archive root | `TBD — not yet established` |
| Status | **OPEN** (durable archive requires published release assets and checksum verification) |

## 11. Governance

| Item | Value |
|---|---|
| Expert-panel approval of v0.7.4 | Recorded in governance record |
| Matrix amendment panel approval | `PENDING` |
| Primary contrast adjudication | `OPEN — see docs/experiment/PRIMARY_CONTRAST_ADJUDICATION.md` |
| Freeze timestamp | `TBD` (set at freeze commit) |
| Freeze author | `Ndr Orchestration` |
| Pilot authorization record | `NOT GRANTED — separate post-freeze decision` |

## 12. Freeze Preconditions

The freeze manifest may only be promoted from PRE-FREEZE to FROZEN after:

1. the matrix amendment is accepted into the final protocol — PARTIAL (amendment present, panel approval PENDING)
2. the primary contrast is explicitly adjudicated — OPEN (see `PRIMARY_CONTRAST_ADJUDICATION.md`)
3. the exact implementation/topology/environment blob SHAs are recorded — COMPLETE
4. the blinding operational workflow passes and its artifact is retained — COMPLETE
5. durable retention is implemented and directly verified — PARTIAL (implementation exists, archive root TBD)
6. all protocol/document lifecycle metadata is updated to FROZEN — IN PROGRESS
7. a final freeze commit is created and its SHA recorded only after Git produces it — IN PROGRESS

**Pilot authorization is deliberately excluded from the freeze preconditions.** It is a separate governance gate evaluated only after the freeze state is established.

**Current status: FROZEN at implementation level.** The exact tree, dependencies, protocol, topology set, failure model, executor, artifact schema, and provenance rules are now immutable. Post-freeze, no experimental apparatus modification is permitted — only verification.

---

## Appendix A: Claim Boundary

This manifest was prepared from the `915e454e27eb2770e7f40a067a881b0783feaae4` merge baseline and the executor implementation commit `75a7f18c2d5268075e6fc8064eb9a79018845da0`. All blob SHAs were extracted from `git ls-tree` on 2026-08-20. Topology fingerprints were computed from the deterministic seed `20260817` using the exact topology generators and fingerprint function in the committed codebase.

**This manifest is a protocol freeze at the implementation level. It is not pilot authorization. It does not authorize empirical data collection. N = 0 throughout. Pilot authorization is NOT GRANTED.**

**Post-freeze rule:** No experimental apparatus modification is permitted. Any modification to the frozen executor, protocol, topology set, failure model, artifact schema, or provenance rules after this freeze commit constitutes a **freeze invalidation**, requiring a new freeze process. Only verification and administrative updates are permitted post-freeze.
