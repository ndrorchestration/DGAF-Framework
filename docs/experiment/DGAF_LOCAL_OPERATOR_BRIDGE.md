# DGAF Local Operator Bridge — Epoch 002

Status: **PROSPECTIVE TOOLING ONLY**

Scientific/control effect: **NONE**

`PRE-FREEZE / FAIL-CLOSED / PRIMARY ANALYSIS NOT AUTHORIZED / N=0`

## Purpose

The local operator bridge removes the manual "run this script and bring back the
safe file" handoff without moving custody secrets into GitHub, CI, Notion, chat,
or a cloud agent.

It is deliberately a **local process boundary**, not a network service.

The bridge allows an orchestration client to request only four operations:

1. `status`
2. `verify_inputs`
3. `materialize`
4. `get_evidence`

There is no arbitrary command execution, no shell action, no file-browser action,
no delete/reset action, no GitHub mutation action, and no primary-analysis action.

## Security boundary

The following values are configured only in the operator's local environment:

- `DGAF_PUBLIC_ARCHIVE`
- `DGAF_PROTECTED_ARCHIVE`
- `DGAF_CUSTODY_PRIVATE_KEY`
- `DGAF_MATERIALIZATION_OUTPUT_DIR`
- `DGAF_RETENTION_ID`

The bridge never returns those paths.

The public/protected archives and custody private key must remain outside the
repository. Symlinks are rejected. The public and protected archives are checked
against the canonical dataset-lock artifact contracts before materialization.

The custody private key is checked only for local presence and external-file
placement. Its bytes are never returned.

## Invocation

The bridge consumes exactly one JSON object on standard input and emits exactly
one JSON response on standard output.

Example:

```bash
printf '{"action":"status"}' | python scripts/dgaf_local_operator_bridge.py
```

Verification:

```bash
printf '{"action":"verify_inputs"}' | python scripts/dgaf_local_operator_bridge.py
```

Materialization:

```bash
printf '{"action":"materialize"}' | python scripts/dgaf_local_operator_bridge.py
```

Safe evidence retrieval:

```bash
printf '{"action":"get_evidence"}' | python scripts/dgaf_local_operator_bridge.py
```

`get_evidence` returns only the non-secret
`TRACK_A_EPOCH_002_MATERIALIZATION_EVIDENCE.json` content plus its digest.
It refuses evidence that claims primary-analysis authorization, primary-analysis
execution, or a scientific-N increment.

## Intended autonomous flow

```text
agent/orchestrator
    |
    | JSON: status / verify_inputs / materialize / get_evidence
    v
local DGAF operator bridge
    |
    | reads custody material locally only
    | invokes accepted canonical materializer
    | retains five-file bundle locally
    v
non-secret materialization evidence
    |
    v
agent/orchestrator
    |
    | later repository evidence-admission event
    v
GitHub protected review/CI
```

The bridge itself does **not** create a branch, commit, PR, receipt, authorization
record, or primary-analysis result. Those remain separate governed events.

## Why no network listener

A network listener would enlarge the attack surface around custody material and
would create a second authentication/authorization problem before it solves the
first one.

The JSON-over-stdin/stdout contract is intentionally transport-neutral. A later
local MCP/plugin/desktop adapter can wrap this exact process without changing the
scientific or custody semantics.

That adapter should expose these operations as explicit tools while preserving:

- local-only secret access;
- no arbitrary shell;
- no secret-bearing output;
- exact allow-listing;
- content-addressed evidence;
- fail-closed behavior;
- separate human/governance authorization at consequential state transitions.

## Non-effects

Acceptance or execution of this bridge does not:

- authorize primary analysis;
- run primary analysis;
- increment scientific N;
- establish canonical DGAF efficacy;
- establish independent validation;
- authorize High-Assurance;
- create a materialization repository receipt;
- change the accepted dataset lock or bounded unblinding authorization.

Only the existing governed event chain may change those states.
