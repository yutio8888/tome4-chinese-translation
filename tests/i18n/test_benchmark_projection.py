"""Deterministic regression tests for the one-projection benchmark harness.

Nothing here replays history: the module's expensive ``run`` is
always mocked, so argument preflight and comparison semantics are exercised in
milliseconds.  The tests assert that a rejected argument never calls ``run`` and
never truncates an existing report.
"""
from __future__ import annotations

import contextlib
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest import mock

from tools.orchestration import benchmark_projection as benchmark

REPO_ROOT = Path(__file__).resolve().parents[2]
TREEISH = "a" * 40


def _call_main(argv: list[str]) -> int:
    """Invoke the CLI without echoing the report JSON into test output."""
    with contextlib.redirect_stdout(io.StringIO()):
        return benchmark.main(argv)


def _result(base_root: Path = REPO_ROOT, **overrides: object) -> dict[str, object]:
    """A minimal well-formed benchmark report for comparison/preflight tests."""
    result: dict[str, object] = {
        "kind": "projection_benchmark",
        "root": str(base_root.resolve()),
        "treeish": TREEISH,
        "peak_self_rss_kib": 1_000_000,
        "wall_s": 100.0,
        "total_user_s": 90.0,
        "identity": {field: 0 for field in benchmark.IDENTITY_FIELDS},
        "progress": {},
        "head_unchanged": True,
        "queue_invariance": {"unchanged": True},
    }
    result.update(overrides)
    return result


class CompareRootTests(unittest.TestCase):
    def test_different_root_fails_comparison(self):
        baseline = _result(REPO_ROOT)
        candidate = _result(REPO_ROOT, root=str(REPO_ROOT.parent))
        report = benchmark.compare(candidate, baseline)
        self.assertFalse(report["passed"])
        self.assertFalse(report["checks"]["same_root"]["passed"])

    def test_same_root_and_identity_passes(self):
        baseline = _result(REPO_ROOT)
        candidate = _result(REPO_ROOT, peak_self_rss_kib=100_000)
        self.assertTrue(benchmark.compare(candidate, baseline)["passed"])

    def test_same_root_is_required_in_addition_to_treeish(self):
        baseline = _result(REPO_ROOT)
        candidate = _result(REPO_ROOT, root=str(REPO_ROOT.parent))
        self.assertNotEqual(candidate["root"], baseline["root"])
        self.assertEqual(candidate["treeish"], baseline["treeish"])
        self.assertFalse(benchmark.compare(candidate, baseline)["passed"])


class FrozenThresholdTests(unittest.TestCase):
    def test_threshold_constants_unchanged(self):
        self.assertEqual(benchmark.RSS_LIMIT_KIB, 4 * 1024 * 1024)
        self.assertEqual(benchmark.RSS_BASELINE_FRACTION, 0.35)
        self.assertEqual(benchmark.TIME_BASELINE_FRACTION, 1.10)
        self.assertEqual(benchmark.IDENTITY_FIELDS, (
            "head", "catalog_id", "entries_n", "overrides_n", "reconciliation_n",
            "entries_d", "overrides_d", "reconciliation_d",
        ))

    def test_rss_and_time_limits_still_reject_regressions(self):
        baseline = _result(REPO_ROOT)
        oversized = _result(REPO_ROOT, peak_self_rss_kib=benchmark.RSS_LIMIT_KIB + 1)
        self.assertFalse(benchmark.compare(oversized, baseline)["passed"])
        slow = _result(REPO_ROOT, wall_s=baseline["wall_s"] * 1.5)
        self.assertFalse(benchmark.compare(slow, baseline)["passed"])
        slow_user = _result(REPO_ROOT, total_user_s=baseline["total_user_s"] * 1.5)
        self.assertFalse(benchmark.compare(slow_user, baseline)["passed"])


class PreflightTests(unittest.TestCase):
    def _expect_rejected(self, argv: list[str]) -> SystemExit:
        with mock.patch.object(benchmark, "run") as run:
            with self.assertRaises(SystemExit) as caught:
                _call_main(argv)
            run.assert_not_called()
        return caught.exception

    def _base_argv(self, output: Path, compare: Path | None = None) -> list[str]:
        argv = ["--root", str(REPO_ROOT), "--treeish", TREEISH, "--output", str(output)]
        if compare is not None:
            argv += ["--compare", str(compare)]
        return argv

    def test_missing_compare_file_rejected_before_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "report.json"
            self._expect_rejected(self._base_argv(output, Path(tmp) / "absent.json"))
            self.assertFalse(output.exists())

    def test_wrong_kind_compare_rejected_before_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            compare = Path(tmp) / "compare.json"
            compare.write_text(json.dumps({"kind": "something_else"}), encoding="utf-8")
            output = Path(tmp) / "report.json"
            self._expect_rejected(self._base_argv(output, compare))
            self.assertFalse(output.exists())

    def test_bad_json_compare_rejected_before_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            compare = Path(tmp) / "compare.json"
            compare.write_text("{not json", encoding="utf-8")
            self._expect_rejected(self._base_argv(Path(tmp) / "report.json", compare))

    def test_directory_output_rejected_before_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "as-directory"
            output.mkdir()
            self._expect_rejected(self._base_argv(output))

    def test_output_parent_is_a_file_rejected_before_run(self):
        with tempfile.TemporaryDirectory() as tmp:
            blocker = Path(tmp) / "blocker"
            blocker.write_text("not a directory", encoding="utf-8")
            self._expect_rejected(self._base_argv(blocker / "report.json"))

    def test_rejected_arguments_do_not_truncate_existing_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            output = Path(tmp) / "report.json"
            output.write_text("KEEP", encoding="utf-8")
            compare = Path(tmp) / "compare.json"
            compare.write_text(json.dumps({"kind": "something_else"}), encoding="utf-8")
            self._expect_rejected(self._base_argv(output, compare))
            self.assertEqual(output.read_text(encoding="utf-8"), "KEEP")


class SuccessPathTests(unittest.TestCase):
    def test_valid_arguments_measure_once_and_write_report(self):
        with tempfile.TemporaryDirectory() as tmp:
            compare = Path(tmp) / "compare.json"
            compare.write_text(json.dumps(_result(REPO_ROOT)), encoding="utf-8")
            output = Path(tmp) / "nested" / "report.json"
            candidate = _result(REPO_ROOT, peak_self_rss_kib=100_000)
            with mock.patch.object(benchmark, "run", return_value=candidate) as run:
                code = _call_main(self._argv(output, compare))
            self.assertEqual(code, 0)
            run.assert_called_once()
            self.assertEqual(str(run.call_args.args[0]), str(REPO_ROOT))
            self.assertEqual(run.call_args.args[1], TREEISH)
            report = json.loads(output.read_text(encoding="utf-8"))
            self.assertTrue(report["comparison"]["passed"])
            self.assertEqual(report["kind"], "projection_benchmark")

    def test_failing_comparison_still_writes_measurement_and_exits_nonzero(self):
        with tempfile.TemporaryDirectory() as tmp:
            compare = Path(tmp) / "compare.json"
            compare.write_text(json.dumps(_result(REPO_ROOT)), encoding="utf-8")
            output = Path(tmp) / "report.json"
            candidate = _result(REPO_ROOT, root=str(REPO_ROOT.parent),
                                peak_self_rss_kib=benchmark.RSS_LIMIT_KIB + 1)
            with mock.patch.object(benchmark, "run", return_value=candidate) as run:
                code = _call_main(self._argv(output, compare))
            self.assertEqual(code, 1)
            run.assert_called_once()
            report = json.loads(output.read_text(encoding="utf-8"))
            self.assertFalse(report["comparison"]["passed"])

    def _argv(self, output: Path, compare: Path) -> list[str]:
        return ["--root", str(REPO_ROOT), "--treeish", TREEISH,
                "--output", str(output), "--compare", str(compare)]


if __name__ == "__main__":
    unittest.main()
