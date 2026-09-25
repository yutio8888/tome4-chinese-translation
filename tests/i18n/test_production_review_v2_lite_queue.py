from __future__ import annotations

import fcntl
import hashlib
import copy
import io
import os
import json
from collections import Counter
import sqlite3
import subprocess
import sys
import tempfile
import unittest
import shutil
from contextlib import closing, contextmanager, nullcontext, redirect_stderr, redirect_stdout
from pathlib import Path
from unittest import mock

from tools.i18nlib import capacity_policy
from tools.i18nlib import production_review as wp1
from tools.i18nlib import production_review_v2_lite as catalog
from tools.i18nlib import production_review_v2_lite_queue as queue
from tools.i18nlib import production_review_v2_lite_batch as batch
from tools.i18nlib import production_review_v2_lite_migration as migration
from tools.i18nlib import git_evidence_reader as reader
from tools.i18nlib import gate_results
from tools.i18nlib import projection_cache
import contextual_result_check
from tests.i18n.test_production_review_v2_lite_migration import pin_projection_cache_default

ROOT = Path(__file__).resolve().parents[2]
STAMP = "2026-09-02T01:02:03Z"
FIXTURE_ROOT = Path(os.environ.get("TOME_TEST_FIXTURE_ROOT", ROOT / ".artifacts/i18n"))


@contextmanager
def isolated_publication_git_environment():
    """Real Git/guard, with private system/global files and no inherited GIT_*.

    Keep HOME/CODEX_HOME and all other non-Git environment entries unchanged.
    The explicit editor also exercises the actual reviewer's invocation setting.
    """
    with tempfile.TemporaryDirectory() as temporary:
        directory = Path(temporary)
        selectors = {}
        for name in ("GIT_CONFIG_GLOBAL", "GIT_CONFIG_SYSTEM"):
            config = directory / name
            config.write_text("")
            selectors[name] = str(config)
        environment = {key: value for key, value in os.environ.items() if not key.startswith("GIT_")}
        environment.update(selectors, GIT_EDITOR="true")
        with mock.patch.dict(os.environ, environment, clear=True):
            yield


class PublicationHistoryTests(unittest.TestCase):
    """Small real Git DAGs: compare the success optimization to the old oracle."""

    def setUp(self):
        pin_projection_cache_default(self)
        environment = isolated_publication_git_environment()
        environment.__enter__()
        self.addCleanup(environment.__exit__, None, None, None)
        FIXTURE_ROOT.mkdir(parents=True, exist_ok=True)
        temporary = tempfile.TemporaryDirectory(dir=FIXTURE_ROOT)
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.git("init", "-q")
        self.git("config", "user.name", "Publication fixture")
        self.git("config", "user.email", "fixture@example.invalid")
        self.serial = 0
        self.blob = self.git("hash-object", "-w", "--stdin", data=b"evidence\n").strip().decode()
        self.other = self.git("hash-object", "-w", "--stdin", data=b"changed\n").strip().decode()
        self.file = ("100644", "blob", self.blob)
        self.changed = ("100644", "blob", self.other)
        self.directory = queue.BATCH_PREFIX + "batch-test"
        self.paths = {self.directory + "/manifest.json", self.directory + "/raw/input.json"}
        self.seed = {"seed": self.file}
        self.base = self.commit(self.seed)
        self.entries = {**self.seed, **dict.fromkeys(self.paths, self.file)}

    def git(self, *args, data=None):
        return subprocess.run(["git", *args], cwd=self.root, input=data, check=True,
                              stdout=subprocess.PIPE, stderr=subprocess.PIPE).stdout

    def tree(self, entries):
        nested = {}
        for path, value in entries.items():
            target = nested
            parts = path.split("/")
            for part in parts[:-1]:
                target = target.setdefault(part, {})
            target[parts[-1]] = value

        def build(node):
            records = []
            for name, value in sorted(node.items()):
                mode, kind, oid = ("040000", "tree", build(value)) if isinstance(value, dict) else value
                records.append(f"{mode} {kind} {oid}\t{name}".encode() + b"\0")
            return self.git("mktree", "-z", data=b"".join(records)).decode().strip()
        return build(nested)

    def commit(self, entries, *parents):
        self.serial += 1
        args = ["commit-tree", self.tree(entries)]
        for parent in parents:
            args.extend(("-p", parent))
        oid = self.git(*args, data=f"fixture {self.serial}\n".encode()).decode().strip()
        self.git("update-ref", "HEAD", oid)
        return oid

    @staticmethod
    def outcome(operation):
        try:
            return ("return", operation())
        except (wp1.ProductionReviewError, UnicodeError, ValueError) as error:
            return ("error", type(error), str(error))

    def compare(self, head, *, base=None, paths=None, fallback=None, logs=None):
        base = self.base if base is None else base
        paths = self.paths if paths is None else paths
        tree = queue._tree(self.root, head)
        with reader.projection_scope(self.root):
            expected = self.outcome(lambda: queue._publication_commit_slow(self.root, head, tree, paths, base))
        with reader.projection_scope(self.root):
            with mock.patch.object(queue, "_publication_commit_slow", wraps=queue._publication_commit_slow) as slow:
                with mock.patch.object(queue, "_git", wraps=queue._git) as git:
                    actual = self.outcome(lambda: queue._publication_commit(self.root, head, tree, paths, base))
            self.assertEqual(actual, expected)
            if fallback is not None:
                self.assertEqual(slow.call_count, int(fallback))
            if logs is not None:
                self.assertEqual(sum(c.args[1] == "log" for c in git.call_args_list), logs)
        return actual

    def test_new_directory_uses_one_original_am_log(self):
        head = self.commit(self.entries, self.base)
        self.assertEqual(self.compare(head, fallback=False, logs=1), ("return", head))
        tree = queue._tree(self.root, head)
        with reader.projection_scope(self.root), mock.patch.object(queue, "_git", wraps=queue._git) as git:
            self.assertEqual(queue._publication_commit(self.root, head, tree, self.paths, self.base), head)
        logs = [c.args[1:] for c in git.call_args_list if c.args[1] == "log"]
        self.assertEqual(logs, [("log", "--full-history", "--format=%H", "--diff-filter=AM",
                                 head, "--", sorted(self.paths)[0])])

    def test_split_raw_core_and_merge_itself_publishing_are_rejected(self):
        anchor, raw = sorted(self.paths)
        first = self.commit({**self.seed, raw: self.file}, self.base)
        split = self.commit(self.entries, first)
        self.assertEqual(self.compare(split, fallback=True)[0], "error")
        sibling = self.commit({**self.seed, "sibling": self.changed}, self.base)
        merge = self.commit(self.entries, first, sibling)
        self.assertEqual(self.compare(merge, fallback=True)[0], "error")

    def test_identical_siblings_rejected_but_one_matching_child_succeeds(self):
        first = self.commit(self.entries, self.base)
        second = self.commit(self.entries, self.base)
        merged = self.commit(self.entries, first, second)
        self.assertEqual(self.compare(merged, fallback=True)[0], "error")
        different = self.commit({**self.entries, sorted(self.paths)[1]: self.changed}, self.base)
        merged = self.commit(self.entries, different, first)
        self.assertEqual(self.compare(merged, fallback=False), ("return", first))

    def test_change_revert_deletion_restore_and_other_base(self):
        first = self.commit(self.entries, self.base)
        changed = self.commit({**self.entries, sorted(self.paths)[1]: self.changed}, first)
        reverted = self.commit(self.entries, changed)
        self.assertEqual(self.compare(reverted, fallback=False), ("return", first))
        deleted = self.commit(self.seed, reverted)
        restored = self.commit(self.entries, deleted)
        self.assertEqual(self.compare(restored, fallback=False), ("return", first))
        self.assertEqual(self.compare(restored, base=deleted, fallback=False), ("return", restored))
        # Only raw changed here: the unchanged core has no AM at revert.
        self.assertEqual(self.compare(restored, base=changed, fallback=True)[0], "error")
        all_changed = self.commit({**self.seed, **dict.fromkeys(self.paths, self.changed)}, restored)
        all_reverted = self.commit(self.entries, all_changed)
        self.assertEqual(self.compare(all_reverted, base=all_changed, fallback=True), ("return", all_reverted))
        self.assertEqual(self.compare(restored, base=first, fallback=True)[0], "error")

    def test_external_rename_and_copy_use_real_single_path_am(self):
        base = self.commit({**self.seed, "outside": self.file}, self.base)
        for copy_source in (False, True):
            with self.subTest(copy=copy_source):
                entries = {**self.entries, **({"outside": self.file} if copy_source else {})}
                head = self.commit(entries, base)
                self.assertEqual(self.compare(head, base=base, fallback=False, logs=1), ("return", head))

    def test_mode_type_and_oid_are_all_required(self):
        first = self.commit(self.entries, self.base)
        anchor = sorted(self.paths)[0]
        for mode, kind, oid in (("100755", "blob", self.blob), ("120000", "blob", self.blob),
                                ("160000", "commit", self.base)):
            with self.subTest(mode=mode):
                head = self.commit({**self.entries, anchor: (mode, kind, oid)}, first)
                self.assertEqual(self.compare(head, fallback=True)[0], "error")
                # When the old batch directory exists even a later valid M
                # boundary must be decided by the unchanged slow algorithm.
                self.compare(head, base=first, fallback=True)

    def test_file_directory_empty_tree_and_ancestor_blockers_fall_back(self):
        empty = self.git("mktree", data=b"").decode().strip()
        cases = [{self.directory: ("040000", "tree", empty)},
                 {self.directory + "/empty": ("040000", "tree", empty)},
                 {self.directory: self.file},
                 {self.directory + "/manifest.json/child": self.file}]
        for ancestor in ("evidence", "evidence/production-review-v2-lite", queue.BATCH_PREFIX[:-1]):
            for entry in (self.file, ("120000", "blob", self.blob), ("160000", "commit", self.base)):
                cases.append({ancestor: entry})
        for before in cases:
            with self.subTest(before=before):
                base = self.commit({**self.seed, **before}, self.base)
                head = self.commit(self.entries, base)
                self.compare(head, base=base, fallback=True)
        # Explicitly prove why a leaf-only tree cannot establish absence.
        base = self.commit({self.directory: ("040000", "tree", empty)}, self.base)
        self.assertEqual(queue._tree(self.root, base), {})
        with reader.projection_scope(self.root):
            self.assertIn(b"batch-test", queue._publication_base_layout(self.root, base)[1])

    def test_noncanonical_and_pathspec_paths_and_aliases_use_oracle(self):
        for name in ("汉字", "has space", "has\ttab", "has\nnewline", "glob*", "q?", "[x]", ":magic", "back\\slash"):
            with self.subTest(name=name):
                paths = {self.directory + "/" + name, self.directory + "/raw/input.json"}
                head = self.commit({**self.seed, **dict.fromkeys(paths, self.file)}, self.base)
                self.compare(head, paths=paths, fallback=True)
        head = self.commit(self.entries, self.base)
        self.git("tag", "base-alias", self.base)
        for base in ("base-alias", self.base[:12], self.base.upper(), " " + self.base, ""):
            self.compare(head, base=base, fallback=True)
        self.compare("HEAD", fallback=True)
        other_paths = {"outside/a", "outside/b"}
        head = self.commit(dict.fromkeys(other_paths, self.file), self.base)
        self.compare(head, paths=other_paths, fallback=True)
        paths = self.paths | {queue.BATCH_PREFIX + "other/raw.json"}
        head = self.commit(dict.fromkeys(paths, self.file), self.base)
        self.compare(head, paths=paths, fallback=True)

    def test_subdirectory_cwd_cannot_borrow_full_tree_addition_proof(self):
        # log pathspecs are cwd-relative, while ls-tree --full-tree is not.
        # Only the nested anchor exists; the oracle must reject missing raw.
        anchor = sorted(self.paths)[0]
        head = self.commit({**self.entries, "nested/" + anchor: self.file}, self.base)
        original = self.root
        self.root = original / "nested"
        self.root.mkdir()
        try:
            self.assertEqual(self.compare(head, fallback=True)[0], "error")
        finally:
            self.root = original

    def test_effective_config_includes_and_same_scope_changes(self):
        head = self.commit(self.entries, self.base)
        tree = queue._tree(self.root, head)
        with reader.projection_scope(self.root):
            self.assertEqual(queue._publication_commit_fast(self.root, head, tree, self.paths, self.base), head)
            for key, value in (("diff.renames", "copies"), ("log.follow", "true"),
                               ("diff.external", "false"), ("diff.fixture.textconv", "cat"),
                               ("diff.algorithm", "patience"), ("log.diffMerges", "first-parent"),
                               ("core.attributesFile", "/dev/null")):
                with self.subTest(key=key):
                    self.git("config", key, value)
                    try:
                        self.assertIsNone(queue._publication_commit_fast(self.root, head, tree, self.paths, self.base))
                        self.compare(head, fallback=True)
                    finally:
                        self.git("config", "--unset-all", key)
            include = self.root / "included-config"
            include.write_text("[diff]\n\trenames = copies\n")
            self.git("config", "include.path", str(include))
            self.compare(head, fallback=True)
            include.write_text("[diff]\n\trenames = true\n[log]\n\tfollow = false\n")
            self.assertIsNone(queue._publication_commit_fast(self.root, head, tree, self.paths, self.base))
            self.compare(head, fallback=False)
            self.git("config", "--unset-all", "include.path")

    def test_environment_overrides_are_rechecked_without_secret_output(self):
        head = self.commit(self.entries, self.base)
        tree = queue._tree(self.root, head)
        environments = [{"GIT_LITERAL_PATHSPECS": "1"}, {"GIT_GLOB_PATHSPECS": "1"},
                        {"GIT_NOGLOB_PATHSPECS": "1"}, {"GIT_ICASE_PATHSPECS": "1"},
                        {"GIT_NO_REPLACE_OBJECTS": "1"}, {"GIT_REPLACE_REF_BASE": "refs/custom/"},
                        {"GIT_EXTERNAL_DIFF": "false"},
                        {"GIT_CONFIG_COUNT": "1", "GIT_CONFIG_KEY_0": "diff.renames", "GIT_CONFIG_VALUE_0": "copies"},
                        {"GIT_SHALLOW_FILE": str(self.root / "absent-shallow")},
                        {"GIT_GRAFT_FILE": str(self.root / "absent-grafts")}]
        with reader.projection_scope(self.root):
            self.assertEqual(queue._publication_commit_fast(self.root, head, tree, self.paths, self.base), head)
            for environment in environments:
                with self.subTest(keys=sorted(environment)), mock.patch.dict(os.environ, environment):
                    self.assertIsNone(queue._publication_commit_fast(self.root, head, tree, self.paths, self.base))
                    self.compare(head, fallback=True)
            self.assertIsNone(queue._publication_commit_fast(self.root, head, tree, self.paths, self.base))
            self.compare(head, fallback=False)

    def test_replace_custom_namespace_graft_shallow_and_linked_worktree(self):
        head = self.commit(self.entries, self.base)
        replacement = self.commit({**self.entries, "extra": self.changed}, self.base)
        self.git("update-ref", "HEAD", head)
        self.git("replace", head, replacement)
        self.compare(head, fallback=True)
        self.git("replace", "-d", head)
        self.git("update-ref", "refs/custom/" + head, replacement)
        with mock.patch.dict(os.environ, {"GIT_REPLACE_REF_BASE": "refs/custom/"}):
            self.compare(head, fallback=True)
        graft = self.root / ".git/info/grafts"
        graft.write_text(head + " " + self.base + "\n")
        self.compare(head, fallback=True)
        graft.unlink()
        with tempfile.TemporaryDirectory(dir=FIXTURE_ROOT) as temporary:
            original = self.root
            clone = Path(temporary) / "shallow"
            self.git("clone", "-q", "--depth=1", original.as_uri(), str(clone))
            self.root = clone
            try:
                self.compare(head, fallback=True)
            finally:
                self.root = original
            worktree = Path(temporary) / "worktree"
            self.git("worktree", "add", "-q", "--detach", str(worktree), head)
            self.root = worktree
            try:
                self.assertTrue((worktree / ".git").is_file())
                self.compare(head, fallback=False, logs=1)
                graft.write_text("")
                self.compare(head, fallback=True)
                graft.unlink()
            finally:
                self.root = original
                self.git("worktree", "remove", "--force", str(worktree))

    def test_probe_failures_retry_and_preserve_original_errors(self):
        head = self.commit(self.entries, self.base)
        tree = queue._tree(self.root, head)
        original = queue._git
        for probe in ("config", "rev-parse", "for-each-ref", "ls-tree"):
            with self.subTest(probe=probe), reader.projection_scope(self.root):
                def fail(root, *args):
                    if args[0] == probe:
                        raise wp1.ProductionReviewError("probe unavailable")
                    return original(root, *args)
                with mock.patch.object(queue, "_git", side_effect=fail):
                    expected = self.outcome(lambda: queue._publication_commit_slow(self.root, head, tree, self.paths, self.base))
                    actual = self.outcome(lambda: queue._publication_commit(self.root, head, tree, self.paths, self.base))
                    self.assertEqual(actual, expected)
                if probe == "ls-tree":
                    # Metadata loader failure is retryable, unlike environment
                    # inspection failure. The failed derived value is absent.
                    self.assertNotIn(("publication-base-layout-v1", self.base),
                                     reader.active_reader(self.root).derived)
                    self.assertEqual(queue._publication_commit_fast(self.root, head, tree, self.paths, self.base), head)
                else:
                    self.assertIsNone(queue._publication_commit_fast(self.root, head, tree, self.paths, self.base))
                    self.assertEqual(queue._publication_commit(self.root, head, tree, self.paths, self.base),
                                     queue._publication_commit_slow(self.root, head, tree, self.paths, self.base))
                self.compare(head, fallback=False)
        for raw in (b"unterminated", b"040000 tree invalid\tpath\0", b"bad\0"):
            with self.subTest(layout=raw), reader.projection_scope(self.root):
                def malformed(root, *args):
                    return raw if args[:4] == ("ls-tree", "-r", "-t", "-z") else original(root, *args)
                with mock.patch.object(queue, "_git", side_effect=malformed):
                    self.assertEqual(queue._publication_commit(self.root, head, tree, self.paths, self.base), head)
                self.assertEqual(queue._publication_commit_fast(self.root, head, tree, self.paths, self.base), head)
        with reader.projection_scope(self.root), mock.patch.object(queue, "_git", side_effect=wp1.ProductionReviewError("git unavailable")):
            expected = self.outcome(lambda: queue._publication_commit_slow(self.root, head, tree, self.paths, self.base))
            actual = self.outcome(lambda: queue._publication_commit(self.root, head, tree, self.paths, self.base))
            self.assertEqual(actual, expected)
            self.assertEqual(actual[2], "git unavailable")

    def test_replace_fallback_cache_never_reenables_fast_in_same_scope(self):
        good = self.commit(self.entries, self.base)
        anchor = sorted(self.paths)[0]
        publication = self.commit({**self.seed, anchor: self.file}, self.base)
        head = self.commit(self.entries, publication)
        replacement = self.commit(self.entries, self.base)
        self.git("update-ref", "HEAD", head)
        tree = queue._tree(self.root, head)
        for warm, alias in ((False, False), (True, False), (False, True)):
            with self.subTest(warm=warm, ineligible_alias=alias), reader.projection_scope(self.root):
                scope = reader.active_reader(self.root)
                if warm:
                    self.assertEqual(queue._publication_commit_fast(self.root, good, tree, self.paths, self.base), good)
                self.git("replace", publication, replacement)
                try:
                    with mock.patch.object(queue, "_publication_commit_slow", wraps=queue._publication_commit_slow) as slow:
                        # Enter through the wrapper, so replaced bytes really
                        # populate the old reader cache before the ref is removed.
                        self.assertEqual(queue._publication_commit(self.root, "HEAD" if alias else head,
                                                                  tree, self.paths, self.base), publication)
                        self.assertEqual(slow.call_count, 1)
                    cached = scope.trees[publication]
                finally:
                    self.git("replace", "-d", publication)
                self.assertIsNone(queue._publication_commit_fast(self.root, head, tree, self.paths, self.base))
                with mock.patch.object(queue, "_publication_commit_slow", wraps=queue._publication_commit_slow) as slow:
                    actual = self.outcome(lambda: queue._publication_commit(self.root, head, tree, self.paths, self.base))
                    self.assertEqual(slow.call_count, 1)
                expected = self.outcome(lambda: queue._publication_commit_slow(self.root, head, tree, self.paths, self.base))
                self.assertEqual(actual, expected)
                self.assertEqual(actual[0], "error")
                self.assertIs(scope.trees[publication], cached)
                # A nested safe projection is independent even on exception;
                # restoring the outer scope must also restore its disabled state.
                with self.assertRaisesRegex(RuntimeError, "nested abort"):
                    with reader.projection_scope(self.root):
                        inner = reader.active_reader(self.root)
                        self.assertEqual(queue._publication_commit_fast(self.root, good, tree, self.paths, self.base), good)
                        raise RuntimeError("nested abort")
                self.assertEqual(inner.derived, {})
                self.assertIs(reader.active_reader(self.root), scope)
                self.assertIsNone(queue._publication_commit_fast(self.root, good, tree, self.paths, self.base))
                with tempfile.TemporaryDirectory(dir=FIXTURE_ROOT) as temporary:
                    other = Path(temporary) / "clone"
                    self.git("clone", "-q", str(self.root), str(other))
                    self.assertIsNone(queue._publication_commit_fast(other, good, tree, self.paths, self.base))
                    with reader.projection_scope(other):
                        self.assertEqual(queue._publication_commit_fast(other, good, tree, self.paths, self.base), good)
                self.assertIs(reader.active_reader(self.root), scope)
                self.assertIsNone(queue._publication_commit_fast(self.root, good, tree, self.paths, self.base))
            self.assertEqual(scope.derived, {})
            fresh = self.outcome(lambda: queue._publication_commit_slow(self.root, head, tree, self.paths, self.base))
            self.assertEqual(actual, fresh)
            self.compare(head, fallback=True)
            self.compare(good, fallback=False)

    def test_disabled_inner_exception_does_not_disable_safe_outer(self):
        head = self.commit(self.entries, self.base)
        tree = queue._tree(self.root, head)
        with reader.projection_scope(self.root):
            self.assertEqual(queue._publication_commit_fast(self.root, head, tree, self.paths, self.base), head)
            with self.assertRaisesRegex(RuntimeError, "unsafe abort"):
                with reader.projection_scope(self.root):
                    inner = reader.active_reader(self.root)
                    with mock.patch.dict(os.environ, {"GIT_UNKNOWN_PUBLICATION_INPUT": "1"}):
                        self.assertIsNone(queue._publication_commit_fast(self.root, head, tree, self.paths, self.base))
                    raise RuntimeError("unsafe abort")
            self.assertEqual(inner.derived, {})
            self.assertEqual(queue._publication_commit_fast(self.root, head, tree, self.paths, self.base), head)

    def test_editor_and_config_selectors_check_actual_contents_every_time(self):
        head = self.commit(self.entries, self.base)
        tree = queue._tree(self.root, head)
        self.assertEqual(os.environ["GIT_EDITOR"], "true")
        self.git("config", "core.editor", "false")
        self.assertEqual(self.compare(head, fallback=False, logs=1), ("return", head))
        with mock.patch.dict(os.environ):
            del os.environ["GIT_EDITOR"]
            self.assertEqual(self.compare(head, fallback=False, logs=1), ("return", head))
        for selector in ("GIT_CONFIG_GLOBAL", "GIT_CONFIG_SYSTEM"):
            selected = Path(os.environ[selector])
            included = selected.with_name(selected.name + "-include")
            for indirect in (False, True):
                with self.subTest(selector=selector, include=indirect), reader.projection_scope(self.root):
                    selected.write_text("[include]\npath = " + str(included) + "\n" if indirect else "")
                    target = included if indirect else selected
                    target.write_text("[core]\neditor = false\n")
                    self.assertEqual(queue._publication_commit_fast(self.root, head, tree, self.paths, self.base), head)
                    target.write_text("[diff]\nrenames = copies\n")
                    try:
                        self.assertIsNone(queue._publication_commit_fast(self.root, head, tree, self.paths, self.base))
                        self.compare(head, fallback=True)
                    finally:
                        target.write_text("[core]\neditor = false\n")
                    self.assertIsNone(queue._publication_commit_fast(self.root, head, tree, self.paths, self.base))
                    self.assertEqual(queue._publication_commit(self.root, head, tree, self.paths, self.base),
                                     queue._publication_commit_slow(self.root, head, tree, self.paths, self.base))
                    self.compare(head, fallback=False)
            # Switching the selector itself also requires reading the new file.
            selected.write_text("")
            included.write_text("[log]\nfollow = true\n")
            with reader.projection_scope(self.root):
                self.assertEqual(queue._publication_commit_fast(self.root, head, tree, self.paths, self.base), head)
                with mock.patch.dict(os.environ, {selector: str(included)}):
                    self.assertIsNone(queue._publication_commit_fast(self.root, head, tree, self.paths, self.base))
                    self.compare(head, fallback=True)
                self.assertIsNone(queue._publication_commit_fast(self.root, head, tree, self.paths, self.base))
            selected.write_text("")
            with reader.projection_scope(self.root):
                selected.write_text("[invalid config\n")
                try:
                    expected = self.outcome(lambda: queue._publication_commit_slow(self.root, head, tree, self.paths, self.base))
                    actual = self.outcome(lambda: queue._publication_commit(self.root, head, tree, self.paths, self.base))
                    self.assertEqual(actual, expected)
                    self.assertEqual(actual[0], "error")
                finally:
                    selected.write_text("")
                self.assertIsNone(queue._publication_commit_fast(self.root, head, tree, self.paths, self.base))
                self.assertEqual(queue._publication_commit(self.root, head, tree, self.paths, self.base),
                                 queue._publication_commit_slow(self.root, head, tree, self.paths, self.base))
        for key, value in (("color.ui", "auto"), ("alias.st", "status"), ("pull.rebase", "true"),
                           ("push.default", "simple"), ("gc.auto", "0"), ("commit.gpgsign", "false")):
            with self.subTest(unknown_config=key):
                self.git("config", key, value)
                try:
                    self.compare(head, fallback=True)
                finally:
                    self.git("config", "--unset-all", key)
        with mock.patch.dict(os.environ, {"GIT_UNKNOWN_PUBLICATION_INPUT": "1"}):
            self.compare(head, fallback=True)

    def test_three_finite_wrong_algorithms_are_detected(self):
        # Deliberately wrong local variants, each fed real Git histories/trees.
        def wrong(head, base, variant):
            current = queue._tree(self.root, head)
            histories = ([self.git("rev-list", head).decode().splitlines()] if variant == "ignore-AM" else
                         [queue._candidate_commits(self.root, head, path) for path in sorted(self.paths)])
            common = set(histories[0]).intersection(*(set(h) for h in histories[1:]))
            matches = []
            for commit in histories[0]:
                candidate = queue._tree(self.root, commit)
                if commit not in common:
                    continue
                equal = all(candidate.get(p) == current[p] for p in self.paths)
                if variant == "OID-only":
                    equal = all(candidate.get(p, (None, None, None))[2] == current[p][2] for p in self.paths)
                if equal and queue._commit_parent(self.root, commit) == base:
                    matches.append(commit)
                    if variant == "first-match":
                        return commit
            return matches[0] if len(matches) == 1 else None

        anchor = sorted(self.paths)[0]
        before = {**self.entries, anchor: ("120000", "blob", self.blob)}
        base = self.commit(before, self.base)
        type_change = self.commit(self.entries, base)
        self.assertEqual(self.compare(type_change, base=base, fallback=True)[0], "error")
        self.assertEqual(wrong(type_change, base, "ignore-AM"), type_change)
        first = self.commit(self.entries, self.base)
        sibling = self.commit(self.entries, self.base)
        merged = self.commit(self.entries, first, sibling)
        self.assertEqual(self.compare(merged)[0], "error")
        self.assertIn(wrong(merged, self.base, "first-match"), {first, sibling})
        executable = self.commit({**self.entries, anchor: ("100755", "blob", self.blob)}, first)
        self.assertEqual(self.compare(executable)[0], "error")
        self.assertEqual(wrong(executable, self.base, "OID-only"), first)


class QueueFixture(unittest.TestCase):
    def setUp(self):
        pin_projection_cache_default(self)
        # Minimal repository fixture: inject execution in-process, never in production
        # through an environment marker or a missing-file fallback.
        self.real_actual_gates = batch._actual_gate_records
        def fixture_gates(root, selected):
            def execute(argv, cwd, log):
                log.write_bytes(b"fixture gate execution\n")
                return 0
            return gate_results.run(root, selected, execute=execute)
        patcher = mock.patch.object(batch, "_actual_gate_records", side_effect=fixture_gates)
        self.gate_runner = patcher.start()
        self.addCleanup(patcher.stop)
        FIXTURE_ROOT.mkdir(parents=True, exist_ok=True)
        self.temp = tempfile.TemporaryDirectory(dir=FIXTURE_ROOT)
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        subprocess.run(["git", "init", "-q"], cwd=self.root, check=True)
        subprocess.run(["git", "config", "user.email", "test@example.invalid"], cwd=self.root, check=True)
        subprocess.run(["git", "config", "user.name", "Test"], cwd=self.root, check=True)
        (self.root / ".gitignore").write_text("/.artifacts/\n", encoding="utf-8")
        self.entries = [self._entry("1"), self._entry("2")]
        self._write_catalog()
        queue_schema = self.root / "i18n/quality/production-review-v2-lite/queue-v1.schema.sql"
        queue_schema.write_text("-- planned WP2-Lite queue schema fixture\n", encoding="utf-8")
        self._commit("catalog")

    def _entry(self, digit):
        source, target, fixed, terminology = "source " + digit, "target " + digit, "commit:" + "a" * 40, "b" * 64
        core = {"component": "tome", "duplicate_index": 0, "function_name": "t", "normalized_source_tag": "",
                "section": "fixture", "source": source, "translation_path": "tome.lua"}
        locator = catalog._plain_id(catalog.CALL_LOCATOR_KIND, "locator", core)
        logical = wp1.surface.logical_entry_identity(component="tome", normalized_path="tome.lua",
                                                      call_locator=locator, source_tag="")
        revision = wp1.surface.entry_revision_identity(logical_entry_identity=logical, source=source, target=target,
            fixed_source_identity=fixed, terminology_snapshot=terminology, rules_version=catalog.RULES_VERSION,
            args_order=None)
        return {"schema_version": 1, "component": "tome", "normalized_path": "tome.lua",
                "section": "fixture", "call_locator": locator, "logical_entry_identity": logical,
                "entry_revision_identity": revision, "source": source, "target": target, "source_tag": "",
                "source_sha256": hashlib.sha256(source.encode()).hexdigest(),
                "target_sha256": hashlib.sha256(target.encode()).hexdigest(), "fixed_source_identity": fixed,
                "terminology_snapshot_sha256": terminology, "rules_version": catalog.RULES_VERSION,
                "risk": {"has_args_order": False, "has_special": False, "source_utf8_bytes": len(source.encode()),
                         "target_utf8_bytes": len(target.encode()), "component_group_size": 1, "component_group_last": True,
                         "args_order": None}}

    def _write_catalog(self):
        entries_raw = wp1._jsonl(sorted(self.entries, key=lambda row: row["entry_revision_identity"]))
        exclusions_raw = b""
        manifest = {"schema_version": 1, "kind": catalog.CATALOG_KIND, "catalog_id": "",
                    "rules_version": catalog.RULES_VERSION, "recorded_at": STAMP, "recorded_by": "fixture",
                    "manifest_sha256": "c" * 64, "loader_contract_path": "tools/i18nlib/locale_model.py",
                    "loader_contract_sha256": "d" * 64, "lua_runtime": "Lua 5.1",
                    "manifest_component_ordinals": [{"component": name, "ordinal": index} for index, name in
                        enumerate(["engine", "boot", "tome", "ashes-urhrok", "cults", "orcs"])],
                    "component_counts": {"ashes-urhrok": 0, "boot": 0, "cults": 0, "engine": 0,
                                                              "orcs": 0, "tome": len(self.entries)},
                    "occurrence_count": len(self.entries), "entry_count": len(self.entries), "exclusion_count": 0,
                    "entries_sha256": hashlib.sha256(entries_raw).hexdigest(),
                    "exclusions_sha256": hashlib.sha256(exclusions_raw).hexdigest(),
                    "terminology_snapshot_sha256": "b" * 64,
                    "source_identities": {name: "commit:" + "a" * 40 for name in
                                          ["engine", "boot", "tome", "ashes-urhrok", "cults", "orcs"]},
                    "policy_sha256": hashlib.sha256(catalog.POLICY_RAW).hexdigest()}
        manifest["catalog_id"] = catalog.catalog_id(manifest)
        files = {catalog.SCHEMA_PATH: catalog.SCHEMA_RAW, catalog.POLICY_PATH: catalog.POLICY_RAW,
                 f"{catalog.CATALOG_PREFIX}/manifest.json": wp1.canonical_bytes(manifest),
                 f"{catalog.CATALOG_PREFIX}/entries.jsonl": entries_raw,
                 f"{catalog.CATALOG_PREFIX}/exclusions.jsonl": exclusions_raw}
        for name, raw in files.items():
            path = self.root / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
        self.catalog_id = manifest["catalog_id"]

    def _commit(self, message):
        subprocess.run(["git", "add", "."], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-qm", message], cwd=self.root, check=True)
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.root, text=True).strip()

    def _install_contextual_done_state(self, ref, output_raw):
        """Install a real v2 review-only DONE_VERIFIED fixture for this run."""
        fixture = ROOT / "tests/i18n/fixtures/paseo_state_v2/contextual_v2"
        task_id = ref["task_id"]
        task_dir = self.root / ".ai/task" / task_id
        task_dir.mkdir(parents=True, exist_ok=True)
        envelope_raw = Path(ref["input_path"]).read_bytes()
        envelope = json.loads(envelope_raw)
        input_path = task_dir / "CONTEXTUAL-ENVELOPE-final-full.json"
        raw_path = self.root / ".ai/reviews" / task_id / "raw-final-full.txt"
        raw_path.parent.mkdir(parents=True, exist_ok=True)
        input_path.write_bytes(envelope_raw)
        raw_path.write_bytes(output_raw)
        state = json.loads((fixture / "STATE.json").read_text(encoding="utf-8"))
        record = json.loads((fixture / "review-final-full.json").read_text(encoding="utf-8"))
        relative_input = input_path.relative_to(self.root).as_posix()
        relative_raw = raw_path.relative_to(self.root).as_posix()
        record.update({"task_id": task_id, "cycle": 0, "review_phase": "REVIEW",
                       "task_id": task_id, "candidate_identity": ref["candidate_identity"],
                       "input_path": relative_input, "raw_output_path": relative_raw,
                       "raw_output_sha256": hashlib.sha256(output_raw).hexdigest(),
                       "dispatch_id": "final-full", "agent_id": "agent-final-full"})
        record_path = task_dir / "review-final-full.json"
        record_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        dispatch = {"dispatch_id": "final-full", "role": "REVIEWER",
                    "purpose": "translation_contextual_v2", "agent_id": "agent-final-full",
                    "parent_agent_id": "agent-orchestrator", "workspace_id": "fixture-workspace",
                    "lineage_verified": True, "lifecycle": "archived", "archive_confirmed": True,
                    "candidate_identity": ref["candidate_identity"], "input_path": relative_input,
                    "labels": {"task_id": task_id, "role": "reviewer", "purpose": "translation_contextual_v2",
                               "candidate_identity": ref["candidate_identity"], "dispatch_id": "final-full"}}
        state.update({"task_id": task_id, "cycle": 0, "state": "DONE", "mode": "review_only",
                      "change_class": "standard",
                      "contextual_reviewers": [{"role": "REVIEWER", "purpose": "translation_contextual_v2",
                          "candidate_identity": ref["candidate_identity"], "dispatch_id": "final-full",
                          "input_path": relative_input, "agent_id": "agent-final-full"}],
                      "child_dispatches": [dispatch],
                      "review_records": [record_path.relative_to(self.root).as_posix()],
                      "senior_review_records": []})
        state_path = task_dir / "STATE.json"
        state_path.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        sys.path.insert(0, str(ROOT / "tools"))
        import ai_state_check
        checked = ai_state_check.check_state(state_path, target="DONE", workspace_root=self.root)
        if checked.outcome != "DONE_VERIFIED":
            raise AssertionError(f"fixture state rejected: {checked.detail}")

    def _batch(self, state="done", batch="batch-1", *, contract="surface", adapter_entry_index=0):
        base = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.root, text=True).strip()
        entry = self.entries[0]
        revision = entry["entry_revision_identity"]
        adapter_entry = self.entries[adapter_entry_index]
        adapter_revision = adapter_entry["entry_revision_identity"]
        if contract == "surface":
            contract_name = "translation_surface_screen_v1"
            surface_entry = {key: adapter_entry[key] for key in wp1.surface.ENTRY_KEYS}
            surface_entry["args_order"] = adapter_entry["risk"]["args_order"]
            payload = {"contract": contract_name, "fixed_source_identity": adapter_entry["fixed_source_identity"],
                       "terminology_snapshot": adapter_entry["terminology_snapshot_sha256"],
                       "rules_version": adapter_entry["rules_version"], "rendered_briefing": "fixture",
                       "entries": [surface_entry]}
            adapter_output_value = {"contract": contract_name, "candidate_identity": "",
                                    "results": [{"entry_revision_identity": adapter_revision, "verdict": "OK"}]}
        elif contract == "contextual":
            contract_name = "translation_contextual_v2"
            payload = {"contract": contract_name, "ordered_revision_keys": [adapter_revision],
                       "translation_snapshot": [{"revision_key": adapter_revision,
                                                   "source": adapter_entry["source"],
                                                   "target": adapter_entry["target"]}],
                       "fixed_source_identity": adapter_entry["fixed_source_identity"],
                       "terminology_snapshot": adapter_entry["terminology_snapshot_sha256"],
                       "bounded_context": [{"revision_key": adapter_revision, "context": "fixture"}],
                       "rendered_briefing": "fixture"}
            adapter_output_value = {"contract": contract_name, "candidate_identity": "",
                                    "verdicts": [{"revision_key": adapter_revision, "verdict": "OK"}]}
        else:
            raise AssertionError(contract)
        candidate_identity = hashlib.sha256(wp1.surface.canonical_bytes(payload)).hexdigest()
        adapter_input = wp1.surface.canonical_bytes({"candidate_identity": candidate_identity, "payload": payload})
        adapter_output_value["candidate_identity"] = candidate_identity
        adapter_output = (wp1.surface.canonical_bytes(adapter_output_value) if contract == "surface" else
                          json.dumps(adapter_output_value, ensure_ascii=False,
                                     separators=(",", ":")).encode("utf-8"))
        input_hash, output_hash = hashlib.sha256(adapter_input).hexdigest(), hashlib.sha256(adapter_output).hexdigest()
        row = {"schema_version": 1, "source": entry["source"], "target": entry["target"],
               "source_tag": "", "normalized_path": "tome.lua", "call_locator": entry["call_locator"],
               "logical_entry_identity": entry["logical_entry_identity"], "entry_revision_identity": revision,
               "surface_verdict": "OK" if contract == "surface" else None, "surface_observation": None,
               "deep_verdict": "OK" if contract == "contextual" else None, "deep_observation": None,
               "input_sha256": input_hash, "output_sha256": output_hash, "final_state": state,
               "completion_level": "surface_only" if contract == "surface" else "deep_reviewed"}
        results = wp1._jsonl([row])
        adjudications = b""
        gates = wp1.canonical_bytes({"schema_version": 1, "commands": []})
        manifest = {"schema_version": 1, "kind": "production_review_v2_lite_batch_v1",
                    "catalog_id": self.catalog_id, "policy_sha256": hashlib.sha256(catalog.POLICY_RAW).hexdigest(),
                    "base_commit": base, "batch_id": batch, "attempt": 1, "ordered_revisions": [revision],
                    "ordered_revisions_sha256": hashlib.sha256(wp1.canonical_bytes([revision])).hexdigest(),
                    "entry_snapshots_sha256": hashlib.sha256(wp1.canonical_bytes([entry])).hexdigest(),
                    "adapter_refs": [{"contract": contract_name,
                        "input_path": f"evidence/production-review-v2-lite/batches/{batch}/raw/{contract}/input.json",
                        "input_sha256": input_hash,
                        "output_path": f"evidence/production-review-v2-lite/batches/{batch}/raw/{contract}/output.json",
                        "output_sha256": output_hash, "candidate_identity": candidate_identity}],
                    "results_sha256": hashlib.sha256(results).hexdigest(),
                    "adjudications_sha256": hashlib.sha256(adjudications).hexdigest(),
                    "gates_sha256": hashlib.sha256(gates).hexdigest(), "producer_task_ids": ["fixture"],
                    "recorded_at": STAMP, "recorded_by": "fixture"}
        root = self.root / f"evidence/production-review-v2-lite/batches/{batch}"
        root.mkdir(parents=True)
        (root / "manifest.json").write_bytes(wp1.canonical_bytes(manifest))
        (root / "results.jsonl").write_bytes(results)
        (root / "adjudications.jsonl").write_bytes(adjudications)
        (root / "gates.json").write_bytes(gates)
        (root / f"raw/{contract}").mkdir(parents=True)
        (root / f"raw/{contract}/input.json").write_bytes(adapter_input)
        (root / f"raw/{contract}/output.json").write_bytes(adapter_output)
        return root

    def _add_overlapping_contract(self, root, contract):
        entry = self.entries[0]
        revision = entry["entry_revision_identity"]
        if contract == "surface":
            contract_name = "translation_surface_screen_v1"
            surface_entry = {key: entry[key] for key in wp1.surface.ENTRY_KEYS}
            surface_entry["args_order"] = entry["risk"]["args_order"]
            payload = {"contract": contract_name, "fixed_source_identity": entry["fixed_source_identity"],
                       "terminology_snapshot": entry["terminology_snapshot_sha256"],
                       "rules_version": entry["rules_version"], "rendered_briefing": "fixture",
                       "entries": [surface_entry]}
            output_value = {"contract": contract_name, "candidate_identity": "",
                            "results": [{"entry_revision_identity": revision, "verdict": "OK"}]}
        elif contract == "contextual":
            contract_name = "translation_contextual_v2"
            payload = {"contract": contract_name, "ordered_revision_keys": [revision],
                       "translation_snapshot": [{"revision_key": revision, "source": entry["source"],
                                                  "target": entry["target"]}],
                       "fixed_source_identity": entry["fixed_source_identity"],
                       "terminology_snapshot": entry["terminology_snapshot_sha256"],
                       "bounded_context": [{"revision_key": revision, "context": "fixture"}],
                       "rendered_briefing": "fixture"}
            output_value = {"contract": contract_name, "candidate_identity": "",
                            "verdicts": [{"revision_key": revision, "verdict": "OK"}]}
        else:
            raise AssertionError(contract)
        candidate_identity = hashlib.sha256(wp1.surface.canonical_bytes(payload)).hexdigest()
        input_raw = wp1.surface.canonical_bytes({"candidate_identity": candidate_identity, "payload": payload})
        output_value["candidate_identity"] = candidate_identity
        output_raw = (wp1.surface.canonical_bytes(output_value) if contract == "surface" else
                      json.dumps(output_value, ensure_ascii=False, separators=(",", ":")).encode("utf-8"))
        raw_root = root / f"raw/{contract}"
        raw_root.mkdir(parents=True)
        (raw_root / "input.json").write_bytes(input_raw)
        (raw_root / "output.json").write_bytes(output_raw)
        manifest_path = root / "manifest.json"
        manifest = wp1.parse_canonical_object(manifest_path.read_bytes(), "manifest")
        manifest["adapter_refs"].append({
            "contract": contract_name,
            "input_path": (raw_root / "input.json").relative_to(self.root).as_posix(),
            "input_sha256": hashlib.sha256(input_raw).hexdigest(),
            "output_path": (raw_root / "output.json").relative_to(self.root).as_posix(),
            "output_sha256": hashlib.sha256(output_raw).hexdigest(),
            "candidate_identity": candidate_identity,
        })
        manifest_path.write_bytes(wp1.canonical_bytes(manifest))
        results_path = root / "results.jsonl"
        row = wp1.parse_jsonl(results_path.read_bytes(), "results")[0]
        prefix = "surface" if contract == "surface" else "deep"
        row[prefix + "_verdict"] = "OK"
        row[prefix + "_observation"] = None
        results_path.write_bytes(wp1._jsonl([row]))
        manifest["results_sha256"] = hashlib.sha256(results_path.read_bytes()).hexdigest()
        manifest_path.write_bytes(wp1.canonical_bytes(manifest))

    def _rewrite_catalog(self, rows):
        rows = sorted(rows, key=lambda row: row["entry_revision_identity"])
        entries_path = self.root / catalog.CATALOG_PREFIX / "entries.jsonl"
        entries_path.write_bytes(wp1._jsonl(rows))
        manifest_path = self.root / catalog.CATALOG_PREFIX / "manifest.json"
        manifest = wp1.parse_canonical_object(manifest_path.read_bytes(), "manifest")
        manifest["entries_sha256"] = hashlib.sha256(entries_path.read_bytes()).hexdigest()
        for row in rows:
            manifest["source_identities"][row["component"]] = row["fixed_source_identity"]
        counts = Counter(row["component"] for row in rows)
        manifest["component_counts"] = {key: counts.get(key, 0) for key in manifest["component_counts"]}
        manifest["catalog_id"] = catalog.catalog_id(manifest)
        manifest_path.write_bytes(wp1.canonical_bytes(manifest))
        self.catalog_id = manifest["catalog_id"]


class ProjectionCacheTests(QueueFixture):
    def test_actual_projection_repeated_blobs_read_once_per_invocation(self):
        self._batch()
        self._commit("batch")
        with mock.patch.object(queue.git_evidence_reader, "projection_scope",
                               side_effect=lambda root: nullcontext()):
            with mock.patch.object(queue, "_git", wraps=queue._git) as git:
                uncached = queue._projection(self.root, "HEAD")
            uncached_calls = Counter(call.args[1:] for call in git.call_args_list
                                     if call.args[1:3] == ("cat-file", "blob"))
            self.assertGreater(max(uncached_calls.values()), 1)
        projections = []
        for _ in range(2):
            with mock.patch.object(queue, "_git", wraps=queue._git) as git:
                projections.append(queue._projection(self.root, "HEAD"))
            calls = Counter(call.args[1:] for call in git.call_args_list
                            if call.args[1:3] == ("cat-file", "blob"))
            self.assertTrue(calls)
            self.assertEqual(set(calls.values()), {1})
            self.assertEqual(set(calls), set(uncached_calls))
        self.assertEqual(projections[0], uncached)
        self.assertEqual(projections[0], projections[1])


class CatalogViewCacheTests(QueueFixture):
    """The lightweight catalog view must keep validating bytes and metadata."""

    def test_validated_bytes_are_reused_but_every_candidate_is_rechecked(self):
        with reader.projection_scope(self.root):
            tree = queue._tree(self.root, "HEAD")
            with mock.patch.object(queue, "_ordinary_blob", wraps=queue._ordinary_blob) as blob:
                first = queue._catalog_view(self.root, tree)
                self.assertEqual(blob.call_count, len(catalog.CANDIDATE_FILES))
                second = queue._catalog_view(self.root, tree)
                # A content-identity hit revalidates neither bytes nor digests.
                self.assertEqual(blob.call_count, len(catalog.CANDIDATE_FILES))
            self.assertEqual(first, second)
            # Metadata is still proven on every call, including a cache hit.
            for path in (f"{catalog.CATALOG_PREFIX}/entries.jsonl", catalog.SCHEMA_PATH):
                for entry in (None, ("120000", "blob", tree[path][2]), ("100644", "tree", tree[path][2])):
                    with self.subTest(path=path, entry=entry):
                        broken = dict(tree)
                        if entry is None:
                            broken.pop(path)
                        else:
                            broken[path] = entry
                        with self.assertRaises(wp1.ProductionReviewError):
                            queue._catalog_view(self.root, broken)
            # An unexpected catalog sibling fails the subtree check even on a hit.
            extra = dict(tree)
            extra[f"{catalog.CATALOG_PREFIX}/extra.json"] = ("100644", "blob", "0" * 40)
            with self.assertRaises(wp1.ProductionReviewError):
                queue._catalog_view(self.root, extra)

    def test_new_candidate_blob_and_manifest_identity_revalidate(self):
        with reader.projection_scope(self.root):
            manifest, entries, _ = queue._catalog_view(self.root, queue._tree(self.root, "HEAD"))
            # Identical entry rows under a different manifest: the catalog
            # identity changes, the complete rows are reused object-for-object.
            path = self.root / catalog.CATALOG_PREFIX / "manifest.json"
            value = wp1.parse_canonical_object(path.read_bytes(), "manifest")
            value["source_identities"]["engine"] = "commit:" + "9" * 40
            value["catalog_id"] = catalog.catalog_id(value)
            path.write_bytes(wp1.canonical_bytes(value))
            commit = self._commit("manifest-only catalog identity change")
            with mock.patch.object(queue, "_ordinary_blob", wraps=queue._ordinary_blob) as blob:
                manifest2, entries2, _ = queue._catalog_view(self.root, queue._tree(self.root, commit))
                self.assertEqual(blob.call_count, len(catalog.CANDIDATE_FILES))
            self.assertNotEqual(manifest["catalog_id"], manifest2["catalog_id"])
            self.assertEqual(len(entries), len(entries2))
            self.assertTrue(all(left is right for left, right in zip(entries, entries2)))


class QueueTests(QueueFixture):
    def _resize_and_init(self, count):
        database = queue.database_path(self.root)
        queue.checkpoint_path(self.root).unlink(missing_ok=True)
        scratch = queue.checkpoint_path(self.root).parent / "surface"
        if scratch.exists():
            import shutil
            shutil.rmtree(scratch)
        for path in (database, Path(str(database) + "-wal"), Path(str(database) + "-shm")):
            path.unlink(missing_ok=True)
        self.entries = [self._entry(str(i)) for i in range(count)]
        self._write_catalog()
        self._commit(f"catalog {count}")
        queue.init(self.root)

    def _surface_outputs(self):
        checkpoint = batch.show(self.root)
        outputs = {}
        for index, ref in enumerate(checkpoint["surface"]):
            envelope = wp1.surface.strict_json_bytes(Path(ref["input_path"]).read_bytes(), label="surface envelope")
            outputs[str(index)] = wp1.surface.canonical_bytes({
                "contract": wp1.surface.CONTRACT,
                "candidate_identity": ref["candidate_identity"],
                "results": [{"entry_revision_identity": entry["entry_revision_identity"], "verdict": "OK"}
                            for entry in envelope["payload"]["entries"]],
            })
        return outputs

    def _blocked_batch(self, batch):
        root = self._batch(batch=batch)
        self._add_overlapping_contract(root, "contextual")
        # Surface ISSUE + contextual ISSUE + pending adjudication is the
        # exact durable blocked shape consumed by current replay.
        surface_out = root / "raw/surface/output.json"
        value = wp1.parse_canonical_object(surface_out.read_bytes(), "surface output")
        value["results"][0].update({"verdict": "ISSUE", "observation": "blocked fixture"})
        surface_out.write_bytes(wp1.canonical_bytes(value))
        contextual_out = root / "raw/contextual/output.json"
        contextual_value = json.loads(contextual_out.read_bytes())
        contextual_value["verdicts"][0].update({"verdict": "ISSUE", "observation": "contextual issue"})
        contextual_out.write_bytes(wp1.canonical_bytes(contextual_value))
        result_path = root / "results.jsonl"
        result = wp1.parse_jsonl(result_path.read_bytes(), "results")[0]
        result.update({"surface_verdict": "ISSUE", "surface_observation": "blocked fixture",
                       "deep_verdict": "ISSUE", "deep_observation": "contextual issue",
                       "completion_level": "deep_reviewed", "final_state": "blocked",
                       "input_sha256": hashlib.sha256((root / "raw/surface/input.json").read_bytes()).hexdigest(),
                       "output_sha256": hashlib.sha256(surface_out.read_bytes()).hexdigest()})
        result_path.write_bytes(wp1._jsonl([result]))
        adjud_path = root / "adjudications.jsonl"
        adjud_path.write_bytes(wp1._jsonl([{"schema_version": 1,
            "entry_revision_identity": result["entry_revision_identity"],
            "observation_sha256": hashlib.sha256(b"contextual issue").hexdigest(),
            "disposition": "pending", "evidence_path": None, "evidence_commit": None,
            "evidence_snapshot": None, "conclusion": "blocked fixture", "repair_required": False}]))
        manifest_path = root / "manifest.json"
        manifest = wp1.parse_canonical_object(manifest_path.read_bytes(), "manifest")
        manifest["results_sha256"] = hashlib.sha256(result_path.read_bytes()).hexdigest()
        manifest["adjudications_sha256"] = hashlib.sha256(adjud_path.read_bytes()).hexdigest()
        manifest["adapter_refs"][0]["output_sha256"] = hashlib.sha256(surface_out.read_bytes()).hexdigest()
        manifest["adapter_refs"][1]["output_sha256"] = hashlib.sha256(contextual_out.read_bytes()).hexdigest()
        manifest_path.write_bytes(wp1.canonical_bytes(manifest))
        return root

    def test_c12_real_git_retry_blocked_abandon_restores_exact_committed_tuple(self):
        root = self._blocked_batch("blocked-winner")
        self._commit("blocked winner")
        queue.init(self.root)
        before = queue.business_rows(queue.database_path(self.root))[0][0]
        batch.start(self.root, limit=1, retry_blocked=True)
        batch.abandon(self.root)
        after = queue.business_rows(queue.database_path(self.root))[0][0]
        self.assertEqual(after, before)
        self.assertEqual(queue.status(self.root)["explicit_overrides"], {"blocked": 1})

    def test_c21_sqlite_first_exact_winner_recover_then_abandon_is_byte_exact(self):
        self._blocked_batch("blocked-exact")
        self._commit("blocked exact winner")
        queue.init(self.root)
        winner = queue.business_rows(queue.database_path(self.root))[0][0]
        batch.start(self.root, limit=1, retry_blocked=True)
        with sqlite3.connect(queue.database_path(self.root)) as con:
            con.execute("INSERT OR REPLACE INTO state_override VALUES (?,?,?,?,?,?,?)", winner)
            con.commit()
        batch.recover(self.root)
        self.assertEqual(queue.business_rows(queue.database_path(self.root))[0][0][2], "reserved")
        batch.abandon(self.root)
        self.assertEqual(queue.business_rows(queue.database_path(self.root))[0][0], winner)

    def test_c22_tampered_prior_state_rejects_before_sqlite_mutation(self):
        self._resize_and_init(1)
        batch.start(self.root, limit=1)
        path = queue.checkpoint_path(self.root)
        value = batch._load(path)
        value["entry_snapshots"][0]["prior_effective_state"] = "blocked"
        batch._atomic(path, batch._checkpoint_bytes(value))
        before = queue.business_rows(queue.database_path(self.root))[0]
        with self.assertRaisesRegex(wp1.ProductionReviewError, "non-queued"):
            batch.recover(self.root)
        self.assertEqual(queue.business_rows(queue.database_path(self.root))[0], before)
        path.unlink()

    def test_c23_retry_attempt_and_batch_identity_are_deterministic(self):
        self._blocked_batch("blocked-attempt")
        self._commit("blocked attempt winner")
        queue.init(self.root)
        first = batch.start(self.root, limit=1, retry_blocked=True)
        checkpoint = batch.show(self.root)
        self.assertEqual(checkpoint["attempt"], 2)
        self.assertEqual(first["batch_id"], batch._batch_id("retry_blocked", checkpoint["selected"], 2))
        batch.abandon(self.root)
        second = batch.start(self.root, limit=1, retry_blocked=True)
        self.assertEqual(second["batch_id"], first["batch_id"])
        self.assertEqual(batch.show(self.root)["attempt"], 2)
        batch.abandon(self.root)

    def test_c23_checkpoint_attempt_tamper_is_rejected_before_sqlite_open(self):
        cases = (("queued", False), ("retry_blocked", True))
        for mode, retry_blocked in cases:
            with self.subTest(mode=mode):
                # Each mode is an independent transaction fixture.  In
                # particular, queue.init must not inherit the previous mode's
                # database, and SQLite's WAL/checkpoint bytes are not a stable
                # representation of the durable projection.
                for candidate in (queue.checkpoint_path(self.root), queue.database_path(self.root),
                                  Path(str(queue.database_path(self.root)) + "-wal"),
                                  Path(str(queue.database_path(self.root)) + "-shm")):
                    candidate.unlink(missing_ok=True)
                if retry_blocked:
                    self._blocked_batch("blocked-attempt-authority")
                    self._commit("blocked attempt authority")
                else:
                    self._resize_and_init(1)
                if retry_blocked:
                    queue.init(self.root)
                batch.start(self.root, limit=1, retry_blocked=retry_blocked)
                path = queue.checkpoint_path(self.root)
                value = batch._load(path)
                value["attempt"] = 9
                value["batch_id"] = batch._batch_id(mode, value["selected"], value["attempt"])
                batch._atomic(path, batch._checkpoint_bytes(value))
                database = queue.database_path(self.root)
                before = queue.business_rows(database)
                with mock.patch.object(queue, "_connect", side_effect=AssertionError("SQLite opened before checkpoint validation")):
                    with self.assertRaisesRegex(wp1.ProductionReviewError, "authoritative winners"):
                        batch.recover(self.root)
                self.assertEqual(queue.business_rows(database), before)
                path.unlink()
                for candidate in (database, Path(str(database) + "-wal"), Path(str(database) + "-shm")):
                    candidate.unlink(missing_ok=True)

    def test_c24_missing_reservation_rejects_canonical_replacement_before_sqlite(self):
        self._resize_and_init(2)
        batch.start(self.root, limit=1)
        path = queue.checkpoint_path(self.root)
        value = batch._load(path)
        selected_revision = value["selected"][0]
        replacement = next(entry for entry in self.entries
                           if entry["entry_revision_identity"] != selected_revision)
        value["selected"] = [replacement["entry_revision_identity"]]
        value["selected_sha256"] = batch._sha(wp1.canonical_bytes(value["selected"]))
        value["entry_snapshots"] = [{**replacement, "prior_effective_state": "queued",
                                      "row_sha256": batch._sha(wp1.canonical_bytes(replacement))}]
        value["batch_id"] = batch._batch_id("queued", value["selected"], value["attempt"])
        batch._atomic(path, batch._checkpoint_bytes(value))
        database = queue.database_path(self.root)
        with sqlite3.connect(database) as con:
            con.execute("DELETE FROM state_override")
            con.commit()
        before = {candidate: candidate.read_bytes() for candidate in
                  (database, Path(str(database) + "-wal"), Path(str(database) + "-shm"))
                  if candidate.exists()}
        with self.assertRaisesRegex(wp1.ProductionReviewError, "stable selection"):
            batch.recover(self.root)
        after = {candidate: candidate.read_bytes() for candidate in before}
        self.assertEqual(after, before)
        path.unlink()
        for candidate in (database, Path(str(database) + "-wal"), Path(str(database) + "-shm")):
            candidate.unlink(missing_ok=True)

    def test_c12_sqlite_first_abandon_crash_checkpoint_remaining_recovers_blocked(self):
        self._blocked_batch("blocked-crash")
        self._commit("blocked crash winner")
        queue.init(self.root)
        batch.start(self.root, limit=1, retry_blocked=True)
        with sqlite3.connect(queue.database_path(self.root)) as con:
            con.execute("DELETE FROM state_override")
            con.commit()
        batch.abandon(self.root)
        self.assertEqual(queue.status(self.root)["explicit_overrides"], {"blocked": 1})
        self.assertFalse(batch.show(self.root)["active"])

    def test_c12_checkpoint_first_import_with_sqlite_lag_and_deleted_row_recovers(self):
        self._resize_and_init(1)
        batch.start(self.root, limit=1)
        batch.surface_export(self.root)
        outputs = self._surface_outputs()
        with sqlite3.connect(queue.database_path(self.root)) as con:
            con.execute("DELETE FROM state_override")
            con.commit()
        imported = batch.surface_import(self.root, outputs)
        self.assertEqual(imported["imported"], 1)
        with sqlite3.connect(queue.database_path(self.root)) as con:
            con.execute("DELETE FROM state_override")
            con.commit()
        batch.recover(self.root)
        self.assertEqual(queue.status(self.root)["explicit_overrides"], {"screened": 1})

    def test_c12_real_surface_full_and_lane_group_round_trip(self):
        for count, expected_lanes in ((1, 1), (4, 4)):
            with self.subTest(count=count):
                self._resize_and_init(count)
                batch.start(self.root, limit=count)
                exported = batch.surface_export(self.root)
                self.assertEqual(exported["runs"], 1)
                checkpoint = batch.show(self.root)
                self.assertEqual(len(checkpoint["surface"]), expected_lanes)
                if count == 4:
                    self.assertTrue(checkpoint["surface"][0]["group_manifest_path"])
                batch.surface_import(self.root, self._surface_outputs())
                self.assertEqual(queue.status(self.root)["explicit_overrides"], {"screened": count})
                batch.abandon(self.root, discard_uncommitted_results=True)
                runtime = queue.checkpoint_path(self.root).parent
                self.assertEqual(list(runtime.glob(".active-batch.json.tmp")), [])
                self.assertEqual(list((runtime / "surface").glob("*")) if (runtime / "surface").exists() else [], [])

    def test_c13_c16_integer_output_key_is_rejected_before_any_write(self):
        self._resize_and_init(1)
        batch.start(self.root, limit=1)
        batch.surface_export(self.root)
        outputs = self._surface_outputs()
        with self.assertRaisesRegex(wp1.ProductionReviewError, "exact strings"):
            batch.surface_import(self.root, {0: outputs["0"]})
        self.assertIsNone(batch._load(queue.checkpoint_path(self.root))["surface"][0]["output_path"])
        batch.abandon(self.root)

    def test_c15_group_consumer_layout_never_touches_preexisting_workspace_task(self):
        self._resize_and_init(4)
        task_file = self.root / ".ai/task/preexisting/STATE.json"
        task_file.parent.mkdir(parents=True)
        task_file.write_bytes(b"keep me")
        batch.start(self.root, limit=4)
        batch.surface_export(self.root)
        self.assertEqual(task_file.read_bytes(), b"keep me")
        self.assertEqual([p.relative_to(self.root).as_posix() for p in self.root.glob(".ai/task/**/SURFACE-*")], [])
        batch.abandon(self.root)

    def test_c12_reimport_requires_exact_output_key_set_and_bytes(self):
        self._resize_and_init(1)
        batch.start(self.root, limit=1)
        batch.surface_export(self.root)
        outputs = self._surface_outputs()
        with self.assertRaisesRegex(wp1.ProductionReviewError, "missing or extra"):
            batch.surface_import(self.root, {"0": outputs["0"], "extra": outputs["0"]})
        with self.assertRaisesRegex(wp1.ProductionReviewError, "rejected"):
            batch.surface_import(self.root, {"0": b"missing output"})
        batch.surface_import(self.root, outputs)
        with self.assertRaisesRegex(wp1.ProductionReviewError, "changed"):
            batch.surface_import(self.root, {"0": outputs["0"][:-1] + b" "})
        batch.abandon(self.root, discard_uncommitted_results=True)

    def test_c12_stale_atomic_temp_is_controlled_and_removed(self):
        self._resize_and_init(1)
        runtime = queue.checkpoint_path(self.root).parent
        runtime.mkdir(parents=True, exist_ok=True)
        (runtime / ".active-batch.json.tmp").write_bytes(b"stale")
        batch.start(self.root, limit=1)
        batch.surface_export(self.root)
        self.assertFalse((runtime / ".active-batch.json.tmp").exists())
        batch.abandon(self.root)
        residue = [p.name for p in runtime.iterdir()
                   if p.name not in {queue.LOCK_NAME, queue.DATABASE_NAME}]
        self.assertEqual(residue, [])

    def test_real_git_sqlite_batch_start_duplicate_and_abandon_restores_queue(self):
        queue.init(self.root)
        started = batch.start(self.root, limit=1)
        self.assertEqual(started["selected"], 1)
        checkpoint = batch.show(self.root)
        self.assertEqual(checkpoint["entry_snapshots"][0]["prior_effective_state"], "queued")
        with self.assertRaisesRegex(wp1.ProductionReviewError, "active batch"):
            batch.start(self.root, limit=1)
        batch.abandon(self.root)
        self.assertFalse(batch.show(self.root)["active"])
        self.assertEqual(queue.status(self.root)["implicit_queued"], 2)

    def test_catalog_loader_allows_only_planned_quality_sibling(self):
        self.assertEqual(queue.init(self.root)["catalog_id"], self.catalog_id)
        extra = self.root / "i18n/quality/production-review-v2-lite/unplanned.txt"
        extra.write_text("unexpected\n", encoding="utf-8")
        self._commit("unplanned quality sibling")
        with self.assertRaisesRegex(wp1.ProductionReviewError, "sibling|extra"):
            queue.rebuild(self.root)

    def test_implicit_queued_seven_state_schema_and_deterministic_rebuild(self):
        first = queue.init(self.root)
        self.assertEqual(first["implicit_queued"], 2)
        db = queue.database_path(self.root)
        with closing(sqlite3.connect(db)) as connection:
            tables = {row[0] for row in connection.execute("SELECT name FROM sqlite_master WHERE type='table'")}
            self.assertEqual(tables, {"meta", "state_override", "reconciliation"})
            self.assertEqual(queue.BUSINESS_STATES,
                             {"queued", "reserved", "screened", "deep_required", "repair_required", "done", "blocked"})
            for state in ("queued", "invalid"):
                with self.assertRaises(sqlite3.IntegrityError):
                    connection.execute("INSERT INTO state_override VALUES (?,?,?,?,?,?,?)",
                                       ("f" * 64, "e" * 64, state, None, 0, None, STAMP))
        self._batch()
        self._commit("batch")
        queue.rebuild(self.root)
        before = queue.business_rows(db)
        db.unlink()
        queue.rebuild(self.root)
        self.assertEqual(queue.business_rows(db), before)
        self.assertEqual(queue.status(self.root)["explicit_overrides"], {"done": 1})

    def test_failed_validation_preserves_old_database_and_dirty_evidence_is_rejected(self):
        queue.init(self.root)
        db = queue.database_path(self.root)
        old = db.read_bytes()
        root = self._batch()
        (root / "results.jsonl").write_bytes(b"{bad\n")
        self._commit("bad batch")
        with self.assertRaises(wp1.ProductionReviewError):
            queue.rebuild(self.root)
        self.assertEqual(db.read_bytes(), old)
        subprocess.run(["git", "reset", "--hard", "HEAD^", "-q"], cwd=self.root, check=True)
        dirty = self.root / "evidence/production-review-v2-lite/dirty"
        dirty.write_text("x")
        with self.assertRaisesRegex(wp1.ProductionReviewError, "clean"):
            queue.rebuild(self.root)

    def test_evidence_rejects_duplicate_keys_invalid_utf8_and_extra_keys(self):
        queue.init(self.root)
        old = queue.database_path(self.root).read_bytes()
        for label in ("duplicate", "utf8", "extra"):
            with self.subTest(label=label):
                root = self._batch()
                path = root / "results.jsonl"
                if label == "duplicate":
                    path.write_bytes(b'{"schema_version":1,"schema_version":1}\n')
                elif label == "utf8":
                    path.write_bytes(b"\xff\n")
                else:
                    row = wp1.parse_jsonl(path.read_bytes(), "result")[0]
                    row["extra"] = True
                    path.write_bytes(wp1._jsonl([row]))
                manifest_path = root / "manifest.json"
                manifest = wp1.parse_canonical_object(manifest_path.read_bytes(), "manifest")
                manifest["results_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
                manifest_path.write_bytes(wp1.canonical_bytes(manifest))
                self._commit("invalid " + label)
                with self.assertRaises(wp1.ProductionReviewError):
                    queue.rebuild(self.root)
                self.assertEqual(queue.database_path(self.root).read_bytes(), old)
                subprocess.run(["git", "reset", "--hard", "HEAD^", "-q"], cwd=self.root, check=True)

    def test_catalog_reuses_strict_traversal_duplicate_extra_and_nonliteral_checks(self):
        cases = ("traversal", "duplicate-logical", "extra-file", "nonliteral")
        for label in cases:
            with self.subTest(label=label):
                rows = [dict(row) for row in self.entries]
                if label == "traversal":
                    row = rows[0]; row["normalized_path"] = "../tome.lua"
                    core = {"component": row["component"], "duplicate_index": 0, "function_name": "t",
                            "normalized_source_tag": row["source_tag"], "section": row["section"],
                            "source": row["source"], "translation_path": row["normalized_path"]}
                    row["call_locator"] = catalog._plain_id(catalog.CALL_LOCATOR_KIND, "locator", core)
                    row["logical_entry_identity"] = wp1.surface.logical_entry_identity(
                        component=row["component"], normalized_path=row["normalized_path"],
                        call_locator=row["call_locator"], source_tag=row["source_tag"])
                    row["entry_revision_identity"] = wp1.surface.entry_revision_identity(
                        logical_entry_identity=row["logical_entry_identity"], source=row["source"], target=row["target"],
                        fixed_source_identity=row["fixed_source_identity"],
                        terminology_snapshot=row["terminology_snapshot_sha256"], rules_version=row["rules_version"],
                        args_order=row["risk"].get("args_order"))
                    self._rewrite_catalog(rows)
                elif label == "duplicate-logical":
                    first, row = rows
                    row.update({key: first[key] for key in ("source", "source_sha256", "normalized_path",
                                                            "call_locator", "logical_entry_identity")})
                    row["risk"] = dict(row["risk"]); row["risk"]["source_utf8_bytes"] = len(row["source"].encode())
                    row["entry_revision_identity"] = wp1.surface.entry_revision_identity(
                        logical_entry_identity=row["logical_entry_identity"], source=row["source"], target=row["target"],
                        fixed_source_identity=row["fixed_source_identity"],
                        terminology_snapshot=row["terminology_snapshot_sha256"], rules_version=row["rules_version"],
                        args_order=row["risk"].get("args_order"))
                    self._rewrite_catalog(rows)
                elif label == "extra-file":
                    extra = self.root / catalog.CATALOG_PREFIX / "extra.json"
                    extra.write_text("{}", encoding="utf-8")
                else:
                    rows[0]["source"] = ["not", "a", "literal"]
                    self._rewrite_catalog(rows)
                self._commit("invalid catalog " + label)
                with self.assertRaises(wp1.ProductionReviewError):
                    queue.init(self.root)
                subprocess.run(["git", "reset", "--hard", "HEAD^", "-q"], cwd=self.root, check=True)
                self.entries = [self._entry("1"), self._entry("2")]
                self._write_catalog()

    def test_results_require_bound_validator_accepted_adapter_bytes(self):
        for label in ("empty", "unbound", "mismatched", "invalid-raw"):
            with self.subTest(label=label):
                root = self._batch(batch="batch-" + label)
                manifest_path, results_path = root / "manifest.json", root / "results.jsonl"
                manifest = wp1.parse_canonical_object(manifest_path.read_bytes(), "manifest")
                row = wp1.parse_jsonl(results_path.read_bytes(), "results")[0]
                if label == "empty":
                    manifest["adapter_refs"] = []
                    for path in (root / "raw").rglob("*"):
                        if path.is_file(): path.unlink()
                elif label == "unbound":
                    row["input_sha256"] = "e" * 64
                elif label == "mismatched":
                    manifest["adapter_refs"][0]["output_sha256"] = "f" * 64
                else:
                    output = root / "raw/surface/output.json"
                    output.write_bytes(b'{"invalid":true}')
                    digest = hashlib.sha256(output.read_bytes()).hexdigest()
                    manifest["adapter_refs"][0]["output_sha256"] = digest
                    row["output_sha256"] = digest
                results_path.write_bytes(wp1._jsonl([row]))
                manifest["results_sha256"] = hashlib.sha256(results_path.read_bytes()).hexdigest()
                manifest_path.write_bytes(wp1.canonical_bytes(manifest))
                self._commit("invalid adapter " + label)
                with self.assertRaises(wp1.ProductionReviewError):
                    queue.rebuild(self.root)
                subprocess.run(["git", "reset", "--hard", "HEAD^", "-q"], cwd=self.root, check=True)

    def test_results_reject_borrowed_run_for_wrong_revision_surface_and_contextual(self):
        for contract in ("surface", "contextual"):
            with self.subTest(contract=contract):
                self._batch(batch="batch-wrong-" + contract, contract=contract, adapter_entry_index=1)
                self._commit("wrong revision " + contract)
                with self.assertRaisesRegex(wp1.ProductionReviewError, "revision|union|membership"):
                    queue.rebuild(self.root)
                subprocess.run(["git", "reset", "--hard", "HEAD^", "-q"], cwd=self.root, check=True)

    def test_results_match_accepted_contract_verdict_and_observation(self):
        for contract in ("surface", "contextual"):
            with self.subTest(contract=contract):
                root = self._batch(batch="batch-verdict-" + contract, contract=contract)
                results_path = root / "results.jsonl"
                row = wp1.parse_jsonl(results_path.read_bytes(), "results")[0]
                prefix = "surface" if contract == "surface" else "deep"
                row[prefix + "_verdict"] = "ISSUE"
                row[prefix + "_observation"] = "forged observation"
                results_path.write_bytes(wp1._jsonl([row]))
                manifest_path = root / "manifest.json"
                manifest = wp1.parse_canonical_object(manifest_path.read_bytes(), "manifest")
                manifest["results_sha256"] = hashlib.sha256(results_path.read_bytes()).hexdigest()
                manifest_path.write_bytes(wp1.canonical_bytes(manifest))
                self._commit("forged verdict " + contract)
                with self.assertRaisesRegex(wp1.ProductionReviewError, "verdict|observation|accepted"):
                    queue.rebuild(self.root)
                subprocess.run(["git", "reset", "--hard", "HEAD^", "-q"], cwd=self.root, check=True)

    def test_results_validate_matching_surface_contextual_overlap(self):
        root = self._batch(batch="batch-overlap", contract="surface")
        self._add_overlapping_contract(root, "contextual")
        self._commit("matching cross-contract overlap")
        with self.assertRaisesRegex(wp1.ProductionReviewError, "surface ISSUE"):
            queue.rebuild(self.root)

    def test_results_require_null_fields_for_absent_contract(self):
        for contract, forged_prefix in (("surface", "deep"), ("contextual", "surface")):
            with self.subTest(absent=forged_prefix):
                root = self._batch(batch="batch-absent-" + forged_prefix, contract=contract)
                results_path = root / "results.jsonl"
                row = wp1.parse_jsonl(results_path.read_bytes(), "results")[0]
                row[forged_prefix + "_verdict"] = "OK"
                results_path.write_bytes(wp1._jsonl([row]))
                manifest_path = root / "manifest.json"
                manifest = wp1.parse_canonical_object(manifest_path.read_bytes(), "manifest")
                manifest["results_sha256"] = hashlib.sha256(results_path.read_bytes()).hexdigest()
                manifest_path.write_bytes(wp1.canonical_bytes(manifest))
                self._commit("forged absent contract " + forged_prefix)
                with self.assertRaisesRegex(wp1.ProductionReviewError, "verdict|observation|accepted"):
                    queue.rebuild(self.root)
                subprocess.run(["git", "reset", "--hard", "HEAD^", "-q"], cwd=self.root, check=True)

    def test_results_reject_cross_contract_mismatch_in_both_directions(self):
        for primary, overlapping, forged_prefix in (
                ("surface", "contextual", "deep"),
                ("contextual", "surface", "surface")):
            with self.subTest(forged=forged_prefix):
                root = self._batch(batch="batch-mismatch-" + forged_prefix, contract=primary)
                self._add_overlapping_contract(root, overlapping)
                results_path = root / "results.jsonl"
                row = wp1.parse_jsonl(results_path.read_bytes(), "results")[0]
                row[forged_prefix + "_verdict"] = "ISSUE"
                row[forged_prefix + "_observation"] = "forged observation"
                results_path.write_bytes(wp1._jsonl([row]))
                manifest_path = root / "manifest.json"
                manifest = wp1.parse_canonical_object(manifest_path.read_bytes(), "manifest")
                manifest["results_sha256"] = hashlib.sha256(results_path.read_bytes()).hexdigest()
                manifest_path.write_bytes(wp1.canonical_bytes(manifest))
                self._commit("forged cross-contract " + forged_prefix)
                with self.assertRaisesRegex(wp1.ProductionReviewError, "verdict|observation|accepted"):
                    queue.rebuild(self.root)
                subprocess.run(["git", "reset", "--hard", "HEAD^", "-q"], cwd=self.root, check=True)

    def test_durable_batch_schema_versions_reject_json_true(self):
        for boundary in ("manifest", "result", "adjudication", "gates"):
            with self.subTest(boundary=boundary):
                root = self._batch(batch="batch-bool-" + boundary)
                manifest_path = root / "manifest.json"
                manifest = wp1.parse_canonical_object(manifest_path.read_bytes(), "manifest")
                if boundary == "manifest":
                    manifest["schema_version"] = True
                elif boundary == "result":
                    path = root / "results.jsonl"
                    row = wp1.parse_jsonl(path.read_bytes(), "result")[0]
                    row["schema_version"] = True
                    path.write_bytes(wp1._jsonl([row]))
                    manifest["results_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
                elif boundary == "adjudication":
                    path = root / "adjudications.jsonl"
                    row = {"schema_version": True, "entry_revision_identity": self.entries[0]["entry_revision_identity"],
                           "observation_sha256": "a" * 64, "disposition": "advisory",
                           "evidence_path": None, "evidence_commit": None, "evidence_snapshot": None,
                           "conclusion": "fixture", "repair_required": False}
                    path.write_bytes(wp1._jsonl([row]))
                    manifest["adjudications_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
                else:
                    path = root / "gates.json"
                    path.write_bytes(wp1.canonical_bytes({"schema_version": True, "commands": []}))
                    manifest["gates_sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
                manifest_path.write_bytes(wp1.canonical_bytes(manifest))
                self._commit("boolean schema " + boundary)
                with self.assertRaisesRegex(wp1.ProductionReviewError, "schema"):
                    queue.rebuild(self.root)
                subprocess.run(["git", "reset", "--hard", "HEAD^", "-q"], cwd=self.root, check=True)

    def test_split_raw_and_core_commits_are_rejected(self):
        queue.init(self.root)
        root = self._batch(batch="batch-split")
        subprocess.run(["git", "add", str(root / "raw")], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-qm", "raw before core"], cwd=self.root, check=True)
        raw_commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=self.root, text=True).strip()
        manifest_path = root / "manifest.json"
        manifest = wp1.parse_canonical_object(manifest_path.read_bytes(), "manifest")
        manifest["base_commit"] = raw_commit
        manifest_path.write_bytes(wp1.canonical_bytes(manifest))
        self._commit("batch core after raw")
        with self.assertRaisesRegex(wp1.ProductionReviewError, "raw.*one commit|one commit.*raw"):
            queue.rebuild(self.root)

    def test_merged_sibling_identical_publications_are_rejected_as_ambiguous(self):
        queue.init(self.root)
        base = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=self.root, text=True).strip()
        self._batch(batch="batch-siblings")
        first = self._commit("first identical publication")

        subprocess.run(["git", "checkout", "-qb", "sibling-publication", base],
                       cwd=self.root, check=True)
        self._batch(batch="batch-siblings")
        self._commit("second identical publication")
        subprocess.run(["git", "merge", "-q", "--no-ff", first, "-m", "merge publications"],
                       cwd=self.root, check=True)

        with self.assertRaisesRegex(wp1.ProductionReviewError, "one commit"):
            queue.rebuild(self.root)

    def test_current_tree_only_and_same_commit_revert_deletion(self):
        queue.init(self.root)
        self._batch()
        committed = self._commit("batch")
        queue.rebuild(self.root)
        self.assertEqual(queue.status(self.root)["implicit_queued"], 1)
        subprocess.run(["git", "revert", "--no-edit", committed], cwd=self.root,
                       check=True, stdout=subprocess.DEVNULL)
        queue.rebuild(self.root)
        self.assertEqual(queue.status(self.root)["implicit_queued"], 2)
        queue.rebuild(self.root, treeish=committed)
        self.assertEqual(queue.status(self.root, treeish=committed)["implicit_queued"], 1)

    def test_same_path_replacement_revert_restores_prior_publication(self):
        queue.init(self.root)
        root = self._batch(batch="batch-replaced")
        original_commit = self._commit("original batch publication")
        queue.rebuild(self.root)
        self.assertEqual(queue.status(self.root)["explicit_overrides"], {"done": 1})

        input_path = root / "raw/surface/input.json"
        input_value = wp1.parse_canonical_object(input_path.read_bytes(), "surface input")
        input_value["payload"]["rendered_briefing"] = "replacement fixture"
        candidate_identity = hashlib.sha256(wp1.surface.canonical_bytes(input_value["payload"])).hexdigest()
        input_value["candidate_identity"] = candidate_identity
        input_path.write_bytes(wp1.surface.canonical_bytes(input_value))
        output_path = root / "raw/surface/output.json"
        output_value = wp1.parse_canonical_object(output_path.read_bytes(), "surface output")
        output_value["candidate_identity"] = candidate_identity
        output_path.write_bytes(wp1.surface.canonical_bytes(output_value))
        input_hash = hashlib.sha256(input_path.read_bytes()).hexdigest()
        output_hash = hashlib.sha256(output_path.read_bytes()).hexdigest()

        results_path = root / "results.jsonl"
        result = wp1.parse_jsonl(results_path.read_bytes(), "results")[0]
        result.update({"input_sha256": input_hash, "output_sha256": output_hash,
                       "final_state": "blocked"})
        results_path.write_bytes(wp1._jsonl([result]))
        adjudications_path = root / "adjudications.jsonl"
        adjudications_path.write_bytes(wp1._jsonl([{
            "schema_version": 1, "entry_revision_identity": result["entry_revision_identity"],
            "observation_sha256": "a" * 64, "disposition": "advisory",
            "evidence_path": None, "evidence_commit": None, "evidence_snapshot": None,
            "conclusion": "replacement fixture", "repair_required": False}]))
        gates_path = root / "gates.json"
        gates_path.write_bytes(wp1.canonical_bytes({"schema_version": 1,
                                                     "commands": ["replacement fixture"]}))
        manifest_path = root / "manifest.json"
        manifest = wp1.parse_canonical_object(manifest_path.read_bytes(), "manifest")
        manifest["base_commit"] = original_commit
        manifest["adapter_refs"][0].update({
            "candidate_identity": candidate_identity, "input_sha256": input_hash,
            "output_sha256": output_hash})
        manifest["results_sha256"] = hashlib.sha256(results_path.read_bytes()).hexdigest()
        manifest["adjudications_sha256"] = hashlib.sha256(adjudications_path.read_bytes()).hexdigest()
        manifest["gates_sha256"] = hashlib.sha256(gates_path.read_bytes()).hexdigest()
        manifest_path.write_bytes(wp1.canonical_bytes(manifest))
        replacement_commit = self._commit("same-path replacement publication")
        with self.assertRaisesRegex(wp1.ProductionReviewError, "adjudications must exactly cover"):
            queue.rebuild(self.root)

        subprocess.run(["git", "revert", "--no-edit", replacement_commit], cwd=self.root,
                       check=True, stdout=subprocess.DEVNULL)
        queue.rebuild(self.root)
        self.assertEqual(queue.status(self.root)["explicit_overrides"], {"done": 1})

    def test_progress_cli_all_public_queue_reports(self):
        self._batch()
        self._commit("review for CLI")
        command = """import argparse, sys
from pathlib import Path
from tools.i18nlib import cli_production
from tools.i18nlib import production_review_v2_lite_queue as queue
fixture, action = Path(sys.argv[1]), sys.argv[2]
operation = getattr(queue, action)
setattr(cli_production.production_review_v2_lite_queue, action,
        lambda _root, **kwargs: operation(fixture, **kwargs))
raise SystemExit(cli_production._production(argparse.Namespace(
    production_command='queue', production_action=action, treeish='HEAD', json=sys.argv[3]=='json')))
"""
        for action, form in (("init", "json"), ("rebuild", "json"), ("check", "json"),
                             ("status", "json"), ("status", "text")):
            with self.subTest(action=action, form=form):
                completed = subprocess.run([sys.executable, "-B", "-c", command,
                                            str(self.root), action, form], cwd=ROOT,
                                           capture_output=True, text=True, timeout=20)
                self.assertEqual(completed.returncode, 0, completed.stderr)
                if form == "json":
                    report = json.loads(completed.stdout)
                    self.assertEqual(report["override_basis"], "sqlite_state_codes")
                    self.assertEqual(report["progress"]["committed_done_by_completion_level"],
                                     {"surface_only": 1, "deep_reviewed": 0})
                else:
                    self.assertIn("raw state codes", completed.stdout)
                    self.assertIn("committed evidence progress; eligible=2", completed.stdout)
                    self.assertIn("surface_covered=1/2", completed.stdout)
                    self.assertIn("deep_reviewed=0/2", completed.stdout)
                    self.assertIn("surface_only=1; deep_reviewed=0", completed.stdout)

    def test_progress_committed_basis_single_replay_and_active_transient(self):
        self._batch(batch="first")
        self._commit("first accepted result")
        self._batch(batch="second")
        self._commit("duplicate review")
        with mock.patch.object(queue, "_projection_contents", wraps=queue._projection_contents) as replay:
            initialized = queue.init(self.root)
        self.assertEqual(replay.call_count, 1)
        with mock.patch.object(queue, "_projection_contents", wraps=queue._projection_contents) as replay:
            rebuilt = queue.rebuild(self.root)
        self.assertEqual(replay.call_count, 1)
        self.assertEqual(initialized["progress"], rebuilt["progress"])
        self.assertEqual(initialized["override_basis"], "sqlite_state_codes")
        with mock.patch.object(queue, "_projection_contents", wraps=queue._projection_contents) as replay:
            report = queue.status(self.root)
        self.assertEqual(replay.call_count, 1)
        progress = report["progress"]
        self.assertEqual(progress, initialized["progress"])
        self.assertEqual(progress["metrics"]["surface_covered"]["count"], 1)
        self.assertEqual(progress["metrics"]["deep_reviewed"]["count"], 0)
        self.assertEqual(progress["committed_done_by_completion_level"],
                         {"surface_only": 1, "deep_reviewed": 0})
        self.assertEqual(progress["eligible"], 2)
        # Active SQLite can temporarily claim another done row; durable coverage stays 1.
        with closing(queue._connect(queue.database_path(self.root))) as connection:
            connection.execute("INSERT INTO state_override VALUES (?,?,?,?,?,?,?)",
                               (self.entries[1]["entry_revision_identity"],
                                self.entries[1]["logical_entry_identity"], "done", "active", 1, "f" * 64, STAMP))
            connection.commit()
        queue.checkpoint_path(self.root).write_text("{}")
        with mock.patch.object(queue, "writer_active", return_value=True):
            active = queue.status(self.root)
            self.assertEqual(active["explicit_overrides"], {"done": 2})
            self.assertEqual(active["override_basis"], "sqlite_state_codes")
            self.assertEqual(active["progress"], progress)
            queue.database_path(self.root).unlink()
            fallback = queue.check(self.root)
            self.assertFalse(fallback["ok"])
            self.assertEqual(fallback["override_basis"], "committed_evidence_state_codes")
            self.assertEqual(fallback["progress"], progress)
        missing = queue.status(self.root, allow_missing=True)
        self.assertFalse(missing["active_writer"])
        self.assertEqual(missing["progress"], progress)

    def test_lock_is_nonblocking_and_readers_report_writer(self):
        lock = queue.repository_lock_path(self.root)
        lock.parent.mkdir(parents=True, exist_ok=True)
        with lock.open("a+b") as handle:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            self.assertTrue(queue.writer_active(self.root))
            with self.assertRaisesRegex(wp1.ProductionReviewError, "lock"):
                queue.init(self.root)
            self.assertTrue(queue.status(self.root)["active_writer"])
            self.assertTrue(queue.check(self.root)["active_writer"])
        self.assertFalse(queue.writer_active(self.root))

    def test_cli_check_exits_nonzero_for_drift_during_active_writer(self):
        queue.init(self.root)
        with closing(sqlite3.connect(queue.database_path(self.root))) as connection:
            connection.execute("UPDATE meta SET catalog_id=?", ("f" * 64,))
            connection.commit()
        lock = queue.repository_lock_path(self.root)
        command = """import argparse, sys
from pathlib import Path
from tools.i18nlib import cli_production
from tools.i18nlib import production_review_v2_lite_queue as queue
fixture = Path(sys.argv[1])
check = queue.check
cli_production.production_review_v2_lite_queue.check = lambda _root: check(fixture)
raise SystemExit(cli_production._production(argparse.Namespace(
    production_command='queue', production_action='check')))
"""
        with lock.open("a+b") as handle:
            fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
            result = subprocess.run([sys.executable, "-B", "-c", command, str(self.root)], cwd=ROOT,
                                    capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn('"active_writer": true', result.stdout)
        self.assertIn('"ok": false', result.stdout)
        self.assertNotIn("Traceback", result.stdout + result.stderr)

    def test_post_replace_check_failure_restores_old_database(self):
        queue.init(self.root)
        database = queue.database_path(self.root)
        old = database.read_bytes()
        original = queue._check_projection

        def fail_post_replace(*args, **kwargs):
            if kwargs.get("database") is None:
                raise wp1.ProductionReviewError("injected post-replace failure")
            return original(*args, **kwargs)

        with mock.patch.object(queue, "_check_projection", side_effect=fail_post_replace):
            with self.assertRaisesRegex(wp1.ProductionReviewError, "injected"):
                queue.rebuild(self.root)
        self.assertEqual(database.read_bytes(), old)
        self.assertEqual(list(database.parent.glob(".queue.sqlite3.rollback.*")), [])

    def test_check_rejects_orphan_override(self):
        queue.init(self.root)
        with closing(sqlite3.connect(queue.database_path(self.root))) as connection:
            connection.execute("INSERT INTO state_override VALUES (?,?,?,?,?,?,?)",
                               ("f" * 64, "e" * 64, "done", None, 0, None, STAMP))
            connection.commit()
        with self.assertRaises(wp1.ProductionReviewError):
            queue.check(self.root)

    def test_missing_real_catalog_is_controlled_cli_failure(self):
        command = [sys.executable, "-B", str(ROOT / "tools/i18n"),
                   "production", "queue", "status"]
        env = os.environ.copy()
        env["I18N_REPOSITORY_ROOT"] = str(self.root)
        queue.init(self.root)
        result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("Traceback", result.stdout + result.stderr)

        shutil.rmtree(self.root / catalog.CATALOG_PREFIX)
        self._commit("missing formal catalog")
        result = subprocess.run(command, cwd=ROOT, env=env, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertNotIn("Traceback", result.stdout + result.stderr)


class PublicApiFlowTests(QueueTests):
    def _host_block_input(self, checkpoint, *, revision=None, literal_source_match=False):
        revision = revision or checkpoint["selected"][0]
        relative = ".artifacts/i18n/host-block-attribution.json"
        attribution = {"schema": "freeze-miss-attribution/1", "attribution_done": True,
                       "miss_entry": {"entry_revision_identity": revision,
                                      "public_source_path": "game/source.lua",
                                      "literal_source_match": literal_source_match},
                       "bounded_diagnosis": {
                           "step2_is_the_literal_present_in_the_code_file": {"result": "NO"}},
                       "whole_code_scope_verification": {
                           "fixed_source_commit": "a" * 40,
                           "search_scope": "all_code_files",
                           "literal_source_present": False},
                       "attribution": "the frozen source literal is absent at the fixed commit"}
        path = self.root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(attribution, indent=2) + "\n", encoding="utf-8")
        request = {"batch_id": checkpoint["batch_id"],
                   "entry_revision_identity": revision,
                   "reason_code": catalog.HOST_BLOCK_REASON,
                   "fixed_source_commit": "a" * 40,
                   "public_source_path": "game/source.lua",
                   "attribution_evidence_path": relative}
        request_path = self.root / "host-block-input.json"
        request_path.write_bytes(wp1.canonical_bytes(request))
        return request_path

    def test_host_block_projection_and_git_replay_use_same_embedded_evidence(self):
        self._resize_and_init(1)
        batch.start(self.root, limit=1)
        checkpoint = batch.show(self.root)
        request = self._host_block_input(checkpoint)
        env = dict(os.environ, I18N_REPOSITORY_ROOT=str(self.root))
        recorded = subprocess.run(
            [sys.executable, "-B", str(ROOT / "tools/i18n"), "production", "batch",
             "host-block", "--input", str(request)],
            cwd=self.root, env=env, capture_output=True, text=True, timeout=20)
        self.assertEqual(recorded.returncode, 0, recorded.stderr)
        self.assertEqual(json.loads(recorded.stdout)["host_blocks"], 1)
        batch.surface_export(self.root)
        batch.surface_import(self.root, self._surface_outputs())
        empty = self.root / "empty-adjudication.json"
        empty.write_bytes(wp1.canonical_bytes({"batch_id": checkpoint["batch_id"], "decisions": []}))
        batch.adjudicate(self.root, empty)
        active = queue.status(self.root)
        self.assertEqual(active["explicit_overrides"], {"blocked": 1})
        prepared = batch.prepare_evidence(self.root)
        prospective = Path(prepared["prospective"])
        manifest = wp1.parse_canonical_object((prospective / "manifest.json").read_bytes(), "manifest")
        self.assertEqual(manifest["host_blocks_sha256"], hashlib.sha256(
            (prospective / "host_blocks.jsonl").read_bytes()).hexdigest())
        embedded = wp1.parse_jsonl((prospective / "host_blocks.jsonl").read_bytes(), "host blocks")
        self.assertFalse(embedded[0]["literal_source_match"])
        commit = self._publish_generated(prospective)
        batch.finalize(self.root, commit)
        replayed = queue.status(self.root)
        self.assertEqual(replayed["explicit_overrides"], active["explicit_overrides"])
        self.assertTrue(queue.check(self.root)["ok"])

    def test_host_block_record_requires_evidence_and_selected_revision(self):
        self._resize_and_init(1)
        batch.start(self.root, limit=1)
        checkpoint = batch.show(self.root)
        request = self._host_block_input(checkpoint, revision="f" * 64)
        with self.assertRaisesRegex(wp1.ProductionReviewError, "unselected"):
            batch.record_host_block(self.root, request)
        request = self._host_block_input(checkpoint)
        value = wp1.parse_canonical_object(request.read_bytes(), "request")
        value.pop("attribution_evidence_path")
        request.write_bytes(wp1.canonical_bytes(value))
        with self.assertRaisesRegex(wp1.ProductionReviewError, "canonical and bind"):
            batch.record_host_block(self.root, request)
        self.assertEqual(batch.show(self.root).get("host_blocks"), [])
        batch.abandon(self.root)

    def test_host_block_does_not_downgrade_surface_issue_repair_in_active_or_replay(self):
        self._resize_and_init(1)
        batch.start(self.root, limit=1)
        checkpoint = batch.show(self.root)
        batch.record_host_block(self.root, self._host_block_input(checkpoint))
        batch.surface_export(self.root)
        surface_ref = batch.show(self.root)["surface"][0]
        batch.surface_import(self.root, {"0": self._surface_bytes(surface_ref, "ISSUE")})
        batch.contextual_export(self.root)
        contextual_ref = batch.show(self.root)["contextual"][0]
        contextual_output = self._contextual_bytes(contextual_ref, "OK")
        self._install_contextual_done_state(contextual_ref, contextual_output)
        batch.contextual_import(self.root, {"0": contextual_output})
        observations = batch._accepted_observations(batch.show(self.root))
        self.assertEqual([item["contract"] for item in observations],
                         [wp1.surface.CONTRACT])
        source_snapshot = {"sha256": hashlib.sha256(b"host block repair source").hexdigest(),
                           "content": "host block repair source"}
        decisions = [self._decision(item, disposition="confirmed",
                                    snapshot=source_snapshot, repair_required=True)
                     for item in observations]
        adjudication = self.root / "host-block-repair-adjudication.json"
        adjudication.write_bytes(wp1.canonical_bytes({
            "batch_id": checkpoint["batch_id"], "decisions": decisions}))
        self.assertEqual(batch.adjudicate(self.root, adjudication)["repair_required"], 1)
        self.assertEqual(queue.status(self.root)["explicit_overrides"],
                         {"repair_required": 1})
        prepared = batch.prepare_evidence(self.root)
        publication = self._publish_generated(Path(prepared["prospective"]))
        batch.finalize(self.root, publication)
        queue.rebuild(self.root)
        self.assertEqual(queue.status(self.root)["explicit_overrides"],
                         {"repair_required": 1})

    def test_repair_preflight_accepts_host_blocks_and_selects_only_repair_winners(self):
        self._resize_and_init(2)
        batch.start(self.root, limit=2)
        checkpoint = batch.show(self.root)
        repair_revision, blocked_revision = checkpoint["selected"]
        batch.record_host_block(self.root, self._host_block_input(
            checkpoint, revision=blocked_revision))
        batch.surface_export(self.root)
        surface_ref = batch.show(self.root)["surface"][0]
        output = json.loads(self._surface_bytes(surface_ref))
        output["results"][0].update(verdict="ISSUE", observation="repair fixture")
        batch.surface_import(self.root, {"0": wp1.canonical_bytes(output)})
        batch.contextual_export(self.root)
        contextual_ref = batch.show(self.root)["contextual"][0]
        contextual_output = self._contextual_bytes(contextual_ref, "OK")
        self._install_contextual_done_state(contextual_ref, contextual_output)
        batch.contextual_import(self.root, {"0": contextual_output})
        observations = batch._accepted_observations(batch.show(self.root))
        snapshot = {"sha256": hashlib.sha256(b"repair source").hexdigest(),
                    "content": "repair source"}
        decisions = [self._decision(item, disposition="confirmed", snapshot=snapshot,
                                    repair_required=True) for item in observations]
        adjudication = self.root / "mixed-repair-adjudication.json"
        adjudication.write_bytes(wp1.canonical_bytes({
            "batch_id": checkpoint["batch_id"], "decisions": decisions}))
        batch.adjudicate(self.root, adjudication)
        prepared = batch.prepare_evidence(self.root)
        publication = self._publish_generated(Path(prepared["prospective"]))
        batch.finalize(self.root, publication)
        queue.rebuild(self.root)
        self.assertEqual(queue.status(self.root)["explicit_overrides"],
                         {"repair_required": 1, "blocked": 1})
        # The fixture lacks a real Lua/version manifest. Keep Git evidence,
        # manifest/hash validation and durable winner selection real.
        with mock.patch.object(migration, "_validate_live_repair_preimage"):
            report = migration.repair_preflight(self.root, checkpoint["batch_id"])
        workset = wp1.parse_canonical_object(Path(report["workset"]).read_bytes(), "workset")
        self.assertEqual([item["entry_revision_identity"] for item in workset["items"]],
                         [repair_revision])
        self.assertEqual(workset["evidence_commit"], publication)
        self.assertNotIn(blocked_revision, [item["entry_revision_identity"]
                                           for item in workset["items"]])

    def _surface_bytes(self, ref, verdict="OK"):
        raw = Path(ref["input_path"]).read_bytes()
        envelope = wp1.surface.strict_json_bytes(raw, label="surface envelope")
        payload, candidate = wp1.surface.validate_envelope(envelope)
        results = []
        for entry in payload["entries"]:
            item = {"entry_revision_identity": entry["entry_revision_identity"], "verdict": verdict}
            if verdict == "ISSUE":
                item["observation"] = "review issue"
            results.append(item)
        return wp1.surface.canonical_bytes({"contract": wp1.surface.CONTRACT,
            "candidate_identity": candidate, "results": results})

    def _contextual_bytes(self, ref, verdict="OK"):
        raw = Path(ref["input_path"]).read_bytes()
        envelope = contextual_result_check.strict_json_bytes(raw, label="contextual envelope")
        payload, candidate = contextual_result_check.validate_envelope(envelope)
        verdicts = []
        for position, revision in enumerate(payload["ordered_revision_keys"]):
            item_verdict = verdict if position == 0 else "OK"
            item = {"revision_key": revision, "verdict": item_verdict}
            if item_verdict == "ISSUE":
                item["observation"] = "contextual issue"
            verdicts.append(item)
        return wp1.canonical_bytes({"contract": "translation_contextual_v2",
            "candidate_identity": candidate, "verdicts": verdicts})

    def _decision(self, observation, *, disposition="advisory", path=None,
                  commit=None, snapshot=None, repair_required=False):
        return {"entry_revision_identity": observation["entry_revision_identity"],
                "observation_contract": observation["contract"],
                "observation_identity": observation["observation_identity"],
                "observation_sha256": hashlib.sha256(
                    (observation["observation"] or "").encode()).hexdigest(),
                "disposition": disposition, "evidence_path": path,
                "evidence_commit": commit, "evidence_snapshot": snapshot,
                "conclusion": "current producer fixture",
                "repair_required": repair_required}

    def _publish_generated(self, batch_root):
        destination = self.root / "evidence/production-review-v2-lite/batches" / batch_root.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        import shutil
        shutil.copytree(batch_root, destination)
        self._commit("publish generated evidence")
        return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.root, text=True).strip()

    def test_public_api_all_surface_ok_full_n_1_4_80_and_commit_same_tree(self):
        for count in (1, 4, 80):
            with self.subTest(count=count):
                self._resize_and_init(count)
                batch.start(self.root, limit=count)
                batch.surface_export(self.root)
                checkpoint = batch.show(self.root)
                outputs = {str(i): self._surface_bytes(ref) for i, ref in enumerate(checkpoint["surface"])}
                batch.surface_import(self.root, outputs)
                empty = self.root / "empty-adjudication.json"
                empty.write_bytes(wp1.canonical_bytes({"batch_id": checkpoint["batch_id"], "decisions": []}))
                batch.adjudicate(self.root, empty)
                self.gate_runner.reset_mock()
                prepared = batch.prepare_evidence(self.root)
                self.assertEqual(self.gate_runner.call_count, 1)
                receipt = json.loads((Path(prepared["prospective"]) / "gates.json").read_bytes())
                # New receipts name the policy they were measured under, so a
                # later ceiling change cannot widen this batch's acceptance.
                self.assertEqual(receipt["schema_version"], 3)
                self.assertEqual(receipt["capacity_policy_id"], capacity_policy.CURRENT_POLICY_ID)
                self.assertEqual(receipt["capacity_policy_sha256"],
                                 capacity_policy.digest(capacity_policy.CURRENT_POLICY_ID))
                self.assertEqual(receipt["result"]["binding"]["candidate"]["ordered_revisions"], checkpoint["selected"])
                if count == 80:
                    commit = self._publish_generated(Path(prepared["prospective"]))
                    batch.finalize(self.root, commit)
                else:
                    batch.abandon(self.root, discard_uncommitted_results=True, restore_evidence=True)
                self.assertFalse(queue.checkpoint_path(self.root).exists())
                if count == 80:
                    queue.rebuild(self.root)
                self.assertTrue(queue.check(self.root)["ok"])

    def _mixed_identity_entries(self):
        variants = []
        for digit, component, fixed, terminology in (
                ("0", "tome", "commit:" + "a" * 40, "b" * 64),
                ("1", "tome", "commit:" + "a" * 40, "b" * 64),
                ("2", "boot", "commit:" + "d" * 40, "b" * 64),
                ("3", "boot", "commit:" + "d" * 40, "b" * 64)):
            entry = self._entry(digit)
            entry["component"] = component
            entry["fixed_source_identity"] = fixed
            entry["terminology_snapshot_sha256"] = terminology
            core = {"component": component, "duplicate_index": 0, "function_name": "t",
                    "normalized_source_tag": "", "section": "fixture", "source": entry["source"],
                    "translation_path": "tome.lua"}
            entry["call_locator"] = catalog._plain_id(catalog.CALL_LOCATOR_KIND, "locator", core)
            entry["logical_entry_identity"] = wp1.surface.logical_entry_identity(
                component=component, normalized_path="tome.lua", call_locator=entry["call_locator"], source_tag="")
            entry["entry_revision_identity"] = wp1.surface.entry_revision_identity(
                logical_entry_identity=entry["logical_entry_identity"], source=entry["source"], target=entry["target"],
                fixed_source_identity=fixed, terminology_snapshot=terminology, rules_version=catalog.RULES_VERSION,
                args_order=entry["risk"].get("args_order"))
            variants.append(entry)
        return variants

    def test_public_api_contextual_e2e_mixed_identity_commit_rebuild_revert(self):
        self._resize_and_init(1)
        self.entries = self._mixed_identity_entries()
        self._write_catalog()
        self._rewrite_catalog(self.entries)
        self._commit("mixed identity catalog")
        (self.root / "src.lua").write_text("-- verified public source fixture\\n", encoding="utf-8")
        source_commit = self._commit("public source fixture")
        queue.rebuild(self.root)

        started = batch.start(self.root, limit=4)
        self.assertEqual(started["selected"], 4)
        batch.surface_export(self.root)
        checkpoint = batch.show(self.root)
        surface_runs = batch.partition_surface_entries(checkpoint["entry_snapshots"])
        self.assertEqual([min(run["parent_indexes"]) for run in surface_runs], [0, 2])
        self.assertEqual(len({run["identity"] for run in surface_runs}), 2)
        surface_outputs = {str(i): self._surface_bytes(ref, "ISSUE")
                           for i, ref in enumerate(checkpoint["surface"])}
        batch.surface_import(self.root, surface_outputs)

        exported = batch.contextual_export(self.root)
        self.assertEqual(exported["runs"], 2)
        checkpoint = batch.show(self.root)
        runs = batch.partition_contextual_entries(checkpoint)
        self.assertEqual([min(run["parent_indexes"]) for run in runs], [0, 2])
        self.assertEqual(len({run["identity"] for run in runs}), 2)
        deep_indexes = sorted(i for run in runs for i in run["parent_indexes"])
        self.assertEqual(deep_indexes, [0, 1, 2, 3])
        self.assertEqual(sum(len(run["parent_indexes"]) for run in runs), len(set(deep_indexes)))
        for run in runs:
            self.assertEqual(len({(row["fixed_source_identity"], row["terminology_snapshot_sha256"],
                                   row["rules_version"]) for row in run["entries"]}), 1)

        contextual_outputs = {str(i): self._contextual_bytes(ref, "ISSUE")
                              for i, ref in enumerate(checkpoint["contextual"])}
        for ref, raw in zip(checkpoint["contextual"], contextual_outputs.values()):
            self._install_contextual_done_state(ref, raw)
        import_report = batch.contextual_import(self.root, contextual_outputs)
        self.assertEqual(import_report["imported"], 4)
        checkpoint = batch.show(self.root)
        for ref in checkpoint["contextual"]:
            accepted = contextual_result_check.validate_result_bytes(
                Path(ref["input_path"]).read_bytes(), Path(ref["output_path"]).read_bytes())
            expected = [checkpoint["entry_snapshots"][i]["entry_revision_identity"]
                        for i in ref["parent_indexes"]]
            self.assertEqual([item["revision_key"] for item in accepted["verdicts"]], expected)

        decisions = [self._decision(item, disposition="advisory")
                     for item in batch._accepted_observations(batch.show(self.root))]
        adjudication = self.root / "adjudication.json"
        adjudication.write_bytes(wp1.canonical_bytes({"batch_id": checkpoint["batch_id"], "decisions": decisions}))
        self.assertEqual(batch.adjudicate(self.root, adjudication)["adjudicated"], 4)
        prepared = batch.prepare_evidence(self.root)
        prospective = Path(prepared["prospective"])
        raw_files = sorted(p for p in prospective.rglob("*") if p.is_file())
        self.assertEqual(len(raw_files), 4 + 2 * len(checkpoint["surface"] + checkpoint["contextual"]))
        destination = self.root / "evidence/production-review-v2-lite/batches" / prospective.name
        import shutil
        shutil.copytree(prospective, destination)
        subprocess.run(["git", "add", str(destination.relative_to(self.root))], cwd=self.root, check=True)
        subprocess.run(["git", "commit", "-qm", "publish mixed identity review evidence"],
                       cwd=self.root, check=True)
        publication = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.root, text=True).strip()
        changed = subprocess.check_output(["git", "diff-tree", "--no-commit-id", "--name-only", "-r", publication],
                                          cwd=self.root, text=True).splitlines()
        self.assertEqual(len(changed), len(raw_files))
        self.assertTrue(all(path.startswith("evidence/production-review-v2-lite/batches/") for path in changed))
        self.assertEqual(batch.finalize(self.root, publication)["commit"], publication)
        self.assertFalse(queue.checkpoint_path(self.root).exists())
        overrides, _reconciliation, _meta = queue.business_rows(queue.database_path(self.root))
        self.assertEqual({row[2] for row in overrides}, {"done"})

        database = queue.database_path(self.root)
        database.unlink()
        Path(str(database) + "-wal").unlink(missing_ok=True)
        Path(str(database) + "-shm").unlink(missing_ok=True)
        queue.rebuild(self.root)
        overrides, _reconciliation, _meta = queue.business_rows(database)
        self.assertEqual({row[2] for row in overrides}, {"done"})
        subprocess.run(["git", "revert", "--no-edit", publication], cwd=self.root, check=True,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        queue.rebuild(self.root)
        overrides, _reconciliation, _meta = queue.business_rows(database)
        self.assertEqual(overrides, [])
        self.assertTrue(queue.check(self.root)["ok"])

    def test_public_api_contextual_review_only_mixed_identities_and_unique_outcomes(self):
        self._resize_and_init(4)
        (self.root / "src.lua").write_text("-- public source fixture\n", encoding="utf-8")
        self._commit("public source fixture")
        queue.rebuild(self.root)
        batch.start(self.root, limit=4)
        batch.surface_export(self.root)
        checkpoint = batch.show(self.root)
        surface_outputs = {str(i): self._surface_bytes(ref, "ISSUE") for i, ref in enumerate(checkpoint["surface"])}
        batch.surface_import(self.root, surface_outputs)
        exported = batch.contextual_export(self.root)
        self.assertEqual(exported["runs"], 1)
        checkpoint = batch.show(self.root)
        # The real checker is exercised for rejection; acceptance is explicitly
        # supplied only after that fail-closed result, using the public API.
        bad = self.root / "bad-state.json"
        bad.write_text("{}", encoding="utf-8")
        sys.path.insert(0, str(ROOT / "tools"))
        import ai_state_check
        self.assertNotEqual(ai_state_check.check_state(bad, target="DONE", workspace_root=self.root).outcome,
                            "DONE_VERIFIED")
        contextual_outputs = {str(i): self._contextual_bytes(ref, "ISSUE") for i, ref in enumerate(checkpoint["contextual"])}
        for ref, raw in zip(batch.show(self.root)["contextual"], contextual_outputs.values()):
            self._install_contextual_done_state(ref, raw)
        batch.contextual_import(self.root, contextual_outputs)
        input_path = self.root / "adjudication.json"
        issues = [self._decision(item, disposition="advisory")
            for item in batch._accepted_observations(batch.show(self.root))]
        input_path.write_bytes(wp1.canonical_bytes({"batch_id": batch.show(self.root)["batch_id"], "decisions": issues}))
        report = batch.adjudicate(self.root, input_path)
        self.assertEqual(report["adjudicated"], len(set(item["entry_revision_identity"] for item in issues)))
        self.assertEqual(len(set(item["entry_revision_identity"] for item in issues)), 4)

    def test_public_api_contextual_n_1_and_80_real_done_verified(self):
        for count in (1, 80):
            with self.subTest(count=count):
                self._resize_and_init(count)
                batch.start(self.root, limit=count)
                batch.surface_export(self.root)
                checkpoint = batch.show(self.root)
                surface_outputs = {str(i): self._surface_bytes(ref, "ISSUE")
                                   for i, ref in enumerate(checkpoint["surface"])}
                batch.surface_import(self.root, surface_outputs)
                exported = batch.contextual_export(self.root)
                checkpoint = batch.show(self.root)
                contextual_outputs = {str(i): self._contextual_bytes(ref, "ISSUE")
                                      for i, ref in enumerate(checkpoint["contextual"])}
                for ref, raw in zip(checkpoint["contextual"], contextual_outputs.values()):
                    self._install_contextual_done_state(ref, raw)
                batch.contextual_import(self.root, contextual_outputs)
                accepted = contextual_result_check.validate_result_bytes(
                    Path(checkpoint["contextual"][0]["input_path"]).read_bytes(),
                    contextual_outputs["0"])
                issue = next(item for item in accepted["verdicts"] if item["verdict"] == "ISSUE")
                adjudication = self.root / "adjudication.json"
                decisions = [self._decision(item, disposition="advisory")
                             for item in batch._accepted_observations(batch.show(self.root))]
                adjudication.write_bytes(wp1.canonical_bytes({"batch_id": checkpoint["batch_id"], "decisions": decisions}))
                report = batch.adjudicate(self.root, adjudication)
                self.assertEqual(report["adjudicated"], len(set(item["entry_revision_identity"] for item in decisions)))
                batch.abandon(self.root, discard_uncommitted_results=True)
                self.assertFalse(queue.checkpoint_path(self.root).exists())

    def test_public_api_checkpoint_first_recovery_delete_rebuild_revert_and_forged_adjudication(self):
        self._resize_and_init(1)
        batch.start(self.root, limit=1)
        batch.surface_export(self.root)
        checkpoint = queue.checkpoint_path(self.root)
        database = queue.database_path(self.root)
        database.unlink()
        batch.recover(self.root)
        self.assertTrue(database.exists())
        batch.surface_import(self.root, {"0": self._surface_bytes(batch.show(self.root)["surface"][0])})
        empty = self.root / "empty.json"
        empty.write_bytes(wp1.canonical_bytes({"batch_id": batch.show(self.root)["batch_id"], "decisions": []}))
        batch.adjudicate(self.root, empty)
        batch.prepare_evidence(self.root)
        value = batch.show(self.root)
        forged = self.root / "forged.json"
        forged.write_bytes(wp1.canonical_bytes({"batch_id": value["batch_id"], "decisions": [{"bad": True}]}))
        with self.assertRaises(wp1.ProductionReviewError):
            batch.adjudicate(self.root, forged)
        self.assertTrue(checkpoint.exists())
        batch.abandon(self.root, discard_uncommitted_results=True, restore_evidence=True)
        self.assertFalse(checkpoint.exists())
        queue.rebuild(self.root)
        self.assertTrue(queue.check(self.root)["ok"])


    def _prepare_for_count(self, count):
        self._resize_and_init(count)
        batch.start(self.root, limit=count)
        batch.surface_export(self.root)
        checkpoint = batch.show(self.root)
        outputs = {str(i): self._surface_bytes(ref) for i, ref in enumerate(checkpoint["surface"])}
        batch.surface_import(self.root, outputs)
        empty = self.root / "empty-adjudication.json"
        empty.write_bytes(wp1.canonical_bytes({"batch_id": checkpoint["batch_id"], "decisions": []}))
        batch.adjudicate(self.root, empty)
        self.gate_runner.reset_mock()
        return batch.prepare_evidence(self.root)

    def test_group_manifest_is_copied_once_per_distinct_content(self):
        """Four lanes cite one group manifest, so one file is written, not four."""
        prepared = self._prepare_for_count(4)
        prospective = Path(prepared["prospective"])
        groups = sorted(p.name for p in (prospective / "raw" / "surface").glob("group-*.json"))
        self.assertEqual(len(groups), 1, groups)
        # The old per-section copies must be gone entirely, not merely unused.
        self.assertEqual(sorted(p.name for p in prospective.rglob("*-group.json")), [])
        manifest = wp1.parse_canonical_object(
            (prospective / "manifest.json").read_bytes(), "manifest")
        bound = {(ref["group_manifest_path"], ref["group_manifest_sha256"])
                 for ref in manifest["adapter_refs"] if "group_manifest_path" in ref}
        self.assertEqual(len(bound), 1, bound)
        group_path, group_hash = next(iter(bound))
        self.assertTrue(group_path.endswith(f"/raw/surface/group-{group_hash}.json"), group_path)
        self.assertEqual(
            hashlib.sha256((prospective / "raw" / "surface" / f"group-{group_hash}.json"
                            ).read_bytes()).hexdigest(), group_hash)
        # Lane inputs and outputs are NOT shared: still one file per section.
        self.assertEqual(len(list((prospective / "raw" / "surface").glob("*-input_path.json"))), 4)
        self.assertEqual(len(list((prospective / "raw" / "surface").glob("*-output_path.json"))), 4)

    def test_full_mode_has_no_group_file_at_all(self):
        prospective = Path(self._prepare_for_count(1)["prospective"])
        self.assertEqual(sorted(p.name for p in prospective.rglob("group-*.json")), [])
        manifest = wp1.parse_canonical_object(
            (prospective / "manifest.json").read_bytes(), "manifest")
        self.assertTrue(all("group_manifest_path" not in ref
                            for ref in manifest["adapter_refs"]))

    def test_copy_plan_is_one_walk_and_reports_group_conflicts(self):
        """The declared inventory and the copy tasks come from the same walk."""
        self._prepare_for_count(4)
        checkpoint = batch._load(queue.checkpoint_path(self.root))
        plan = batch._raw_copy_plan(checkpoint)
        planned = {batch._batch_relative(checkpoint["batch_id"], *parts) for parts in plan["copies"]}
        core = {batch._batch_relative(checkpoint["batch_id"], name)
                for name in batch.evidence.CORE_FILES}
        self.assertEqual(plan["declared"], planned | core)
        self.assertEqual(batch._prospective_declared_paths(checkpoint), plan["declared"])

        # One source path carrying two different recorded hashes is a conflict,
        # not something to resolve by picking one.
        conflicted = copy.deepcopy(checkpoint)
        conflicted["surface"][1]["group_manifest_sha256"] = "b" * 64
        with self.assertRaisesRegex(wp1.ProductionReviewError,
                                    "one source path carries two different hashes"):
            batch._raw_copy_plan(conflicted)

        # A reference with no usable hash cannot be content-addressed at all.
        missing = copy.deepcopy(checkpoint)
        missing["surface"][0]["group_manifest_sha256"] = None
        with self.assertRaisesRegex(wp1.ProductionReviewError, "lacks a recorded SHA-256"):
            batch._raw_copy_plan(missing)

    def test_group_bytes_changing_after_import_fail_closed(self):
        """Group bytes that drift after import stop the prepare, at some layer.

        The existing surface projection check catches this first; the copy-time
        hash check added with the dedup plan is a backstop for the case where
        the bytes change between that check and the copy itself.
        """
        self._resize_and_init(4)
        batch.start(self.root, limit=4)
        batch.surface_export(self.root)
        checkpoint = batch.show(self.root)
        outputs = {str(i): self._surface_bytes(ref) for i, ref in enumerate(checkpoint["surface"])}
        batch.surface_import(self.root, outputs)
        empty = self.root / "empty-adjudication.json"
        empty.write_bytes(wp1.canonical_bytes({"batch_id": checkpoint["batch_id"], "decisions": []}))
        batch.adjudicate(self.root, empty)
        source = Path(batch.show(self.root)["surface"][0]["group_manifest_path"])
        source.write_bytes(source.read_bytes() + b" ")
        self.gate_runner.reset_mock()
        with self.assertRaisesRegex(wp1.ProductionReviewError, "group manifest hash drift"):
            batch.prepare_evidence(self.root)

    def _publish_mutated(self, prospective, mutate):
        """Commit a batch whose receipt was rewritten after the batch was closed.

        The batch is abandoned before the rewrite lands, so the rewritten
        receipt is only ever read the way a historical one is: by replaying
        committed evidence, with no active checkpoint in the picture.
        """
        staging = Path(tempfile.mkdtemp()) / prospective.name
        shutil.copytree(prospective, staging)
        batch.abandon(self.root, discard_uncommitted_results=True, restore_evidence=True)
        destination = self.root / "evidence/production-review-v2-lite/batches" / prospective.name
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(staging, destination)
        gates = wp1.parse_canonical_object((destination / "gates.json").read_bytes(), "gates")
        mutate(gates)
        gates_raw = wp1.canonical_bytes(gates)
        (destination / "gates.json").write_bytes(gates_raw)
        manifest = wp1.parse_canonical_object(
            (destination / "manifest.json").read_bytes(), "manifest")
        manifest["gates_sha256"] = hashlib.sha256(gates_raw).hexdigest()
        (destination / "manifest.json").write_bytes(wp1.canonical_bytes(manifest))
        self._commit("publish evidence with a rewritten receipt")

    def test_historical_receipts_keep_the_legacy_ceiling(self):
        """Raising the current ceiling must not widen an old receipt's domain."""
        between = capacity_policy.LEGACY_TRACKED_LIMIT + 1
        self.assertLess(between, capacity_policy.CURRENT_TRACKED_LIMIT)
        def rewrite(schema):
            def mutate(gates):
                gates["schema_version"] = schema
                gates["prospective_bytes"] = gates["committed_bytes"] = between
                if schema == 2:
                    gates.pop("capacity_policy_id")
                    gates.pop("capacity_policy_sha256")
            return mutate

        # A schema 2 receipt predates the policy binding, so it is read under
        # 128 MiB even though the current ceiling is 512 MiB.
        self._publish_mutated(Path(self._prepare_for_count(1)["prospective"]), rewrite(2))
        with self.assertRaisesRegex(wp1.ProductionReviewError, "exceed the combined 128 MiB"):
            queue.rebuild(self.root)
        subprocess.run(["git", "revert", "--no-edit", "HEAD"], cwd=self.root,
                       check=True, stdout=subprocess.DEVNULL)
        # The same byte count under a schema 3 receipt naming the current
        # policy is inside budget.  The only difference is the binding.
        # A different entry count keeps this a distinct catalog and batch.
        self._publish_mutated(Path(self._prepare_for_count(2)["prospective"]), rewrite(3))
        queue.rebuild(self.root)

    def test_gates_v3_rejects_an_unknown_or_mismatched_policy(self):
        def wrong_digest(gates):
            gates["capacity_policy_sha256"] = capacity_policy.digest(
                capacity_policy.LEGACY_POLICY_ID)

        self._publish_mutated(Path(self._prepare_for_count(1)["prospective"]), wrong_digest)
        with self.assertRaisesRegex(wp1.ProductionReviewError, "capacity policy invalid"):
            queue.rebuild(self.root)


    def test_gates_ceiling_is_exact_on_both_sides_of_each_policy(self):
        """limit / limit+1 for the receipt reader, under both policies."""
        cases = [(2, capacity_policy.LEGACY_TRACKED_LIMIT, "accept"),
                 (2, capacity_policy.LEGACY_TRACKED_LIMIT + 1, "reject"),
                 (3, capacity_policy.CURRENT_TRACKED_LIMIT, "accept"),
                 (3, capacity_policy.CURRENT_TRACKED_LIMIT + 1, "reject")]
        for index, (schema, value, expectation) in enumerate(cases):
            with self.subTest(schema=schema, value=value):
                def mutate(gates, schema=schema, value=value):
                    gates["schema_version"] = schema
                    gates["prospective_bytes"] = gates["committed_bytes"] = value
                    if schema == 2:
                        gates.pop("capacity_policy_id", None)
                        gates.pop("capacity_policy_sha256", None)

                self._publish_mutated(
                    Path(self._prepare_for_count(index + 1)["prospective"]), mutate)
                if expectation == "reject":
                    with self.assertRaisesRegex(wp1.ProductionReviewError,
                                                "exceed the combined"):
                        queue.rebuild(self.root)
                else:
                    queue.rebuild(self.root)
                subprocess.run(["git", "revert", "--no-edit", "HEAD"], cwd=self.root,
                               check=True, stdout=subprocess.DEVNULL)

    def test_committed_production_bytes_is_exact_at_the_ceiling(self):
        prospective = Path(self._prepare_for_count(1)["prospective"])
        commit = self._publish_generated(prospective)
        batch.finalize(self.root, commit)
        total = batch._committed_production_bytes(self.root, commit)
        for ceiling, expectation in ((total - 1, "reject"), (total, "accept"),
                                     (total + 1, "accept")):
            with self.subTest(ceiling=ceiling):
                with mock.patch.object(catalog, "TRACKED_LIMIT", ceiling):
                    if expectation == "reject":
                        with self.assertRaisesRegex(wp1.ProductionReviewError,
                                                    "committed production evidence exceeds"):
                            batch._committed_production_bytes(self.root, commit)
                    else:
                        self.assertEqual(
                            batch._committed_production_bytes(self.root, commit), total)

    def _interrupted_prepare(self, count=4):
        """Return a prepared batch rewound to the phase prepare resumes from."""
        prepared = self._prepare_for_count(count)
        prospective = Path(prepared["prospective"])
        checkpoint = batch._load(queue.checkpoint_path(self.root))
        checkpoint["phase"] = "adjudicated"
        checkpoint["last_safe_boundary"] = "before_commit"
        return prospective, checkpoint

    def test_prepare_resumes_from_a_half_written_deduped_tree(self):
        prospective, checkpoint = self._interrupted_prepare()
        declared = batch._prospective_declared_paths(checkpoint)
        checkpoint["gates"] = {"commands": [], "prospective": {path: None for path in sorted(declared)},
                               "preimage_absent": sorted(declared),
                               "prospective_bytes": 0, "committed_bytes": 0}
        batch._atomic(queue.checkpoint_path(self.root), batch._checkpoint_bytes(checkpoint))
        for path in sorted((prospective / "raw" / "surface").glob("*"))[:2]:
            path.unlink()
        self.gate_runner.reset_mock()
        batch.prepare_evidence(self.root)
        groups = sorted(p.name for p in (prospective / "raw" / "surface").glob("group-*.json"))
        self.assertEqual(len(groups), 1, groups)

    def test_prepare_resumes_from_complete_registered_postimages(self):
        prospective, checkpoint = self._interrupted_prepare()
        self.assertTrue(all(value is not None
                            for value in checkpoint["gates"]["prospective"].values()))
        batch._atomic(queue.checkpoint_path(self.root), batch._checkpoint_bytes(checkpoint))
        self.gate_runner.reset_mock()
        batch.prepare_evidence(self.root)
        groups = sorted(p.name for p in (prospective / "raw" / "surface").glob("group-*.json"))
        self.assertEqual(len(groups), 1, groups)

    def test_a_stale_old_layout_file_is_rejected_not_adopted(self):
        """Resume never infers the layout from whatever happens to be on disk."""
        prospective, checkpoint = self._interrupted_prepare()
        batch._atomic(queue.checkpoint_path(self.root), batch._checkpoint_bytes(checkpoint))
        stale = prospective / "raw" / "surface" / "000-group.json"
        stale.write_bytes(b"{}\n")
        self.gate_runner.reset_mock()
        with self.assertRaisesRegex(wp1.ProductionReviewError,
                                    "prospective evidence contains undeclared paths"):
            batch.prepare_evidence(self.root)

    def test_abandon_accepts_the_deduped_prospective_tree(self):
        prospective = Path(self._prepare_for_count(4)["prospective"])
        self.assertEqual(
            len(list((prospective / "raw" / "surface").glob("group-*.json"))), 1)
        batch.abandon(self.root, discard_uncommitted_results=True, restore_evidence=True)
        self.assertFalse(prospective.exists())
        self.assertFalse(queue.checkpoint_path(self.root).exists())


    def test_two_distinct_group_contents_stay_two_files(self):
        """Dedup is by content: same bytes collapse, different bytes do not.

        The fixture only ever builds one run, so the second run is synthesised
        on the checkpoint.  The rule under test is the plan's, not the flow's.
        """
        self._prepare_for_count(4)
        checkpoint = batch._load(queue.checkpoint_path(self.root))
        second = copy.deepcopy(checkpoint["surface"])
        other_hash = hashlib.sha256(b"a second run's group manifest").hexdigest()
        for lane in second:
            lane["run_index"] = checkpoint["surface"][0]["run_index"] + 1
            lane["group_manifest_path"] = lane["group_manifest_path"] + ".second"
            lane["group_manifest_sha256"] = other_hash
        two_runs = copy.deepcopy(checkpoint)
        two_runs["surface"] = checkpoint["surface"] + second
        plan = batch._raw_copy_plan(two_runs)
        groups = sorted(parts[2] for parts in plan["copies"] if parts[2].startswith("group-"))
        self.assertEqual(len(groups), 2, groups)
        self.assertIn(f"group-{other_hash}.json", groups)
        # Eight lanes, two group files: four-to-one on each side.
        self.assertEqual(len([item for item in plan["sections"] if item["group"] is not None]), 8)
        self.assertEqual(len({item["group"] for item in plan["sections"]
                              if item["group"] is not None}), 2)
        # Every group file on disk is named after exactly its own bytes.
        prospective = Path(batch._prospective_batch_path(self.root, checkpoint["batch_id"]))
        for name in sorted(p.name for p in (prospective / "raw" / "surface").glob("group-*.json")):
            digest = name[len("group-"):-len(".json")]
            self.assertEqual(hashlib.sha256(
                (prospective / "raw" / "surface" / name).read_bytes()).hexdigest(), digest)

    def test_a_gap_in_section_numbers_does_not_shift_any_name(self):
        """Sections without an output are skipped; the rest keep their own index."""
        self._prepare_for_count(4)
        checkpoint = batch._load(queue.checkpoint_path(self.root))
        full = batch._raw_copy_plan(checkpoint)
        holed = copy.deepcopy(checkpoint)
        holed["surface"][1]["output_path"] = None
        plan = batch._raw_copy_plan(holed)
        self.assertEqual([item["number"] for item in plan["sections"]], [0, 2, 3])
        # The surviving sections keep the exact names they had before the gap.
        for item in plan["sections"]:
            for key in ("input_path", "output_path"):
                name = batch._raw_evidence_name(item["number"], key)
                self.assertIn(("raw", item["kind"], name), full["copies"])
                self.assertIn(("raw", item["kind"], name), plan["copies"])
        # The skipped section's own files are gone, and nothing inherited them.
        for key in ("input_path", "output_path"):
            self.assertNotIn(("raw", "surface", batch._raw_evidence_name(1, key)),
                             plan["copies"])
        # One group manifest is still shared by the three surviving lanes.
        self.assertEqual(len([parts for parts in plan["copies"]
                              if parts[2].startswith("group-")]), 1)


class C31PublicApiTests(PublicApiFlowTests):
    def _contextual_issue_ready(self, count=1, *, surface_verdict="ISSUE", source_before=False):
        self._resize_and_init(count)
        if source_before:
            (self.root / "source.lua").write_text("-- C31 public source\n", encoding="utf-8")
            self._commit("C31 source")
            queue.rebuild(self.root)
        batch.start(self.root, limit=count)
        batch.surface_export(self.root)
        batch.surface_import(self.root, {str(i): self._surface_bytes(ref, surface_verdict)
                                         for i, ref in enumerate(batch.show(self.root)["surface"])})
        batch.contextual_export(self.root)
        ref = batch.show(self.root)["contextual"][0]
        output = self._contextual_bytes(ref, "ISSUE")
        return ref, output

    def _install_and_import_contextual(self, ref, output):
        self._install_contextual_done_state(ref, output)
        return batch.contextual_import(self.root, {"0": output})

    def _legacy_decision(self, observation, *, disposition="advisory", path=None,
                         commit=None, snapshot=None, repair_required=False):
        # Keep the historical helper name for older test call sites while
        # emitting the current producer's exact contract binding.  A textual
        # legacy snapshot is upgraded to the exact named Git blob.
        if commit is not None and path is not None and snapshot is not None:
            commit_id = commit[7:] if commit.startswith("commit:") else commit
            raw = subprocess.check_output(
                ["git", "cat-file", "blob", f"{commit_id}:{path}"],
                cwd=self.root)
            snapshot = {"sha256": hashlib.sha256(raw).hexdigest(),
                        "content_base64": __import__("base64").b64encode(raw).decode("ascii")}
        return self._decision(observation, disposition=disposition, path=path,
                              commit=commit, snapshot=snapshot,
                              repair_required=repair_required)

    def _decision(self, observation, *, disposition="advisory", path=None,
                  commit=None, snapshot=None, repair_required=False):
        return {"entry_revision_identity": observation["entry_revision_identity"],
                "observation_contract": observation["contract"],
                "observation_identity": observation["observation_identity"],
                "observation_sha256": hashlib.sha256(
                    (observation["observation"] or "").encode()).hexdigest(),
                "disposition": disposition, "evidence_path": path,
                "evidence_commit": commit, "evidence_snapshot": snapshot,
                "conclusion": "C31 fixture", "repair_required": repair_required}

    def test_c31_contextual_full_n4_publish(self):
        ref, output = self._contextual_issue_ready(4, source_before=True)
        # A full run must be bound to the exact producer output, not merely to
        # a validator-accepted result.  The predecessor accepts this forged
        # but contract-valid alternate verdict.
        self._install_contextual_done_state(ref, output)
        with self.assertRaisesRegex(wp1.ProductionReviewError, "DONE_VERIFIED"):
            batch.contextual_import(self.root, {"0": self._contextual_bytes(ref, "OK")})
        self._install_and_import_contextual(ref, output)
        observations = batch._accepted_observations(batch.show(self.root))
        self.assertEqual(len(observations), 5)  # four surface + one contextual ISSUE
        source_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.root, text=True).strip()
        decisions = []
        for item in observations:
            if item["contract"] == "translation_contextual_v2":
                decisions.append(self._legacy_decision(
                    item, disposition="confirmed", path="source.lua",
                    commit="commit:" + source_commit, snapshot="source"))
            else:
                decisions.append(self._legacy_decision(item, disposition="advisory"))
        adjudication = self.root / "adjudication.json"
        adjudication.write_bytes(wp1.canonical_bytes({"batch_id": batch.show(self.root)["batch_id"],
                                                       "decisions": decisions}))
        self.assertEqual(batch.adjudicate(self.root, adjudication)["adjudicated"], 4)
        prepared = batch.prepare_evidence(self.root)
        published = self._publish_generated(Path(prepared["prospective"]))
        self.assertEqual(batch.finalize(self.root, published)["commit"], published)
        self.assertFalse(queue.checkpoint_path(self.root).exists())
        self.assertTrue(queue.check(self.root)["ok"])

    def test_c31_fresh_contextual_import_without_done_verified_fails(self):
        ref, output = self._contextual_issue_ready()
        with self.assertRaisesRegex(wp1.ProductionReviewError, "DONE_VERIFIED"):
            batch.contextual_import(self.root, {"0": output})
        self.assertIsNone(batch.show(self.root)["contextual"][0]["output_path"])
        batch.abandon(self.root, discard_uncommitted_results=True)

    def test_c31_unrelated_task_candidate_input_and_output_done_fail(self):
        cases = ("task", "candidate", "input", "output")
        for kind in cases:
            with self.subTest(kind=kind):
                shutil.rmtree(self.root / ".ai", ignore_errors=True)
                ref, output = self._contextual_issue_ready(1 if kind in {"task", "input"} else 2)
                self._install_contextual_done_state(ref, output)
                checkpoint = batch._load(queue.checkpoint_path(self.root))
                if kind == "task":
                    checkpoint["contextual"][0]["task_id"] = "unrelated-task"
                elif kind == "candidate":
                    checkpoint["contextual"][0]["candidate_identity"] = "0" * 64
                elif kind == "input":
                    Path(ref["input_path"]).write_bytes(Path(ref["input_path"]).read_bytes() + b" ")
                else:
                    output = output[:-1] + b" "
                if kind in {"task", "candidate"}:
                    batch._atomic(queue.checkpoint_path(self.root), batch._checkpoint_bytes(checkpoint))
                with self.assertRaises(wp1.ProductionReviewError):
                    batch.contextual_import(self.root, {"0": output})
                shutil.rmtree(self.root / ".ai", ignore_errors=True)

    def test_c31_two_observations_same_revision_keep_two_adjudications_and_fold_state(self):
        ref, output = self._contextual_issue_ready()
        self._install_and_import_contextual(ref, output)
        observations = batch._accepted_observations(batch.show(self.root))
        same_revision = [item for item in observations
                         if item["entry_revision_identity"] == observations[0]["entry_revision_identity"]]
        self.assertEqual(len(same_revision), 2)
        adjudication = self.root / "adjudication.json"
        evidence = {"sha256": hashlib.sha256(b"C31 source snapshot").hexdigest(),
                    "content": "C31 source snapshot"}
        decisions = [self._decision(item, disposition=("confirmed" if index == 0 else "advisory"),
                                     snapshot=(evidence if index == 0 else None),
                                     repair_required=(index == 0))
                     for index, item in enumerate(same_revision)]
        adjudication.write_bytes(wp1.canonical_bytes({
            "batch_id": batch.show(self.root)["batch_id"], "decisions": decisions}))
        self.assertEqual(batch.adjudicate(self.root, adjudication)["repair_required"], 1)
        checkpoint = batch.show(self.root)
        self.assertEqual(len(checkpoint["adjudications"]), 2)
        self.assertEqual(queue.status(self.root)["explicit_overrides"], {"repair_required": 1})

    def test_c31_free_form_snapshot_and_absolute_path_are_rejected(self):
        for forged in ((None, None, "not-a-snapshot"), ("/tmp/forged.lua", None, None)):
            with self.subTest(forged=forged):
                ref, output = self._contextual_issue_ready()
                self._install_and_import_contextual(ref, output)
                observations = batch._accepted_observations(batch.show(self.root))
                path, commit, snapshot = forged
                decisions = [self._legacy_decision(item) for item in observations]
                decisions[0] = self._legacy_decision(observations[0], disposition="confirmed", path=path,
                                                     commit=commit, snapshot=snapshot)
                input_path = self.root / "adjudication.json"
                input_path.write_bytes(wp1.canonical_bytes({"batch_id": batch.show(self.root)["batch_id"],
                                                            "decisions": decisions}))
                with self.assertRaises(wp1.ProductionReviewError):
                    batch.adjudicate(self.root, input_path)
                batch.abandon(self.root, discard_uncommitted_results=True)
        # A normalized path is part of the current source-evidence contract.
        # The predecessor's existence-only check accepts this equivalent path.
        ref, output = self._contextual_issue_ready(1, source_before=True)
        self._install_and_import_contextual(ref, output)
        source_commit = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.root, text=True).strip()
        tree = subprocess.check_output(["git", "rev-parse", f"{source_commit}^{{tree}}"], cwd=self.root, text=True).strip()
        observations = batch._accepted_observations(batch.show(self.root))
        decisions = [self._decision(item, disposition="confirmed", path="source.lua",
                                     commit="commit:" + tree, snapshot=None)
                     for item in observations]
        input_path = self.root / "adjudication.json"
        input_path.write_bytes(wp1.canonical_bytes({"batch_id": batch.show(self.root)["batch_id"],
                                                    "decisions": decisions}))
        with self.assertRaisesRegex(wp1.ProductionReviewError, "public-source path"):
            batch.adjudicate(self.root, input_path)
        batch.abandon(self.root, discard_uncommitted_results=True)

    def test_p2_initial_gate_binding_wraps_git_failure(self):
        selected = gate_results.candidate("batch-fixture", "catalog-fixture",
                                           queue._head(self.root, "HEAD"), "a" * 64, ["b" * 64])
        result = self.gate_runner(self.root, selected)
        failure = subprocess.CalledProcessError(128, ["git", "rev-parse", "HEAD"])
        with mock.patch.object(gate_results, "run", return_value=result) as runner, \
             mock.patch.object(gate_results, "binding", side_effect=failure) as binding:
            with self.assertRaisesRegex(wp1.ProductionReviewError, "applicable gate command failed") as caught:
                self.real_actual_gates(self.root, selected)
        self.assertIs(caught.exception.__cause__, failure)
        runner.assert_called_once_with(self.root, selected)
        binding.assert_called_once_with(self.root, selected)

    def test_p2_post_prospective_binding_wraps_git_failure_and_can_resume(self):
        ref, output = self._contextual_issue_ready()
        self._install_and_import_contextual(ref, output)
        adjudication = self.root / "adjudication.json"
        adjudication.write_bytes(wp1.canonical_bytes({"batch_id": batch.show(self.root)["batch_id"],
            "decisions": [self._legacy_decision(item) for item in
                          batch._accepted_observations(batch.show(self.root))]}))
        batch.adjudicate(self.root, adjudication)
        runtime = batch._prospective_batch_path(self.root, batch.show(self.root)["batch_id"])
        real_binding = gate_results.binding
        failure = subprocess.CalledProcessError(128, ["git", "rev-parse", "HEAD"])
        failures = []
        def fail_after_prospective(*args, **kwargs):
            if (runtime / "manifest.json").exists():
                failures.append(failure)
                raise failure
            return real_binding(*args, **kwargs)
        with mock.patch.object(gate_results, "binding", side_effect=fail_after_prospective):
            with self.assertRaisesRegex(wp1.ProductionReviewError, "gate reuse rejected") as caught:
                batch.prepare_evidence(self.root)
        self.assertIs(caught.exception.__cause__, failure)
        self.assertEqual(failures, [failure])
        self.assertEqual(self.gate_runner.call_count, 1)
        self.assertTrue((runtime / "gates.json").is_file())
        self.assertEqual(batch.show(self.root)["phase"], "adjudicated")
        batch.prepare_evidence(self.root)
        self.assertEqual(self.gate_runner.call_count, 2)
        self.assertEqual(batch.show(self.root)["phase"], "commit_ready")
        batch.abandon(self.root, discard_uncommitted_results=True, restore_evidence=True)

    def test_p2_prepare_reuse_rejects_live_worktree_drift_and_can_resume(self):
        ref, output = self._contextual_issue_ready()
        self._install_and_import_contextual(ref, output)
        adjudication = self.root / "adjudication.json"
        adjudication.write_bytes(wp1.canonical_bytes({"batch_id": batch.show(self.root)["batch_id"],
            "decisions": [self._legacy_decision(item) for item in
                          batch._accepted_observations(batch.show(self.root))]}))
        batch.adjudicate(self.root, adjudication)
        real_write = batch._write_fsynced
        changed = self.root / "drift"
        def drift(path, raw):
            real_write(path, raw)
            changed.write_bytes(b"unexpected worktree change")
        with mock.patch.object(batch, "_write_fsynced", side_effect=drift):
            with self.assertRaisesRegex(wp1.ProductionReviewError, "gate reuse rejected"):
                batch.prepare_evidence(self.root)
        self.assertEqual(self.gate_runner.call_count, 1)
        self.assertEqual(batch.show(self.root)["phase"], "adjudicated")
        changed.unlink()
        batch.prepare_evidence(self.root)
        self.assertEqual(self.gate_runner.call_count, 2)  # Fresh command, fresh execution.
        self.assertEqual(batch.show(self.root)["phase"], "commit_ready")
        batch.abandon(self.root, discard_uncommitted_results=True, restore_evidence=True)

    def test_p2_queue_v2_rechecks_batch_binding_and_exact_receipt(self):
        root = self._batch(batch="p2-receipt")
        manifest_path = root / "manifest.json"
        manifest = json.loads(manifest_path.read_bytes())
        selected = gate_results.candidate(manifest["batch_id"], manifest["catalog_id"],
            manifest["base_commit"], manifest["policy_sha256"], manifest["ordered_revisions"])
        receipt = self.gate_runner(self.root, selected)
        value = {"schema_version": 2, "result": receipt, "prospective_bytes": 0, "committed_bytes": 0}
        original_head = queue._head(self.root, "HEAD")
        variants = []
        bad = copy.deepcopy(value); bad["result"]["checks"].pop(); variants.append(bad)
        bad = copy.deepcopy(value); bad["result"]["checks"][0]["exit_code"] = 1; variants.append(bad)
        bad = copy.deepcopy(value)
        bad["result"]["binding"]["candidate"]["batch_id"] = "different"
        bad["result"]["binding"]["candidate_sha256"] = gate_results.digest(bad["result"]["binding"]["candidate"])
        variants.append(bad)
        bad = copy.deepcopy(value); bad["result"]["binding"]["config_sha256"] = None; variants.append(bad)
        bad = copy.deepcopy(value); bad["result"]["binding"]["tool_commit"] = "0" * 40; variants.append(bad)
        bad = copy.deepcopy(value); bad["result"]["binding"]["skip_build"] = True; variants.append(bad)
        bad = copy.deepcopy(value); bad["extra"] = 1; variants.append(bad)
        bad = copy.deepcopy(value); bad["schema_version"] = 3; variants.append(bad)
        for variant in [*variants, value]:
            # Publish each candidate from the same parent; immutable-publication
            # checks still run, so failures reach the receipt validator itself.
            subprocess.run(["git", "reset", "--soft", original_head], cwd=self.root, check=True)
            raw = wp1.canonical_bytes(variant)
            (root / "gates.json").write_bytes(raw)
            manifest["gates_sha256"] = hashlib.sha256(raw).hexdigest()
            manifest_path.write_bytes(wp1.canonical_bytes(manifest))
            self._commit("P2 receipt fixture")
            if variant is value:
                queue.rebuild(self.root)
                self.assertTrue(queue.check(self.root)["ok"])
                with mock.patch.object(gate_results, "CHECKS", gate_results.CHECKS[:-1]), \
                     mock.patch.object(gate_results, "COVERAGE", {"new.py": "01-doctor"}), \
                     mock.patch.object(gate_results, "VERSION", "ci-gates-v3"):
                    queue.rebuild(self.root)
                    self.assertTrue(queue.check(self.root)["ok"])
                    with self.assertRaises(gate_results.GateError):
                        gate_results.validate(receipt, selected=selected)
            else:
                with self.assertRaisesRegex(wp1.ProductionReviewError, "gates"):
                    queue.rebuild(self.root)

    def test_c31_checkpoint_first_postimage_mismatch_keeps_checkpoint_then_restores(self):
        ref, output = self._contextual_issue_ready()
        self._install_and_import_contextual(ref, output)
        adjudication = self.root / "adjudication.json"
        adjudication.write_bytes(wp1.canonical_bytes({"batch_id": batch.show(self.root)["batch_id"],
                                                       "decisions": [self._legacy_decision(item) for item in
                                                                      batch._accepted_observations(batch.show(self.root))]}))
        batch.adjudicate(self.root, adjudication)
        prepared = batch.prepare_evidence(self.root)
        checkpoint = batch._load(queue.checkpoint_path(self.root))
        self.assertIsInstance(checkpoint["gates"]["prospective"], dict)
        self.assertEqual(set(checkpoint["gates"]), {"commands", "prospective", "preimage_absent",
                                                     "prospective_bytes", "committed_bytes"})
        prospective = Path(prepared["prospective"])
        target = next(path for path in prospective.rglob("*") if path.is_file())
        original = target.read_bytes()
        target.write_bytes(original + b"tamper")
        with self.assertRaisesRegex(wp1.ProductionReviewError, "postimages"):
            batch.abandon(self.root, discard_uncommitted_results=True, restore_evidence=True)
        self.assertTrue(queue.checkpoint_path(self.root).exists())
        # The checkpoint remains the recovery authority until a later
        # operator retry; this test intentionally leaves its scratch tree to
        # TemporaryDirectory cleanup.

    def test_c31_committed_overbudget_and_gate_mismatch_fail_closed(self):
        ref, output = self._contextual_issue_ready()
        self._install_and_import_contextual(ref, output)
        adjudication = self.root / "adjudication.json"
        adjudication.write_bytes(wp1.canonical_bytes({"batch_id": batch.show(self.root)["batch_id"],
                                                       "decisions": [self._legacy_decision(item) for item in
                                                                      batch._accepted_observations(batch.show(self.root))]}))
        batch.adjudicate(self.root, adjudication)
        prepared = batch.prepare_evidence(self.root)
        checkpoint = batch._load(queue.checkpoint_path(self.root))
        self.assertIsInstance(checkpoint["gates"]["prospective"], dict)
        prospective = Path(prepared["prospective"])
        published = self._publish_generated(prospective)
        checkpoint = batch._load(queue.checkpoint_path(self.root))
        checkpoint["gates"]["committed_bytes"] = 0
        batch._atomic(queue.checkpoint_path(self.root), batch._checkpoint_bytes(checkpoint))
        with mock.patch.object(catalog, "TRACKED_LIMIT", 0):
            with self.assertRaisesRegex(wp1.ProductionReviewError,
                                        "committed production evidence exceeds the combined 0 MiB"):
                batch.finalize(self.root, published)
        checkpoint = batch._load(queue.checkpoint_path(self.root))
        checkpoint["gates"]["committed_bytes"] = batch._committed_production_bytes(self.root, published) + 1
        batch._atomic(queue.checkpoint_path(self.root), batch._checkpoint_bytes(checkpoint))
        with self.assertRaisesRegex(wp1.ProductionReviewError, "occupancy"):
            batch.finalize(self.root, published)

    def test_mixed_surface_and_contextual_keeps_groups_under_surface_only(self):
        ref, output = self._contextual_issue_ready(count=4)
        self._install_and_import_contextual(ref, output)
        adjudication = self.root / "adjudication.json"
        adjudication.write_bytes(wp1.canonical_bytes({"batch_id": batch.show(self.root)["batch_id"],
                                                       "decisions": [self._legacy_decision(item) for item in
                                                                      batch._accepted_observations(batch.show(self.root))]}))
        batch.adjudicate(self.root, adjudication)
        prospective = Path(batch.prepare_evidence(self.root)["prospective"])
        self.assertEqual(len(list((prospective / "raw" / "surface").glob("group-*.json"))), 1)
        # Contextual sections carry no group manifest at all, so none is written
        # for them and none is shared across the two contracts.
        contextual = prospective / "raw" / "contextual"
        self.assertTrue(contextual.is_dir())
        self.assertEqual(sorted(p.name for p in contextual.glob("group-*.json")), [])
        manifest = wp1.parse_canonical_object(
            (prospective / "manifest.json").read_bytes(), "manifest")
        by_contract = {}
        for item in manifest["adapter_refs"]:
            by_contract.setdefault(item["contract"], []).append(item)
        self.assertEqual(len(by_contract), 2, sorted(by_contract))
        self.assertTrue(all("group_manifest_path" not in item
                            for item in by_contract["translation_contextual_v2"]))

    def test_c39_named_dual_observations_publish_and_rebuild(self):
        ref, output = self._contextual_issue_ready()
        self._install_and_import_contextual(ref, output)
        observations = batch._accepted_observations(batch.show(self.root))
        decisions = [{"entry_revision_identity": item["entry_revision_identity"],
                      "observation_contract": item["contract"],
                      "observation_identity": item["observation_identity"],
                      "observation_sha256": hashlib.sha256(
                          (item["observation"] or "").encode()).hexdigest(),
                      "disposition": "advisory", "evidence_path": None,
                      "evidence_commit": None, "evidence_snapshot": None,
                      "conclusion": "C39 named dual observation", "repair_required": False}
                     for item in observations]
        input_path = self.root / "c39-adjudication.json"
        input_path.write_bytes(wp1.canonical_bytes({
            "batch_id": batch.show(self.root)["batch_id"], "decisions": decisions}))
        self.assertEqual(batch.adjudicate(self.root, input_path)["adjudicated"], 1)
        prepared = batch.prepare_evidence(self.root)
        published = self._publish_generated(Path(prepared["prospective"]))
        self.assertEqual(batch.finalize(self.root, published)["commit"], published)
        queue.rebuild(self.root)
        overrides, _reconciliation, _meta = queue.business_rows(queue.database_path(self.root))
        self.assertEqual({row[2] for row in overrides}, {"done"})

    def test_c40_repeated_recovery_accepts_exact_previous_and_desired_tuples(self):
        self._resize_and_init(1)
        batch.start(self.root, limit=1)
        batch.surface_export(self.root)
        reserved = queue.business_rows(queue.database_path(self.root))[0][0]
        surface_ref = batch.show(self.root)["surface"][0]
        batch.surface_import(self.root, {"0": self._surface_bytes(surface_ref, "ISSUE")})
        surface_complete = queue.business_rows(queue.database_path(self.root))[0][0]
        with sqlite3.connect(queue.database_path(self.root)) as connection:
            connection.execute("INSERT OR REPLACE INTO state_override VALUES (?,?,?,?,?,?,?)", reserved)
            connection.commit()
        batch.recover(self.root)
        batch.recover(self.root)
        self.assertEqual(queue.business_rows(queue.database_path(self.root))[0][0][:6], surface_complete[:6])
        batch.contextual_export(self.root)
        checkpoint = batch.show(self.root)
        contextual_output = self._contextual_bytes(checkpoint["contextual"][0], "ISSUE")
        self._install_contextual_done_state(checkpoint["contextual"][0], contextual_output)
        batch.contextual_import(self.root, {"0": contextual_output})
        contextual_complete = queue.business_rows(queue.database_path(self.root))[0][0]
        with sqlite3.connect(queue.database_path(self.root)) as connection:
            connection.execute("INSERT OR REPLACE INTO state_override VALUES (?,?,?,?,?,?,?)", surface_complete)
            connection.commit()
        batch.recover(self.root)
        batch.recover(self.root)
        self.assertEqual(queue.business_rows(queue.database_path(self.root))[0][0][:6], contextual_complete[:6])
        observations = batch._accepted_observations(batch.show(self.root))
        adjudication = self.root / "c40-adjudication.json"
        adjudication.write_bytes(wp1.canonical_bytes({
            "batch_id": batch.show(self.root)["batch_id"],
            "decisions": [self._legacy_decision(item) for item in observations]}))
        batch.adjudicate(self.root, adjudication)
        final_complete = queue.business_rows(queue.database_path(self.root))[0][0]
        with sqlite3.connect(queue.database_path(self.root)) as connection:
            connection.execute("INSERT OR REPLACE INTO state_override VALUES (?,?,?,?,?,?,?)", contextual_complete)
            connection.commit()
        batch.recover(self.root)
        batch.recover(self.root)
        self.assertEqual(queue.business_rows(queue.database_path(self.root))[0][0][:6], final_complete[:6])

    def _run_c45_surface_issue_contextual_ok(self, disposition, expected_state):
        ref, output = self._contextual_issue_ready()
        output = self._contextual_bytes(ref, "OK")
        self._install_and_import_contextual(ref, output)
        observations = batch._accepted_observations(batch.show(self.root))
        self.assertEqual({item["contract"] for item in observations},
                         {"translation_surface_screen_v1"})
        snapshot = {"sha256": hashlib.sha256(b"C45 source").hexdigest(),
                    "content": "C45 source"}
        decisions = [self._decision(
            item, disposition=disposition,
            snapshot=snapshot if disposition == "confirmed" else None,
            repair_required=disposition == "confirmed")
            for item in observations]
        adjudication = self.root / "c45-adjudication.json"
        adjudication.write_bytes(wp1.canonical_bytes({
            "batch_id": batch.show(self.root)["batch_id"],
            "decisions": decisions}))
        batch.adjudicate(self.root, adjudication)
        self.assertEqual(queue.status(self.root)["explicit_overrides"],
                         {expected_state: 1})
        prepared = batch.prepare_evidence(self.root)
        published = self._publish_generated(Path(prepared["prospective"]))
        if disposition == "confirmed":
            batch.finalize(self.root, published)
        else:
            # Exercise committed-before-finalize recovery for the pending
            # fold, then rebuild from the durable Git tree.
            batch.recover(self.root)
        queue.rebuild(self.root)
        self.assertEqual(queue.status(self.root)["explicit_overrides"],
                         {expected_state: 1})

    def test_c45_surface_issue_contextual_ok_confirmed_repair(self):
        self._run_c45_surface_issue_contextual_ok("confirmed", "repair_required")

    def test_c45_surface_issue_contextual_ok_pending_blocked(self):
        self._run_c45_surface_issue_contextual_ok("pending", "blocked")

    def test_c46_exact_prospective_temps_resume_and_abandon_is_mutation_free(self):
        self._resize_and_init(1)
        batch.start(self.root, limit=1)
        batch.surface_export(self.root)
        checkpoint = batch.show(self.root)
        batch.surface_import(self.root, {"0": self._surface_bytes(
            checkpoint["surface"][0], "OK")})
        empty = self.root / "c46-empty.json"
        empty.write_bytes(wp1.canonical_bytes({
            "batch_id": batch.show(self.root)["batch_id"], "decisions": []}))
        batch.adjudicate(self.root, empty)
        checkpoint = batch._load(queue.checkpoint_path(self.root))
        declared = batch._prospective_declared_paths(checkpoint)
        checkpoint["gates"] = {
            "commands": [],
            "prospective": {path: None for path in sorted(declared)},
            "preimage_absent": sorted(declared),
            "prospective_bytes": 0,
            "committed_bytes": 0,
        }
        batch._atomic(queue.checkpoint_path(self.root),
                      batch._checkpoint_bytes(checkpoint))
        runtime = batch._prospective_batch_path(self.root, checkpoint["batch_id"])
        core = runtime / "manifest.json"
        raw = runtime / "raw/surface/000-input_path.json"
        output = runtime / "raw/surface/000-output_path.json"
        core.parent.mkdir(parents=True, exist_ok=True)
        raw.parent.mkdir(parents=True, exist_ok=True)
        (core.with_name("." + core.name + ".tmp")).write_bytes(b"partial core")
        # These are the exact destinations used by _write_fsynced below;
        # recovery must remove their atomic temp targets before retrying.
        (raw.with_name("." + raw.name + ".tmp")).write_bytes(b"partial raw")
        (output.with_name("." + output.name + ".tmp")).write_bytes(b"partial output")
        script = self.root / "tools/ci-gates.sh"
        script.parent.mkdir(parents=True, exist_ok=True)
        script.write_text("#!/bin/sh\nexit 9\n", encoding="utf-8")
        script.chmod(0o755)
        prepared = batch.prepare_evidence(self.root)
        self.assertEqual(self.gate_runner.call_count, 1)
        self.assertFalse((core.with_name("." + core.name + ".tmp")).exists())
        self.assertFalse((raw.with_name("." + raw.name + ".tmp")).exists())
        self.assertFalse((output.with_name("." + output.name + ".tmp")).exists())
        self.assertEqual(
            [record["id"] for record in batch.show(self.root)["gates"]["commands"]],
            ["01-doctor", "02-strict-lint", "03-test-group-registration",
             "03-toolchain-unit-tests", "04-quality-facts-unit-tests",
             "04-semantic-claim-unit-tests", "04-semantic-claims-strict-registry",
             "05-contract-suite-unit-tests", "05-production-shadow-surface-ledger-tests",
             "06-runtime-collision-scan", "07-runtime-key-classification",
             "08-terminology-static-audit", "09-terminology-dynamic-audit",
             "10-domain-annotation", "11-worktree-whitespace", "11-staged-whitespace",
             "12-core-addon-build"])
        manifest = wp1.parse_canonical_object(
            (Path(prepared["prospective"]) / "manifest.json").read_bytes(), "manifest")
        self.assertEqual(manifest["adapter_refs"][0]["input_path"].split("/")[-1],
                         batch._raw_evidence_name(0, "input_path"))
        self.assertEqual(manifest["adapter_refs"][0]["output_path"].split("/")[-1],
                         batch._raw_evidence_name(0, "output_path"))
        database = queue.database_path(self.root)
        before_db = database.read_bytes()
        checkpoint_path = queue.checkpoint_path(self.root)
        before_checkpoint = checkpoint_path.read_bytes()
        unexpected = Path(prepared["prospective"]) / "unexpected.tmp"
        unexpected.write_bytes(b"not generated")
        with self.assertRaisesRegex(wp1.ProductionReviewError, "undeclared"):
            batch.abandon(self.root, discard_uncommitted_results=True,
                          restore_evidence=True)
        self.assertEqual(database.read_bytes(), before_db)
        self.assertEqual(checkpoint_path.read_bytes(), before_checkpoint)
        self.assertTrue(checkpoint_path.exists())
        unexpected.unlink()
        batch.abandon(self.root, discard_uncommitted_results=True,
                      restore_evidence=True)
        self.assertFalse(checkpoint_path.exists())
        self.assertFalse(Path(prepared["prospective"]).exists())

    def test_c47_gate_records_include_current_consumers_full_ci_and_failures(self):
        # The production runner must try every required command even in a minimal
        # repository, regardless of the old environment marker. No fake wrapper
        # or missing tests can turn that into a successful full gate.
        selected = gate_results.candidate("batch-fixture", "catalog-fixture",
                                           queue._head(self.root, "HEAD"), "a" * 64, ["b" * 64])
        with mock.patch.dict(os.environ, {"I18N_CI_GATES_FROM_PRODUCTION": "1"}):
            with self.assertRaisesRegex(wp1.ProductionReviewError, "gate command failed"):
                self.real_actual_gates(self.root, selected)
        results = list((self.root / ".artifacts/i18n/ci-gates").glob("run.*/results.json"))
        self.assertEqual(len(results), 1)
        result = json.loads(results[0].read_bytes())
        self.assertFalse(result["success"])
        self.assertEqual([r["id"] for r in result["checks"]], [i for i, _ in gate_results.CHECKS])
        self.assertEqual(result["coverage"], gate_results.COVERAGE)
        self.assertNotEqual(result["checks"][-1]["exit_code"], 0)

    def test_c48_public_cli_recovery_aliases_rebuild_temp_sqlite_idempotently(self):
        self._batch(batch="c48-cli")
        self._commit("C48 durable evidence")
        queue.init(self.root)
        database = queue.database_path(self.root)
        database.unlink()
        Path(str(database) + "-wal").unlink(missing_ok=True)
        Path(str(database) + "-shm").unlink(missing_ok=True)
        environment = os.environ.copy()
        environment["I18N_REPOSITORY_ROOT"] = str(self.root)
        command = [sys.executable, "-B", str(ROOT / "tools/i18n"),
                   "production", "batch"]
        reports = []
        first_rows = None
        for action in (("recover", "--from-head"), ("recover-from-head",)):
            result = subprocess.run(command + list(action), cwd=ROOT,
                                    env=environment, capture_output=True,
                                    text=True)
            self.assertEqual(result.returncode, 0,
                             result.stdout + result.stderr)
            self.assertNotIn("Traceback", result.stdout + result.stderr)
            report = json.loads(result.stdout)
            self.assertTrue(report["ok"])
            reports.append(report)
            current_rows = queue.business_rows(database)[0]
            if first_rows is None:
                first_rows = current_rows
            else:
                self.assertEqual(first_rows, current_rows)
        self.assertTrue(database.exists())
        self.assertTrue(all(report["recovered"] for report in reports))

    def test_c42_interrupted_prepare_reuses_canonical_inventory_and_can_abandon(self):
        self._resize_and_init(1)
        batch.start(self.root, limit=1)
        batch.surface_export(self.root)
        checkpoint = batch.show(self.root)
        batch.surface_import(self.root, {"0": self._surface_bytes(
            checkpoint["surface"][0], "OK")})
        empty = self.root / "c42-empty.json"
        empty.write_bytes(wp1.canonical_bytes({
            "batch_id": batch.show(self.root)["batch_id"], "decisions": []}))
        batch.adjudicate(self.root, empty)
        checkpoint = batch._load(queue.checkpoint_path(self.root))
        declared = batch._prospective_declared_paths(checkpoint)
        checkpoint["gates"] = {"commands": [],
                                "prospective": {path: None for path in sorted(declared)},
                                "preimage_absent": sorted(declared),
                                "prospective_bytes": 0, "committed_bytes": 0}
        batch._atomic(queue.checkpoint_path(self.root), batch._checkpoint_bytes(checkpoint))
        runtime = batch._prospective_batch_path(self.root, checkpoint["batch_id"])
        (runtime / "manifest.json").parent.mkdir(parents=True, exist_ok=True)
        (runtime / "manifest.json").write_bytes(b"partial prepare")
        batch.prepare_evidence(self.root)
        batch.abandon(self.root, discard_uncommitted_results=True,
                      restore_evidence=True)
        self.assertFalse(queue.checkpoint_path(self.root).exists())
        self.assertFalse(runtime.exists())

    def test_c31_wal_rollback_preserves_old_logical_projection(self):
        queue.init(self.root)
        database = queue.database_path(self.root)
        with sqlite3.connect(database) as connection:
            connection.execute("UPDATE meta SET catalog_id=?", ("e" * 64,))
            connection.commit()
        before = queue.business_rows(database)
        original = queue._check_projection
        def fail_after_replace(*args, **kwargs):
            if kwargs.get("database") is None:
                raise wp1.ProductionReviewError("C31 injected failure")
            return original(*args, **kwargs)
        with mock.patch.object(queue, "_check_projection", side_effect=fail_after_replace):
            with self.assertRaisesRegex(wp1.ProductionReviewError, "C31 injected"):
                queue.rebuild(self.root)
        self.assertEqual(queue.business_rows(database), before)

    def test_c44_direct_cli_forms_cover_active_batch_actions(self):
        from tools.i18nlib import cli
        parser = cli._parser()
        cases = (
            (["production", "batch", "start", "--limit", "1"], "start"),
            (["production", "batch", "show"], "show"),
            (["production", "batch", "abandon", "--discard-uncommitted-results", "--restore-evidence"], "abandon"),
            (["production", "batch", "recover", "--from-head"], "recover"),
            (["production", "batch", "surface-export"], "surface-export"),
            (["production", "batch", "surface-import", "--input", "result.json"], "surface-import"),
            (["production", "batch", "contextual-export"], "contextual-export"),
            (["production", "batch", "contextual-import", "--input", "result.json"], "contextual-import"),
            (["production", "batch", "adjudicate", "--input", "adjudications.json"], "adjudicate"),
            (["production", "batch", "prepare-evidence"], "prepare-evidence"),
            (["production", "batch", "finalize", "--commit", "HEAD"], "finalize"),
            (["production", "batch", "recover-from-head"], "recover-from-head"),
        )
        for argv, expected in cases:
            with self.subTest(argv=argv):
                self.assertEqual(parser.parse_args(argv).production_action, expected)

    def test_c31_recover_from_head_cli_alias_no_checkpoint_missing_db_is_idempotent(self):
        from tools.i18nlib import cli
        parser = cli._parser()
        self.assertEqual(parser.parse_args(["production", "batch", "recover", "--from-head"]).production_action, "recover")
        self.assertEqual(parser.parse_args(["production", "batch", "recover-from-head"]).production_action, "recover-from-head")
        queue.init(self.root)
        database = queue.database_path(self.root)
        database.unlink()
        self.assertTrue(batch.recover(self.root)["ok"])
        first = batch.finalize(self.root, queue._head(self.root, "HEAD"))
        second = batch.finalize(self.root, queue._head(self.root, "HEAD"))
        self.assertEqual(first, {"active": False, "ok": True})
        self.assertEqual(second, first)
        self.assertTrue(database.exists())


_FIXED_GATE_TIME = "2026-09-02T01:02:03+00:00"


class ProjectionChainTests(QueueFixture):
    """PERF-3: the run_batch_steps wrapper changes grouping, not behavior.

    Every step stays the ordinary CLI action; the only thing one wrapper
    invocation shares is one replay of the same evidence commit.  These tests
    count the real ``queue._projection`` calls while driving the real
    ``tools.i18nlib.cli`` entry point and the real ``run_batch_steps`` consumer
    against disposable Git/SQLite fixtures.

    The seventeen production gates are **not** run here: ``prepare-evidence``
    keeps using the existing in-process ``batch._actual_gate_records`` seam from
    ``QueueFixture``.  No assertion in this class claims the real gates passed.
    """

    # Reuse the existing helper implementations without inheriting their test
    # methods (inheriting PublicApiFlowTests would re-run its whole suite).
    _surface_bytes = PublicApiFlowTests._surface_bytes
    _contextual_bytes = PublicApiFlowTests._contextual_bytes
    _decision = PublicApiFlowTests._decision
    _resize_and_init = QueueTests._resize_and_init

    _steps_module = None

    def setUp(self):
        super().setUp()
        import tools.i18nlib as tools_package
        from tools.i18nlib import cli as tools_cli
        self._tools_cli = tools_cli
        self._aliases: list[str] = []
        self._bind_alias("i18nlib", tools_package)
        for name, module in list(sys.modules.items()):
            if name.startswith("tools.i18nlib."):
                self._bind_alias("i18nlib." + name[len("tools.i18nlib."):], module)
        self.addCleanup(self._drop_aliases)
        self._steps = self._load_wrapper()

    def _bind_alias(self, name, module):
        if name not in sys.modules:
            sys.modules[name] = module
            self._aliases.append(name)

    def _drop_aliases(self):
        for name in self._aliases:
            sys.modules.pop(name, None)

    def _load_wrapper(self):
        """Load the real wrapper against the aliased i18nlib namespace.

        ``tools/i18n`` and ``run_batch_steps.py`` import the top-level
        ``i18nlib`` package while this module imports ``tools.i18nlib``.  The
        alias above makes both names the same module objects, so a spy on
        ``queue._projection`` really observes the wrapper's calls; without it
        the two namespaces would be distinct and the spy would miss everything.
        """
        if ProjectionChainTests._steps_module is None:
            import importlib.util
            spec = importlib.util.spec_from_file_location(
                "perf_cli_projection_run_batch_steps",
                ROOT / "tools/orchestration/run_batch_steps.py")
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
            ProjectionChainTests._steps_module = module
        return ProjectionChainTests._steps_module

    @contextmanager
    def _repo_env(self):
        with mock.patch.dict(os.environ, {"I18N_REPOSITORY_ROOT": str(self.root)}):
            yield

    @contextmanager
    def _fixed_clock(self):
        """Pin the clocks and the gate log directory the two runs must share."""
        def fixed_mkdtemp(prefix=None, dir=None):
            directory = Path(dir) / "run.fixture"
            directory.mkdir(parents=True, exist_ok=True)
            return str(directory)
        fake_tempfile = type("_FixedTempfile", (), {"mkdtemp": staticmethod(fixed_mkdtemp)})()
        with mock.patch.object(catalog, "utc_now", return_value=STAMP), \
                mock.patch.object(gate_results, "_now", return_value=_FIXED_GATE_TIME), \
                mock.patch.object(gate_results, "tempfile", fake_tempfile):
            yield

    @contextmanager
    def _count_projections(self):
        calls = []
        original = queue._projection

        def counted(root, treeish, **kwargs):
            calls.append((Path(root).resolve(), treeish))
            return original(root, treeish, **kwargs)

        with mock.patch.object(queue, "_projection", side_effect=counted):
            yield calls

    def _run_cli(self, *argv):
        stdout, stderr = io.StringIO(), io.StringIO()
        with redirect_stdout(stdout), redirect_stderr(stderr):
            code = self._tools_cli.main(["production", "batch", *argv])
        return code, stdout.getvalue(), stderr.getvalue()

    def _run_wrapper(self, *tokens):
        stdout, stderr = io.StringIO(), io.StringIO()
        error = ""
        try:
            with redirect_stdout(stdout), redirect_stderr(stderr):
                code = self._steps.main(list(tokens))
        except SystemExit as exit_error:
            code = exit_error.code if isinstance(exit_error.code, int) else 1
            error = str(exit_error)
        return code, stdout.getvalue(), stderr.getvalue() + error

    def _input_dir(self):
        directory = Path(tempfile.mkdtemp(prefix="perf-cli-projection.", dir=FIXTURE_ROOT))
        self.addCleanup(shutil.rmtree, directory, True)
        return directory

    def _surface_index(self, verdict):
        checkpoint = batch.show(self.root)
        directory = self._input_dir()
        outputs = {}
        for index, ref in enumerate(checkpoint["surface"]):
            path = directory / f"surface-{index}.json"
            path.write_bytes(self._surface_bytes(ref, verdict))
            outputs[str(index)] = str(path)
        index_path = directory / "surface-index.json"
        index_path.write_text(json.dumps(outputs), encoding="utf-8")
        return index_path

    def _contextual_index(self):
        checkpoint = batch.show(self.root)
        directory = self._input_dir()
        outputs = {}
        for index, ref in enumerate(checkpoint["contextual"]):
            path = directory / f"contextual-{index}.json"
            path.write_bytes(self._contextual_bytes(ref, "OK"))
            outputs[str(index)] = str(path)
        index_path = directory / "contextual-index.json"
        index_path.write_text(json.dumps(outputs), encoding="utf-8")
        return index_path

    def _adjudication_file(self, batch_id, decisions):
        path = self._input_dir() / "adjudication.json"
        path.write_bytes(wp1.canonical_bytes({"batch_id": batch_id, "decisions": decisions}))
        return path

    def _prospective_bytes(self, batch_id):
        root = batch._prospective_batch_path(self.root, batch_id)
        return {path.relative_to(root).as_posix(): path.read_bytes()
                for path in sorted(root.rglob("*")) if path.is_file()}

    def _clone_repo(self):
        directory = Path(tempfile.mkdtemp(prefix="perf-cli-clone.", dir=FIXTURE_ROOT))
        self.addCleanup(shutil.rmtree, directory, True)
        target = directory / "repo"
        shutil.copytree(self.root, target, symlinks=True)
        return target

    def _failing_gate_records(self):
        def failing(root, selected):
            def execute(argv, cwd, log):
                log.write_bytes(b"fixture gate failure\n")
                return 1
            return gate_results.run(root, selected, execute=execute)
        return failing

    def test_wrapper_and_cli_share_the_spied_real_module(self):
        self.assertIs(self._steps.queue, queue)
        self.assertIs(self._steps.cli_main, self._tools_cli.main)
        import i18nlib.production_review_v2_lite_queue as aliased_queue
        import i18nlib.production_review_v2_lite_batch as aliased_batch
        self.assertIs(aliased_queue, queue)
        self.assertIs(aliased_batch, batch)

    def test_issue_chain_wrapper_projects_once_and_matches_separate_calls(self):
        with self._repo_env(), self._fixed_clock():
            self._resize_and_init(1)
            batch.start(self.root, limit=1)
            batch.surface_export(self.root)
            prepared = queue.checkpoint_path(self.root).read_bytes()
            index_path = self._surface_index("ISSUE")

            with self._count_projections() as separate:
                imported = self._run_cli("surface-import", "--input", str(index_path))
                exported = self._run_cli("contextual-export")
            self.assertEqual(imported[0], 0, imported[2])
            self.assertEqual(exported[0], 0, exported[2])
            checkpoint_separate = queue.checkpoint_path(self.root).read_bytes()
            rows_separate = queue.business_rows(queue.database_path(self.root))
            progress_separate = queue.check(self.root)["progress"]

            batch.abandon(self.root, discard_uncommitted_results=True)
            batch.start(self.root, limit=1)
            batch.surface_export(self.root)
            self.assertEqual(queue.checkpoint_path(self.root).read_bytes(), prepared)

            with self._count_projections() as wrapped:
                code, stdout, stderr = self._run_wrapper(
                    f"surface-import={index_path}", "contextual-export")
            self.assertEqual(code, 0, stderr)
            self.assertEqual([len(separate), len(wrapped)], [2, 1])
            self.assertEqual(queue.checkpoint_path(self.root).read_bytes(), checkpoint_separate)
            self.assertEqual(queue.business_rows(queue.database_path(self.root)), rows_separate)
            self.assertEqual(stdout, imported[1] + exported[1])
            report = queue.check(self.root)
            self.assertTrue(report["ok"])
            self.assertEqual(report["progress"], progress_separate)

    def test_rebuild_hands_its_replay_to_a_carry_scope(self):
        with self._repo_env():
            self._resize_and_init(1)
            with self._count_projections() as calls:
                with queue.carry_projection():
                    rebuilt = queue.rebuild(self.root)
                    self.assertTrue(rebuilt["progress"])
                    carried = queue.projection_for(self.root, "HEAD")
                    self.assertEqual(len(calls), 1)
                    (self.root / "moved.txt").write_text("moved\n", encoding="utf-8")
                    moved = self._commit("moved head")
                    self.assertEqual(queue.projection_for(self.root, "HEAD")[0], moved)
                    self.assertNotEqual(carried[0], moved)
                self.assertIsNone(queue._carry_slot.get())
                queue.rebuild(self.root)
            self.assertEqual(len(calls), 3)

    def test_rollover_chain_projects_once_and_matches_separate_calls(self):
        with self._repo_env(), self._fixed_clock():
            self._resize_and_init(1)
            with self._count_projections() as separate:
                stdout, stderr = io.StringIO(), io.StringIO()
                with redirect_stdout(stdout), redirect_stderr(stderr):
                    rebuilt = self._tools_cli.main(["production", "queue", "rebuild"])
                started = self._run_cli("start", "--limit", "1")
            self.assertEqual(rebuilt, 0, stderr.getvalue())
            self.assertEqual(started[0], 0, started[2])
            checkpoint_separate = queue.checkpoint_path(self.root).read_bytes()
            rows_separate = queue.business_rows(queue.database_path(self.root))

            batch.abandon(self.root, discard_uncommitted_results=True)
            with self._count_projections() as wrapped:
                code, _stdout, stderr_text = self._run_wrapper("rollover-chain", "--limit", "1")
            self.assertEqual(code, 0, stderr_text)
            self.assertEqual(len(wrapped), 1)
            self.assertLess(len(wrapped), len(separate))
            self.assertEqual(queue.checkpoint_path(self.root).read_bytes(), checkpoint_separate)
            self.assertEqual(queue.business_rows(queue.database_path(self.root)), rows_separate)

    def test_rollover_chain_stops_when_rebuild_is_refused(self):
        with self._repo_env():
            self._resize_and_init(1)
            batch.start(self.root, limit=1)
            before = queue.checkpoint_path(self.root).read_bytes()
            code, _stdout, _stderr = self._run_wrapper("rollover-chain", "--limit", "1")
            self.assertNotEqual(code, 0)
            self.assertEqual(queue.checkpoint_path(self.root).read_bytes(), before)

    def test_all_ok_import_then_second_chain_matches_separate_calls(self):
        with self._repo_env(), self._fixed_clock():
            self._resize_and_init(1)
            batch.start(self.root, limit=1)
            batch.surface_export(self.root)
            batch_id = batch.show(self.root)["batch_id"]
            index_path = self._surface_index("OK")
            adjudication = self._adjudication_file(batch_id, [])

            # All-OK: import runs on its own, contextual-export is skipped and
            # would be rejected if attempted.
            with self._count_projections() as single:
                code, _, stderr = self._run_wrapper(f"surface-import={index_path}")
            self.assertEqual(code, 0, stderr)
            self.assertEqual(len(single), 1)
            self.assertEqual(batch.show(self.root)["phase"], "surface_collected")
            skipped = self._run_cli("contextual-export")
            self.assertNotEqual(skipped[0], 0)
            self.assertIn("no deep_required", skipped[2])

            with self._count_projections() as separate:
                adjudicated = self._run_cli("adjudicate", "--input", str(adjudication))
                prepared = self._run_cli("prepare-evidence")
            self.assertEqual(adjudicated[0], 0, adjudicated[2])
            self.assertEqual(prepared[0], 0, prepared[2])
            checkpoint_separate = queue.checkpoint_path(self.root).read_bytes()
            rows_separate = queue.business_rows(queue.database_path(self.root))
            prospective_separate = self._prospective_bytes(batch_id)

            batch.abandon(self.root, discard_uncommitted_results=True, restore_evidence=True)
            batch.start(self.root, limit=1)
            batch.surface_export(self.root)
            self.assertEqual(self._run_cli("surface-import", "--input", str(index_path))[0], 0)

            with self._count_projections() as wrapped:
                code, stdout, stderr = self._run_wrapper(
                    f"adjudicate={adjudication}", "prepare-evidence")
            self.assertEqual(code, 0, stderr)
            self.assertEqual([len(separate), len(wrapped)], [2, 1])
            self.assertEqual(stdout, adjudicated[1] + prepared[1])
            self.assertEqual(queue.checkpoint_path(self.root).read_bytes(), checkpoint_separate)
            self.assertEqual(queue.business_rows(queue.database_path(self.root)), rows_separate)
            wrapped_prospective = self._prospective_bytes(batch_id)
            self.assertEqual(wrapped_prospective, prospective_separate)
            separate_receipt = json.loads(prospective_separate["gates.json"])
            wrapped_receipt = json.loads(wrapped_prospective["gates.json"])
            self.assertEqual(wrapped_receipt, separate_receipt)
            self.assertEqual(separate_receipt["result"]["binding"]["candidate"]["ordered_revisions"],
                             batch.show(self.root)["selected"])

    def test_sqlite_row_drift_between_steps_is_rejected_not_reused(self):
        with self._repo_env():
            self._resize_and_init(1)
            batch.start(self.root, limit=1)
            batch.surface_export(self.root)
            index_path = self._surface_index("ISSUE")
            with self._count_projections() as calls:
                with queue.carry_projection():
                    imported = self._run_cli("surface-import", "--input", str(index_path))
                    self.assertEqual(imported[0], 0, imported[2])
                    with closing(sqlite3.connect(queue.database_path(self.root))) as connection:
                        connection.execute("UPDATE state_override SET state='screened'")
                        connection.commit()
                    code, _, stderr = self._run_cli("contextual-export")
            self.assertNotEqual(code, 0)
            self.assertIn("not the exact previous or desired phase tuple", stderr)
            self.assertEqual(len(calls), 1)
            self.assertEqual(batch.show(self.root)["phase"], "surface_collected")

    def test_raw_input_drift_between_steps_is_rejected_not_reused(self):
        with self._repo_env():
            self._resize_and_init(1)
            batch.start(self.root, limit=1)
            batch.surface_export(self.root)
            index_path = self._surface_index("ISSUE")
            with self._count_projections() as calls:
                with queue.carry_projection():
                    imported = self._run_cli("surface-import", "--input", str(index_path))
                    self.assertEqual(imported[0], 0, imported[2])
                    raw = Path(batch.show(self.root)["surface"][0]["input_path"])
                    raw.write_bytes(raw.read_bytes() + b"\n")
                    code, _, stderr = self._run_cli("contextual-export")
            self.assertNotEqual(code, 0)
            self.assertIn("drift", stderr)
            self.assertEqual(len(calls), 1)
            self.assertEqual(batch.show(self.root)["phase"], "surface_collected")

    def test_failing_later_step_keeps_earlier_commit_and_skips_the_rest(self):
        with self._repo_env():
            self._resize_and_init(1)
            batch.start(self.root, limit=1)
            batch.surface_export(self.root)
            index_path = self._surface_index("OK")
            bad = self._input_dir() / "bad-adjudication.json"
            bad.write_text("{}", encoding="utf-8")

            with self._count_projections() as calls:
                code, _, stderr = self._run_wrapper(
                    f"surface-import={index_path}", f"adjudicate={bad}", "prepare-evidence")
            self.assertNotEqual(code, 0)
            self.assertIn("ERROR: adjudicate failed; remaining steps not run", stderr)
            checkpoint = batch.show(self.root)
            self.assertEqual(checkpoint["phase"], "surface_collected")
            self.assertIsNone(checkpoint["adjudications"])
            self.assertFalse(batch._prospective_batch_path(self.root, checkpoint["batch_id"]).exists())
            # surface-import projected once; adjudicate reuses that carried
            # replay before rejecting its own input; prepare-evidence never ran.
            self.assertEqual(len(calls), 1)

    def test_missing_later_input_rejects_the_whole_command_first(self):
        with self._repo_env():
            self._resize_and_init(1)
            batch.start(self.root, limit=1)
            batch.surface_export(self.root)
            index_path = self._surface_index("ISSUE")
            missing = self._input_dir() / "does-not-exist.json"

            with self._count_projections() as calls:
                code, _, stderr = self._run_wrapper(
                    f"surface-import={index_path}", f"adjudicate={missing}")
            self.assertNotEqual(code, 0)
            self.assertIn("not a file", stderr)
            self.assertEqual(len(calls), 0)
            self.assertEqual(batch.show(self.root)["phase"], "surface_ready")

            code, _, stderr = self._run_wrapper("finalize")
            self.assertNotEqual(code, 0)
            self.assertIn("not chainable", stderr)
            code, _, stderr = self._run_wrapper("surface-import")
            self.assertNotEqual(code, 0)
            self.assertIn("requires =<input path>", stderr)
            code, _, stderr = self._run_wrapper("surface-import=" + str(index_path), "surface-export=x")
            self.assertNotEqual(code, 0)
            self.assertIn("takes no input", stderr)

    def test_held_writer_lock_rejects_chain_before_any_step(self):
        with self._repo_env():
            self._resize_and_init(1)
            batch.start(self.root, limit=1)
            batch.surface_export(self.root)
            index_path = self._surface_index("ISSUE")
            lock = queue.repository_lock_path(self.root)
            with lock.open("a+b") as handle:
                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                with self._count_projections() as calls:
                    code, _, stderr = self._run_wrapper(
                        f"surface-import={index_path}", "contextual-export")
            self.assertNotEqual(code, 0)
            self.assertIn("lock", stderr)
            self.assertEqual(len(calls), 0)
            self.assertEqual(batch.show(self.root)["phase"], "surface_ready")

    def test_moved_head_is_rejected_inside_a_carry_scope(self):
        with self._repo_env():
            self._resize_and_init(1)
            batch.start(self.root, limit=1)
            with self._count_projections() as calls:
                with queue.carry_projection():
                    queue.projection_for(self.root, "HEAD")
                    (self.root / "drift.txt").write_text("drift\n", encoding="utf-8")
                    self._commit("head moves during active batch")
                    code, _, stderr = self._run_cli("surface-export")
            self.assertNotEqual(code, 0)
            self.assertIn("drift", stderr)
            self.assertEqual(len(calls), 2)
            self.assertEqual(batch.show(self.root)["phase"], "reserved")

    def test_carry_reuse_keys_on_root_and_head_and_resets_on_exit(self):
        with self._repo_env():
            self._resize_and_init(1)
            elsewhere = self._clone_repo()
            with self._count_projections() as calls:
                with queue.carry_projection():
                    first = queue.projection_for(self.root, "HEAD")
                    self.assertIs(queue.projection_for(self.root, "HEAD"), first)
                    # Same HEAD, different root: the slot must replay instead of
                    # reusing, which is the only case that catches a root-blind key.
                    other = queue.projection_for(elsewhere, "HEAD")
                    self.assertEqual(other[0], first[0])
                    self.assertIsNot(other, first)
                    (self.root / "moved.txt").write_text("moved\n", encoding="utf-8")
                    moved = self._commit("moved head")
                    self.assertEqual(queue.projection_for(self.root, "HEAD")[0], moved)
                after = queue.projection_for(self.root, "HEAD")
            self.assertEqual(after[0], moved)
            self.assertEqual(len(calls), 4)

    def test_exceptional_carry_exit_does_not_hold_a_slot(self):
        with self._repo_env():
            self._resize_and_init(1)
            with self._count_projections() as calls:
                with self.assertRaisesRegex(RuntimeError, "boom"):
                    with queue.carry_projection():
                        queue.projection_for(self.root, "HEAD")
                        raise RuntimeError("boom")
                self.assertIsNone(queue._carry_slot.get())
                queue.projection_for(self.root, "HEAD")
            self.assertEqual(len(calls), 2)

    def test_queue_check_replays_inside_a_carry_scope(self):
        with self._repo_env():
            self._resize_and_init(1)
            with self._count_projections() as calls:
                with queue.carry_projection():
                    queue.projection_for(self.root, "HEAD")
                    carried = queue.check(self.root)
                independent = queue.check(self.root)
            self.assertEqual(len(calls), 3)
            self.assertTrue(carried["ok"])
            self.assertEqual(carried["progress"], independent["progress"])

    def test_chained_contextual_import_still_requires_done_verified(self):
        with self._repo_env():
            self._resize_and_init(1)
            batch.start(self.root, limit=1)
            batch.surface_export(self.root)
            index_path = self._surface_index("ISSUE")
            self.assertEqual(self._run_cli("surface-import", "--input", str(index_path))[0], 0)
            self.assertEqual(self._run_cli("contextual-export")[0], 0)
            checkpoint = batch.show(self.root)
            contextual_index = self._contextual_index()
            adjudication = self._adjudication_file(checkpoint["batch_id"], [])
            with self._count_projections() as calls:
                code, _, stderr = self._run_wrapper(
                    f"contextual-import={contextual_index}", f"adjudicate={adjudication}")
            self.assertNotEqual(code, 0)
            self.assertIn("DONE_VERIFIED", stderr)
            self.assertEqual(len(calls), 1)
            self.assertEqual(batch.show(self.root)["phase"], "deep_ready")

    def test_prepare_gate_failure_then_recovery_reruns_the_gates(self):
        with self._repo_env(), self._fixed_clock():
            self._resize_and_init(1)
            batch.start(self.root, limit=1)
            batch.surface_export(self.root)
            index_path = self._surface_index("OK")
            self.assertEqual(self._run_cli("surface-import", "--input", str(index_path))[0], 0)
            checkpoint = batch.show(self.root)
            adjudication = self._adjudication_file(checkpoint["batch_id"], [])

            with mock.patch.object(batch, "_actual_gate_records",
                                   side_effect=self._failing_gate_records()) as failed:
                with self._count_projections() as calls:
                    code, _, stderr = self._run_wrapper(f"adjudicate={adjudication}", "prepare-evidence")
            self.assertNotEqual(code, 0)
            self.assertIn("gate", stderr.lower())
            self.assertEqual(failed.call_count, 1)
            self.assertEqual(len(calls), 1)
            self.assertEqual(batch.show(self.root)["phase"], "adjudicated")

            with self._count_projections() as calls:
                code, _, stderr = self._run_wrapper("prepare-evidence")
            self.assertEqual(code, 0, stderr)
            self.assertEqual(len(calls), 1)
            self.assertEqual(self.gate_runner.call_count, 1)
            self.assertEqual(batch.show(self.root)["phase"], "commit_ready")

    def test_parent_cache_on_prepare_hits_history_keeps_gate_failure_and_retries_alone(self):
        # The shell that runs the batch chain exports the cache switch; only
        # the gate seam differs from production.  History reads must hit, the
        # gate failure must still surface and keep ``adjudicated``, and the
        # retry must be prepare-evidence alone (no second adjudication import).
        with isolated_publication_git_environment(), self._repo_env(), self._fixed_clock(), \
                mock.patch.dict(os.environ, {projection_cache.MODE_ENV: "on"}):
            self._resize_and_init(1)
            batch.start(self.root, limit=1)  # a complete replay; publishes this HEAD
            self.assertTrue(list(projection_cache.cache_directory(self.root).glob("v1-*.json")), projection_cache.events)
            batch.surface_export(self.root)
            index_path = self._surface_index("OK")
            self.assertEqual(self._run_cli("surface-import", "--input", str(index_path))[0], 0)
            checkpoint = batch.show(self.root)
            adjudication = self._adjudication_file(checkpoint["batch_id"], [])

            projection_cache.events.clear()
            with mock.patch.object(batch, "_actual_gate_records",
                                   side_effect=self._failing_gate_records()) as failed, \
                    mock.patch.object(self._steps, "cli_main", wraps=self._steps.cli_main) as steps, \
                    self._count_projections() as calls:
                code, _, stderr = self._run_wrapper(f"adjudicate={adjudication}", "prepare-evidence")
            self.assertNotEqual(code, 0)
            self.assertIn("gate", stderr.lower())
            self.assertEqual(failed.call_count, 1)
            self.assertEqual([call.args[0][2] for call in steps.call_args_list],
                             ["adjudicate", "prepare-evidence"])
            self.assertEqual(calls, [])
            self.assertIn("hit", [event["event"] for event in projection_cache.events])
            self.assertEqual(batch.show(self.root)["phase"], "adjudicated")
            adjudicated = batch.show(self.root)["adjudications"]

            projection_cache.events.clear()
            with mock.patch.object(self._steps, "cli_main", wraps=self._steps.cli_main) as steps, \
                    self._count_projections() as calls:
                code, _, stderr = self._run_wrapper("prepare-evidence")
            self.assertEqual(code, 0, stderr)
            self.assertEqual([call.args[0][2] for call in steps.call_args_list], ["prepare-evidence"])
            self.assertEqual(calls, [])
            self.assertIn("hit", [event["event"] for event in projection_cache.events])
            self.assertEqual(self.gate_runner.call_count, 1)
            shown = batch.show(self.root)
            self.assertEqual(shown["phase"], "commit_ready")
            self.assertEqual(shown["adjudications"], adjudicated)





class SourceFactsChainTests(QueueFixture):
    """P1-C real CLI + SQLite + Git; only the inherited gate runner is synthetic."""
    # Reuse bounded fixture helpers, without inheriting/re-running their tests.
    _surface_bytes = ProjectionChainTests._surface_bytes
    _contextual_bytes = ProjectionChainTests._contextual_bytes
    _decision = ProjectionChainTests._decision
    _bind_alias = ProjectionChainTests._bind_alias
    _drop_aliases = ProjectionChainTests._drop_aliases
    _load_wrapper = ProjectionChainTests._load_wrapper
    _repo_env = ProjectionChainTests._repo_env
    _fixed_clock = ProjectionChainTests._fixed_clock
    _count_projections = ProjectionChainTests._count_projections
    _run_cli = ProjectionChainTests._run_cli
    _run_wrapper = ProjectionChainTests._run_wrapper
    _input_dir = ProjectionChainTests._input_dir
    _surface_index = ProjectionChainTests._surface_index
    _adjudication_file = ProjectionChainTests._adjudication_file

    def setUp(self):
        super().setUp()
        import tools.i18nlib as tools_package
        from tools.i18nlib import cli as tools_cli
        self._tools_cli = tools_cli
        self._aliases = []
        self._bind_alias("i18nlib", tools_package)
        for name, module in list(sys.modules.items()):
            if name.startswith("tools.i18nlib."):
                self._bind_alias("i18nlib." + name[len("tools.i18nlib."):], module)
        self.addCleanup(self._drop_aliases)
        self._steps = self._load_wrapper()
        from tests.i18n import test_review_source_facts as source_fixture
        self.source_fixture = source_fixture
        rows = [self._entry('1'), self._entry('2'), dict(self._entry('3'), component='cults')]
        self.entries, self.source_root = source_fixture.install_sources(self.root, rows)
        self._write_catalog()
        self._rewrite_catalog(self.entries)
        manifest_path = self.root / catalog.CATALOG_PREFIX / 'manifest.json'
        manifest = json.loads(manifest_path.read_bytes())
        manifest['terminology_snapshot_sha256'] = wp1.terminology_snapshot(self.root)
        manifest['catalog_id'] = catalog.catalog_id(manifest)
        manifest_path.write_bytes(wp1.canonical_bytes(manifest))
        self._commit('P1-C real source and terms identities')
        queue.init(self.root)
        with self._fixed_clock():
            batch.start(self.root, limit=3)
            batch.surface_export(self.root)
        cp = batch.show(self.root)
        self.workset_value = source_fixture.workset(self.root, cp)
        self.workset_path = self._input_dir() / 'source-workset.json'
        self.workset_path.write_bytes(wp1.canonical_bytes(self.workset_value))
        self.index_path = self._surface_index('ISSUE')
        # One selected revision stays shallow; the remaining two form two runs.
        self.shallow = next(r['entry_revision_identity'] for r in cp['entry_snapshots'] if r['component'] == 'tome')
        for name in json.loads(self.index_path.read_bytes()).values():
            path = Path(name)
            output = json.loads(path.read_bytes())
            for item in output['results']:
                if item['entry_revision_identity'] == self.shallow:
                    item['verdict'] = 'OK'
                    item.pop('observation', None)
            path.write_bytes(wp1.canonical_bytes(output))

    def inputs(self):
        cp = batch.show(self.root)
        return {ref['run_index']: Path(ref['input_path']).read_bytes() for ref in cp['contextual']}

    def test_enriched_real_wrapper_two_to_one_projection_exact_output_and_consumers(self):
        with self._repo_env(), self._fixed_clock():
            initial = queue.checkpoint_path(self.root).read_bytes()
            with self._count_projections() as separate:
                imported = self._run_cli('surface-import', '--input', str(self.index_path))
                exported = self._run_cli('contextual-export', '--source-workset', str(self.workset_path))
            self.assertEqual(imported[0], 0, imported[2])
            self.assertEqual(exported[0], 0, exported[2])
            separate_cp = queue.checkpoint_path(self.root).read_bytes()
            separate_rows = queue.business_rows(queue.database_path(self.root))
            separate_inputs = self.inputs()
            self.assertEqual(len(separate_inputs), 2)
            batch.abandon(self.root, discard_uncommitted_results=True)
            batch.start(self.root, limit=3)
            batch.surface_export(self.root)
            self.assertEqual(queue.checkpoint_path(self.root).read_bytes(), initial)
            with self._count_projections() as wrapped:
                code, stdout, stderr = self._run_wrapper(f'surface-import={self.index_path}', f'contextual-export={self.workset_path}')
            self.assertEqual(code, 0, stderr)
            self.assertEqual([len(separate), len(wrapped)], [2, 1])
            self.assertEqual(stdout, imported[1] + exported[1])
            self.assertEqual(queue.checkpoint_path(self.root).read_bytes(), separate_cp)
            self.assertEqual(queue.business_rows(queue.database_path(self.root)), separate_rows)
            self.assertEqual(self.inputs(), separate_inputs)
            cp = batch.show(self.root)
            deep_rows = batch._deep_rows(cp)
            expected = [row['entry_revision_identity'] for _, row in deep_rows]
            actual = []
            for ref in cp['contextual']:
                raw = Path(ref['input_path']).read_bytes()
                payload, identity = contextual_result_check.validate_envelope(json.loads(raw))
                self.assertEqual(identity, hashlib.sha256(contextual_result_check.canonical_payload_bytes(payload)).hexdigest())
                self.assertEqual(set(payload), contextual_result_check.PAYLOAD_KEYS)
                actual.extend(payload['ordered_revision_keys'])
                facts = self.source_fixture.facts
                parts = [json.loads(c['context'].split(facts.CONTEXT_MARKER)[1]) for c in payload['bounded_context']]
                package = dict(parts[0]['binding'], entries=[p['fact'] for p in parts])
                self.assertEqual(facts.sha(facts.canonical(package)), parts[0]['package_sha256'])
                self.assertEqual(package['ordered_revisions'], payload['ordered_revision_keys'])
                shallow_row = next(r for r in cp['entry_snapshots'] if r['entry_revision_identity'] == self.shallow)
                self.assertNotIn(shallow_row['target'], raw.decode())
                self.assertNotIn(shallow_row['source'], raw.decode())
                self.assertNotIn(self.shallow, raw.decode())
            self.assertEqual(actual, expected)
            # Consumers use the frozen envelope after ALL external source inputs
            # disappear. Terms are tracked base inputs; their disk copy also goes.
            shutil.rmtree(self.source_root)
            shutil.rmtree(self.root / 'terminology')
            (self.root / 'i18n/versions/tome-1.7.6.json').unlink()
            self.workset_path.unlink()
            outputs = {}
            for i, ref in enumerate(cp['contextual']):
                raw = self._contextual_bytes(ref, 'OK')
                self._install_contextual_done_state(ref, raw)
                output_path = self._input_dir() / f'contextual-{i}.json'
                output_path.write_bytes(raw)
                outputs[str(i)] = str(output_path)
            index = self._input_dir() / 'contextual-index.json'
            index.write_bytes(wp1.canonical_bytes(outputs))
            imported = self._run_cli('contextual-import', '--input', str(index))
            self.assertEqual(imported[0], 0, imported[2])
            decisions = [self._decision(item) for item in batch._accepted_observations(batch.show(self.root))]
            path = self._adjudication_file(cp['batch_id'], decisions)
            code, _, stderr = self._run_cli('adjudicate', '--input', str(path))
            self.assertEqual(code, 0, stderr)
            code, stdout, stderr = self._run_cli('prepare-evidence')
            self.assertEqual(code, 0, stderr)
            prospective = batch._prospective_batch_path(self.root, cp['batch_id'])
            raw_copies = [p.read_bytes() for p in prospective.rglob('*') if p.is_file()]
            for frozen in separate_inputs.values():
                self.assertIn(frozen, raw_copies)
            self.assertGreater(self.gate_runner.call_count, 0)

    def test_second_run_failure_and_changed_or_bare_retry_never_overwrite(self):
        with self._repo_env():
            self.assertEqual(self._run_cli('surface-import', '--input', str(self.index_path))[0], 0)
            self.assertEqual(self._run_cli('contextual-export', '--source-workset', str(self.workset_path))[0], 0)
            before_cp, before_inputs = queue.checkpoint_path(self.root).read_bytes(), self.inputs()
            # Idempotent reuse first, then a second-run hash failure.
            self.assertEqual(self._run_cli('contextual-export', '--source-workset', str(self.workset_path))[0], 0)
            cp = batch.show(self.root)
            second = batch.partition_contextual_entries(cp)[1]['entries'][0]['entry_revision_identity']
            value = copy.deepcopy(self.workset_value)
            next(v for v in value['source_verification'] if v['entry_revision_identity'] == second)['source_file_sha256'] = '0'*64
            self.workset_path.write_bytes(wp1.canonical_bytes(value))
            code, _, stderr = self._run_cli('contextual-export', '--source-workset', str(self.workset_path))
            self.assertNotEqual(code, 0)
            self.assertIn('SHA mismatch', stderr)
            self.assertEqual(queue.checkpoint_path(self.root).read_bytes(), before_cp)
            self.assertEqual(self.inputs(), before_inputs)
            # Legal raw-byte change is still a new candidate; frozen paths reject it.
            self.workset_path.write_bytes(wp1.canonical_bytes(self.workset_value) + b'\n')
            for args in [('contextual-export', '--source-workset', str(self.workset_path)), ('contextual-export',)]:
                code, _, stderr = self._run_cli(*args)
                self.assertNotEqual(code, 0)
                self.assertIn('frozen source-facts candidate differs', stderr)
                self.assertEqual(queue.checkpoint_path(self.root).read_bytes(), before_cp)
                self.assertEqual(self.inputs(), before_inputs)

    def test_raw_bytes_fact_and_terms_changes_bind_new_candidate_on_fresh_boundary(self):
        with self._repo_env(), self._fixed_clock():
            def export():
                self.assertEqual(self._run_cli('surface-import', '--input', str(self.index_path))[0], 0)
                code, _, stderr = self._run_cli('contextual-export', '--source-workset', str(self.workset_path))
                self.assertEqual(code, 0, stderr)
                return [json.loads(v)['candidate_identity'] for v in self.inputs().values()]
            def restart():
                batch.abandon(self.root, discard_uncommitted_results=True)
                batch.start(self.root, limit=3)
                batch.surface_export(self.root)
            original = export()
            restart()
            self.workset_path.write_bytes(wp1.canonical_bytes(self.workset_value) + b'\n')
            self.assertNotEqual(export(), original)
            restart()
            changed = copy.deepcopy(self.workset_value)
            for v in changed['source_verification']:
                v['matching_literal_lines'] = []  # legal pending evidence, not a false proof
            self.workset_path.write_bytes(wp1.canonical_bytes(changed))
            self.assertNotEqual(export(), original)
            # Pure terminology changes preserve rules-v2 revision keys. Bind a
            # matching current snapshot by rebuilding a valid catalog/base.
            restart()
            batch.abandon(self.root, discard_uncommitted_results=True)
            terms = self.root / 'terminology/terms.tsv'
            terms.write_text(terms.read_text().replace('术语', '新术语'))
            term_digest = wp1.terminology_snapshot(self.root)
            for row in self.entries:
                row['terminology_snapshot_sha256'] = term_digest
            self._rewrite_catalog(self.entries)
            mp = self.root / catalog.CATALOG_PREFIX / 'manifest.json'
            manifest = json.loads(mp.read_bytes())
            manifest['terminology_snapshot_sha256'] = term_digest
            manifest['catalog_id'] = catalog.catalog_id(manifest)
            mp.write_bytes(wp1.canonical_bytes(manifest))
            self._commit('new legitimate term binding')
            queue.rebuild(self.root)
            batch.start(self.root, limit=3)
            batch.surface_export(self.root)
            cp = batch.show(self.root)
            ws = self.source_fixture.workset(self.root, cp)
            self.workset_path.write_bytes(wp1.canonical_bytes(ws))
            self.index_path = self._surface_index('ISSUE')
            updated = export()
            self.assertNotEqual(updated, original)
            self.assertIn('新术语', b''.join(self.inputs().values()).decode())

    def test_fresh_export_validates_second_run_source_and_target_before_any_write(self):
        with self._repo_env():
            self.assertEqual(self._run_cli('surface-import', '--input', str(self.index_path))[0], 0)
            cp = batch.show(self.root)
            original = queue.checkpoint_path(self.root).read_bytes()
            runs = batch.partition_contextual_entries(cp)
            second = runs[1]['entries'][0]['entry_revision_identity']
            value = copy.deepcopy(self.workset_value)
            next(v for v in value['source_verification'] if v['entry_revision_identity'] == second)['source_file_sha256'] = '0'*64
            self.workset_path.write_bytes(wp1.canonical_bytes(value))
            runtime = queue.checkpoint_path(self.root).parent / 'contextual'
            code, _, stderr = self._run_cli('contextual-export', '--source-workset', str(self.workset_path))
            self.assertNotEqual(code, 0)
            self.assertIn('SHA mismatch', stderr)
            self.assertFalse(runtime.exists())
            self.assertEqual(queue.checkpoint_path(self.root).read_bytes(), original)
            # A bad second destination must likewise not write run zero.
            self.workset_path.write_bytes(wp1.canonical_bytes(self.workset_value))
            runtime.mkdir()
            blocker = runtime / '.run-001-input.json.tmp'
            blocker.mkdir()
            code, _, stderr = self._run_cli('contextual-export', '--source-workset', str(self.workset_path))
            self.assertNotEqual(code, 0)
            self.assertIn('temporary is not ordinary', stderr)
            self.assertEqual(list(runtime.iterdir()), [blocker])
            self.assertEqual(queue.checkpoint_path(self.root).read_bytes(), original)


class AdjudicationChainTests(QueueFixture):
    """Real bounded P2-B chain; gate execution uses only QueueFixture's seam."""
    _surface_bytes = PublicApiFlowTests._surface_bytes
    _contextual_bytes = PublicApiFlowTests._contextual_bytes
    _resize_and_init = QueueTests._resize_and_init
    _bind_alias = ProjectionChainTests._bind_alias
    _drop_aliases = ProjectionChainTests._drop_aliases
    _load_wrapper = ProjectionChainTests._load_wrapper
    _repo_env = ProjectionChainTests._repo_env
    _fixed_clock = ProjectionChainTests._fixed_clock
    _count_projections = ProjectionChainTests._count_projections
    _run_cli = ProjectionChainTests._run_cli
    _run_wrapper = ProjectionChainTests._run_wrapper
    _input_dir = ProjectionChainTests._input_dir
    _surface_index = ProjectionChainTests._surface_index
    _prospective_bytes = ProjectionChainTests._prospective_bytes
    _clone_repo = ProjectionChainTests._clone_repo
    _failing_gate_records = ProjectionChainTests._failing_gate_records

    def setUp(self):
        super().setUp()
        import tools.i18nlib as package
        from tools.i18nlib import cli
        self._tools_cli, self._aliases = cli, []
        self._bind_alias('i18nlib', package)
        for name, module in list(sys.modules.items()):
            if name.startswith('tools.i18nlib.'):
                self._bind_alias('i18nlib.' + name[len('tools.i18nlib.'):], module)
        self.addCleanup(self._drop_aliases)
        self._steps = self._load_wrapper()
        self.generator = self._steps.adjudication
        self._resize_and_init(1)
        self.inputs = self._input_dir()
        self.source_root = self.root / '.artifacts/source'
        self.source_root.mkdir(parents=True)
        self.source = self.source_root / 'fixture.lua'
        self.source.write_bytes('源码\r\nreturn 1\n'.encode())
        self.output = self.root / '.artifacts/i18n/adjudication-chain/result.json'
        self.spec_path = self.inputs / 'spec.json'
        self.workset_path = self.inputs / 'workset.json'
        self.index = self.inputs / 'contextual-index.json'
        original_preflight = batch.preflight
        def fixture_preflight(root, **kwargs):
            self.assertEqual(Path(root).resolve(), self.root.resolve(), 'preflight escaped fixture')
            return original_preflight(root, **kwargs)
        guard = mock.patch.object(batch, 'preflight', side_effect=fixture_preflight)
        guard.start()
        self.addCleanup(guard.stop)

    def ready(self, contextual='ISSUE', disposition='confirmed'):
        with self._fixed_clock():
            batch.start(self.root, limit=1)
            batch.surface_export(self.root)
            self.surface_index = self._surface_index('ISSUE')
            self.assertEqual(self._run_cli('surface-import', '--input', str(self.surface_index))[0], 0)
            self.assertEqual(self._run_cli('contextual-export')[0], 0)
        cp = batch.show(self.root)
        outputs = {}
        for i, ref in enumerate(cp['contextual']):
            raw = self._contextual_bytes(ref, contextual)
            self._install_contextual_done_state(ref, raw)
            path = self.inputs / f'raw-{i}.json'
            path.write_bytes(raw)
            outputs[str(i)] = str(path)
        self.index.write_bytes(wp1.canonical_bytes(outputs))
        verifications = []
        decisions = {}
        for row in cp['entry_snapshots']:
            rev = row['entry_revision_identity']
            verifications.append(dict(entry_revision_identity=rev, source=row['source'],
                section=row['section'], source_tag=row['source_tag'], args_order=row['risk']['args_order'],
                public_source_path='fixture.lua', source_file_sha256=hashlib.sha256(self.source.read_bytes()).hexdigest(),
                matching_literal_lines=[]))
            for kind in ['surface'] + (['contextual'] if contextual == 'ISSUE' else []):
                decisions[rev[:10] + '|' + kind] = dict(disposition=disposition,
                    repair_required=disposition == 'confirmed', conclusion='host fixture conclusion')
        ws = {key: cp[key] for key in ('batch_id', 'catalog_id', 'base_commit')}
        ws.update(entries=cp['entry_snapshots'], source_verification=verifications)
        self.workset_path.write_bytes(wp1.canonical_bytes(ws))
        self.spec_path.write_bytes(wp1.canonical_bytes(dict(workset=str(self.workset_path), decisions=decisions)))
        return cp

    def legacy(self, module, output):
        # Historical CLI deliberately uses cwd, not I18N_REPOSITORY_ROOT.
        previous = Path.cwd()
        try:
            os.chdir(self.root)
            return module.main([str(self.spec_path), str(output)])
        finally:
            os.chdir(previous)

    def chain(self):
        return self._run_wrapper('contextual-adjudication-chain', '--input', str(self.index),
            '--spec', str(self.spec_path), '--output', str(self.output), '--source-root', str(self.source_root))

    def snapshot(self):
        cp = batch._load(queue.checkpoint_path(self.root))
        return (queue.checkpoint_path(self.root).read_bytes(),
                queue.business_rows(queue.database_path(self.root)), self._prospective_bytes(cp['batch_id']))

    def restore(self, saved):
        shutil.rmtree(self.root)
        shutil.copytree(saved, self.root, symlinks=True)

    def test_real_three_to_one_reports_bytes_business_receipts_and_module_identity(self):
        self.assertIs(self.generator.B, batch)
        self.assertIs(self.generator.B.queue, queue)
        self.assertIs(self._steps.queue, queue)
        self.assertIs(self._steps.cli_main, self._tools_cli.main)
        self.assertIs(self._tools_cli.cli_production.production_review_v2_lite_batch, batch)
        with self._repo_env(), self._fixed_clock():
            for contextual in ('ISSUE', 'OK'):
                with self.subTest(contextual=contextual):
                    cp = self.ready(contextual)
                    saved = self._clone_repo()
                    old_states = []
                    actual_cli = self._steps.cli_main
                    def record(argv):
                        result = actual_cli(argv)
                        old_states.append(self.snapshot())
                        return result
                    with mock.patch.object(self._steps, 'cli_main', side_effect=record):
                        with self._count_projections() as old:
                            import_report = io.StringIO()
                            with redirect_stdout(import_report):
                                first = record(['production', 'batch', 'contextual-import', '--input', str(self.index)])
                            summary = io.StringIO()
                            with redirect_stdout(summary), mock.patch.object(self.generator, 'ENGINE', self.source_root):
                                self.assertEqual(self.legacy(self.generator, self.inputs / 'old.json'), 0)
                            after_generation = self.snapshot()
                            rest = self._run_wrapper(f'adjudicate={self.inputs / "old.json"}', 'prepare-evidence')
                    self.assertEqual(first, 0)
                    self.assertEqual(rest[0], 0, rest[2])
                    expected = self.snapshot()
                    expected_bytes = (self.inputs / 'old.json').read_bytes()
                    self.assertEqual(len(json.loads(expected_bytes)['decisions']), 2 if contextual == 'ISSUE' else 1)
                    self.restore(saved)  # fixture reset explicitly outside counted scope
                    new_states, new_reports = [], []
                    def capture(argv):
                        stdout = io.StringIO()
                        with redirect_stdout(stdout):
                            result = actual_cli(argv)
                        new_reports.append(stdout.getvalue())
                        print(stdout.getvalue(), end='')
                        new_states.append(self.snapshot())
                        return result
                    with mock.patch.object(self._steps, 'cli_main', side_effect=capture):
                        with self._count_projections() as new:
                            result = self.chain()
                    self.assertEqual(result[0], 0, result[2])
                    self.assertEqual([len(old), len(new)], [3, 1])
                    self.assertEqual(new_states, old_states)
                    self.assertEqual(after_generation, old_states[0])
                    self.assertEqual(self.snapshot(), expected)
                    self.assertEqual(self.output.read_bytes(), expected_bytes)
                    self.assertIn(summary.getvalue(), result[1])
                    self.assertEqual(new_reports[0], import_report.getvalue())
                    self.assertEqual(''.join(new_reports[1:]), rest[1])
                    print(f'P2B measured contextual={contextual} projection old=3 new=1; state/bytes/receipt equal')
                    batch.abandon(self.root, discard_uncommitted_results=True, restore_evidence=True)
                    self.output.unlink()

    def test_precheck_invalid_inputs_and_stale_output_call_nothing(self):
        with self._repo_env():
            self.ready()
            original_spec, original_ws = self.spec_path.read_bytes(), self.workset_path.read_bytes()
            before = self.snapshot()
            variants = [b'{"workset":1,"workset":2}', b'[]']
            for field, value in [('repair_required', 1), ('disposition', 'bogus'), ('repair_required', 'false')]:
                spec = json.loads(original_spec)
                next(iter(spec['decisions'].values()))[field] = value
                variants.append(wp1.canonical_bytes(spec))
            for raw in variants:
                with self.subTest(raw=raw):
                    self.spec_path.write_bytes(raw)
                    with mock.patch.object(self._steps, 'cli_main', wraps=self._steps.cli_main) as calls:
                        self.assertEqual(self.chain()[0], 1)
                    self.assertEqual(calls.call_count, 0)
                    self.assertEqual(self.snapshot(), before)
            self.spec_path.write_bytes(original_spec)
            ws = json.loads(original_ws)
            ws['entries'].append(ws['entries'][0])
            self.workset_path.write_bytes(wp1.canonical_bytes(ws))
            with mock.patch.object(self._steps, 'cli_main', wraps=self._steps.cli_main) as calls:
                self.assertEqual(self.chain()[0], 1)
            self.assertEqual(calls.call_count, 0)
            self.workset_path.write_bytes(original_ws)
            self.output.parent.mkdir(parents=True)
            for kind in ('file', 'dangling', 'directory'):
                with self.subTest(kind=kind):
                    if kind == 'file': self.output.write_bytes(b'previous adjudication')
                    elif kind == 'dangling': self.output.symlink_to(self.root / 'absent')
                    else: self.output.mkdir()
                    with mock.patch.object(self._steps, 'cli_main', wraps=self._steps.cli_main) as calls:
                        self.assertEqual(self.chain()[0], 1)
                    self.assertEqual(calls.call_count, 0)
                    if kind == 'file': self.assertEqual(self.output.read_bytes(), b'previous adjudication')
                    if kind == 'directory': self.output.rmdir()
                    else: self.output.unlink()
            for output in (self.spec_path, self.root / 'evidence/no.json', self.output.parent / '../escape.json'):
                with mock.patch.object(self, 'output', output), mock.patch.object(self._steps, 'cli_main') as calls:
                    self.assertEqual(self.chain()[0], 1)
                    self.assertEqual(calls.call_count, 0)
            self.assertEqual(self.snapshot(), before)

    def test_missing_extra_decisions_source_sha_and_workset_binding_fail_after_import(self):
        with self._repo_env():
            self.ready()
            saved = self._clone_repo()
            spec_raw, ws_raw = self.spec_path.read_bytes(), self.workset_path.read_bytes()
            for variant in ('missing', 'extra', 'sha', 'batch', 'row', 'path', 'symlink', 'missing-source'):
                with self.subTest(variant=variant):
                    self.restore(saved)
                    spec, ws = json.loads(spec_raw), json.loads(ws_raw)
                    if variant == 'missing': spec['decisions'].pop(next(iter(spec['decisions'])))
                    if variant == 'extra': spec['decisions']['f'*10 + '|surface'] = next(iter(spec['decisions'].values()))
                    if variant == 'sha': self.source.write_bytes(b'drifted checkout')
                    if variant == 'batch': ws['batch_id'] = 'unrelated'
                    if variant == 'row': ws['entries'][0]['target'] = 'changed frozen target'
                    if variant == 'path': ws['source_verification'][0]['public_source_path'] = '../escape'
                    if variant == 'symlink':
                        self.source.unlink()
                        self.source.symlink_to(self.spec_path)
                    if variant == 'missing-source': self.source.unlink()
                    self.spec_path.write_bytes(wp1.canonical_bytes(spec))
                    self.workset_path.write_bytes(wp1.canonical_bytes(ws))
                    with mock.patch.object(self._steps, 'cli_main', wraps=self._steps.cli_main) as calls:
                        result = self.chain()
                    self.assertEqual(result[0], 1, result)
                    self.assertEqual([call.args[0][2] for call in calls.call_args_list], ['contextual-import'])
                    self.assertEqual(batch.show(self.root)['phase'], 'deep_collected')
                    self.assertFalse(self.output.exists())

    def test_generator_owns_lock_preflight_and_frozen_decisions(self):
        with self._repo_env():
            self.ready()
            actual = self._steps.cli_main
            lock_handle = None
            def held_after_import(argv):
                nonlocal lock_handle
                result = actual(argv)
                lock_handle = queue.repository_lock_path(self.root).open('a+b')
                fcntl.flock(lock_handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                return result
            try:
                with mock.patch.object(self._steps, 'cli_main', side_effect=held_after_import) as calls:
                    result = self.chain()
                self.assertEqual(result[0], 1)
                self.assertIn('lock', result[2])
                self.assertEqual(calls.call_count, 1)
                self.assertFalse(self.output.exists())
            finally:
                if lock_handle: lock_handle.close()
            original_spec = self.spec_path.read_bytes()
            real_preflight = batch.preflight
            locks = []
            def verify_lock(root, **kwargs):
                with queue.repository_lock_path(root).open('a+b') as handle:
                    try:
                        fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                    except BlockingIOError:
                        locks.append(True)
                    else:
                        locks.append(False)
                return real_preflight(root, **kwargs)
            def change_spec(argv):
                code = actual(argv)
                if argv[2] == 'contextual-import':
                    self.spec_path.write_bytes(b'{}')
                    self.workset_path.write_bytes(b'{}')
                return code
            with mock.patch.object(batch, 'preflight', side_effect=verify_lock), \
                    mock.patch.object(self._steps, 'cli_main', side_effect=change_spec):
                result = self.chain()
            self.assertEqual(result[0], 0, result[2])
            self.assertEqual(locks, [True]*4)
            self.assertEqual(len(json.loads(self.output.read_bytes())['decisions']), len(json.loads(original_spec)['decisions']))

    def test_raw_state_checkpoint_sqlite_and_head_drift_stop_downstream(self):
        with self._repo_env():
            self.ready()
            saved = self._clone_repo()
            raw_path = Path(json.loads(self.index.read_bytes())['0'])
            raw = raw_path.read_bytes()
            actual = self._steps.cli_main
            for kind in ('raw-before', 'state-before', 'raw-after', 'sqlite', 'checkpoint', 'head'):
                with self.subTest(kind=kind):
                    self.restore(saved)
                    raw_path.write_bytes(raw)
                    if kind == 'raw-before': raw_path.write_bytes(b'{}')
                    if kind == 'state-before':
                        state = next((self.root / '.ai/task').glob('*/STATE.json'))
                        value = json.loads(state.read_bytes()); value['task_id'] = 'unrelated-task'
                        state.write_bytes(wp1.canonical_bytes(value))
                    def change(argv):
                        result = actual(argv)
                        if result == 0 and argv[2] == 'contextual-import':
                            if kind == 'raw-after': raw_path.write_bytes(b'{}')
                            if kind == 'sqlite':
                                with sqlite3.connect(queue.database_path(self.root)) as con:
                                    con.execute("UPDATE meta SET catalog_id=?", ('f'*64,))
                            if kind == 'checkpoint':
                                cp = batch._load(queue.checkpoint_path(self.root)); cp['catalog_id'] = 'f'*64
                                queue.checkpoint_path(self.root).write_bytes(batch._checkpoint_bytes(cp))
                            if kind == 'head': self._commit('head moved')
                        return result
                    with mock.patch.object(self._steps, 'cli_main', side_effect=change) as calls:
                        result = self.chain()
                    self.assertNotEqual(result[0], 0, result)
                    self.assertEqual(calls.call_count, 1)
                    self.assertFalse(self.output.exists())

    def test_publish_race_fsync_failure_and_symlink_parent_preserve_import(self):
        with self._repo_env():
            self.ready()
            saved = self._clone_repo()
            real_link = os.link
            for kind in ('race', 'fsync', 'parent'):
                with self.subTest(kind=kind):
                    self.restore(saved)
                    def link(source, target):
                        Path(target).write_bytes(b'racing winner')
                        return real_link(source, target)
                    def publish(root, output, raw):
                        self.output.parent.mkdir(parents=True)
                        self.output.parent.rmdir()
                        self.output.parent.symlink_to(self.inputs, target_is_directory=True)
                        return real_publish(root, output, raw)
                    real_publish = self.generator.publish_fresh
                    patch = (mock.patch.object(self.generator.os, 'link', side_effect=link) if kind == 'race' else
                             mock.patch.object(self.generator.os, 'fsync', side_effect=OSError('sync failed')) if kind == 'fsync' else
                             mock.patch.object(self.generator, 'publish_fresh', side_effect=publish))
                    # fsync fault is limited to generation; production import remains real.
                    real_generate = self.generator.generate
                    def generate(*args, **kwargs):
                        with patch: return real_generate(*args, **kwargs)
                    with mock.patch.object(self.generator, 'generate', side_effect=generate), \
                            mock.patch.object(self._steps, 'cli_main', wraps=self._steps.cli_main) as calls:
                        result = self.chain()
                    self.assertEqual(result[0], 1, result)
                    self.assertEqual(calls.call_count, 1)
                    self.assertEqual(batch.show(self.root)['phase'], 'deep_collected')
                    if kind == 'race': self.assertEqual(self.output.read_bytes(), b'racing winner')
                    else: self.assertFalse(self.output.exists())
                    self.assertFalse(list(self.output.parent.glob('.adjudication-*.tmp')))

    def test_adjudicate_failure_preserves_output_and_prepare_failure_recovers(self):
        with self._repo_env():
            self.ready()
            actual = self._steps.cli_main
            original = None
            def corrupt(argv):
                nonlocal original
                if argv[2] == 'adjudicate':
                    original = self.output.read_bytes()
                    value = json.loads(original)
                    value['decisions'][0]['observation_sha256'] = '0'*64
                    self.output.write_bytes(wp1.canonical_bytes(value))
                return actual(argv)
            with mock.patch.object(self._steps, 'cli_main', side_effect=corrupt) as calls:
                result = self.chain()
            self.assertEqual(result[0], 1)
            self.assertEqual(calls.call_count, 2)
            self.assertTrue(self.output.exists())
            self.assertEqual(batch.show(self.root)['phase'], 'deep_collected')
            self.output.write_bytes(original)
            self.assertEqual(self._run_cli('adjudicate', '--input', str(self.output))[0], 0)
            with mock.patch.object(batch, '_actual_gate_records', side_effect=self._failing_gate_records()):
                result = self._run_cli('prepare-evidence')
            self.assertEqual(result[0], 1)
            self.assertEqual(batch.show(self.root)['phase'], 'adjudicated')
            before = self.gate_runner.call_count
            self.assertEqual(self._run_cli('prepare-evidence')[0], 0)
            self.assertGreater(self.gate_runner.call_count, before)

    def test_nonconfirmed_never_reads_source_and_nested_scope_probe_detects_extra_replay(self):
        with self._repo_env():
            self.ready(disposition='advisory')
            saved = self._clone_repo()
            self.source.unlink()
            with self._count_projections() as calls:
                result = self.chain()
            self.assertEqual(result[0], 0, result[2])
            self.assertEqual(len(calls), 1)
            self.restore(saved)
            actual = self.generator.generate
            def nested(*args, **kwargs):
                with queue.carry_projection(): return actual(*args, **kwargs)
            with mock.patch.object(self.generator, 'generate', side_effect=nested), self._count_projections() as wrong:
                result = self.chain()
            self.assertEqual(result[0], 0, result[2])
            self.assertGreater(len(wrong), 1)  # bounded wrong variant cannot pass 3 -> 1 oracle
            print(f'P2B nested-carry wrong variant projections={len(wrong)} (expected production=1)')

    def test_import_has_no_side_effect_and_legacy_cli_default_engine_overwrites(self):
        import importlib.util
        with mock.patch.object(batch, 'preflight', side_effect=AssertionError('import preflight')):
            spec = importlib.util.spec_from_file_location('p2b_import_probe', ROOT / 'tools/orchestration/make_adjudication.py')
            module = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(module)
        self.assertEqual(module.ENGINE, Path('/workspace/t-engine4'))
        self.assertIs(module.B, batch)
        with self._repo_env():
            self.ready()
            self.assertEqual(self._run_cli('contextual-import', '--input', str(self.index))[0], 0)
            target = self.inputs / 'legacy.json'
            target.write_bytes(b'old ordinary output')
            with mock.patch.object(module, 'ENGINE', self.source_root):
                self.assertEqual(self.legacy(module, target), 0)
            self.assertEqual(len(json.loads(target.read_bytes())['decisions']), 2)

    def test_prepare_failure_in_chain_preserves_adjudicated_and_independent_retry(self):
        with self._repo_env():
            self.ready()
            with mock.patch.object(batch, '_actual_gate_records', side_effect=self._failing_gate_records()), \
                    mock.patch.object(self._steps, 'cli_main', wraps=self._steps.cli_main) as calls:
                result = self.chain()
            self.assertEqual(result[0], 1)
            self.assertEqual([c.args[0][2] for c in calls.call_args_list],
                             ['contextual-import', 'adjudicate', 'prepare-evidence'])
            self.assertEqual(batch.show(self.root)['phase'], 'adjudicated')
            self.assertTrue(self.output.is_file())
            before = self.gate_runner.call_count
            with self._count_projections() as count:
                result = self._run_cli('prepare-evidence')
            self.assertEqual(result[0], 0, result[2])
            self.assertEqual(len(count), 1)
            self.assertGreater(self.gate_runner.call_count, before)

    def test_post_publication_error_stops_and_does_not_adopt_existing_output(self):
        with self._repo_env():
            self.ready()
            actual_generate, actual_sync = self.generator.generate, os.fsync
            def generate(*args, **kwargs):
                count = 0
                def sync(fd):
                    nonlocal count
                    count += 1
                    if count == 2: raise OSError('directory sync after publication failed')
                    return actual_sync(fd)
                with mock.patch.object(self.generator.os, 'fsync', side_effect=sync):
                    return actual_generate(*args, **kwargs)
            with mock.patch.object(self.generator, 'generate', side_effect=generate), \
                    mock.patch.object(self._steps, 'cli_main', wraps=self._steps.cli_main) as calls:
                result = self.chain()
            self.assertEqual(result[0], 1)
            self.assertEqual(calls.call_count, 1)
            raw = self.output.read_bytes()
            self.assertFalse(list(self.output.parent.glob('.adjudication-*.tmp')))
            with mock.patch.object(self._steps, 'cli_main') as calls:
                self.assertEqual(self.chain()[0], 1)
            self.assertEqual(calls.call_count, 0)
            self.assertEqual(self.output.read_bytes(), raw)
            self.assertEqual(self._run_cli('adjudicate', '--input', str(self.output))[0], 0)

    def test_bounded_wrong_variants_are_distinguished_at_generation_boundary(self):
        # Deliberately unsafe IN-MEMORY variants, scoped to this disposable root.
        # They must disagree with the production failure assertions above.
        with self._repo_env():
            self.ready()
            saved = self._clone_repo()
            actual_cli, actual_generate = self._steps.cli_main, self.generator.generate
            original_assemble = self.generator._assemble
            for kind in ('no-lock', 'stale-preflight', 'no-source-sha', 'reuse-old-output'):
                with self.subTest(kind=kind):
                    self.restore(saved)
                    handle = None
                    accepted = None
                    if kind == 'no-source-sha': self.source.write_bytes(b'wrong source bytes\n')
                    if kind == 'reuse-old-output':
                        self.output.parent.mkdir(parents=True)
                        self.output.write_bytes(b'stale output')
                    def cli(argv):
                        nonlocal handle, accepted
                        result = actual_cli(argv)
                        if argv[2] == 'contextual-import' and result == 0:
                            accepted = batch._load(queue.checkpoint_path(self.root))
                            if kind == 'no-lock':
                                handle = queue.repository_lock_path(self.root).open('a+b')
                                fcntl.flock(handle.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
                            if kind == 'stale-preflight':
                                with sqlite3.connect(queue.database_path(self.root)) as con:
                                    con.execute('UPDATE meta SET catalog_id=?', ('e'*64,))
                        return result
                    def generate(*args, **kwargs):
                        if kind == 'no-lock':
                            patch = mock.patch.object(queue, 'writer_lock', side_effect=lambda root: nullcontext())
                        elif kind == 'stale-preflight':
                            patch = mock.patch.object(batch, 'preflight', return_value=accepted)
                        elif kind == 'no-source-sha':
                            def assemble(*args, **kwargs):
                                kwargs['strict'] = False
                                return original_assemble(*args, **kwargs)
                            patch = mock.patch.object(self.generator, '_assemble', side_effect=assemble)
                        else:
                            patch = nullcontext()
                        try:
                            with patch: return actual_generate(*args, **kwargs)
                        finally:
                            if handle: handle.close()
                    try:
                        from contextlib import ExitStack
                        with ExitStack() as stack:
                            if kind == 'reuse-old-output':
                                stack.enter_context(mock.patch.object(self.generator, 'fresh_output',
                                    side_effect=lambda root, output, **kw: Path(output)))
                                stack.enter_context(mock.patch.object(self.generator, 'publish_fresh',
                                    side_effect=lambda root, output, raw: Path(output).write_bytes(raw)))
                            stack.enter_context(mock.patch.object(self.generator, 'generate', side_effect=generate))
                            calls = stack.enter_context(mock.patch.object(self._steps, 'cli_main', side_effect=cli))
                            result = self.chain()
                        self.assertTrue(self.output.is_file())  # production rejects before publication
                        self.assertGreaterEqual(calls.call_count, 2)
                        if kind == 'stale-preflight': self.assertEqual(result[0], 1)
                        else: self.assertEqual(result[0], 0, result[2])
                        print(f'P2B wrong variant {kind}: generated=yes CLI calls={calls.call_count} exit={result[0]}')
                    finally:
                        if handle: handle.close()


    def test_root_truthiness_uses_one_fixture_for_all_four_real_steps(self):
        from contextlib import ExitStack

        fixture = self.root.resolve()
        actual_lock, actual_preflight = queue.writer_lock, batch.preflight
        actual_cli, actual_generate = self._steps.cli_main, self.generator.generate
        actual_fresh, actual_projection = self.generator.fresh_output, queue._projection
        stage = 'setup'
        locks, preflights, stages, outputs, projections = [], [], [], [], []

        def same_root(root):
            self.assertEqual(Path(root).resolve(), fixture, 'root escaped fixture')

        def lock(root):
            same_root(root)  # Guard before even creating a lock or its parents.
            locks.append(stage)
            return actual_lock(root)

        def preflight(root, **kwargs):
            same_root(root)
            preflights.append(stage)
            return actual_preflight(root, **kwargs)

        def fresh(root, output, **kwargs):
            same_root(root)
            self.assertEqual(Path(output), self.output)
            outputs.append(stage)
            return actual_fresh(root, output, **kwargs)

        def projection(root, treeish, **kwargs):
            same_root(root)
            projections.append((Path(root).resolve(), treeish))
            return actual_projection(root, treeish, **kwargs)

        def cli(argv):
            nonlocal stage
            stage = argv[2]
            stages.append(stage)
            return actual_cli(argv)

        def generate(root, *args, **kwargs):
            nonlocal stage
            stage = 'generate-adjudication'
            stages.append(stage)
            same_root(root)
            return actual_generate(root, *args, **kwargs)

        with tempfile.TemporaryDirectory(prefix='p2b-root-cwd-', dir=FIXTURE_ROOT) as td, ExitStack() as stack:
            other = Path(td).resolve()
            self.assertNotEqual(other, fixture)
            # Install every boundary guard before setup/preflight. Default-root
            # anchors are disposable even when the environment is empty/unset.
            stack.enter_context(mock.patch.object(queue, 'writer_lock', side_effect=lock))
            stack.enter_context(mock.patch.object(batch, 'preflight', side_effect=preflight))
            stack.enter_context(mock.patch.object(queue, '_projection', side_effect=projection))
            stack.enter_context(mock.patch.object(self.generator, 'fresh_output', side_effect=fresh))
            stack.enter_context(mock.patch.object(self._steps, 'ROOT', fixture))
            stack.enter_context(mock.patch.object(self.generator, 'ROOT', fixture))
            stack.enter_context(mock.patch.object(self._tools_cli.cli_production, '__file__',
                str(fixture / 'tools/i18nlib/cli_production.py')))
            with self._repo_env(), self._fixed_clock():
                self.ready()
            saved = self._clone_repo()
            previous = Path.cwd()
            stack.callback(os.chdir, previous)
            os.chdir(other)
            for name, configured in (('empty', ''), ('unset', None),
                    ('absolute', str(fixture)), ('relative', os.path.relpath(fixture, other))):
                with self.subTest(root_case=name), mock.patch.dict(os.environ), self._fixed_clock():
                    self.restore(saved)  # Setup/reset excluded from projection count.
                    if configured is None:
                        os.environ.pop('I18N_REPOSITORY_ROOT', None)
                    else:
                        os.environ['I18N_REPOSITORY_ROOT'] = configured
                    stage = 'chain-input-precheck'
                    for records in (locks, preflights, stages, outputs, projections):
                        records.clear()
                    with mock.patch.object(self._steps, 'cli_main', side_effect=cli), \
                            mock.patch.object(self.generator, 'generate', side_effect=generate):
                        result = self.chain()
                    expected = ['contextual-import', 'generate-adjudication', 'adjudicate', 'prepare-evidence']
                    self.assertEqual(result[0], 0, result[2])
                    self.assertEqual(stages, expected)
                    self.assertEqual(locks, expected)
                    self.assertEqual(preflights, expected)
                    self.assertEqual(len(projections), 1)
                    self.assertEqual(projections[0][0], fixture)
                    self.assertEqual(outputs[0], 'chain-input-precheck')
                    self.assertIn('generate-adjudication', outputs)
                    self.assertEqual(len(json.loads(self.output.read_bytes())['decisions']), 2)
                    self.assertEqual(batch._load(queue.checkpoint_path(fixture))['phase'], 'commit_ready')
                    self.assertEqual(list(other.iterdir()), [])
                    print(f'P2B root={name}: four real steps/locks/preflights at fixture, projection=1, other cwd untouched')


if __name__ == "__main__":
    unittest.main()
