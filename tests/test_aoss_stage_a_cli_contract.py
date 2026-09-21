import json

from scripts import run_aoss_v0_6_stage_a as cli


def test_preflight_success_surfaces_static_report_without_side_effects(
    tmp_path, monkeypatch, capsys
):
    dgaf = tmp_path / "dgaf"
    acp = tmp_path / "acp"
    dgaf.mkdir()
    acp.mkdir()
    expected = {
        "record_type": "AOSS_STAGE_A_STATIC_PREFLIGHT",
        "static_identity_checks": "PASS",
        "collection_readiness": "NOT_ESTABLISHED",
        "mapping_binding": "NOT_ESTABLISHED",
        "runtime_binding": "NOT_ESTABLISHED",
        "scientific_n_increment": 0,
        "outcomes_generated": False,
        "external_validation_established": False,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "high_assurance": "NOT_AUTHORIZED",
    }
    observed = {}

    def fake_inspect_preflight(observed_dgaf, observed_acp):
        observed["paths"] = (observed_dgaf, observed_acp)
        return expected

    monkeypatch.setattr(cli, "inspect_preflight", fake_inspect_preflight)

    exit_code = cli.main(
        [
            "preflight",
            "--dgaf-root",
            str(dgaf),
            "--acp-root",
            str(acp),
        ]
    )

    assert exit_code == 0
    assert observed["paths"] == (dgaf, acp)
    assert json.loads(capsys.readouterr().out) == expected
    assert list(tmp_path.iterdir()) == [dgaf, acp]
