"""Toolchain tests: cli preflight."""

from __future__ import annotations

from tests.i18n import toolchain_fixtures
from tests.i18n.toolchain_fixtures import EMPTY_POLICY, _component_selection_document
import argparse
import contextlib
import io
import subprocess
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, call, patch
from i18nlib.cli_localization import _build as cli_build
from i18nlib.cli import main as cli_main
from i18nlib.cli_common import _select_components
from i18nlib.errors import ConfigurationError, ValidationError
from i18nlib.lint import Policy
from i18nlib.locale_model import LocaleLoader
from i18nlib.runtime import LuaRuntime


class PublishPreflightTests(unittest.TestCase):
    def test_direct_commit_without_apply_fails_before_dependencies(self) -> None:
        import i18nlib.publish as publish_module

        with (
            patch.object(publish_module, "build_addon_locale") as build,
            patch.object(publish_module, "_official_locale_keys") as official_keys,
            patch.object(publish_module, "_dlc_overlay_entries") as dlc_entries,
            patch.object(publish_module, "_render_addon_locale") as renderer,
            patch.object(publish_module, "subprocess") as git_subprocess,
        ):
            with self.assertRaisesRegex(
                ValidationError, "commit=True requires apply=True"
            ):
                publish_module.publish_addon(
                    None,
                    None,
                    apply=False,
                    bump=True,
                    commit=True,
                )

        build.assert_not_called()
        official_keys.assert_not_called()
        dlc_entries.assert_not_called()
        renderer.assert_not_called()
        git_subprocess.run.assert_not_called()

    def test_cli_commit_without_apply_fails_before_manifest_and_runtime(self) -> None:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with (
            patch("i18nlib.cli._inject_public_dlc_env"),
            patch("i18nlib.cli_localization._manifest") as manifest_factory,
            patch("i18nlib.cli_localization.LuaRuntime") as runtime_factory,
            patch("i18nlib.cli_localization.LocaleLoader") as loader_factory,
            patch("i18nlib.cli_localization.publish_addon") as publish,
            contextlib.redirect_stdout(stdout),
            contextlib.redirect_stderr(stderr),
        ):
            exit_code = cli_main(["publish", "--commit"])

        self.assertEqual(exit_code, ValidationError.exit_code)
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(
            stderr.getvalue(),
            "ERROR: publish --commit requires --apply\n",
        )
        manifest_factory.assert_not_called()
        runtime_factory.assert_not_called()
        loader_factory.assert_not_called()
        publish.assert_not_called()

    def test_release_layout_fails_before_build_loader_and_git(self) -> None:
        import i18nlib.publish as publish_module

        for missing in ("root", "locale", "init"):
            with self.subTest(missing=missing), tempfile.TemporaryDirectory(
                prefix=f"tome4-publish-missing-{missing}-"
            ) as temporary:
                addon_root = Path(temporary) / "addon"
                locale_path = addon_root / "data" / "locales" / "zh_hans.lua"
                init_path = addon_root / "init.lua"
                if missing != "root":
                    addon_root.mkdir(parents=True)
                    if missing != "locale":
                        locale_path.parent.mkdir(parents=True)
                        locale_path.write_text(
                            'locale "zh_hans"\n', encoding="utf-8"
                        )
                    if missing != "init":
                        init_path.write_text(
                            "addon_version = {0,0,1}\n", encoding="utf-8"
                        )

                manifest = Mock()
                manifest.repositories = {"addon": object()}
                manifest.repository_path.return_value = addon_root
                manifest.components = (Mock(id="tome"),)
                loader = Mock(spec=LocaleLoader)
                with (
                    patch.object(publish_module, "build_addon_locale") as build,
                    patch.object(
                        publish_module, "_official_locale_keys"
                    ) as official_keys,
                    patch.object(
                        publish_module, "_dlc_overlay_entries"
                    ) as dlc_entries,
                    patch.object(
                        publish_module, "_render_addon_locale"
                    ) as renderer,
                    patch.object(publish_module, "subprocess") as git_subprocess,
                ):
                    with self.assertRaisesRegex(
                        ValidationError,
                        r"release repository (?:not found|layout mismatch)",
                    ):
                        publish_module.publish_addon(
                            manifest,
                            loader,
                            apply=True,
                            bump=True,
                            commit=True,
                        )

                build.assert_not_called()
                official_keys.assert_not_called()
                dlc_entries.assert_not_called()
                renderer.assert_not_called()
                self.assertEqual(loader.mock_calls, [])
                git_subprocess.run.assert_not_called()

    def test_release_layout_rejects_symlink_publish_files_before_build(self) -> None:
        import i18nlib.publish as publish_module

        for symlink_name in ("locale", "init"):
            with self.subTest(symlink=symlink_name), tempfile.TemporaryDirectory(
                prefix=f"tome4-publish-symlink-{symlink_name}-"
            ) as temporary:
                addon_root = Path(temporary) / "addon"
                locale_path = addon_root / "data" / "locales" / "zh_hans.lua"
                init_path = addon_root / "init.lua"
                locale_path.parent.mkdir(parents=True)
                locale_path.write_text('locale "zh_hans"\n', encoding="utf-8")
                init_path.write_text(
                    "addon_version = {0,0,1}\n",
                    encoding="utf-8",
                )
                selected_path = locale_path if symlink_name == "locale" else init_path
                target_path = selected_path.with_name(f"real-{selected_path.name}")
                selected_path.replace(target_path)
                selected_path.symlink_to(target_path.name)
                subprocess.run(
                    ["git", "init", "-q"],
                    cwd=addon_root,
                    check=True,
                    capture_output=True,
                    text=True,
                )

                manifest = Mock()
                manifest.repositories = {"addon": object()}
                manifest.repository_path.return_value = addon_root
                manifest.components = (Mock(id="tome"),)
                loader = Mock(spec=LocaleLoader)
                with (
                    patch.object(publish_module, "build_addon_locale") as build,
                    patch.object(
                        publish_module,
                        "_official_locale_keys",
                    ) as official_keys,
                    patch.object(
                        publish_module,
                        "_dlc_overlay_entries",
                    ) as dlc_entries,
                    patch.object(
                        publish_module,
                        "_render_addon_locale",
                    ) as renderer,
                    patch.object(publish_module, "subprocess") as git_subprocess,
                ):
                    with self.assertRaisesRegex(
                        ValidationError,
                        r"publish files must be regular files, not symbolic links",
                    ):
                        publish_module.publish_addon(
                            manifest,
                            loader,
                            apply=True,
                            bump=True,
                            commit=True,
                        )

                build.assert_not_called()
                official_keys.assert_not_called()
                dlc_entries.assert_not_called()
                renderer.assert_not_called()
                self.assertEqual(loader.mock_calls, [])
                git_subprocess.run.assert_not_called()


class CliLightweightPreflightTests(unittest.TestCase):
    def test_unknown_components_fail_before_runtime_and_downstream_work(self) -> None:
        cases = (
            ("lint", ["lint", "--component", "missing"]),
            ("status", ["status", "--component", "missing"]),
            (
                "merge",
                [
                    "merge",
                    "--component",
                    "missing",
                    "--snapshot",
                    "unused.jsonl",
                ],
            ),
        )
        for command, arguments in cases:
            with self.subTest(command=command):
                manifest = Mock()
                manifest.component.side_effect = ConfigurationError(
                    "unknown component 'missing'"
                )
                runtime = Mock(spec=LuaRuntime)
                stdout = io.StringIO()
                stderr = io.StringIO()

                with (
                    patch("i18nlib.cli._inject_public_dlc_env"),
                    patch(
                        f"i18nlib.{'cli_lint' if command == 'lint' else 'cli_localization'}._manifest", return_value=manifest
                    ) as manifest_factory,
                    patch(
                        "i18nlib.cli_lint.load_policy"
                    ) as load_policy_mock,
                    patch(
                        f"i18nlib.{'cli_lint' if command == 'lint' else 'cli_localization'}.LuaRuntime", return_value=runtime
                    ) as runtime_factory,
                    patch(f"i18nlib.{'cli_lint' if command == 'lint' else 'cli_localization'}.LocaleLoader") as loader_factory,
                    patch("i18nlib.cli_lint.lint_documents") as lint_documents_mock,
                    patch("i18nlib.cli_lint.lint_terminology") as lint_terms,
                    patch("i18nlib.cli_localization.status_report") as build_status,
                    patch("i18nlib.cli_localization.run_merge") as merge,
                    patch(f"i18nlib.{'cli_lint' if command == 'lint' else 'cli_localization'}.create_run_directory") as create_run,
                    patch(f"i18nlib.{'cli_lint' if command == 'lint' else 'cli_localization'}.write_json") as write_json_mock,
                    contextlib.redirect_stdout(stdout),
                    contextlib.redirect_stderr(stderr),
                ):
                    exit_code = cli_main(arguments)

                self.assertEqual(exit_code, ConfigurationError.exit_code)
                self.assertEqual(stdout.getvalue(), "")
                self.assertEqual(
                    stderr.getvalue(), "ERROR: unknown component 'missing'\n"
                )
                manifest_factory.assert_called_once()
                manifest.component.assert_called_once_with("missing")
                load_policy_mock.assert_not_called()
                runtime_factory.assert_not_called()
                runtime.doctor.assert_not_called()
                loader_factory.assert_not_called()
                lint_documents_mock.assert_not_called()
                lint_terms.assert_not_called()
                build_status.assert_not_called()
                merge.assert_not_called()
                create_run.assert_not_called()
                write_json_mock.assert_not_called()

    def test_lint_policy_error_fails_after_selection_but_before_runtime(self) -> None:
        component = SimpleNamespace(id="known")
        manifest = Mock()
        manifest.component.return_value = component
        runtime = Mock(spec=LuaRuntime)
        stdout = io.StringIO()
        stderr = io.StringIO()

        with (
            patch("i18nlib.cli._inject_public_dlc_env"),
            patch(
                "i18nlib.cli_lint._manifest", return_value=manifest
            ) as manifest_factory,
            patch(
                "i18nlib.cli_lint.load_policy",
                side_effect=ConfigurationError("invalid lint policy"),
            ) as load_policy_mock,
            patch(
                "i18nlib.cli_lint.LuaRuntime", return_value=runtime
            ) as runtime_factory,
            patch("i18nlib.cli_lint.LocaleLoader") as loader_factory,
            patch("i18nlib.cli_lint.lint_documents") as lint_documents_mock,
            patch("i18nlib.cli_lint.lint_terminology") as lint_terms,
            patch("i18nlib.cli_lint.create_run_directory") as create_run,
            patch("i18nlib.cli_lint.write_json") as write_json_mock,
            contextlib.redirect_stdout(stdout),
            contextlib.redirect_stderr(stderr),
        ):
            exit_code = cli_main(
                [
                    "lint",
                    "--component",
                    "known",
                    "--component",
                    "known",
                ]
            )

        self.assertEqual(exit_code, ConfigurationError.exit_code)
        self.assertEqual(stdout.getvalue(), "")
        self.assertEqual(stderr.getvalue(), "ERROR: invalid lint policy\n")
        manifest_factory.assert_called_once()
        manifest.component.assert_called_once_with("known")
        load_policy_mock.assert_called_once_with(manifest)
        runtime_factory.assert_not_called()
        runtime.doctor.assert_not_called()
        loader_factory.assert_not_called()
        lint_documents_mock.assert_not_called()
        lint_terms.assert_not_called()
        create_run.assert_not_called()
        write_json_mock.assert_not_called()

    def test_valid_commands_resolve_once_before_runtime(self) -> None:
        cases = (
            (
                "lint",
                [
                    "lint",
                    "--component",
                    "known",
                    "--component",
                    "known",
                    "--json",
                ],
                [
                    "manifest",
                    "component",
                    "policy",
                    "runtime",
                    "doctor",
                    "loader",
                    "lint-canonical",
                    "lint-copy-fragment",
                    "terminology",
                ],
            ),
            (
                "status",
                [
                    "status",
                    "--component",
                    "known",
                    "--component",
                    "known",
                    "--json",
                ],
                [
                    "manifest",
                    "component",
                    "runtime",
                    "doctor",
                    "loader",
                    "status",
                ],
            ),
            (
                "merge",
                [
                    "merge",
                    "--component",
                    "known",
                    "--snapshot",
                    "unused.jsonl",
                    "--json",
                ],
                [
                    "manifest",
                    "component",
                    "runtime",
                    "doctor",
                    "loader",
                    "merge",
                ],
            ),
        )
        for command, arguments, expected_events in cases:
            with self.subTest(command=command):
                events: list[str] = []
                component = SimpleNamespace(
                    id="known",
                    translation="known.lua",
                    copy_fragment=None,
                )
                manifest = Mock()
                manifest.root = Path("/fixture")
                manifest.version = "fixture"
                manifest.terminology = "terminology.tsv"

                def resolve_component(identifier: str) -> object:
                    events.append("component")
                    self.assertEqual(identifier, "known")
                    return component

                manifest.component.side_effect = resolve_component
                runtime = Mock(spec=LuaRuntime)
                runtime.doctor.side_effect = lambda: events.append("doctor")
                loader = Mock(spec=LocaleLoader)
                loader.load_path.return_value = _component_selection_document(
                    "known.lua", "Known"
                )

                def load_manifest_for_test(_arguments: object) -> object:
                    events.append("manifest")
                    return manifest

                def load_policy_for_test(_manifest: object) -> Policy:
                    events.append("policy")
                    return EMPTY_POLICY

                def make_runtime(_manifest: object) -> Mock:
                    events.append("runtime")
                    return runtime

                def make_loader(_runtime: object) -> Mock:
                    events.append("loader")
                    return loader

                def lint_for_test(
                    _documents: object,
                    _policy: object,
                    *,
                    require_nonempty: bool,
                ) -> tuple[list[object], dict[str, object]]:
                    events.append(
                        "lint-canonical"
                        if require_nonempty
                        else "lint-copy-fragment"
                    )
                    return (
                        [],
                        {
                            "translations": 1 if require_nonempty else 0,
                            "components": {"known": 1}
                            if require_nonempty
                            else {},
                            "duplicate_runtime_keys": 0,
                        },
                    )

                with (
                    patch("i18nlib.cli._inject_public_dlc_env"),
                    patch(
                        f"i18nlib.{'cli_lint' if command == 'lint' else 'cli_localization'}._manifest",
                        side_effect=load_manifest_for_test,
                    ) as manifest_factory,
                    patch(
                        "i18nlib.cli_lint.load_policy",
                        side_effect=load_policy_for_test,
                    ) as load_policy_mock,
                    patch(
                        f"i18nlib.{'cli_lint' if command == 'lint' else 'cli_localization'}.LuaRuntime", side_effect=make_runtime
                    ) as runtime_factory,
                    patch(
                        f"i18nlib.{'cli_lint' if command == 'lint' else 'cli_localization'}.LocaleLoader", side_effect=make_loader
                    ) as loader_factory,
                    patch(
                        "i18nlib.cli_lint.lint_documents",
                        side_effect=lint_for_test,
                    ) as lint_documents_mock,
                    patch(
                        "i18nlib.cli_lint.lint_terminology",
                        side_effect=lambda _path: (
                            events.append("terminology") or ([], {"rows": 0})
                        ),
                    ) as lint_terms,
                    patch(
                        "i18nlib.cli_localization.status_report",
                        side_effect=lambda *_args: (
                            events.append("status") or {"components": []}
                        ),
                    ) as build_status,
                    patch(
                        "i18nlib.cli_localization.run_merge",
                        side_effect=lambda *_args, **_kwargs: (
                            events.append("merge") or {"ok": True}
                        ),
                    ) as merge,
                    patch(
                        f"i18nlib.{'cli_lint' if command == 'lint' else 'cli_localization'}.create_run_directory",
                        return_value=Path("/fixture/run"),
                    ),
                    patch(f"i18nlib.{'cli_lint' if command == 'lint' else 'cli_localization'}.write_json"),
                    patch(f"i18nlib.{'cli_lint' if command == 'lint' else 'cli_localization'}._print_json"),
                ):
                    self.assertEqual(cli_main(arguments), 0)

                self.assertEqual(events, expected_events)
                manifest_factory.assert_called_once()
                manifest.component.assert_called_once_with("known")
                runtime_factory.assert_called_once_with(manifest)
                runtime.doctor.assert_called_once_with()
                loader_factory.assert_called_once_with(runtime)
                if command == "lint":
                    load_policy_mock.assert_called_once_with(manifest)
                    self.assertEqual(lint_documents_mock.call_count, 2)
                    lint_terms.assert_called_once_with(
                        Path("/fixture/terminology.tsv")
                    )
                    build_status.assert_not_called()
                    merge.assert_not_called()
                elif command == "status":
                    load_policy_mock.assert_not_called()
                    lint_documents_mock.assert_not_called()
                    lint_terms.assert_not_called()
                    build_status.assert_called_once_with(
                        manifest, loader, [component]
                    )
                    merge.assert_not_called()
                else:
                    load_policy_mock.assert_not_called()
                    lint_documents_mock.assert_not_called()
                    lint_terms.assert_not_called()
                    build_status.assert_not_called()
                    merge.assert_called_once_with(
                        manifest,
                        loader,
                        component,
                        new_snapshot_path=Path("unused.jsonl"),
                        base_snapshot_path=None,
                    )


class ComponentSelectionTests(unittest.TestCase):
    def test_explicit_selection_deduplicates_ids_in_first_seen_order(self) -> None:
        first = SimpleNamespace(id="first")
        second = SimpleNamespace(id="second")
        manifest = Mock()
        manifest.component.side_effect = {"first": first, "second": second}.__getitem__

        selected = _select_components(
            manifest,
            ["second", "first", "second", "first"],
            default="lint",
        )

        self.assertEqual(selected, [second, first])
        self.assertEqual(
            manifest.component.call_args_list,
            [call("second"), call("first")],
        )

    def test_default_manifest_selections_are_unchanged(self) -> None:
        first = SimpleNamespace(
            id="first", extract_by_default=False, official_locale="first.lua"
        )
        second = SimpleNamespace(
            id="second", extract_by_default=True, official_locale=None
        )
        third = SimpleNamespace(
            id="third", extract_by_default=True, official_locale="third.lua"
        )
        manifest = Mock(components=(first, second, third))

        self.assertEqual(
            _select_components(manifest, [], default="extract"),
            [second, third],
        )
        self.assertEqual(
            _select_components(manifest, [], default="status"),
            [first, third],
        )
        self.assertEqual(
            _select_components(manifest, [], default="lint"),
            [first, second, third],
        )
        manifest.component.assert_not_called()

    def test_build_command_deduplicates_explicit_components_for_each_profile(
        self,
    ) -> None:
        for profile in ("full", "addon"):
            with self.subTest(profile=profile):
                first = SimpleNamespace(
                    id="first",
                    addon_eligible=True,
                    full_output="first.lua",
                )
                second = SimpleNamespace(
                    id="second",
                    addon_eligible=True,
                    full_output="second.lua",
                )
                manifest = Mock()
                manifest.component.side_effect = {
                    "first": first,
                    "second": second,
                }.__getitem__
                runtime = Mock()
                loader = Mock(spec=LocaleLoader)
                arguments = argparse.Namespace(
                    component=["second", "first", "second"],
                    profile=profile,
                    json=True,
                    require_complete=False,
                )
                full_report = {
                    "components": [],
                    "run_directory": "/artifacts/full",
                }
                addon_report = {"complete": True}

                with (
                    patch("i18nlib.cli_localization._manifest", return_value=manifest),
                    patch("i18nlib.cli_localization.LuaRuntime", return_value=runtime),
                    patch("i18nlib.cli_localization.LocaleLoader", return_value=loader),
                    patch(
                        "i18nlib.cli_localization.build_full_locales",
                        return_value=full_report,
                    ) as full_build,
                    patch(
                        "i18nlib.cli_localization.build_addon_locale",
                        return_value=addon_report,
                    ) as addon_build,
                    patch("i18nlib.cli_localization._print_json"),
                ):
                    self.assertEqual(cli_build(arguments), 0)

                self.assertEqual(
                    manifest.component.call_args_list,
                    [call("second"), call("first")],
                )
                runtime.doctor.assert_called_once_with()
                if profile == "full":
                    full_build.assert_called_once_with(
                        manifest, loader, [second, first]
                    )
                    addon_build.assert_not_called()
                else:
                    addon_build.assert_called_once_with(
                        manifest,
                        loader,
                        [second, first],
                        include_external_requirements=False,
                    )
                    full_build.assert_not_called()

    def test_invalid_explicit_build_selections_fail_before_runtime_and_io(
        self,
    ) -> None:
        eligible = SimpleNamespace(
            id="eligible",
            addon_eligible=True,
            full_output="eligible.lua",
        )
        no_full_output = SimpleNamespace(
            id="no-full-output",
            addon_eligible=True,
            full_output=None,
        )
        non_eligible = SimpleNamespace(
            id="non-eligible",
            addon_eligible=False,
            full_output="non-eligible.lua",
        )
        cases = (
            (
                "full invalid first",
                "full",
                [no_full_output, eligible],
                r"component 'no-full-output' has no full_output mapping",
            ),
            (
                "full invalid later",
                "full",
                [eligible, no_full_output],
                r"component 'no-full-output' has no full_output mapping",
            ),
            (
                "addon invalid first",
                "addon",
                [non_eligible, eligible],
                r"addon build requires addon-eligible components; "
                r"not eligible: non-eligible",
            ),
            (
                "addon invalid later",
                "addon",
                [eligible, non_eligible],
                r"addon build requires addon-eligible components; "
                r"not eligible: non-eligible",
            ),
        )
        for label, profile, selected, expected_error in cases:
            with self.subTest(case=label):
                manifest = Mock(components=tuple(selected))
                manifest.component.side_effect = {
                    component.id: component for component in selected
                }.__getitem__
                arguments = argparse.Namespace(
                    component=[component.id for component in selected],
                    profile=profile,
                    json=True,
                    require_complete=False,
                )
                with (
                    patch("i18nlib.cli_localization._manifest", return_value=manifest),
                    patch("i18nlib.cli_localization.LuaRuntime") as runtime_type,
                    patch("i18nlib.cli_localization.LocaleLoader") as loader_type,
                    patch("i18nlib.cli_localization.build_full_locales") as full_build,
                    patch("i18nlib.cli_localization.build_addon_locale") as addon_build,
                    patch(
                        "i18nlib.build.create_run_directory"
                    ) as create_run_directory,
                    patch("i18nlib.build._compose_full_locale") as compose,
                    patch("i18nlib.build.atomic_write_bytes") as write_bytes,
                    patch("i18nlib.build.write_json") as write_json,
                ):
                    with self.assertRaisesRegex(ValidationError, expected_error):
                        cli_build(arguments)

                runtime_type.assert_not_called()
                loader_type.assert_not_called()
                full_build.assert_not_called()
                addon_build.assert_not_called()
                create_run_directory.assert_not_called()
                compose.assert_not_called()
                write_bytes.assert_not_called()
                write_json.assert_not_called()

    def test_default_build_profile_selections_and_external_requirements_are_unchanged(
        self,
    ) -> None:
        both = SimpleNamespace(
            id="both",
            addon_eligible=True,
            full_output="both.lua",
        )
        full_only = SimpleNamespace(
            id="full-only",
            addon_eligible=False,
            full_output="full-only.lua",
        )
        addon_only = SimpleNamespace(
            id="addon-only",
            addon_eligible=True,
            full_output=None,
        )
        neither = SimpleNamespace(
            id="neither",
            addon_eligible=False,
            full_output=None,
        )
        manifest = Mock(components=(both, full_only, addon_only, neither))
        for profile, expected in (
            ("full", [both, full_only]),
            ("addon", [both, addon_only]),
        ):
            with self.subTest(profile=profile):
                runtime = Mock()
                loader = Mock(spec=LocaleLoader)
                arguments = argparse.Namespace(
                    component=[],
                    profile=profile,
                    json=True,
                    require_complete=False,
                )
                full_report = {
                    "components": [],
                    "run_directory": "/artifacts/full",
                }
                addon_report = {"complete": True}
                with (
                    patch("i18nlib.cli_localization._manifest", return_value=manifest),
                    patch("i18nlib.cli_localization.LuaRuntime", return_value=runtime),
                    patch("i18nlib.cli_localization.LocaleLoader", return_value=loader),
                    patch(
                        "i18nlib.cli_localization.build_full_locales",
                        return_value=full_report,
                    ) as full_build,
                    patch(
                        "i18nlib.cli_localization.build_addon_locale",
                        return_value=addon_report,
                    ) as addon_build,
                    patch("i18nlib.cli_localization._print_json"),
                ):
                    self.assertEqual(cli_build(arguments), 0)

                runtime.doctor.assert_called_once_with()
                manifest.component.assert_not_called()
                if profile == "full":
                    full_build.assert_called_once_with(manifest, loader, expected)
                    addon_build.assert_not_called()
                else:
                    addon_build.assert_called_once_with(
                        manifest,
                        loader,
                        expected,
                        include_external_requirements=True,
                    )
                    full_build.assert_not_called()

    def test_unknown_explicit_build_component_fails_before_runtime_and_io(
        self,
    ) -> None:
        known = SimpleNamespace(
            id="known",
            addon_eligible=True,
            full_output="known.lua",
        )
        for identifiers in (["missing"], ["known", "missing"]):
            with self.subTest(identifiers=identifiers):
                manifest = Mock(components=(known,))

                def resolve(component_id: str) -> object:
                    if component_id == "known":
                        return known
                    raise ConfigurationError(f"unknown component {component_id!r}")

                manifest.component.side_effect = resolve
                arguments = argparse.Namespace(
                    component=identifiers,
                    profile="full",
                    json=True,
                    require_complete=False,
                )
                with (
                    patch("i18nlib.cli_localization._manifest", return_value=manifest),
                    patch("i18nlib.cli_localization.LuaRuntime") as runtime_type,
                    patch("i18nlib.cli_localization.LocaleLoader") as loader_type,
                    patch("i18nlib.cli_localization.build_full_locales") as full_build,
                    patch("i18nlib.cli_localization.build_addon_locale") as addon_build,
                    patch(
                        "i18nlib.build.create_run_directory"
                    ) as create_run_directory,
                    patch("i18nlib.build._compose_full_locale") as compose,
                    patch("i18nlib.build.atomic_write_bytes") as write_bytes,
                    patch("i18nlib.build.write_json") as write_json,
                ):
                    with self.assertRaisesRegex(
                        ConfigurationError, r"unknown component 'missing'"
                    ):
                        cli_build(arguments)

                runtime_type.assert_not_called()
                loader_type.assert_not_called()
                full_build.assert_not_called()
                addon_build.assert_not_called()
                create_run_directory.assert_not_called()
                compose.assert_not_called()
                write_bytes.assert_not_called()
                write_json.assert_not_called()


if __name__ == "__main__":
    unittest.main()
