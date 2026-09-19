from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/run_track_a_epoch_002_primary_analysis_autopilot.ps1"


def source() -> str:
    return SCRIPT.read_text(encoding="utf-8")


def test_autopilot_uses_expected_local_paths_and_exact_runtime() -> None:
    text = source()

    assert "DGAF-Epoch002-Materialization" in text
    assert "track_a_epoch_002_unblinded_analysis_input.json" in text
    assert "DGAF-Epoch002-Analysis-Result" in text
    assert '$ExpectedPython = "3.12.0"' in text
    assert '$ExpectedNumPy = "2.5.1"' in text
    assert "requirements-full-lock.txt" in text
    assert "--require-hashes" in text


def test_autopilot_bootstraps_exact_python_side_by_side_when_needed() -> None:
    text = source()

    assert "https://dist.nuget.org/win-x86-commandline/latest/nuget.exe" in text
    assert "https://api.nuget.org/v3/index.json" in text
    assert '"install", "python"' in text
    assert '"-Version", $ExpectedPython' in text
    assert '"-ExcludeVersion"' in text
    assert "Get-AuthenticodeSignature" in text
    assert '"Microsoft"' in text
    assert "Python Software Foundation" in text
    assert "DGAF_EXACT_PYTHON_PROVISIONING=NUGET_SIDE_BY_SIDE" in text
    assert "python\\tools\\python.exe" in text


def test_autopilot_runs_preflight_before_empirical_execution() -> None:
    text = source()

    preflight = text.index('"--preflight-only"')
    execute = text.index('"--input", $InputPath')
    assert preflight < execute
    assert "AUTHORIZED" not in text[execute : execute + 150]


def test_autopilot_resumes_retained_output_without_reexecution() -> None:
    text = source()

    assert "RETAINED_LOCKED_ANALYSIS_OUTPUT=FOUND_RESUME_WITHOUT_REEXECUTION" in text
    assert "partial prior analysis output exists; refusing to overwrite or rerun" in text
    assert "refusing to reuse it" in text
    assert "without re-executing analysis" in text


def test_autopilot_never_reads_or_prints_numerical_result() -> None:
    text = source()

    forbidden = (
        "estimate_pdmal_minus_random_regular",
        "two_sided_95pct_percentile_ci",
        '"classification"',
        "ConvertFrom-Json",
    )
    for token in forbidden:
        assert token not in text

    assert "NUMERICAL_OUTCOME_DISPLAYED=FALSE" in text


def test_autopilot_admits_exactly_one_result_record_path() -> None:
    text = source()

    assert (
        "$ResultRecordRel = "
        '"docs/experiment/track_a_runs/'
        'TRACK_A_EPOCH_002_LOCKED_ANALYSIS_RESULT_RECORD.json"' in text
    )
    assert '"status", "--porcelain"' in text
    assert '$expectedStatus = "?? $ResultRecordRel"' in text
    assert '"--event-commit", "HEAD"' in text
    assert '"--accepted-parent", $attemptBase' in text


def test_autopilot_creates_draft_pr_and_preserves_nonpromotion() -> None:
    text = source()

    assert '"pr", "create"' in text
    assert '"--draft"' in text
    assert "EPOCH002_LOCKED_RESULT_ADMISSION_PR=" in text
    assert "SCIENTIFIC_N_INCREMENT=0" in text
    assert "CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED" in text
    assert "INDEPENDENT_VALIDATION=NOT_ESTABLISHED" in text
    assert "HIGH_ASSURANCE=NOT_AUTHORIZED" in text


def test_autopilot_retries_main_movement_without_rerunning_analysis() -> None:
    text = source()

    assert "Protected main moved during admission preparation" in text
    assert "for ($attempt = 1; $attempt -le 3" in text
    analysis_execution = text.index("Executing the already-authorized frozen primary analysis locally")
    retry_loop = text.index("for ($attempt = 1; $attempt -le 3")
    assert analysis_execution < retry_loop
