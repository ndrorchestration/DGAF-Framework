# AOSS v0.6 Stage-A independent validation handoff

Status: **PRE-VALIDATION HANDOFF ONLY**

Controller: #927

Protected-main identity at handoff preparation:

`054a300447627f3e87e92b24f16d261abc7d8d77`

External target identity:

- repository: `ndrorchestration/agent-control-plane`;
- frozen commit: `dbab7c1afafec524ce7c18157de2089cafe79c87`.

This document is intended for a reviewer who is operationally independent of
the DGAF implementation and who can return independently retained evidence.
Following this document does not itself establish reviewer independence,
external validation, execution readiness, canonical DGAF efficacy, or
High-Assurance authorization.

## 1. What DGAF may provide

DGAF may provide source locations, exact identities, frozen contracts,
non-secret candidate records, and instructions for reproducing the governed
checks. DGAF must not provide a pre-filled positive result, a required
conclusion, or an instruction to reinterpret fixture data as collected
outcomes.

The reviewer should obtain the repositories independently and verify the
identities below before relying on their contents.

## 2. Frozen Stage-A inputs

All paths below are bound to DGAF protected main
`054a300447627f3e87e92b24f16d261abc7d8d77`.

| Artifact | Repository path | Git blob identity |
|---|---|---|
| ACP measurement manifest | `registry/aoss_v0_6_acp_measurement_manifest_v1.json` | `1c690abbe2ab451f5081f56c25970eb85b031ce4` |
| analysis/multiplicity contract | `registry/aoss_v0_6_stage_a_analysis_multiplicity_contract_v1.json` | `8e95d00e6cc12f95336b004c75c3771ac7530bf6` |
| artifact/replay receipt contract | `registry/aoss_v0_6_stage_a_artifact_replay_receipt_contract_v1.json` | `1d2b44acb63f30660253e3c96f1a6cac602d62eb` |
| collection authorization | `registry/aoss_v0_6_stage_a_collection_authorization_v1.json` | `3a5efa22b99e03ef35bea71c261a4bcd681f0e6f` |
| decision policy | `registry/aoss_v0_6_stage_a_decision_policy_v1.json` | `b93f01af1825e93279e945f7dc07f299daab89bb` |
| environment manifest | `registry/aoss_v0_6_stage_a_environment_manifest_v1.json` | `d6d67fc4542d47e22f6f40503335c2e7580b405c` |
| episode eligibility/repetition | `registry/aoss_v0_6_stage_a_episode_eligibility_repetition_v1.json` | `f91735ae51b44921e78a50e9f6bb4486750ba96f` |
| executable/destination binding | `registry/aoss_v0_6_stage_a_executable_destination_binding_v1.json` | `80e7ea19a3da601b1a80c4d9c9e89c774f303814` |
| failure ground truth | `registry/aoss_v0_6_stage_a_failure_ground_truth_v1.json` | `02a393bf025df6dbd8bd0126a0626a31d832ee00` |
| freshness/calibration | `registry/aoss_v0_6_stage_a_freshness_calibration_v1.json` | `694ecec6c7214e5c4047f6d7de612513d176b740` |
| observer/measurement boundary | `registry/aoss_v0_6_stage_a_observer_measurement_boundary_v1.json` | `108dc570dd5dc1903e49a2b4afbf9a4eb3d604ce` |
| PolicyInput mapping | `registry/aoss_v0_6_stage_a_policy_input_mapping_v1.json` | `5948f0dbdbcf55e5e2d77a9e5f7cd14bb9e75a27` |
| practical-effect/adoption rule | `registry/aoss_v0_6_stage_a_practical_effect_adoption_rule_v1.json` | `4576366f839f80af1fcb1318a3a9ac69f90e7244` |
| pre-collection receipt | `registry/aoss_v0_6_stage_a_precollection_receipt_v1.json` | `99dea885164f02ed0bf77722fd9610529ce65582` |
| pre-data readiness | `registry/aoss_v0_6_stage_a_predata_readiness_v1.json` | `9592e0357d7b20baf4b64c0a05513fb5d68cb11d` |
| primary comparator amendment | `registry/aoss_v0_6_stage_a_primary_comparator_amendment_v1.json` | `aaf2a62399158dda0ffdc3006d6b7fbe64a1d0e8` |
| runtime binding | `registry/aoss_v0_6_stage_a_runtime_binding_v1.json` | `e5d13796fa43e6ffd77dc93313c03213d335efbc` |
| source-driver binding | `registry/aoss_v0_6_stage_a_source_driver_binding_v1.json` | `fcb1d3a810da8bf3b4708c08b7672829fde273c0` |
| source-driver recipe catalog | `registry/aoss_v0_6_stage_a_source_driver_recipe_catalog_v1.json` | `178471a6a871fec5d5a7a6349f6f439af8667284` |

The Git blob identities above are repository object identities, not SHA-256
content digests. Where a contract requires SHA-256, the reviewer must recompute
that SHA-256 from the exact retrieved bytes and record it independently.

## 3. Reviewer independence disclosure

Before reviewing substantive evidence, the reviewer should record:

- reviewer name or durable reviewer identifier;
- organization or affiliation, if any;
- relationship to the DGAF author/project;
- whether the reviewer authored, modified, or selected any DGAF Stage-A code,
  policy, analysis rule, test fixture, or outcome;
- whether the reviewer had access to Stage-A outcomes before completing the
  prospective identity/custody checks;
- any financial, employment, contractual, or collaborative relationship that
  could affect independence;
- a plain-language independence conclusion and its limitations.

DGAF must not classify the reviewer as independent on the reviewer's behalf.
The returned disclosure is evidence for later local adjudication.

## 4. Required independent verification procedure

The reviewer should perform the following from independently obtained source
copies.

1. Verify DGAF protected-main commit and every handoff artifact Git blob
   identity listed above.
2. Verify the ACP repository is checked out at
   `dbab7c1afafec524ce7c18157de2089cafe79c87` and that the study does not
   silently substitute another ACP revision.
3. Verify the frozen Stage-A episode-class set directly from the accepted
   measurement, eligibility, recipe-catalog, and ground-truth contracts. The
   expected study scope is the accepted 16-class Stage-A corpus, including the
   structural-rejection controls.
4. Verify the prospective runtime/interpreter/dependency identity and compare
   the observed installed environment with the accepted environment candidate.
   Observation is not acceptance; discrepancies must be reported.
5. Verify the exact source-driver/collector executable identity and its binding
   to the frozen ACP source and source-driver recipe catalog.
6. Verify the destination and prospective attempt identity existed before
   outcome inspection and are not fixture-only identities.
7. Verify ingest-time capture and the frozen freshness rules. The accepted
   apparatus uses a 30-second maximum age and 2-second maximum future skew;
   the reviewer must verify the controlling contract bytes rather than rely
   only on this prose summary.
8. Verify retained custody for exactly the required study, source, normalized,
   decision, and analysis bundles and independently recompute their SHA-256
   identities.
9. Verify exactly five read-only exact-byte replay passes and the required
   replay-verification booleans from the accepted replay contract.
10. Verify identity/hash/class drift invalidates the attempt and that retry is
    prohibited after outcome inspection.
11. Verify the external observer does not manufacture source authority,
    validation, or provenance that the ACP source does not expose.
12. Verify any reported Stage-A conclusion against the frozen analysis and
    practical-effect contracts without changing those contracts after seeing
    outcomes.

Any unresolved required identity, missing artifact, stale/future-skewed input,
unexpected class set, replay mismatch, or post-inspection retry should be
reported as a blocker rather than repaired silently.

## 5. Required returned evidence package

The reviewer should return an independently retained record containing, at
minimum:

```json
{
  "review_scope": "AOSS_V0_6_STAGE_A",
  "dgaf_commit": "<40-hex commit>",
  "acp_commit": "<40-hex commit>",
  "reviewer_identity": "<durable identity>",
  "reviewer_affiliation": "<string-or-null>",
  "relationship_disclosure": "<text>",
  "independence_finding": "VERIFIED|NOT_VERIFIED|BLOCKED",
  "review_started_at": "<offset-aware timestamp>",
  "review_completed_at": "<offset-aware timestamp>",
  "artifact_checks": [
    {
      "path": "<path-or-independent-uri>",
      "declared_identity": "<identity>",
      "observed_sha256": "<64-hex sha256>",
      "match": true
    }
  ],
  "installed_environment_finding": "ACCEPT|REJECT|BLOCKED",
  "source_driver_executable_finding": "ACCEPT|REJECT|BLOCKED",
  "destination_attempt_finding": "ACCEPT|REJECT|BLOCKED",
  "freshness_finding": "PASS|FAIL|BLOCKED",
  "custody_finding": "PASS|FAIL|BLOCKED",
  "five_replay_finding": "PASS|FAIL|BLOCKED",
  "no_retry_after_inspection_finding": "PASS|FAIL|BLOCKED",
  "limitations": ["<text>"],
  "record_sha256": "<64-hex sha256>",
  "signature_or_attestation": "<reference-or-null>"
}
```

The reviewer may use a richer schema, but omission of a consequential finding
must remain explicit rather than being inferred as PASS.

The review record and consequential evidence should be retained outside the
DGAF repository or in another independently controlled location when
practicable. Returned URIs should be immutable or content-addressed where
possible.

## 6. Claim ceiling

A positive review of Stage A may support claims only within the exact accepted
study and review scope. In particular:

- the Stage-A primary comparison is not, by itself, proof that DGAF or AOSS is
  generally correct or superior;
- exact-byte replay does not create independent experimental replications;
- reviewer independence is a separate evidentiary question from hash matching;
- a positive external report is not automatically a local acceptance event;
- Stage-A acceptance does not reopen Track A Epoch 002;
- canonical DGAF efficacy remains a separate claim;
- production certification and High-Assurance authorization remain separate
  governance programs.

Before an accepted local trust/execution-admission transition, the controlling
state remains:

```text
trust_promotion=NOT_EXECUTED
reviewer_attribution_verified=false
independence_verified=false
INSTALLED_ENVIRONMENT_ACCEPTANCE=NOT_ESTABLISHED
SOURCE_DRIVER_BINDING=NOT_ESTABLISHED
EXECUTABLE_ACCEPTANCE=NOT_ESTABLISHED
DESTINATION_ACCEPTANCE=NOT_ESTABLISHED
execution_allowed=false
COLLECTION_EXECUTION_READINESS=NOT_ESTABLISHED
SCIENTIFIC_N_INCREMENT=0
EXTERNAL_VALIDATION_ESTABLISHED=FALSE
CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED
INDEPENDENT_VALIDATION=NOT_ESTABLISHED
HIGH_ASSURANCE=NOT_AUTHORIZED
```

## 7. What completes this handoff phase

The handoff phase is complete when this document is accepted on protected main
and can be given to an external reviewer without additional undocumented
instructions.

That completion means only **independent validation is operationally
requestable**. It does not mean an independent review has occurred.
