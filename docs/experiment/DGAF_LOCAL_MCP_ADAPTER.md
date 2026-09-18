# DGAF Local MCP Adapter — Epoch 002

Status: **PROSPECTIVE TOOLING ONLY**

Scientific/control effect: **NONE**

`PRE-FREEZE / FAIL-CLOSED / PRIMARY ANALYSIS NOT AUTHORIZED / N=0`

## Purpose

This adapter makes the accepted DGAF local operator bridge consumable by a
standards-based MCP host while preserving the same custody boundary.

It uses the official MCP Python SDK over **stdio only**. The host launches the
adapter as a child process and communicates over stdin/stdout. The adapter does
not listen on a TCP port and does not expose HTTP, SSE, or Streamable HTTP.

## Exact tool surface

The adapter exposes exactly four zero-argument tools:

- `status`
- `verify_inputs`
- `materialize`
- `get_evidence`

Each tool delegates to the already bounded
`scripts/dgaf_local_operator_bridge.py` dispatch contract.

There is no MCP tool for:

- arbitrary shell execution;
- arbitrary filesystem reads or writes;
- Git operations;
- GitHub mutations;
- changing custody configuration;
- generating a materialization receipt;
- authorizing primary analysis;
- running primary analysis;
- changing scientific N or efficacy state.

## Dependency

Install the separately pinned local-only MCP dependency:

```powershell
py -m venv .venv-dgaf-mcp
.\.venv-dgaf-mcp\Scripts\python.exe -m pip install -r requirements-local-mcp.txt
```

This dependency is intentionally not added to the ordinary DGAF runtime or CI
requirements because MCP hosting is an optional operator integration boundary.

## Required local configuration

The underlying accepted bridge reads these variables locally:

```text
DGAF_PUBLIC_ARCHIVE
DGAF_PROTECTED_ARCHIVE
DGAF_CUSTODY_PRIVATE_KEY
DGAF_MATERIALIZATION_OUTPUT_DIR
DGAF_RETENTION_ID
```

Values must identify the operator-controlled retained artifacts. Do not place a
private-key value or passphrase itself in any variable; `DGAF_CUSTODY_PRIVATE_KEY`
is a local path to the key file.

A host configuration must pass these variables explicitly if that host does not
inherit the operator shell environment. Never commit their machine-specific
values.

## Pre-host validation

Before connecting an MCP host, prove the underlying bridge directly:

```powershell
'{"action":"status"}' |
  .\.venv-dgaf-mcp\Scripts\python.exe scripts\dgaf_local_operator_bridge.py

'{"action":"verify_inputs"}' |
  .\.venv-dgaf-mcp\Scripts\python.exe scripts\dgaf_local_operator_bridge.py
```

Then verify that the MCP adapter starts and waits for the host:

```powershell
.\.venv-dgaf-mcp\Scripts\python.exe scripts\dgaf_local_operator_mcp.py
```

Silence while it waits on stdio is expected.

## Host command

Register the following absolute local command with an MCP-capable desktop host:

```text
<absolute-repo-path>\.venv-dgaf-mcp\Scripts\python.exe
<absolute-repo-path>\scripts\dgaf_local_operator_mcp.py
```

Configure the five environment variables above in the host's local MCP server
configuration. Use absolute paths.

## Governed autonomous sequence

An orchestration client may then perform:

```text
status
  -> verify_inputs
  -> materialize
  -> get_evidence
```

The returned evidence can be used by a separate GitHub-capable orchestration
layer to prepare the repository evidence-admission event.

The MCP adapter itself cannot create that event and cannot cross the subsequent
materialization-receipt or primary-analysis authorization boundaries.

## Failure behavior

Any bridge refusal propagates as a tool failure. A failed materialization remains:

```text
MATERIALIZATION = NOT_ESTABLISHED
PRIMARY_ANALYSIS = NOT_AUTHORIZED / NOT RUN
N = 0
```

No fallback action broadens authority.
