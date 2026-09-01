import hashlib
import subprocess
import tempfile
import unittest
from pathlib import Path
from tools.i18nlib import production_review_v2_lite_evidence as evidence
from tools.i18nlib.production_review import ProductionReviewError


class EvidenceBoundaryTests(unittest.TestCase):
    def test_exact_core_and_budget_helpers(self):
        self.assertEqual(evidence.sha256_bytes(b"x"), evidence.sha256_bytes(b"x"))
        self.assertEqual(evidence.prospective_bytes([b"a", b"b"]), 2)
        with self.assertRaises(ProductionReviewError):
            evidence.prospective_bytes([b"x"] * (evidence.MAX_TRACKED_BYTES + 1))

    def test_c41_snapshot_bytes_are_hashed_and_bound_to_git_blob(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.name", "Test"], cwd=root, check=True)
            source = b"source bytes\n"
            (root / "source.lua").write_bytes(source)
            subprocess.run(["git", "add", "source.lua"], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "source"], cwd=root, check=True)
            commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
            good = {"sha256": hashlib.sha256(source).hexdigest(),
                    "content_base64": "c291cmNlIGJ5dGVzCg=="}
            evidence.validate_source_evidence(root, "source.lua", commit, good)
            bad = {"sha256": hashlib.sha256(b"other").hexdigest(), "content": "other"}
            with self.assertRaises(ProductionReviewError):
                evidence.validate_source_evidence(root, "source.lua", commit, bad)

    def test_c43_staged_and_worktree_production_occupancy_is_conservative(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(["git", "init", "-q"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=root, check=True)
            subprocess.run(["git", "config", "user.name", "Test"], cwd=root, check=True)
            existing = root / "evidence/production-review/existing"
            existing.parent.mkdir(parents=True)
            existing.write_bytes(b"old")
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(["git", "commit", "-qm", "existing"], cwd=root, check=True)
            # A larger staged blob must not be hidden by the smaller worktree.
            existing.write_bytes(b"staged-large-content")
            subprocess.run(["git", "add", str(existing.relative_to(root))], cwd=root, check=True)
            existing.write_bytes(b"x")
            untracked = existing.parent / "untracked"
            untracked.write_bytes(b"untracked")
            candidate = root / "scratch" / "batch-test"
            candidate.mkdir(parents=True)
            (candidate / "manifest.json").write_bytes(b"candidate")
            self.assertEqual(evidence.prospective_tracked_bytes(root, candidate),
                             len(b"staged-large-content") + len(b"untracked") + len(b"candidate"))

    def test_symlink_is_fail_closed(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "real").write_bytes(b"x")
            (root / "link").symlink_to(root / "real")
            with self.assertRaises(ProductionReviewError):
                evidence.ordinary_files(root)


if __name__ == "__main__":
    unittest.main()
