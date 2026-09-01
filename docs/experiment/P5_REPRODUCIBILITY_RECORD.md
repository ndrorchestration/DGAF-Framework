# P5 Reproducibility / Provenance Record — Candidate `45074856e82fc8e9c97153c41091c7fbc800d42c`

## Status

**VERIFIED for the controlled candidate.** This record is current-candidate evidence only; it does not authorize freeze, pilot execution, or production deployment.

## Evidence binding

- Candidate SHA: `45074856e82fc8e9c97153c41091c7fbc800d42c`
- Source workflow: `PDMAL Instrumentation Dry Run`
- Source run: `33558082367`
- Instrumentation artifact: `9820126686`
- Instrumentation artifact digest: `sha256:887fecad61ece397a0d4ce454a4fdd21a08745a7bb42e9a6b63e86187c78c1c0`
- Evidence-registry artifact: `9820128042`
- Evidence-registry digest: `sha256:adf32374797b9a9e78b7ebc80557f06058ba8b3a916ddd3f223523dbff8563f5`

## Reproducibility checks

1. **RNG stream separation:** `experiments/pdmal_topology/seeds.py` derives named streams from `pdmal-v1|<master_seed>|<stream>` using SHA-256, with distinct topology and failure streams used by the graph harness.
2. **Determinism:** the same seed/topology/failure-count case was executed twice in the source workflow and both JSON output and digest matched.
3. **Artifact integrity:** the masked one-seed artifact passed schema and checksum validation, was uploaded, downloaded again, and its inner CSV SHA-256 was recomputed and matched the recorded sidecar.
4. **Exact-candidate binding:** the evidence registry records the same candidate SHA, workflow run, artifact ID, and artifact digest used by the controller.

## Boundary

This closes **P5 reproducibility/provenance evidence for the controlled candidate** at the level established by the current dry-run apparatus. It does not claim production deployment provenance (P2), scientific freeze (P7), analysis lock (P8), or independent reconstruction (P9). Empirical execution remains unauthorized and empirical N remains zero.
