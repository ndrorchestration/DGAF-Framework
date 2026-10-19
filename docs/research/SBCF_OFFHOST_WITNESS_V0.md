# SBCF off-host witness prototype v0

Status: RESEARCH PROTOTYPE / FAIL-CLOSED / NOT AUTHORIZED.

This increment moves a monotonic checkpoint store behind an HTTPS service so the
SBCF client process does not directly own the witness database. The service
requires a bearer token, binds records to source/run/policy, rejects replay and
lower sequences, rejects policy drift within a run, and makes checkpoint IDs
unique. The client requires HTTPS and a configured trust anchor; network,
certificate, authentication, parsing, or availability failures return no
verified checkpoint.

## Security boundary

A separate computer is a stronger failure-domain separation than two SQLite
files under one process, but it is **not independent validation**. In the planned
two-host demonstration both machines remain under the same operator and the
client holds a bearer credential that can advance the witness. A compromised
authorized client could therefore advance the remote counter and cause
fail-closed denial of service. Compromise or rollback of the witness host itself
is not solved by this interface.

TLS server private-key material and the witness SQLite file must remain on the
witness host during live QA. Only the public certificate/trust anchor and an
ephemeral test credential are supplied to the client. No credential, private
key, or live witness database belongs in Git.

## QA obligations

- Preserve all existing SBCF rollback and same-process counterexamples.
- Test monotonicity, policy binding, unique checkpoint identity, authentication,
  strict request shape, and fail-closed transport behavior.
- Run an ephemeral two-host HTTPS demonstration and retain command/results
  without publishing secrets or private keys.
- Explicitly distinguish remote-host custody from independently managed custody.
- Require a separately governed writer identity, durable anti-rollback storage,
  key rotation/revocation, availability policy, and outside falsification before
  any stronger assurance claim.

This work does not establish live containment, matched comparator efficacy,
scientific N, independent validation, canonical efficacy, or high assurance.
