# PDMAL Blinding Custody and Separation-of-Duties Record

## Status

**PRE-FREEZE / BLINDING PRIMITIVE VERIFIED / OPERATIONAL CUSTODY NOT YET VERIFIED**

This record distinguishes the existence of the deterministic blinding primitive from operational custody of the secret, protected mapping, and unblinding event. It does not claim that those operational controls have already been exercised.

## Implemented blinding primitive

`experiments/pdmal_pilot/harness_contract.py` implements deterministic blinded identifiers with HMAC-SHA256:

```text
blind_condition(condition, key)
    -> blind_<first-16-hex-digest-characters>
```

The implementation accepts the blinding key as an argument and does not store the real secret in source. The pre-freeze contract tests use test-only keys. This establishes the deterministic transformation, not operational secret custody.

## Required operational roles

| Role | Required access boundary |
|---|---|
| Key holder | Controls the operational `PDMAL_BLINDING_KEY`; must not perform primary analysis. |
| Executor | Runs the experiment using blinded condition IDs; must not receive the key or protected mapping. |
| Analyst | Receives the blinded analytical dataset; must not receive the key or protected mapping before authorized unblinding. |
| Unblinder / panel chair | Controls the release of the protected mapping only after the pre-unblinding freeze conditions and authorization are satisfied. |

Role separation must be demonstrated operationally before protocol freeze. A written role definition alone is not evidence of access separation.

## Protected mapping mechanism

The experiment requires a real-condition-to-blinded-ID mapping to remain separate from the analytical dataset.

The repository must not contain the operational mapping or secret. The intended custody boundary is:

```text
Protected mapping object
        |
        +-- stored outside the Git repository
        +-- access limited to authorized key holder / unblinder custody
        +-- not uploaded as a normal experiment artifact
        +-- released only after the pre-unblinding freeze
```

The exact storage technology is **not yet designated as verified**. Before freeze, one approved mechanism must be selected and its access controls recorded. No encrypted-file, cloud-vault, or other mechanism is claimed here unless it is actually configured and tested.

## Unblinding procedure

Unblinding may occur only after all of the following are recorded:

1. raw observations are frozen;
2. artifact IDs and integrity hashes are recorded;
3. preprocessing rules are frozen;
4. exclusion decisions are frozen;
5. analysis code and analysis commit are frozen;
6. the analysis dataset is frozen;
7. integrity verification passes;
8. the panel chair records explicit authorization.

The unblinding record must contain, at minimum:

```text
unblinding event ID
timestamp
requester / authorizer
mapping custodian
experiment/protocol commit SHA
analysis-dataset freeze identifier
integrity verification result
reason for unblinding
```

The operational secret itself must never appear in the unblinding record.

## Access-control verification

Before freeze, verify separately that:

- the executor cannot read the operational key;
- the analyst cannot read the operational key;
- the executor cannot access the protected mapping;
- the analyst cannot access the protected mapping;
- the unblinder can access the mapping only under the documented authorization procedure;
- the repository contains no operational key or mapping artifact;
- CI logs and retained artifacts contain no key material.

A successful documentation review is insufficient; the access boundaries must be tested or otherwise evidenced through the actual custody system.

## Current evidence

| Control | Current status | Evidence boundary |
|---|---|---|
| Deterministic HMAC blinding primitive | **IMPLEMENTED / CI-VERIFIED** | `harness_contract.py` and test-only contract execution. |
| Operational secret excluded from source | **SUPPORTED BY IMPLEMENTATION** | The primitive receives the key; no secret value is committed. |
| Protected mapping stored separately | **NOT YET VERIFIED** | No protected mapping object is currently evidenced in the repository. |
| Role separation | **DOCUMENTED / NOT YET OPERATIONALLY VERIFIED** | Protocol and this record define roles; actual access controls remain to be tested. |
| Unblinding event record | **NOT YET IMPLEMENTED** | No operational event record has yet been evidenced. |
| Key rotation / custody test | **NOT YET VERIFIED** | No operational rotation or access-control test evidence yet retained. |

## Freeze criterion

The blinding-control gate can be marked **VERIFIED** only after the protected mapping mechanism, access boundaries, and authorized unblinding event procedure have been concretely configured and independently evidenced.

Until then:

```text
Blinding primitive:       VERIFIED/VALIDATED
Operational custody:      OPEN
Protocol freeze:          BLOCKED
Pilot authorization:     NOT GRANTED
```
