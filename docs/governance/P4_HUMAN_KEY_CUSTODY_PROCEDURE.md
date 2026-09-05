# P4 Human / Key Custody Procedure

**Status:** PROCEDURE DRAFT / NOT EXECUTED / P4 REMAINS OPEN  
**Authority:** DGAF/PDMAL pre-freeze governance  
**Purpose:** Define the minimum real-world custody, access-separation, commitment, and audit evidence required before P4 Security / Blinding may be considered for closure.

## Scope

This procedure addresses the gap synthetic CI cannot close: actual human custody of the blinding secret and actual separation between people who can access the key/mapping and people who can inspect blinded experimental outputs before authorized unblinding.

Passing synthetic mock-key tests, storing a repository secret, seeing a successful workflow, or proving that code supports blinding does **not** establish this procedure was performed.

## Minimum role separation

At minimum, two distinct human principals are required:

1. **Key Custodian** — creates or receives the real blinding key and condition mapping; must not inspect blinded pilot outcomes for scientific interpretation before authorized unblinding.
2. **Execution / Analysis Principal** — may execute or inspect blinded artifacts but must not possess the blinding key or cleartext condition mapping before authorized unblinding.

A three-role arrangement is preferred when practical:

- **Key Custodian** — holds key and mapping.
- **Executor** — runs authorized blinded execution without access to cleartext mapping.
- **Analyst / Verifier** — receives only blinded outputs until formal unblinding authorization.

One person acting simultaneously as sole key custodian and blinded-results analyst does not satisfy the intended access-separation claim.

## Key and mapping commitments

A plain unsalted SHA-256 hash of the condition mapping is **not acceptable**. With four canonical conditions there are only 24 possible bijections, so an unsalted public mapping hash could be brute-forced and reveal the mapping before unblinding.

The custody procedure therefore uses domain-separated, nonce-hardened hash commitments.

### Required commitment construction

Generate independent cryptographically secure random nonces of at least 32 bytes:

- `key_commitment_nonce`
- `mapping_commitment_nonce`

The nonces remain secret under Key Custodian control until the corresponding authorized verification/release event.

Use deterministic canonical encodings and domain separation:

```text
key_commitment_sha256 = SHA256(
  b"DGAF-P4-KEY-v1\x00" || key_commitment_nonce || raw_blinding_key
)

mapping_commitment_sha256 = SHA256(
  b"DGAF-P4-MAP-v1\x00" || mapping_commitment_nonce || canonical_mapping_bytes
)
```

The published pre-execution evidence contains only the resulting commitment digests, never the raw key, cleartext mapping, or commitment nonces.

This is a hash-based commitment construction whose binding property depends on SHA-256 collision resistance and whose hiding property depends on the random nonce remaining secret until authorized release. It is not claimed to provide information-theoretic hiding.

### Canonical mapping encoding

Before commitment, serialize the condition mapping deterministically so the same mapping/nonces reproduce the same digest. The encoding specification must itself be frozen with the experiment. A suitable v1 encoding is canonical JSON with:

- UTF-8;
- sorted object keys;
- no insignificant whitespace;
- blinded identifiers as keys;
- canonical condition names as values.

No outcome information may enter the commitment input.

## Key lifecycle

### 1. Key creation

The real blinding key must be generated outside repository-visible state using a cryptographically secure random source and should contain at least 256 bits of entropy.

The raw key must never be committed to Git, written into an issue/PR/comment, placed in an artifact, copied into ordinary logs, or exposed in documentation.

### 2. Custody assignment

The Key Custodian records an out-of-band custody acknowledgment containing:

- custodian identity;
- date/time with timezone;
- experiment/candidate identifier;
- key-generation method class, without revealing the key;
- published `key_commitment_sha256`;
- published `mapping_commitment_sha256`;
- commitment construction/version;
- storage medium/location class;
- acknowledgment that the custodian will not provide the key, mapping, or commitment nonces to the execution/analysis principal before authorized release.

### 3. Storage

The raw key, cleartext mapping, and commitment nonces must be stored in a location accessible only to the Key Custodian or explicitly authorized backup custodian(s).

Acceptable storage must provide access control appropriate to the experiment. The public evidence record should identify the storage class, not secret material.

Examples include a dedicated password-manager vault, hardware-backed secret store, or equivalent access-controlled out-of-band mechanism.

### 4. Repository/runtime use

If the key must be injected into an execution environment, the mechanism must not expose the raw value to repository-visible logs or artifacts.

Runtime evidence may demonstrate that a key was available where required; it must not reveal the key itself.

### 5. Mapping custody

The cleartext mapping between blinded condition identifiers and canonical conditions must remain under custodian control until authorized unblinding.

The analyst-facing artifact surface must contain only blinded identifiers during the blinded phase.

## P4-A — pre-execution custody closure evidence

P4-A is the upstream custody gate consumed by P7/P8/P9. Before P4-A may be reviewed for closure, the evidence packet must include all of the following:

1. **Custodian attestation** — signed or otherwise attributable statement from the Key Custodian.
2. **Distinct-role attestation** — attributable statement showing the execution/analysis principal is a different human principal from the Key Custodian.
3. **Key commitment** — domain-separated nonce-hardened commitment generated before empirical execution.
4. **Mapping commitment** — domain-separated nonce-hardened commitment generated before empirical execution.
5. **Access statement** — explicit declaration of who had access to the key, mapping, and commitment nonces during the blinded period.
6. **No-access statement** — explicit declaration from the execution/analysis principal that they did not possess the key, cleartext mapping, or commitment nonces during the blinded period.
7. **Timestamp ordering** — evidence that commitments and custody assignment predate any authorized empirical execution.
8. **Unblinding rule** — explicit condition under which the custodian may release the mapping and its commitment nonce.
9. **Evidence provenance/integrity** — retained packet identity/digest and reviewable history.
10. **Independent pre-execution review** — confirmation that the principals are genuinely distinct, required statements/commitments are present, no secret material is disclosed, and no contradictory access record is known.

P4-A closure requires only evidence that can exist before freeze, authorization, pilot execution, or unblinding. Runtime use, release, and continuity recomputation are downstream P4-B evidence and must not be used as prerequisites for P4-A closure.

## P4-B — post-unblinding custody continuity audit

P4-B occurs only after separately authorized blinded execution and unblinding. It appends evidence to the historical P4-A record; it does not rewrite or retroactively manufacture P4-A closure.

P4-B must retain, as applicable:

- evidence that the authorized runtime actually used the custody object associated with the recorded commitment;
- release authorization and attributable release timestamp;
- released mapping plus nonce and exact recomputation of the pre-execution mapping commitment;
- controlled key-continuity verification when required by the frozen protocol;
- any adopted destruction attestation; and
- any custody exception, contradiction, or breach.

A failed or contradictory P4-B audit can invalidate downstream scientific interpretation or require explicit exception adjudication, while the historical P4-A record remains immutable as a statement of what was established pre-execution.

## Release and continuity verification

At authorized unblinding:

- release the cleartext mapping and `mapping_commitment_nonce` to the authorized verifier/analyst;
- independently recompute `mapping_commitment_sha256` using the frozen canonical encoding;
- require exact equality with the pre-execution published commitment;
- record the verification result and timestamp.

The raw blinding key does not need to become public. If key continuity must be independently verified, the verifier may inspect the raw key and `key_commitment_nonce` under controlled access, recompute `key_commitment_sha256`, record equality, and leave the raw secret undisclosed.

If a destruction policy is adopted, destroy secret material only after all required continuity checks and authorized unblinding are complete, then retain an attributable destruction attestation. Destruction is not required by this procedure unless separately adopted before freeze.

## Freeze and authorization ordering

The following ordering is mandatory:

1. candidate and protocol identities selected;
2. analysis/configuration identities selected;
3. P4 custody roles assigned and commitment digests published;
4. final pre-freeze evidence chain reviewed;
5. immutable freeze created and independently verified;
6. separate pilot authorization granted;
7. blinded empirical execution begins;
8. blinded analysis proceeds according to the locked plan;
9. unblinding occurs only under the predeclared release rule;
10. mapping commitment continuity is verified;
11. unblinding/release evidence is appended without rewriting earlier records.

Neither freeze nor authorization may be inferred from custody setup. Custody setup is a prerequisite, not permission to execute.

## Evidence packet template

The operational P4 packet should contain a machine-readable manifest and human attestations.

Suggested public machine-readable fields:

```yaml
p4_custody_version: "1"
experiment_id: "PDMAL-PILOT-V1"
candidate_sha: "<40-hex candidate SHA>"
candidate_tree_sha: "<40-hex tree SHA>"
protocol_version: "0.7.5"
commitment_scheme: "sha256-domain-separated-secret-nonce-v1"
key_custodian_id: "<non-secret attributable identity>"
execution_principal_id: "<distinct attributable identity>"
analyst_principal_id: "<attributable identity or same as executor if allowed>"
key_commitment_sha256: "<64-hex digest>"
mapping_commitment_sha256: "<64-hex digest>"
custody_assigned_at: "<RFC3339 timestamp>"
mapping_commitment_nonce_released_at: null
mapping_commitment_verified_at: null
key_commitment_verified_at: null
freeze_id: null
freeze_verified_at: null
pilot_authorization_id: null
empirical_execution_started_at: null
unblinding_authorization_id: null
unblinding_released_at: null
p4_status: "OPEN"
```

The public manifest must never contain the raw key, cleartext mapping before authorized unblinding, or unreleased commitment nonces.

Fields corresponding to events that have not occurred must remain null. They must not be pre-populated with placeholder claims that look like completed events.

## P4-A closure review predicates

P4-A may be considered for `CLOSED / VERIFIED (PRE-EXECUTION CUSTODY)` only if an independent reviewer can establish:

- at least two genuinely distinct human principals participate in custody/analysis separation;
- attributable custodian and execution/analysis no-access attestations exist;
- raw key, cleartext mapping, and secret commitment nonces are held out of band under the declared access/storage class;
- nonce-hardened key and mapping commitments were published before any empirical execution;
- custody assignment and commitment timestamps are retained;
- the release rule is predeclared;
- the evidence packet is retained with provenance and integrity checks;
- no key, mapping, or unreleased nonce is disclosed in the public packet; and
- no contradictory access record is known at closure.

If any required P4-A predicate is missing or cannot be independently checked, P4-A remains **OPEN / BLOCKED** rather than being inferred from intent.

P7/P8/P9 consume only this P4-A pre-execution closure. They must not require P4-B evidence that can exist only after pilot execution or unblinding.

## P4-B adjudication predicates

After authorized unblinding, the continuity audit checks runtime custody use, release authorization/timestamp, mapping-commitment recomputation, controlled key continuity when required, adopted destruction evidence, and exceptions/breaches. Missing or contradictory required P4-B evidence is preserved as a downstream failure/exception and may invalidate scientific interpretation; it does not rewrite the historical P4-A evidence.

## Failure and exception handling

Any of the following must fail closed:

- key, mapping, or commitment nonce exposed to the blinded analyst before authorized release;
- plain unsalted/public-nonce mapping hash used as the only pre-execution mapping commitment;
- same human acting as both sole key custodian and blinded scientific analyst;
- commitment created only after outcomes are available;
- missing or contradictory custody timestamps;
- missing attributable custodian or analyst statements;
- mapping commitment cannot be reproduced at authorized release;
- required key continuity cannot be demonstrated under the frozen protocol;
- evidence packet altered without preserved history;
- unblinding performed without the predeclared release condition being satisfied.

A failed custody attempt must remain preserved as historical evidence. A new attempt requires a new explicit custody instance; it must not overwrite the failed record.

## Relationship to CI

CI may verify schema, completeness, timestamp syntax, digest formatting, candidate identity, deterministic canonicalization, commitment recomputation on synthetic fixtures, and fail-closed state transitions. CI cannot establish that two GitHub usernames or two strings correspond to genuinely distinct humans with real-world access separation.

Human-role separation therefore requires attributable operational evidence outside the synthetic test environment.

## Explicit non-claims

Creating or merging this procedure does **not**:

- establish that a Key Custodian exists;
- establish that two distinct humans have performed the required roles;
- prove access separation;
- create a real blinding key;
- create or publish real commitment digests;
- create a freeze;
- authorize a pilot;
- permit empirical execution;
- authorize unblinding;
- increase empirical N.

**P4 remains OPEN until the procedure is actually performed and independently verified.**  
**Freeze: NOT ESTABLISHED.**  
**Pilot authorization: NOT GRANTED.**  
**Empirical N: 0.**
