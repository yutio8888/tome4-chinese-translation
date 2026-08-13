"""Incremental invalidation tests (contract/0.1-rc3 §8): G8 whole-set
canonical self-check, the §8.3 round-trip parity contract and the
affected-set mapping."""

from __future__ import annotations

import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

TOOLS = Path(__file__).resolve().parents[3] / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from i18nlib.config import ComponentSpec, SourceMount  # noqa: E402
from i18nlib.fingerprint import canonical_findings_form  # noqa: E402
from i18nlib.git_source import GitRepository  # noqa: E402
from i18nlib.invalidation import (  # noqa: E402
    affected_for_source_domain,
    parity_check,
    section_to_source_git_path,
    source_git_path_to_section,
)
from i18nlib.invalidation import self_check as canonical_self_check  # noqa: E402
from i18nlib.invalidation import incremental_findings  # noqa: E402
from i18nlib.snapshot import read_snapshot  # noqa: E402

from tests.i18n.fingerprint.test_fingerprint import _record  # noqa: E402
from tests.i18n.identity.fixture import (  # noqa: E402
    FIXTURE_EFFECTS,
    FIXTURE_ENTITIES,
    FIXTURE_MISC,
    FIXTURE_TALENTS,
    build_fixture_index,
    loader,
    manifest,
    runtime,
)


def _component(**overrides) -> ComponentSpec:
    defaults = dict(
        id="tome",
        translation="mod-tome.lua",
        copy_fragment=None,
        source_repository="engine",
        sources=(
            SourceMount(git_path="game/modules/tome", mount="mod-tome"),
            SourceMount(git_path="game/engines/default/data", mount="engine/data"),
        ),
        protected_source=None,
        source_baseline=None,
        extract_by_default=True,
        official_locale=None,
        full_output=None,
        addon_eligible=True,
    )
    defaults.update(overrides)
    return ComponentSpec(**defaults)


class SectionMappingTests(unittest.TestCase):
    def test_forward_mapping(self) -> None:
        component = _component()
        self.assertEqual(
            source_git_path_to_section(
                component, "game/modules/tome/data/talents/spells/fire.lua"
            ),
            "mod-tome/data/talents/spells/fire.lua",
        )
        self.assertEqual(
            source_git_path_to_section(component, "game/modules/tome/init.lua"),
            "mod-tome/init.lua",
        )
        self.assertIsNone(
            source_git_path_to_section(component, "game/modules/example/init.lua")
        )

    def test_round_trip_parity(self) -> None:
        """§8.3 parity: every real section must round-trip."""
        sections = [
            "mod-tome/data/talents/spells/fire.lua",
            "mod-tome/init.lua",
            "engine/data/quests/main.lua",
        ]
        self.assertEqual(parity_check(_component(), sections), [])
        broken = sections + ["mod-other/x.lua"]
        self.assertEqual(len(parity_check(_component(), broken)), 1)

        # Real boot sections (pinned snapshot of the boot component) must
        # round-trip through the mod-boot mount as well (G12).
        boot = _component(
            id="boot",
            translation="mod-boot.lua",
            sources=(
                SourceMount(
                    git_path="game/engines/default/modules/boot", mount="mod-boot"
                ),
            ),
        )
        boot_sections = [
            "mod-boot/class/Game.lua",
            "mod-boot/data/birth/descriptors.lua",
            "mod-boot/data/talents.lua",
        ]
        self.assertEqual(parity_check(boot, boot_sections), [])
        for section in boot_sections:
            self.assertEqual(
                source_git_path_to_section(
                    boot, section_to_source_git_path(boot, section)
                ),
                section,
            )
        self.assertEqual(
            source_git_path_to_section(
                boot, "game/engines/default/modules/boot/class/Game.lua"
            ),
            "mod-boot/class/Game.lua",
        )
        self.assertEqual(
            len(parity_check(boot, boot_sections + ["mod-other/x.lua"])), 1
        )

    def test_affected_set_ignores_other_components(self) -> None:
        affected = affected_for_source_domain(
            _component(),
            [
                "game/modules/tome/data/x.lua",
                "game/modules/example/y.lua",
                "game/modules/tome/readme.txt",
            ],
        )
        self.assertEqual(affected.sections, {"mod-tome/data/x.lua"})


class IncrementalAlgorithmTests(unittest.TestCase):
    def test_f_new_keeps_unaffected_and_replaces_affected(self) -> None:
        all_records = {
            "affected": _record(tu_uid="TU-AFFECTED", fingerprint="a" * 64),
            "kept": _record(tu_uid="TU-KEPT", fingerprint="k" * 64),
        }
        recomputed = [_record(tu_uid="TU-AFFECTED", fingerprint="n" * 64)]
        result = incremental_findings(
            previous=list(all_records.values()),
            affected_tu_uids={"TU-AFFECTED"},
            recomputed=recomputed,
        )
        self.assertEqual(
            {record.tu_uid for record in result}, {"TU-AFFECTED", "TU-KEPT"}
        )
        self.assertNotIn(
            all_records["affected"].fingerprint,
            {record.fingerprint for record in result},
        )

    def test_g8_canonical_self_check(self) -> None:
        """G8: a consistent partition makes incremental == full byte-wise."""
        full = [
            _record(tu_uid="TU-A", fingerprint="a" * 64),
            _record(tu_uid="TU-B", fingerprint="b" * 64),
            _record(tu_uid="TU-C", fingerprint="c" * 64),
        ]
        affected = {"TU-B"}
        recomputed = [_record(tu_uid="TU-B", fingerprint="b2" * 32)]
        # An adversarial recompute that matches the full set.
        full_recomputed = [
            record for record in full if record.tu_uid != "TU-B"
        ] + recomputed
        incremental = incremental_findings(
            previous=full, affected_tu_uids=affected, recomputed=recomputed
        )
        self.assertEqual(
            canonical_findings_form(incremental),
            canonical_findings_form(full_recomputed),
        )
        self.assertTrue(
            canonical_self_check(incremental=incremental, full=full_recomputed)
        )
        # A wrong partition must be detected.
        self.assertFalse(
            canonical_self_check(incremental=incremental, full=full)
        )

    def test_self_check_writes_artifacts_on_mismatch(self) -> None:
        import tempfile

        with tempfile.TemporaryDirectory(prefix="tome4-i18n-selfcheck-") as tmp:
            directory = Path(tmp)
            passed = canonical_self_check(
                incremental=[_record(fingerprint="x" * 64)],
                full=[_record(fingerprint="y" * 64)],
                artifact_directory=directory,
            )
            self.assertFalse(passed)
            self.assertTrue((directory / "incremental-canonical.jsonl").is_file())
            self.assertTrue((directory / "full-canonical.jsonl").is_file())


class IncrementalSourceFlowTests(unittest.TestCase):
    """G8 (production entry): incremental_source_flow over a synthetic git repo.

    A temporary git repository holds the mini-tome fixture at engine git paths
    (game/modules/tome/...); the head commit changes the T_FLAME numeric value
    (contract G8: 修改 T_FLAME 数值). The production chain runs for real:
    GitRepository.changed_paths -> affected_for_source_domain -> affected TU
    set -> staged partial re-extraction (real patched extractor) -> recompute
    -> whole-set canonical self-check. Only the full-extraction step
    (pipeline.extract_enriched, which would pull the pinned engine repository)
    is stubbed, per ORCHESTRATOR adjudication (F2), to keep the test
    deterministic and fast.
    """

    _BASE_FILES = {
        "game/modules/tome/data/talents.lua": FIXTURE_TALENTS,
        "game/modules/tome/data/effects.lua": FIXTURE_EFFECTS,
        "game/modules/tome/data/entities.lua": FIXTURE_ENTITIES,
        "game/modules/tome/data/misc.lua": FIXTURE_MISC,
    }

    @staticmethod
    def _git(repository: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            ["git", "-C", str(repository), *arguments],
            capture_output=True,
            text=True,
            check=False,
        )

    @classmethod
    def _commit_all(cls, repository: Path, message: str) -> str:
        cls._git(repository, "add", "-A")
        result = cls._git(
            repository,
            "-c", "user.name=test",
            "-c", "user.email=test@example.invalid",
            "commit", "-q", "-m", message,
        )
        assert result.returncode == 0, result.stderr
        head = cls._git(repository, "rev-parse", "HEAD")
        assert head.returncode == 0, head.stderr
        return head.stdout.strip()

    @classmethod
    def _repo_file_list(cls, repository: Path, commit: str, git_path: str) -> list[str]:
        result = cls._git(repository, "ls-tree", "-r", "--name-only", commit)
        assert result.returncode == 0, result.stderr
        prefix = git_path + "/"
        return [
            name for name in result.stdout.splitlines() if name.startswith(prefix)
        ]

    @classmethod
    def _stub_extract_enriched(cls, repository: Path):
        """Stub for pipeline.extract_enriched: materialize the synthetic repo
        at the override commit into a mini tree and build the real index."""

        def extract_enriched(
            manifest_, runtime_, components, *, timeout=900, commit_overrides=None
        ):
            indexes = {}
            for component in components:
                override = (commit_overrides or {}).get(component.source_repository)
                assert override is not None, "stub requires a commit override"
                with tempfile.TemporaryDirectory(
                    prefix="tome4-i18n-stub-extract-"
                ) as temporary:
                    tree = Path(temporary)
                    git_repository = GitRepository(repository)
                    for source in component.sources:
                        for path in cls._repo_file_list(
                            repository, override, source.git_path
                        ):
                            relative = path[len(source.git_path) + 1 :]
                            target = tree / source.mount / relative
                            target.parent.mkdir(parents=True, exist_ok=True)
                            target.write_bytes(
                                git_repository.read_blob(override, path)
                            )
                    indexes[component.id] = build_fixture_index(
                        tree, component=component.id
                    )
            return indexes, {}

        return extract_enriched

    def test_g8_incremental_source_flow_end_to_end(self) -> None:
        import importlib

        from unittest import mock

        from i18nlib.incremental import incremental_source_flow

        with tempfile.TemporaryDirectory(prefix="tome4-i18n-g8-git-") as temporary:
            temporary_root = Path(temporary)
            repository = temporary_root / "engine"
            for relative, content in self._BASE_FILES.items():
                path = repository / relative
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(content, encoding="utf-8", newline="\n")
            self._git(repository, "init", "-q")
            base_commit = self._commit_all(repository, "base fixture")

            # Head: contract G8 change - the T_FLAME numeric value.
            talents = repository / "game/modules/tome/data/talents.lua"
            talents.write_text(
                FIXTURE_TALENTS.replace("tformat(10)", "tformat(20)"),
                encoding="utf-8",
                newline="\n",
            )
            head_commit = self._commit_all(repository, "head: T_FLAME numeric")

            # Canonical translation document with two defects: one on an
            # affected TU (talents.lua info, format-mismatch) and one on an
            # unaffected TU (effects.lua Burning, empty-target) so both the
            # recomputed and the kept branches of the algorithm are covered.
            translation_path = temporary_root / "mod-test.lua"
            translation_path.write_text(
                'section "mod-test/data/talents.lua"\n'
                't("Deals %d fire damage.", "QuedianMubiao", "tformat")\n'
                'section "mod-test/data/effects.lua"\n'
                't("Burning", "", "_t")\n',
                encoding="utf-8",
            )

            component = _component(
                id="test-component",
                translation=str(translation_path),
                sources=(SourceMount(git_path="game/modules/tome", mount="mod-test"),),
                addon_eligible=False,
            )

            artifact_directory = temporary_root / "artifacts"
            with mock.patch.object(
                importlib.import_module("i18nlib.pipeline"),
                "extract_enriched",
                self._stub_extract_enriched(repository),
            ):
                result = incremental_source_flow(
                    manifest=manifest(),
                    runtime=runtime(),
                    loader=loader(),
                    components=[component],
                    engine_repository=GitRepository(repository),
                    base_commit=base_commit,
                    head_commit=head_commit,
                    self_check=True,
                    artifact_directory=artifact_directory,
                )

            self.assertEqual(result["domain"], "source")
            self.assertEqual(result["changed_paths"], 1)
            self.assertEqual(
                result["affected_sections"],
                {"test-component": ["mod-test/data/talents.lua"]},
            )
            self.assertEqual(result["widened_components"], {})
            self.assertGreater(result["affected_tus"], 0)
            self.assertGreater(result["findings"]["previous"], 1)
            self.assertGreater(result["findings"]["kept"], 0)
            self.assertGreater(result["findings"]["recomputed"], 0)
            # Whole-set canonical byte-level equality (self-check) plus the
            # same finding counts prove incremental == full.
            self.assertIs(result["self_check"]["passed"], True)
            self.assertEqual(
                result["self_check"]["full_findings"],
                result["findings"]["incremental"],
            )


if __name__ == "__main__":
    unittest.main()
