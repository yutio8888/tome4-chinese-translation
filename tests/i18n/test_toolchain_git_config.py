"""Toolchain tests: git config."""

from __future__ import annotations

from tests.i18n import toolchain_fixtures
from tests.i18n.toolchain_fixtures import ROOT, TEST_FIXTURE_BASE, TEST_FIXTURE_ROOT
import sys
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import call, patch
from i18nlib.config import load_manifest
from i18nlib.errors import ConfigurationError
from i18nlib.git_source import GitRepository


class TestFixtureIsolationTests(unittest.TestCase):
    def test_import_in_child_process_uses_distinct_fixture_root(self) -> None:
        sentinel = TEST_FIXTURE_ROOT / "parent-sentinel"
        sentinel.write_text("parent fixture", encoding="utf-8")
        completed = subprocess.run(
            [
                sys.executable,
                "-c",
                (
                    "import json\n"
                    "from tests.i18n import toolchain_fixtures\n"
                    "print(json.dumps({\"fixture_root\": "
                    "str(toolchain_fixtures.TEST_FIXTURE_ROOT)}))\n"
                ),
            ],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
            timeout=30,
        )
        self.assertEqual(
            completed.returncode,
            0,
            msg=f"stdout:\n{completed.stdout}\nstderr:\n{completed.stderr}",
        )
        child_fixture_root = Path(json.loads(completed.stdout)["fixture_root"])
        self.assertTrue(sentinel.is_file())
        self.assertNotEqual(child_fixture_root, TEST_FIXTURE_ROOT)
        self.assertEqual(child_fixture_root.parent, TEST_FIXTURE_BASE)


class GitRepositoryValidationTests(unittest.TestCase):
    commit = "a" * 40
    head = "b" * 40

    def setUp(self) -> None:
        temporary = tempfile.TemporaryDirectory(prefix="git-validation-")
        self.addCleanup(temporary.cleanup)
        self.path = Path(temporary.name).resolve()
        with patch(
            "i18nlib.git_source.shutil.which", return_value="/usr/bin/git"
        ):
            self.repository = GitRepository(self.path)

    @staticmethod
    def _completed(
        returncode: int = 0, *, stdout: str = "", stderr: str = ""
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.CompletedProcess(
            ["git"], returncode, stdout=stdout, stderr=stderr
        )

    def _validation_results(
        self, status: subprocess.CompletedProcess[str] | None = None
    ) -> list[subprocess.CompletedProcess[str]]:
        results = [
            self._completed(stdout=f"{self.path}\n"),
            self._completed(stdout=f"{self.commit}\n"),
            self._completed(stdout=f"{self.head}\n"),
        ]
        if status is not None:
            results.append(status)
        return results

    @classmethod
    def _expected_calls(cls, *, include_status: bool) -> list[object]:
        calls = [
            call(["rev-parse", "--show-toplevel"], text=True),
            call(
                ["rev-parse", "--verify", f"{cls.commit}^{{commit}}"],
                text=True,
            ),
            call(["rev-parse", "--verify", "HEAD"], text=True),
        ]
        if include_status:
            calls.append(
                call(
                    ["status", "--porcelain", "--untracked-files=all"],
                    text=True,
                )
            )
        return calls

    def test_validate_rejects_failed_worktree_status(self) -> None:
        cases = (
            (
                "fatal: cannot read index\n",
                "ignored stdout\n",
                "fatal: cannot read index",
            ),
            (
                "",
                "",
                "git status exited with code 128 without an error message",
            ),
        )
        for stderr, stdout, expected_detail in cases:
            with self.subTest(stderr=stderr):
                status = self._completed(
                    128, stdout=stdout, stderr=stderr
                )
                with patch.object(
                    self.repository,
                    "_run",
                    side_effect=self._validation_results(status),
                ) as run:
                    with self.assertRaises(ConfigurationError) as raised:
                        self.repository.validate(self.commit)

                message = str(raised.exception)
                self.assertIn(str(self.path), message)
                self.assertIn(expected_detail, message)
                if stderr:
                    self.assertNotIn(stdout.strip(), message)
                self.assertEqual(
                    run.call_args_list,
                    self._expected_calls(include_status=True),
                )

    def test_validate_reports_clean_worktree(self) -> None:
        status = self._completed(stdout="")
        with patch.object(
            self.repository,
            "_run",
            side_effect=self._validation_results(status),
        ) as run:
            result = self.repository.validate(self.commit)

        self.assertEqual(result["path"], str(self.path))
        self.assertEqual(result["commit"], self.commit)
        self.assertEqual(result["head"], self.head)
        self.assertIs(result["clean"], True)
        self.assertIs(result["worktree_checked"], True)
        self.assertEqual(
            run.call_args_list, self._expected_calls(include_status=True)
        )

    def test_validate_reports_dirty_worktree(self) -> None:
        status = self._completed(stdout=" M tracked.lua\n?? new.lua\n")
        with patch.object(
            self.repository,
            "_run",
            side_effect=self._validation_results(status),
        ) as run:
            result = self.repository.validate(self.commit)

        self.assertIs(result["clean"], False)
        self.assertIs(result["worktree_checked"], True)
        self.assertEqual(
            run.call_args_list, self._expected_calls(include_status=True)
        )

    def test_validate_skips_worktree_status_when_disabled(self) -> None:
        with patch.object(
            self.repository,
            "_run",
            side_effect=self._validation_results(),
        ) as run:
            result = self.repository.validate(
                self.commit, check_worktree=False
            )

        self.assertIsNone(result["clean"])
        self.assertIs(result["worktree_checked"], False)
        self.assertEqual(
            run.call_args_list, self._expected_calls(include_status=False)
        )


class ManifestTests(unittest.TestCase):
    @staticmethod
    def _manifest_data() -> dict[str, object]:
        path = ROOT / "i18n" / "versions" / "tome-1.7.6.json"
        return json.loads(path.read_text(encoding="utf-8"))

    @staticmethod
    def _load_isolated_manifest(data: dict[str, object]) -> object:
        with tempfile.TemporaryDirectory(prefix="manifest-types-") as temporary:
            path = Path(temporary) / "tome-1.7.6.json"
            path.write_text(json.dumps(data), encoding="utf-8")
            return load_manifest(manifest_path=path)

    @staticmethod
    def _component_data(
        data: dict[str, object], component_id: str
    ) -> dict[str, object]:
        components = data["components"]
        assert isinstance(components, list)
        return next(
            component
            for component in components
            if isinstance(component, dict) and component.get("id") == component_id
        )

    def test_manifest_pins_current_release(self) -> None:
        manifest = load_manifest()
        self.assertEqual(manifest.version, "tome-1.7.6")
        self.assertEqual(
            manifest.repositories["engine"].commit,
            "624a67329fe2ad440c5b344785a9c73fcf22ae63",
        )
        self.assertEqual(manifest.component("tome").translation, "mod-tome.lua")
        self.assertTrue(manifest.component("tome").addon_eligible)
        self.assertFalse(manifest.component("boot").addon_eligible)
        self.assertEqual(
            manifest.protected_source_roots["dlc"].access,
            "lua-extractor-only",
        )
        self.assertEqual(manifest.protected_repositories, frozenset({"engine"}))
        self.assertEqual(
            {
                component.id
                for component in manifest.components
                if component.protected_source is not None
            },
            {"ashes-urhrok", "cults", "orcs"},
        )
        ashes = manifest.component("ashes-urhrok")
        self.assertIsNone(ashes.source_repository)
        self.assertEqual(ashes.sources, ())
        self.assertIsNotNone(ashes.protected_source)
        assert ashes.protected_source is not None
        self.assertEqual(ashes.protected_source.mount, "tome-ashes-urhrok")
        assert ashes.source_baseline is not None
        self.assertEqual(ashes.source_baseline.tdef_count, 999)
        self.assertEqual(
            ashes.source_baseline.kind, "protected-extraction-snapshot"
        )
        self.assertEqual(
            {
                layer.id: layer.status for layer in manifest.release_layers
            },
            {
                "core-addon": "releaseable",
                "dlc-addon": "baseline-pending",
                "legacy-lore-addon": "optional",
                "nullpack-addon": "optional",
            },
        )
        core_layer = next(
            layer for layer in manifest.release_layers if layer.id == "core-addon"
        )
        self.assertEqual(core_layer.components, ("tome",))
        self.assertEqual(core_layer.external_requirements, ())
        dlc_layer = next(
            layer for layer in manifest.release_layers if layer.id == "dlc-addon"
        )
        self.assertEqual(dlc_layer.components, ("ashes-urhrok", "cults", "orcs"))
        for component_id in ("items-vault", "possessors"):
            ignored = manifest.component(component_id)
            self.assertIsNone(ignored.protected_source)
            self.assertFalse(ignored.addon_eligible)
            self.assertTrue((manifest.root / ignored.translation).is_file())

    def test_manifest_integer_fields_reject_json_true(self) -> None:
        cases = (
            (
                "manifest.schema_version",
                lambda data: data.__setitem__("schema_version", True),
            ),
            (
                "extractor.max_stack",
                lambda data: data["extractor"].__setitem__("max_stack", True),
            ),
            (
                "source_baseline.tdef_count",
                lambda data: self._component_data(data, "ashes-urhrok")[
                    "source_baseline"
                ].__setitem__("tdef_count", True),
            ),
        )
        for field, mutate in cases:
            with self.subTest(field=field):
                data = self._manifest_data()
                mutate(data)
                with self.assertRaises(ConfigurationError) as raised:
                    self._load_isolated_manifest(data)
                self.assertIn(field, str(raised.exception))

    def test_manifest_boolean_fields_reject_strings_and_numbers(self) -> None:
        cases = (
            (
                "repositories.engine.required",
                lambda data, value: data["repositories"]["engine"].__setitem__(
                    "required", value
                ),
            ),
            (
                "extractor.preserve_duplicate_occurrences",
                lambda data, value: data["extractor"].__setitem__(
                    "preserve_duplicate_occurrences", value
                ),
            ),
            (
                "extract_by_default",
                lambda data, value: self._component_data(data, "example").__setitem__(
                    "extract_by_default", value
                ),
            ),
            (
                "addon_eligible",
                lambda data, value: self._component_data(data, "example").__setitem__(
                    "addon_eligible", value
                ),
            ),
        )
        for field, mutate in cases:
            for invalid_value in ("false", 0):
                with self.subTest(field=field, value=invalid_value):
                    data = self._manifest_data()
                    mutate(data, invalid_value)
                    with self.assertRaises(ConfigurationError) as raised:
                        self._load_isolated_manifest(data)
                    self.assertIn(field, str(raised.exception))

    def test_manifest_boolean_fields_preserve_json_false(self) -> None:
        data = self._manifest_data()
        data["repositories"]["engine"]["required"] = False
        data["extractor"]["preserve_duplicate_occurrences"] = False
        tome = self._component_data(data, "tome")
        tome["extract_by_default"] = False
        boot = self._component_data(data, "boot")
        boot["addon_eligible"] = False

        manifest = self._load_isolated_manifest(data)

        self.assertFalse(manifest.repositories["engine"].required)
        self.assertFalse(manifest.extractor.preserve_duplicate_occurrences)
        self.assertFalse(manifest.component("tome").extract_by_default)
        self.assertFalse(manifest.component("boot").addon_eligible)

    def test_pinned_official_locale_is_a_regular_blob(self) -> None:
        manifest = load_manifest()
        repository = GitRepository(manifest.repository_path("engine"))
        component = manifest.component("boot")
        assert component.official_locale is not None
        data = repository.read_blob(
            manifest.repositories["engine"].commit,
            component.official_locale,
        )
        self.assertTrue(data.startswith(b'locale "zh_hans"'))


class ScopedGitTests(unittest.TestCase):
    def test_real_scans_are_literal_scoped_and_optional(self):
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            def git(*args):
                return subprocess.check_output(["git", "-C", temporary, *args], stderr=subprocess.PIPE).decode().strip()
            git("init")
            for directory in ("public", "outside", "wild*", "wild-other", ":(glob)**", "bracket[ab]", "bracketa"):
                (root / directory).mkdir()
                (root / directory / "file").write_text("base")
            git("add", ".")
            git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid", "commit", "-m", "base")
            commit = git("rev-parse", "HEAD")
            repo = GitRepository(root)
            self.assertTrue(repo.validate(commit, scan_allowlist=["public"])["clean"])
            (root / "outside/file").write_text("dirty")
            (root / "outside/new").write_text("new")
            self.assertTrue(repo.validate(commit, scan_allowlist=["public"])["clean"])
            self.assertFalse(repo.validate(commit)["clean"])
            self.assertFalse(repo.validate(commit, scan_allowlist=["."])["clean"])
            with patch.object(repo, "_run", wraps=repo._run) as run:
                empty = repo.validate(commit, scan_allowlist=[])
                self.assertIsNone(empty["clean"])
                self.assertFalse(empty["worktree_checked"])
                self.assertFalse(any(c.args[0][0] == "status" for c in run.call_args_list))
            for directory, sibling in (("wild*", "wild-other"), ("bracket[ab]", "bracketa"), (":(glob)**", "outside")):
                (root / sibling / "file").write_text("dirty")
                self.assertTrue(repo.validate(commit, scan_allowlist=[directory])["clean"])
                (root / directory / "new").write_text("new")
                self.assertFalse(repo.validate(commit, scan_allowlist=[directory])["clean"])
            (root / "public/new").write_text("new")
            self.assertFalse(repo.validate(commit, scan_allowlist=["public"])["clean"])
            (root / "public/new").unlink()
            (root / "public/file").write_text("dirty")
            self.assertFalse(repo.validate(commit, scan_allowlist=["public"])["clean"])
            git("add", "public/file")
            self.assertFalse(repo.validate(commit, scan_allowlist=["public"])["clean"])
            original = repo._run
            def fail_status(args, **kwargs):
                if args[0] == "status":
                    return subprocess.CompletedProcess(args, 1, "", "status failure")
                return original(args, **kwargs)
            with patch.object(repo, "_run", side_effect=fail_status):
                with self.assertRaisesRegex(ConfigurationError, "status failure"):
                    repo.validate(commit, scan_allowlist=["public"])
            with self.assertRaises(ConfigurationError):
                repo.validate("f" * 40, scan_allowlist=[])


class SourceAttributesTests(unittest.TestCase):
    _manifest_data = staticmethod(ManifestTests._manifest_data)
    _load_isolated_manifest = staticmethod(ManifestTests._load_isolated_manifest)
    _component_data = staticmethod(ManifestTests._component_data)
    def test_independent_real_attributes_and_legacy_defaults(self):
        manifest = load_manifest()
        for name, spec in manifest.repositories.items():
            self.assertEqual((spec.visibility, spec.extraction_mode, spec.source_pinning), ("public", "full-tree", "pinned"))
        self.assertEqual(manifest.repositories["addon"].scan_allowlist, (".",))
        expected = sorted({m.git_path for c in manifest.components if c.source_repository == "engine" for m in c.sources} | {manifest.extractor.git_path})
        self.assertEqual(list(manifest.repositories["engine"].scan_allowlist), expected)
        data = self._manifest_data()
        for component in data["components"]:
            if "protected_source" in component:
                source = manifest.component(component["id"]).protected_source
                self.assertEqual((source.visibility, source.extraction_mode, source.source_pinning, source.scan_allowlist), ("public", "lua-extractor-only", "unpinned", ()))
                for key in ("visibility", "extraction_mode", "source_pinning", "scan_allowlist"):
                    del component["protected_source"][key]
        for spec in data["repositories"].values():
            for key in ("visibility", "extraction_mode", "source_pinning", "scan_allowlist"):
                del spec[key]
        legacy = self._load_isolated_manifest(data)
        self.assertEqual(legacy.repositories["engine"].scan_allowlist, (".",))
        self.assertEqual(legacy.component("orcs").protected_source.visibility, "protected")
        self.assertEqual(legacy.component("orcs").protected_source.source_pinning, "unpinned")

    def test_invalid_attributes_and_paths(self):
        cases = [(key, bad) for key in ("visibility", "extraction_mode", "source_pinning") for bad in (None, True, [], {}, "invalid")]
        cases += [("scan_allowlist", bad) for bad in (None, "public", True, [None], [""], ["/public"], ["../public"], ["public/../x"], ["./public"], ["public//x"], ["public/"], ["public/./x"], ["C:/x"], ["x\\y"], ["x\0y"], [".", "public"], ["public", "public"])]
        for key, bad in cases:
            for broker in (False, True):
                with self.subTest(key=key, bad=bad, broker=broker):
                    data = self._manifest_data()
                    spec = self._component_data(data, "orcs")["protected_source"] if broker else data["repositories"]["engine"]
                    spec[key] = bad
                    with self.assertRaises(ConfigurationError):
                        self._load_isolated_manifest(data)
        from i18nlib.config import scan_paths
        self.assertEqual(scan_paths(["wild*", ":(glob)**", "bracket[ab]"], "paths"), ("wild*", ":(glob)**", "bracket[ab]"))
        for key, value in (("source_pinning", "pinned"), ("extraction_mode", "full-tree"), ("scan_allowlist", ["."])):
            data = self._manifest_data()
            self._component_data(data, "orcs")["protected_source"][key] = value
            with self.assertRaises(ConfigurationError):
                self._load_isolated_manifest(data)


if __name__ == "__main__":
    unittest.main()
