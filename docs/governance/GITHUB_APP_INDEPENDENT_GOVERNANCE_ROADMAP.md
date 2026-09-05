# GitHub App Independent Governance Plane — Roadmap

**Status:** POST-CLOSURE ARCHITECTURE TRACK / NON-BLOCKING  
**Purpose:** Explore a GitHub-native independent governance/evidence plane without interrupting the current PDMAL pre-freeze closure path.

## Program context

The project owner has joined the GitHub Developer Program. GitHub describes that program as open to individual developers and companies building integrations in development or production using the GitHub API and maintaining a support contact.

This membership is useful ecosystem context for DGAF's integration work. It is **not** GitHub endorsement, certification, partnership, security approval, scientific validation, or evidence that any DGAF/PDMAL gate is closed.

## Why this track exists

DGAF already relies heavily on GitHub-native control surfaces:

- protected branches and required checks;
- GitHub Actions workflow identity;
- exact run/job provenance;
- artifact IDs and SHA-256 digests;
- pull-request and issue control-state reconciliation;
- deployment-source binding;
- candidate-scoped evidence registries.

A dedicated GitHub App could move selected governance functions outside the repository's own workflow execution context. That separation could strengthen the distinction between **the system being evaluated** and **the system asserting whether its evidence is valid**.

## Candidate responsibilities

A future DGAF governance app may, subject to explicit design and security review:

1. Observe completed workflow runs and bind evidence to exact triggering run IDs rather than "latest matching" lookups.
2. Verify immutable tuples such as repository, workflow, run, head SHA, event, conclusion, artifact ID, artifact digest, candidate SHA, and deployment ID.
3. Publish narrowly scoped check runs representing governance/evidence state without treating CI health as scientific efficacy.
4. Detect stale candidate/SHA/deployment references in issues and control documents.
5. Maintain an append-only or externally durable evidence index whose authority is distinct from mutable repository prose.
6. Verify artifact-retention and independent-custody references without silently recreating missing evidence.
7. Enforce fail-closed transitions for freeze, authorization, unblinding, and empirical-count changes.
8. Provide repository-installation scoping so DGAF governance can eventually operate across multiple repositories without broad personal credentials.

## Security and epistemic requirements

Any implementation must:

- use least-privilege GitHub App permissions;
- separate read/verification capabilities from mutation capabilities wherever practical;
- never store or expose experimental blinding keys in repository-visible state;
- never fabricate credentials, evidence, deployment state, external-source text, or empirical results;
- distinguish deployment health, CI success, structural evidence, runtime evidence, custody evidence, and empirical evidence;
- preserve historical failed artifacts and superseded candidate records rather than rewriting history;
- bind every closure claim to explicit immutable provenance;
- require independent verification before final freeze acceptance;
- keep pilot authorization separate from freeze completion.

## Relationship to the current critical path

This track must **not** delay or replace the active closure sequence:

1. P4 real human/key custody and access separation.
2. P5 exact analysis implementation/configuration binding.
3. P7 final scientific identity binding.
4. P8 final pre-freeze analysis lock and immutable freeze construction.
5. Independent P9 verification.
6. Separate explicit pilot authorization.
7. Only then blinded empirical execution.

The GitHub App work should begin as architecture/specification work or a sandbox prototype after the current control-plane reconciliation is stable. It should not become a new reason to expand scope before the experiment's existing blockers are closed.

## Suggested phased implementation

### Phase A — specification only

- Define app trust boundary and threat model.
- Define exact GitHub permissions required.
- Define immutable evidence tuple schema.
- Define check-run state vocabulary: `PASS`, `FAIL`, `BLOCKED`, `SKIPPED`, `NOT_EXECUTED`, `UNKNOWN`.
- Define mutation policy and independent-verifier policy.

### Phase B — read-only verifier prototype

- Install only on a non-critical/sandbox repository first.
- Read workflow/run/artifact/check/deployment references.
- Produce a signed or digest-addressed reconciliation report without mutating source-of-record state.
- Adversarially test stale-run selection, wrong-SHA artifacts, expired artifacts, deployment drift, and contradictory documentation.

### Phase C — constrained governance checks

- Publish GitHub checks from verified evidence tuples.
- Keep issue/PR mutations disabled until the read-only verifier demonstrates deterministic behavior and fails closed under incomplete data.

### Phase D — controlled reconciliation

- Permit narrowly scoped issue/comment/control-state reconciliation.
- Require explicit provenance in every mutation.
- Preserve immutable history and support rollback/audit.

### Phase E — multi-repository governance plane

- Evaluate installation across DGAF ecosystem repositories only after single-repository behavior is stable and independently reviewed.

## Non-claims

This roadmap does not close P4, P5, P7, P8, or P9. It does not create a freeze, authorize a pilot, unblind conditions, increase empirical N, or establish GitHub endorsement of DGAF.

**Current experimental boundary remains: PRE-FREEZE / FAIL-CLOSED / NOT AUTHORIZED / N=0.**
