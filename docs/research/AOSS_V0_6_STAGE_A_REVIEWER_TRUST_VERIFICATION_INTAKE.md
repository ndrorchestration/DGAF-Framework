# AOSS v0.6 Stage-A reviewer trust verification intake

This tranche follows the accepted external decision intake and cryptographic
reverification layers. It records a separate external verifier's findings about
reviewer attribution and reviewer independence.

The intake binds exactly to:

- the external admission-decision intake record SHA-256; and
- the cryptographic reverification packet SHA-256.

It records the external verifier identity, verification timestamp, retained
verification-record URI and SHA-256, verification-method summary, and separate
findings for reviewer attribution and independence.

Allowed external findings are `VERIFIED`, `NOT_VERIFIED`, or `BLOCKED`.

An external `VERIFIED` finding is still evidence for later local adjudication;
it is not itself local trust establishment. Therefore even the positive fixture
path retains:

```text
REVIEWER_ATTRIBUTION_VERIFIED=false
INDEPENDENCE_VERIFIED=false
LOCAL_ADJUDICATION=NOT_EXECUTED
INSTALLED_ENVIRONMENT_ACCEPTANCE=NOT_ESTABLISHED
SOURCE_DRIVER_BINDING=NOT_ESTABLISHED
EXECUTABLE_ACCEPTANCE=NOT_ESTABLISHED
DESTINATION_ACCEPTANCE=NOT_ESTABLISHED
execution_allowed=false
COLLECTION_EXECUTION_READINESS=NOT_ESTABLISHED
SCIENTIFIC_N_INCREMENT=0
```

The tests use structural fixture records only. They demonstrate the intake and
fail-closed boundary; they do not claim any real reviewer or verifier has been
authenticated or shown independent.
