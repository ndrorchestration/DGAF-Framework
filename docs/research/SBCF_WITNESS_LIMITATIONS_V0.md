# SBCF separate-store synthetic witness

Status: DRAFT / PRE-FREEZE / NOT AUTHORIZED. Updated 2026-10-11.

`WitnessedVerifier` keeps high-water values in a second SQLite file. Its admission path now uses a single attached-database transaction with persistent DELETE journals and FULL synchronization. Counter disagreement blocks later admissions pending reconciliation. This is local failure-domain separation and a tested synthetic admission protocol, not independently trusted or anti-rollback-secure storage. See [crash-consistency QA](SBCF_CRASH_CONSISTENCY_QA_V0.md) for tests and precise scope.

Both files and the signature keys remain on the same host under the same principal. Coordinated rollback of both still defeats replay protection. Direct use of the evidence-only API can split counters; the witnessed API detects the mismatch but cannot undo that bypass. The strict standalone rollback, evidence-only bypass and coordinated rollback counterexamples remain present.

Application-boundary process exits and a four-process duplicate race have been tested. Interruptions inside SQLite's commit, physical power loss, faulty filesystem flush/locking, sustained concurrency, disk-full behavior, hostile file replacement, isolated signing keys and independently authorized external sources are not established. Database creation is separate from admission; startup on corrupt stores may raise. Mismatch recovery has no automatic reconciliation path.

Before production design: independently managed witness and authenticated communication; protected append-only evidence; isolated keys and source authority; lower-level crash/storage injection; explicit reconciliation with external evidence; sustained contention testing and independent review. Local passing tests do not authorize live containment or high assurance.
