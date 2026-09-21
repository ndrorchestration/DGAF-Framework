# AOSS v0.6 Stage-A external admission decision intake

Issue #901 still requires separate acceptance of the installed environment,
source-driver/collector executable identity, and destination/attempt identity.

The repository can now construct exact review candidates for those obligations.
This tranche adds a non-promoting intake for a decision returned by an external
reviewer.

The intake binds the returned decision to:

- the exact installed-environment evidence candidate;
- the exact prospective execution-identity candidate;
- reviewer identity and review timestamp;
- an external decision-record URI and SHA-256;
- the reviewer's independence claim and stated basis; and
- three explicit dispositions: installed environment, source-driver/executable,
  and destination/attempt.

Allowed external dispositions are `ACCEPT`, `REJECT`, and `BLOCKED`.

An external `ACCEPT` is preserved as an external report only. Structural
validation does not verify reviewer attribution, verify independence, retrieve
the external artifact, cryptographically reverify it, perform local governance
adjudication, or promote any execution-readiness predicate.

A successful validation therefore means only:

```text
EXTERNAL_DECISION_INTAKE=PASS_EXTERNAL_DECISION_STRUCTURAL_ONLY
REVIEWER_ATTRIBUTION_VERIFIED=false
INDEPENDENCE_VERIFIED=false
CRYPTOGRAPHIC_REVERIFICATION=NOT_EXECUTED
LOCAL_ADJUDICATION=NOT_EXECUTED
INSTALLED_ENVIRONMENT_ACCEPTANCE=NOT_ESTABLISHED
SOURCE_DRIVER_BINDING=NOT_ESTABLISHED
EXECUTABLE_ACCEPTANCE=NOT_ESTABLISHED
DESTINATION_ACCEPTANCE=NOT_ESTABLISHED
execution_allowed=false
COLLECTION_EXECUTION_READINESS=NOT_ESTABLISHED
SCIENTIFIC_N_INCREMENT=0
```

A later trust transition must separately verify attribution and evidence and
perform the authorized local adjudication. This intake cannot perform that
transition itself.
