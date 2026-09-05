"""Toolchain tests: review diff."""

from __future__ import annotations

from tests.i18n import toolchain_fixtures
from tests.i18n.toolchain_fixtures import ROOT, TOOLS
import contextlib
from dataclasses import replace
import io
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, call, patch
import review_diff
from i18nlib.config import load_manifest
from i18nlib.locale_model import LocaleLoader
from i18nlib.quality import compute_unit_id
from i18nlib.runtime import LuaRuntime


class ReviewDiffTests(unittest.TestCase):
    TERMINOLOGY_HEADER = (
        "source\ttarget\tcategory\tsource_tag\tstatus\tscope\tnotes\n"
    ).encode("utf-8")

    @staticmethod
    def _commit_repository(root: Path, files: dict[str, bytes]) -> str:
        subprocess.run(["git", "init", "-q", str(root)], check=True)
        for relative, content in files.items():
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(content)
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
                "baseline",
            ],
            check=True,
        )
        return review_diff._resolve_baseline_tree(root, "HEAD")

    @staticmethod
    def _initialize_repository(root: Path) -> str:
        return ReviewDiffTests._commit_repository(
            root,
            {
                "locale.lua": b"baseline locale\n",
                "empty.lua": b"",
            },
        )

    @staticmethod
    def _translation(
        source: str,
        target: str,
        *,
        section: str = "fixture.lua",
        source_tag: str | None = None,
        args_order: object = None,
        special: object = None,
    ) -> dict[str, object]:
        return {
            "section": section,
            "source": source,
            "target": target,
            "source_tag": source_tag,
            "args_order": args_order,
            "special": special,
            "line": 1,
        }

    def _review_manifest_fixture(
        self,
        root: Path,
        locales: tuple[tuple[str, str, bytes, bytes], ...],
        *,
        terminology: bytes | None = None,
    ) -> object:
        original = load_manifest()
        baseline_files = {
            relative: baseline
            for _, relative, baseline, _ in locales
        }
        baseline_files["tools/lua/load_locale.lua"] = (
            TOOLS / "lua" / "load_locale.lua"
        ).read_bytes()
        baseline_files["terminology.tsv"] = (
            self.TERMINOLOGY_HEADER
            if terminology is None
            else terminology
        )
        baseline_files["i18n/review/translation-semantic-v2.json"] = (
            ROOT / "i18n" / "review" / "translation-semantic-v2.json"
        ).read_bytes()
        self._commit_repository(root, baseline_files)
        for _, relative, _, current in locales:
            (root / relative).write_bytes(current)
        components = tuple(
            replace(
                original.components[index],
                id=component_id,
                translation=relative,
            )
            for index, (component_id, relative, _, _) in enumerate(locales)
        )
        return replace(
            original,
            root=root,
            components=components,
            terminology="terminology.tsv",
        )

    @staticmethod
    def _run_review_diff(
        root: Path,
        manifest: object,
        output: Path,
    ) -> tuple[int, str, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with (
            patch.object(review_diff, "ROOT", root),
            patch.object(review_diff, "load_manifest", return_value=manifest),
            patch.object(review_diff.signal, "alarm"),
            contextlib.redirect_stdout(stdout),
            contextlib.redirect_stderr(stderr),
        ):
            exit_code = review_diff.main(
                ["--baseline", "HEAD", "--out-dir", str(output)]
            )
        return exit_code, stdout.getvalue(), stderr.getvalue()

    def _assert_failed_run_is_clean(
        self,
        *,
        exit_code: int,
        stdout: str,
        stderr: str,
        output: Path,
    ) -> None:
        self.assertEqual(exit_code, 2)
        self.assertEqual(stdout, "")
        self.assertIn("error: ", stderr)
        self.assertNotIn("Traceback", stderr)
        self.assertFalse(output.exists())
        self.assertEqual(
            list(output.parent.glob(f".{output.name}.staging-*")),
            [],
        )

    def test_invalid_second_current_locale_does_not_publish_first_bundle(self) -> None:
        baseline = b'section("fixture.lua")\nt("source", "old")\n'
        changed = b'section("fixture.lua")\nt("source", "new")\n'
        invalid = b'section("broken"\n'
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-diff-current-parse-"
        ) as temporary:
            root = Path(temporary)
            manifest = self._review_manifest_fixture(
                root,
                (
                    ("first", "locale/first.lua", baseline, changed),
                    ("second", "locale/second.lua", baseline, invalid),
                ),
            )
            output = root / "output"

            exit_code, stdout, stderr = self._run_review_diff(
                root, manifest, output
            )

            self._assert_failed_run_is_clean(
                exit_code=exit_code,
                stdout=stdout,
                stderr=stderr,
                output=output,
            )
        self.assertIn("Lua locale load failed for locale/second.lua", stderr)

    def test_invalid_baseline_locale_is_controlled_and_not_published(self) -> None:
        invalid = b'section("broken"\n'
        current = b'section("fixture.lua")\nt("source", "new")\n'
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-diff-baseline-parse-"
        ) as temporary:
            root = Path(temporary)
            manifest = self._review_manifest_fixture(
                root,
                (("fixture", "locale/fixture.lua", invalid, current),),
            )
            output = root / "output"

            exit_code, stdout, stderr = self._run_review_diff(
                root, manifest, output
            )

            self._assert_failed_run_is_clean(
                exit_code=exit_code,
                stdout=stdout,
                stderr=stderr,
                output=output,
            )
        self.assertIn("Lua locale load failed for locale/fixture.lua", stderr)

    def test_invalid_terminology_does_not_block_blind_semantic_review(self) -> None:
        locale = b'section("fixture.lua")\nt("source", "target")\n'
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-diff-terminology-parse-"
        ) as temporary:
            root = Path(temporary)
            manifest = self._review_manifest_fixture(
                root,
                (("fixture", "locale/fixture.lua", locale, locale),),
                terminology=b"source\ttarget\nsource\ttarget\n",
            )
            output = root / "output"

            exit_code, stdout, stderr = self._run_review_diff(
                root, manifest, output
            )

            self.assertEqual(exit_code, 0, stderr)
            self.assertEqual(stderr, "")
            self.assertTrue(output.is_dir())
            index = json.loads(
                (output / "review-index.json").read_text(encoding="utf-8")
            )
            self.assertEqual(index["bundles"], [])
        self.assertIn("changed entries: 0, bundles: 0", stdout)

    def test_success_preserves_artifact_bytes_ids_and_final_paths(self) -> None:
        baseline = b'section("fixture.lua")\nt("source", "old")\n'
        current = b'section("fixture.lua")\nt("source", "new")\n'
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-diff-artifact-semantics-"
        ) as temporary:
            root = Path(temporary)
            manifest = self._review_manifest_fixture(
                root,
                (("fixture", "locale/fixture.lua", baseline, current),),
            )
            output = root / "output"

            exit_code, stdout, stderr = self._run_review_diff(
                root, manifest, output
            )

            self.assertEqual(exit_code, 0, stderr)
            self.assertEqual(stderr, "")
            index_path = output / "review-index.json"
            index_bytes = index_path.read_bytes()
            index = json.loads(index_bytes)
            self.assertEqual(len(index["bundles"]), 1)
            bundle_record = index["bundles"][0]
            bundle_path = Path(bundle_record["path"])
            self.assertEqual(
                bundle_path,
                output
                / "translations"
                / "fixture"
                / f'{bundle_record["bundle_id"]}.json',
            )
            bundle_bytes = bundle_path.read_bytes()
            bundle = json.loads(bundle_bytes)

            bundle_identity = dict(bundle)
            bundle_identity.pop("bundle_id")
            self.assertEqual(
                bundle["bundle_id"], review_diff._bundle_id(bundle_identity)
            )
            index_identity = dict(index)
            index_identity.pop("review_id")
            self.assertEqual(
                index["review_id"],
                review_diff._review_index_id(index_identity),
            )
            self.assertEqual(
                bundle_bytes,
                (
                    json.dumps(
                        bundle, ensure_ascii=False, sort_keys=True, indent=2
                    )
                    + "\n"
                ).encode("utf-8"),
            )
            self.assertEqual(
                index_bytes,
                (
                    json.dumps(
                        index, ensure_ascii=False, sort_keys=True, indent=2
                    )
                    + "\n"
                ).encode("utf-8"),
            )
            self.assertNotIn(b".staging-", bundle_bytes)
            self.assertNotIn(b".staging-", index_bytes)
            self.assertEqual(
                stdout,
                "\n".join(
                    (
                        "baseline: HEAD",
                        "changed entries: 1, bundles: 1",
                        f'review_id: {index["review_id"]}',
                        f"run_dir: {output}",
                        "",
                    )
                ),
            )

    def test_staged_write_failure_leaves_no_final_or_staging_directory(self) -> None:
        baseline = b'section("fixture.lua")\nt("source", "old")\n'
        current = b'section("fixture.lua")\nt("source", "new")\n'
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-diff-staged-write-"
        ) as temporary:
            root = Path(temporary)
            manifest = self._review_manifest_fixture(
                root,
                (("fixture", "locale/fixture.lua", baseline, current),),
            )
            output = root / "output"
            write_json = review_diff._write_json

            def fail_on_index(path: Path, payload: dict[str, object]) -> None:
                if path.name == "review-index.json":
                    raise OSError("fixture staged index failure")
                write_json(path, payload)

            with patch.object(
                review_diff, "_write_json", side_effect=fail_on_index
            ):
                exit_code, stdout, stderr = self._run_review_diff(
                    root, manifest, output
                )

            self._assert_failed_run_is_clean(
                exit_code=exit_code,
                stdout=stdout,
                stderr=stderr,
                output=output,
            )
        self.assertIn("fixture staged index failure", stderr)

    def test_existing_explicit_output_is_rejected_without_overwrite(self) -> None:
        baseline = b'section("fixture.lua")\nt("source", "old")\n'
        current = b'section("fixture.lua")\nt("source", "new")\n'
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-diff-existing-output-"
        ) as temporary:
            root = Path(temporary)
            manifest = self._review_manifest_fixture(
                root,
                (("fixture", "locale/fixture.lua", baseline, current),),
            )
            output = root / "output"
            output.mkdir()
            sentinel = output / "keep.txt"
            sentinel.write_text("keep", encoding="utf-8")

            exit_code, stdout, stderr = self._run_review_diff(
                root, manifest, output
            )

            self.assertEqual(exit_code, 2)
            self.assertEqual(stdout, "")
            self.assertNotIn("Traceback", stderr)
            self.assertIn("refusing to overwrite", stderr)
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "keep")
            self.assertEqual(list(output.iterdir()), [sentinel])

    def test_output_parent_creation_failure_is_controlled(self) -> None:
        baseline = b'section("fixture.lua")\nt("source", "old")\n'
        current = b'section("fixture.lua")\nt("source", "new")\n'
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-diff-parent-failure-"
        ) as temporary:
            root = Path(temporary)
            manifest = self._review_manifest_fixture(
                root,
                (("fixture", "locale/fixture.lua", baseline, current),),
            )
            blocked_parent = root / "blocked-parent"
            blocked_parent.write_text("not a directory", encoding="utf-8")
            output = blocked_parent / "output"

            exit_code, stdout, stderr = self._run_review_diff(
                root, manifest, output
            )

            self.assertEqual(exit_code, 2)
            self.assertEqual(stdout, "")
            self.assertIn("error: ", stderr)
            self.assertNotIn("Traceback", stderr)
            self.assertFalse(output.exists())

    def test_invalid_baseline_returns_nonzero_with_clear_error(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-diff-invalid-"
        ) as temporary:
            root = Path(temporary)
            subprocess.run(["git", "init", "-q", str(root)], check=True)
            stderr = io.StringIO()
            alarm = Mock()
            with (
                patch.object(review_diff, "ROOT", root),
                patch.object(review_diff.signal, "alarm", alarm),
                contextlib.redirect_stderr(stderr),
            ):
                exit_code = review_diff.main(["--baseline", "missing-baseline"])

        self.assertEqual(exit_code, 2)
        self.assertIn("error: cannot resolve baseline", stderr.getvalue())
        self.assertIn("as a commit or tree", stderr.getvalue())
        self.assertEqual(alarm.call_args_list, [call(600), call(0)])

    def test_cli_rejects_out_of_range_batch_sizes_before_side_effects(self) -> None:
        invalid_sizes = (0, -1, review_diff.MAX_REVIEW_BATCH_SIZE + 1)
        for batch_size in invalid_sizes:
            with self.subTest(batch_size=batch_size), tempfile.TemporaryDirectory(
                prefix="tome4-review-diff-batch-invalid-"
            ) as temporary:
                root = Path(temporary)
                output = root / "output"
                stderr = io.StringIO()
                alarm = Mock()
                with (
                    patch.object(review_diff, "ROOT", root),
                    patch.object(
                        review_diff, "_resolve_baseline_tree"
                    ) as resolve_baseline,
                    patch.object(review_diff.signal, "alarm", alarm),
                    contextlib.redirect_stderr(stderr),
                    self.assertRaises(SystemExit) as raised,
                ):
                    review_diff.main(
                        [
                            "--baseline",
                            "missing-baseline",
                            "--batch-size",
                            str(batch_size),
                            "--out-dir",
                            str(output),
                        ]
                    )

                self.assertEqual(raised.exception.code, 2)
                self.assertIn(
                    "review batch size must be between 1 and "
                    f"{review_diff.MAX_REVIEW_BATCH_SIZE}",
                    stderr.getvalue(),
                )
                resolve_baseline.assert_not_called()
                self.assertFalse(output.exists())
                self.assertEqual(alarm.call_args_list, [call(600), call(0)])

    def test_cli_accepts_minimum_and_maximum_batch_sizes(self) -> None:
        manifest = load_manifest()
        component = manifest.component("example")
        manifest = replace(manifest, components=(component,))
        current_document = LocaleLoader(LuaRuntime(manifest)).load_path(
            manifest.root / component.translation,
            logical_path=component.translation,
        )
        expected_count = len(current_document.translations)
        self.assertGreater(expected_count, 0)

        with tempfile.TemporaryDirectory(
            prefix="tome4-review-diff-batch-boundary-"
        ) as temporary:
            root = Path(temporary)
            self._commit_repository(root, {"unrelated.txt": b"fixture\n"})
            for batch_size in (1, review_diff.MAX_REVIEW_BATCH_SIZE):
                with self.subTest(batch_size=batch_size):
                    output = root / f"output-{batch_size}"
                    stderr = io.StringIO()
                    alarm = Mock()
                    with (
                        patch.object(review_diff, "ROOT", root),
                        patch.object(
                            review_diff, "load_manifest", return_value=manifest
                        ),
                        patch.object(review_diff.signal, "alarm", alarm),
                        contextlib.redirect_stdout(io.StringIO()),
                        contextlib.redirect_stderr(stderr),
                    ):
                        exit_code = review_diff.main(
                            [
                                "--baseline",
                                "HEAD",
                                "--batch-size",
                                str(batch_size),
                                "--out-dir",
                                str(output),
                            ]
                        )

                    self.assertEqual(exit_code, 0, stderr.getvalue())
                    self.assertEqual(stderr.getvalue(), "")
                    index = json.loads(
                        (output / "review-index.json").read_text(encoding="utf-8")
                    )
                    self.assertEqual(
                        sum(bundle["count"] for bundle in index["bundles"]),
                        expected_count,
                    )
                    self.assertTrue(
                        all(
                            1 <= bundle["count"] <= batch_size
                            for bundle in index["bundles"]
                        )
                    )
                    self.assertEqual(
                        alarm.call_args_list, [call(600), call(0)]
                    )

    def test_alarm_is_cancelled_when_review_generation_raises(self) -> None:
        alarm = Mock()
        with (
            patch.object(
                review_diff, "_resolve_baseline_tree", return_value="0" * 40
            ),
            patch.object(
                review_diff,
                "load_manifest",
                side_effect=RuntimeError("fixture failure"),
            ),
            patch.object(review_diff.signal, "alarm", alarm),
            self.assertRaisesRegex(RuntimeError, "fixture failure"),
        ):
            review_diff.main(["--baseline", "HEAD"])

        self.assertEqual(alarm.call_args_list, [call(600), call(0)])

    def test_missing_current_translation_returns_nonzero_without_output(self) -> None:
        original = load_manifest()
        component = replace(
            original.component("example"),
            id="missing-current",
            translation="locale/missing.lua",
        )
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-diff-current-missing-"
        ) as temporary:
            root = Path(temporary)
            self._commit_repository(root, {"unrelated.txt": b"fixture\n"})
            manifest = replace(original, root=root, components=(component,))
            output = root / "nested" / "output"
            stderr = io.StringIO()
            alarm = Mock()
            with (
                patch.object(review_diff, "ROOT", root),
                patch.object(review_diff, "load_manifest", return_value=manifest),
                patch.object(review_diff.signal, "alarm", alarm),
                contextlib.redirect_stdout(io.StringIO()),
                contextlib.redirect_stderr(stderr),
            ):
                exit_code = review_diff.main(
                    ["--baseline", "HEAD", "--out-dir", str(output)]
                )

            self.assertFalse(output.exists())

        self.assertEqual(exit_code, 2)
        self.assertIn("missing or not regular files", stderr.getvalue())
        self.assertIn("component 'missing-current'", stderr.getvalue())
        self.assertIn("locale/missing.lua", stderr.getvalue())
        self.assertEqual(alarm.call_args_list, [call(600), call(0)])

    def test_translation_preflight_aggregates_all_invalid_paths(self) -> None:
        original = load_manifest()
        template = original.component("example")
        components = (
            replace(
                template,
                id="missing-alpha",
                translation="locale/missing-alpha.lua",
            ),
            replace(
                template,
                id="not-regular-beta",
                translation="locale/not-regular-beta.lua",
            ),
        )
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-diff-current-invalid-"
        ) as temporary:
            root = Path(temporary)
            (root / "locale" / "not-regular-beta.lua").mkdir(parents=True)
            manifest = replace(original, root=root, components=components)

            with self.assertRaises(review_diff.ReviewDiffError) as caught:
                review_diff._preflight_translation_paths(manifest)

        message = str(caught.exception)
        self.assertIn("component 'missing-alpha': locale/missing-alpha.lua", message)
        self.assertIn(
            "component 'not-regular-beta': locale/not-regular-beta.lua",
            message,
        )
        self.assertLess(message.index("missing-alpha"), message.index("not-regular-beta"))

    def test_cli_continues_when_all_current_translation_files_exist(self) -> None:
        original = load_manifest()
        component = original.component("example")
        manifest = replace(original, components=(component,))
        translation_path = manifest.root / component.translation
        self.assertTrue(translation_path.is_file())
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-diff-current-complete-"
        ) as temporary:
            root = Path(temporary)
            self._commit_repository(
                root, {component.translation: translation_path.read_bytes()}
            )
            output = root / "output"
            stderr = io.StringIO()
            alarm = Mock()
            with (
                patch.object(review_diff, "ROOT", root),
                patch.object(review_diff, "load_manifest", return_value=manifest),
                patch.object(review_diff.signal, "alarm", alarm),
                contextlib.redirect_stdout(io.StringIO()),
                contextlib.redirect_stderr(stderr),
            ):
                exit_code = review_diff.main(
                    ["--baseline", "HEAD", "--out-dir", str(output)]
                )

            index = json.loads(
                (output / "review-index.json").read_text(encoding="utf-8")
            )

        self.assertEqual(exit_code, 0, stderr.getvalue())
        self.assertEqual(stderr.getvalue(), "")
        self.assertEqual(index["bundles"], [])
        self.assertEqual(alarm.call_args_list, [call(600), call(0)])

    def test_unreadable_baseline_blob_returns_nonzero_with_clear_error(self) -> None:
        manifest = load_manifest()
        component = manifest.component("example")
        manifest = replace(manifest, components=(component,))
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-diff-unreadable-"
        ) as temporary:
            root = Path(temporary)
            self._commit_repository(
                root,
                {component.translation: b"baseline locale\n"},
            )
            object_name = subprocess.run(
                [
                    "git",
                    "-C",
                    str(root),
                    "rev-parse",
                    f"HEAD:{component.translation}",
                ],
                check=True,
                capture_output=True,
                text=True,
            ).stdout.strip()
            object_path = (
                root / ".git" / "objects" / object_name[:2] / object_name[2:]
            )
            self.assertTrue(object_path.is_file())
            object_path.unlink()

            output = root / "output"
            stderr = io.StringIO()
            with (
                patch.object(review_diff, "ROOT", root),
                patch.object(review_diff, "load_manifest", return_value=manifest),
                patch.object(review_diff.signal, "alarm"),
                contextlib.redirect_stdout(io.StringIO()),
                contextlib.redirect_stderr(stderr),
            ):
                exit_code = review_diff.main(
                    ["--baseline", "HEAD", "--out-dir", str(output)]
                )
            self.assertFalse((output / "review-index.json").exists())

        self.assertEqual(exit_code, 2)
        self.assertIn("error: cannot read baseline path", stderr.getvalue())

    def test_baseline_blob_preserves_content_and_empty_file(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-diff-blob-"
        ) as temporary:
            root = Path(temporary)
            tree = self._initialize_repository(root)

            content = review_diff._read_baseline_blob(root, tree, "locale.lua")
            empty = review_diff._read_baseline_blob(root, tree, "empty.lua")

        self.assertEqual(content, b"baseline locale\n")
        self.assertEqual(empty, b"")

    def test_baseline_blob_returns_none_only_for_missing_path(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-diff-missing-"
        ) as temporary:
            root = Path(temporary)
            tree = self._initialize_repository(root)

            missing = review_diff._read_baseline_blob(root, tree, "new-locale.lua")

        self.assertIsNone(missing)

    def test_baseline_git_read_failure_is_not_treated_as_missing(self) -> None:
        with tempfile.TemporaryDirectory(
            prefix="tome4-review-diff-read-failure-"
        ) as temporary:
            root = Path(temporary)
            self._initialize_repository(root)

            with self.assertRaisesRegex(
                review_diff.ReviewDiffError, "cannot inspect baseline path"
            ):
                review_diff._read_baseline_blob(root, "0" * 40, "locale.lua")

    def test_new_translation_file_produces_all_bundle_items(self) -> None:
        current = [
            self._translation("first", "第一"),
            self._translation("second", "第二"),
        ]

        items = review_diff._changed_translation_items("fixture", current, None)

        self.assertEqual([item["ordinal"] for item in items], [0, 1])
        self.assertEqual([item["source"] for item in items], ["first", "second"])
        self.assertTrue(all(item["component"] == "fixture" for item in items))

    def test_target_only_change_produces_bundle_item(self) -> None:
        baseline = [self._translation("changed", "旧译")]
        current = [self._translation("changed", "新译")]

        items = review_diff._changed_translation_items("fixture", current, baseline)

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["target"], "新译")

    def test_cross_section_runtime_key_change_is_not_masked(self) -> None:
        baseline = [
            self._translation("same", "甲", section="a.lua"),
            self._translation("same", "乙", section="b.lua"),
        ]
        current = [
            self._translation("same", "乙", section="a.lua"),
            self._translation("same", "乙", section="b.lua"),
        ]

        items = review_diff._changed_translation_items("fixture", current, baseline)

        self.assertEqual(
            [
                (item["ordinal"], item["section"], item["target"])
                for item in items
            ],
            [(0, "a.lua", "乙")],
        )

    def test_section_only_move_produces_bundle_item(self) -> None:
        baseline = [self._translation("moved", "译文", section="old.lua")]
        current = [self._translation("moved", "译文", section="new.lua")]

        items = review_diff._changed_translation_items("fixture", current, baseline)

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["section"], "new.lua")

    def test_identical_duplicate_occurrences_consume_distinct_baselines(self) -> None:
        baseline = [
            self._translation("duplicate", "译文"),
            self._translation("duplicate", "译文"),
        ]
        current = [
            self._translation("duplicate", "译文"),
            self._translation("duplicate", "译文"),
        ]

        items = review_diff._changed_translation_items("fixture", current, baseline)

        self.assertEqual(items, [])

    def test_added_duplicate_occurrence_produces_one_bundle_item(self) -> None:
        baseline = [self._translation("duplicate", "译文")]
        current = [
            self._translation("duplicate", "译文"),
            self._translation("duplicate", "译文"),
        ]

        items = review_diff._changed_translation_items("fixture", current, baseline)

        self.assertEqual([item["ordinal"] for item in items], [1])

    def test_one_to_many_editorial_splits_changed_items(self) -> None:
        # A one-to-many editorial (one locale key backing several strong TUs)
        # must yield one changed item per TU, each keeping the document
        # ordinal, instead of a single fallback/subject item (review F8).
        editorial_to_tu = {
            ("fixture", compute_unit_id("fixture", "fixture.lua", "duplicate", None)): (
                "a" * 64,
                "b" * 64,
            )
        }
        current = [self._translation("duplicate", "译文")]
        items = review_diff._changed_translation_items(
            "fixture",
            current,
            None,
            editorial_to_tu=editorial_to_tu,
        )
        self.assertEqual(len(items), 2)
        self.assertEqual({item["tu_uid"] for item in items}, {"a" * 64, "b" * 64})
        self.assertTrue(all(item["ordinal"] == 0 for item in items))

    def test_duplicate_semantic_change_consumes_only_one_matching_baseline(self) -> None:
        baseline = [
            self._translation("duplicate", "甲"),
            self._translation("duplicate", "乙"),
        ]
        current = [
            self._translation("duplicate", "乙"),
            self._translation("duplicate", "乙"),
        ]

        items = review_diff._changed_translation_items("fixture", current, baseline)

        self.assertEqual(
            [(item["ordinal"], item["target"]) for item in items],
            [(1, "乙")],
        )

    def test_args_order_only_change_produces_bundle_item(self) -> None:
        baseline = [self._translation("changed", "译文")]
        current = [
            self._translation("changed", "译文", args_order=[2, 1])
        ]

        items = review_diff._changed_translation_items("fixture", current, baseline)

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["args_order"], [2, 1])

    def test_special_only_change_produces_bundle_item(self) -> None:
        # Lua/JSON and revision identity distinguish these types; Python's
        # native deep equality does not because True == 1.
        baseline = [
            self._translation("changed", "译文", special={"mode": True})
        ]
        current = [
            self._translation("changed", "译文", special={"mode": 1})
        ]

        items = review_diff._changed_translation_items("fixture", current, baseline)

        self.assertEqual(len(items), 1)
        self.assertEqual(items[0]["special"], {"mode": 1})

    def test_deep_equivalent_special_is_skipped(self) -> None:
        baseline = [
            self._translation(
                "same",
                "译文",
                special={
                    "enabled": True,
                    "nested": {
                        "right": 2,
                        "items": [{"last": "b", "first": "a"}],
                    },
                },
            ),
        ]
        current = [
            self._translation(
                "same",
                "译文",
                special={
                    "nested": {
                        "items": [{"first": "a", "last": "b"}],
                        "right": 2,
                    },
                    "enabled": True,
                },
            ),
        ]

        items = review_diff._changed_translation_items("fixture", current, baseline)

        self.assertEqual(items, [])

    def test_combined_semantic_changes_preserve_full_bundle_item(self) -> None:
        baseline = [
            self._translation(
                "changed %s %d",
                "旧译 %s %d",
                args_order=[1, 2],
                special={"wrap": False},
            )
        ]
        current_entry = self._translation(
            "changed %s %d",
            "新译 %d %s",
            args_order=[2, 1],
            special={"wrap": True},
        )

        items = review_diff._changed_translation_items(
            "fixture", [current_entry], baseline
        )

        self.assertEqual(
            items,
            [
                review_diff.build_translation_item(
                    version=review_diff.DEFAULT_VERSION,
                    component="fixture",
                    ordinal=0,
                    entry=current_entry,
                )
            ],
        )

    def test_identical_runtime_semantics_are_skipped(self) -> None:
        baseline = [
            self._translation(
                "same",
                "译文",
                args_order=[2, 1],
                special={"wrap": True},
            )
        ]
        current = [
            self._translation(
                "same",
                "译文",
                args_order=[2, 1],
                special={"wrap": True},
            )
        ]

        items = review_diff._changed_translation_items("fixture", current, baseline)

        self.assertEqual(items, [])

    def test_loader_normalization_drives_semantic_comparison(self) -> None:
        manifest = load_manifest()
        loader = LocaleLoader(LuaRuntime(manifest))
        baseline = loader.load_bytes(
            b'''section("fixture.lua")
t("changed %s %d", "translation %d %s", "tformat", {1, 2}, {nested={z=2, a=1}, flags={"a", "b"}})
t("same", "translation", nil, nil, {nested={z=2, a=1}, flags={"a", "b"}})
''',
            logical_path="baseline.lua",
        )
        current = loader.load_bytes(
            b'''section("fixture.lua")
t("changed %s %d", "translation %d %s", "tformat", {2, 1}, {flags={"a", "b"}, nested={a=1, z=2}})
t("same", "translation", nil, nil, {flags={"a", "b"}, nested={a=1, z=2}})
''',
            logical_path="current.lua",
        )

        items = review_diff._changed_translation_items(
            "fixture", current.translations, baseline.translations
        )

        self.assertEqual([item["source"] for item in items], ["changed %s %d"])
        self.assertEqual(items[0]["args_order"], [2, 1])
        self.assertEqual(
            items[0]["special"],
            {"flags": ["a", "b"], "nested": {"a": 1, "z": 2}},
        )

    def test_cli_handles_missing_empty_and_unchanged_baseline_files(self) -> None:
        manifest = load_manifest()
        component = manifest.component("example")
        manifest = replace(manifest, components=(component,))
        translation_path = manifest.root / component.translation
        current_document = LocaleLoader(LuaRuntime(manifest)).load_path(
            translation_path,
            logical_path=component.translation,
        )
        expected = [
            (entry["source"], entry["target"], entry["source_tag"])
            for entry in current_document.translations
        ]
        self.assertTrue(expected)

        cases = (
            ("missing", {"unrelated.txt": b"fixture\n"}, expected),
            ("empty", {component.translation: b""}, expected),
            (
                "unchanged",
                {component.translation: translation_path.read_bytes()},
                [],
            ),
        )
        for label, baseline_files, expected_entries in cases:
            with self.subTest(case=label), tempfile.TemporaryDirectory(
                prefix=f"tome4-review-diff-cli-{label}-"
            ) as temporary:
                root = Path(temporary)
                self._commit_repository(root, baseline_files)
                output = root / "output"
                stdout = io.StringIO()
                stderr = io.StringIO()
                with (
                    patch.object(review_diff, "ROOT", root),
                    patch.object(review_diff, "load_manifest", return_value=manifest),
                    patch.object(review_diff.signal, "alarm"),
                    contextlib.redirect_stdout(stdout),
                    contextlib.redirect_stderr(stderr),
                ):
                    exit_code = review_diff.main(
                        [
                            "--baseline",
                            "HEAD",
                            "--batch-size",
                            str(review_diff.MAX_REVIEW_BATCH_SIZE),
                            "--out-dir",
                            str(output),
                        ]
                    )

                self.assertEqual(exit_code, 0, stderr.getvalue())
                self.assertEqual(stderr.getvalue(), "")
                index = json.loads(
                    (output / "review-index.json").read_text(encoding="utf-8")
                )
                items = []
                for bundle in index["bundles"]:
                    payload = json.loads(
                        Path(bundle["path"]).read_text(encoding="utf-8")
                    )
                    items.extend(payload["items"])
                actual = [
                    (item["source"], item["target"], item["source_tag"])
                    for item in items
                ]
                self.assertEqual(actual, expected_entries)
                self.assertIn(
                    f"changed entries: {len(expected_entries)}", stdout.getvalue()
                )


if __name__ == "__main__":
    unittest.main()
