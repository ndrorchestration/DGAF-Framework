# P6a — Essential Runtime Hardening

**Status:** Planned / required before empirical runtime claims

P6a is the minimum safety and integrity boundary required before using DGAF's API as an empirical evidence source. It intentionally excludes production-scale operations such as rate limiting infrastructure and long-term persistence.

## Required gates

### Authentication
Protected evaluation endpoints MUST require the configured test authentication mechanism. Authentication failures must return structured errors and must not reveal protected state.

### CORS
Production-like evaluation environments MUST use an explicit allowed-origin policy. `*` is prohibited for authenticated/state-changing evaluation paths.

### Request validation
Every externally callable evaluation endpoint must validate:

- HTTP method;
- JSON object shape;
- required fields;
- field types and bounds;
- payload size where relevant;
- unsupported fields where strict schemas are required.

Invalid input must fail closed without executing governance side effects.

### Audit integrity
Every evidence-producing runtime execution must emit or reference:

- run/session identifier;
- commit/version;
- timestamp;
- input fingerprint where appropriate;
- decision;
- gate trace;
- evidence mode/status;
- failure reason when blocked/rejected.

Audit records must not claim stronger evidence than the endpoint actually executed.

## Acceptance tests

1. Unauthenticated access to protected endpoint → rejected.
2. Wrong credentials → rejected without state disclosure.
3. Allowed test credentials → accepted.
4. Disallowed origin → no permissive credential-bearing CORS response.
5. Malformed JSON/object → rejected.
6. Invalid types/bounds → rejected.
7. Prompt-injection negative fixtures → deterministic rejection path.
8. Evidence envelope present on success and failure.
9. Blocked/unimplemented governance checkpoint → explicit BLOCKED/NOT_IMPLEMENTED, never fabricated PASS.
10. Repeated identical request under identical state → deterministic response fields except explicitly documented timestamps/IDs.

## Boundary
Passing P6a does not establish production readiness. It establishes that the runtime is sufficiently controlled to serve as an honest integration/experimental surface.
