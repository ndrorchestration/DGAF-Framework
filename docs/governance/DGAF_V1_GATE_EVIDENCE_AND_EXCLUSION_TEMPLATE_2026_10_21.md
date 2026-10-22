# DGAF v1 release evidence and gate adjudication template

**Controller:** https://github.com/ndrorchestration/DGAF-Framework/issues/1421
**Status:** TEMPLATE ONLY / NO GATE ACCEPTANCE.
**Prerequisite:** bind every disposition to the frozen Gate 0 oracle version/hash; independent acceptance remains required before filing a PASS.

## Evidence record
- gate_id: G0|G1|G2|G3|G4|G5|G6|G7
- gate_criteria_version_and_sha256:
- support_envelope_and_action_class:
- exact_release_candidate_sha:
- implementation_owner:
- evidence_producer_identity:
- eligible_independent_verifier_identity:
- reviewer_relationship_conflict_disclosure:
- verifier_eligibility_adjudicator:
- acceptance_oracle_frozen_before_test:
- raw_evidence_uri_and_sha256:
- clean_environment_dependency_lock_identity:
- test_runtime_driver_and_version:
- observed_positive_cases:
- observed_negative_falsification_cases:
- test_failure_or_inconclusive_result:
- evidence_reproducibility:
- residual_risk_and_excluded_paths:
- reviewer_written_disposition: BLOCKED
- reviewer_signature_or_attributed_signoff:
- decision_date:
- upstream_issue_or_pr:
- downstream_claims_affected:

## Release blocker classification
- P0 critical: probable unauthorized consequential action, protected disclosure or
  unbounded trust bypass. Cannot self-close. Eligible independent confirmation required.
- P1 high: reproducible severe violation within advertised supported scope.
- P2 moderate: bounded defect with explicit mitigation and impact.
- P3 low: hygiene or non-consequential documentation defect.
This severity taxonomy is frozen with the Gate 0 oracle version. Severity application and release-blocker closure still require evidence and eligible independent adjudication.

## Exclusion reachability worksheet
- excluded_capability:
- runtime entry points and alternate routes:
- deployment and routing assumptions:
- disabled/removed source commit:
- direct negative execution test:
- indirect/alternate execution negative test:
- external policy/dependency gates:
- artifacts and raw result hashes:
- independent confirmation:
- disposition: BLOCKED

## Threat-model worksheet
- protected_asset:
- trust_boundary:
- adversary_capability_and_assumptions:
- environment_topology:
- secret_and_artifact_recipient_exposure:
- fault_model:
- attack/failure mode:
- denial oracle:
- tested evidence:
- untested assumptions:

No template field alone establishes acceptance; absent or conflicted evidence is
BLOCKED. Operator assertions do not become independent verifications.
