"""Stage-1 projection optimisation: exact reuse and measurement harness.

The reference for every reuse check is the original algorithm run in the same
fixture: migration edges validated without the current-boundary rows and the
reconciliation always taken from the independent ``reconciliation_rows_for_tree``.
Comparisons are on complete values (every tuple, its order, and the complete
progress report), never on counts alone.
"""
from __future__ import annotations

import contextlib
import io
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tests.i18n import test_production_review_v2_lite_migration as migration_tests
from tools.i18nlib import production_review as wp1
from tools.i18nlib import production_review_v2_lite as catalog
from tools.i18nlib import production_review_v2_lite_migration as migration
from tools.i18nlib import production_review_v2_lite_queue as queue
from tools.i18nlib import git_evidence_reader as reader
from tools.orchestration import benchmark_projection_stage1 as stage1

@contextlib.contextmanager
def _top_level_i18nlib():
    """Make top-level ``i18nlib`` the already-imported ``tools.i18nlib`` modules.

    The harness and ``run_batch_steps.py`` import ``i18nlib``; without the
    alias they would load a second copy and leave it in ``sys.modules``, where
    it silently defeats other suites' mocks.  Every name added here is removed.
    """
    import tools.i18nlib as package
    from tools.i18nlib import cli as _cli  # noqa: F401  (bind before aliasing)
    before = set(sys.modules)
    sys.modules.setdefault("i18nlib", package)
    for name, module in list(sys.modules.items()):
        if name.startswith("tools.i18nlib."):
            sys.modules.setdefault(name[len("tools."):], module)
    try:
        yield
    finally:
        for name in set(sys.modules) - before:
            if name == "i18nlib" or name.startswith("i18nlib."):
                sys.modules.pop(name, None)


EDGE_KEYS = {"path", "old_catalog_id", "new_catalog_id", "base_commit",
             "publication_commit", "rows_by_old"}


class _Boundaries(migration_tests.MigrationFixture):
    # Borrow helpers without inheriting (and re-running) MigrationTests.
    _publish_surface_batch = migration_tests.MigrationTests._publish_surface_batch
    _publish_terminology_boundary = migration_tests.MigrationTests._publish_terminology_boundary

    def _publish_boundary(self, entries: list[dict], name: str) -> dict:
        queue.rebuild(self.root)
        candidate = self.candidate(entries)
        artifact = self.root / ".artifacts" / f"{name}.json"
        report = migration.plan(self.root, candidate, output=artifact)
        migration.apply(self.root, artifact, candidate_catalog=candidate)
        files = catalog.ordinary_tree(candidate)
        shutil.rmtree(candidate)
        for relative, raw in files.items():
            path = self.root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(raw)
        target = self.root / report["target_path"]
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(artifact.read_bytes())
        self.commit(f"{name} boundary")
        self.entries = entries
        self.catalog_id = report["new_catalog_id"]
        return report

    def _reference(self):
        """Original algorithm: no retained rows, independent reconciliation."""
        original = queue._validated_migration_edges

        def without_current_rows(root, tree, treeish, **_ignored):
            return original(root, tree, treeish)

        def independent_reconciliation(root, tree, manifest, entries, _matching):
            return migration.reconciliation_rows_for_tree(root, tree, manifest, entries)

        progress: dict = {}
        with mock.patch.object(queue, "_validated_migration_edges", side_effect=without_current_rows), \
                mock.patch.object(queue, "_current_reconciliation",
                                  side_effect=independent_reconciliation), \
                mock.patch.object(migration, "reconciliation_rows_for_tree",
                                  wraps=migration.reconciliation_rows_for_tree) as independent:
            projection = queue._projection(self.root, "HEAD", progress=progress)
        return projection, progress, independent.call_count

    def _candidate(self):
        progress: dict = {}
        with mock.patch.object(migration, "reconciliation_rows_for_tree",
                               wraps=migration.reconciliation_rows_for_tree) as independent:
            projection = queue._projection(self.root, "HEAD", progress=progress)
        return projection, progress, independent.call_count

    def _assert_same_as_reference(self):
        candidate, candidate_progress, candidate_calls = self._candidate()
        reference, reference_progress, reference_calls = self._reference()
        self.assertEqual(candidate[0], reference[0])
        self.assertEqual(candidate[1], reference[1])
        self.assertEqual(list(candidate[2]), list(reference[2]))
        self.assertEqual(candidate[3], reference[3])
        self.assertEqual(candidate[4], reference[4])
        self.assertEqual(candidate_progress, reference_progress)
        self.assertTrue(candidate_progress)
        return candidate, candidate_calls, reference_calls


class CurrentBoundaryReuseTests(_Boundaries):
    def test_current_boundary_rows_equal_the_independent_replay(self):
        self._publish_surface_batch(repair=False, entry_index=1)
        report = self._publish_boundary(
            [self.replace(self.entries[0], target="revised target"), *self.entries[1:]], "changed")
        candidate, candidate_calls, reference_calls = self._assert_same_as_reference()
        self.assertEqual((candidate_calls, reference_calls), (0, 1))
        reconciliation = candidate[4]
        self.assertEqual(len(reconciliation), len(self.entries))
        self.assertEqual({row[5] for row in reconciliation}, {"unchanged", "target_changed"})
        self.assertEqual({row[6] for row in reconciliation}, {report["migration_id"]})
        self.assertTrue(candidate[3])

    def test_only_the_current_edge_retains_complete_rows(self):
        self._publish_terminology_boundary("historical")
        historical_catalog = self.catalog_id
        self._publish_boundary(
            [self.replace(self.entries[0], target="revised target"), *self.entries[1:]], "current")
        with reader.projection_scope(self.root):
            tree = queue._tree(self.root, "HEAD")
            head = queue._head(self.root, "HEAD")
            manifest, entries, _sha = queue._catalog_view(self.root, tree)
            edges = queue._validated_migration_edges(
                self.root, tree, head,
                current_catalog=(manifest["catalog_id"], queue._catalog_identity(tree)))
            self.assertEqual(len(edges), 2)
            by_target = {edge["new_catalog_id"]: edge for edge in edges}
            self.assertEqual(set(by_target[historical_catalog]), EDGE_KEYS)
            current = by_target[manifest["catalog_id"]]
            self.assertEqual(set(current), EDGE_KEYS | {"reconciliation_rows"})
            self.assertEqual(current["reconciliation_rows"],
                             migration.reconciliation_rows_for_tree(self.root, tree, manifest, entries))
            # A different content identity for the same catalog id is not the
            # current boundary's bytes: nothing is retained.
            unbound = queue._validated_migration_edges(
                self.root, tree, head, current_catalog=(manifest["catalog_id"], "0" * 64))
            self.assertTrue(all(set(edge) == EDGE_KEYS for edge in unbound))
        _candidate, candidate_calls, reference_calls = self._assert_same_as_reference()
        self.assertEqual((candidate_calls, reference_calls), (0, 1))

    def test_no_matching_boundary_keeps_an_empty_reconciliation(self):
        self._publish_boundary(
            [self.replace(self.entries[0], target="revised target"), *self.entries[1:]], "first")
        # A later catalog without a migration: no boundary targets it.
        self.write_catalog([self.replace(self.entries[1], target="unmigrated"),
                            self.entries[0], self.entries[2]])
        self.commit("catalog without boundary")
        candidate, candidate_calls, reference_calls = self._assert_same_as_reference()
        self.assertEqual(candidate[4], [])
        self.assertEqual((candidate_calls, reference_calls), (0, 1))

    def test_duplicate_current_boundaries_still_fail_closed(self):
        self._publish_boundary(
            [self.replace(self.entries[0], target="revised target"), *self.entries[1:]], "only")
        original = queue._validated_migration_edges

        def duplicated(*args, **kwargs):
            edges = original(*args, **kwargs)
            return edges + [dict(edges[-1], path=edges[-1]["path"] + ".copy")]

        with mock.patch.object(queue, "_validated_migration_edges", side_effect=duplicated):
            with self.assertRaisesRegex(wp1.ProductionReviewError,
                                        "more than one migration boundary targets the current catalog"):
                queue._projection(self.root, "HEAD")

    def test_independent_reconciliation_entry_still_validates_its_boundary(self):
        self._publish_boundary(
            [self.replace(self.entries[0], target="revised target"), *self.entries[1:]], "checked")
        with reader.projection_scope(self.root):
            tree = queue._tree(self.root, "HEAD")
            manifest, entries, _sha = queue._catalog_view(self.root, tree)
            with self.assertRaises(wp1.ProductionReviewError):
                migration.reconciliation_rows_for_tree(self.root, tree, manifest, list(entries)[:-1])
            rows = migration.reconciliation_rows_for_tree(self.root, tree, manifest, entries)
        self.assertEqual(rows, queue._projection(self.root, "HEAD")[4])


class CarryProgressTests(_Boundaries):
    def setUp(self):
        super().setUp()
        self._publish_surface_batch(repair=False, entry_index=1)
        self._publish_boundary(
            [self.replace(self.entries[0], target="revised target"), *self.entries[1:]], "carry")

    @contextlib.contextmanager
    def _count(self):
        with mock.patch.object(queue, "_projection", wraps=queue._projection) as spy:
            yield spy

    def _independent(self):
        progress: dict = {}
        return queue._projection(self.root, "HEAD", progress=progress), progress

    def test_rebuild_hands_projection_and_complete_progress_to_the_scope(self):
        expected_projection, expected_progress = self._independent()
        with self._count() as calls:
            with queue.carry_projection():
                report = queue.rebuild(self.root)
                projection, progress = queue.projection_and_progress_for(self.root, "HEAD")
                self.assertEqual(calls.call_count, 1)
                self.assertEqual(progress, report["progress"])
                self.assertEqual(progress, expected_progress)
                self.assertEqual(projection, expected_projection)
                # The old tuple interface still returns the same carried replay.
                self.assertIs(queue.projection_for(self.root, "HEAD"), projection)
                self.assertEqual(len(projection), 5)
                # Callers cannot change the carried progress through a result.
                progress["eligible"] = -1
                report["progress"]["eligible"] = -2
                self.assertEqual(queue.projection_and_progress_for(self.root, "HEAD")[1],
                                 expected_progress)
                self.assertEqual(calls.call_count, 1)

    def test_projection_only_slot_replays_once_for_progress(self):
        _projection, expected_progress = self._independent()
        with self._count() as calls:
            with queue.carry_projection():
                first = queue.projection_for(self.root, "HEAD")
                self.assertEqual(calls.call_count, 1)
                projection, progress = queue.projection_and_progress_for(self.root, "HEAD")
                self.assertEqual(calls.call_count, 2)
                self.assertEqual(progress, expected_progress)
                self.assertEqual(projection, first)
                self.assertIs(queue.projection_for(self.root, "HEAD"), projection)
                queue.projection_and_progress_for(self.root, "HEAD")
                self.assertEqual(calls.call_count, 2)

    def test_moved_head_recomputes_projection_and_progress(self):
        with self._count() as calls:
            with queue.carry_projection():
                queue.rebuild(self.root)
                (self.root / "moved.txt").write_text("moved\n", encoding="utf-8")
                moved = self.commit("moved head")
                projection, progress = queue.projection_and_progress_for(self.root, "HEAD")
                self.assertEqual(projection[0], moved)
                self.assertEqual(calls.call_count, 2)
        independent_projection, independent_progress = self._independent()
        self.assertEqual(projection, independent_projection)
        self.assertEqual(progress, independent_progress)

    def test_other_root_is_not_shared_and_failures_are_not_carried(self):
        elsewhere = Path(tempfile.mkdtemp(prefix="stage1-clone-"))
        self.addCleanup(shutil.rmtree, elsewhere, True)
        subprocess.run(["git", "clone", "-q", str(self.root), str(elsewhere)], check=True)
        with queue.carry_projection():
            with self._count() as calls:
                mine = queue.projection_and_progress_for(self.root, "HEAD")
                other = queue.projection_and_progress_for(elsewhere, "HEAD")
                self.assertEqual(calls.call_count, 2)
                self.assertEqual(other[0][0], mine[0][0])
                self.assertIsNot(other[0], mine[0])
            with mock.patch.object(queue, "_projection", side_effect=wp1.ProductionReviewError("boom")):
                with self.assertRaisesRegex(wp1.ProductionReviewError, "boom"):
                    queue.projection_and_progress_for(self.root, "HEAD")
            # The failed replay left the previous (other-root) entry in place.
            with self._count() as calls:
                self.assertIs(queue.projection_and_progress_for(elsewhere, "HEAD")[0], other[0])
                self.assertEqual(calls.call_count, 0)
        with queue.carry_projection():
            with mock.patch.object(queue, "_projection", side_effect=wp1.ProductionReviewError("boom")):
                with self.assertRaises(wp1.ProductionReviewError):
                    queue.projection_and_progress_for(self.root, "HEAD")
            self.assertEqual(queue._carry_slot.get(), [])

    def test_outside_a_scope_every_call_replays(self):
        with self._count() as calls:
            first = queue.projection_and_progress_for(self.root, "HEAD")
            second = queue.projection_and_progress_for(self.root, "HEAD")
        self.assertEqual(calls.call_count, 2)
        self.assertEqual(first, second)
        self.assertIsNone(queue._carry_slot.get())


class _Clock:
    def __init__(self, values):
        self.values = iter(values)

    def __call__(self):
        return next(self.values)


class SegmentsTests(unittest.TestCase):
    def test_segments_are_exclusive_and_sum_to_the_projection(self):
        segments = stage1.Segments()
        inner = segments.wrap("b", lambda: "inner")
        outer = segments.wrap("a", lambda: inner())
        projection = segments.root(lambda: outer())
        # root start/a start/b start/b end/a end/root end
        with mock.patch.object(stage1.time, "perf_counter", _Clock([0.0, 1.0, 2.0, 5.0, 7.0, 10.0])):
            self.assertEqual(projection(), "inner")
        report = segments.report()
        self.assertEqual(report["segments_exclusive_s"], {"a": 3.0, "b": 3.0, stage1.INLINE: 4.0})
        self.assertEqual(report["segments_sum_s"], 10.0)
        self.assertEqual(report["segment_calls"], {"a": 1, "b": 1, stage1.INLINE: 1})

    def test_wrappers_record_nothing_outside_the_projection(self):
        segments = stage1.Segments()
        wrapped = segments.wrap("a", lambda value: value + 1)
        self.assertEqual(wrapped(1), 2)
        counted = segments.git(lambda argv, **kwargs: argv)
        counted(["git", "status"])
        self.assertEqual(segments.report()["segments_exclusive_s"], {})
        self.assertEqual(segments.report()["git_calls_total"], 0)

    def test_git_calls_are_counted_by_subcommand_only_inside(self):
        segments = stage1.Segments()
        counted = segments.git(lambda *args, **kwargs: args)

        def body():
            counted(["git", "cat-file", "blob", "x"])
            counted(args=["git", "ls-tree", "HEAD"])
            counted(["python3", "-c", "pass"])
            return True

        self.assertTrue(segments.root(body)())
        report = segments.report()
        self.assertEqual(report["git_calls"], {"cat-file": 1, "ls-tree": 1})
        self.assertEqual(report["git_calls_total"], 2)

    def test_a_second_projection_inside_the_first_is_refused(self):
        segments = stage1.Segments()
        holder: dict = {}
        holder["projection"] = segments.root(lambda: holder["projection"]())
        with self.assertRaisesRegex(RuntimeError, "exactly one projection"):
            holder["projection"]()
        self.assertFalse(segments.active)


def _report(**overrides):
    value = {"kind": stage1.KIND, "root": "/r", "treeish": "a" * 40, "wall_s": 100.0,
             "peak_self_rss_kib": 1000, "identity": {field: 1 for field in stage1.base.IDENTITY_FIELDS},
             "progress": {"eligible": 3}, "head_unchanged": True,
             "queue_invariance": {"unchanged": True}}
    value.update(overrides)
    return value


class CompareTests(unittest.TestCase):
    def test_identical_passes_and_each_limit_is_inclusive(self):
        self.assertTrue(stage1.compare(_report(), _report())["passed"])
        self.assertTrue(stage1.compare(_report(wall_s=110.0, peak_self_rss_kib=1100), _report())["passed"])

    def test_each_rule_fails_independently(self):
        identity = {field: 1 for field in stage1.base.IDENTITY_FIELDS}
        identity["reconciliation_d"] = 2
        cases = {
            "wall_fraction": _report(wall_s=110.1),
            "peak_self_rss_fraction": _report(peak_self_rss_kib=1101),
            "progress_identical": _report(progress={"eligible": 4}),
            "identity_reconciliation_d": _report(identity=identity),
            "same_treeish": _report(treeish="b" * 40),
            "head_unchanged": _report(head_unchanged=False),
        }
        for check, candidate in cases.items():
            with self.subTest(check=check):
                result = stage1.compare(candidate, _report())
                self.assertFalse(result["passed"])
                failed = {name for name, entry in result["checks"].items() if not entry["passed"]}
                self.assertEqual(failed, {check})


class HarnessTests(_Boundaries):
    def test_run_measures_one_projection_and_restores_the_modules(self):
        with _top_level_i18nlib():
            self._check_run()

    def _check_run(self):
        self._publish_surface_batch(repair=False, entry_index=1)
        self._publish_boundary(
            [self.replace(self.entries[0], target="revised target"), *self.entries[1:]], "harness")
        head = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=self.root, text=True).strip()
        _reader, measured_queue = stage1.base._load_modules(self.root)
        self.assertIs(measured_queue, queue)
        original, original_run = measured_queue._projection, subprocess.run
        result = stage1.run(self.root, head, "fixture")
        self.assertIs(measured_queue._projection, original)
        self.assertIs(subprocess.run, original_run)
        report = result["stage1"]
        self.assertEqual(result["kind"], stage1.KIND)
        self.assertEqual(result["identity"]["head"], head)
        self.assertEqual(result["identity"]["reconciliation_n"], len(self.entries))
        self.assertEqual(report["segment_calls"][stage1.INLINE], 1)
        self.assertIn("migration", report["segments_exclusive_s"])
        self.assertIn("batch", report["segments_exclusive_s"])
        self.assertGreater(report["git_calls_total"], 0)
        self.assertAlmostEqual(report["segments_sum_s"], result["wall_s"], delta=0.05 + result["wall_s"] * 0.05)
        self.assertTrue(result["progress"])

    def test_existing_output_is_refused_before_any_replay(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "report.json"
            output.write_text("kept\n", encoding="utf-8")
            with mock.patch.object(stage1, "run") as run, \
                    contextlib.redirect_stdout(io.StringIO()):
                with self.assertRaises(SystemExit):
                    stage1.main(["--root", str(self.root), "--treeish", "HEAD", "--output", str(output)])
            run.assert_not_called()
            self.assertEqual(output.read_text(encoding="utf-8"), "kept\n")


class BatchWrapperCountTests(unittest.TestCase):
    def _wrapper(self):
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "stage1_run_batch_steps", Path(stage1.__file__).with_name("run_batch_steps.py"))
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        return module

    def test_step_lines_count_real_replays_and_restore_the_projection(self):
        with _top_level_i18nlib():
            self._check_step_lines()

    def _check_step_lines(self):
        steps = self._wrapper()
        self.assertIs(steps.queue, queue)
        original = steps.queue._projection
        with mock.patch.object(steps.queue, "_projection", return_value="replayed") as replay:
            with steps._counted_projections() as samples:
                self.assertEqual(steps.queue._projection("root", "HEAD"), "replayed")
                first = len(samples)
                steps.queue._projection("root", "HEAD", progress={})
                line = steps._step_line("surface-import", 0, steps.time.monotonic(), samples, first)
            self.assertIs(steps.queue._projection, replay)
        self.assertIs(steps.queue._projection, original)
        self.assertEqual(replay.call_count, 2)
        self.assertEqual(len(samples), 2)
        self.assertRegex(line, r"^--- surface-import: exit=0 elapsed=\d+\.\ds "
                               r"projections=1 projection_elapsed=\d+\.\ds$")


if __name__ == "__main__":
    unittest.main()
