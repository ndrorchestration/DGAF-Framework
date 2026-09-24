param(
    [string]$AcpRoot = (Join-Path $HOME "DGAF-ACP-SelfTest"),
    [switch]$RefreshDependencies
)

$ErrorActionPreference = "Stop"
$ExpectedAcpCommit = "dbab7c1afafec524ce7c18157de2089cafe79c87"
$DgafRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$VenvRoot = Join-Path $HOME ".venvs\dgaf-operator-selftest"
$Python = Join-Path $VenvRoot "Scripts\python.exe"

function Invoke-Checked {
    param([scriptblock]$Command, [string]$Label)
    & $Command
    if ($LASTEXITCODE -ne 0) {
        throw "$Label failed with exit code $LASTEXITCODE"
    }
}

Write-Host "[DGAF] Operator self-test bootstrap"
Write-Host "DGAF: $DgafRoot"
Write-Host "ACP:  $AcpRoot"

if (-not (Get-Command py -ErrorAction SilentlyContinue)) {
    throw "Python launcher 'py' was not found. Install/use Python 3.12 before running this suite."
}

& py -3.12 -c "import sys; assert sys.version_info[:2] == (3, 12); print(sys.version)"
if ($LASTEXITCODE -ne 0) {
    throw "Python 3.12 is required."
}

if (-not (Test-Path $VenvRoot)) {
    Write-Host "[DGAF] Creating isolated Python 3.12 environment..."
    Invoke-Checked { & py -3.12 -m venv $VenvRoot } "venv creation"
    $RefreshDependencies = $true
}

if (-not (Test-Path $Python)) {
    throw "Expected virtualenv interpreter not found: $Python"
}

if ($RefreshDependencies) {
    Write-Host "[DGAF] Installing pinned repository test dependencies..."
    Invoke-Checked { & $Python -m pip install --upgrade "pip==26.2.1" } "pip bootstrap"
    Invoke-Checked { & $Python -m pip install -r (Join-Path $DgafRoot "requirements-ci.txt") "networkx==3.6.1" } "test dependency installation"
}

$PytestCheck = & $Python -c "import pytest, jsonschema, numpy, networkx; print('operator dependencies present')" 2>&1
if ($LASTEXITCODE -ne 0) {
    Write-Host $PytestCheck
    throw "Operator dependencies are missing. Re-run with -RefreshDependencies."
}
Write-Host $PytestCheck

if (-not (Test-Path $AcpRoot)) {
    Write-Host "[DGAF] Cloning frozen agent-control-plane target..."
    Invoke-Checked { & git clone "https://github.com/ndrorchestration/agent-control-plane.git" $AcpRoot } "ACP clone"
}

Invoke-Checked { & git -C $AcpRoot rev-parse --git-dir *> $null } "ACP repository check"

$AcpDirty = & git -C $AcpRoot status --porcelain=v1 --untracked-files=all
if ($LASTEXITCODE -ne 0) {
    throw "Could not inspect ACP worktree."
}
if ($AcpDirty) {
    throw "ACP self-test checkout is dirty. Clean it manually before testing: $AcpRoot"
}

Write-Host "[DGAF] Refreshing ACP refs and checking out frozen target..."
Invoke-Checked { & git -C $AcpRoot fetch --prune origin } "ACP fetch"
Invoke-Checked { & git -C $AcpRoot checkout --detach $ExpectedAcpCommit } "ACP frozen checkout"

$ObservedAcp = (& git -C $AcpRoot rev-parse HEAD).Trim()
if ($ObservedAcp -ne $ExpectedAcpCommit) {
    throw "ACP commit mismatch: expected $ExpectedAcpCommit, observed $ObservedAcp"
}

$DgafDirty = & git -C $DgafRoot status --porcelain=v1 --untracked-files=all
if ($LASTEXITCODE -ne 0) {
    throw "Could not inspect DGAF worktree."
}
if ($DgafDirty) {
    throw "DGAF checkout is dirty. Commit/stash/remove changes before operator self-testing."
}

Write-Host "[DGAF] Running bounded self-test..."
& $Python (Join-Path $DgafRoot "scripts\run_dgaf_operator_selftest.py") --dgaf-root $DgafRoot --acp-root $AcpRoot

$ExitCode = $LASTEXITCODE
if ($ExitCode -eq 0) {
    Write-Host "[DGAF] SELF-TEST PASS"
    Write-Host "Evidence retained under: $(Join-Path $HOME 'DGAF-Operator-SelfTest-Results')"
} else {
    Write-Host "[DGAF] SELF-TEST FAIL/BLOCKED"
    Write-Host "Inspect retained evidence under: $(Join-Path $HOME 'DGAF-Operator-SelfTest-Results')"
}
exit $ExitCode
