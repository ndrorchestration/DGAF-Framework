#!/usr/bin/env python3
"""Materialize the locked Track A Epoch 001 unblinded analysis input.

This utility does not run the primary analysis. It accepts the already-retained
blinded public artifact, the encrypted protected CMS bundle, and the separately
held custody private key only after the repository's one-file unblinding
authorization has been established. It verifies exact retained identities,
decrypts the protected mapping, joins topology labels to blinded records, and
emits one deterministic unblinded dataset plus SHA-256 sidecar.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import subprocess
import tarfile
import tempfile
import zipfile
from pathlib import Path
from typing import Any

AUTHORIZATION_SHA = "2e1981870a8455abed36fd72dcb3aaa35e2f9bff"
COLLECTION_AUTHORIZATION_SHA = "659aaa4dea2dd42624747952f1a47f307e69a014"
FROZEN_CANDIDATE_SHA = "961b9918002c4c68afac9c0fd5dd3e352e49b926"
PROTOCOL_ID = "PDMAL-TRACK-A-TOPOLOGY-ROBUSTNESS-EPOCH-001"
ALGORITHM_ID = "REFERENCE_NEIGHBOR_MEAN_ALPHA_0_5_V1"
PUBLIC_ARTIFACT_ARCHIVE_SHA256 = "32851068cc61421f756041d0671681823b38c054f06e5082ed26c800bf296231"
PROTECTED_ARTIFACT_ARCHIVE_SHA256 = "f52d2144cfb8c699347c56cf92a41c1ac11cba98787fefabb56891c9f680c69f"
PROTECTED_CIPHERTEXT_SHA256 = "15ba9d630cea0c26baca3ab50c33f7bcf10681a24293350b12acf3d4aeac4614"
PROTECTED_PLAINTEXT_TAR_SHA256 = "ec51a5451b63c5cbccfd83d01290f939d7a1832181af190c5fabd31fa806eb35"
CUSTODY_CERTIFICATE_SHA256 = "cfa468d1091f2179cfe0c96ff000bfe45ae7c5bd1414146fbb99c77572dba707"
SEEDS = tuple(range(20270101, 20270151))
TOPOLOGIES = {"ring", "pdmal", "random_regular", "small_world", "complete"}
FAILURE_COUNTS = {0, 1, 2, 3, 4, 5, 6, 8, 10}
EXPECTED_TOTAL = 2250


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def require(condition: bool, message: str) -> None:
    if not condition:
        raise SystemExit(f"Track A unblinding materialization refused: {message}")


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    require(isinstance(value, dict), f"{path.name} must contain a JSON object")
    return value


def verify_sidecar(path: Path) -> None:
    sidecar = path.with_suffix(path.suffix + ".sha256")
    require(sidecar.is_file(), f"missing sidecar for {path.name}")
    fields = sidecar.read_text(encoding="utf-8").strip().split()
    require(fields and fields[0] == sha256_file(path), f"sidecar mismatch for {path.name}")


def safe_extract_tar(tar_path: Path, destination: Path) -> None:
    with tarfile.open(tar_path, "r:") as archive:
        for member in archive.getmembers():
            target = (destination / member.name).resolve()
            require(str(target).startswith(str(destination.resolve())), "unsafe protected tar path")
        archive.extractall(destination)


def materialize(public_zip: Path, protected_zip: Path, private_key: Path, output: Path) -> None:
    require(public_zip.is_file(), "public artifact ZIP missing")
    require(protected_zip.is_file(), "protected artifact ZIP missing")
    require(private_key.is_file(), "custody private key missing")
    require(sha256_file(public_zip) == PUBLIC_ARTIFACT_ARCHIVE_SHA256, "public artifact archive digest mismatch")
    require(sha256_file(protected_zip) == PROTECTED_ARTIFACT_ARCHIVE_SHA256, "protected artifact archive digest mismatch")

    with tempfile.TemporaryDirectory(prefix="track-a-unblind-") as temp_name:
        root = Path(temp_name)
        public_root = root / "public"
        protected_root = root / "protected"
        decrypted_root = root / "decrypted"
        public_root.mkdir()
        protected_root.mkdir()
        decrypted_root.mkdir()

        with zipfile.ZipFile(public_zip) as archive:
            archive.extractall(public_root)
        with zipfile.ZipFile(protected_zip) as archive:
            archive.extractall(protected_root)

        public_dir = public_root / "track_a_epoch_001_public"
        require(public_dir.is_dir(), "expected public artifact directory missing")
        cipher = protected_root / "track_a_epoch_001_protected.cms"
        cert = protected_root / "track_a_epoch_001_custody_cert.pem"
        plaintext_digest_file = protected_root / "track_a_epoch_001_protected_plaintext_tar.sha256"
        require(cipher.is_file() and cert.is_file() and plaintext_digest_file.is_file(), "protected artifact members missing")
        require(sha256_file(cipher) == PROTECTED_CIPHERTEXT_SHA256, "protected ciphertext digest mismatch")
        require(sha256_file(cert) == CUSTODY_CERTIFICATE_SHA256, "custody certificate digest mismatch")

        decrypted_tar = root / "track_a_epoch_001_protected.tar"
        completed = subprocess.run(
            [
                "openssl",
                "cms",
                "-decrypt",
                "-binary",
                "-inform",
                "DER",
                "-in",
                str(cipher),
                "-recip",
                str(cert),
                "-inkey",
                str(private_key),
                "-out",
                str(decrypted_tar),
            ],
            check=False,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.PIPE,
            text=True,
        )
        require(completed.returncode == 0, "CMS decryption failed; private key/certificate mismatch or corrupt ciphertext")
        require(sha256_file(decrypted_tar) == PROTECTED_PLAINTEXT_TAR_SHA256, "decrypted protected tar digest mismatch")
        expected_plaintext_digest = plaintext_digest_file.read_text(encoding="utf-8").split()[0]
        require(expected_plaintext_digest == PROTECTED_PLAINTEXT_TAR_SHA256, "retained plaintext tar digest record mismatch")
        safe_extract_tar(decrypted_tar, decrypted_root)

        records: list[dict[str, Any]] = []
        seen_cells: set[tuple[int, str, int]] = set()
        mapping_hashes: dict[str, str] = {}

        for seed in SEEDS:
            public_path = public_dir / f"track_a_epoch_001_seed_{seed}.json"
            mapping_path = decrypted_root / f"track_a_epoch_001_mapping_{seed}.json"
            require(public_path.is_file(), f"public seed file missing for {seed}")
            require(mapping_path.is_file(), f"protected mapping missing for {seed}")
            verify_sidecar(public_path)
            verify_sidecar(mapping_path)

            public_doc = load_json(public_path)
            mapping_doc = load_json(mapping_path)
            require(public_doc.get("record_type") == "TRACK_A_EPOCH_001_BLINDED_SEED_DATASET", f"bad public record type for {seed}")
            require(public_doc.get("schema_version") == 2, f"bad public schema for {seed}")
            require(public_doc.get("seed_id") == seed, f"public seed mismatch for {seed}")
            require(public_doc.get("unblinding_authorized") is False, f"public artifact unexpectedly marked unblinded for {seed}")
            require(mapping_doc.get("record_type") == "TRACK_A_EPOCH_001_PROTECTED_TOPOLOGY_MAPPING", f"bad mapping record type for {seed}")
            require(mapping_doc.get("schema_version") == 2, f"bad mapping schema for {seed}")
            require(mapping_doc.get("seed_id") == seed, f"mapping seed mismatch for {seed}")
            require(mapping_doc.get("unblinding_authorized") is False, f"protected source artifact mutated for {seed}")
            require(mapping_doc.get("custody") == "PROTECTED_SAME_SYSTEM_NONINDEPENDENT", f"mapping custody mismatch for {seed}")

            mapping = mapping_doc.get("mapping")
            require(isinstance(mapping, dict) and len(mapping) == 5, f"mapping cardinality mismatch for {seed}")
            require(set(mapping.values()) == TOPOLOGIES, f"topology mapping set mismatch for {seed}")
            mapping_hashes[str(seed)] = sha256_file(mapping_path)

            seed_records = public_doc.get("records")
            require(isinstance(seed_records, list) and len(seed_records) == 45, f"public matrix size mismatch for {seed}")
            for record in seed_records:
                require(isinstance(record, dict), f"non-object public record for {seed}")
                blind_id = record.get("blinded_topology_id")
                require(isinstance(blind_id, str) and blind_id in mapping, f"unknown blinded topology for {seed}")
                topology = mapping[blind_id]
                failure_count = record.get("failure_count")
                require(isinstance(failure_count, int) and not isinstance(failure_count, bool), f"invalid failure count for {seed}")
                require(failure_count in FAILURE_COUNTS, f"unexpected failure count for {seed}")
                success = record.get("ffcr_success")
                require(isinstance(success, bool), f"non-boolean endpoint for {seed}")
                require(record.get("algorithm_id") == ALGORITHM_ID, f"algorithm identity mismatch for {seed}")
                require(record.get("protocol_id") == PROTOCOL_ID, f"protocol identity mismatch for {seed}")
                require(record.get("frozen_candidate_sha") == FROZEN_CANDIDATE_SHA, f"candidate identity mismatch for {seed}")
                require(record.get("excluded") is False, f"outcome exclusion present for {seed}")

                cell = (seed, topology, failure_count)
                require(cell not in seen_cells, f"duplicate unblinded cell {cell}")
                seen_cells.add(cell)
                records.append(
                    {
                        "protocol_id": PROTOCOL_ID,
                        "algorithm_id": ALGORITHM_ID,
                        "frozen_candidate_sha": FROZEN_CANDIDATE_SHA,
                        "seed_id": seed,
                        "topology": topology,
                        "failure_count": failure_count,
                        "ffcr_success": success,
                        "excluded": False,
                    }
                )

        require(len(records) == EXPECTED_TOTAL, "unblinded record count mismatch")
        expected_cells = {
            (seed, topology, failure_count)
            for seed in SEEDS
            for topology in TOPOLOGIES
            for failure_count in FAILURE_COUNTS
        }
        require(seen_cells == expected_cells, "unblinded matrix incomplete")

        output_doc = {
            "record_type": "TRACK_A_EPOCH_001_UNBLINDED_ANALYSIS_INPUT",
            "schema_version": 1,
            "protocol_id": PROTOCOL_ID,
            "authorization_sha": AUTHORIZATION_SHA,
            "collection_authorization_sha": COLLECTION_AUTHORIZATION_SHA,
            "frozen_candidate_sha": FROZEN_CANDIDATE_SHA,
            "paired_seed_units": 50,
            "record_count": EXPECTED_TOTAL,
            "mapping_source_sha256_by_seed": mapping_hashes,
            "records": sorted(records, key=lambda row: (row["seed_id"], row["topology"], row["failure_count"])),
            "primary_analysis_authorized": False,
            "primary_analysis_run": False,
            "outcome_aggregation_performed": False,
            "historical_pooling_allowed": False,
            "epoch_004_substitution_allowed": False,
            "high_assurance_authorized": False,
            "canonical_dgaf_efficacy": "NOT_ESTABLISHED",
        }
        payload = (json.dumps(output_doc, sort_keys=True, separators=(",", ":")) + "\n").encode()
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_bytes(payload)
        digest = hashlib.sha256(payload).hexdigest()
        output.with_suffix(output.suffix + ".sha256").write_text(f"{digest}  {output.name}\n", encoding="utf-8")

        # Ensure decrypted protected material cannot survive this process outside
        # the caller-selected unblinded output.
        decrypted_tar.unlink(missing_ok=True)
        shutil.rmtree(decrypted_root, ignore_errors=True)

        print("TRACK_A_EPOCH_001_UNBLINDED_INPUT_MATERIALIZED: 50 seeds; 2250 records")
        print(f"UNBLINDED_INPUT_SHA256={digest}")
        print("PRIMARY_ANALYSIS=NOT_AUTHORIZED_NOT_RUN")
        print("OUTCOME_AGGREGATION=NOT_PERFORMED")
        print("CANONICAL_DGAF_EFFICACY=NOT_ESTABLISHED")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--public-artifact-zip", type=Path, required=True)
    parser.add_argument("--protected-artifact-zip", type=Path, required=True)
    parser.add_argument("--custody-private-key", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    materialize(args.public_artifact_zip, args.protected_artifact_zip, args.custody_private_key, args.output)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
