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

    def test_blob_cache_is_a_bounded_lru_and_oversize_blobs_are_never_retained(self):
        with reader.projection_scope(self.root):
            scope_reader = reader.active_reader(self.root)
            self.assertIsNotNone(scope_reader)
            loads: list[str] = []

            def loader(object_id, data):
                def load():
                    loads.append(object_id)
                    return data
                return load

            with mock.patch.object(reader, "BLOB_CACHE_LIMIT_BYTES", 8):
                self.assertEqual(scope_reader.read("blob", "first", loader("first", b"12345678")), b"12345678")
                self.assertEqual(scope_reader.read("blob", "first", loader("first", b"rerun")), b"12345678")
                self.assertEqual(loads, ["first"])
                self.assertEqual(scope_reader.blob_bytes, 8)
                # Inserting another 8-byte blob evicts the least-recently-used one.
                scope_reader.read("blob", "second", loader("second", b"abcdefgh"))
                self.assertEqual(list(scope_reader.blobs), ["second"])
                self.assertEqual(scope_reader.blob_bytes, 8)
                # An evicted blob is reloaded and its bytes are still equal.
                self.assertEqual(scope_reader.read("blob", "first", loader("first", b"12345678")), b"12345678")
                self.assertEqual(loads, ["first", "second", "first"])
                # A blob over the budget is returned uncached and never counted.
                before = scope_reader.blob_bytes
                self.assertEqual(scope_reader.read("blob", "big", loader("big", b"123456789")), b"123456789")
                self.assertNotIn("big", scope_reader.blobs)
                self.assertEqual(scope_reader.blob_bytes, before)
                scope_reader.read("blob", "big", loader("big", b"123456789"))
                self.assertEqual(loads, ["first", "second", "first", "big", "big"])

    def test_blob_failure_is_not_cached_and_retry_uses_the_current_loader(self):
        with reader.projection_scope(self.root):
            scope_reader = reader.active_reader(self.root)
            calls = []

            def failing():
                calls.append("fail")
                raise wp1.ProductionReviewError("read failed")

            with self.assertRaisesRegex(wp1.ProductionReviewError, "read failed"):
                scope_reader.read("blob", "flaky", failing)
            self.assertNotIn("flaky", scope_reader.blobs)
            self.assertEqual(scope_reader.read("blob", "flaky", lambda: b"recovered"), b"recovered")
            self.assertEqual(calls, ["fail"])

    def test_row_and_tuple_pools_share_complete_equals_never_revisions(self):
        with reader.projection_scope(self.root):
            scope_reader = reader.active_reader(self.root)
            row = {"entry_revision_identity": "rev", "target": "x", "risk": {"args_order": None}}
            equal = {"entry_revision_identity": "rev", "target": "x", "risk": {"args_order": None}}
            digest_a, canonical_a = scope_reader.intern_row("D1", row)
            self.assertIs(canonical_a, row)
            digest_b, canonical_b = scope_reader.intern_row("D1", equal)
            self.assertIs(canonical_b, row)
            self.assertIs(digest_a, digest_b)
            # The same revision with a different digest/content must not merge.
            provenance = {"entry_revision_identity": "rev", "target": "y", "risk": {"args_order": None}}
            _digest_c, canonical_c = scope_reader.intern_row("D2", provenance)
            self.assertIs(canonical_c, provenance)
            # A digest collision (equal digest, unequal row) is never trusted.
            collision = {"entry_revision_identity": "rev", "target": "z", "risk": {"args_order": None}}
            _digest_d, canonical_d = scope_reader.intern_row("D1", collision)
            self.assertIs(canonical_d, collision)
            self.assertIs(scope_reader.rows["D1"][1], row)
            # The module wrapper refuses to guess a scope outside a projection.
            self.assertEqual(reader.intern_row(self.root, "D9", row), ("D9", row))
            first = ("logical", "unchanged", "logical", "rev")
            self.assertIs(scope_reader.intern_tuple(first), first)
            self.assertIs(scope_reader.intern_tuple(tuple(first)), first)
            self.assertEqual(reader.intern_tuple(self.root, first), first)

    def test_pools_are_scope_local_and_cleared_on_normal_and_failed_exit(self):
        with reader.projection_scope(self.root):
            outer = reader.active_reader(self.root)
            outer.intern_row("outer", {"entry_revision_identity": "outer", "target": "o"})
            outer.intern_tuple(("outer", "unchanged", "outer", "outer"))
            with reader.projection_scope(self.root):
                inner = reader.active_reader(self.root)
                self.assertIsNot(inner, outer)
                self.assertEqual(inner.rows, {})
                self.assertEqual(inner.tuples, {})
                inner.intern_row("inner", {"entry_revision_identity": "inner", "target": "i"})
                inner.intern_tuple(("inner", "unchanged", "inner", "inner"))
                self.assertIn("inner", inner.rows)
            self.assertNotIn("inner", outer.rows)
            self.assertEqual(set(outer.rows), {"outer"})
            self.assertEqual(set(outer.tuples), {("outer", "unchanged", "outer", "outer")})
            with self.assertRaisesRegex(RuntimeError, "abort"):
                with reader.projection_scope(self.root):
                    failed = reader.active_reader(self.root)
                    failed.intern_row("failed", {"entry_revision_identity": "failed", "target": "f"})
                    raise RuntimeError("abort")
            self.assertIs(reader.active_reader(self.root), outer)
        self.assertIsNone(reader.active_reader(self.root))
        cleared = reader.GitEvidenceReader(self.root)
        self.assertEqual(cleared.rows, {})
        self.assertEqual(outer.rows, {})
        self.assertEqual(outer.tuples, {})

class PublicationReaderTests(unittest.TestCase):
    # Isolate only the P2 fixtures, including their setup; original reader tests
    # and assertions retain their pre-task bodies and environment behaviour.
    git = GitEvidenceReaderTests.git
    commit = GitEvidenceReaderTests.commit

    def setUp(self):
        from tests.i18n.test_production_review_v2_lite_queue import isolated_publication_git_environment
        environment = isolated_publication_git_environment()
        environment.__enter__()
        self.addCleanup(environment.__exit__, None, None, None)
        GitEvidenceReaderTests.setUp(self)

    def test_publication_layout_is_compact_root_local_and_released_on_exit(self):
        base = self.head
        paths = {queue.BATCH_PREFIX + "new/manifest.json", queue.BATCH_PREFIX + "new/raw/input.json"}
        for path in paths:
            destination = self.root / path
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(b"evidence")
        self.commit()
        head = self.git("rev-parse", "HEAD").decode().strip()
        tree = queue._tree(self.root, head)
        self.assertIsNone(queue._publication_commit_fast(self.root, head, tree, paths, base))
        with reader.projection_scope(self.root):
            outer = reader.active_reader(self.root)
            with mock.patch.object(queue, "_publication_base_layout", wraps=queue._publication_base_layout) as layout:
                for _ in range(2):
                    self.assertEqual(queue._publication_commit_fast(self.root, head, tree, paths, base), head)
                self.assertEqual(layout.call_count, 1)
                retained = outer.derived[("publication-base-layout-v1", base)]
                self.assertEqual(retained, (False, frozenset()))
                with self.assertRaisesRegex(RuntimeError, "abort"):
                    with reader.projection_scope(self.root):
                        inner = reader.active_reader(self.root)
                        self.assertEqual(queue._publication_commit_fast(self.root, head, tree, paths, base), head)
                        raise RuntimeError("abort")
                self.assertEqual(inner.derived, {})
                self.assertIs(reader.active_reader(self.root), outer)
                self.assertEqual(layout.call_count, 2)
                with tempfile.TemporaryDirectory() as temporary:
                    other = Path(temporary) / "clone"
                    subprocess.run(["git", "clone", "-q", str(self.root), str(other)], check=True)
                    self.assertIsNone(queue._publication_commit_fast(other, head, tree, paths, base))
                    with reader.projection_scope(other):
                        self.assertEqual(queue._publication_commit_fast(other, head, tree, paths, base), head)
                    self.assertIs(reader.active_reader(self.root), outer)
                self.assertEqual(layout.call_count, 3)
        self.assertEqual(outer.derived, {})
        self.assertIsNone(reader.active_reader(self.root))

    def test_publication_moved_head_resolves_new_fixed_identity(self):
        base = self.head
        paths = {queue.BATCH_PREFIX + "new/manifest.json", queue.BATCH_PREFIX + "new/raw/input.json"}
        for path in paths:
            destination = self.root / path
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(b"evidence")
        self.commit()
        with reader.projection_scope(self.root):
            original = queue._head(self.root, "HEAD")
            original_tree = queue._tree(self.root, original)
            self.assertEqual(queue._publication_commit_fast(self.root, original, original_tree, paths, base), original)
            for path in paths:
                (self.root / path).write_bytes(b"changed")
            self.commit()
            moved = queue._head(self.root, "HEAD")
            moved_tree = queue._tree(self.root, moved)
            self.assertNotEqual(original, moved)
            self.assertEqual(queue._publication_commit(self.root, moved, moved_tree, paths, original), moved)
            self.assertEqual(queue._publication_commit_fast(self.root, original, original_tree, paths, base), original)
            with self.assertRaises(wp1.ProductionReviewError):
                queue._publication_commit(self.root, moved, moved_tree, paths, base)
