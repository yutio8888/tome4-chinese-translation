"""Toolchain tests: doctor."""

from __future__ import annotations

from tests.i18n import toolchain_fixtures
import contextlib
from dataclasses import replace
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from i18nlib.config import load_manifest
from i18nlib.cli import main as cli_main
from i18nlib.errors import ValidationError


class DoctorTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.base_manifest = load_manifest()

    @classmethod
    def _manifest(cls, root: Path, copy_fragment: str) -> object:
        component = replace(
            cls.base_manifest.component("ashes-urhrok"),
            translation="canonical.lua",
            copy_fragment=copy_fragment,
        )
        return replace(
            cls.base_manifest,
            root=root,
            components=(component,),
            manual_definitions=("manual.lua",),
            terminology="terminology.tsv",
            policy="policy.json",
        )

    @staticmethod
    def _write_files(root: Path, *relative_paths: str) -> None:
        for relative_path in relative_paths:
            path = root / relative_path
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("-- fixture\n", encoding="utf-8")

    def test_missing_copy_fragment_fails_before_expensive_checks(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tome4-doctor-missing-") as temporary:
            root = Path(temporary)
            manifest = self._manifest(root, "fragment.lua")
            self._write_files(
                root,
                "terminology.tsv",
                "policy.json",
                "canonical.lua",
                "manual.lua",
            )
            stdout = io.StringIO()
            stderr = io.StringIO()

            with (
                patch("i18nlib.cli_doctor._manifest", return_value=manifest),
                patch("i18nlib.cli_doctor.LuaRuntime") as runtime_class,
                patch("i18nlib.cli_doctor.GitRepository") as repository_class,
                patch("i18nlib.cli_doctor.probe_protected_component") as protected_probe,
                contextlib.redirect_stdout(stdout),
                contextlib.redirect_stderr(stderr),
            ):
                exit_code = cli_main(["doctor"])

        self.assertEqual(exit_code, ValidationError.exit_code)
        self.assertEqual(stdout.getvalue(), "")
        self.assertIn(f"missing: {root / 'fragment.lua'}", stderr.getvalue())
        self.assertNotIn("not regular files:", stderr.getvalue())
        runtime_class.assert_not_called()
        repository_class.assert_not_called()
        protected_probe.assert_not_called()

    def test_missing_and_non_file_paths_are_reported_separately(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tome4-doctor-non-file-") as temporary:
            root = Path(temporary)
            manifest = self._manifest(root, "fragment.lua")
            self._write_files(
                root,
                "terminology.tsv",
                "canonical.lua",
                "manual.lua",
            )
            (root / "fragment.lua").mkdir()
            stderr = io.StringIO()

            with (
                patch("i18nlib.cli_doctor._manifest", return_value=manifest),
                patch("i18nlib.cli_doctor.LuaRuntime") as runtime_class,
                patch("i18nlib.cli_doctor.GitRepository") as repository_class,
                patch("i18nlib.cli_doctor.probe_protected_component") as protected_probe,
                contextlib.redirect_stdout(io.StringIO()),
                contextlib.redirect_stderr(stderr),
            ):
                exit_code = cli_main(["doctor"])

        self.assertEqual(exit_code, ValidationError.exit_code)
        self.assertEqual(
            stderr.getvalue(),
            "ERROR: required localization files are invalid: "
            f"missing: {root / 'policy.json'}; "
            f"not regular files: {root / 'fragment.lua'}\n",
        )
        runtime_class.assert_not_called()
        repository_class.assert_not_called()
        protected_probe.assert_not_called()

    def test_declared_copy_fragment_allows_normal_doctor_checks(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tome4-doctor-valid-") as temporary:
            root = Path(temporary)
            manifest = self._manifest(root, "fragment.lua")
            self._write_files(
                root,
                "terminology.tsv",
                "policy.json",
                "canonical.lua",
                "fragment.lua",
                "manual.lua",
            )
            stdout = io.StringIO()
            stderr = io.StringIO()

            with (
                patch("i18nlib.cli_doctor._manifest", return_value=manifest),
                patch("i18nlib.cli_doctor.LuaRuntime") as runtime_class,
                patch("i18nlib.cli_doctor.GitRepository") as repository_class,
                patch(
                    "i18nlib.cli_doctor.probe_protected_component", return_value=True
                ) as protected_probe,
                contextlib.redirect_stdout(stdout),
                contextlib.redirect_stderr(stderr),
            ):
                runtime = runtime_class.return_value
                runtime.doctor.return_value = {
                    "lua_version": "Lua 5.1",
                    "luajit_version": "LuaJIT fixture",
                    "lpeg_rock_version": "0.10.2-1",
                    "lpeg_runtime_version": "0.10",
                }
                repository_class.return_value.validate.return_value = {
                    "path": "/fixture/repository",
                    "clean": True,
                }
                exit_code = cli_main(["doctor", "--json"])

        self.assertEqual(exit_code, 0)
        self.assertEqual(stderr.getvalue(), "")
        self.assertTrue(json.loads(stdout.getvalue())["ok"])
        runtime.doctor.assert_called_once_with()
        repository_class.return_value.validate.assert_called()
        protected_probe.assert_called_once_with(
            manifest, runtime, manifest.components[0]
        )


    def test_attributes_scans_and_all_dlc_availability_combinations(self):
        import itertools
        for availability in itertools.product((False, True), repeat=3):
            for as_json in (False, True):
                with self.subTest(availability=availability, json=as_json), tempfile.TemporaryDirectory() as temporary:
                    root = Path(temporary)
                    components = tuple(replace(self.base_manifest.component(name), translation="canonical.lua", copy_fragment=None) for name in ("ashes-urhrok", "cults", "orcs"))
                    repositories = {name: replace(spec, env="P6_UNUSED_FIXTURE_" + name, default=str(root / name)) for name, spec in self.base_manifest.repositories.items()}
                    (root / "engine").mkdir()
                    manifest = replace(self._manifest(root, "unused"), components=components, repositories=repositories)
                    self._write_files(root, "canonical.lua", "terminology.tsv", "manual.lua", "policy.json")
                    stdout = io.StringIO()
                    with patch("i18nlib.cli_doctor._manifest", return_value=manifest), patch("i18nlib.cli_doctor.LuaRuntime") as runtime, patch("i18nlib.cli_doctor.GitRepository") as repository, patch("i18nlib.cli_doctor.probe_protected_component", side_effect=availability), contextlib.redirect_stdout(stdout):
                        runtime.return_value.doctor.return_value = dict(lua_version="Lua 5.1", luajit_version="fixture", lpeg_rock_version="0.10.2-1", lpeg_runtime_version="0.10")
                        repository.return_value.validate.side_effect = lambda *args, **kwargs: dict(path="fixture", clean=False)
                        self.assertEqual(cli_main(["doctor"] + (["--json"] if as_json else [])), 0)
                    from unittest.mock import call
                    self.assertEqual(repository.return_value.validate.call_args_list, [call(repositories["engine"].commit, scan_allowlist=repositories["engine"].scan_allowlist), call(manifest.extractor.commit, check_worktree=False)])
                    output = stdout.getvalue()
                    self.assertNotIn("contains a protected source", output)
                    self.assertNotIn("declared protected source", output)
                    self.assertIn("repository has worktree changes", output)
                    self.assertIn("optional repository is absent", output)
                    for name in ("ashes-urhrok", "cults", "orcs"):
                        self.assertIn("source-unpinned: " + name, output)
                    if as_json:
                        report = json.loads(output)
                        for name, spec in repositories.items():
                            row = report["repositories"][name]
                            self.assertEqual(row["available"], name == "engine")
                            self.assertEqual([row[k] for k in ("visibility", "extraction_mode", "source_pinning", "scan_allowlist")], [spec.visibility, spec.extraction_mode, spec.source_pinning, list(spec.scan_allowlist)])
                        for component, available in zip(components, availability):
                            row = report["protected_sources"][component.id]
                            self.assertEqual(row, dict(available=available, access="lua-extractor-only", visibility="public", extraction_mode="lua-extractor-only", source_pinning="unpinned", scan_allowlist=[]))
                    else:
                        self.assertIn("visibility=public extraction_mode=full-tree source_pinning=pinned", output)
                        self.assertEqual(output.count("visibility=public extraction_mode=lua-extractor-only source_pinning=unpinned scan_allowlist=[]"), 3)


if __name__ == "__main__":
    unittest.main()
