---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL evidence control
last_verified: 2026-08-21
applies_to_sha: CURRENT_MAIN_AT_VERIFICATION
state: POLICY ACTIVE / IMPLEMENTATION PRESENT / EVIDENCE OPEN
---

# PDMAL Artifact Retention Policy

## Policy decision

The project distinguishes CI operational artifacts from the durable research record.

### CI operational artifacts

GitHub Actions artifacts used for transient CI verification may use the repository's configured retention period. They are not represented as permanent research archival.

### Durable freeze/research record

The durable record consists of repository-controlled source, protocol, configuration, lockfile, freeze manifest, evidence index, artifact identifiers/digests, and authorization records. The canonical raw empirical dataset, when eventually authorized and generated, must be copied before transient CI expiration to a separately approved durable research repository or institutional/object storage location.

The repository now contains `experiments/pdmal_pilot/durable_retention.py`, which provides explicit archive-root configuration, SHA-256 computation, copy/archive, retrieval, and round-trip verification primitives. It does not itself prove that a production archive exists.

## Access control

- CI artifacts: repository permissions and workflow artifact access controls.
- Freeze manifest and provenance: repository-controlled review/merge permissions.
- Raw empirical dataset: restricted research-data access according to the frozen custody procedure.
- Blinding mapping/key: separate protected custody; never stored with the analytical dataset.

## Deletion / expiration

Transient CI artifacts may expire under platform retention policy.

Durable research artifacts must not be deleted during the declared retention period. Any later deletion requires documented authorization and an updated provenance record.

## Freeze requirement

Before final freeze and authorization, the project must record:

```text
Durable archive location: <approved repository/object store>
Durable archive identifier: <record ID / DOI / object ID>
Archive retention period: <explicit period>
Access-control owner: <role>
Integrity record: <SHA-256 / retention manifest digest>
Retention verification run: <run / audit identifier>
```

## Evidence boundary

Documenting the policy or committing the retention implementation is not evidence that a durable archive exists. The retention gate closes only after a real archive root is configured and a controlled write → retrieval → independently recomputed SHA verification succeeds.
