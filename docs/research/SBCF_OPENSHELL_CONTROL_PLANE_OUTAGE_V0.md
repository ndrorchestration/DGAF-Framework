# SBCF OpenShell control-plane outage characterization v0

Status: RESEARCH CHARACTERIZATION / NOT A MATCHED BENCHMARK / NOT AUTHORIZED.

This checkpoint characterizes one concrete control-plane-unavailable condition
for the pinned NVIDIA OpenShell baseline used by the SBCF matched-effect
candidate.

Pinned identity:

- repository: `NVIDIA/OpenShell`;
- commit: `5a7728c304b5528e954e9ae900cf21f84e1a12b1`;
- tag: `v0.1.4`;
- runner: `ubuntu-24.04`.

The receiver is still `https://api.github.com`, not the common external receiver
required by the parent matched HTTP contract. This evidence therefore cannot
establish matched-effect equivalence.

## Topology diagnostic

Hosted run `39229673726` completed successfully without stopping or mutating
the control plane.

Observed runtime topology:

- `openshell-gateway` runs as a user service on the runner host;
- the sandbox and supervisor are separate containers;
- the supervisor uses host networking;
- the sandbox uses Docker network `none`;
- the active rule allowed `api.github.com:443`;
- `example.com:443` remained denied after the diagnostic.

This confirms that the supervisor can remain alive independently of the
gateway user service.

## Gateway-outage probe

Hosted run `39229671143` completed successfully.

The probe first established a positive control: the sandbox successfully
performed an allowed GET to `https://api.github.com/zen`.

The workflow then stopped **only**
`openshell-gateway.service`. The service reported inactive and
`openshell status` exited nonzero. After waiting beyond one policy-poll
interval, the supervisor container remained running but reported unhealthy.

The request was then executed from inside the already-running sandbox rather
than through the OpenShell CLI.

Observed post-outage result:

- exact allowed host GET: exit code `0`, non-empty response, **ALLOW**;
- adjacent `example.com` GET: nonzero exit, denied/unreachable;
- supervisor OCSF logs still recorded the exact `api.github.com` request as
  allowed under `policy:matched_http`;
- supervisor logs still recorded the adjacent host as denied.

The candidate common effect contract currently expects **DENY** when the
control plane is unavailable. Pinned OpenShell v0.1.4 therefore does not match
that candidate semantic under this tested gateway-service-loss condition.

The machine-readable mapping now records:

- mapping state: `OBSERVED_SEMANTIC_MISMATCH`;
- observed decision: `ALLOW`;
- blocker: `candidate_expected_deny_observed_allow`.

This is stronger than leaving the case `UNRESOLVED`, but it does **not** make
the OpenShell mapping ready. The baseline receiver is still unmatched, the
negative-observation bound is not frozen, and the candidate contract itself is
not frozen.

## Interpretation boundary

The result supports only this bounded statement:

> With the pinned OpenShell v0.1.4 gateway service stopped while the existing
> sandbox and supervisor remain running, the previously published allow rule
> continued to permit the tested `api.github.com` GET.

It does not establish behavior for every possible OpenShell control-plane
failure, network partition, process crash, stale-policy duration, or future
OpenShell version. It also does not establish that continuing last-known-good
policy is intrinsically unsafe; it establishes that this behavior differs from
the candidate matched contract's chosen fail-closed `DENY` semantic.

Secret-free receipt:
`docs/research/sbcf_openshell_evidence/2026-10-19/control_plane_outage.json`.

No fairness, efficacy, parity, superiority, independent-validation, freeze,
release, or scientific-N claim follows from this characterization.

`SCIENTIFIC_N_INCREMENT=0`

`INDEPENDENT_VALIDATION=NOT_ESTABLISHED`

`CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED`

`HIGH_ASSURANCE=NOT_AUTHORIZED`
