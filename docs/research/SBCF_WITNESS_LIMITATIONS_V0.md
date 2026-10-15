# SBCF separate-store synthetic witness

Status: DRAFT / PRE-FREEZE / NOT AUTHORIZED.

The new WitnessedVerifier places high-water values in a second SQLite file and rejects replay when the primary evidence store alone is restored from an older snapshot. It is a **demonstration of failure-domain separation**, NOT independent or anti-rollback-secure storage.

Both files remain on the same host, writable by the same principal. A coordinated rollback of both still defeats the protection. The process may crash between evidence commit and witness commit, creating inconsistent state. Lock ordering, cross-store atomicity, signature key isolation, external source authority, multi-process stress and recovery are NOT ESTABLISHED.

Before production design: externally managed witness and authenticated communication; atomic admission protocol or conservative recovery; durable append-only audit; isolated keys, signed counters, fault injection, and independent review. The original rollback xfail must remain present as evidence of the unprotected baseline.
