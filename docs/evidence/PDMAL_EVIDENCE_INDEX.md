---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL control plane
last_verified: 2026-08-28
applies_to_sha: ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a
scope_note: >-
  This index records evidence and gate state. Historical evidence remains
  scoped to the exact SHA/run that produced it. Candidate verification does
  not inherit historical verification automatically.
---

# PDMAL Evidence Index

This is a control-plane registry, not empirical evidence and not a self-authorizing freeze record.

## Evidence inventory

| Evidence | State | Identity | Interpretation |
|---|---|---|---|
| Current repository lineage | CURRENT | `main` | Active documentation/evidence lineage; not experimental apparatus identity |
| Experimental verification boundary | CANDIDATE-SCOPED | `ac8ea267a9f0d995626cf9c3eaf9e6b008b5dc8a` | Current pre-freeze candidate verification boundary; later documentation commits do not inherit its evidence automatically |
| Historical implementation freeze | HISTORICAL / SUPERSEDED | `3510b86889cd341f7a7cf9ab684fd37b2fafd758` | Historical apparatus only |
| Corrected pilot runner | CANDIDATE | Current verification boundary | Exact candidate verification pending |
| TGL contract | BLOCKED / ADVERSARIAL REVIEW | PR #132 / PR #133 | 41-pass / 2-fail regression at TGL → P-35 seam; isolated contract-restoration remediation remains pending exact-head validation |
| Environment lock | VERIFY | Python 3.12.0; NumPy 2.5.1; NetworkX 3.6.1 | Fresh matching environment required |
| Runtime characterization | CLOSED FOR CHARACTERIZATION | Run `32112658368` | Operational characterization, not efficacy evidence |
| Blinding operational verification | CLOSED FOR SYNTHETIC VERIFICATION | Run `32113226935` | Synthetic custody only |
| Artifact contract | PARTIAL | `pilot_artifact_schema.py` + tests + inline runner enforcement | Fresh candidate CI/audit pending |
| Security controls | VERIFY | `test_security_controls.py` + pre-authorization workflow | Fresh CI pending |
| Topology provenance | VERIFY | `PDMAL_TOPOLOGY_FINGERPRINT_MANIFEST.md` | Recompute against exact freeze candidate |
| Durable retention | OPEN | Policy present; operational archive not established | Direct write/retrieval/hash evidence required |
| Primary contrast | ADJUDICATED / BINDING PENDING | `dgaf` vs `null`; FFCR; paired seed | Scientific target selected; exact freeze binding remains required |
| Analysis lock | OPEN / FAIL-CLOSED | `PDMAL_ANALYSIS_CONTROL_PLAN.md` / P8 lock | Candidate implementation/configuration SHA required |
| Independent verification | NOT EXECUTED | P9 audit design | Must verify candidate-scoped evidence |

## Runtime characterization provenance

Latest recorded reconciliation:

- Release ZIP SHA-256: `ba2d44016a9ef7f76546746bd03cd2964776e735ce4bbd5034d28f8cebee6f20`
- Inner `runtime_characterization.json` SHA-256: `42da11122cf4bca517d93888c946d26b31a8ae6b304433e56ae9c2f4c155f6ea`
- Run: `32112658368`
- Artifact: `9315467977`

These values supersede the older conflicting `f6db...` record in this registry. A fresh byte-level recomputation from the release asset should be performed before the final freeze packet when the asset is available.

## Evidence boundary

Historical acceptance, characterization, synthetic blinding, topology, and security evidence may establish engineering or operational properties. None establishes empirical PDMAL efficacy. Empirical N remains `0` until an explicitly authorized 50-seed pilot occurs.

## TGL/P-35 boundary

The TGL review is an implementation/governance control issue, not experimental evidence. PR #132 remains blocked/draft. Its 41-pass / 2-fail result is retained as a substantive regression signal. The isolated remediation candidate must pass its own exact-head validation before the execution-contract predicate can advance.

The remediation boundary does not create a freeze, authorize execution, close P7/P8, or increase empirical N.
