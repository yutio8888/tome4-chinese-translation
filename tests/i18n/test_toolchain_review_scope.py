"""Toolchain tests: review scope."""

from __future__ import annotations

from tests.i18n import toolchain_fixtures
import contextlib
from dataclasses import replace
import io
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from i18nlib.config import Manifest, load_manifest
from i18nlib.cli import _parser as cli_parser
from i18nlib.errors import ValidationError
from i18nlib.review import (
    MAX_REVIEW_BATCH_SIZE,
    REVIEW_INDEX_CONTRACT,
    REVIEW_INDEX_SCHEMA_VERSION,
    REVIEW_CONTRACT,
    REVIEW_SCHEMA_VERSION,
    _code_items,
    _git_diff,
    _git_status_paths,
    _is_public_review_path,
    create_review_index,
)
from i18nlib.translation_review import (
    TRANSLATION_REVIEW_BUNDLE_CONTRACT,
    TRANSLATION_REVIEW_CHANNEL,
    TRANSLATION_REVIEW_SCHEMA_VERSION,
)


class ReviewScopeTests(unittest.TestCase):
    def _assert_review_validation_has_no_side_effects(
        self,
        manifest: Manifest,
        *,
        batch_size: object,
        include_translations: object,
        include_code: object,
        expected_error: str,
    ) -> None:
        with (
            patch("i18nlib.review.create_run_directory") as create_directory,
            patch("i18nlib.review.LuaRuntime") as runtime_class,
            patch("i18nlib.review.LocaleLoader") as loader_class,
            patch(
                "i18nlib.review._write_translation_bundles"
            ) as write_translations,
            patch(
                "i18nlib.review._translation_items_from_bytes"
            ) as scan_translations,
            patch("i18nlib.review._write_code_bundles") as write_code,
            patch("i18nlib.review._code_items") as scan_code,
            patch("i18nlib.review.write_json") as write_json_mock,
            self.assertRaisesRegex(ValidationError, expected_error),
        ):
            create_review_index(
                manifest,
                batch_size=batch_size,  # type: ignore[arg-type]
                include_translations=include_translations,  # type: ignore[arg-type]
                include_code=include_code,  # type: ignore[arg-type]
            )

        create_directory.assert_not_called()
        runtime_class.assert_not_called()
        loader_class.assert_not_called()
        write_translations.assert_not_called()
        scan_translations.assert_not_called()
        write_code.assert_not_called()
        scan_code.assert_not_called()
        write_json_mock.assert_not_called()

    def test_create_review_index_rejects_non_integer_batch_size_before_side_effects(
        self,
    ) -> None:
        manifest = load_manifest()
        for batch_size in (True, 1.0, "1"):
            with self.subTest(batch_size=batch_size):
                self._assert_review_validation_has_no_side_effects(
                    manifest,
                    batch_size=batch_size,
                    include_translations=True,
                    include_code=False,
                    expected_error="review batch size must be an integer",
                )

    def test_create_review_index_rejects_out_of_range_batch_size_before_side_effects(
        self,
    ) -> None:
        manifest = load_manifest()
        for batch_size in (0, -1, MAX_REVIEW_BATCH_SIZE + 1):
            with self.subTest(batch_size=batch_size):
                self._assert_review_validation_has_no_side_effects(
                    manifest,
                    batch_size=batch_size,
                    include_translations=True,
                    include_code=False,
                    expected_error=(
                        "review batch size must be between 1 and "
                        f"{MAX_REVIEW_BATCH_SIZE}"
                    ),
                )

    def test_create_review_index_rejects_non_boolean_scopes_before_side_effects(
        self,
    ) -> None:
        manifest = load_manifest()
        invalid_values = (0, 1, "false", None)
        for parameter in ("include_translations", "include_code"):
            for invalid_value in invalid_values:
                with self.subTest(parameter=parameter, value=invalid_value):
                    arguments: dict[str, object] = {
                        "batch_size": 1,
                        "include_translations": True,
                        "include_code": True,
                    }
                    arguments[parameter] = invalid_value
                    self._assert_review_validation_has_no_side_effects(
                        manifest,
                        batch_size=arguments["batch_size"],
                        include_translations=arguments["include_translations"],
                        include_code=arguments["include_code"],
                        expected_error=f"review {parameter} must be a boolean",
                    )

    def test_create_review_index_requires_a_true_scope_before_side_effects(
        self,
    ) -> None:
        self._assert_review_validation_has_no_side_effects(
            load_manifest(),
            batch_size=1,
            include_translations=False,
            include_code=False,
            expected_error="review must include translations or code",
        )

    def test_create_review_index_accepts_batch_size_boundaries(self) -> None:
        manifest = load_manifest()
        run_directory = manifest.root / ".artifacts" / "i18n" / "review-fixture"
        for batch_size in (1, MAX_REVIEW_BATCH_SIZE):
            with (
                self.subTest(batch_size=batch_size),
                patch(
                    "i18nlib.review.create_run_directory",
                    return_value=run_directory,
                ),
                patch(
                    "i18nlib.review._write_code_bundles",
                    return_value=([], 0),
                ) as write_code,
                patch("i18nlib.review.write_json"),
            ):
                create_review_index(
                    manifest,
                    batch_size=batch_size,
                    include_translations=False,
                    include_code=True,
                )

            write_code.assert_called_once_with(
                run_directory, manifest, batch_size
            )

    def test_translation_review_rejects_more_than_ten_items(self) -> None:
        self._assert_review_validation_has_no_side_effects(
            load_manifest(),
            batch_size=11,
            include_translations=True,
            include_code=False,
            expected_error="translation review batch size must be between 1 and 10",
        )

    def _code_review_repository(self, root: Path) -> Path:
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        tracked = root / "tools" / "fixture.py"
        tracked.parent.mkdir(parents=True)
        tracked.write_text("one\ntwo\nthree\n", encoding="utf-8")
        subprocess.run(
            ["git", "-C", str(root), "add", "tools/fixture.py"], check=True
        )
        subprocess.run(
            [
                "git",
                "-C",
                str(root),
                "-c",
                "user.name=fixture",
                "-c",
                "user.email=fixture@example.invalid",
                "commit",
                "-qm",
                "fixture",
            ],
            check=True,
        )
        return tracked

    def test_pi_agent_analysis_is_in_public_review_scope(self) -> None:
        self.assertTrue(_is_public_review_path("pi-agent-analysis.md"))
        self.assertFalse(_is_public_review_path("private/pi-agent-analysis.md"))

    def test_fixed_public_review_roots_are_in_scope(self) -> None:
        for root in (".agents", ".codex", "docs", "i18n", "tools", "tests"):
            with self.subTest(root=root):
                self.assertTrue(_is_public_review_path(root))
                self.assertTrue(_is_public_review_path(f"{root}/fixture.txt"))
        self.assertFalse(_is_public_review_path(".github/fixture.txt"))

    def test_manifest_copy_and_manual_files_enter_code_items_and_bundle(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-manifest-files-"
        ) as temporary:
            root = Path(temporary)
            self._code_review_repository(root)
            original = load_manifest()
            component = replace(
                original.component("engine"),
                translation="canonical.lua",
                copy_fragment="engine.copy.lua",
            )
            manifest = replace(
                original,
                root=root,
                components=(component,),
                manual_definitions=("_tdef_append.lua",),
            )
            baseline_files = {
                "engine.copy.lua": "copy baseline\n",
                "_tdef_append.lua": "manual baseline\n",
                "canonical.lua": "translation baseline\n",
                "undeclared.lua": "undeclared baseline\n",
                "tools/lua/load_locale.lua": "-- loader bridge fixture\n",
            }
            for relative, content in baseline_files.items():
                path = root / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8")
            subprocess.run(["git", "-C", str(root), "add", "--all"], check=True)
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(root),
                    "-c",
                    "user.name=fixture",
                    "-c",
                    "user.email=fixture@example.invalid",
                    "commit",
                    "-qm",
                    "manifest files",
                ],
                check=True,
            )

            (root / "engine.copy.lua").write_text("copy staged\n", encoding="utf-8")
            subprocess.run(
                ["git", "-C", str(root), "add", "engine.copy.lua"], check=True
            )
            (root / "_tdef_append.lua").write_text(
                "manual unstaged\n", encoding="utf-8"
            )
            (root / "canonical.lua").write_text(
                "translation changed\n", encoding="utf-8"
            )
            (root / "undeclared.lua").write_text(
                "undeclared changed\n", encoding="utf-8"
            )

            self.assertTrue(_is_public_review_path("engine.copy.lua", manifest))
            self.assertTrue(_is_public_review_path("_tdef_append.lua", manifest))
            self.assertFalse(_is_public_review_path("canonical.lua", manifest))
            self.assertFalse(_is_public_review_path("undeclared.lua", manifest))

            paths = _git_status_paths(root, manifest)
            items, _ = _code_items(root, manifest)
            index = create_review_index(
                manifest,
                batch_size=100,
                include_translations=False,
                include_code=True,
            )
            bundle_files: list[dict[str, object]] = []
            for bundle in index["bundles"]:
                payload = json.loads(
                    Path(bundle["path"]).read_text(encoding="utf-8")
                )
                bundle_files.extend(payload["files"])

        self.assertEqual(
            {(status, path) for status, path, _ in paths},
            {("M ", "engine.copy.lua"), (" M", "_tdef_append.lua")},
        )
        self.assertEqual(
            {item["path"] for item in items},
            {"engine.copy.lua", "_tdef_append.lua"},
        )
        self.assertEqual(
            {item["path"] for item in bundle_files},
            {"engine.copy.lua", "_tdef_append.lua"},
        )

    def test_review_cli_requires_an_explicit_scope(self) -> None:
        with contextlib.redirect_stderr(io.StringIO()):
            with self.assertRaises(SystemExit):
                cli_parser().parse_args(["review"])
        arguments = cli_parser().parse_args(
            ["review", "--scope", "code", "--scope", "translations"]
        )
        self.assertEqual(arguments.scope, ["code", "translations"])

    def test_code_only_review_does_not_initialize_lua(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-code-only-"
        ) as temporary:
            root = Path(temporary)
            tracked = self._code_review_repository(root)
            tracked.write_text("changed\ntwo\nthree\n", encoding="utf-8")
            manifest = replace(load_manifest(), root=root)

            with (
                patch(
                    "i18nlib.review.LuaRuntime",
                    side_effect=AssertionError("code review initialized LuaRuntime"),
                ) as runtime_class,
                patch(
                    "i18nlib.review.LocaleLoader",
                    side_effect=AssertionError("code review initialized LocaleLoader"),
                ) as loader_class,
            ):
                index = create_review_index(
                    manifest,
                    batch_size=100,
                    include_translations=False,
                    include_code=True,
                )

            bundle = json.loads(
                Path(index["bundles"][0]["path"]).read_text(encoding="utf-8")
            )
            stored_index = json.loads(
                Path(index["index"]).read_text(encoding="utf-8")
            )

        runtime_class.assert_not_called()
        loader_class.assert_not_called()
        self.assertEqual(
            index["scope"],
            {
                "translations": False,
                "code": True,
                "protected_sources": False,
            },
        )
        self.assertEqual(len(index["bundles"]), 1)
        self.assertEqual(index["bundles"][0]["kind"], "code")
        self.assertEqual(stored_index, index)
        self.assertEqual(bundle["kind"], "code")
        self.assertEqual(
            [item["path"] for item in bundle["files"]], ["tools/fixture.py"]
        )

    def test_translation_enabled_review_initializes_one_loader_pair(self) -> None:
        manifest = load_manifest()
        run_directory = manifest.root / ".artifacts" / "i18n" / "review-fixture"
        translation_bundles = [
            {
                "bundle_id": "translation-fixture",
                "schema_version": TRANSLATION_REVIEW_SCHEMA_VERSION,
                "review_contract": TRANSLATION_REVIEW_BUNDLE_CONTRACT,
                "channel": TRANSLATION_REVIEW_CHANNEL,
                "kind": "translations",
                "component": "boot",
                "offset": 0,
                "count": 1,
                "total": 1,
                "path": str(run_directory / "translation.json"),
            }
        ]
        code_bundles = [
            {
                "bundle_id": "code-fixture",
                "schema_version": REVIEW_SCHEMA_VERSION,
                "review_contract": REVIEW_CONTRACT,
                "channel": "code-findings",
                "kind": "code",
                "offset": 0,
                "count": 1,
                "total": 1,
                "path": str(run_directory / "code.json"),
            }
        ]

        with (
            patch(
                "i18nlib.review.create_run_directory",
                return_value=run_directory,
            ) as create_directory,
            patch("i18nlib.review.LuaRuntime") as runtime_class,
            patch("i18nlib.review.LocaleLoader") as loader_class,
            patch(
                "i18nlib.review._write_translation_bundles",
                return_value=translation_bundles,
            ) as write_translations,
            patch(
                "i18nlib.review._write_code_bundles",
                return_value=(code_bundles, 0),
            ) as write_code,
            patch("i18nlib.review.write_json") as write_json_mock,
        ):
            index = create_review_index(
                manifest,
                batch_size=10,
                include_translations=True,
                include_code=True,
            )

        runtime_class.assert_called_once_with(manifest)
        loader_class.assert_called_once_with(runtime_class.return_value)
        create_directory.assert_called_once_with(manifest.root, "review")
        write_translations.assert_called_once_with(
            run_directory,
            manifest,
            loader_class.return_value,
            10,
            24000,
        )
        write_code.assert_called_once_with(run_directory, manifest, 10)
        self.assertEqual(index["bundles"], translation_bundles + code_bundles)
        self.assertEqual(index["schema_version"], REVIEW_INDEX_SCHEMA_VERSION)
        self.assertEqual(index["review_contract"], REVIEW_INDEX_CONTRACT)
        write_json_mock.assert_called_once_with(
            run_directory / "review-index.json", index
        )

    def test_code_review_includes_staged_only_modification(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-staged-modify-"
        ) as temporary:
            root = Path(temporary)
            tracked = self._code_review_repository(root)
            tracked.write_text("staged\ntwo\nthree\n", encoding="utf-8")
            subprocess.run(
                ["git", "-C", str(root), "add", "tools/fixture.py"], check=True
            )

            items, _ = _code_items(root)

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["status"], "M ")
        self.assertIn("--- a/tools/fixture.py", items[0]["diff"])
        self.assertIn("-one", items[0]["diff"])
        self.assertIn("+staged", items[0]["diff"])
        self.assertNotIn("--- /dev/null", items[0]["diff"])

    def test_code_review_preserves_dev_null_for_staged_new_file(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-staged-new-"
        ) as temporary:
            root = Path(temporary)
            self._code_review_repository(root)
            staged = root / "tools" / "staged.py"
            staged.write_text(
                'source = "/Users/fixture/private.txt"\n', encoding="utf-8"
            )
            subprocess.run(
                ["git", "-C", str(root), "add", "tools/staged.py"], check=True
            )

            items, redactions = _code_items(root)

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["status"], "A ")
        self.assertIn("new file mode", items[0]["diff"])
        self.assertIn("--- /dev/null", items[0]["diff"])
        self.assertIn("+++ b/tools/staged.py", items[0]["diff"])
        self.assertNotIn("/Users/fixture", items[0]["diff"])
        self.assertIn("<redacted-absolute-path>", items[0]["diff"])
        self.assertEqual(redactions, 1)

    def test_code_review_includes_staged_only_deletion(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-staged-delete-"
        ) as temporary:
            root = Path(temporary)
            tracked = self._code_review_repository(root)
            tracked.unlink()
            subprocess.run(
                ["git", "-C", str(root), "add", "-u", "tools/fixture.py"],
                check=True,
            )

            items, redactions = _code_items(root)

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["status"], "D ")
        self.assertIn("deleted file mode", items[0]["diff"])
        self.assertIn("--- a/tools/fixture.py", items[0]["diff"])
        self.assertIn("+++ /dev/null", items[0]["diff"])
        self.assertIn("-one", items[0]["diff"])
        self.assertEqual(redactions, 0)

    def test_code_review_combines_staged_and_unstaged_changes(self) -> None:
        with tempfile.TemporaryDirectory(prefix="tome4-review-mixed-") as temporary:
            root = Path(temporary)
            tracked = self._code_review_repository(root)
            tracked.write_text("staged\ntwo\nthree\n", encoding="utf-8")
            subprocess.run(
                ["git", "-C", str(root), "add", "tools/fixture.py"], check=True
            )
            tracked.write_text("staged\nunstaged\nthree\n", encoding="utf-8")

            items, _ = _code_items(root)

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["status"], "MM")
        self.assertIn("-one", items[0]["diff"])
        self.assertIn("+staged", items[0]["diff"])
        self.assertIn("-two", items[0]["diff"])
        self.assertIn("+unstaged", items[0]["diff"])
        self.assertNotIn("--- /dev/null", items[0]["diff"])

    def test_code_review_synthesizes_addition_only_for_untracked_file(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-untracked-"
        ) as temporary:
            root = Path(temporary)
            self._code_review_repository(root)
            untracked = root / "tools" / "untracked.py"
            untracked.write_text("untracked\n", encoding="utf-8")

            raw_diff = _git_diff(root, "tools/untracked.py", untracked=True)
            items, redactions = _code_items(root)

        self.assertTrue(raw_diff.startswith("--- /dev/null\n"))
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["path"], "tools/untracked.py")
        self.assertEqual(items[0]["status"], "??")
        self.assertIn("--- /dev/null", items[0]["diff"])
        self.assertIn("+++ b/tools/untracked.py", items[0]["diff"])
        self.assertIn("untracked\n", items[0]["diff"])
        self.assertEqual(redactions, 0)

    def test_code_review_includes_unicode_untracked_path(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-unicode-untracked-"
        ) as temporary:
            root = Path(temporary)
            self._code_review_repository(root)
            untracked = root / "tools" / "中文.py"
            untracked.write_text("unicode path\n", encoding="utf-8")

            items, _ = _code_items(root)

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["path"], "tools/中文.py")
        self.assertEqual(items[0]["status"], "??")
        self.assertIn("+++ b/tools/中文.py", items[0]["diff"])

    def test_git_status_paths_preserves_literal_rename_marker(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-literal-arrow-"
        ) as temporary:
            root = Path(temporary)
            self._code_review_repository(root)
            ordinary = root / "tools" / "literal -> marker.py"
            ordinary.write_text("before\n", encoding="utf-8")
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(root),
                    "add",
                    "--",
                    "tools/literal -> marker.py",
                ],
                check=True,
            )
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(root),
                    "-c",
                    "user.name=fixture",
                    "-c",
                    "user.email=fixture@example.invalid",
                    "commit",
                    "-qm",
                    "literal arrow fixture",
                ],
                check=True,
            )
            ordinary.write_text("after\n", encoding="utf-8")

            paths = _git_status_paths(root)

        self.assertEqual(paths, [(" M", "tools/literal -> marker.py", None)])

    def test_code_review_includes_both_sides_of_public_rename(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-tracked-rename-"
        ) as temporary:
            root = Path(temporary)
            tracked = self._code_review_repository(root)
            destination = root / "tools" / "renamed.py"
            tracked.rename(destination)
            subprocess.run(
                ["git", "-C", str(root), "add", "--all"], check=True
            )

            paths = _git_status_paths(root)
            items, _ = _code_items(root)

        self.assertEqual(
            paths,
            [
                ("R ", "tools/renamed.py", "tools/fixture.py"),
            ],
        )
        self.assertEqual(len(items), 2)
        by_path = {item["path"]: item for item in items}
        self.assertEqual(set(by_path), {"tools/fixture.py", "tools/renamed.py"})
        self.assertEqual(by_path["tools/fixture.py"]["status"], "R ")
        self.assertIn("deleted file mode", by_path["tools/fixture.py"]["diff"])
        self.assertIn("--- a/tools/fixture.py", by_path["tools/fixture.py"]["diff"])
        self.assertEqual(by_path["tools/renamed.py"]["status"], "R ")
        self.assertIn("new file mode", by_path["tools/renamed.py"]["diff"])
        self.assertIn("+++ b/tools/renamed.py", by_path["tools/renamed.py"]["diff"])

    def test_code_review_keeps_rename_source_and_untracked_replacement(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-rename-replacement-"
        ) as temporary:
            root = Path(temporary)
            tracked = self._code_review_repository(root)
            destination = root / "tools" / "renamed.py"
            tracked.rename(destination)
            subprocess.run(
                ["git", "-C", str(root), "add", "--all"], check=True
            )
            tracked.write_text("replacement\n", encoding="utf-8")

            paths = _git_status_paths(root)
            items, _ = _code_items(root)

        self.assertEqual(
            paths,
            [
                ("R ", "tools/renamed.py", "tools/fixture.py"),
                ("??", "tools/fixture.py", None),
            ],
        )
        self.assertEqual(
            [(item["status"], item["path"]) for item in items],
            [
                ("R ", "tools/renamed.py"),
                ("R ", "tools/fixture.py"),
                ("??", "tools/fixture.py"),
            ],
        )
        renamed, removed, replacement = items
        self.assertIn("+++ b/tools/renamed.py", renamed["diff"])
        self.assertIn("deleted file mode", removed["diff"])
        self.assertIn("--- a/tools/fixture.py", removed["diff"])
        self.assertIn("-one", removed["diff"])
        self.assertIn("+++ b/tools/fixture.py", replacement["diff"])
        self.assertIn("replacement\n", replacement["diff"])

    def test_code_review_keeps_public_source_when_rename_leaves_scope(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-rename-outside-scope-"
        ) as temporary:
            root = Path(temporary)
            tracked = self._code_review_repository(root)
            destination = root / "private" / "renamed.py"
            destination.parent.mkdir()
            tracked.rename(destination)
            subprocess.run(
                ["git", "-C", str(root), "add", "--all"], check=True
            )

            paths = _git_status_paths(root)
            items, _ = _code_items(root)

        self.assertEqual(
            paths,
            [("D ", "tools/fixture.py", None)],
        )
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["path"], "tools/fixture.py")
        self.assertEqual(items[0]["status"], "D ")
        self.assertIn("deleted file mode", items[0]["diff"])
        self.assertIn("--- a/tools/fixture.py", items[0]["diff"])
        self.assertNotIn("private/renamed.py", items[0]["diff"])

    def test_code_review_keeps_public_destination_when_rename_enters_scope(
        self,
    ) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-rename-into-scope-"
        ) as temporary:
            root = Path(temporary)
            tracked = self._code_review_repository(root)
            source = root / "private" / "fixture.py"
            source.parent.mkdir()
            tracked.rename(source)
            subprocess.run(
                ["git", "-C", str(root), "add", "--all"], check=True
            )
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(root),
                    "-c",
                    "user.name=fixture",
                    "-c",
                    "user.email=fixture@example.invalid",
                    "commit",
                    "-qm",
                    "private fixture",
                ],
                check=True,
            )
            destination = root / "tools" / "renamed.py"
            source.rename(destination)
            subprocess.run(
                ["git", "-C", str(root), "add", "--all"], check=True
            )

            paths = _git_status_paths(root)
            items, _ = _code_items(root)

        self.assertEqual(
            paths,
            [("A ", "tools/renamed.py", None)],
        )
        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["path"], "tools/renamed.py")
        self.assertEqual(items[0]["status"], "A ")
        self.assertIn("new file mode", items[0]["diff"])
        self.assertIn("+++ b/tools/renamed.py", items[0]["diff"])
        self.assertNotIn("private/fixture.py", items[0]["diff"])

    def test_git_status_paths_keeps_copy_source_and_reviews_public_copy(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-tracked-copy-"
        ) as temporary:
            root = Path(temporary)
            tracked = self._code_review_repository(root)
            subprocess.run(
                ["git", "-C", str(root), "config", "status.renames", "copies"],
                check=True,
            )
            destination = root / "tests" / "copied.py"
            destination.parent.mkdir()
            destination.write_bytes(tracked.read_bytes())
            tracked.write_text("one\ntwo\nthree\nsource changed\n", encoding="utf-8")
            subprocess.run(
                [
                    "git",
                    "-C",
                    str(root),
                    "add",
                    "tests/copied.py",
                    "tools/fixture.py",
                ],
                check=True,
            )

            paths = _git_status_paths(root)
            items, _ = _code_items(root)

        self.assertEqual(
            paths,
            [
                ("C ", "tests/copied.py", "tools/fixture.py"),
                ("M ", "tools/fixture.py", None),
            ],
        )
        self.assertEqual(len(items), 2)
        by_path = {item["path"]: item for item in items}
        self.assertEqual(set(by_path), {"tests/copied.py", "tools/fixture.py"})
        self.assertEqual(by_path["tests/copied.py"]["status"], "C ")
        self.assertIn("+++ b/tests/copied.py", by_path["tests/copied.py"]["diff"])
        self.assertEqual(by_path["tools/fixture.py"]["status"], "M ")
        self.assertIn("+source changed", by_path["tools/fixture.py"]["diff"])

    def test_git_status_paths_preserves_tab_and_newline(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-control-paths-"
        ) as temporary:
            root = Path(temporary)
            self._code_review_repository(root)
            expected = [
                ("??", "tools/tab\tname.py", None),
                ("??", "tools/line\nname.py", None),
            ]
            for _, relative, _ in expected:
                (root / relative).write_text("control path\n", encoding="utf-8")

            paths = _git_status_paths(root)

        self.assertCountEqual(paths, expected)


if __name__ == "__main__":
    unittest.main()
