"""Materialize Track A Epoch 002 into a bounded, non-analytical input record.

This utility verifies the locked public/protected artifacts and the bounded
unblinding authorization before decrypting protected topology mappings with an
operator-supplied custody key.  It does not perform primary analysis.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import tarfile
import tempfile
from pathlib import Path
from typing import Any

OUTPUT_NAME = "track_a_epoch_002_unblinded_analysis_input.json"
PRIMARY_ANALYSIS = "NOT_AUTHORIZED_NOT_RUN"
PROTOCOL = "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-002"
SEEDS = range(20270201, 20270251)


def fail(message: str) -> None:
    raise SystemExit(f"materialization refused: {message}")


def canonical(value: Any) -> bytes:
    return (json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=False) + "\n").encode()


def digest_bytes(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def digest_file(path: Path) -> str:
    return digest_bytes(path.read_bytes())


def read_exact_tar_members(path: Path, expected: frozenset[str], label: str) -> dict[str, bytes]:
    try:
        with tarfile.open(path, "r:*") as archive:
            members = archive.getmembers()
            actual = {member.name for member in members}
            if actual != set(expected):
                fail(f"{label} member set does not match contract")
            output: dict[str, bytes] = {}
            for member in members:
                if (
                    not member.isfile()
                    or member.issym()
                    or member.islnk()
                    or member.name.startswith("/")
                    or ".." in Path(member.name).parts
                ):
                    fail(f"{label} contains unsafe member")
                handle = archive.extractfile(member)
                if handle is None:
                    fail(f"{label} cannot read member")
                assert handle is not None
                output[member.name] = handle.read()
            return output
    except (OSError, tarfile.TarError) as error:
        fail(f"{label} cannot be read: {error}")
    raise AssertionError("unreachable")


def verify_sidecar(members: dict[str, bytes], name: str, label: str) -> None:
    sidecar = name + ".sha256"
    if sidecar not in members:
        fail(f"{label} missing digest sidecar")
    expected = f"{digest_bytes(members[name])}  {name}\n".encode()
    if members[sidecar] != expected:
        fail(f"{label} digest sidecar mismatch")


def load_json(value: bytes, label: str) -> dict[str, Any]:
    try:
        parsed = json.loads(value)
    except json.JSONDecodeError as error:
        fail(f"{label} is not valid JSON: {error}")
    if not isinstance(parsed, dict):
        fail(f"{label} must be an object")
    return parsed


def require(condition: bool, message: str) -> None:
    if not condition:
        fail(message)


def validate_contracts(
    contracts: dict[str, Any], public_archive: Path, protected_archive: Path
) -> tuple[dict[str, Any], dict[str, Any]]:
    evidence = contracts.get("dataset_lock_evidence")
    receipt = contracts.get("dataset_lock_receipt")
    decision = contracts.get("unblinding_decision")
    require(isinstance(evidence, dict), "dataset-lock evidence is required")
    require(isinstance(receipt, dict), "dataset-lock receipt is required")
    require(isinstance(decision, dict), "unblinding decision is required")
    assert isinstance(evidence, dict)
    assert isinstance(receipt, dict)
    assert isinstance(decision, dict)

    receipt_sha = digest_bytes(canonical(receipt))
    require(contracts.get("dataset_lock_receipt_sha256") == receipt_sha, "receipt digest mismatch")
    require(
        contracts.get("unblinding_decision_sha256") == digest_bytes(canonical(decision)),
        "decision digest mismatch",
    )
    require(receipt.get("record_type") == "DATASET_LOCK_RECEIPT", "receipt record type mismatch")
    require(receipt.get("status") == "PASS", "dataset lock is not PASS")
    require(
        decision.get("evidence_scope") == "CONTROLLED_MAPPING_RELEASE_OR_DECRYPTION_ONLY",
        "unblinding scope exceeds bounded release",
    )
    require(decision.get("status") == "PASS", "unblinding decision is not PASS")
    require(receipt.get("record_id") in decision.get("predecessor_record_ids", []), "receipt predecessor missing")
    immutable_subject = decision.get("immutable_subject")
    require(
        isinstance(immutable_subject, dict) and immutable_subject.get("sha256") == receipt_sha,
        "decision does not bind receipt",
    )

    public = evidence.get("public_artifact")
    protected = evidence.get("protected_artifact")
    require(isinstance(public, dict) and isinstance(protected, dict), "artifact evidence is required")
    assert isinstance(public, dict)
    assert isinstance(protected, dict)
    require(public.get("archive_sha256") == digest_file(public_archive), "public archive digest mismatch")
    require(protected.get("archive_sha256") == digest_file(protected_archive), "protected archive digest mismatch")
    require(evidence.get("protocol_id") == PROTOCOL, "evidence protocol mismatch")
    require(evidence.get("paired_seed_units") == 50, "evidence seed count mismatch")
    require(evidence.get("blinded_observations") == 2250, "evidence observation count mismatch")
    return evidence, protected


def decrypt_cms(ciphertext: bytes, certificate: Path, private_key: Path, destination: Path) -> None:
    try:
        subprocess.run(
            [
                "openssl",
                "cms",
                "-decrypt",
                "-binary",
                "-inform",
                "DER",
                "-in",
                str(destination.with_suffix(".cms")),
                "-recip",
                str(certificate),
                "-inkey",
                str(private_key),
                "-out",
                str(destination),
            ],
            input=None,
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except (OSError, subprocess.CalledProcessError) as error:
        fail(f"protected mapping decrypt failed: {error}")


def materialize(
    public_archive: Path,
    protected_archive: Path,
    custody_private_key: Path,
    output_dir: Path,
    *,
    contracts: dict[str, Any],
) -> dict[str, Any]:
    public_archive = Path(public_archive)
    protected_archive = Path(protected_archive)
    custody_private_key = Path(custody_private_key)
    output_dir = Path(output_dir)
    require(public_archive.is_file(), "public archive is absent")
    require(protected_archive.is_file(), "protected archive is absent")
    require(custody_private_key.is_file(), "operator custody private key is absent")
    evidence, protected_evidence = validate_contracts(contracts, public_archive, protected_archive)

    public_expected = {
        "track_a_epoch_002_manifest.json",
        "track_a_epoch_002_manifest.json.sha256",
    }
    for seed in SEEDS:
        name = f"track_a_epoch_002_seed_{seed}.json"
        public_expected.update({name, name + ".sha256"})
    public_members = read_exact_tar_members(public_archive, frozenset(public_expected), "public archive")
    for name in sorted(public_expected):
        if not name.endswith(".sha256"):
            verify_sidecar(public_members, name, "public archive")

    manifest = load_json(public_members["track_a_epoch_002_manifest.json"], "manifest")
    require(manifest.get("protocol_id") == PROTOCOL, "manifest protocol mismatch")
    require(manifest.get("seed_count") == 50, "manifest seed count mismatch")
    require(manifest.get("expected_observations") == 2250, "manifest observation count mismatch")
    require(
        evidence["public_artifact"].get("manifest_sha256")
        == digest_bytes(public_members["track_a_epoch_002_manifest.json"]),
        "manifest digest mismatch",
    )

    outer_expected = frozenset(
        {
            "track_a_epoch_002_custody_cert.pem",
            "track_a_epoch_002_custody_cert.sha256",
            "track_a_epoch_002_protected.cms",
            "track_a_epoch_002_protected_ciphertext.sha256",
            "track_a_epoch_002_protected_plaintext_tar.sha256",
        }
    )
    outer = read_exact_tar_members(protected_archive, outer_expected, "protected archive")
    expected_certificate = (
        f"{digest_bytes(outer['track_a_epoch_002_custody_cert.pem'])}  track_a_epoch_002_custody_cert.pem\n".encode()
    )
    require(
        outer["track_a_epoch_002_custody_cert.sha256"] == expected_certificate,
        "custody certificate sidecar mismatch",
    )
    expected_ciphertext = (
        f"{digest_bytes(outer['track_a_epoch_002_protected.cms'])}  track_a_epoch_002_protected.cms\n".encode()
    )
    require(
        outer["track_a_epoch_002_protected_ciphertext.sha256"] == expected_ciphertext,
        "ciphertext sidecar mismatch",
    )
    require(
        protected_evidence.get("ciphertext_sha256") == digest_bytes(outer["track_a_epoch_002_protected.cms"]),
        "ciphertext digest mismatch",
    )
    require(
        protected_evidence.get("custody_certificate_sha256")
        == digest_bytes(outer["track_a_epoch_002_custody_cert.pem"]),
        "custody certificate digest mismatch",
    )

    with tempfile.TemporaryDirectory(prefix="epoch002-materialize-") as temporary:
        work = Path(temporary)
        certificate = work / "custody-cert.pem"
        ciphertext = work / "protected.cms"
        plaintext = work / "protected.tar"
        certificate.write_bytes(outer["track_a_epoch_002_custody_cert.pem"])
        ciphertext.write_bytes(outer["track_a_epoch_002_protected.cms"])
        decrypt_cms(ciphertext.read_bytes(), certificate, custody_private_key, plaintext)
        require(
            outer["track_a_epoch_002_protected_plaintext_tar.sha256"]
            == f"{digest_file(plaintext)}  track_a_epoch_002_protected.tar\n".encode(),
            "protected plaintext digest mismatch",
        )
        require(protected_evidence.get("plaintext_tar_sha256") == digest_file(plaintext), "plaintext evidence mismatch")

        protected_expected = {
            "track_a_epoch_002_blinding_key_custody.json",
            "track_a_epoch_002_blinding_key_custody.json.sha256",
        }
        for seed in SEEDS:
            name = f"track_a_epoch_002_mapping_{seed}.json"
            protected_expected.update({name, name + ".sha256"})
        protected_members = read_exact_tar_members(plaintext, frozenset(protected_expected), "protected plaintext")
        for name in sorted(protected_expected):
            if not name.endswith(".sha256"):
                verify_sidecar(protected_members, name, "protected plaintext")

    records: list[dict[str, Any]] = []
    for seed in SEEDS:
        public_name = f"track_a_epoch_002_seed_{seed}.json"
        mapping_name = f"track_a_epoch_002_mapping_{seed}.json"
        public_document = load_json(public_members[public_name], public_name)
        mapping_document = load_json(protected_members[mapping_name], mapping_name)
        mapping = mapping_document.get("mapping")
        source_records = public_document.get("records")
        require(isinstance(mapping, dict) and isinstance(source_records, list), f"seed {seed} malformed")
        assert isinstance(mapping, dict)
        assert isinstance(source_records, list)
        require(public_document.get("seed_id") == seed and mapping_document.get("seed_id") == seed, "seed mismatch")
        for row in source_records:
            require(isinstance(row, dict), f"seed {seed} record malformed")
            blinded_id = row.get("blinded_topology_id")
            topology = mapping.get(blinded_id)
            require(isinstance(topology, str), f"seed {seed} mapping is incomplete")
            output_row = dict(row)
            output_row["topology"] = topology
            records.append(output_row)

    require(len(records) == 2250, "materialized record count mismatch")
    output = {
        "record_type": "TRACK_A_EPOCH_002_UNBLINDED_ANALYSIS_INPUT",
        "schema_version": 1,
        "protocol_id": PROTOCOL,
        "paired_seed_units": 50,
        "record_count": len(records),
        "records": records,
        "primary_analysis_authorized": False,
        "primary_analysis_run": False,
        "outcome_aggregation_performed": False,
        "scientific_n_increment": 0,
        "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        "primary_analysis_status": PRIMARY_ANALYSIS,
    }
    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / OUTPUT_NAME
    payload = canonical(output)
    destination.write_bytes(payload)
    return {"output_path": str(destination), "materialized_input_sha256": digest_bytes(payload)}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--public-archive", type=Path, required=True)
    parser.add_argument("--protected-archive", type=Path, required=True)
    parser.add_argument("--custody-private-key", type=Path, required=True)
    parser.add_argument("--contracts-json", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    contracts = load_json(args.contracts_json.read_bytes(), "contracts")
    materialize(
        args.public_archive,
        args.protected_archive,
        args.custody_private_key,
        args.output_dir,
        contracts=contracts,
    )


if __name__ == "__main__":
    main()
