# Evidence Gate v0 — Quickstart

Status: candidate API. Evidence Gate is non-authorizing and does not establish downstream lifecycle state.

## Current packaging

The candidate currently ships inside the DGAF repository:

```bash
python -m pytest tests/test_evidence_gate.py tests/test_evidence_gate_adapters.py tests/test_evidence_gate_serialization.py -q
```

A standalone package/repository is intentionally deferred until a real outside consumer demonstrates an independent versioning or dependency boundary.

## Minimal local-test example

```python
from components.evidence_gate import admit_evidence
from components.evidence_gate_adapters import (
    LocalTestArtifact,
    local_test_artifact_to_gate_inputs,
)
from components.evidence_gate_serialization import (
    evidence_admission_receipt_to_dict,
)

mapped = local_test_artifact_to_gate_inputs(
    LocalTestArtifact(
        artifact_id="pytest-run-42",
        test_name="test_widget",
        source_revision="abc123",
        runtime_identity="pytest-9.0",
        environment_identity="python-3.12",
        output_bytes=b'{"status":"passed"}\n',
    )
)

receipt = admit_evidence(
    mapped.evidence,
    mapped.target,
    mapped.provenance,
    mapped.claim_scope,
    evidence_bytes=mapped.evidence_bytes,
    expected_target=mapped.target,
    required_producer_class="LOCAL_TEST",
)

print(evidence_admission_receipt_to_dict(receipt))
```

The receipt records:
- admitted / denied;
- stable reason code;
- evidence and exact target identities;
- verified digest;
- which checks actually ran;
- provenance class;
- claim/evidence class;
- explicit claim ceiling;
- `authorization_effect: NONE`.

## Domain adapters

### Track A operator evidence

`validated_track_a_operator_admission_to_gate_inputs(...)` is intentionally gated by `domain_validation_passed=True`.

That flag must only be supplied after the existing Track A evidence-mode validator succeeds against the concrete execution receipt and retained archives. The adapter does not replace archive member checks, custody binding, protocol identity checks, or any scientific/non-authorizing constraints.

### Generic local test artifact

`local_test_artifact_to_gate_inputs(...)` demonstrates that the same gate contract can classify deterministic test evidence without Track A, PDMAL, dataset-lock, or scientific-state fields.

This is an in-repository second-consumer conformance case, not external-runtime portability.

## Claim ceiling

An admitted receipt means only:

> The supplied evidence satisfied the declared Evidence Gate v0 contract for the exact recorded target, provenance class, and claim scope.

Admission does not establish:
- deployment or release authority;
- execution or mutation authority;
- dataset lock;
- unblinding;
- analysis authority;
- independent validation;
- efficacy;
- production readiness;
- certification/compliance;
- system-wide safety or reliability.

## Historical evidence

Historical evidence remains bound to its original target unless an explicit transfer/rebinding checker succeeds. A changed target must not inherit old evidence merely because the artifact is internally valid.

## Current validation state

The candidate is designed to preserve DGAF's existing exact-identity and non-transfer discipline while extracting a smaller reusable contract. Repository CI and outside-consumer usability must be evaluated separately before any product-readiness claim.
