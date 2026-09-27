from __future__ import annotations

import json

from scripts.run_dgaf_smoke_v1 import FIXTURES, SCHEMA, main, run_smoke


def test_dgaf_smoke_v1_passes_all_required_gates(monkeypatch):
    monkeypatch.setenv("DGAF_REVISION", "test-revision")
    result = run_smoke()

    assert result["schema"] == SCHEMA
    assert result["revision"] == "test-revision"
    assert result["outcome"] == "PASS"
    assert set(result["gates"]) == {
        "SMOKE_BOOT",
        "SMOKE_ROUTE",
        "SMOKE_EXECUTE",
        "SMOKE_PROVENANCE",
        "SMOKE_DENY",
        "SMOKE_STATE",
    }
    assert all(gate["outcome"] == "PASS" for gate in result["gates"].values())


def test_dgaf_smoke_v1_preserves_nonempirical_boundary():
    result = run_smoke()

    assert result["fixtures"] == {
        "allow": FIXTURES["allow"],
        "deny": FIXTURES["deny"],
        "ambiguous": FIXTURES["ambiguous"],
    }
    assert result["boundary"] == {
        "scientific_n_increment": 0,
        "authorization_effect": "NONE",
        "independent_validation": "NOT_ESTABLISHED",
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "high_assurance": "NOT_AUTHORIZED",
    }


def test_dgaf_smoke_v1_emits_machine_readable_result(tmp_path, monkeypatch):
    output = tmp_path / "result.json"
    monkeypatch.setattr(
        "sys.argv",
        ["run_dgaf_smoke_v1.py", "--output", str(output)],
    )

    assert main() == 0
    payload = json.loads(output.read_text(encoding="utf-8"))
    assert payload["schema"] == SCHEMA
    assert payload["outcome"] == "PASS"
    assert payload["gates"]["SMOKE_DENY"]["rejected"] is True
    assert payload["gates"]["SMOKE_STATE"]["promotion_blocked"] is True
