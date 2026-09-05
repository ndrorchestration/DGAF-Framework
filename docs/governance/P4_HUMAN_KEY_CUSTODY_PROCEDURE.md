# P4 Human / Key Custody Procedure

**Status:** PROCEDURE DRAFT / NOT EXECUTED / P4 REMAINS OPEN  
**Authority:** DGAF/PDMAL pre-freeze governance  
**Purpose:** Define the minimum real-world custody, access-separation, and audit evidence required before P4 Security / Blinding may be considered for closure.

## Scope

This procedure addresses the gap that synthetic CI cannot close: actual human custody of the blinding secret and actual separation between people who can access the key/mapping and people who can inspect blinded experimental outputs before authorized unblinding.

Passing synthetic mock-key tests, storing a repository secret, seeing a successful workflow, or proving that code supports blinding does **not** establish this procedure was performed.

## Minimum role separation

At minimum, two distinct human principals are required:

1. **Key Custodian** — creates or receives the real blinding key and condition mapping; must not inspect blinded pilot outcomes for scientific interpretation before authorized unblinding.
2. **Execution / Analysis Principal** — may execute or inspect blinded artifacts but must not possess the blinding key or cleartext condition mapping before authorized unblinding.

A three-role arrangement is preferred when practical:

- **Key Custodian** — holds key and mapping.
- **Executor** — runs authorized blinded execution without access to cleartext mapping.
- **Analyst / Verifier** — receives only blinded outputs until formal unblinding authorization.

One person acting simultaneously as key custodian and blinded-results analyst does not satisfy the intended access-separation claim.

## Key lifecycle

### 1. Key creation

The real blinding key must be generated outside repository-visible state using a cryptographically secure random source.

The raw key must never be committed to Git, written into an issue/PR/comment, placed in an artifact, copied into ordinary logs, or exposed in documentation.

### 2. Custody assignment

The Key Custodian records an out-of-band custody acknowledgment containing:

- custodian identity;
- date/time with timezone;
- experiment/candidate identifier;
- key-generation method class, without revealing the key;
- key commitment/fingerprint sufficient to later prove continuity without disclosing the secret;
- storage medium/location class;
- acknowledgment that the custodian will not provide the key or mapping to the execution/analysis principal before authorized unblinding.

### 3. Storage

The raw key must be stored in a location accessible only to the Key Custodian or explicitly authorized backup custodian(s).

Acceptable storage must provide access control appropriate to the experiment. The evidence record should identify the storage class, not secret material.

Examples include a dedicated password manager vault, hardware-backed secret store, or equivalent access-controlled out-of-band mechanism.

### 4. Repository/runtime use

If the key must be injected into an execution environment, the mechanism must not expose the raw value to repository-visible logs or artifacts.

The runtime evidence must demonstrate only that a key was available where required; it must not reveal the key itself.

### 5. Mapping custody

The cleartext mapping between blinded condition identifiers and canonical conditions must remain under custodian control until authorized unblinding.

The analyst-facing artifact surface must contain only blinded identifiers during the blinded phase.

## Required access-separation evidence

Before P4 may be reviewed for closure, the evidence packet must include all of the following:

1. **Custodian attestation** — signed or otherwise attributable statement from the Key Custodian.
2. **Distinct-role attestation** — attributable statement showing the execution/analysis principal is a different human principal from the Key Custodian.
3. **Key commitment** — non-secret fingerprint/commitment generated before blinded execution.
4. **Mapping commitment** — non-secret commitment to the condition mapping generated before blinded execution, without revealing the mapping.
5. **Access statement** — explicit declaration of who had access to the key and mapping during the blinded period.
6. **No-access statement** — explicit declaration from the execution/analysis principal that they did not possess the key or cleartext mapping during the blinded period.
7. **Timestamp ordering** — evidence that commitments and custody assignment predate any authorized empirical execution.
8. **Unblinding rule** — explicit condition under which the custodian may release the mapping/key-derived unblinding material.
9. **Release record** — after authorized unblinding, an attributable release event with timestamp and authorization reference.
10. **Continuity verification** — proof that the commitment/fingerprint at release corresponds to the same custody object committed before execution.

## Freeze and authorization ordering

The following ordering is mandatory:

1. candidate and protocol identities selected;
2. analysis/configuration identities selected;
3. P4 custody roles assigned and commitments created;
4. final pre-freeze evidence chain reviewed;
5. immutable freeze created and independently verified;
6. separate pilot authorization granted;
7. blinded empirical execution begins;
8. blinded analysis proceeds according to the locked plan;
9. unblinding occurs only under the predeclared release rule;
10. unblinding/release evidence is appended without rewriting earlier records.

Neither freeze nor authorization may be inferred from custody setup. Custody setup is a prerequisite, not permission to execute.

## Evidence packet template

The operational P4 packet should contain a machine-readable manifest and human attestations.

Suggested machine-readable fields:

```yaml
p4_custody_version: "1"
experiment_id: "PDMAL-PILOT-V1"
candidate_sha: "<40-hex candidate SHA>"
candidate_tree_sha: "<40-hex tree SHA>"
protocol_version: "0.7.5"
key_custodian_id: "<non-secret attributable identity>"
execution_principal_id: "<distinct attributable identity>"
analyst_principal_id: "<attributable identity or same as executor if allowed>"
key_commitment_sha256: "<non-secret commitment>"
mapping_commitment_sha256: "<non-secret commitment>"
custody_assigned_at: "<RFC3339 timestamp>"
freeze_id: null
freeze_verified_at: null
pilot_authorization_id: null
empirical_execution_started_at: null
unblinding_authorization_id: null
unblinding_released_at: null
p4_status: "OPEN"
```

Fields corresponding to events that have not occurred must remain null. They must not be pre-populated with placeholder claims that look like completed events.

## Closure review predicates

P4 may be considered for `CLOSED / VERIFIED` only if an independent reviewer can establish:

- at least two distinct human principals participated in the custody/analysis separation;
- the key and cleartext mapping were not available to the blinded-results analyst before authorized unblinding;
- non-secret commitments predate empirical execution;
- the runtime/blinding mechanism used the custody object associated with those commitments;
- release/unblinding occurred only after the required freeze/authorization/analysis conditions;
- the evidence packet is retained with provenance and integrity checks;
- no conflicting access record exists.

If any required predicate is missing or cannot be independently checked, P4 remains **OPEN / BLOCKED** rather than being inferred from intent.

## Failure and exception handling

Any of the following must fail closed:

- key or mapping exposed to the blinded analyst before authorized release;
- same human acting as both sole key custodian and blinded scientific analyst;
- commitment created only after outcomes are available;
- missing or contradictory custody timestamps;
- missing attributable custodian or analyst statements;
- key continuity cannot be demonstrated;
- evidence packet altered without preserved history;
- unblinding performed without the predeclared release condition being satisfied.

A failed custody attempt must remain preserved as historical evidence. A new attempt requires a new explicit custody instance; it must not overwrite the failed record.

## Relationship to CI

CI may verify schema, completeness, timestamp syntax, commitment formatting, candidate identity, and fail-closed state transitions. CI cannot establish that two GitHub usernames or two strings correspond to genuinely distinct humans with real-world access separation.

Human-role separation therefore requires attributable operational evidence outside the synthetic test environment.

## Explicit non-claims

Creating or merging this procedure does **not**:

- establish that a Key Custodian exists;
- establish that two distinct humans have performed the required roles;
- prove access separation;
- create a real blinding key;
- create a freeze;
- authorize a pilot;
- permit empirical execution;
- authorize unblinding;
- increase empirical N.

**P4 remains OPEN until the procedure is actually performed and independently verified.**  
**Freeze: NOT ESTABLISHED.**  
**Pilot authorization: NOT GRANTED.**  
**Empirical N: 0.**
