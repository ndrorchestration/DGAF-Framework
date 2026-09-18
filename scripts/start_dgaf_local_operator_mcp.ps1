Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$Python = Join-Path $RepoRoot ".venv-dgaf-mcp\Scripts\python.exe"
$Adapter = Join-Path $RepoRoot "scripts\dgaf_local_operator_mcp.py"

$Required = @(
    "DGAF_PUBLIC_ARCHIVE",
    "DGAF_PROTECTED_ARCHIVE",
    "DGAF_CUSTODY_PRIVATE_KEY",
    "DGAF_MATERIALIZATION_OUTPUT_DIR",
    "DGAF_RETENTION_ID"
)

if (-not (Test-Path $Python)) {
    throw "DGAF MCP environment is missing. Run scripts\bootstrap_dgaf_local_operator_mcp.ps1 first."
}

foreach ($Name in $Required) {
    $Value = [Environment]::GetEnvironmentVariable($Name, "Process")
    if ([string]::IsNullOrWhiteSpace($Value)) {
        throw "Required local environment variable is missing: $Name"
    }
}

& $Python $Adapter
exit $LASTEXITCODE
