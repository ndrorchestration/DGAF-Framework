# P4 Mode T Transparency / Anti-Deletion Evidence Design — 2026-09-05

**Status:** DESIGN / NOT EXECUTED / NOT YET CANONICAL  
**Issue:** #287  
**Scientific boundary:** PRE-FREEZE · FAIL-CLOSED · NOT AUTHORIZED · empirical N=0.

## Problem

The existing PDMAL durable-retention primitive verifies archive copy/retrieval/hash equality against a configured archive root. That is useful for byte preservation, but it does not itself prove that an operator cannot delete or suppress a run record.

GitHub separately documents that users with write access can delete workflow runs and logs. Mode T therefore needs an anti-deletion/transparency layer for the evidence used to prove:

- which exact run was reserved;
- which exact run was authorized;
- that authorization was consumed before any protected material existed;
- that secret instantiation occurred only in the authorized attempt;
- that primary analysis was locked before the timelock release;
- that no extra accepted execution can be silently hidden by deleting GitHub history.

## Candidate transparency mechanism: Sigstore / Rekor

Sigstore documents Rekor as an immutable, append-only transparency log. Its security documentation states that entries cannot later be modified or removed from a valid monitored log, and that an entry can establish that a signed artifact existed prior to a logged time. Cosign can sign ordinary blobs and return a bundle containing the signature, certificate, timestamp and transparency-log inclusion proof.

Sources:

- [Sigstore documentation](https://docs.sigstore.dev/)
- [Rekor overview](https://docs.sigstore.dev/logging/overview/)
- [Sigstore security model](https://docs.sigstore.dev/about/security/)
- [Cosign quickstart](https://docs.sigstore.dev/quickstart/quickstart-cosign/)
- [Signing blobs](https://docs.sigstore.dev/cosign/signing/signing_with_blobs/)
- [GitHub Actions CI quickstart](https://docs.sigstore.dev/quickstart/quickstart-ci/)

This is a **candidate design**, not an assertion that Sigstore is automatically sufficient for P4/P6.

## Record sequence

### R — run reservation transparency record

Before any secret generation, the frozen runner creates canonical public JSON containing only:

```yaml
record_type: PDMAL_MODE_T_RUN_RESERVATION
freeze_sha256: <exact frozen bytes digest>
github_run_id: <exact run ID>
github_run_attempt: 1
github_sha: <frozen execution SHA>
workflow_sha256: <frozen workflow digest>
helper_sha256: <frozen helper digest>
reserved_at_github_metadata: <non-authoritative GitHub metadata>
secret_instantiation_status: NOT_EXECUTED
```

The record is keylessly signed from the frozen GitHub Actions workflow and submitted to the production Rekor transparency log. The returned Sigstore bundle/inclusion proof is retained through the ordinary P6 archive as a second copy.

No protected material exists yet.

### A — exact-run authorization

A separate authorization record binds exactly:

- freeze identity;
- reservation record digest;
- Rekor inclusion/bundle identity;
- exact `github_run_id`;
- `allowed_run_attempt: 1`;
- expiration/failure policy;
- authorization identity.

The same run may proceed only after it retrieves and verifies the authorization record plus its own R transparency evidence.

A different run ID or attempt fails before secret generation.

### C — authorization-consumption transparency record

After the reserved run verifies A but **before any key, mapping, or commitment nonce is generated**, it must publish a single-use consumption record:

```yaml
record_type: PDMAL_MODE_T_AUTHORIZATION_CONSUMPTION
reservation_sha256: <R canonical-record digest>
authorization_sha256: <A canonical-record digest>
freeze_sha256: <exact frozen bytes digest>
github_run_id: <exact reserved run ID>
github_run_attempt: 1
secret_instantiation_status: NOT_EXECUTED
```

C is signed/logged to Rekor and independently retained before P4-T-X begins.

The frozen rule is strict: **one authorization may have at most one accepted C record**. Once C exists, that authorization is consumed even if the runner later crashes before producing a blinded dataset or X record. A replacement execution requires a new custody instance and a new explicit authorization decision; it cannot silently retry the consumed authorization.

This closes a crash-window ambiguity in which a first run could generate protected material, fail before X publication, and then be replaced by a second apparently legitimate execution.

### X — execution / ciphertext transparency record

Only after C is verified as published may P4-T-X generate protected material. After execution, emit only non-secret evidence:

- exact R/A/C identities;
- key/mapping commitment digests;
- timelock chain/release round;
- ciphertext digest;
- blinded-dataset digest;
- leak-scan result;
- execution completion classification.

Sign/log that public evidence to Rekor and archive the bundle. The real key/mapping/nonces remain only inside the timelocked ciphertext and transient process memory.

### L — primary-analysis lock transparency record

Before the selected drand release round, the frozen primary-analysis workflow creates canonical public JSON containing:

- R/A/C/X identities;
- blinded dataset digest;
- exact analysis implementation/config identities;
- primary result digest;
- selected drand chain hash and release round.

The analysis-lock record is keylessly signed and entered into Rekor.

P4-T-L is valid only if the independently verifiable Rekor integration time for L is **strictly earlier** than the deterministic release time for the frozen drand round.

A payload-supplied timestamp is not sufficient.

## Why this improves the design

### GitHub deletion no longer erases the only evidence

A repository writer can delete GitHub Actions run/log records, but a valid Rekor entry is designed to be append-only and externally auditable. Deleting GitHub history therefore cannot erase an already-published R/C/X/L transparency event.

### Backdating the primary analysis becomes harder

The analyst cannot make a post-release analysis become pre-release merely by writing an earlier timestamp into the payload. The verifier uses the transparency-log integration evidence, not the self-asserted payload time, and compares it to the deterministic drand release round/time.

### Duplicate or crashed executions become externally visible

Every exact frozen run must publish R before it can consume authorization, and every authorization must publish C before secret generation. Final review rejects a lineage containing more than one C for one authorization. A crash after C is therefore visible as a consumed-but-invalid execution rather than becoming an invisible reason to retry.

Multiple R records may exist only if the frozen policy classifies the extras as pre-authorization/pre-consumption aborts and proves that no C exists for them. There is no retry after C under the same authorization.

## GitHub OIDC identity constraint

Sigstore's GitHub Actions examples use the OIDC issuer `https://token.actions.githubusercontent.com` and verify workflow identities in the form `https://github.com/OWNER/REPOSITORY/.github/workflows/WORKFLOW@refs/...`.

The transparency signature identity is therefore another bound input, not a substitute for the frozen repository SHA/workflow digest contained in the signed record.

The verifier must check both:

1. expected Sigstore workflow identity/issuer; and
2. the exact frozen SHA/workflow/helper digests inside the signed canonical record.

## Required workflow permissions

The transparency-signing job needs GitHub OIDC token issuance (`id-token: write`). Other `GITHUB_TOKEN` permissions should remain explicitly minimal. Granting OIDC does not authorize empirical execution; it only lets the already-authorized frozen workflow obtain a short-lived workload identity for signing public evidence.

## Remaining trust assumptions

Sigstore explicitly documents limits that must stay visible:

- Rekor's append-only property relies on a valid monitored transparency log;
- long-term trust requires monitoring;
- Sigstore notes that short-window timestamp forgery by the log operator is a different risk from long-term append-only verification;
- availability failure must fail closed rather than silently skip transparency publication.

Therefore final Mode T should treat Rekor as independent transparency/timestamp evidence under its published trust model, not as mathematical proof that no external actor can misbehave.

## Proposed fail-closed rules

- If R cannot be signed/logged before authorization consumption: **STOP / NO SECRET**.
- If A does not bind R and exact run attempt 1: **STOP / NO SECRET**.
- If C cannot be signed/logged before protected-material generation: **STOP / NO SECRET**.
- If more than one C exists for the same authorization: **PILOT INVALID**.
- If a run fails after C: **AUTHORIZATION CONSUMED / PILOT INVALID / NO RETRY UNDER SAME AUTHORIZATION**.
- If X cannot be signed/logged after a usable blinded execution: **PILOT INVALID**.
- If L cannot be signed/logged before release: **PILOT INVALID / NO PRIMARY INTERPRETATION**.
- If L's verified transparency-log time is not strictly before release: **PILOT INVALID**.
- If unexpected duplicate R/C/X records are discovered: **PILOT INVALID pending adjudication under the frozen rerun policy**.
- If Sigstore identity, bundle inclusion proof, frozen SHA, workflow digest or helper digest mismatches: **FAIL-CLOSED**.

## Relationship to existing P6

Existing P6 byte-retention remains useful for retaining Sigstore bundles, public evidence JSON, ciphertext and blinded artifacts. For Mode T, however, ordinary archive/retrieve/hash equality must not be promoted into proof that run history was append-only.

The Mode T mechanism evidence should bind a separate transparency contract digest in addition to the ordinary P6 retention contract.

## Current disposition

**Candidate anti-deletion mechanism identified; implementation and trust review remain OPEN.**

No Sigstore entry has been created for empirical evidence, no real secret exists, and no experimental transition has occurred.
