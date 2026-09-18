Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
$VenvDir = Join-Path $RepoRoot ".venv-epoch002-autopilot"
$Python = Join-Path $VenvDir "Scripts\python.exe"
$Requirements = Join-Path $RepoRoot "requirements-ci.txt"
$Autopilot = Join-Path $RepoRoot "scripts\run_track_a_epoch_002_local_autopilot.py"

if (-not (Test-Path $VenvDir)) {
    Write-Host "Creating isolated Epoch 002 autopilot environment..."
    py -3 -m venv $VenvDir
}

if (-not (Test-Path $Python)) {
    throw "Autopilot Python environment is unavailable: $Python"
}

Write-Host "Installing pinned/declared DGAF CI dependencies..."
& $Python -m pip install -r $Requirements
if ($LASTEXITCODE -ne 0) {
    throw "Dependency installation failed."
}

Write-Host "Starting bounded Epoch 002 local autopilot..."
Write-Host "Custody secrets remain local. An encrypted private key may prompt locally for its passphrase."
& $Python $Autopilot
exit $LASTEXITCODE
