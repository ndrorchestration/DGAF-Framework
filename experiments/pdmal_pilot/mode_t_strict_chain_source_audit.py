#!/usr/bin/env python3
"""Audit pinned drand/tlock source semantics relevant to DGAF P4-B strict-chain continuity.

This is engineering/source evidence only. It does not decrypt protected material,
instantiate custody, authorize P4, select W, freeze the protocol, or increase N.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

TLOCK_SOURCE_COMMIT = "7b54141a9733fd6fa207587a11148280e6fb020d"
QUICKNET_CHAIN_HASH = "52db9ba70e0cc0f6eaf7803dd07447a1f5477735fd3f661792ba94600c84e971"
QUICKNET_SCHEME = "bls-unchained-g1-rfc9380"


class AuditError(RuntimeError):
    pass


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit_sources(tlock_go: Path, tlock_age_go: Path, tle_go: Path) -> dict[str, object]:
    tlock_text = tlock_go.read_text(encoding="utf-8")
    age_text = tlock_age_go.read_text(encoding="utf-8")
    tle_text = tle_go.read_text(encoding="utf-8")

    required_tlock = (
        "trustChainhash: true",
        "func (t Tlock) Strict() Tlock",
        "t.trustChainhash = false",
        "tleIdentity{network: t.network, trustChainhash: t.trustChainhash}",
    )
    required_age = (
        "if t.network.ChainHash() != stanza.Args[1]",
        "if t.trustChainhash",
        "t.network.SwitchChainHash(invalid)",
        "ErrWrongChainhash",
    )
    required_tle = ("tlock.New(network).Decrypt(dst, src)",)

    missing = [needle for needle in required_tlock if needle not in tlock_text]
    missing += [needle for needle in required_age if needle not in age_text]
    missing += [needle for needle in required_tle if needle not in tle_text]
    if missing:
        raise AuditError(f"required pinned-source semantics missing: {missing}")

    stock_cli_strict = ".Strict().Decrypt(dst, src)" in tle_text
    if stock_cli_strict:
        raise AuditError("pinned stock tle unexpectedly uses Strict() for decryption")

    result = {
        "schema_version": 1,
        "evidence_class": "P4_B_MODE_T_PINNED_SOURCE_AUDIT_V1",
        "tlock_source_commit": TLOCK_SOURCE_COMMIT,
        "quicknet_chain_hash": QUICKNET_CHAIN_HASH,
        "quicknet_scheme": QUICKNET_SCHEME,
        "source_sha256": {
            "tlock.go": _sha256(tlock_go),
            "tlock_age.go": _sha256(tlock_age_go),
            "cmd/tle/tle.go": _sha256(tle_go),
        },
        "new_defaults_to_trust_ciphertext_chainhash": True,
        "strict_method_available": True,
        "strict_disables_chainhash_switch": True,
        "wrong_chainhash_has_explicit_error": True,
        "stock_tle_decrypt_uses_strict": False,
        "stock_tle_acceptable_as_dgaf_strict_continuity_evidence": False,
        "dedicated_strict_continuity_verifier_still_required": True,
        "empirical_data_collection": False,
        "secret_instantiation": False,
        "freeze_established": False,
        "pilot_authorized": False,
        "empirical_n": 0,
    }
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--tlock-go", type=Path, required=True)
    parser.add_argument("--tlock-age-go", type=Path, required=True)
    parser.add_argument("--tle-go", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()

    result = audit_sources(args.tlock_go, args.tlock_age_go, args.tle_go)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    raw = json.dumps(result, indent=2, sort_keys=True) + "\n"
    args.output.write_text(raw, encoding="utf-8")
    digest = hashlib.sha256(raw.encode("utf-8")).hexdigest()
    args.output.with_suffix(args.output.suffix + ".sha256").write_text(
        f"{digest}  {args.output.name}\n", encoding="utf-8"
    )
    print(json.dumps({"status": "PASS", "evidence_sha256": digest}, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
