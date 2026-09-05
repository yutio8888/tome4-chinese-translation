"""Toolchain tests: build."""

from __future__ import annotations

from tests.i18n import toolchain_fixtures
from tests.i18n.toolchain_fixtures import _component_selection_document
import contextlib
from dataclasses import replace
import io
import os
import stat
import subprocess
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, call, patch
import smoke_release
from i18nlib.config import load_manifest
from i18nlib.build import build_addon_locale, build_full_locales
from i18nlib.errors import ValidationError
from i18nlib.locale_model import LocaleDocument, LocaleLoader
from i18nlib.quality import build_report
from i18nlib.runtime import LuaRuntime


class BuildApiComponentDeduplicationTests(unittest.TestCase):
    def _assert_full_output_preflight_failure(
        self,
        selected: list[object],
        expected_message: str,
    ) -> None:
        manifest = SimpleNamespace(root=Path("/fixture"), version="fixture")
        loader = Mock(spec=LocaleLoader)
        with (
            patch("i18nlib.build.create_run_directory") as create_run_directory,
            patch("i18nlib.build._compose_full_locale") as compose,
            patch("i18nlib.build._assert_same_semantics") as compare,
            patch("i18nlib.build.atomic_write_bytes") as write_bytes,
            patch("i18nlib.build.write_json") as write_json,
        ):
            with self.assertRaises(ValidationError) as raised:
                build_full_locales(manifest, loader, selected)

        self.assertEqual(str(raised.exception), expected_message)
        self.assertEqual(loader.mock_calls, [])
        create_run_directory.assert_not_called()
        compose.assert_not_called()
        compare.assert_not_called()
        write_bytes.assert_not_called()
        write_json.assert_not_called()

    def test_full_build_empty_selection_retains_existing_preflight_error(
        self,
    ) -> None:
        manifest = SimpleNamespace(root=Path("/fixture"), version="fixture")
        loader = Mock(spec=LocaleLoader)
        with (
            patch("i18nlib.build.create_run_directory") as create_run_directory,
            patch("i18nlib.build._compose_full_locale") as compose,
            patch("i18nlib.build.atomic_write_bytes") as write_bytes,
            patch("i18nlib.build.write_json") as write_json,
        ):
            with self.assertRaisesRegex(
                ValidationError, r"^no full-locale components selected$"
            ):
                build_full_locales(manifest, loader, [])

        self.assertEqual(loader.mock_calls, [])
        create_run_directory.assert_not_called()
        compose.assert_not_called()
        write_bytes.assert_not_called()
        write_json.assert_not_called()

    def test_full_build_invalid_component_fails_before_runtime_and_io(
        self,
    ) -> None:
        valid = SimpleNamespace(
            id="valid",
            translation="valid.lua",
            copy_fragment=None,
            full_output="shared-output.lua",
        )
        conflicting = SimpleNamespace(
            id="conflicting",
            translation="conflicting.lua",
            copy_fragment=None,
            full_output="shared-output.lua",
        )
        invalid = SimpleNamespace(
            id="invalid",
            translation="invalid.lua",
            copy_fragment=None,
            full_output=None,
        )
        manifest = SimpleNamespace(root=Path("/fixture"), version="fixture")
        for selected in (
            [invalid, valid, conflicting],
            [valid, conflicting, invalid],
        ):
            with self.subTest(components=[component.id for component in selected]):
                loader = Mock(spec=LocaleLoader)
                with (
                    patch(
                        "i18nlib.build.create_run_directory"
                    ) as create_run_directory,
                    patch("i18nlib.build._compose_full_locale") as compose,
                    patch(
                        "i18nlib.build._assert_same_semantics"
                    ) as compare,
                    patch("i18nlib.build.atomic_write_bytes") as write_bytes,
                    patch("i18nlib.build.write_json") as write_json,
                ):
                    with self.assertRaisesRegex(
                        ValidationError,
                        r"component 'invalid' has no full_output mapping",
                    ):
                        build_full_locales(manifest, loader, selected)

                self.assertEqual(loader.mock_calls, [])
                create_run_directory.assert_not_called()
                compose.assert_not_called()
                compare.assert_not_called()
                write_bytes.assert_not_called()
                write_json.assert_not_called()

    def test_full_build_rejects_exact_output_collision_before_runtime_and_io(
        self,
    ) -> None:
        alpha = SimpleNamespace(id="alpha", full_output="shared.lua")
        beta = SimpleNamespace(id="beta", full_output="shared.lua")
        expected = (
            "full_output collision (exact duplicate output path): "
            "component 'alpha' maps to 'shared.lua'; "
            "component 'beta' maps to 'shared.lua'"
        )
        for selected in ([alpha, beta], [beta, alpha]):
            with self.subTest(components=[component.id for component in selected]):
                self._assert_full_output_preflight_failure(selected, expected)

    def test_full_build_rejects_ancestor_output_collision_before_runtime_and_io(
        self,
    ) -> None:
        parent = SimpleNamespace(id="parent", full_output="locales")
        child = SimpleNamespace(id="child", full_output="locales/zh_hans.lua")
        expected = (
            "full_output collision (ancestor/descendant output paths): "
            "component 'parent' maps to 'locales'; "
            "component 'child' maps to 'locales/zh_hans.lua'"
        )
        for selected in ([parent, child], [child, parent]):
            with self.subTest(components=[component.id for component in selected]):
                self._assert_full_output_preflight_failure(selected, expected)

    def test_full_build_performs_component_work_once_in_first_seen_order(
        self,
    ) -> None:
        second = SimpleNamespace(
            id="second",
            translation="second.lua",
            copy_fragment=None,
            full_output="second-output.lua",
        )
        first = SimpleNamespace(
            id="first",
            translation="first.lua",
            copy_fragment=None,
            full_output="first-output.lua",
        )
        duplicate_second = SimpleNamespace(
            id="second",
            translation="duplicate-second.lua",
            copy_fragment=None,
            full_output="first-output.lua",
        )
        manifest = SimpleNamespace(root=Path("/fixture"), version="fixture")
        loader = Mock(spec=LocaleLoader)
        loader.load_path.side_effect = (
            lambda path, *, logical_path: _component_selection_document(
                logical_path, logical_path
            )
        )
        loader.load_bytes.return_value = _component_selection_document("generated")
        run_directory = Path("/artifacts/build-full")

        with (
            patch(
                "i18nlib.build._compose_full_locale",
                side_effect=lambda _manifest, component: component.id.encode(),
            ) as compose,
            patch("i18nlib.build._assert_same_semantics") as compare,
            patch(
                "i18nlib.build.create_run_directory",
                return_value=run_directory,
            ) as create_run_directory,
            patch("i18nlib.build.atomic_write_bytes") as write_bytes,
            patch("i18nlib.build.write_json") as write_json,
        ):
            report = build_full_locales(
                manifest,
                loader,
                [second, first, duplicate_second, first],
            )

        self.assertEqual(
            [item["component"] for item in report["components"]],
            ["second", "first"],
        )
        self.assertEqual(
            loader.load_path.call_args_list,
            [
                call(Path("/fixture/second.lua"), logical_path="second.lua"),
                call(Path("/fixture/first.lua"), logical_path="first.lua"),
            ],
        )
        self.assertEqual(loader.load_bytes.call_count, 2)
        self.assertEqual(
            [args.args[1] for args in compose.call_args_list],
            [second, first],
        )
        self.assertEqual(compare.call_count, 2)
        create_run_directory.assert_called_once_with(
            Path("/fixture"), "build-full"
        )
        self.assertEqual(
            write_bytes.call_args_list,
            [
                call(
                    run_directory / "full" / "second-output.lua",
                    b"second",
                ),
                call(
                    run_directory / "full" / "first-output.lua",
                    b"first",
                ),
            ],
        )
        write_json.assert_called_once_with(run_directory / "build.json", report)

    def test_addon_build_performs_component_work_once_and_does_not_inflate_stats(
        self,
    ) -> None:
        def component(component_id: str, translation: str | None = None) -> object:
            return SimpleNamespace(
                id=component_id,
                addon_eligible=True,
                source_repository="engine",
                official_locale=f"official-{component_id}.lua",
                translation=translation or f"{component_id}.lua",
                copy_fragment=None,
            )

        second = component("second")
        first = component("first")
        duplicate_second = component("second", "duplicate-second.lua")
        repository_path = Mock(return_value=Path("/repository"))
        manifest = SimpleNamespace(
            root=Path("/fixture"),
            version="fixture",
            locale="zh_hans",
            repositories={"engine": SimpleNamespace(commit="a" * 40)},
            repository_path=repository_path,
            addon_external_requirements=(),
        )
        canonical = {
            "second.lua": _component_selection_document(
                "second.lua", "source second"
            ),
            "first.lua": _component_selection_document(
                "first.lua", "source first"
            ),
        }
        loader = Mock(spec=LocaleLoader)
        loader.load_path.side_effect = (
            lambda path, *, logical_path: canonical[logical_path]
        )
        loader.load_bytes.side_effect = (
            lambda data, *, logical_path: _component_selection_document(logical_path)
        )
        run_directory = Path("/artifacts/build-addon")
        verification = {
            "expected_runtime_keys": 2,
            "patch_runtime_keys": 2,
            "missing": 0,
            "unexpected": 0,
            "mismatched": 0,
            "redundant": 0,
        }

        with (
            patch("i18nlib.build.GitRepository") as repository,
            patch(
                "i18nlib.build._render_addon_locale", return_value=b"addon"
            ) as render,
            patch(
                "i18nlib.build._verify_overlay", return_value=verification
            ) as verify,
            patch(
                "i18nlib.build.create_run_directory",
                return_value=run_directory,
            ) as create_run_directory,
            patch("i18nlib.build.atomic_write_bytes") as write_bytes,
            patch("i18nlib.build.write_json") as write_json,
        ):
            repository.return_value.read_blob.side_effect = [
                b"official second",
                b"official first",
            ]
            report = build_addon_locale(
                manifest,
                loader,
                [second, first, duplicate_second, first],
                include_external_requirements=False,
            )

        self.assertEqual(
            [item["component"] for item in report["components"]],
            ["second", "first"],
        )
        self.assertEqual(report["new_entries"], 2)
        self.assertEqual(report["override_entries"], 0)
        self.assertEqual(report["inherited_entries"], 0)
        self.assertEqual(len(report["delta_entries"]), 2)
        self.assertEqual(repository.call_count, 2)
        self.assertEqual(repository.return_value.read_blob.call_count, 2)
        self.assertEqual(repository_path.call_count, 2)
        self.assertEqual(
            loader.load_path.call_args_list,
            [
                call(Path("/fixture/second.lua"), logical_path="second.lua"),
                call(Path("/fixture/first.lua"), logical_path="first.lua"),
            ],
        )
        self.assertEqual(loader.load_bytes.call_count, 3)
        render.assert_called_once()
        verify.assert_called_once()
        create_run_directory.assert_called_once_with(
            Path("/fixture"), "build-addon"
        )
        write_bytes.assert_called_once_with(
            run_directory / "addon" / "data" / "locales" / "zh_hans.lua",
            b"addon",
        )
        write_json.assert_called_once_with(run_directory / "build.json", report)


class BuildSemanticComparisonTests(unittest.TestCase):
    @staticmethod
    def _document(special: object) -> LocaleDocument:
        return LocaleDocument(
            logical_path="fixture.lua",
            sha256="a" * 64,
            records=(
                {
                    "kind": "translation",
                    "source": "fixture source",
                    "source_tag": None,
                    "target": "fixture target",
                    "args_order": None,
                    "special": special,
                },
            ),
        )

    def test_build_comparison_rejects_bool_int_but_accepts_reordered_objects(
        self,
    ) -> None:
        from i18nlib.build import _assert_same_semantics

        expected = self._document(
            {"outer": {"enabled": True, "values": [1, {"wrapped": False}]}}
        )
        equivalent = self._document(
            {"outer": {"values": [1, {"wrapped": False}], "enabled": True}}
        )
        _assert_same_semantics([expected], equivalent, label="fixture")

        type_drift = self._document(
            {"outer": {"values": [1, {"wrapped": 0}], "enabled": True}}
        )
        with self.assertRaisesRegex(ValidationError, "changed 1 translation values"):
            _assert_same_semantics([expected], type_drift, label="fixture")

    def test_overlay_bool_int_override_is_not_redundant(self) -> None:
        from i18nlib.build import _verify_overlay

        official = self._document({"enabled": True})
        canonical = self._document({"enabled": 1})
        patch_document = self._document({"enabled": 1})

        verification = _verify_overlay(
            [official],
            [canonical],
            patch_document,
        )
        self.assertEqual(verification["mismatched"], 0)
        self.assertEqual(verification["redundant"], 0)
        self.assertEqual(verification["patch_runtime_keys"], 1)


class StatusTests(unittest.TestCase):
    @staticmethod
    def _document(*entries: dict[str, object]) -> LocaleDocument:
        return LocaleDocument(
            logical_path="fixture.lua",
            sha256="a" * 64,
            records=tuple(
                {
                    "kind": "translation",
                    "source_tag": None,
                    "target": "fixture target",
                    "args_order": None,
                    **entry,
                }
                for entry in entries
            ),
        )

    def test_status_counts_nested_bool_int_drift_as_changed(self) -> None:
        from i18nlib.status import status_report

        canonical = self._document(
            {
                "source": "deep equivalent",
                "special": {"outer": {"enabled": True, "count": 1}},
            },
            {"source": "type drift", "special": {"enabled": True}},
        )
        official = self._document(
            {
                "source": "deep equivalent",
                "special": {"outer": {"count": 1, "enabled": True}},
            },
            {"source": "type drift", "special": {"enabled": 1}},
        )
        component = Mock(
            id="fixture",
            translation="fixture.lua",
            source_repository="engine",
            official_locale="official.lua",
        )
        manifest = Mock(
            version="fixture-version",
            root=Path("/fixture"),
            repositories={"engine": Mock(commit="a" * 40)},
        )
        manifest.repository_path.return_value = Path("/unused")
        loader = Mock(spec=LocaleLoader)
        loader.load_path.return_value = canonical
        loader.load_bytes.return_value = official

        with patch("i18nlib.status.GitRepository") as repository:
            repository.return_value.read_blob.return_value = b"official"
            report = status_report(manifest, loader, [component])

        counts = report["components"][0]
        self.assertEqual(counts["identical"], 1)
        self.assertEqual(counts["changed"], 1)
        self.assertEqual(report["totals"]["changed"], 1)


class AddonBuildTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = load_manifest()
        cls.runtime = LuaRuntime(cls.manifest)
        cls.runtime.doctor()
        cls.loader = LocaleLoader(cls.runtime)

    def test_noneligible_selections_fail_before_build_operations(self) -> None:
        eligible = self.manifest.component("tome")
        noneligible = self.manifest.component("boot")
        cases = (
            ("mixed", [eligible, noneligible]),
            ("only noneligible", [noneligible]),
        )
        for label, components in cases:
            with self.subTest(selection=label):
                loader = Mock(spec=LocaleLoader)
                with (
                    patch("i18nlib.build.GitRepository") as repository,
                    patch("i18nlib.build._render_addon_locale") as render,
                    patch(
                        "i18nlib.build.create_run_directory"
                    ) as create_run_directory,
                    patch("i18nlib.build.atomic_write_bytes") as write_bytes,
                    patch("i18nlib.build.write_json") as write_json,
                ):
                    with self.assertRaisesRegex(
                        ValidationError,
                        r"addon build requires addon-eligible components; "
                        r"not eligible: boot$",
                    ):
                        build_addon_locale(
                            self.manifest,
                            loader,
                            components,
                            include_external_requirements=False,
                        )

                self.assertEqual(loader.mock_calls, [])
                repository.assert_not_called()
                render.assert_not_called()
                create_run_directory.assert_not_called()
                write_bytes.assert_not_called()
                write_json.assert_not_called()

    def test_explicit_core_build_omits_inherited_translations(self) -> None:
        report = build_addon_locale(
            self.manifest,
            self.loader,
            [self.manifest.component("tome")],
            include_external_requirements=False,
        )
        self.assertTrue(report["complete"])
        self.assertEqual(report["skipped"], [])
        self.assertFalse(report["external_requirements_included"])
        component = report["components"][0]
        self.assertGreater(component["inherited_entries"], 0)
        self.assertGreater(component["delta_entries"], 0)
        self.assertLess(
            component["delta_entries"], component["canonical_runtime_keys"]
        )
        self.assertEqual(
            component["override_entries"] + component["new_entries"],
            component["delta_entries"],
        )
        self.assertEqual(
            report["verification"]["patch_runtime_keys"],
            component["delta_entries"],
        )

    def test_publish_dry_run_does_not_touch_release_repository(self) -> None:
        from i18nlib.publish import publish_addon

        addon_root = self.manifest.repository_path("addon")
        locale_file = addon_root / "data" / "locales" / "zh_hans.lua"
        before = locale_file.read_bytes() if locale_file.is_file() else None
        report = publish_addon(
            self.manifest,
            self.loader,
            apply=False,
            bump=False,
            commit=False,
        )
        self.assertFalse(report["applied"])
        self.assertTrue(report["new_entries"] > 0)
        after = locale_file.read_bytes() if locale_file.is_file() else None
        self.assertEqual(before, after)

    def test_publish_bump_version_regex(self) -> None:
        from i18nlib.publish import _bump_init_version

        text = 'addon_version = {0,2,0}\n'
        updated, version = _bump_init_version(text)
        self.assertEqual(updated, "addon_version = {0,2,1}\n")
        self.assertEqual(version, "0.2.1")

    def test_publish_dlc_entries_are_official_disjoint(self) -> None:
        from i18nlib.publish import _dlc_overlay_entries, _official_locale_keys

        official = _official_locale_keys(self.manifest, self.loader)
        entries = _dlc_overlay_entries(self.manifest, self.loader, official)
        self.assertGreater(len(entries), 0)
        keys = {(e["source"], e["source_tag"]) for e in entries}
        self.assertTrue(
            keys.isdisjoint(official),
            "DLC overlay entries must not shadow official locale keys",
        )
        for component_id in ("ashes-urhrok", "cults", "orcs"):
            count = sum(1 for e in entries if e.get("section") == component_id)
            self.assertGreater(count, 0, f"no overlay entries for {component_id}")

    def test_publish_dry_run_reports_dlc_merge(self) -> None:
        from i18nlib.publish import publish_addon

        report = publish_addon(
            self.manifest,
            self.loader,
            apply=False,
            bump=False,
            commit=False,
        )
        self.assertGreater(report["dlc_entries"], 0)
        self.assertEqual(
            report["new_entries"],
            report["delta_runtime_keys"] + report["dlc_entries"],
        )
        for component_id in ("ashes-urhrok", "cults", "orcs"):
            self.assertGreater(report["dlc_entries_by_component"][component_id], 0)

    def test_publish_commit_rejects_staged_target_before_build_or_loader(
        self,
    ) -> None:
        import i18nlib.publish as publish_module

        cases = (
            ("committed locale", False, "data/locales/zh_hans.lua", True),
            ("committed init", True, "init.lua", True),
            ("initial repository", False, "data/locales/zh_hans.lua", False),
        )
        for label, bump, staged_relative, commit_baseline in cases:
            with self.subTest(case=label), tempfile.TemporaryDirectory(
                prefix="tome4-publish-staged-target-"
            ) as temporary:
                manifest, locale_path, init_path, _ = self._isolated_publish_fixture(
                    Path(temporary),
                    commit_baseline=commit_baseline,
                )
                addon_root = locale_path.parents[2]
                staged_path = addon_root / staged_relative
                original_files = {
                    locale_path: locale_path.read_bytes(),
                    init_path: init_path.read_bytes(),
                }
                staged_path.write_bytes(
                    original_files[staged_path] + b"-- staged user content\n"
                )
                self._git(addon_root, "add", "--", staged_relative)
                staged_path.write_bytes(original_files[staged_path])

                index_before = self._git(addon_root, "write-tree").stdout
                index_entries_before = self._git(
                    addon_root,
                    "ls-files",
                    "--stage",
                ).stdout
                status_before = self._git(
                    addon_root,
                    "status",
                    "--porcelain=v1",
                ).stdout
                head_before = self._git(
                    addon_root,
                    "rev-parse",
                    "--verify",
                    "HEAD",
                    check=False,
                )
                loader = Mock(spec=LocaleLoader)

                with (
                    patch.dict(
                        os.environ,
                        {"TOME4_PUBLISH_TEST_ADDON_ROOT": str(addon_root)},
                    ),
                    patch.object(publish_module, "build_addon_locale") as build,
                    patch.object(
                        publish_module, "_official_locale_keys"
                    ) as official_keys,
                    patch.object(
                        publish_module, "_dlc_overlay_entries"
                    ) as dlc_entries,
                    patch.object(publish_module, "_render_addon_locale") as renderer,
                ):
                    with self.assertRaisesRegex(
                        ValidationError,
                        r"release git staged-state preflight refused:.*"
                        r"staged changes relative to HEAD",
                    ):
                        publish_module.publish_addon(
                            manifest,
                            loader,
                            apply=True,
                            bump=bump,
                            commit=True,
                        )

                build.assert_not_called()
                official_keys.assert_not_called()
                dlc_entries.assert_not_called()
                renderer.assert_not_called()
                self.assertEqual(loader.mock_calls, [])
                self.assertEqual(
                    {path: path.read_bytes() for path in original_files},
                    original_files,
                )
                self.assertEqual(
                    self._git(addon_root, "write-tree").stdout,
                    index_before,
                )
                self.assertEqual(
                    self._git(addon_root, "ls-files", "--stage").stdout,
                    index_entries_before,
                )
                self.assertEqual(
                    self._git(addon_root, "status", "--porcelain=v1").stdout,
                    status_before,
                )
                head_after = self._git(
                    addon_root,
                    "rev-parse",
                    "--verify",
                    "HEAD",
                    check=False,
                )
                self.assertEqual(head_after.returncode, head_before.returncode)
                self.assertEqual(head_after.stdout, head_before.stdout)
                self.assertEqual(head_after.stderr, head_before.stderr)

    def test_publish_git_preflight_failures_are_controlled_before_build(
        self,
    ) -> None:
        import i18nlib.publish as publish_module

        cases = (
            (
                "launch",
                FileNotFoundError("controlled missing git"),
                r"preflight failed to start: controlled missing git",
            ),
            (
                "nonzero",
                subprocess.CompletedProcess(
                    ["git", "diff"],
                    128,
                    stdout="",
                    stderr="controlled index failure\n",
                ),
                r"preflight failed: controlled index failure",
            ),
        )
        for label, outcome, expected in cases:
            with self.subTest(case=label), tempfile.TemporaryDirectory(
                prefix="tome4-publish-git-preflight-failure-"
            ) as temporary:
                manifest, locale_path, init_path, _ = self._isolated_publish_fixture(
                    Path(temporary)
                )
                addon_root = locale_path.parents[2]
                files_before = {
                    locale_path: locale_path.read_bytes(),
                    init_path: init_path.read_bytes(),
                }
                index_before = self._git(addon_root, "write-tree").stdout
                loader = Mock(spec=LocaleLoader)
                run_kwargs = (
                    {"side_effect": outcome}
                    if isinstance(outcome, BaseException)
                    else {"return_value": outcome}
                )

                with (
                    patch.dict(
                        os.environ,
                        {"TOME4_PUBLISH_TEST_ADDON_ROOT": str(addon_root)},
                    ),
                    patch.object(publish_module, "build_addon_locale") as build,
                    patch.object(
                        publish_module.subprocess,
                        "run",
                        **run_kwargs,
                    ),
                ):
                    with self.assertRaisesRegex(ValidationError, expected):
                        publish_module.publish_addon(
                            manifest,
                            loader,
                            apply=True,
                            bump=True,
                            commit=True,
                        )

                build.assert_not_called()
                self.assertEqual(loader.mock_calls, [])
                self.assertEqual(
                    {path: path.read_bytes() for path in files_before},
                    files_before,
                )
                self.assertEqual(
                    self._git(addon_root, "write-tree").stdout,
                    index_before,
                )

    def test_publish_commit_excludes_preexisting_staged_changes(self) -> None:
        import i18nlib.publish as publish_module

        entry = {
            "kind": "translation",
            "section": "fixture/new.lua",
            "source": "fixture source",
            "target": "fixture target",
            "source_tag": None,
            "args_order": None,
            "special": None,
        }
        build_report = self._publish_build_report(entry)

        for bump in (False, True):
            with self.subTest(bump=bump), tempfile.TemporaryDirectory(
                prefix=f"tome4-publish-scoped-commit-{bump}-"
            ) as temporary:
                manifest, locale_path, init_path, _ = self._isolated_publish_fixture(
                    Path(temporary)
                )
                addon_root = locale_path.parents[2]
                unrelated_path = addon_root / "unrelated.txt"
                unrelated_path.write_text("baseline\n", encoding="utf-8")
                locale_mode = stat.S_IMODE(locale_path.stat().st_mode)
                init_mode = stat.S_IMODE(init_path.stat().st_mode)

                def git(*arguments: str) -> subprocess.CompletedProcess[str]:
                    return self._git(addon_root, *arguments)

                git("add", "--", "unrelated.txt")
                git("commit", "-qm", "add unrelated baseline")

                unrelated_path.write_text("staged user change\n", encoding="utf-8")
                staged_before = ["unrelated.txt"]
                git("add", "--", "unrelated.txt")
                if not bump:
                    init_path.write_text(
                        "addon_version = {0,0,1}\n-- staged user change\n",
                        encoding="utf-8",
                    )
                    git("add", "--", "init.lua")
                    staged_before.insert(0, "init.lua")
                preserved_index_before = git(
                    "ls-files",
                    "--stage",
                    "--",
                    *staged_before,
                ).stdout

                with (
                    patch.dict(
                        os.environ,
                        {
                            "TOME4_PUBLISH_TEST_ADDON_ROOT": str(addon_root),
                        },
                    ),
                    patch.object(
                        publish_module,
                        "build_addon_locale",
                        return_value=build_report,
                    ),
                    patch.object(
                        publish_module, "_official_locale_keys", return_value=set()
                    ),
                    patch.object(
                        publish_module, "_dlc_overlay_entries", return_value=[]
                    ),
                ):
                    report = publish_module.publish_addon(
                        manifest,
                        self.loader,
                        apply=True,
                        bump=bump,
                        commit=True,
                    )

                committed_paths = git(
                    "diff-tree",
                    "--no-commit-id",
                    "--name-only",
                    "-r",
                    "HEAD",
                ).stdout.splitlines()
                expected_paths = ["data/locales/zh_hans.lua"]
                if bump:
                    expected_paths.append("init.lua")
                self.assertEqual(committed_paths, expected_paths)
                self.assertEqual(
                    git("diff", "--cached", "--name-only").stdout.splitlines(),
                    staged_before,
                )
                self.assertEqual(
                    git("ls-files", "--stage", "--", *staged_before).stdout,
                    preserved_index_before,
                )
                self.assertEqual(
                    report["release_head"], git("rev-parse", "HEAD").stdout.strip()
                )
                self.assertEqual(
                    stat.S_IMODE(locale_path.stat().st_mode),
                    locale_mode,
                )
                self.assertEqual(stat.S_IMODE(init_path.stat().st_mode), init_mode)
                if bump:
                    self.assertIn(b"addon_version = {0,0,2}\r\n", init_path.read_bytes())

    @staticmethod
    def _git(
        root: Path,
        *arguments: str,
        check: bool = True,
    ) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", *arguments],
            cwd=root,
            check=check,
            capture_output=True,
            text=True,
        )

    def _isolated_publish_fixture(
        self,
        root: Path,
        *,
        commit_baseline: bool = True,
    ) -> tuple[object, Path, Path, str]:
        addon_root = (root / "addon").resolve()
        locale_path = addon_root / "data" / "locales" / "zh_hans.lua"
        init_path = addon_root / "init.lua"
        locale_path.parent.mkdir(parents=True)
        locale_text = (
            'locale "zh_hans"\n'
            'section "fixture/old.lua"\n'
            't("old source", "old target")\n'
        )
        locale_path.write_text(locale_text, encoding="utf-8")
        init_path.write_bytes(b"addon_version = {0,0,1}\r\n")
        locale_path.chmod(0o640)
        init_path.chmod(0o600)
        self._git(addon_root, "init", "-q")
        self._git(addon_root, "config", "user.name", "fixture")
        self._git(
            addon_root,
            "config",
            "user.email",
            "fixture@example.invalid",
        )
        if commit_baseline:
            self._git(
                addon_root,
                "add",
                "--",
                "data/locales/zh_hans.lua",
                "init.lua",
            )
            self._git(addon_root, "commit", "-qm", "baseline")
        repositories = dict(self.manifest.repositories)
        repositories["addon"] = replace(
            repositories["addon"],
            env="TOME4_PUBLISH_TEST_ADDON_ROOT",
            default="addon",
        )
        manifest = replace(self.manifest, root=root, repositories=repositories)
        return manifest, locale_path, init_path, locale_text

    @staticmethod
    def _publish_build_report(entry: dict[str, object]) -> dict[str, object]:
        return {
            "delta_entries": [entry],
            "components": [{"delta_entries": 1}],
            "override_entries": 0,
            "new_entries": 1,
            "verification": {"patch_runtime_keys": 1},
        }

    def test_publish_non_bump_does_not_read_init_contents(self) -> None:
        import i18nlib.publish as publish_module

        entry = {
            "kind": "translation",
            "section": "fixture/new.lua",
            "source": "fixture source",
            "target": "fixture target",
            "source_tag": None,
            "args_order": None,
            "special": None,
        }
        build_report = self._publish_build_report(entry)
        with tempfile.TemporaryDirectory(
            prefix="tome4-publish-non-bump-read-"
        ) as temporary:
            manifest, locale_path, init_path, _ = self._isolated_publish_fixture(
                Path(temporary)
            )
            original_read_snapshot = publish_module._read_file_snapshot
            snapshot_paths: list[Path] = []

            def tracked_read_snapshot(path: Path, *, label: str) -> object:
                snapshot_paths.append(path)
                return original_read_snapshot(path, label=label)

            with (
                patch.dict(
                    os.environ,
                    {"TOME4_PUBLISH_TEST_ADDON_ROOT": str(locale_path.parents[2])},
                ),
                patch.object(
                    publish_module,
                    "build_addon_locale",
                    return_value=build_report,
                ),
                patch.object(publish_module, "_official_locale_keys", return_value=set()),
                patch.object(publish_module, "_dlc_overlay_entries", return_value=[]),
                patch.object(
                    publish_module,
                    "_read_file_snapshot",
                    side_effect=tracked_read_snapshot,
                ),
            ):
                report = publish_module.publish_addon(
                    manifest,
                    self.loader,
                    apply=False,
                    bump=False,
                    commit=False,
                )

            self.assertFalse(report["applied"])
            self.assertEqual(snapshot_paths, [locale_path])
            self.assertNotIn(init_path, snapshot_paths)

    def test_publish_hash_failure_restores_locale_bytes_and_mode(self) -> None:
        import i18nlib.publish as publish_module

        entry = {
            "kind": "translation",
            "section": "fixture/new.lua",
            "source": "fixture source",
            "target": "fixture target",
            "source_tag": None,
            "args_order": None,
            "special": None,
        }
        build_report = self._publish_build_report(entry)
        with tempfile.TemporaryDirectory(
            prefix="tome4-publish-hash-rollback-"
        ) as temporary:
            manifest, locale_path, _, _ = self._isolated_publish_fixture(
                Path(temporary)
            )
            addon_root = locale_path.parents[2]
            original_locale = locale_path.read_bytes()
            original_mode = stat.S_IMODE(locale_path.stat().st_mode)
            index_before = self._git(addon_root, "write-tree").stdout
            original_atomic_replace = publish_module._atomic_replace_bytes

            def corrupt_locale_write(
                path: Path,
                data: bytes,
                mode: int,
                *,
                label: str,
            ) -> None:
                if label == "publish locale write":
                    data += b"\n-- controlled post-write corruption\n"
                original_atomic_replace(path, data, mode, label=label)

            with (
                patch.dict(
                    os.environ,
                    {"TOME4_PUBLISH_TEST_ADDON_ROOT": str(addon_root)},
                ),
                patch.object(
                    publish_module,
                    "build_addon_locale",
                    return_value=build_report,
                ),
                patch.object(publish_module, "_official_locale_keys", return_value=set()),
                patch.object(publish_module, "_dlc_overlay_entries", return_value=[]),
                patch.object(
                    publish_module,
                    "_atomic_replace_bytes",
                    side_effect=corrupt_locale_write,
                ),
            ):
                with self.assertRaisesRegex(
                    ValidationError,
                    r"publish verification failed: written file hash mismatch",
                ):
                    publish_module.publish_addon(
                        manifest,
                        self.loader,
                        apply=True,
                        bump=False,
                        commit=False,
                    )

            self.assertEqual(locale_path.read_bytes(), original_locale)
            self.assertEqual(stat.S_IMODE(locale_path.stat().st_mode), original_mode)
            self.assertEqual(self._git(addon_root, "write-tree").stdout, index_before)
            self.assertEqual(
                list(locale_path.parent.glob(f".{locale_path.name}.*.tmp")),
                [],
            )

    def test_publish_second_file_failure_rolls_back_both_files_in_reverse(
        self,
    ) -> None:
        import i18nlib.publish as publish_module

        entry = {
            "kind": "translation",
            "section": "fixture/new.lua",
            "source": "fixture source",
            "target": "fixture target",
            "source_tag": None,
            "args_order": None,
            "special": None,
        }
        build_report = self._publish_build_report(entry)
        with tempfile.TemporaryDirectory(
            prefix="tome4-publish-second-write-rollback-"
        ) as temporary:
            manifest, locale_path, init_path, _ = self._isolated_publish_fixture(
                Path(temporary)
            )
            addon_root = locale_path.parents[2]
            original_locale = locale_path.read_bytes()
            original_init = init_path.read_bytes()
            original_modes = {
                locale_path: stat.S_IMODE(locale_path.stat().st_mode),
                init_path: stat.S_IMODE(init_path.stat().st_mode),
            }
            index_before = self._git(addon_root, "write-tree").stdout
            original_os_replace = publish_module.os.replace
            replaced_paths: list[Path] = []
            failed_init_replace = False

            def fail_after_init_replace(source: object, target: object) -> None:
                nonlocal failed_init_replace
                original_os_replace(source, target)
                target_path = Path(target)
                replaced_paths.append(target_path)
                if target_path == init_path and not failed_init_replace:
                    failed_init_replace = True
                    raise OSError("controlled second-file replace failure")

            with (
                patch.dict(
                    os.environ,
                    {"TOME4_PUBLISH_TEST_ADDON_ROOT": str(addon_root)},
                ),
                patch.object(
                    publish_module,
                    "build_addon_locale",
                    return_value=build_report,
                ),
                patch.object(publish_module, "_official_locale_keys", return_value=set()),
                patch.object(publish_module, "_dlc_overlay_entries", return_value=[]),
                patch.object(
                    publish_module.os,
                    "replace",
                    side_effect=fail_after_init_replace,
                ),
            ):
                with self.assertRaisesRegex(
                    ValidationError,
                    "controlled second-file replace failure",
                ):
                    publish_module.publish_addon(
                        manifest,
                        self.loader,
                        apply=True,
                        bump=True,
                        commit=False,
                    )

            self.assertEqual(replaced_paths, [locale_path, init_path, init_path, locale_path])
            self.assertEqual(locale_path.read_bytes(), original_locale)
            self.assertEqual(init_path.read_bytes(), original_init)
            self.assertEqual(
                stat.S_IMODE(locale_path.stat().st_mode),
                original_modes[locale_path],
            )
            self.assertEqual(
                stat.S_IMODE(init_path.stat().st_mode),
                original_modes[init_path],
            )
            self.assertEqual(self._git(addon_root, "write-tree").stdout, index_before)

    def test_publish_failed_commit_restores_files_and_preserves_index(self) -> None:
        import i18nlib.publish as publish_module

        entry = {
            "kind": "translation",
            "section": "fixture/new.lua",
            "source": "fixture source",
            "target": "fixture target",
            "source_tag": None,
            "args_order": None,
            "special": None,
        }
        build_report = self._publish_build_report(entry)
        with tempfile.TemporaryDirectory(
            prefix="tome4-publish-commit-failure-"
        ) as temporary:
            manifest, locale_path, init_path, _ = self._isolated_publish_fixture(
                Path(temporary)
            )
            addon_root = locale_path.parents[2]
            unrelated_path = addon_root / "unrelated.txt"
            unrelated_path.write_text("baseline\n", encoding="utf-8")
            self._git(addon_root, "add", "--", "unrelated.txt")
            self._git(addon_root, "commit", "-qm", "add unrelated baseline")

            original_locale = locale_path.read_bytes()
            original_init = init_path.read_bytes()
            original_modes = {
                locale_path: stat.S_IMODE(locale_path.stat().st_mode),
                init_path: stat.S_IMODE(init_path.stat().st_mode),
            }

            unrelated_path.write_text("staged unrelated change\n", encoding="utf-8")
            self._git(addon_root, "add", "--", "unrelated.txt")

            index_tree_before = self._git(addon_root, "write-tree").stdout
            index_entries_before = self._git(
                addon_root,
                "ls-files",
                "--stage",
            ).stdout
            cached_diff_before = self._git(
                addon_root,
                "diff",
                "--cached",
                "--binary",
                "--no-ext-diff",
            ).stdout
            status_before = self._git(
                addon_root,
                "status",
                "--porcelain=v1",
            ).stdout
            head_before = self._git(addon_root, "rev-parse", "HEAD").stdout

            hook_path = addon_root / ".git" / "hooks" / "pre-commit"
            hook_path.write_text(
                "#!/bin/sh\necho controlled hook failure >&2\nexit 23\n",
                encoding="utf-8",
            )
            hook_path.chmod(0o755)

            with (
                patch.dict(
                    os.environ,
                    {"TOME4_PUBLISH_TEST_ADDON_ROOT": str(addon_root)},
                ),
                patch.object(
                    publish_module,
                    "build_addon_locale",
                    return_value=build_report,
                ),
                patch.object(publish_module, "_official_locale_keys", return_value=set()),
                patch.object(publish_module, "_dlc_overlay_entries", return_value=[]),
            ):
                with self.assertRaisesRegex(
                    ValidationError,
                    r"release git commit failed: controlled hook failure",
                ):
                    publish_module.publish_addon(
                        manifest,
                        self.loader,
                        apply=True,
                        bump=True,
                        commit=True,
                    )

            self.assertEqual(locale_path.read_bytes(), original_locale)
            self.assertEqual(init_path.read_bytes(), original_init)
            self.assertEqual(
                stat.S_IMODE(locale_path.stat().st_mode),
                original_modes[locale_path],
            )
            self.assertEqual(
                stat.S_IMODE(init_path.stat().st_mode),
                original_modes[init_path],
            )
            self.assertEqual(
                self._git(addon_root, "write-tree").stdout,
                index_tree_before,
            )
            self.assertEqual(
                self._git(addon_root, "ls-files", "--stage").stdout,
                index_entries_before,
            )
            self.assertEqual(
                self._git(
                    addon_root,
                    "diff",
                    "--cached",
                    "--binary",
                    "--no-ext-diff",
                ).stdout,
                cached_diff_before,
            )
            self.assertEqual(
                self._git(addon_root, "status", "--porcelain=v1").stdout,
                status_before,
            )
            self.assertEqual(
                self._git(addon_root, "rev-parse", "HEAD").stdout,
                head_before,
            )

    def test_publish_git_launch_failure_is_wrapped_and_rolled_back(self) -> None:
        import i18nlib.publish as publish_module

        entry = {
            "kind": "translation",
            "section": "fixture/new.lua",
            "source": "fixture source",
            "target": "fixture target",
            "source_tag": None,
            "args_order": None,
            "special": None,
        }
        build_report = self._publish_build_report(entry)
        with tempfile.TemporaryDirectory(
            prefix="tome4-publish-git-launch-rollback-"
        ) as temporary:
            manifest, locale_path, init_path, _ = self._isolated_publish_fixture(
                Path(temporary)
            )
            addon_root = locale_path.parents[2]
            original_locale = locale_path.read_bytes()
            original_init = init_path.read_bytes()
            index_before = self._git(addon_root, "write-tree").stdout
            original_subprocess_run = subprocess.run

            def fail_git_commit(command: object, **kwargs: object) -> object:
                if isinstance(command, list) and command[:2] == ["git", "commit"]:
                    raise FileNotFoundError("controlled missing git")
                return original_subprocess_run(command, **kwargs)

            with (
                patch.dict(
                    os.environ,
                    {"TOME4_PUBLISH_TEST_ADDON_ROOT": str(addon_root)},
                ),
                patch.object(
                    publish_module,
                    "build_addon_locale",
                    return_value=build_report,
                ),
                patch.object(publish_module, "_official_locale_keys", return_value=set()),
                patch.object(publish_module, "_dlc_overlay_entries", return_value=[]),
                patch.object(
                    publish_module.subprocess,
                    "run",
                    side_effect=fail_git_commit,
                ),
            ):
                with self.assertRaisesRegex(
                    ValidationError,
                    r"release git commit failed to start: controlled missing git",
                ):
                    publish_module.publish_addon(
                        manifest,
                        self.loader,
                        apply=True,
                        bump=True,
                        commit=True,
                    )

            self.assertEqual(locale_path.read_bytes(), original_locale)
            self.assertEqual(init_path.read_bytes(), original_init)
            self.assertEqual(self._git(addon_root, "write-tree").stdout, index_before)

    def test_publish_keyboard_interrupt_rolls_back_and_propagates(self) -> None:
        import i18nlib.publish as publish_module

        entry = {
            "kind": "translation",
            "section": "fixture/new.lua",
            "source": "fixture source",
            "target": "fixture target",
            "source_tag": None,
            "args_order": None,
            "special": None,
        }
        build_report = self._publish_build_report(entry)
        interrupt = KeyboardInterrupt("controlled publish interrupt")
        with tempfile.TemporaryDirectory(
            prefix="tome4-publish-interrupt-rollback-"
        ) as temporary:
            manifest, locale_path, _, _ = self._isolated_publish_fixture(
                Path(temporary)
            )
            addon_root = locale_path.parents[2]
            original_locale = locale_path.read_bytes()
            original_mode = stat.S_IMODE(locale_path.stat().st_mode)
            original_verify = publish_module._verify_file_snapshot

            def interrupt_post_write(
                path: Path,
                expected: object,
                *,
                label: str,
            ) -> bytes:
                if label == "publish verification":
                    raise interrupt
                return original_verify(path, expected, label=label)

            with (
                patch.dict(
                    os.environ,
                    {"TOME4_PUBLISH_TEST_ADDON_ROOT": str(addon_root)},
                ),
                patch.object(
                    publish_module,
                    "build_addon_locale",
                    return_value=build_report,
                ),
                patch.object(publish_module, "_official_locale_keys", return_value=set()),
                patch.object(publish_module, "_dlc_overlay_entries", return_value=[]),
                patch.object(
                    publish_module,
                    "_verify_file_snapshot",
                    side_effect=interrupt_post_write,
                ),
            ):
                with self.assertRaises(KeyboardInterrupt) as raised:
                    publish_module.publish_addon(
                        manifest,
                        self.loader,
                        apply=True,
                        bump=False,
                        commit=False,
                    )

            self.assertIs(raised.exception, interrupt)
            self.assertEqual(locale_path.read_bytes(), original_locale)
            self.assertEqual(stat.S_IMODE(locale_path.stat().st_mode), original_mode)

    def test_publish_rollback_failure_is_explicit_and_chains_original(self) -> None:
        import i18nlib.publish as publish_module

        entry = {
            "kind": "translation",
            "section": "fixture/new.lua",
            "source": "fixture source",
            "target": "fixture target",
            "source_tag": None,
            "args_order": None,
            "special": None,
        }
        build_report = self._publish_build_report(entry)
        with tempfile.TemporaryDirectory(
            prefix="tome4-publish-rollback-failure-"
        ) as temporary:
            manifest, locale_path, _, _ = self._isolated_publish_fixture(
                Path(temporary)
            )
            addon_root = locale_path.parents[2]
            original_atomic_replace = publish_module._atomic_replace_bytes
            loader = Mock(spec=LocaleLoader)
            loader.load_bytes.side_effect = self.loader.load_bytes
            locale_loads = 0

            def fail_post_write_load(
                path: Path,
                *,
                logical_path: str,
            ) -> LocaleDocument:
                nonlocal locale_loads
                locale_loads += 1
                if locale_loads == 2:
                    raise ValidationError("controlled post-write failure")
                return self.loader.load_path(path, logical_path=logical_path)

            def fail_rollback(
                path: Path,
                data: bytes,
                mode: int,
                *,
                label: str,
            ) -> None:
                if label == "publish rollback":
                    raise OSError("controlled rollback failure")
                original_atomic_replace(path, data, mode, label=label)

            loader.load_path.side_effect = fail_post_write_load
            with (
                patch.dict(
                    os.environ,
                    {"TOME4_PUBLISH_TEST_ADDON_ROOT": str(addon_root)},
                ),
                patch.object(
                    publish_module,
                    "build_addon_locale",
                    return_value=build_report,
                ),
                patch.object(publish_module, "_official_locale_keys", return_value=set()),
                patch.object(publish_module, "_dlc_overlay_entries", return_value=[]),
                patch.object(
                    publish_module,
                    "_atomic_replace_bytes",
                    side_effect=fail_rollback,
                ),
            ):
                with self.assertRaisesRegex(
                    ValidationError,
                    r"publish transaction rollback failed after ValidationError:.*"
                    r"controlled rollback failure",
                ) as raised:
                    publish_module.publish_addon(
                        manifest,
                        loader,
                        apply=True,
                        bump=False,
                        commit=False,
                    )

            self.assertIsInstance(raised.exception.__cause__, ValidationError)
            self.assertIn(
                "controlled post-write failure",
                str(raised.exception.__cause__),
            )

    def test_publish_rejects_bool_int_artifact_change_before_release_writes(
        self,
    ) -> None:
        import i18nlib.publish as publish_module

        entry = {
            "kind": "translation",
            "section": "fixture/new.lua",
            "source": "fixture source",
            "target": "fixture target",
            "source_tag": None,
            "args_order": None,
            "special": True,
        }
        build_report = self._publish_build_report(entry)
        original_renderer = publish_module._render_addon_locale

        def corrupted_renderer(
            manifest: object,
            entries: object,
            *,
            skipped: object,
        ) -> bytes:
            rendered = original_renderer(manifest, entries, skipped=skipped)
            self.assertIn(b", true)", rendered)
            return rendered.replace(b", true)", b", 1)", 1)

        with tempfile.TemporaryDirectory(
            prefix="tome4-publish-prewrite-"
        ) as temporary:
            manifest, locale_path, init_path, locale_text = (
                self._isolated_publish_fixture(Path(temporary))
            )
            original_init = init_path.read_bytes()
            release_writes: list[Path] = []
            original_write_bytes = Path.write_bytes

            def tracked_write_bytes(path: Path, data: bytes) -> int:
                if path in (locale_path, init_path):
                    release_writes.append(path)
                return original_write_bytes(path, data)

            git_subprocess = Mock()
            git_subprocess.run.return_value = subprocess.CompletedProcess(
                ["git", "diff"],
                0,
                stdout="",
                stderr="",
            )
            with (
                patch.dict(
                    os.environ,
                    {"TOME4_PUBLISH_TEST_ADDON_ROOT": str(locale_path.parents[2])},
                ),
                patch.object(
                    publish_module,
                    "build_addon_locale",
                    return_value=build_report,
                ),
                patch.object(publish_module, "_official_locale_keys", return_value=set()),
                patch.object(publish_module, "_dlc_overlay_entries", return_value=[]),
                patch.object(
                    publish_module,
                    "_render_addon_locale",
                    side_effect=corrupted_renderer,
                ),
                patch.object(Path, "write_bytes", tracked_write_bytes),
                patch.object(publish_module, "subprocess", git_subprocess),
                patch.object(publish_module, "_bump_init_version") as bump_version,
            ):
                with self.assertRaisesRegex(
                    ValidationError,
                    r"publish pre-write verification failed:.*mismatched=1",
                ):
                    publish_module.publish_addon(
                        manifest,
                        self.loader,
                        apply=True,
                        bump=True,
                        commit=True,
                    )

            self.assertEqual(release_writes, [])
            self.assertEqual(locale_path.read_text(encoding="utf-8"), locale_text)
            self.assertEqual(init_path.read_bytes(), original_init)
            bump_version.assert_not_called()
            git_subprocess.run.assert_called_once_with(
                [
                    "git",
                    "diff",
                    "--cached",
                    "--quiet",
                    "--",
                    "data/locales/zh_hans.lua",
                    "init.lua",
                ],
                cwd=locale_path.parents[2],
                capture_output=True,
                text=True,
            )

    def test_publish_post_write_semantic_failure_precedes_git(self) -> None:
        import i18nlib.publish as publish_module

        entry = {
            "kind": "translation",
            "section": "fixture/new.lua",
            "source": "fixture source",
            "target": "fixture target",
            "source_tag": None,
            "args_order": None,
            "special": None,
        }
        build_report = self._publish_build_report(entry)

        with tempfile.TemporaryDirectory(
            prefix="tome4-publish-postwrite-"
        ) as temporary:
            manifest, locale_path, init_path, _ = self._isolated_publish_fixture(
                Path(temporary)
            )
            original_locale = locale_path.read_bytes()
            original_locale_mode = stat.S_IMODE(locale_path.stat().st_mode)
            loader = Mock(spec=LocaleLoader)
            loader.load_bytes.side_effect = self.loader.load_bytes
            locale_loads = 0

            def load_path(path: Path, *, logical_path: str) -> LocaleDocument:
                nonlocal locale_loads
                document = self.loader.load_path(path, logical_path=logical_path)
                if path != locale_path:
                    return document
                locale_loads += 1
                if locale_loads != 2:
                    return document
                records = tuple(
                    {
                        **record,
                        "target": "renderer-preserving post-write corruption",
                    }
                    if record.get("kind") == "translation"
                    else record
                    for record in document.records
                )
                return LocaleDocument(
                    logical_path=document.logical_path,
                    sha256=document.sha256,
                    records=records,
                )

            loader.load_path.side_effect = load_path
            git_subprocess = Mock()
            git_subprocess.run.return_value = subprocess.CompletedProcess(
                ["git", "diff"],
                0,
                stdout="",
                stderr="",
            )
            with (
                patch.dict(
                    os.environ,
                    {"TOME4_PUBLISH_TEST_ADDON_ROOT": str(locale_path.parents[2])},
                ),
                patch.object(
                    publish_module,
                    "build_addon_locale",
                    return_value=build_report,
                ),
                patch.object(publish_module, "_official_locale_keys", return_value=set()),
                patch.object(publish_module, "_dlc_overlay_entries", return_value=[]),
                patch.object(publish_module, "subprocess", git_subprocess),
            ):
                with self.assertRaisesRegex(
                    ValidationError,
                    r"publish post-write verification failed:.*mismatched=1",
                ):
                    publish_module.publish_addon(
                        manifest,
                        loader,
                        apply=True,
                        bump=False,
                        commit=True,
                    )

            self.assertEqual(locale_loads, 2)
            self.assertEqual(locale_path.read_bytes(), original_locale)
            self.assertEqual(
                stat.S_IMODE(locale_path.stat().st_mode),
                original_locale_mode,
            )
            self.assertEqual(
                init_path.read_text(encoding="utf-8"),
                "addon_version = {0,0,1}\n",
            )
            git_subprocess.run.assert_called_once_with(
                [
                    "git",
                    "diff",
                    "--cached",
                    "--quiet",
                    "--",
                    "data/locales/zh_hans.lua",
                ],
                cwd=locale_path.parents[2],
                capture_output=True,
                text=True,
            )


class SmokeReleaseTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.manifest = load_manifest()

    @staticmethod
    def _write_layout(root: Path) -> dict[str, Path]:
        paths = {
            "locale": root / "data" / "locales" / "zh_hans.lua",
            "null": root / "data" / "null_translation.lua",
            "hooks": root / "hooks" / "load.lua",
            "init": root / "init.lua",
        }
        for path in paths.values():
            path.parent.mkdir(parents=True, exist_ok=True)
        paths["locale"].write_text("-- release fixture\n", encoding="utf-8")
        paths["null"].write_text("-- null fixture\n", encoding="utf-8")
        paths["hooks"].write_text(
            'load("/data/null_translation.lua")\n', encoding="utf-8"
        )
        paths["init"].write_text(
            '-- GNU General Public License\nfor_module = "tome"\n'
            "addon_version = {0, 0, 1}\n",
            encoding="utf-8",
        )
        return paths

    @staticmethod
    def _entry(
        source: str,
        target: str,
        *,
        section: str = "ashes-urhrok",
        args_order: object = None,
        special: object = None,
    ) -> dict[str, object]:
        return {
            "kind": "translation",
            "section": section,
            "source": source,
            "target": target,
            "source_tag": None,
            "args_order": args_order,
            "special": special,
        }

    def _run_fixture(
        self,
        root: Path,
        release_entries: list[dict[str, object]],
        expected_entries: list[dict[str, object]],
        *,
        runtime_error: Exception | None = None,
    ) -> tuple[int, str, Mock, Mock, Mock]:
        paths = self._write_layout(root)
        runtime = Mock(spec=LuaRuntime)
        runtime.manifest = self.manifest

        def run_probe(
            arguments: list[object], **kwargs: object
        ) -> subprocess.CompletedProcess[str]:
            if runtime_error is not None:
                raise runtime_error
            target = Path(str(arguments[-1]))
            stdout = ""
            if target == paths["locale"]:
                stdout = "entries:6001\n"
            elif target == paths["null"]:
                stdout = "entries:401\n"
            return subprocess.CompletedProcess(arguments, 0, stdout, "")

        runtime.run.side_effect = run_probe
        runtime_factory = Mock(return_value=runtime)
        loader = Mock(spec=LocaleLoader)
        loader.load_path.return_value = LocaleDocument(
            logical_path="release",
            sha256="0" * 64,
            records=tuple(release_entries),
        )
        loader_factory = Mock(return_value=loader)
        official_keys_loader = Mock(return_value=set())
        overlay_entries_loader = Mock(return_value=expected_entries)
        stdout = io.StringIO()
        with contextlib.redirect_stdout(stdout):
            exit_code = smoke_release.run_release_smoke(
                self.manifest,
                root,
                runtime_factory=runtime_factory,
                loader_factory=loader_factory,
                official_keys_loader=official_keys_loader,
                overlay_entries_loader=overlay_entries_loader,
            )
        return exit_code, stdout.getvalue(), runtime, runtime_factory, loader_factory

    def test_missing_layout_files_short_circuit_before_runtime_or_reads(self) -> None:
        for missing_name in ("locale", "null", "hooks", "init"):
            with self.subTest(missing=missing_name), tempfile.TemporaryDirectory(
                prefix="tome4-smoke-layout-"
            ) as temporary:
                root = Path(temporary)
                paths = self._write_layout(root)
                paths[missing_name].unlink()
                runtime_factory = Mock(side_effect=AssertionError("runtime called"))
                loader_factory = Mock(side_effect=AssertionError("loader called"))
                text_reader = Mock(side_effect=AssertionError("read called"))
                stdout = io.StringIO()

                with contextlib.redirect_stdout(stdout):
                    exit_code = smoke_release.run_release_smoke(
                        self.manifest,
                        root,
                        runtime_factory=runtime_factory,
                        loader_factory=loader_factory,
                        text_reader=text_reader,
                    )

                self.assertEqual(exit_code, 1)
                for label in (
                    "locale file exists",
                    "null_translation exists",
                    "hooks/load.lua exists",
                    "init.lua exists",
                ):
                    self.assertIn(label, stdout.getvalue())
                runtime_factory.assert_not_called()
                loader_factory.assert_not_called()
                text_reader.assert_not_called()

    def test_configured_runtime_and_timeout_are_used_for_all_lua_smoke_checks(
        self,
    ) -> None:
        entries = [
            self._entry("ashes", "余烬"),
            self._entry("cults", "邪教", section="cults"),
            self._entry("orcs", "兽人", section="orcs"),
        ]
        with tempfile.TemporaryDirectory(prefix="tome4-smoke-runtime-") as temporary:
            root = Path(temporary)
            exit_code, stdout, runtime, runtime_factory, loader_factory = (
                self._run_fixture(root, entries, entries)
            )

        self.assertEqual(exit_code, 0, stdout)
        runtime_factory.assert_called_once_with(self.manifest)
        runtime.doctor.assert_called_once_with()
        loader_factory.assert_called_once_with(runtime)
        self.assertEqual(runtime.run.call_count, 3)
        targets = []
        for runtime_call in runtime.run.call_args_list:
            arguments = runtime_call.args[0]
            targets.append(Path(str(arguments[-1])))
            self.assertEqual(runtime_call.kwargs["cwd"], self.manifest.root)
            self.assertEqual(
                runtime_call.kwargs["timeout"],
                smoke_release._LUA_TIMEOUT_SECONDS,
            )
        self.assertEqual(
            targets,
            [
                root / "data" / "locales" / "zh_hans.lua",
                root / "data" / "null_translation.lua",
                root / "hooks" / "load.lua",
            ],
        )
        self.assertIn("SMOKE OK", stdout)
        for component_id in ("ashes-urhrok", "cults", "orcs"):
            self.assertIn(
                f"DLC {component_id} exact runtime overlay", stdout
            )
            self.assertIn("missing=0, unexpected=0, mismatched=0", stdout)

    def test_runtime_errors_are_clean_failures_without_tracebacks(self) -> None:
        entries = [
            self._entry("ashes", "余烬"),
            self._entry("cults", "邪教", section="cults"),
            self._entry("orcs", "兽人", section="orcs"),
        ]
        for detail in ("luajit not found", "luajit command timed out after 300 seconds"):
            with self.subTest(detail=detail), tempfile.TemporaryDirectory(
                prefix="tome4-smoke-runtime-error-"
            ) as temporary:
                exit_code, stdout, _, _, _ = self._run_fixture(
                    Path(temporary),
                    entries,
                    entries,
                    runtime_error=RuntimeError(detail),
                )

            self.assertEqual(exit_code, 1)
            self.assertIn("[FAIL]", stdout)
            self.assertIn(detail, stdout)
            self.assertNotIn("Traceback", stdout)

    def test_exact_dlc_comparison_rejects_all_drift_classes(self) -> None:
        key = ("same key", None)
        expected_entry = self._entry(
            "same key",
            "正确译文",
            args_order=[2, 1],
            special={"enabled": True},
        )
        expected = {key: expected_entry}
        cases = {
            "wrong target": {
                key: {**expected_entry, "target": "错误译文"},
            },
            "wrong args_order": {
                key: {**expected_entry, "args_order": [1, 2]},
            },
            "wrong special": {
                key: {**expected_entry, "special": {"enabled": False}},
            },
            "missing": {},
            "unexpected": {
                key: expected_entry,
                ("stale extra", None): self._entry("stale extra", "旧译文"),
            },
            "bool versus int": {
                key: {**expected_entry, "special": {"enabled": 1}},
            },
        }
        expected_drift = {
            "wrong target": (0, 0, 1),
            "wrong args_order": (0, 0, 1),
            "wrong special": (0, 0, 1),
            "missing": (1, 0, 0),
            "unexpected": (0, 1, 0),
            "bool versus int": (0, 0, 1),
        }

        for label, actual in cases.items():
            with self.subTest(case=label), tempfile.TemporaryDirectory(
                prefix="tome4-smoke-dlc-drift-"
            ) as temporary:
                comparison = smoke_release.compare_dlc_runtime_maps(
                    expected, actual
                )
                self.assertFalse(comparison.ok)
                self.assertEqual(
                    (
                        len(comparison.missing),
                        len(comparison.unexpected),
                        len(comparison.mismatched),
                    ),
                    expected_drift[label],
                )
                exit_code, stdout, _, _, _ = self._run_fixture(
                    Path(temporary),
                    list(actual.values()),
                    [expected_entry],
                )
                self.assertEqual(exit_code, 1, stdout)
                self.assertIn(
                    "[FAIL] DLC ashes-urhrok exact runtime overlay", stdout
                )

        exact = smoke_release.compare_dlc_runtime_maps(expected, dict(expected))
        self.assertTrue(exact.ok)
        self.assertEqual(
            exact.detail,
            "expected=1, actual=1, missing=0, unexpected=0, mismatched=0",
        )


if __name__ == "__main__":
    unittest.main()
