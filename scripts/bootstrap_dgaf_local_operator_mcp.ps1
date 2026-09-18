Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$VenvDir = Join-Path $RepoRoot ".venv-dgaf-mcp"
$Python = Join-Path $VenvDir "Scripts\python.exe"
$Requirements = Join-Path $RepoRoot "requirements-local-mcp.txt"
$Adapter = Join-Path $RepoRoot "scripts\dgaf_local_operator_mcp.py"
$Bridge = Join-Path $RepoRoot "scripts\dgaf_local_operator_bridge.py"

if (-not (Test-Path $VenvDir)) {
    Write-Host "Creating isolated DGAF MCP environment..."
    py -3 -m venv $VenvDir
}

if (-not (Test-Path $Python)) {
    throw "DGAF MCP Python environment was not created successfully: $Python"
}

Write-Host "Installing exact local MCP dependency pin..."
& $Python -m pip install --upgrade pip
& $Python -m pip install -r $Requirements

Write-Host "Compiling local operator adapter..."
& $Python -m py_compile $Adapter
& $Python -m py_compile $Bridge

Write-Host "Checking non-authorizing bridge status..."
'{"action":"status"}' | & $Python $Bridge

Write-Host ""
Write-Host "DGAF local MCP bootstrap complete."
Write-Host "No materialization was performed."
Write-Host "Primary analysis remains NOT AUTHORIZED / NOT RUN."
Write-Host ""
Write-Host "Host command:"
Write-Host "  $Python"
Write-Host "Host argument:"
Write-Host "  $Adapter"
