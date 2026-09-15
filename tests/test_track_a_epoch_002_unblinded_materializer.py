import io
import runpy
import tarfile
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATERIALIZER = ROOT / "scripts" / "materialize_track_a_epoch_002_unblinded_input.py"


def test_accepted_materializer_path_exists() -> None:
    assert MATERIALIZER.is_file(), "accepted Stage-1 materializer path is absent"


def test_source_preserves_operator_secret_and_analysis_boundary() -> None:
    text = MATERIALIZER.read_text(encoding="utf-8")
    assert "--custody-private-key" in text
    assert "--passphrase" not in text
    assert "--private-key-passphrase" not in text
    assert "track_a_epoch_002_analysis" not in text
    assert "PRIMARY_ANALYSIS=NOT_AUTHORIZED_NOT_RUN" in text


def test_exact_tar_reader_accepts_only_expected_regular_members() -> None:
    namespace = runpy.run_path(str(MATERIALIZER), run_name="epoch002_materializer")
    reader = namespace["read_exact_tar_members"]
    with tempfile.TemporaryDirectory(prefix="epoch002-tar-test-") as temp_dir:
        root = Path(temp_dir)
        safe = root / "safe.tar"
        with tarfile.open(safe, "w") as archive:
            payload = b"ok"
            info = tarfile.TarInfo("safe.txt")
            info.size = len(payload)
            archive.addfile(info, io.BytesIO(payload))
        assert reader(safe, frozenset({"safe.txt"}), "synthetic") == {"safe.txt": b"ok"}

        traversal = root / "traversal.tar"
        with tarfile.open(traversal, "w") as archive:
            payload = b"escape"
            info = tarfile.TarInfo("../escape.txt")
            info.size = len(payload)
            archive.addfile(info, io.BytesIO(payload))
        try:
            reader(traversal, frozenset({"safe.txt"}), "synthetic")
        except SystemExit:
            pass
        else:
            raise AssertionError("path traversal member was not rejected")

        linked = root / "linked.tar"
        with tarfile.open(linked, "w") as archive:
            info = tarfile.TarInfo("safe.txt")
            info.type = tarfile.SYMTYPE
            info.linkname = "elsewhere"
            archive.addfile(info)
        try:
            reader(linked, frozenset({"safe.txt"}), "synthetic")
        except SystemExit:
            pass
        else:
            raise AssertionError("symlink member was not rejected")
