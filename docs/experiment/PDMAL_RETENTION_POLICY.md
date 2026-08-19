---
status: ACTIVE
authority: Both
owner: DGAF/PDMAL evidence control
last_verified: 2026-08-18
applies_to_sha: pending-next-verification-commit
state: POLICY DECIDED / IMPLEMENTATION SCOPE DEFINED
---

# PDMAL Artifact Retention Policy

## Policy decision

The project distinguishes **CI operational artifacts** from the **durable research record**.

### CI operational artifacts

GitHub Actions artifacts used for transient CI verification and runtime characterization use the repository's configured **30-day retention**. Examples include:

- contract-test manifests;
- runtime-characterization artifacts;
- temporary verification logs;
- checksums associated with those transient artifacts.

A 30-day CI retention period is not represented as permanent research archival.

### Durable freeze/research record

The durable record for protocol freeze consists of repository-controlled source, protocol, configuration, lockfile, freeze manifest, evidence index, artifact identifiers/digests, and authorization records.

The canonical raw empirical dataset, when eventually authorized and generated, must be copied before expiration to a separately approved durable research repository or institutional/object storage location. The location, identifier, access policy, checksum, and retention period must be recorded in the freeze manifest before pilot authorization.

## Access control

- CI artifacts: repository permissions and workflow artifact access controls.
- Freeze manifest and provenance: repository-controlled review/merge permissions.
- Raw empirical dataset: restricted research-data access; the analyst receives the approved blinded dataset according to the frozen custody procedure.
- Blinding mapping/key: separate protected custody; never stored with the analytical dataset.

## Deletion / expiration

Transient GitHub artifacts may expire after 30 days under platform retention policy.

Durable research artifacts must not be deleted during the declared retention period. Any later deletion requires a documented authorization and an updated provenance record.

## Freeze requirement

Before protocol freeze, the project must record:

```text
CI artifact retention: 30 days
Durable archive location: <approved repository/object store>
Durable archive identifier: <record ID / DOI / object ID>
Archive retention period: <explicit period>
Access-control owner: <role>
Integrity record: <SHA-256 / manifest digest>
```

This policy does not claim that a durable external archive already exists. The archive remains an implementation prerequisite before final pilot authorization.

## Evidence boundary

Documenting a retention policy is not evidence that the durable archive exists. The retention gate closes only when the stated durable storage and access arrangement has been implemented and directly verified.
