from contextlib import redirect_stdout
import io
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import unittest

from tools import test_groups
from tools.i18nlib import gate_results


class TestGroupsTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory(prefix="test-groups-")
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        (self.root / "tests").mkdir()
        (self.root / "tests/__init__.py").touch()
        (self.root / "tests/test_one.py").write_text(
            "import unittest\nclass One(unittest.TestCase):\n"
            "    def test_one(self): self.assertTrue(True)\n", encoding="utf-8")
        self.config = {"groups": {"one": ["tests/test_one.py"]}, "indirect": {}, "excluded": {}}

    def run_cli(self, *args, raw=None):
        path = self.root / "groups.json"
        path.write_text(raw if raw is not None else json.dumps(self.config), encoding="utf-8")
        return subprocess.run(
            [sys.executable, "-B", str(test_groups.ROOT / "tools/test_groups.py"),
             "--root", str(self.root), "--config", str(path), *args],
            capture_output=True, text=True, timeout=15)

    def test_unregistered_nested_file_fails_then_registration_passes(self):
        (self.root / "tests/nested").mkdir()
        (self.root / "tests/nested/test_zzz.py").touch()
        result = self.run_cli("--check")
        self.assertEqual(result.returncode, 2)
        self.assertIn("unregistered tests: tests/nested/test_zzz.py", result.stderr)
        self.config["groups"]["one"].append("tests/nested/test_zzz.py")
        result = self.run_cli("--check")
        self.assertEqual(result.returncode, 0, result.stderr)
        result = self.run_cli("--group", "one")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("MODULE tests/nested/test_zzz.py: 0 tests", result.stdout)

    def test_bad_configs_fail_closed(self):
        variants = [None, {}, {**self.config, "extra": {}}]
        for change in (
            {"groups": {}}, {"groups": {"one": []}},
            {"groups": {"one": "tests/test_one.py"}},
            {"groups": {"one": ["tests/test_missing.py"]}},
            {"groups": {"one": ["tests/test_one.py", "tests/test_one.py"]}},
            {"groups": {"one": ["tests/../tests/test_one.py"]}},
            {"excluded": {"tests/test_one.py": "duplicate"}},
        ):
            variants.append({**self.config, **change})
        for variant in variants:
            with self.subTest(variant=variant):
                self.assertEqual(self.run_cli("--check", raw=json.dumps(variant)).returncode, 2)
        for raw in ('{', '{"groups":{},"groups":{}}'):
            self.assertEqual(self.run_cli("--check", raw=raw).returncode, 2)
        self.assertEqual(self.run_cli("--group", "missing").returncode, 2)

    def test_exclusion_requires_nonempty_reason(self):
        (self.root / "tests/test_zzz.py").touch()
        for reason in (None, "", " "):
            self.config["excluded"]["tests/test_zzz.py"] = reason
            self.assertEqual(self.run_cli("--check").returncode, 2)
        self.config["excluded"]["tests/test_zzz.py"] = "Fixture only; deliberately not executable."
        self.assertEqual(self.run_cli("--check").returncode, 0)

    def test_indirect_loading_is_verified_and_not_duplicated(self):
        (self.root / "tests/test_extra.py").write_text(
            "import unittest\nclass Extra(unittest.TestCase):\n"
            "    def test_extra(self): pass\n", encoding="utf-8")
        self.config["indirect"]["tests/test_extra.py"] = {
            "via": "tests/test_one.py", "reason": "load_tests hook"}
        result = self.run_cli("--group", "one")
        self.assertEqual(result.returncode, 2)
        self.assertIn("missing indirect", result.stderr)
        with (self.root / "tests/test_one.py").open("a", encoding="utf-8") as stream:
            stream.write("\ndef load_tests(loader, tests, pattern):\n"
                         "    from tests import test_extra\n"
                         "    tests.addTests(loader.loadTestsFromModule(test_extra))\n"
                         "    return tests\n")
        result = self.run_cli("--group", "one")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("MODULE tests/test_extra.py: 1 tests (indirect)", result.stdout)
        self.assertIn("Ran 2 tests", result.stderr)
        self.config["groups"]["one"].append("tests/test_extra.py")
        self.assertEqual(self.run_cli("--check").returncode, 2)
        self.config["indirect"] = {}
        result = self.run_cli("--group", "one")
        self.assertEqual(result.returncode, 2)
        self.assertIn("duplicate loaded tests", result.stderr)
        self.config["groups"]["one"].pop()
        self.config["excluded"]["tests/test_extra.py"] = "Incorrect exclusion"
        self.assertIn("unexpected=", self.run_cli("--group", "one").stderr)

    def test_invalid_indirect_owner_and_reason_fail(self):
        (self.root / "tests/test_extra.py").touch()
        for entry in ({}, {"via": [], "reason": "hook"},
                      {"via": "tests/test_missing.py", "reason": "hook"},
                      {"via": "tests/test_one.py", "reason": ""}):
            self.config["indirect"]["tests/test_extra.py"] = entry
            self.assertEqual(self.run_cli("--check").returncode, 2)

    def test_test_failure_and_import_error_propagate(self):
        path = self.root / "tests/test_one.py"
        path.write_text("import unittest\nclass One(unittest.TestCase):\n"
                        "    def test_failure(self): self.fail('sentinel')\n", encoding="utf-8")
        result = self.run_cli("--group", "one")
        self.assertEqual(result.returncode, 1)
        self.assertIn("sentinel", result.stderr)
        path.write_text("raise RuntimeError('import sentinel')\n", encoding="utf-8")
        result = self.run_cli("--group", "one")
        self.assertEqual(result.returncode, 2)
        self.assertIn("import sentinel", result.stderr)

    def test_repository_registry_and_contextual_coverage(self):
        config = test_groups.validate_registry(test_groups.ROOT, json.loads(
            test_groups.DEFAULT_CONFIG.read_text(encoding="utf-8")))
        script = (test_groups.ROOT / "tools/ci-gates.sh").read_text(encoding="utf-8")
        consumed = [argv[-1] for _, argv in gate_results.CHECKS if "--group" in argv]
        self.assertCountEqual(consumed, config["groups"])
        self.assertNotIn("-m unittest", script)
        groups_by_id = {check_id: argv[-1] for check_id, argv in gate_results.CHECKS if "--group" in argv}
        for path, check_id in gate_results.COVERAGE.items():
            owner = config["indirect"].get(path, {}).get("via", path)
            self.assertIn(owner, config["groups"][groups_by_id[check_id]])
        # Load without running the expensive suite: verify actual hook output and unique IDs.
        with redirect_stdout(io.StringIO()):
            suite = test_groups.load_group(config, "contract-suite")
        cases = list(test_groups.test_cases(suite))
        modules = {type(case).__module__ for case in cases}
        for path in config["indirect"]:
            self.assertIn(path[:-3].replace("/", "."), modules)
        self.assertEqual(len(cases), len({case.id() for case in cases}))


if __name__ == "__main__":
    unittest.main()
