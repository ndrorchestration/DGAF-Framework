# SBCF durable synthetic admission — checkpoint QA

Status: RESEARCH PROTOTYPE ONLY. SQLite records admitted source/run sequence high-water marks and rejects replay after verifier restart; field-specific source authority is a local allowlist.

Not a secure evidence service. The DB is local and mutable by its host; the keys and trust registry are caller-controlled. The DB can be deleted or rolled back; high-water marks do not survive deliberate storage replacement. Per-run nonce uniqueness, durable policy identity, expiry, independent witness, isolation and cross-process adversarial race testing are not established. The narrow result is fixture-level sequence persistence and field authorization, not independent validation.

Before promotion require external identity and custody, anti-rollback storage, multi-process concurrency stress, source/field authority completeness, rotation/revocation and failed-disk/recovery behaviors. Existing protected-main, reviewer, scientific N and high-assurance gates remain unchanged.
