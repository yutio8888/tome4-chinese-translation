"""Full gate receipts: execution, exact coverage, binding and failure boundaries."""
from concurrent.futures import ThreadPoolExecutor
from contextlib import redirect_stdout
import copy
import io
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest import mock

from tools.i18nlib import gate_results as gates


class GateResultsTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory()
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        for args in (["init", "-q"], ["config", "user.email", "test@example.invalid"],
                     ["config", "user.name", "Test"]):
            self.git(*args)
        (self.root / ".gitignore").write_text("/.artifacts/\n")
        (self.root / "source").write_text("candidate\n")
        self.git("add", ".")
        self.git("commit", "-qm", "fixture")
        self.selected = gates.candidate("batch-test", "catalog-test", self.git("rev-parse", "HEAD").strip(), "a" * 64, ["b" * 64, "c" * 64])
        self.calls = []

    def git(self, *args):
        return subprocess.check_output(["git", *args], cwd=self.root, text=True)

    def execute(self, argv, root, log):
        self.calls.append(argv)
        log.write_text(" ".join(argv) + "\n")
        return 0

    def run_gates(self, **kwargs):
        with redirect_stdout(io.StringIO()):
            return gates.run(self.root, self.selected, execute=self.execute, **kwargs)

    def test_once_complete_coverage_logs_and_isolated_runs(self):
        result = self.run_gates()
        gates.validate(result, selected=self.selected, expected_binding=gates.binding(self.root, self.selected), root=self.root)
        self.assertEqual(self.calls, [argv for _, argv in gates.CHECKS])
        self.assertEqual(len(self.calls), 17)
        self.assertEqual(result["coverage"], gates.COVERAGE)
        for record in result["checks"]:
            self.assertEqual((self.root / record["log_path"]).suffix, ".log")
        self.calls.clear()
        second = self.run_gates(skip_build=True)
        gates.validate(second, selected=self.selected, require_full=False)
        with self.assertRaises(gates.GateError):
            gates.validate(second, selected=self.selected)
        self.assertEqual(self.calls, [argv for _, argv in gates.CHECKS[:-1]])
        self.assertNotEqual(result["checks"][0]["log_path"], second["checks"][0]["log_path"])

    def test_concurrent_runs_isolate_receipts_and_logs(self):
        with ThreadPoolExecutor(max_workers=2) as pool:
            results = list(pool.map(lambda _: gates.run(self.root, self.selected, execute=self.execute), range(2)))
        paths = [{r["log_path"] for r in result["checks"]} for result in results]
        self.assertTrue(paths[0].isdisjoint(paths[1]))
        for result in results:
            gates.validate(result, selected=self.selected, root=self.root)

    def test_command_failure_continues_and_retains_diagnostics(self):
        def fail(argv, root, log):
            self.execute(argv, root, log)
            return 17
        with redirect_stdout(io.StringIO()):
            result = gates.run(self.root, self.selected, execute=fail)
        self.assertEqual(len(self.calls), 17)
        self.assertTrue(result["complete"])
        self.assertFalse(result["success"])
        path = self.root / result["checks"][0]["log_path"]
        self.assertEqual(json.loads((path.parent / "results.json").read_bytes()), result)
        with self.assertRaises(gates.GateError):
            gates.validate(result, selected=self.selected)

    def test_strict_schema_types_identity_checks_and_coverage(self):
        good = self.run_gates()
        def variants():
            for field, value in (("success", False), ("complete", False), ("schema_version", True),
                                 ("error", "failure"), ("checks", good["checks"][:-1]),
                                 ("coverage", {}), ("finished_at", "invalid")):
                bad = copy.deepcopy(good); bad[field] = value; yield bad
            bad = copy.deepcopy(good); bad["extra"] = 0; yield bad
            for field, value in (("exit_code", True), ("exit_code", 1), ("id", "duplicate"),
                                 ("argv", ["true"]), ("command", "true"), ("output_sha256", ""),
                                 ("log_path", "../../outside"), ("started_at", "2030-01-01T00:00:00+00:00")):
                bad = copy.deepcopy(good); bad["checks"][0][field] = value; yield bad
            bad = copy.deepcopy(good); bad["checks"][1] = bad["checks"][0]; yield bad
            for field, value in (("candidate_sha256", "a" * 64), ("candidate", None),
                                 ("config_sha256", "wrong"), ("tool_commit", "wrong"),
                                 ("tool_version", ""), ("tool_version", "garbage"), ("python_version", " "),
                                 ("tool_commit", "0" * 40), ("runner_version", "v1"),
                                 ("check_set_sha256", "a" * 64), ("skip_build", 0)):
                bad = copy.deepcopy(good); bad["binding"][field] = value; yield bad
        for bad in variants():
            with self.subTest(bad=bad):
                with self.assertRaises(gates.GateError):
                    gates.validate(bad, selected=self.selected)
        for field in ("config_sha256", "worktree_sha256", "tool_commit", "tool_version", "check_set_sha256"):
            expected = copy.deepcopy(good["binding"]); expected[field] = "0" * 64
            with self.assertRaises(gates.GateError):
                gates.validate(good, selected=self.selected, expected_binding=expected)
        changed = copy.deepcopy(self.selected); changed["ordered_revisions"].reverse()
        with self.assertRaises(gates.GateError):
            gates.validate(good, selected=changed)
        (self.root / good["checks"][0]["log_path"]).write_bytes(b"tampered")
        with self.assertRaises(gates.GateError):
            gates.validate(good, selected=self.selected, root=self.root)

    def test_historical_definitions_survive_each_live_definition_change(self):
        result = self.run_gates()
        for name, value in (("CHECKS", gates.CHECKS[:-1]),
                            ("COVERAGE", {"new-consumer.py": gates.CHECKS[0][0]}),
                            ("VERSION", "ci-gates-v3")):
            with self.subTest(definition=name), mock.patch.object(gates, name, value):
                gates.validate_historical(result, selected=self.selected)
                with self.assertRaises(gates.GateError):
                    gates.validate(result, selected=self.selected)

    def test_historical_malformed_receipts_raise_gate_error(self):
        good = self.run_gates()
        variants = []
        for field, value in (("checks", []), ("checks", None), ("coverage", {}),
                             ("coverage", {"consumer": []}), ("coverage", {"consumer": "absent"}),
                             ("coverage", {"": good["checks"][0]["id"]}),
                             ("complete", False), ("success", False), ("error", "failed"),
                             ("finished_at", "invalid"), ("schema_version", True)):
            bad = copy.deepcopy(good); bad[field] = value; variants.append(bad)
        for field, value in (("id", []), ("id", "../bad"), ("id", ""),
                             ("argv", None), ("argv", "true"), ("argv", []),
                             ("argv", [None]), ("argv", [""]), ("argv", ["x\0"]),
                             ("command", []), ("exit_code", True), ("exit_code", 1),
                             ("output_sha256", None), ("log_path", []),
                             ("started_at", "2030-01-01T00:00:00+00:00")):
            bad = copy.deepcopy(good); bad["checks"][0][field] = value; variants.append(bad)
        for field, value in (("runner_version", []), ("runner_version", "v2"),
                             ("skip_build", True), ("candidate", None),
                             ("tool_commit", "0" * 40), ("config_sha256", None),
                             ("tool_version", None), ("python_version", "bad")):
            bad = copy.deepcopy(good); bad["binding"][field] = value; variants.append(bad)
        for records in ([None], good["checks"][:-1], list(reversed(good["checks"])),
                        [good["checks"][0], *good["checks"]]):
            bad = copy.deepcopy(good); bad["checks"] = records; variants.append(bad)
        # Even a recomputed digest must not authorize duplicate IDs.
        bad = copy.deepcopy(good); bad["checks"][1] = bad["checks"][0]
        bad["binding"]["check_set_sha256"] = gates.digest([(r["id"], r["argv"]) for r in bad["checks"]])
        variants.append(bad)
        for bad in variants:
            with self.subTest(bad=bad), self.assertRaises(gates.GateError):
                gates.validate_historical(bad, selected=self.selected)

    def test_live_binding_tracks_index_worktree_config_tools_and_untracked(self):
        original = gates.binding(self.root, self.selected)
        ignored = self.root / ".artifacts/prospective"
        ignored.parent.mkdir(); ignored.write_bytes(b"scratch")
        self.assertEqual(original, gates.binding(self.root, self.selected))
        for name in ("source", "tools/new.py", "tests/i18n/test_groups.json", "i18n/config.json"):
            path = self.root / name; path.parent.mkdir(parents=True, exist_ok=True)
            before = gates.binding(self.root, self.selected)
            path.write_bytes(b"changed")
            self.assertNotEqual(before, gates.binding(self.root, self.selected))
        before = gates.binding(self.root, self.selected)
        self.git("add", "source")
        self.assertNotEqual(before, gates.binding(self.root, self.selected))
        before = gates.binding(self.root, self.selected)
        self.git("commit", "-qm", "new tool commit")
        self.assertNotEqual(before["tool_commit"], gates.binding(self.root, self.selected)["tool_commit"])
        with mock.patch.dict(os.environ, {"TOME_LUAJIT": "/different"}):
            self.assertNotEqual(before["config_sha256"], gates.binding(self.root, self.selected)["config_sha256"])

    def test_mutation_during_execution_rejects_result(self):
        def mutate(argv, root, log):
            (root / "source").write_text("changed")
            return self.execute(argv, root, log)
        with redirect_stdout(io.StringIO()):
            result = gates.run(self.root, self.selected, execute=mutate)
        self.assertFalse(result["complete"])
        self.assertIn("binding changed", result["error"])

    def test_missing_production_commands_never_fail_open_with_marker(self):
        with mock.patch.dict(os.environ, {"I18N_CI_GATES_FROM_PRODUCTION": "1"}):
            with redirect_stdout(io.StringIO()):
                result = gates.run(self.root, self.selected)
        self.assertFalse(result["success"])
        self.assertEqual(len(result["checks"]), 17)
        self.assertNotEqual(result["checks"][-1]["exit_code"], 0)


if __name__ == "__main__":
    unittest.main()
