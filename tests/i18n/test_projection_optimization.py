"""Profile harness for one cache-off projection: exact identity, no side effects."""
from __future__ import annotations

import copy
import hashlib
import json
import os
import pstats
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tests.i18n import test_production_review_v2_lite_migration as migration_tests
from tools.i18nlib import git_evidence_reader as reader
from tools.i18nlib import production_review as wp1
from tools.i18nlib import production_review_v2_lite as catalog
from tools.i18nlib import production_review_v2_lite_migration as migration
from tools.i18nlib import production_review_v2_lite_queue as queue
from tools.i18nlib import projection_cache as cache
from tools.orchestration import benchmark_projection as base

REPO = Path(__file__).resolve().parents[2]
HARNESS = REPO / "tools/orchestration/profile_projection.py"


class ProfileHarnessTests(migration_tests.MigrationFixture):
    _publish_surface_batch = migration_tests.MigrationTests._publish_surface_batch

    def setUp(self):
        super().setUp()
        self._publish_surface_batch(repair=False, entry_index=1, batch_name="done")
        self.out = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, self.out, True)

    def _run(self, output: Path, *, check: bool = True) -> subprocess.CompletedProcess:
        # The parent shell exports the switch: the harness must still not touch the cache.
        environment = {**os.environ, cache.MODE_ENV: "on", cache.TRACE_ENV: "1"}
        return subprocess.run([sys.executable, "-B", str(HARNESS), "--root", str(self.root),
                               "--treeish", "HEAD", "--output-dir", str(output), "--top", "5"],
                              cwd=REPO, env=environment, stdout=subprocess.PIPE,
                              stderr=subprocess.PIPE, text=True, timeout=300, check=check)

    def test_one_profiled_replay_matches_the_oracle_and_writes_nothing_else(self):
        before = subprocess.check_output(["git", "status", "--porcelain", "--ignored"],
                                         cwd=self.root, text=True)
        with cache.disabled():
            oracle = queue._projection(self.root, "HEAD", progress={})
        output = self.out / "profile"
        result = self._run(output)
        self.assertNotIn("projection-cache:", result.stderr)
        report = json.loads((output / "summary.json").read_text(encoding="utf-8"))
        self.assertEqual(report["kind"], "projection_profile")
        self.assertEqual(report["identity"]["head"], oracle[0])
        self.assertEqual(report["identity"]["entries_d"], base._digest(list(oracle[2])))
        self.assertEqual(report["identity"]["overrides_d"], base._digest(oracle[3]))
        self.assertEqual(report["identity"]["reconciliation_d"], base._digest(oracle[4]))
        self.assertTrue(report["head_unchanged"])
        self.assertTrue(report["queue_invariance"]["unchanged"])
        self.assertEqual(len(report["profile"]["top_tottime"]), 5)
        self.assertEqual(sorted(path.name for path in output.iterdir()),
                         ["profile.pstats", "summary.json"])
        self.assertGreater(len(pstats.Stats(str(output / "profile.pstats")).stats), 0)
        self.assertFalse(cache.cache_directory(self.root).exists())
        self.assertEqual(subprocess.check_output(["git", "status", "--porcelain", "--ignored"],
                                                 cwd=self.root, text=True), before)

    def test_refuses_a_used_output_directory_and_an_active_checkpoint(self):
        used = self.out / "used"
        used.mkdir()
        (used / "keep").write_text("prior\n")
        result = self._run(used, check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual((used / "keep").read_text(), "prior\n")
        self.assertEqual([path.name for path in used.iterdir()], ["keep"])

        queue.checkpoint_path(self.root).write_text("{}")
        result = self._run(self.out / "active", check=False)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("active queue checkpoint", result.stderr)
        self.assertFalse((self.out / "active" / "summary.json").exists())

    def test_no_profile_mode_times_the_same_call_and_names_its_implementation(self):
        with cache.disabled():
            oracle = queue._projection(self.root, "HEAD", progress={})
        output = self.out / "timing"
        result = subprocess.run([sys.executable, "-B", str(HARNESS), "--root", str(self.root),
                                 "--treeish", "HEAD", "--output-dir", str(output), "--no-profile"],
                                cwd=REPO, env={**os.environ, cache.MODE_ENV: "on"},
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                timeout=300, check=True)
        self.assertNotIn("projection-cache:", result.stderr)
        report = json.loads((output / "summary.json").read_text(encoding="utf-8"))
        self.assertEqual(report["kind"], "projection_timing")
        self.assertNotIn("profile", report)
        self.assertEqual(report["identity"]["entries_d"], base._digest(list(oracle[2])))
        self.assertEqual(report["identity"]["reconciliation_d"], base._digest(oracle[4]))
        self.assertEqual(report["progress_sha256"], hashlib.sha256(json.dumps(
            report["progress"], ensure_ascii=False, sort_keys=True).encode("utf-8")).hexdigest())
        loaded = report["loaded_implementation"]
        for relative in ("i18nlib/production_review.py", "i18nlib/production_review_v2_lite.py",
                         "i18nlib/production_review_v2_lite_queue.py", "i18nlib/git_evidence_reader.py"):
            self.assertEqual(loaded[relative], base._file_sha256(REPO / "tools" / relative))
        self.assertEqual([path.name for path in output.iterdir()], ["summary.json"])


def _catalog_outcome(files, memo=None):
    """Everything a caller can observe from one validation, errors included."""
    try:
        manifest, entries, exclusions = catalog.validate_catalog_files(files, line_memo=memo)
    except Exception as error:  # noqa: BLE001 - the exact type is the observation
        return ("error", type(error), str(error))
    return ("ok", manifest, [copy.deepcopy(row) for row in entries],
            dict(entries.digest_by_revision), exclusions)


class CatalogLineReuseTests(migration_tests.MigrationFixture):
    """Per-line reuse inside one projection must be invisible except for speed."""

    replace = migration_tests.MigrationFixture.replace

    def setUp(self):
        super().setUp()
        self.base_files = self.files(self.entries)

    def files(self, entries, **kwargs):
        parent = Path(tempfile.mkdtemp())
        self.addCleanup(shutil.rmtree, parent, True)
        return catalog.ordinary_tree(self.write_catalog(entries, parent / "catalog", **kwargs))

    @staticmethod
    def ordered(lines):
        """Entry lines in the catalog's own revision order."""
        return b"".join(sorted(lines, key=lambda line: json.loads(line)["entry_revision_identity"]))

    @staticmethod
    def rebind(files, entries_raw):
        """Replace the entry bytes and re-bind only the manifest hash and self-ID."""
        files = dict(files)
        manifest_path = f"{catalog.CATALOG_PREFIX}/manifest.json"
        manifest = wp1.parse_canonical_object(files[manifest_path], "manifest")
        manifest["entries_sha256"] = hashlib.sha256(entries_raw).hexdigest()
        manifest["catalog_id"] = catalog.catalog_id(manifest)
        files[manifest_path] = wp1.canonical_bytes(manifest)
        files[f"{catalog.CATALOG_PREFIX}/entries.jsonl"] = entries_raw
        return files

    def warmed(self):
        memo = {}
        catalog.validate_catalog_files(self.base_files, line_memo=memo)
        self.assertEqual(len(memo), len(self.entries))
        return memo

    def cases(self):
        entries_path = f"{catalog.CATALOG_PREFIX}/entries.jsonl"
        lines = self.base_files[entries_path].splitlines(keepends=True)
        first = wp1.parse_jsonl(lines[0], "first")[0]
        regrouped = copy.deepcopy(first)
        regrouped["risk"]["component_group_size"] = 4
        wrong_length = copy.deepcopy(first)
        wrong_length["risk"]["target_utf8_bytes"] += 1
        bad_hash = self.replace(self.entry("new"), target="bad hash")
        bad_hash["target_sha256"] = "0" * 64
        pretty = json.dumps(json.loads(lines[1]), ensure_ascii=False, sort_keys=True).encode() + b"\n"
        return {
            "identical": self.base_files,
            "superset": self.files([*self.entries, self.entry("3")]),
            "one_changed": self.files([self.replace(self.entries[0], target="changed"), *self.entries[1:]]),
            "manifest_terminology_only": self.files(self.entries, terminology="c" * 64),
            "manifest_fixed_source_only": self.files(self.entries, fixed="commit:" + "e" * 40),
            "manifest_rules_only": self.files(self.entries, rules=catalog.FROZEN_RULES_VERSION),
            "historical_v1_rows": self.files([self.entry(str(index), rules=catalog.FROZEN_RULES_VERSION)
                                              for index in range(3)]),
            "same_revision_other_valid_bytes": self.rebind(self.base_files, b"".join(
                [wp1.canonical_bytes(regrouped) + b"\n", *lines[1:]])),
            "same_revision_invalid_bytes": self.rebind(self.base_files, b"".join(
                [wp1.canonical_bytes(wrong_length) + b"\n", *lines[1:]])),
            "reordered": self.rebind(self.base_files, b"".join([lines[1], lines[0], *lines[2:]])),
            "duplicated_line": self.rebind(self.base_files, b"".join([lines[0], *lines])),
            "duplicate_logical": self.files([*self.entries, self.replace(self.entries[1], target="twin")]),
            "noncanonical_line": self.rebind(self.base_files, b"".join([lines[0], pretty, lines[2]])),
            "missing_final_lf": self.rebind(self.base_files, b"".join(lines)[:-1]),
            "unbound_extra_line": {**self.base_files, entries_path: self.ordered(
                [*lines, wp1.canonical_bytes(self.entry("3")) + b"\n"])},
            "invalid_new_row_after_reused": self.rebind(self.base_files, self.ordered(
                [*lines, wp1.canonical_bytes(bad_hash) + b"\n"])),
        }

    def test_reuse_matches_full_validation_for_every_case(self):
        # Each rejecting case must reach the check it was built for.
        reasons = {"same_revision_invalid_bytes": "UTF-8 risk length mismatch",
                   "reordered": "not strictly ordered", "duplicated_line": "not strictly ordered",
                   "duplicate_logical": "duplicate logical identities",
                   "noncanonical_line": "line 2 is not canonical", "missing_final_lf": "must end in LF",
                   "unbound_extra_line": "component counts mismatch",
                   "invalid_new_row_after_reused": "source/target hash mismatch"}
        outcomes = set()
        for name, files in self.cases().items():
            with self.subTest(case=name):
                memo = self.warmed()
                expected = _catalog_outcome(files)
                actual = _catalog_outcome(files, memo)
                self.assertEqual(actual, expected)
                outcomes.add(expected[0])
                if name in reasons:
                    self.assertEqual(expected[0], "error")
                    self.assertIn(reasons[name], expected[2])
        # Both directions are exercised: the cases are not all accepted or all rejected.
        self.assertEqual(outcomes, {"ok", "error"})

    def test_reused_lines_recheck_manifest_bound_fields(self):
        for name, pattern in (("manifest_terminology_only", "source/terminology identity mismatch"),
                              ("manifest_fixed_source_only", "source/terminology identity mismatch"),
                              ("manifest_rules_only", "entry 0 rules mismatch")):
            with self.subTest(case=name):
                memo = self.warmed()
                before = dict(memo)
                with self.assertRaisesRegex(wp1.ProductionReviewError, pattern):
                    catalog.validate_catalog_files(self.cases()[name], line_memo=memo)
                self.assertEqual(memo, before)

    def test_hits_reuse_the_validated_rows_and_misses_validate_in_full(self):
        memo = self.warmed()
        pooled = {line: value[1] for line, value in memo.items()}
        with mock.patch.object(catalog.wp1.surface, "validate_call_locator",
                               wraps=catalog.wp1.surface.validate_call_locator) as full:
            _manifest, entries, _ = catalog.validate_catalog_files(self.base_files, line_memo=memo)
            self.assertEqual(full.call_count, 0)
            superset = self.files([*self.entries, self.entry("3")])
            _manifest, more, _ = catalog.validate_catalog_files(superset, line_memo=memo)
            self.assertEqual(full.call_count, 1)
        self.assertEqual(sorted(map(id, entries)), sorted(map(id, pooled.values())))
        self.assertEqual(len(memo), len(self.entries) + 1)
        for line, (digest, row) in memo.items():
            self.assertEqual(digest, hashlib.sha256(line).hexdigest())
            self.assertEqual(wp1.canonical_bytes(row), line)
        self.assertEqual(sum(any(row is old for old in pooled.values()) for row in more), len(self.entries))

    def test_failed_validation_records_nothing(self):
        cases = self.cases()
        for name in ("unbound_extra_line", "invalid_new_row_after_reused", "duplicated_line",
                     "same_revision_invalid_bytes"):
            with self.subTest(case=name):
                memo = {}
                with self.assertRaises(wp1.ProductionReviewError):
                    catalog.validate_catalog_files(cases[name], line_memo=memo)
                self.assertEqual(memo, {})
                warm = self.warmed()
                before = dict(warm)
                with self.assertRaises(wp1.ProductionReviewError):
                    catalog.validate_catalog_files(cases[name], line_memo=warm)
                self.assertEqual(warm, before)
        # A later successful validation with the same memo still works normally.
        memo = {}
        with self.assertRaises(wp1.ProductionReviewError):
            catalog.validate_catalog_files(cases["unbound_extra_line"], line_memo=memo)
        self.assertEqual(_catalog_outcome(self.base_files, memo), _catalog_outcome(self.base_files))
        self.assertEqual(len(memo), len(self.entries))

    def test_memo_is_scoped_to_one_projection_reader_and_root(self):
        tree = queue._tree(self.root, "HEAD")
        seen = []
        original = catalog.validate_catalog_files

        def spy(files, *, line_memo=None):
            seen.append(line_memo)
            return original(files, line_memo=line_memo)

        with mock.patch.object(catalog, "validate_catalog_files", side_effect=spy):
            queue._catalog_view(self.root, tree)          # no scope: full validation
            self.assertIsNone(seen[-1])
            other = Path(tempfile.mkdtemp())
            self.addCleanup(shutil.rmtree, other, True)
            with reader.projection_scope(other):          # a scope for another root
                queue._catalog_view(self.root, tree)
                self.assertIsNone(seen[-1])
            with reader.projection_scope(self.root):
                outer = reader.active_reader(self.root)
                queue._catalog_view(self.root, tree)
                self.assertIs(seen[-1], outer.catalog_lines)
                self.assertEqual(len(outer.catalog_lines), len(self.entries))
                with reader.projection_scope(self.root):  # nested: fresh, empty memo
                    inner = reader.active_reader(self.root)
                    self.assertIsNot(inner, outer)
                    self.assertEqual(inner.catalog_lines, {})
                    queue._catalog_view(self.root, tree)
                    self.assertIs(seen[-1], inner.catalog_lines)
                self.assertEqual(inner.catalog_lines, {})
                self.assertEqual(len(outer.catalog_lines), len(self.entries))
            self.assertEqual(outer.catalog_lines, {})
            with self.assertRaises(RuntimeError):
                with reader.projection_scope(self.root):
                    failed = reader.active_reader(self.root)
                    queue._catalog_view(self.root, tree)
                    self.assertTrue(failed.catalog_lines)
                    raise RuntimeError("abort projection")
            self.assertEqual(failed.catalog_lines, {})
            with reader.projection_scope(self.root):
                self.assertEqual(reader.active_reader(self.root).catalog_lines, {})

    def test_reused_rows_are_the_rows_the_intern_pool_already_shares(self):
        with reader.projection_scope(self.root):
            scope = reader.active_reader(self.root)
            _manifest, entries, _ = queue._catalog_view(self.root, queue._tree(self.root, "HEAD"))
            path = self.root / catalog.CATALOG_PREFIX / "manifest.json"
            value = wp1.parse_canonical_object(path.read_bytes(), "manifest")
            value["source_identities"]["engine"] = "commit:" + "9" * 40
            value["catalog_id"] = catalog.catalog_id(value)
            path.write_bytes(wp1.canonical_bytes(value))
            commit = self.commit("manifest-only catalog identity change")
            _manifest2, entries2, _ = queue._catalog_view(self.root, queue._tree(self.root, commit))
            for row, again in zip(entries, entries2):
                digest = entries.digest_by_revision[row["entry_revision_identity"]]
                self.assertIs(again, row)
                self.assertIs(scope.rows[digest][1], row)
                self.assertIs(scope.catalog_lines[wp1.canonical_bytes(row)][1], row)


class ProjectionLineReuseTests(migration_tests.MigrationFixture):
    """A complete replay over two catalogs is identical with and without reuse."""

    _publish_surface_batch = migration_tests.MigrationTests._publish_surface_batch

    def test_complete_projection_and_progress_match_full_validation(self):
        candidate = self.candidate([self.replace(self.entries[0], target="revised target"),
                                    *self.entries[1:], self.entry("3")])
        artifact = self.root / ".artifacts" / "boundary.json"
        report = migration.plan(self.root, candidate, output=artifact)
        migration.apply(self.root, artifact, candidate_catalog=candidate)
        for relative, raw in catalog.ordinary_tree(candidate).items():
            (self.root / relative).write_bytes(raw)
        shutil.rmtree(candidate)
        target = self.root / report["target_path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(artifact.read_bytes())
        self.commit("catalog boundary")
        self.catalog_id = report["new_catalog_id"]
        self.entries = [self.replace(self.entries[0], target="revised target"), *self.entries[1:]]
        self._publish_surface_batch(repair=False, entry_index=2, batch_name="after")

        original = catalog.validate_catalog_files
        calls = []

        def observed(files, *, line_memo=None):
            calls.append(0 if line_memo is None else len(line_memo))
            return original(files, line_memo=line_memo)

        def full(files, *, line_memo=None):
            return original(files)

        with cache.disabled():
            with mock.patch.object(catalog, "validate_catalog_files", side_effect=observed):
                progress = {}
                reused = queue._projection(self.root, "HEAD", progress=progress)
            with mock.patch.object(catalog, "validate_catalog_files", side_effect=full):
                oracle_progress = {}
                oracle = queue._projection(self.root, "HEAD", progress=oracle_progress)
        self.assertGreaterEqual(len(calls), 2)
        self.assertTrue(any(calls[1:]), "the second catalog must meet already validated lines")
        self.assertEqual(reused, oracle)
        self.assertEqual(progress, oracle_progress)
        self.assertEqual(base._digest(list(reused[2])), base._digest(list(oracle[2])))


class LineReuseTerminationTests(unittest.TestCase):
    """The reuse loops are bounded by the finite line list: a short probe."""

    def test_large_all_hit_and_all_miss_inputs_terminate(self):
        probe = r"""
import hashlib, sys
sys.path.insert(0, sys.argv[1])
from tools.i18nlib import production_review as wp1
from tools.i18nlib import production_review_v2_lite as catalog
from tests.i18n import test_production_review_v2_lite_migration as m
entry = m.MigrationFixture.entry
rows = sorted((entry(None, str(i)) for i in range(4000)), key=lambda r: r["entry_revision_identity"])
raw = wp1._jsonl(rows)
known = {}
digests, lines = [], []
first = wp1.parse_jsonl(raw, "probe", digests=digests, known=known, lines=lines)
known.update({line: (d, r) for line, d, r in zip(lines, digests, first)})
again = wp1.parse_jsonl(raw, "probe", digests=[], known=known, lines=[])
assert all(a is b for a, b in zip(first, again)) and len(again) == 4000
print("ok")
"""
        result = subprocess.run([sys.executable, "-B", "-c", probe, str(REPO)], cwd=REPO,
                                stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
                                timeout=60)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stdout.strip(), "ok")


if __name__ == "__main__":
    unittest.main()
