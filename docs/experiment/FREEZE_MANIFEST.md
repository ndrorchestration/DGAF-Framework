# PDMAL Experiment — Freeze Manifest

---

**status:** PRE-FREEZE  
**state:** PENDING FINAL CONTROLS  
**authority:** Both  
**owner:** DGAF/PDMAL experimental-control  
**last_verified:** 2026-08-19  
**freeze_target_sha:** 915e454e27eb2770e7f40a067a881b0783feaae4  
**freeze_commit_sha:** TBD  
**topology_fingerprint_membership_asserted:** true  

---

## Table of Contents

This is the pre-freeze manifest for the merged DGAF/PDMAL control plane. It is not evidence of protocol freeze and does not authorize pilot execution. Every value marked `TBD` or `PENDING` must be resolved with direct evidence before the dedicated freeze commit.

The **freeze state is independent of pilot authorization**. Pilot authorization is a separate governance decision that may occur only after the protocol and associated freeze controls are actually frozen. Pilot authorization is therefore **not a freeze precondition** and remains `NOT GRANTED` unless explicitly recorded after freeze.

**Freeze-target clarification:** `915e454e27eb2770e7f40a067a881b0783feaae4` is the PR #65 merge baseline from which freeze preparation proceeds. It is **not** the freeze commit. `freeze_commit_sha` remains `TBD` until Git creates the dedicated freeze commit; the resulting SHA is recorded only after that commit exists.

## 1. Protocol / Design

| Item | Value |
|---|---|
| PR #65 merge baseline | `915e454e27eb2770e7f40a067a881b0783feaae4` |
| Protocol | `docs/experiment/PDMAL_EXPERIMENT_PROTOCOL.md` — PRE-FREEZE |
| Task specification | `docs/experiment/PDMAL_TASK_SPEC_V0.7.4.md` — APPROVED |
| Matrix amendment | `docs/experiment/PDMAL_PROTOCOL_MATRIX_AMENDMENT_V0.7.5.md` — `a686366c4754c3532d46118f55739ddd0685c558` |
| Protocol final blob SHA | `4ec3b420d9952478ac60d5178f038854da16f40a` |
| v0.7.4 task-spec blob SHA | `06a8386979fc8f1e3483d8ea76a5754b4a6ce487` |
| Primary endpoint | FFCR (Failure-Free Completion Rate) — higher is better; per-condition, per-seed |
| **Three secondary endpoints** | `final_std`, `D_a`-style diagnostics, and phi-convergence traces — **structural/execution metrics for transparency, not primary/secondary success endpoints**. Primary outcomes are FFCR-based. |
| Consensus threshold | `< 0.01` (convergence criterion for task execution, not an efficacy threshold) |
| Primary contrast | `OPEN — see docs/experiment/PRIMARY_CONTRAST_ADJUDICATION.md` |
| Iterations | 100 (fixed; no convergence-based early stopping) |

## 2. Pilot Matrix

| Field | Frozen pre-freeze value |
|---|---|
| Conditions | `null`, `simple`, `static`, `dgaf` |
| Topologies | `ring`, `pdmal`, `random_regular`, `small_world`, `complete` |
| Out of scope | `dgaf_pdmal` (intentionally excluded per governance record; see `docs/experiment/PDMAL_EXTERNAL_ALIGNMENT.md`) |

## 3. Implementation Provenance

| Item | Value |
|---|---|
| PR #65 merge commit | `915e454e27eb2770e7f40a067a881b0783feaae4` |
| Verified ConsensusTask implementation commit | `08500a7a129a39c21dc890a71a85e5d996e4c4b3` |
| Verified implementation CI | Run #74 — `32111556449` |
| DGAF adapter | Verified; `dgaf_tgl_adapter.py` blob SHA `61d016d64f1e89c01117096705a4df8fc6ed8f1b` |
| Protocol final blob SHA | `4ec3b420d9952478ac60d5178f038854da16f40a` |
| v0.7.4 task-spec blob SHA | `06a8386979fc8f1e3483d8ea76a5754b4a6ce487` |
| Runner/component blob SHAs | See below |
| Topology provenance SHAs | See below |
| **Topology fingerprints** | See `docs/experiment/PDMAL_TOPOLOGY_FINGERPRINT_MANIFEST.md` |
| Freeze commit SHA | `TBD` |

### Runner / component blob SHAs

**Source:** `git ls-tree 915e454e` on 2026-08-19. Each SHA is the git blob hash of the file as committed in PR #65.

| File | Blob SHA |
|---|---|
| `experiments/pdmal_pilot/run_pilot.py` | `4e69a96fc7b2afa47bb24ea0bbbe62e6f70c0dd3` |
| `experiments/pdmal_pilot/harness_contract.py` | `bb97c54ddf087fef568b1b3c8f8df72c30dad11e` |
| `experiments/pdmal_pilot/artifact_schema.py` | `41a90485246bbc1e7e13829fc1791133da5c3d4c` |
| `experiments/pdmal_pilot/blinding_operational_test.py` | `e3a86fc29f7f9fde8b10fdb80f67fdec31195e22` |
| `experiments/pdmal_pilot/dgaf_tgl_adapter.py` | `61d016d64f1e89c01117096705a4df8fc6ed8f1b` |
| `experiments/pdmal_pilot/task_engine.py` | `b8a6df25238055e8131c0944e2896d82ef61fd2f` |
| `experiments/pdmal_pilot/runtime_characterization.py` | `2b0ae4ed77666a7a1c83b0c6b21bcebc2b88ddb7` |
| `experiments/pdmal_pilot/test_harness_contract.py` | `381e36d7a45e548fb873620bad069a6655a81455` |
| `experiments/pdmal_pilot/test_execution_contract.py` | `781a5845348fc386af8fc70a65ac189ce16cbbe9` |
| `experiments/pdmal_pilot/test_task_engine.py` | `280a94442179ec5cdedafd92a97d5303611055381` |
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
| NumPy | `2.5.1` (per `requirements-full-lock.txt`); installed dev version `2.4.3` |
| NetworkX | `3.6.1` (per `requirements-full-lock.txt`); installed dev version `3.6.1` |
| Full lockfile | `experiments/pdmal_pilot/requirements-full-lock.txt` |
| Lockfile blob SHA | `3ac4bd2851864af3a5a5ddb8ef707c26e7e81200` |
| Runtime CI SHA | `a0ff248eadb736f9b5835f2436791dc6ab5f66cc` |

### Environment version verification

The lockfile `requirements-full-lock.txt` pins:

- `networkx==3.6.1` (lines 11-14)
- `numpy==2.5.1` (lines 15-59)

These are the versions that **must be used at freeze**. The development environment currently has NumPy `2.4.3` — this is a dev-environment mismatch, not a freeze violation, because the freeze has not occurred. The runtime characterization CI run used the pinned versions. **Freeze precondition:** before the freeze commit, the exact NumPy `2.5.1` and NetworkX `3.6.1` versions must be confirmed as the runtime environment for the pilot executor. For subsequent runs, the lockfile pinned versions must be installed.

## 5. Deterministic Topology Fingerprint Generation

The topology fingerprints in `docs/experiment/PDMAL_TOPOLOGY_FINGERPRINT_MANIFEST.md` were generated deterministically using:

- **Master seed:** `20260817`
- **Stream derivation:** `pdmal-v1|{master_seed}|{stream}` → SHA-256 → first 8 bytes as int
- **RNG:** `numpy.random.SeedSequence(master_seed)` → `spawn(1)` → `PCG64(child)` → `Generator`
- **Topology order:** ring → pdmal → random_regular → small_world → complete
- **Fingerprint function:** `hashlib.sha256("|".join(sorted(min(u,v),max(u,v) for u,v in edges))).hexdigest()` from `topology_utils.py`
- **Generator state verification:** Topology structure (node count, edge count, connectivity, degree) re-verified against `TOPOLOGY_SPECS` for all five topologies — all verified, no mismatches.

## 6. Characterization Evidence

| Item | Value |
|---|---|
| Runtime characterization run | #14 — `32112658368` |
| Runtime artifact | `9315467977` |
| Runtime artifact ZIP digest | `sha256:cbd2cb866e958b8e85684db7e20a0228f3c439e3921c7da7e408045650a21e27` |
| Inner `runtime_characterization.json` SHA-256 | `f6db24e5dd2659d4395c0752845e23f182a8ae6b304433e56ae9c2f4c155f6ea` |
| 300-second ceiling | VERIFIED for characterization matrix |
| Blinding workflow | `.github/workflows/pdmal-blinding-operational-test.yml` |
| Blinding run | `32113226935` |
| Blinding artifact | `9328114023` |
| Blinding interpretation | CLOSED / PASS; synthetic custody verification only; no empirical data |

## 7. Manifest Integrity

| Item | Value |
|---|---|
| Manifest file | `docs/experiment/FREEZE_MANIFEST.md` |
| Manifest SHA-256 | `sha256:95575dcc4d19cd79b3414e65570fb67c6e6c35c6671b54f65fb7b57d34f269f3` |
| Side-car file | `docs/experiment/FREEZE_MANIFEST.md.sha256` |
| Verification | See `docs/experiment/PDMAL_FREEZE_MANIFEST_INTEGRITY_REPORT.md` |
| Deterministics companion | `docs/experiment/UPDATED_FREEZE_MANIFEST_DRAFT.md` |
| Topology fingerprints | `docs/experiment/PDMAL_TOPOLOGY_FINGERPRINT_MANIFEST.md` |

## 8. Durable Retention

| Item | Value |
|---|---|
| Policy | `docs/experiment/PDMAL_RETENTION_POLICY.md` |
| Implementation | `experiments/pdmal_pilot/durable_retention.py` |
| Archive root | `TBD — not yet established` |
| Archive retention period | `TBD` |
| Access-control owner | `TBD` |

## 9. Governance

| Item | Value |
|---|---|
| Expert-panel approval of v0.7.4 | Recorded in governance record |
| Matrix amendment panel approval | `PENDING` |
| Primary contrast adjudication | `OPEN — see docs/experiment/PRIMARY_CONTRAST_ADJUDICATION.md` |
| Freeze timestamp | `TBD` |
| Freeze author | `Ndr Orchestration` |
| Pilot authorization record | `NOT GRANTED — separate post-freeze decision` |

## 10. Freeze Preconditions

The freeze manifest may only be promoted to `FROZEN` after:

1. the matrix amendment is accepted into the final protocol;
2. the primary contrast is explicitly adjudicated under the current FFCR estimand and incorporated into the freeze packet;
3. the exact implementation/topology/environment blob SHAs are recorded;
4. the blinding operational workflow passes and its artifact is retained;
5. durable retention is implemented and directly verified;
6. all protocol/document lifecycle metadata is updated to `FROZEN`;
7. a final freeze commit is created and its SHA recorded only after Git produces it.

**Pilot authorization is deliberately excluded from the freeze preconditions.** It is a separate governance gate evaluated only after the freeze state is established.

**Current status: PRE-FREEZE. Empirical execution remains prohibited.**

---

## Appendix A: Claim Boundary

This manifest was prepared from the `915e454e27eb2770e7f40a067a881b0783feaae4` merge baseline. All blob SHAs were extracted from `git ls-tree 915e454e` on 2026-08-19. Topology fingerprints were computed from the deterministic seed `20260817` using the exact topology generators and fingerprint function in the committed codebase. The manifest SHA-256 was computed from the final text and verified by an independent Python computation and the side-car file.

**This manifest is not a protocol freeze. It is not pilot authorization. It does not authorize empirical data collection. N = 0 throughout. Pilot authorization is NOT GRANTED.**
