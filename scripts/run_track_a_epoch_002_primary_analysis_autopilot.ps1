[CmdletBinding()]
param(
    [string]$InputPath = (Join-Path $env:USERPROFILE "DGAF-Epoch002-Materialization\track_a_epoch_002_unblinded_analysis_input.json"),
    [string]$ResultDir = (Join-Path $env:USERPROFILE "DGAF-Epoch002-Analysis-Result"),
    [string]$RuntimeDir = (Join-Path $env:USERPROFILE "DGAF-Epoch002-Runtime")
)

$ErrorActionPreference = "Stop"
Set-StrictMode -Version Latest

$ExpectedRepo = "ndrorchestration/DGAF-Framework"
$ExpectedPython = "3.12.0"
$ExpectedNumPy = "2.5.1"
$PythonInstallerUrl = "https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe"
$ResultRecordRel = "docs/experiment/track_a_runs/TRACK_A_EPOCH_002_LOCKED_ANALYSIS_RESULT_RECORD.json"
$OutputName = "track_a_epoch_002_locked_primary_analysis_output.json"
$OutputSidecarName = "$OutputName.sha256"

function Fail([string]$Message) {
    throw "TRACK_A_EPOCH_002_ANALYSIS_AUTOPILOT_FAIL: $Message"
}

function Invoke-Checked {
    param(
        [Parameter(Mandatory = $true)][string]$FilePath,
        [Parameter(Mandatory = $true)][string[]]$Arguments,
        [string]$WorkingDirectory = ""
    )

    if ($WorkingDirectory) {
        Push-Location $WorkingDirectory
    }
    try {
        & $FilePath @Arguments
        if ($LASTEXITCODE -ne 0) {
            Fail "$FilePath exited with code $LASTEXITCODE"
        }
    }
    finally {
        if ($WorkingDirectory) {
            Pop-Location
        }
    }
}

function Invoke-Capture {
    param(
        [Parameter(Mandatory = $true)][string]$FilePath,
        [Parameter(Mandatory = $true)][string[]]$Arguments,
        [string]$WorkingDirectory = ""
    )

    if ($WorkingDirectory) {
        Push-Location $WorkingDirectory
    }
    try {
        $output = & $FilePath @Arguments 2>&1
        if ($LASTEXITCODE -ne 0) {
            Fail "$FilePath $($Arguments -join ' ') failed: $($output -join ' ')"
        }
        return (($output | ForEach-Object { "$_" }) -join [Environment]::NewLine).Trim()
    }
    finally {
        if ($WorkingDirectory) {
            Pop-Location
        }
    }
}

function Get-PythonVersion([string]$PythonExe) {
    if (-not (Test-Path -LiteralPath $PythonExe -PathType Leaf)) {
        return $null
    }
    try {
        $value = & $PythonExe -c "import platform; print(platform.python_version())" 2>$null
        if ($LASTEXITCODE -ne 0) {
            return $null
        }
        return ("$value").Trim()
    }
    catch {
        return $null
    }
}

function Find-ExactPython([string]$TargetRuntimeDir) {
    $candidates = New-Object System.Collections.Generic.List[string]
    $dedicated = Join-Path $TargetRuntimeDir "Python3120\python.exe"
    $candidates.Add($dedicated)

    $knownLocal = Join-Path $env:LOCALAPPDATA "Programs\Python\Python312\python.exe"
    $candidates.Add($knownLocal)

    try {
        $pyExe = (& py -3.12 -c "import sys; print(sys.executable)" 2>$null)
        if ($LASTEXITCODE -eq 0 -and $pyExe) {
            $candidates.Add(("$pyExe").Trim())
        }
    }
    catch {
    }

    try {
        $pythonCommand = Get-Command python -ErrorAction SilentlyContinue
        if ($pythonCommand -and $pythonCommand.Source) {
            $candidates.Add($pythonCommand.Source)
        }
    }
    catch {
    }

    foreach ($candidate in ($candidates | Select-Object -Unique)) {
        if ((Get-PythonVersion $candidate) -eq $ExpectedPython) {
            return $candidate
        }
    }
    return $null
}

function Install-DedicatedPython([string]$TargetRuntimeDir) {
    $pythonRoot = Join-Path $TargetRuntimeDir "Python3120"
    $pythonExe = Join-Path $pythonRoot "python.exe"
    if ((Get-PythonVersion $pythonExe) -eq $ExpectedPython) {
        return $pythonExe
    }

    New-Item -ItemType Directory -Force -Path $TargetRuntimeDir | Out-Null
    $installer = Join-Path $env:TEMP "dgaf-python-3.12.0-amd64.exe"

    Write-Host "Exact Python 3.12.0 is not installed. Installing a dedicated DGAF runtime in your user profile..."
    Invoke-WebRequest -Uri $PythonInstallerUrl -OutFile $installer -UseBasicParsing

    $signature = Get-AuthenticodeSignature -FilePath $installer
    if ($signature.Status -ne "Valid") {
        Remove-Item -Force -ErrorAction SilentlyContinue $installer
        Fail "downloaded Python installer does not have a valid Authenticode signature"
    }
    if (-not $signature.SignerCertificate -or $signature.SignerCertificate.Subject -notmatch "Python Software Foundation") {
        Remove-Item -Force -ErrorAction SilentlyContinue $installer
        Fail "downloaded Python installer signer is not the Python Software Foundation"
    }

    if (Test-Path $pythonRoot) {
        Remove-Item -Recurse -Force $pythonRoot
    }

    $arguments = @(
        "/quiet",
        "InstallAllUsers=0",
        "TargetDir=$pythonRoot",
        "Include_pip=1",
        "Include_launcher=0",
        "PrependPath=0",
        "Include_test=0",
        "Shortcuts=0"
    )
    $process = Start-Process -FilePath $installer -ArgumentList $arguments -Wait -PassThru
    Remove-Item -Force -ErrorAction SilentlyContinue $installer
    if ($process.ExitCode -ne 0) {
        Fail "Python 3.12.0 installer exited with code $($process.ExitCode)"
    }
    if ((Get-PythonVersion $pythonExe) -ne $ExpectedPython) {
        Fail "dedicated Python installation did not produce exact Python $ExpectedPython"
    }
    return $pythonExe
}

function Ensure-Venv {
    param(
        [string]$PythonExe,
        [string]$VenvPath,
        [string]$RequirementsPath,
        [switch]$RequireHashes,
        [string]$RequiredNumPy = ""
    )

    $venvPython = Join-Path $VenvPath "Scripts\python.exe"
    $reuse = $false
    if ((Get-PythonVersion $venvPython) -eq $ExpectedPython) {
        if ($RequiredNumPy) {
            try {
                $numpyVersion = & $venvPython -c "import numpy; print(numpy.__version__)" 2>$null
                if ($LASTEXITCODE -eq 0 -and ("$numpyVersion").Trim() -eq $RequiredNumPy) {
                    $reuse = $true
                }
            }
            catch {
            }
        }
        else {
            $reuse = $true
        }
    }

    if (-not $reuse) {
        if (Test-Path $VenvPath) {
            Remove-Item -Recurse -Force $VenvPath
        }
        Invoke-Checked $PythonExe @("-m", "venv", $VenvPath)
        $venvPython = Join-Path $VenvPath "Scripts\python.exe"
        $installArgs = @("-m", "pip", "install")
        if ($RequireHashes) {
            $installArgs += "--require-hashes"
        }
        $installArgs += @("-r", $RequirementsPath)
        Invoke-Checked $venvPython $installArgs
    }

    if ((Get-PythonVersion $venvPython) -ne $ExpectedPython) {
        Fail "virtual environment is not using exact Python $ExpectedPython"
    }
    if ($RequiredNumPy) {
        $numpyVersion = Invoke-Capture $venvPython @("-c", "import numpy; print(numpy.__version__)")
        if ($numpyVersion -ne $RequiredNumPy) {
            Fail "analysis environment NumPy mismatch: expected $RequiredNumPy, got $numpyVersion"
        }
    }
    return $venvPython
}

$gitCommand = Get-Command git -ErrorAction SilentlyContinue
if (-not $gitCommand) {
    Fail "Git is not installed or not available on PATH"
}
$git = $gitCommand.Source

$ghCommand = Get-Command gh -ErrorAction SilentlyContinue
if (-not $ghCommand) {
    Fail "GitHub CLI is not installed or not available on PATH"
}
$gh = $ghCommand.Source

$repoRoot = Invoke-Capture $git @("rev-parse", "--show-toplevel") (Get-Location).Path
$origin = Invoke-Capture $git @("remote", "get-url", "origin") $repoRoot
if ($origin -notmatch "github\.com[:/]ndrorchestration/DGAF-Framework(?:\.git)?$") {
    Fail "current repository origin is not $ExpectedRepo"
}

Invoke-Checked $gh @("auth", "status", "--hostname", "github.com")
if (-not (Test-Path -LiteralPath $InputPath -PathType Leaf)) {
    Fail "retained materialized input is missing at $InputPath"
}

Invoke-Checked $git @("fetch", "origin", "main") $repoRoot
$baseSha = Invoke-Capture $git @("rev-parse", "origin/main") $repoRoot

$canonicalResultCheck = & $git -C $repoRoot cat-file -e "origin/main:$ResultRecordRel" 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "TRACK_A_EPOCH_002_LOCKED_ANALYSIS_RESULT=ALREADY_ESTABLISHED"
    exit 0
}

$worktree = Join-Path $env:TEMP "DGAF-Epoch002-Analysis-Worktree"
if (Test-Path $worktree) {
    & $git -C $repoRoot worktree remove --force $worktree 2>$null
    if ($LASTEXITCODE -ne 0 -and (Test-Path $worktree)) {
        Remove-Item -Recurse -Force $worktree
    }
}
& $git -C $repoRoot worktree prune | Out-Null
Invoke-Checked $git @("worktree", "add", "--detach", $worktree, $baseSha) $repoRoot

$python = Find-ExactPython $RuntimeDir
if (-not $python) {
    $python = Install-DedicatedPython $RuntimeDir
}
Write-Host "DGAF_LOCKED_PYTHON=$python"

$analysisVenv = Join-Path $RuntimeDir "analysis-venv"
$analysisRequirements = Join-Path $worktree "experiments\pdmal_pilot\requirements-full-lock.txt"
$analysisPython = Ensure-Venv -PythonExe $python -VenvPath $analysisVenv -RequirementsPath $analysisRequirements -RequireHashes -RequiredNumPy $ExpectedNumPy

$runner = Join-Path $worktree "scripts\run_track_a_epoch_002_locked_primary_analysis.py"
Write-Host "Running non-executing authorization/runtime preflight..."
Invoke-Checked $analysisPython @($runner, "--preflight-only") $worktree

$outputFile = Join-Path $ResultDir $OutputName
$outputSidecar = Join-Path $ResultDir $OutputSidecarName
$outputExists = Test-Path -LiteralPath $outputFile -PathType Leaf
$sidecarExists = Test-Path -LiteralPath $outputSidecar -PathType Leaf

if ($outputExists -xor $sidecarExists) {
    Fail "partial prior analysis output exists; refusing to overwrite or rerun"
}

if (-not $outputExists) {
    if (Test-Path $ResultDir) {
        $existing = @(Get-ChildItem -LiteralPath $ResultDir -Force -ErrorAction SilentlyContinue)
        if ($existing.Count -gt 0) {
            Fail "analysis result directory already contains unknown files; refusing to reuse it"
        }
    }

    Write-Host "Executing the already-authorized frozen primary analysis locally..."
    Invoke-Checked $analysisPython @(
        $runner,
        "--input", $InputPath,
        "--output-dir", $ResultDir
    ) $worktree
}
else {
    Write-Host "RETAINED_LOCKED_ANALYSIS_OUTPUT=FOUND_RESUME_WITHOUT_REEXECUTION"
}

if (-not (Test-Path -LiteralPath $outputFile -PathType Leaf) -or -not (Test-Path -LiteralPath $outputSidecar -PathType Leaf)) {
    Fail "locked analysis did not produce the expected retained output bundle"
}

$outputDigest = (Get-FileHash -LiteralPath $outputFile -Algorithm SHA256).Hash.ToLowerInvariant()
Write-Host "LOCKED_ANALYSIS_OUTPUT_SHA256=$outputDigest"
Write-Host "NUMERICAL_OUTCOME_DISPLAYED=FALSE"

$toolingVenv = Join-Path $RuntimeDir "result-admission-venv"
$toolingRequirements = Join-Path $worktree "requirements-ci.txt"
$toolingPython = Ensure-Venv -PythonExe $python -VenvPath $toolingVenv -RequirementsPath $toolingRequirements

$admitted = $false
for ($attempt = 1; $attempt -le 3 -and -not $admitted; $attempt++) {
    Invoke-Checked $git @("fetch", "origin", "main") $repoRoot
    $attemptBase = Invoke-Capture $git @("rev-parse", "origin/main") $repoRoot

    $resultAlreadyExists = & $git -C $repoRoot cat-file -e "origin/main:$ResultRecordRel" 2>$null
    if ($LASTEXITCODE -eq 0) {
        Write-Host "TRACK_A_EPOCH_002_LOCKED_ANALYSIS_RESULT=ALREADY_ESTABLISHED"
        $admitted = $true
        break
    }

    if (Test-Path $worktree) {
        & $git -C $repoRoot worktree remove --force $worktree 2>$null
        if ($LASTEXITCODE -ne 0 -and (Test-Path $worktree)) {
            Remove-Item -Recurse -Force $worktree
        }
    }
    & $git -C $repoRoot worktree prune | Out-Null
    Invoke-Checked $git @("worktree", "add", "--detach", $worktree, $attemptBase) $repoRoot

    $candidate = Join-Path $env:TEMP "TRACK_A_EPOCH_002_LOCKED_ANALYSIS_RESULT_RECORD-$attempt.json"
    Remove-Item -Force -ErrorAction SilentlyContinue $candidate
    $preparer = Join-Path $worktree "scripts\prepare_track_a_epoch_002_locked_analysis_result_record.py"
    Invoke-Checked $toolingPython @(
        $preparer,
        "--analysis-output", $outputFile,
        "--output-record", $candidate,
        "--parent-ref", "HEAD"
    ) $worktree

    $branchName = "autopilot/epoch002-locked-result-{0}-{1}" -f (Get-Date).ToUniversalTime().ToString("yyyyMMdd-HHmmss"), $outputDigest.Substring(0, 8)
    Invoke-Checked $git @("switch", "-c", $branchName) $worktree

    $canonicalResult = Join-Path $worktree ($ResultRecordRel -replace "/", "\")
    New-Item -ItemType Directory -Force -Path (Split-Path -Parent $canonicalResult) | Out-Null
    Copy-Item -LiteralPath $candidate -Destination $canonicalResult

    $status = Invoke-Capture $git @("status", "--porcelain") $worktree
    $expectedStatus = "?? $ResultRecordRel"
    if ($status -ne $expectedStatus) {
        Fail "result admission worktree contains unexpected changes: $status"
    }

    Invoke-Checked $git @("add", "--", $ResultRecordRel) $worktree
    Invoke-Checked $git @("commit", "-m", "evidence(epoch002): admit locked analysis result content address") $worktree

    $validator = Join-Path $worktree "scripts\validate_track_a_epoch_002_locked_analysis_result.py"
    Invoke-Checked $toolingPython @(
        $validator,
        "--event-commit", "HEAD",
        "--accepted-parent", $attemptBase
    ) $worktree

    Invoke-Checked $git @("fetch", "origin", "main") $repoRoot
    $latestMain = Invoke-Capture $git @("rev-parse", "origin/main") $repoRoot
    if ($latestMain -ne $attemptBase) {
        Write-Host "Protected main moved during admission preparation; retrying without re-running analysis."
        & $git -C $repoRoot worktree remove --force $worktree 2>$null
        & $git -C $repoRoot branch -D $branchName 2>$null
        continue
    }

    Invoke-Checked $git @("push", "--set-upstream", "origin", $branchName) $worktree

    $prBody = @"
## Purpose

Admit the content address of the already-authorized, locally executed Track A Epoch 002 locked primary analysis output.

## Boundaries

- exactly one canonical repository result-record path;
- numerical estimate, confidence interval, and classification remain outside this PR;
- result record binds the accepted primary-analysis authorization event and retained local output SHA-256;
- authorization effect remains NONE;
- scientific N increment remains 0;
- canonical DGAF efficacy and independent validation remain NOT_ESTABLISHED;
- High-Assurance remains NOT AUTHORIZED.

This PR is result admission only, not interpretation or claim promotion.
"@

    $prUrl = Invoke-Capture $gh @(
        "pr", "create",
        "--repo", $ExpectedRepo,
        "--base", "main",
        "--head", $branchName,
        "--draft",
        "--title", "evidence(epoch002): admit locked analysis result content address",
        "--body", $prBody
    ) $worktree

    Write-Host "TRACK_A_EPOCH_002_LOCKED_PRIMARY_ANALYSIS=EXECUTED_LOCAL"
    Write-Host "TRACK_A_EPOCH_002_RESULT_RECORD_CANDIDATE=PREPARED"
    Write-Host "EPOCH002_LOCKED_RESULT_ADMISSION_PR=$prUrl"
    Write-Host "SCIENTIFIC_N_INCREMENT=0"
    Write-Host "CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED"
    Write-Host "INDEPENDENT_VALIDATION=NOT_ESTABLISHED"
    Write-Host "HIGH_ASSURANCE=NOT_AUTHORIZED"
    $admitted = $true
}

if (Test-Path $worktree) {
    & $git -C $repoRoot worktree remove --force $worktree 2>$null
    & $git -C $repoRoot worktree prune 2>$null
}

if (-not $admitted) {
    Fail "protected main moved repeatedly; retained analysis output is safe and the same command can be rerun to resume admission without re-executing analysis"
}

Write-Host "EPOCH002_ANALYSIS_AUTOPILOT=COMPLETE"
