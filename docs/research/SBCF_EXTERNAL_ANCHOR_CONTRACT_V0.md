# SBCF external rollback-anchor contract v0

Status: RESEARCH INTERFACE / FAIL-CLOSED / NOT AUTHORIZED.

The recovery layer can now require a caller-supplied checkpoint whose source, run, policy and sequence must match the two local stores and pass an injected verifier. A newer anchor detects coordinated rollback of the local evidence and witness files. Missing, invalid, unverified, stale, future or wrong-scope anchors block.

## Critical boundary

This does **not** create an independent witness. The anchor record and verifier are injected by the caller. If the same controlling principal can roll back the local stores and the anchor or can replace the verifier, the contract can report synthetic consistency. The tests preserve that counterexample as a passing limitation demonstration rather than treating the interface as security evidence.

A production design still needs independently managed identity/key custody, authenticated transport, a monotonic or append-only external checkpoint service, anti-rollback storage, revocation/rotation, availability policy, and outside falsification. The result string deliberately says `MATCHED_VERIFIED_ANCHOR_CONTRACT_ONLY`; it never says authorized, safe, quarantined, independent or high-assurance.

Existing local rollback, direct evidence-API bypass and coordinated local rollback xfails remain unchanged. SCIENTIFIC_N_INCREMENT=0; INDEPENDENT_VALIDATION=NOT_ESTABLISHED; CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED; HIGH_ASSURANCE=NOT_AUTHORIZED.
