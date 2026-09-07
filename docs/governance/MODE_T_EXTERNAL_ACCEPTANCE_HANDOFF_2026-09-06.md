# Mode-T External Acceptance Handoff — 2026-09-06

## Status and authority boundary

Status: **SOURCE-BOUND HANDOFF / EXTERNAL OUTPUTS NOT EXECUTED / NOT AUTHORIZATION / NOT P4 CLOSURE**

Review base:

- repository: `ndrorchestration/DGAF-Framework`
- commit: `62e01c37e6e452e0851aa875fa6c709f049be991`
- tree: `f5ac41ccddc785f3e3e52a3c91daeb4513bccc20`

The machine-readable source and status manifest is `docs/governance/mode_t_external_acceptance_manifest.json`. The manifest is deliberately fail-closed: all four external tracks remain `NOT_EXECUTED`, final candidate remains `NOT_DESIGNATED`, P4 remains `OPEN_FAIL_CLOSED`, freeze remains `NOT_ESTABLISHED`, authorization remains `NOT_GRANTED`, and empirical N remains `0`.

This packet consolidates the evidence an external reviewer/operator needs without creating a new signer, verifier, custody mechanism, authorization authority, or evidence store.

## Why this handoff exists

Current repository engineering has substantial synthetic/read-only coverage, but the remaining P4 predicates cross trust boundaries that the repository cannot self-certify:

1. Issue #320 requires genuinely independent security review of the Google OIDC verifier and its Confidential Space claim-policy integration.
2. Issue #316 requires independently retained and independently re-verifiable production R/A/C plus admission-policy authority, final signer/retention authority, and approved/frozen production TrustedRoot/TUF semantics.
3. Issue #310 requires a real authenticated Confidential Space admission exercise with synthetic fixtures and independently reverified PRE/POST evidence.
4. Issue #295 requires the eventual protected continuity packet, independent retention/retrieval/re-hash, and final independent adjudication.

The repository already has dedicated mechanisms for the bounded engineering parts. This packet is a routing and identity-binding surface only.

## Non-circular sequencing rule

The P4 path has two distinct stages. They must not be collapsed.

### Stage A — apparatus qualification before final-candidate designation

Before Issue #309 designates the final v0.7.6 candidate:

- complete the independent #320 source/security review against the exact reviewed implementation blobs;
- resolve candidate-relevant #316 authority decisions, including the production retention/signing authority and production TrustedRoot/TUF bootstrap/update/validity policy;
- where useful, perform a real Confidential Space **synthetic-only qualification run** against an exact reviewed workload image/configuration to test the substrate and evidence path;
- treat any qualification finding that requires code, policy, image, toolchain, or launch-contract changes as apparatus work that must be integrated before final-candidate designation.

A Stage-A real run is **qualification evidence only**. It cannot close final P4 because the final candidate does not yet exist.

### Candidate designation — Issue #309

After candidate-relevant apparatus choices are settled, explicitly designate one exact immutable v0.7.6-descended candidate SHA/tree under Issue #309. Repository recency alone does not confer candidate authority.

### Stage B — final candidate-bound P4 acceptance

After final-candidate designation and before final P7/freeze:

- bind the accepted #316 production authorization capability and admission policy to the exact final candidate and exact pre-freeze execution contract;
- perform/reperform the real #310 Confidential Space PRE/POST admission on the exact final-candidate workload identity;
- independently retrieve and reverify the accepted evidence;
- adjudicate P4 against the exact final-candidate evidence.

Only after final P4 acceptance may the sequence advance to final P7 binding, immutable freeze F, P8 independent freeze verification, final P9, separate authorization, and empirical execution.

## Freeze-F semantic correction

Immutable freeze **F does not exist during P4 qualification or final P4 acceptance**. Freeze F is created later, after final P4 and final P7 binding.

Therefore:

- P4 must bind the exact candidate plus an exact **pre-freeze execution-contract identity**, not a future freeze-F digest;
- any current synthetic Mode-T fixture field named `freeze_sha256` or `freeze_commit_sha` is a historical **synthetic pre-freeze fixture identifier** only;
- those fixture fields must never be represented as an actual immutable freeze F, because the same synthetic records explicitly retain `freeze_established=false`;
- before a real production admission path consumes that schema, the execution contract must make the pre-freeze role explicit and must not require a nonexistent future freeze F.

This clarification does not modify the later P8/P9 use of actual freeze identities. Actual `freeze_sha256` in the final frozen-chain verification path remains a distinct downstream concept.

## Exact reviewed source set

The machine-readable manifest pins the source identities. Load-bearing current blobs at the review base include:

| Role | Path | Git blob |
| --- | --- | --- |
| Control state | `docs/experiment/PDMAL_CURRENT_CONTROL_STATE.md` | `c6dca09ed6415c2a260f21b40c32067a1e4bce26` |
| Google OIDC verifier | `experiments/pdmal_pilot/mode_t_google_oidc_verifier.py` | `7085d4c710c29821ade07304e3128ae9d8ef8dbf` |
| Confidential Space claim contract | `experiments/pdmal_pilot/mode_t_confidential_space_attestation.py` | `622bfe88116162937f4a3e6993ec66075fceb72e` |
| Admission policy | `experiments/pdmal_pilot/mode_t_admission_policy.py` | `520cd7dab7c0cb4c04c120007f84e05463243eb8` |
| Strict post-release verifier | `experiments/pdmal_pilot/mode_t_strict_verifier.go` | `1ad1e161f0fabcf7ee20ebfaff6d78675e2fb5aa` |
| Continuity acceptance binding | `experiments/pdmal_pilot/mode_t_continuity_acceptance.py` | `fa33309cac0906f0c73360fbea773f4a04f00668` |
| Retention contract | `experiments/pdmal_pilot/mode_t_retention_contract.py` | `eed870e75912cbf979f9835e0272acd1747dabc9` |
| Claim-coverage review scaffold | `docs/governance/MODE_T_CONFIDENTIAL_SPACE_CLAIM_COVERAGE_2026-09-06.md` | `1e55207292f450862eb69f81075201ec098f66e5` |
| Retention governance contract | `docs/governance/P4_MODE_T_RETENTION_CONTRACT_2026-09-06.md` | `c0f37831be744de7055265f1b618f3a8bffeda1e` |
| Continuity governance contract | `docs/governance/P4_B_MODE_T_CONTINUITY_ACCEPTANCE_CONTRACT_2026-09-06.md` | `b956c0a451013fdeff9ac9ab61effa14a9bc350a` |

The source-bound #340/#341 claim-coverage review remains current while these reviewed source blobs and relevant policy semantics remain unchanged. The packet does not convert that repository-authored review scaffold into the independent review required by #320.

## External output A — Issue #320 independent security review

Required reviewer output must record:

- exact reviewed repository SHA/tree and exact reviewed blobs;
- reviewer identity/provenance sufficient for independent attribution;
- findings with severity, evidence, and recommended remediation;
- explicit treatment of discovery/JWKS authenticity, TLS/redirect behavior, issuer/JWKS consistency, algorithm policy, `kid` rotation/cache behavior, JWT-supplied key-source headers, RSA/JWK validation, time handling, parser/DoS edge cases, and dependency assumptions;
- explicit review of the #340/#341 open claim decisions, including TDX TCB status/date, GCE subclaims, `swversion`, image identifiers/reference, image-signature authority, and the `jti` documentation/discovery consistency question;
- final disposition per finding: resolved, accepted-with-rationale, blocked, or unknown.

Repository-authored tests, this handoff, and the #340/#341 matrix are inputs, not independent conclusions.

Current output status: **NOT EXECUTED**.

## External output B — Issue #316 production R/A/C and trust authority

Required output must establish, at minimum:

- a production R/A/C plus admission-policy capability retained outside caller assertion;
- independent retrieval and cryptographic reverification of that retained authority;
- final signer/retention authority identity;
- independently approved/frozen production TrustedRoot bytes and digest;
- explicit TUF bootstrap/update/expiry/rotation policy;
- production key acquisition consuming the accepted retained capability before entropy generation;
- exact binding from retained policy authority into PRE/POST lineage;
- fail-closed behavior for missing, stale, substituted, or synthetic-only retention evidence.

Current output status: **NOT EXECUTED**.

## External output C — Issue #310 real Confidential Space admission

A Stage-A qualification run and the later Stage-B final-candidate acceptance must be distinguished in the retained record.

For any real run, independently establish:

- exact project/zone/VM/service-account and resolved VM subject;
- exact digest-pinned workload and independently reviewed launch policy;
- TDX, Secure Boot, production/non-debug Confidential Space state, accepted support attributes, disabled memory monitoring, `Never` restart policy, and no unreviewed command/environment override;
- Google token signature/key-source verification before claim admission;
- PRE token binding to exact C;
- in-process ≥256-bit CSPRNG operational key with no operator-visible secret input/output surface;
- POST token binding to the exact emitted output/evidence manifest;
- PRE/POST runtime-identity equality and distinct ordered tokens;
- independent retrieval/reverification of retained admission evidence.

Current Stage-A real qualification status: **NOT EXECUTED**.

Current Stage-B final-candidate acceptance status: **NOT EXECUTED**.

## External output D — Issue #295 protected continuity acceptance

After the accepted protected ciphertext and expected plaintext commitment exist, instantiate the existing structural packet with:

- exact candidate/repository/control-plane/helper/tool identities;
- exact protected ciphertext and expected plaintext-commitment identities;
- exact continuity run ID/attempt and report digest;
- strict-chain and non-leakage results;
- accepted independent retention/retrieval/re-hash evidence;
- distinct producer/retrieval actor provenance;
- final independent review/adjudication performed outside the producing packet.

The existing structural validator can return only `PASS_STRUCTURAL_BINDING_ONLY`; it cannot self-adjudicate final acceptance.

Current output status: **NOT EXECUTED**.

## Machine validation

`scripts/validate_mode_t_external_acceptance_manifest.py` verifies that:

- the handoff manifest has a closed schema;
- all source Git blobs match the immutable review-base tree;
- the review base is an ancestor of the tested handoff head;
- all four external tracks remain `NOT_EXECUTED`;
- final candidate remains `NOT_DESIGNATED` under tracker #309;
- P4/P8 remain fail-closed and final P9 remains unexecuted;
- freeze and authorization remain absent;
- empirical N remains zero;
- the packet cannot label itself authorization, independent review, real custody evidence, candidate designation, or empirical promotion.

A validator PASS is only handoff-integrity evidence.

## Non-effects

This handoff does not:

- perform or simulate #320 independent review;
- create production R/A/C retention or signer/root authority;
- execute a real Confidential Space workload;
- instantiate final protected continuity evidence;
- close P4;
- designate the final v0.7.6 candidate;
- close final P7/P8/P9;
- create immutable freeze F;
- grant authorization;
- execute or unblind empirical work;
- increase empirical N.

**Final candidate NOT DESIGNATED · P4 OPEN / FAIL-CLOSED · P7 final binding OPEN · P8 OPEN / FAIL-CLOSED · final P9 NOT EXECUTED · PRE-FREEZE · NOT AUTHORIZED · empirical N=0.**
