# P3 Artifact Contract — Current Candidate Attestation — 2026-09-05

**Status:** CURRENT-CANDIDATE CONTRACT VERIFIED  
**Candidate:** `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`  
**Candidate tree:** `586c00d6dedb589e52108279f9759be3c4f927e1`  
**Experimental boundary:** PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0

## Purpose

Record current-candidate execution evidence for P3 Artifact Contract. This attestation covers schema/identity/uniqueness/balance/canonical-matrix/deviation integrity using synthetic PRE-FREEZE fixtures only. It does not claim empirical validation and does not authorize pilot execution.

## Exact schema identity

| Contract surface | Candidate path | Git blob SHA | Schema version / scope |
|---|---|---|---|
| Canonical pre-freeze artifact validator | `experiments/pdmal_pilot/artifact_schema.py` | `41a90485246bbc1e7e13829fc1791133da5c3d4c` | `ARTIFACT_SCHEMA_VERSION = 1.0` |
| Authorized-pilot artifact integrity validator | `experiments/pdmal_pilot/pilot_artifact_schema.py` | `c620d3755a645c5f2ad14124f42ce07a1c670c5f` | `ARTIFACT_SCHEMA_VERSION = 1.0`; 4 conditions × 5 topologies × 9 failure levels = 180 records/seed |

Both files are read from the exact candidate `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`; this attestation does not transfer schema evidence from another candidate.

## Authoritative execution evidence

- Workflow: `PDMAL Pre-Freeze Runner Validation`
- Mainline run: `33939955138`
- Workflow/control-plane SHA: `821878759797d0bfda2ae7a8bced980bd02c58a9`
- Source artifact: `9961526468` (`pdmal-pre-freeze-contract-evidence`)
- Source ZIP SHA-256: `ed947f8a2f21a1e1122a6e8950240ea4a3ebdec7aad04c4231698de2f250285b`
- Source evidence JSON SHA-256: `d6b7c85a80a2ecf8e857431ab1b132d2dd703176cb481c0e67fbc0d067fe3175`
- Registry artifact: `9961526662` (`pdmal-pre-freeze-p3-p5-registry`)
- Registry ZIP SHA-256: `d7f592b45e76978600b6f1a4f22cac4b97dfe5f60605accbd99b61c50e149e93`

The source-bound registry records the candidate SHA/tree, producer run, workflow-definition SHA, source artifact ID/digest/content digest, and explicitly classifies GitHub Actions retention as non-durable custody. P6 durable custody is handled separately.

## Executed P3 assertions

Run `33939955138` completed successfully and passed:

- exact candidate checkout and tree verification;
- canonical pre-freeze artifact contract validation;
- required document and per-record field validation;
- PRE-FREEZE and `empirical_data_collection=false` enforcement;
- exclusion/exclusion-reason consistency;
- environment fingerprint requirements;
- deterministic SHA-256 sidecar validation;
- 180-record pilot artifact matrix contract fixtures;
- canonical topology/failure coordinate validation;
- four-condition balance/cardinality rules;
- duplicate-cell rejection;
- record/candidate identity and hash integrity;
- FFCR/recovery semantic checks;
- adversarial artifact-substitution/integrity rejection;
- unauthorized pilot fail-closed behavior.

The richer pilot-schema checks are fixture-only structural checks. No authorized pilot artifact or empirical observation was generated.

## P3 adjudication

The active P3 closure condition is retained candidate-scoped artifact-contract evidence covering schema, identity, uniqueness, balance, canonical matrix, and deviation integrity. Those requirements are now executed and retained against the exact designated candidate, with source/run/artifact provenance and durable-custody handling recorded separately.

**P3 result: CLOSED / VERIFIED for candidate `7c1cc4bb78025b21501b6f790bf55f4b5e3bbdc8`.**

## Explicit non-claims

- P3 verification is structural/contract evidence, not efficacy evidence.
- P4 human/key custody separation remains unestablished.
- P5 final analysis implementation/configuration binding remains open.
- P7/P8/P9 remain subject to their own prerequisites.
- Freeze is NOT ESTABLISHED.
- Pilot authorization is NOT GRANTED.
- Empirical N remains `0`.
