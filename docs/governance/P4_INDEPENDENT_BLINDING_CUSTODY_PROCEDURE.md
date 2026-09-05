# P4 Independent Blinding Custody Procedure

**Status:** CANONICAL PROCEDURE / NOT EXECUTED / P4 REMAINS OPEN  
**Authority:** DGAF/PDMAL pre-freeze governance  
**Supersedes as canonical procedure:** `P4_HUMAN_KEY_CUSTODY_PROCEDURE.md`  
**Architecture correction:** Issue #285 — COMPLETED via PR #286 / merge `a3bafa6fca8599df479a685828f5fdddb6bae589`  
**Active Mode-T design/threat-model lane:** Issue #287 — OPEN / DESIGN ONLY  
**Purpose:** Define the minimum pre-execution custody, access-separation, commitment, release-control, and audit evidence required before P4 Security / Blinding may be considered for closure.

## Governing invariant

P4 is about **effective control separation**, not social relationship or headcount.

Before the predeclared release condition, the execution/analysis principal must be unable to obtain the raw blinding key, cleartext condition mapping, commitment nonces, or functionally equivalent recovery material by unilateral action through any ordinary, administrative, recovery, backup, policy-edit, credential-reset, export, or break-glass path.

If the execution/analysis principal can defeat the separation alone, P4-A is not satisfied even if the key is stored in a different product, account, repository secret, vault, machine, or AI-mediated workflow.

Passing synthetic mock-key tests, storing a repository secret, seeing a successful workflow, proving that code supports blinding, or preregistering the analysis plan does **not** establish P4-A.

## Acceptable custody modes

Exactly one custody mode must be selected and evidenced for a P4-A execution instance.

### Mode H — distinct-human custody

A genuinely distinct human Key Custodian creates or receives the real blinding key and cleartext condition mapping and does not provide them to the execution/analysis principal before authorized release.

This is the existing human-custody model and remains fully acceptable.

### Mode I — institutional / third-party custody

An external organization or service controls the blinding secret and release path under terms or access controls that the execution/analysis principal cannot unilaterally override.

Evidence must identify the service/organization, custody policy class, release rule, administrative/recovery model, and the specific reason the analyst cannot independently recover or reconfigure access.

A service account owned and fully administered by the analyst does not become independent merely because the infrastructure belongs to a third party.

### Mode T — independently enforced technical custody

A cryptographic, HSM, KMS, threshold, time/release-gated, or equivalent technical mechanism may satisfy P4-A only when its effective control model prevents the execution/analysis principal from unilaterally recovering, exporting, remapping, decrypting, rekeying, policy-editing, or prematurely releasing the protected material.

Mode T requires an explicit control-path inventory covering at least:

- owner/administrator privileges;
- policy and IAM modification;
- credential reset or account recovery;
- backup/restore paths;
- key export or re-encryption paths;
- break-glass/emergency access;
- alternate root/service credentials;
- support/provider override paths known to the operator; and
- any local copy, escrow, recovery phrase, seed, token, or backup that restores effective access.

If the analyst controls any path that can restore the mapping or secret before authorized release, Mode T fails closed.

### Current Mode-T implementation boundary

Mode T is an **admissible control class**, not a claim that a specific zero-human implementation already satisfies P4.

No solo Mode-T implementation has been accepted or executed. Issue #287 evaluates a possible lifecycle in which secret material is generated only inside an authorized transient execution environment and timelock-released after an analysis-lock deadline. That proposal may require a future mode-specific P4/P7/P8/P9 lifecycle revision because the current universal predicates bind real key/mapping commitments pre-freeze.

Until such a revision is separately reviewed, merged, and verified, this canonical procedure remains controlling as written. The existence of Issue #287, GitHub-hosted runners, drand/timelock tooling, HSM/KMS products, or any other proposed mechanism does **not** close P4 or establish sufficient independence.

## Explicit non-substitutes

The following do not satisfy P4-A by themselves:

- a GitHub/CI/repository secret controlled by the same repository operator;
- a password-manager vault whose owner or recovery path is controlled by the analyst;
- a second account, alias, pseudonym, bot, AI agent, persona, or automation controlled by the same person;
- ordinary encryption when the analyst possesses the decryption key or recovery capability;
- a cloud KMS/HSM when the analyst can change IAM/policy, invoke export/decrypt, recover the owner account, or use a break-glass path;
- a hash of an enumerable mapping without a secret nonce;
- preregistration or timestamping alone.

Preregistration is complementary evidence against outcome-dependent redesign. It is not a substitute for blinding custody.

## Key and mapping commitments

A plain unsalted SHA-256 hash of the condition mapping is **not acceptable**. With four canonical conditions there are only 24 possible bijections, so an unsalted public mapping hash could be brute-forced.

Generate independent cryptographically secure random nonces of at least 32 bytes:

- `key_commitment_nonce`
- `mapping_commitment_nonce`

Use deterministic canonical encodings and domain separation:

```text
key_commitment_sha256 = SHA256(
  b"DGAF-P4-KEY-v1\x00" || key_commitment_nonce || raw_blinding_key
)

mapping_commitment_sha256 = SHA256(
  b"DGAF-P4-MAP-v1\x00" || mapping_commitment_nonce || canonical_mapping_bytes
)
```

The public pre-execution record contains only the resulting digests, never the raw key, cleartext mapping, or unreleased nonces.

The canonical mapping encoding remains UTF-8 canonical JSON with sorted object keys, no insignificant whitespace, blinded identifiers as keys, and canonical condition names as values. No outcome information may enter the commitment input.

## P4-A — pre-execution custody closure

P4-A is the upstream custody gate consumed by P7/P8/P9. P4-A may be considered for closure only when all applicable evidence exists **before** freeze, authorization, empirical execution, or unblinding.

### Universal predicates

Every custody mode must establish:

1. **Custody mode identity** — `H`, `I`, or `T` and an exact custody-instance identifier.
2. **Execution/analysis principal identity** — attributable identity of the person or role that will inspect blinded outputs.
3. **Protected-material scope** — raw key, cleartext mapping, commitment nonces, and equivalent recovery material are enumerated.
4. **Key commitment** — domain-separated nonce-hardened commitment created before empirical execution.
5. **Mapping commitment** — domain-separated nonce-hardened commitment created before empirical execution.
6. **Release rule** — predeclared condition under which the mapping may become available.
7. **Timestamp ordering** — custody assignment, commitments, and release rule predate any empirical execution.
8. **Control-path inventory** — all ordinary/admin/recovery/backup/export/break-glass paths relevant to early recovery are documented in non-secret form.
9. **No-unilateral-access evidence** — evidence supports the claim that the execution/analysis principal cannot use any inventoried path alone to recover protected material before release.
10. **Evidence provenance/integrity** — retained packet identity/digest and reviewable history.
11. **Contradiction check** — no known access record, credential, copy, or control path contradicts the separation claim.
12. **Independent review** — a reviewer, auditable external control, or independently inspectable technical evidence verifies the custody claim without exposing secret material.
13. **Mode-specific evidence** — evidence appropriate to the selected H/I/T path is retained under one exact SHA-256 identity.

### Mode-specific predicates

**Mode H** additionally requires attributable custodian and execution/analysis no-access attestations and evidence that the two principals are genuinely distinct humans.

**Mode I** additionally requires attributable external service/organization identity, custody/release-policy evidence, and evidence that the analyst cannot unilaterally administer or recover the custody function.

**Mode T** additionally requires machine-verifiable or independently inspectable evidence for the relevant policy/configuration and explicit proof that analyst-controlled administrator/recovery/export paths are absent. A configuration screenshot or declarative policy alone is insufficient if an unexamined owner/recovery path still exists.

## Independent review standard

"Independent" does not necessarily mean a second human for Mode I or Mode T. It means the closure claim is not accepted solely because the execution/analysis principal asserts it.

Acceptable review evidence may include a distinct human reviewer, provider-generated immutable audit/configuration evidence, cryptographically verifiable access policy, threshold-control evidence, or another mechanism whose correctness can be checked without granting the analyst the protected material.

Where the reviewer and operator are the same person, the underlying enforcement must itself be external to that person's unilateral control and independently inspectable. Self-authored prose is never sufficient.

## Evidence identities bound into P7 and final P9

At P4-A closure, the retained evidence packet must yield exact non-secret values for:

- `p4_custody_mode`
- `p4_custody_instance_id`
- `p4_custody_authority_id`
- `p4_execution_principal_id`
- `p4_key_commitment_sha256`
- `p4_mapping_commitment_sha256`
- `p4_control_path_inventory_sha256`
- `p4_no_unilateral_access_evidence_sha256`
- `p4_independent_review_evidence_sha256`
- `p4_mode_evidence_sha256`

Closed P7 binds those values before freeze. The immutable freeze copies them into its `p4_custody` object, and final P9 requires exact equality between the freeze and P7. This prevents a custody mode or evidence packet from being substituted after P7 closes.

P9 verifies identity consistency and fail-closed state. It does not magically prove that an external system is independent from its name alone; the retained P4 evidence remains responsible for establishing the actual access-control claim.

## P4-B — post-unblinding custody continuity audit

P4-B occurs only after separately authorized blinded execution and unblinding. It appends evidence to the historical P4-A record; it does not rewrite or retroactively manufacture P4-A closure.

P4-B must retain, as applicable:

- evidence that the authorized runtime used the custody object associated with the recorded commitment;
- release authorization and attributable/auditable release timestamp;
- released mapping plus nonce and exact recomputation of the pre-execution mapping commitment;
- controlled key-continuity verification when required by the frozen protocol;
- custody-policy or access-log evidence covering the blinded period;
- any adopted destruction attestation; and
- any custody exception, override, contradiction, or breach.

A failed or contradictory P4-B audit can invalidate downstream scientific interpretation while the historical P4-A record remains immutable as a statement of what was established pre-execution.

## Release and continuity verification

At authorized unblinding:

- release the cleartext mapping and `mapping_commitment_nonce` through the predeclared release path;
- independently recompute `mapping_commitment_sha256` using the frozen canonical encoding;
- require exact equality with the pre-execution published commitment;
- record the verification result and timestamp.

The raw blinding key need not become public. If key continuity must be independently verified, controlled verification may recompute `key_commitment_sha256` without publishing the raw secret.

## Freeze and authorization ordering

The mandatory order remains:

1. candidate, protocol, analysis, and runner identities selected;
2. custody mode and custody instance selected;
3. protected material created and custody enforced;
4. commitment digests and non-secret custody evidence published;
5. P4-A independently reviewed and closed;
6. P7 final exact binding closed;
7. immutable freeze created and independently verified;
8. final P9 verification completed;
9. separate pilot authorization granted;
10. blinded empirical execution begins;
11. unblinding occurs only under the predeclared release rule;
12. P4-B continuity evidence is appended.

Neither custody setup, preregistration, green CI, nor freeze verification is pilot authorization.

## Public execution-record schema

Suggested machine-readable fields:

```yaml
p4_custody_version: "2"
record_type: "execution-instance"
status: "OPEN"
experiment_id: "PDMAL-PILOT-V1"
custody_mode: null  # H | I | T
custody_instance_id: null
execution_principal_id: null
custody_authority_id: null
custody_system_class: null
commitment_scheme: "sha256-domain-separated-secret-nonce-v1"
key_commitment_sha256: null
mapping_commitment_sha256: null
control_path_inventory_sha256: null
no_unilateral_access_evidence_sha256: null
independent_review_evidence_sha256: null
mode_evidence_sha256: null
custody_assigned_at: null
release_rule: null
release_rule_committed_at: null
freeze_id: null
pilot_authorization_id: null
empirical_execution_started_at: null
unblinding_authorization_id: null
unblinding_released_at: null
p4_status: "OPEN"
```

Fields corresponding to events that have not occurred remain null. The public record must never contain the raw key, pre-unblinding cleartext mapping, unreleased commitment nonces, recovery seeds, or equivalent secret recovery material.

## P4-A closure rule

P4-A may be `CLOSED / VERIFIED (PRE-EXECUTION CUSTODY)` only if the evidence supports the governing invariant for the selected custody mode.

If any required path is unexamined, any unilateral override remains available, any secret/recovery material is exposed to the analyst, or the evidence depends only on the analyst's assertion, P4-A remains **OPEN / BLOCKED**.

P7/P8/P9 consume only P4-A pre-execution closure. They must not require P4-B evidence that can exist only after pilot execution or unblinding.

## Failure and exception handling

Any of the following fails closed:

- protected material exposed to the blinded analyst before authorized release;
- analyst retains owner/admin/recovery/export/break-glass capability that defeats the selected custody mode;
- a same-operator account, AI agent, persona, repository secret, or ordinary vault is represented as independent custody without effective control separation;
- commitment created only after outcomes are available;
- missing or contradictory custody timestamps;
- incomplete control-path inventory;
- mapping commitment cannot be reproduced at authorized release;
- evidence packet altered without preserved history;
- release occurs outside the predeclared rule; or
- a later audit reveals an unrecorded unilateral recovery path that existed during the blinded period.

A failed custody attempt remains historical evidence. A replacement requires a new custody-instance identifier and fresh commitments where required; the failed record is never overwritten.

## Relationship to CI

CI may verify schema, completeness, timestamp syntax, digest formatting, candidate identity, deterministic canonicalization, commitment recomputation on synthetic fixtures, required documentation language, P7/freeze/P9 identity consistency, and fail-closed state transitions.

CI cannot by itself prove an external service's real access model or the absence of every off-platform recovery path. The closure packet must therefore include evidence appropriate to the selected custody mode.
