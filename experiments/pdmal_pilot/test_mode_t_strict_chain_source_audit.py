from __future__ import annotations

from pathlib import Path

import pytest

from experiments.pdmal_pilot.mode_t_strict_chain_source_audit import AuditError, audit_sources


TLOCK_GO = """
type Tlock struct { trustChainhash bool }
func New(network Network) Tlock { return Tlock{trustChainhash: true} }
func (t Tlock) Strict() Tlock {
    t.trustChainhash = false
    return t
}
func (t Tlock) Decrypt() {
    _ = tleIdentity{network: t.network, trustChainhash: t.trustChainhash}
}
"""

TLOCK_AGE_GO = """
var ErrWrongChainhash = errors.New("invalid chainhash")
if t.network.ChainHash() != stanza.Args[1] {
    if t.trustChainhash {
        t.network.SwitchChainHash(invalid)
    }
}
"""

TLE_GO = """
case flags.Decrypt:
    err = tlock.New(network).Decrypt(dst, src)
"""


def _write(tmp_path: Path, name: str, text: str) -> Path:
    path = tmp_path / name
    path.write_text(text, encoding="utf-8")
    return path


def test_expected_pinned_semantics_pass(tmp_path: Path) -> None:
    result = audit_sources(
        _write(tmp_path, "tlock.go", TLOCK_GO),
        _write(tmp_path, "tlock_age.go", TLOCK_AGE_GO),
        _write(tmp_path, "tle.go", TLE_GO),
    )
    assert result["strict_method_available"] is True
    assert result["strict_disables_chainhash_switch"] is True
    assert result["stock_tle_decrypt_uses_strict"] is False
    assert result["stock_tle_acceptable_as_dgaf_strict_continuity_evidence"] is False
    assert result["dedicated_strict_continuity_verifier_still_required"] is True
    assert result["empirical_n"] == 0


def test_missing_strict_semantics_fail_closed(tmp_path: Path) -> None:
    broken = TLOCK_GO.replace("t.trustChainhash = false", "t.trustChainhash = true")
    with pytest.raises(AuditError):
        audit_sources(
            _write(tmp_path, "tlock.go", broken),
            _write(tmp_path, "tlock_age.go", TLOCK_AGE_GO),
            _write(tmp_path, "tle.go", TLE_GO),
        )


def test_missing_switch_path_fails_closed(tmp_path: Path) -> None:
    broken = TLOCK_AGE_GO.replace("t.network.SwitchChainHash(invalid)", "")
    with pytest.raises(AuditError):
        audit_sources(
            _write(tmp_path, "tlock.go", TLOCK_GO),
            _write(tmp_path, "tlock_age.go", broken),
            _write(tmp_path, "tle.go", TLE_GO),
        )


def test_unexpected_stock_cli_strict_change_fails_pinned_audit(tmp_path: Path) -> None:
    changed = TLE_GO.replace(
        "tlock.New(network).Decrypt(dst, src)",
        "tlock.New(network).Strict().Decrypt(dst, src)",
    )
    with pytest.raises(AuditError):
        audit_sources(
            _write(tmp_path, "tlock.go", TLOCK_GO),
            _write(tmp_path, "tlock_age.go", TLOCK_AGE_GO),
            _write(tmp_path, "tle.go", changed),
        )
