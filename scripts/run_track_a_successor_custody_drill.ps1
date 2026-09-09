param(
    [string]$OutputDir = "",
    [string]$BackupA = "",
    [string]$BackupB = "",
    [switch]$ValidateOnly
)

Set-StrictMode -Version Latest
$ErrorActionPreference = "Stop"

$RepoRoot = Split-Path -Parent $PSScriptRoot
$PythonDrill = Join-Path $PSScriptRoot "run_track_a_successor_custody_drill.py"
$ReceiptValidator = Join-Path $PSScriptRoot "validate_track_a_successor_solo_custody_receipt.py"

function Resolve-PythonCommand {
    $py = Get-Command py -ErrorAction SilentlyContinue
    if ($null -ne $py) {
        return [PSCustomObject]@{ Exe = $py.Source; Prefix = @("-3") }
    }

    $python = Get-Command python -ErrorAction SilentlyContinue
    if ($null -ne $python) {
        return [PSCustomObject]@{ Exe = $python.Source; Prefix = @() }
    }

    throw "Python 3 was not found. Install Python 3 or make 'py'/'python' available on PATH."
}

function Resolve-OpenSSL {
    $openssl = Get-Command openssl -ErrorAction SilentlyContinue
    if ($null -ne $openssl) {
        return $openssl.Source
    }

    $candidates = @()
    if ($env:ProgramFiles) {
        $candidates += (Join-Path $env:ProgramFiles "Git\usr\bin\openssl.exe")
        $candidates += (Join-Path $env:ProgramFiles "Git\mingw64\bin\openssl.exe")
    }
    $programFilesX86 = [Environment]::GetFolderPath("ProgramFilesX86")
    if ($programFilesX86) {
        $candidates += (Join-Path $programFilesX86 "Git\usr\bin\openssl.exe")
        $candidates += (Join-Path $programFilesX86 "Git\mingw64\bin\openssl.exe")
    }

    foreach ($candidate in $candidates) {
        if (Test-Path -LiteralPath $candidate -PathType Leaf) {
            return $candidate
        }
    }

    throw "OpenSSL was not found on PATH or in common Git-for-Windows locations."
}

if (-not (Test-Path -LiteralPath $PythonDrill -PathType Leaf)) {
    throw "Custody drill helper missing: $PythonDrill"
}
if (-not (Test-Path -LiteralPath $ReceiptValidator -PathType Leaf)) {
    throw "Receipt validator missing: $ReceiptValidator"
}

$pythonCommand = Resolve-PythonCommand
$opensslPath = Resolve-OpenSSL

if ($ValidateOnly) {
    Write-Output "TRACK_A_SUCCESSOR_WINDOWS_WRAPPER=PASS_VALIDATE_ONLY"
    Write-Output "PYTHON_FOUND=TRUE"
    Write-Output "OPENSSL_FOUND=TRUE"
    Write-Output "SECRET_GENERATION=FALSE"
    Write-Output "EMPIRICAL_COLLECTION_AUTHORIZED=FALSE"
    exit 0
}

if ([string]::IsNullOrWhiteSpace($OutputDir)) {
    $stamp = Get-Date -Format "yyyyMMdd-HHmmss"
    $OutputDir = Join-Path $HOME "DGAF-Custody-Working-$stamp"
}
if ([string]::IsNullOrWhiteSpace($BackupA)) {
    $BackupA = Read-Host "Enter encrypted recovery location A (must be outside the repository)"
}
if ([string]::IsNullOrWhiteSpace($BackupB)) {
    $BackupB = Read-Host "Enter encrypted recovery location B in a distinct storage class"
}

if ([string]::IsNullOrWhiteSpace($BackupA) -or [string]::IsNullOrWhiteSpace($BackupB)) {
    throw "Both recovery locations are required."
}

$opensslDir = Split-Path -Parent $opensslPath
$originalPath = $env:PATH
try {
    if (-not (($env:PATH -split [IO.Path]::PathSeparator) -contains $opensslDir)) {
        $env:PATH = "$opensslDir$([IO.Path]::PathSeparator)$env:PATH"
    }

    $arguments = @()
    $arguments += $pythonCommand.Prefix
    $arguments += $PythonDrill
    $arguments += @(
        "--output-dir", $OutputDir,
        "--backup-a", $BackupA,
        "--backup-b", $BackupB
    )

    Write-Output "Starting local custody drill. OpenSSL will prompt you directly for a new passphrase."
    Write-Output "Do not paste that passphrase into chat, GitHub, Notion, command arguments, or logs."

    & $pythonCommand.Exe @arguments
    if ($LASTEXITCODE -ne 0) {
        throw "The custody drill failed with exit code $LASTEXITCODE."
    }
}
finally {
    $env:PATH = $originalPath
}

$receipt = Join-Path $OutputDir "track_a_successor_solo_custody_receipt.json"
$certificate = Join-Path $OutputDir "track_a_successor_custody_cert.pem"

if (-not (Test-Path -LiteralPath $receipt -PathType Leaf)) {
    throw "Expected non-secret receipt was not created: $receipt"
}
if (-not (Test-Path -LiteralPath $certificate -PathType Leaf)) {
    throw "Expected public certificate was not created: $certificate"
}

Write-Output "TRACK_A_SUCCESSOR_WINDOWS_CUSTODY=PASS_LOCAL"
Write-Output "PUBLIC_CERTIFICATE=$certificate"
Write-Output "NONSECRET_RECEIPT=$receipt"
Write-Output "Only the public certificate and non-secret receipt are eligible for later repository review."
Write-Output "The encrypted private-key files and passphrase must remain outside GitHub, Notion, chat, and CI."
Write-Output "This drill does not authorize empirical collection."
