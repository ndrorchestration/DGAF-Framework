# SBCF loopback HTTP effect adapter v0

Status: **RESEARCH PROTOTYPE / BOUNDED REFERENCE RUNTIME / NOT AUTHORIZED**.

This increment gives SBCF a real, observable policy-effect path without
inventing a second authorization model. It reuses the accepted DGAF capability
governance reference PEP in `scripts/dgaf_capability_pep.py` and the canonical
action transaction in `scripts/dgaf_capability_reference_transaction.py`.

The effect is deliberately limited to HTTP on exact loopback
`127.0.0.1:<explicit-port>`. It is a comparator-development boundary, not an
OS/network sandbox, egress firewall, production gateway, or bypass-resistant
containment layer.

## Effect binding

The canonical transaction binds:

- capability and capability version;
- exact resource URL;
- HTTP method and body;
- principals and delegation chain;
- policy identity/version;
- state guards;
- nonce.

The approved digest must match that canonical action before the PEP calls the
adapter. The adapter then independently requires the runtime request dictionary
to equal the digest-bound method/body parameters before issuing the HTTP
request. A mismatched request is refused before the socket effect.

The adapter accepts only:

- scheme `http`;
- exact host `127.0.0.1`;
- an explicit valid port;
- no URL credentials;
- no query or fragment;
- `GET` or `POST`;
- an empty body for `GET`.

It uses `http.client.HTTPConnection`, so redirect responses are observed but
not followed. Network/HTTP transport failures are conservatively reported as
`EXECUTION_OUTCOME_UNKNOWN` through the existing reference transaction rather
than as false success.

## Bounded runtime evidence

The focused test suite starts a real `ThreadingHTTPServer` on loopback and
observes actual requests.

Covered cases:

1. authorized, digest-bound POST reaches the server and produces an execution
   receipt;
2. revoked authorization blocks before any server request;
3. adjacent-resource authority substitution blocks before any server request;
4. runtime request/body substitution is refused before the HTTP effect;
5. a 302 redirect is returned to the caller but is not followed;
6. non-loopback, implicit-port, credential-bearing, query-bearing, and
   fragment-bearing resources are rejected;
7. unsupported methods and invalid GET bodies are rejected;
8. an unreachable loopback endpoint produces an unknown-outcome/reconciliation
   state rather than a successful receipt.

Focused positive/negative contract result at implementation checkpoint: **15 passed**.

A separate strict expected-failure test opens a direct loopback socket without
calling the PEP. The receiver observes the request, so the assertion that direct
code cannot bypass the reference PEP fails as expected. This is retained
falsification evidence for the absence of OS-level interception.

## Comparator interpretation

For the matched-comparator program this is appropriately classified as
`reference_runtime_effect`, not `enforced_runtime_effect`.

Why: a real effect is mediated when callers use the reference transaction and
PEP, but the host operating system does not prevent other process code from
opening a socket directly. The strict direct-socket counterexample reproduces
that bypass. The adapter therefore proves a bounded application enforcement
path, not universal interception or bypass resistance.

This advances SBCF beyond a purely synthetic effect path, but it does **not**
satisfy the matched-runtime readiness gate. A stronger matched boundary would
need an execution architecture in which the tested effect cannot bypass the PEP
within the declared threat model, plus the same frozen effect semantics and
outcome witness across comparators.

## Authority boundary

This prototype does not authorize production network access, credentials,
external services, live containment, or scientific inference. Tests use only
ephemeral loopback servers.

`SCIENTIFIC_N_INCREMENT=0`

`INDEPENDENT_VALIDATION=NOT_ESTABLISHED`

`CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED`

`HIGH_ASSURANCE=NOT_AUTHORIZED`
