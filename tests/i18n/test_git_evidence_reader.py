"""Real Git probes for the projection-local immutable object cache."""
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock

from tools.i18nlib import git_evidence_reader as reader
from tools.i18nlib import production_review_v2_lite_queue as queue
from tools.i18nlib import production_review as wp1


class GitEvidenceReaderTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.git("init", "-q")
        self.git("config", "user.email", "fixture@example.invalid")
        self.git("config", "user.name", "Fixture")
        (self.root / "a").write_bytes(b"same\n")
        (self.root / "b").write_bytes(b"same\n")
        self.commit()
        self.head = self.git("rev-parse", "HEAD").decode().strip()
        self.blob = self.git("rev-parse", "HEAD:a").decode().strip()

    def git(self, *args):
        return subprocess.check_output(["git", *args], cwd=self.root, stderr=subprocess.PIPE)

    def commit(self):
        self.git("add", ".")
        self.git("commit", "-qm", "fixture")

    def test_same_blob_at_two_paths_once_and_tree_consumer_cannot_mutate_cache(self):
        with mock.patch.object(queue, "_git", wraps=queue._git) as git:
            with reader.projection_scope(self.root):
                tree = queue._tree(self.root, self.head)
                self.assertEqual(queue._ordinary_blob(self.root, tree, "a"), b"same\n")
                self.assertEqual(queue._ordinary_blob(self.root, tree, "b"), b"same\n")
                tree.clear()
                self.assertEqual(set(queue._tree(self.root, self.head)), {"a", "b"})
            self.assertEqual([c.args[1] for c in git.call_args_list], ["ls-tree", "cat-file"])

    def test_nested_and_distinct_scopes_and_unscoped_reads(self):
        with mock.patch.object(queue, "_git", wraps=queue._git) as git:
            with reader.projection_scope(self.root):
                queue._blob(self.root, self.blob, "outer")
                with reader.projection_scope(self.root):
                    queue._blob(self.root, self.blob, "inner")
                queue._blob(self.root, self.blob, "outer again")
            with reader.projection_scope(self.root):
                queue._blob(self.root, self.blob, "new")
            queue._blob(self.root, self.blob, "unscoped")
            queue._blob(self.root, self.blob, "unscoped again")
            self.assertEqual(git.call_count, 5)

    def test_exceptions_restore_outer_scope_and_release_failed_projection(self):
        with mock.patch.object(queue, "_git", wraps=queue._git) as git:
            with reader.projection_scope(self.root):
                queue._blob(self.root, self.blob, "outer")
                with self.assertRaisesRegex(RuntimeError, "abort"):
                    with reader.projection_scope(self.root):
                        queue._blob(self.root, self.blob, "inner")
                        raise RuntimeError("abort")
                queue._blob(self.root, self.blob, "restored")
            with mock.patch.object(queue, "_projection_contents") as project:
                def fail(*args):
                    queue._blob(self.root, self.blob, "projection")
                    raise RuntimeError("abort")
                project.side_effect = fail
                for _ in range(2):
                    with self.assertRaisesRegex(RuntimeError, "abort"):
                        queue._projection(self.root, "HEAD")
            self.assertEqual(git.call_count, 4)

    def test_failed_blob_and_tree_reads_are_retried_with_current_label(self):
        for kind in ("blob", "tree"):
            with self.subTest(kind=kind), reader.projection_scope(self.root):
                operation = (lambda: queue._blob(self.root, self.blob, "current label")) if kind == "blob" else (lambda: queue._tree(self.root, self.head))
                original = queue._git
                with mock.patch.object(queue, "_git", side_effect=wp1.ProductionReviewError("read failed")):
                    with self.assertRaisesRegex(wp1.ProductionReviewError, "current label" if kind == "blob" else "read failed"):
                        operation()
                with mock.patch.object(queue, "_git", wraps=original) as git:
                    operation()
                    operation()
                    self.assertEqual(git.call_count, 1)

    def test_moved_head_alias_resolves_again_in_same_scope_and_process(self):
        with reader.projection_scope(self.root):
            old_tree = queue._tree(self.root, "HEAD")
            self.assertEqual(queue._blob(self.root, "HEAD:a", "alias"), b"same\n")
            (self.root / "a").write_bytes(b"changed\n")
            self.commit()
            new_tree = queue._tree(self.root, "HEAD")
            self.assertNotEqual(old_tree["a"], new_tree["a"])
            self.assertEqual(queue._blob(self.root, "HEAD:a", "alias"), b"changed\n")
        with reader.projection_scope(self.root):
            self.assertEqual(queue._tree(self.root, "HEAD"), new_tree)

    def test_commit_path_blob_and_tree_expressions_keep_git_semantics(self):
        (self.root / "dir").mkdir()
        (self.root / "dir" / "file").write_bytes(b"nested\n")
        self.commit()
        blob = self.git("rev-parse", "HEAD:dir/file").decode().strip()
        tree = self.git("rev-parse", "HEAD:dir").decode().strip()
        with reader.projection_scope(self.root):
            with mock.patch.object(queue, "_git", wraps=queue._git) as git:
                self.assertEqual(queue._blob(self.root, "HEAD:dir/file", "path"),
                                 self.git("cat-file", "blob", "HEAD:dir/file"))
                self.assertEqual(queue._blob(self.root, blob, "hash"), b"nested\n")
                self.assertEqual(queue._tree(self.root, "HEAD:dir"),
                                 {"file": ("100644", "blob", blob)})
                self.assertEqual(queue._tree(self.root, tree),
                                 {"file": ("100644", "blob", blob)})
            reads = [call.args[1:] for call in git.call_args_list
                     if call.args[1] in {"cat-file", "ls-tree"}]
            self.assertEqual(reads, [("cat-file", "blob", blob),
                                     ("ls-tree", "-rz", "--full-tree", "-r", tree)])

    def test_other_repo_does_not_reuse_cached_objects_it_does_not_have(self):
        with tempfile.TemporaryDirectory() as temporary:
            other = Path(temporary)
            subprocess.run(["git", "init", "-q", str(other)], check=True)
            with reader.projection_scope(self.root):
                queue._blob(self.root, self.blob, "present")
                queue._tree(self.root, self.head)
                with self.assertRaises(wp1.ProductionReviewError):
                    queue._blob(other, self.blob, "missing")
                with self.assertRaises(wp1.ProductionReviewError):
                    queue._tree(other, self.head)
                with reader.projection_scope(other):
                    with self.assertRaises(wp1.ProductionReviewError):
                        queue._blob(other, self.blob, "still missing")
                self.assertEqual(queue._blob(self.root, self.blob, "restored"), b"same\n")
