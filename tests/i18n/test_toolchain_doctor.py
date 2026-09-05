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


if __name__ == "__main__":
    unittest.main()
