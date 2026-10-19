# SBCF HMAC evidence envelope — research prototype

Status: SYNTHETIC ONLY / FAIL-CLOSED / NOT AUTHORIZED.

Adds keyed SHA-256 MAC over canonical JSON of source, run, policy, nonce, sequence and state. Verifier requires expected run/policy/nonce, registered source, exact field set, and rejects replay of accepted source-run-sequence tuples. Negative tests cover tampering, spoofed source, unexpected run, unknown source and malformed sequence.

**Ceiling:** HMAC keys live in the test process; their presence does NOT demonstrate independent source identities, secure key custody, authentic external observation or replay safety after restart. The verifier uses volatile in-memory replay state, not persistent monotonic counters; replay can succeed on a new verifier instance. Source event authority is not bound to individual state fields. No clock expiry, secure nonce service, atomic snapshot, credential revocation or OS/network sandbox. This is NOT trusted attestation.

Next QA: persisted source-specific monotonic sequence state, asymmetric identity with protected trust root, field-level source authority, full-chain external retention, corrupted/split-brain tests, real PEP integration, and independent falsification. Keep all scientific N and authorization ceilings unchanged.
