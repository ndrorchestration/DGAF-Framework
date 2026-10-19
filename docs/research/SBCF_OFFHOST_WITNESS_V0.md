# SBCF off-host witness prototype v0

Status: RESEARCH PROTOTYPE / FAIL-CLOSED / NOT AUTHORIZED.

This increment moves a monotonic checkpoint store behind an HTTPS service so the
SBCF client process does not directly own the witness database. The service
requires distinct read and write bearer credentials, binds records to
source/run/policy, rejects replay and lower sequences, rejects policy drift
within a run, and makes checkpoint IDs unique. The service refuses to start if
the two credentials are identical. The client requires HTTPS and a configured
trust anchor; network,
certificate, authentication, parsing, or availability failures return no
verified checkpoint.

## Security boundary

A separate computer is a stronger failure-domain separation than two SQLite
files under one process, but it is **not independent validation**. In the planned
two-host demonstration both machines remain under the same operator and the
client still holds a write credential that can advance the witness. A
read-only credential can no longer advance state, and the write credential
cannot read checkpoints, reducing accidental privilege coupling. A compromised
authorized writer could still advance the remote counter and cause fail-closed
denial of service. Compromise or rollback of the witness host itself is not
solved by this interface.

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

## Two-host live QA — 2026-10-19

The implementation at `f04ddcc6b4e5940ed126f37db5eb89ad65e22bb4` was
run with NeonPC as the SBCF client and neontic as the separate witness host.
The witness used an ephemeral self-signed TLS certificate with host/IP SANs,
a bearer credential, and a SQLite store kept only on the witness machine.

Observed from the client over HTTPS:

- sequence 1 advance: accepted;
- sequence 1 read: returned checkpoint `live-cp-1`;
- sequence 1 replay with a different checkpoint ID: rejected;
- sequence 2 advance: accepted;
- sequence 2 read: returned checkpoint `live-cp-2`;
- read using a wrong bearer credential: failed closed with no checkpoint.

The retained witness row is source `broker`, run `live-run`, policy
`policy-live`, sequence 2, checkpoint `live-cp-2`. The witness DB SHA-256 is
`f7f590bd2bd907a148e4acafa4fe915306b2155d96c501f948094d4d65ebd250`.
The public certificate file SHA-256 is
`e75299f3f0e7e723ad655cdaa18cf4748bd2aa673ea12e6ac50ce5f02fb28e6a`.
The private TLS key and bearer credential were deleted after the test; the
service was stopped. The witness database and public certificate remain on the
witness host as retained local evidence. No firewall rule was added.

Evidence receipt:
`docs/research/sbcf_offhost_evidence/2026-10-19/live_probe.json`.

The first evidence-file write failed because its nested directory was absent;
the directory was created and the same content was retried. The witness host
also lacked the PowerShell `Get-FileHash` command in this session, so SHA-256
hashes were computed with Python `hashlib`. Neither issue changed the witness
implementation or observed protocol behavior.

This two-host result establishes bounded off-host separation only. Both
computers remain under the same operator, the authorized client can advance the
remote counter, and witness-host compromise or rollback remains outside the
demonstrated protections.

This work does not establish live containment, matched comparator efficacy,
scientific N, independent validation, canonical efficacy, or high assurance.
