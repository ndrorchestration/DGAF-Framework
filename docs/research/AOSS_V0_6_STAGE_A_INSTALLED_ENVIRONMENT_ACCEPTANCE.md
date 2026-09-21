# AOSS v0.6 Stage-A installed-environment acceptance packet

Issue #901 requires **accepted** installed-environment evidence before collection
execution readiness can be considered. The candidate-evidence mechanism accepted
through PR #916 creates reviewable evidence, but it cannot accept itself.

This tranche adds the next structural boundary: an acceptance packet that binds:

- the exact complete candidate record via deterministic SHA-256;
- the candidate's evidence-payload SHA-256;
- an explicit source reference for the retained candidate; and
- a reserved adjudication object.

The adjudication object is intentionally fixed to `NOT_EXECUTED` by this
preparation/validation code. Reviewer identity, review time, and decision-record
digest must remain empty. Any attempt to pre-populate those fields or claim
environment acceptance fails closed.

A successful packet validation therefore means only:

```text
INSTALLED_ENVIRONMENT_ACCEPTANCE_PACKET=PASS_STRUCTURAL_BINDING_ONLY
EXTERNAL_ADJUDICATION=NOT_EXECUTED
INSTALLED_ENVIRONMENT_ACCEPTANCE=NOT_ESTABLISHED
SOURCE_DRIVER_BINDING=NOT_ESTABLISHED
EXECUTABLE_ACCEPTANCE=NOT_ESTABLISHED
DESTINATION_ACCEPTANCE=NOT_ESTABLISHED
execution_allowed=false
COLLECTION_EXECUTION_READINESS=NOT_ESTABLISHED
SCIENTIFIC_N_INCREMENT=0
```

A later, separately reviewed decision record may reference this packet and the
retained exact candidate. This module cannot generate that decision or enable
collection.
