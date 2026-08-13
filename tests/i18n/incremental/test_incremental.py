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

    # ------------------------------------------------------------------
    # infra-contract-004 consumer-chain tests (H2/H3/D4)

    def _translation_doc(self, *sections_and_entries: tuple[str, str, str]) -> str:
        """Build a canonical translation document from (section, source, target)
        triples; source_tag defaults to 'talent name' unless the target is
        empty (still fine)."""
        lines: list[str] = []
        for section, source, target in sections_and_entries:
            lines.append(f'section "{section}"')
            lines.append(f't("{source}", "{target}", "talent name")')
        return "\n".join(lines) + "\n"

    def _run_flow(
        self,
        repository: Path,
        base_commit: str,
        head_commit: str,
        translation_doc: str,
        *,
        self_check: bool,
        component_override: dict | None = None,
    ) -> dict:
        import importlib

        from unittest import mock

        from i18nlib.incremental import incremental_source_flow

        translation_path = repository.parent / "mod-test.lua"
        translation_path.write_text(translation_doc, encoding="utf-8")
        component = _component(
            id="test-component",
            translation=str(translation_path),
            sources=(SourceMount(git_path="game/modules/tome", mount="mod-test"),),
            addon_eligible=False,
        )
        if component_override:
            component = _component(**component_override)
        artifact_directory = repository.parent / "artifacts"
        with mock.patch.object(
            importlib.import_module("i18nlib.pipeline"),
            "extract_enriched",
            self._stub_extract_enriched(repository),
        ):
            return incremental_source_flow(
                manifest=manifest(),
                runtime=runtime(),
                loader=loader(),
                components=[component],
                engine_repository=GitRepository(repository),
                base_commit=base_commit,
                head_commit=head_commit,
                self_check=self_check,
                artifact_directory=artifact_directory,
            )

    def _repo(self, head_files: dict[str, str], base_files: dict[str, str] | None = None):
        """Create a synthetic engine git repo; returns (repository, base, head)."""
        temporary = tempfile.TemporaryDirectory(prefix="tome4-i18n-consumer-")
        repository = Path(temporary.name) / "engine"
        for relative, content in (base_files or self._BASE_FILES).items():
            path = repository / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8", newline="\n")
        self._git(repository, "init", "-q")
        base_commit = self._commit_all(repository, "base fixture")
        for relative, content in head_files.items():
            path = repository / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8", newline="\n")
        # Deletions are handled by removing files from the working tree.
        base_names = set((base_files or self._BASE_FILES))
        for name in base_names - set(head_files):
            (repository / name).unlink()
        head_commit = self._commit_all(repository, "head fixture")
        return temporary, repository, base_commit, head_commit

    def test_h2_add_new_file_new_tu_self_check(self) -> None:
        """Head adds a new file with a new talent: the new TU is affected and
        its finding is recomputed; self-check passes."""
        frost = (
            "newTalent{\n"
            '\tname = "Frost",\n'
            '\tshort_name = "FROST",\n'
            '\ttype = {"spell/frost", 1},\n'
            "}\n"
        )
        temporary, repository, base_commit, head_commit = self._repo(
            {
                "game/modules/tome/data/talents.lua": self._BASE_FILES[
                    "game/modules/tome/data/talents.lua"
                ],
                "game/modules/tome/data/effects.lua": self._BASE_FILES[
                    "game/modules/tome/data/effects.lua"
                ],
                "game/modules/tome/data/entities.lua": self._BASE_FILES[
                    "game/modules/tome/data/entities.lua"
                ],
                "game/modules/tome/data/misc.lua": self._BASE_FILES[
                    "game/modules/tome/data/misc.lua"
                ],
                "game/modules/tome/data/talents/frost.lua": frost,
            }
        )
        try:
            doc = self._translation_doc(
                ("mod-test/data/talents/frost.lua", "Frost", ""),
                ("mod-test/data/talents.lua", "Deals %d fire damage.", "OK"),
            )
            result = self._run_flow(
                repository, base_commit, head_commit, doc, self_check=True
            )
            self.assertIn(
                "mod-test/data/talents/frost.lua",
                result["affected_sections"]["test-component"],
            )
            self.assertGreater(result["affected_tus"], 0)
            self.assertEqual(result["widened_components"], {})
            self.assertIs(result["self_check"]["passed"], True)
            # The new-talent empty-target ERROR is recomputed into the set.
            from i18nlib.lint import stable_entry_id

            frost_entry = stable_entry_id(
                "test-component",
                "mod-test/data/talents/frost.lua",
                "Frost",
                "talent name",
            )
            errors = [
                record
                for record in result["records"]
                if record.get("code") == "empty-target"
                and record.get("entry_id") == frost_entry
            ]
            self.assertEqual(len(errors), 1)
        finally:
            temporary.cleanup()

    def test_h2_delete_file_no_crash_deleted_reported(self) -> None:
        """Head deletes effects.lua: no missing-blob crash, the deleted file is
        reported, the deleted-section base TUs leave kept, self-check passes."""
        temporary, repository, base_commit, head_commit = self._repo(
            {
                "game/modules/tome/data/talents.lua": self._BASE_FILES[
                    "game/modules/tome/data/talents.lua"
                ],
                "game/modules/tome/data/entities.lua": self._BASE_FILES[
                    "game/modules/tome/data/entities.lua"
                ],
                "game/modules/tome/data/misc.lua": self._BASE_FILES[
                    "game/modules/tome/data/misc.lua"
                ],
            }
        )
        try:
            doc = self._translation_doc(
                ("mod-test/data/effects.lua", "Burning", ""),
                ("mod-test/data/talents.lua", "Flame", ""),
            )
            result = self._run_flow(
                repository, base_commit, head_commit, doc, self_check=True
            )
            self.assertEqual(
                result["deleted_files"],
                ["game/modules/tome/data/effects.lua"],
            )
            self.assertGreater(result["affected_tus"], 0)
            self.assertIs(result["self_check"]["passed"], True)
            # The deleted section's base TU findings are removed from kept.
            self.assertLess(
                result["findings"]["kept"], result["findings"]["previous"]
            )
        finally:
            temporary.cleanup()

    def test_h2_rename_same_file_new_uid_self_check(self) -> None:
        """Same-file entity rename: the new UID's TU is affected, the old
        editorial's finding is re-bound and self-check passes."""
        from i18nlib.identity import entity_uid, tu_uid_strong

        talents = self._BASE_FILES["game/modules/tome/data/talents.lua"].replace(
            'name = "Burning Shock",\n\tshort_name = "BURNING_SHOCK",',
            'name = "Burning Stun",\n\tshort_name = "BURNING_STUN",',
        )
        temporary, repository, base_commit, head_commit = self._repo(
            {
                "game/modules/tome/data/talents.lua": talents,
                "game/modules/tome/data/effects.lua": self._BASE_FILES[
                    "game/modules/tome/data/effects.lua"
                ],
                "game/modules/tome/data/entities.lua": self._BASE_FILES[
                    "game/modules/tome/data/entities.lua"
                ],
                "game/modules/tome/data/misc.lua": self._BASE_FILES[
                    "game/modules/tome/data/misc.lua"
                ],
            }
        )
        try:
            doc = self._translation_doc(
                ("mod-test/data/talents.lua", "Burning Shock", ""),
                ("mod-test/data/talents.lua", "Burning Stun", ""),
            )
            result = self._run_flow(
                repository, base_commit, head_commit, doc, self_check=True
            )
            expected_new_tu = tu_uid_strong(
                entity_uid("test-component", "talent", "T_BURNING_STUN"),
                "talent.name",
                "default",
            )
            # The renamed editorial's finding is present in the incremental
            # set bound to the new UID (recomputed via the affected issue).
            from i18nlib.lint import stable_entry_id

            stun_entry = stable_entry_id(
                "test-component",
                "mod-test/data/talents.lua",
                "Burning Stun",
                "talent name",
            )
            stun = [
                record
                for record in result["records"]
                if record.get("code") == "empty-target"
                and record.get("entry_id") == stun_entry
            ]
            self.assertEqual(len(stun), 1)
            self.assertEqual(stun[0]["tu_uid"], expected_new_tu)
            # The old-name editorial still surfaces (fallback binding) and the
            # whole-set self-check agrees with the full head.
            self.assertIs(result["self_check"]["passed"], True)
            self.assertEqual(
                result["self_check"]["full_findings"],
                result["findings"]["incremental"],
            )
        finally:
            temporary.cleanup()

    def test_d4_cross_file_duplicate_without_self_check(self) -> None:
        """A changed file defines an anchor that duplicates an unchanged file's
        anchor: the ERROR is detected even without --self-check, and it is a
        NEW error for the CI gate (full-head-equivalent conflict input). The
        anchor (BURNING_SHOCK) has no info slot, so the fixture extractor's
        def_line artifact cannot create a base conflict for it."""
        duplicate = (
            "newTalent{\n"
            '\tname = "Duplicate Shock",\n'
            '\tshort_name = "BURNING_SHOCK",\n'
            '\ttype = {"spell/fire", 9},\n'
            "}\n"
        )
        temporary, repository, base_commit, head_commit = self._repo(
            {
                "game/modules/tome/data/talents.lua": self._BASE_FILES[
                    "game/modules/tome/data/talents.lua"
                ],
                "game/modules/tome/data/effects.lua": self._BASE_FILES[
                    "game/modules/tome/data/effects.lua"
                ],
                "game/modules/tome/data/entities.lua": self._BASE_FILES[
                    "game/modules/tome/data/entities.lua"
                ],
                "game/modules/tome/data/misc.lua": self._BASE_FILES[
                    "game/modules/tome/data/misc.lua"
                ],
                "game/modules/tome/data/talents/duplicate.lua": duplicate,
            }
        )
        try:
            doc = self._translation_doc(
                ("mod-test/data/talents.lua", "Flame", "火焰"),
            )
            result = self._run_flow(
                repository, base_commit, head_commit, doc, self_check=False
            )
            # The partial staged extraction alone cannot see the duplicate
            # (the unchanged talents.lua is not staged); the full-head
            # conflict input must surface it.
            duplicates = [
                record
                for record in result["records"]
                if record.get("code") == "duplicate-talent-id"
                and record.get("evidence_key") == "dup:T_BURNING_SHOCK"
            ]
            self.assertEqual(len(duplicates), 1)
            # H3/V8: recomputed error absent from the base error fingerprints
            # (the base has no conflict for this anchor).
            self.assertEqual(result["ci"]["new_errors"], 1)
            self.assertIn(
                duplicates[0]["fingerprint"],
                result["ci"]["new_error_fingerprints"],
            )
            # V8: the incremental record equals the full-head assembly.
            from tests.i18n.identity.fixture import build_fixture_index
            from tests.i18n.identity.fixture import write_fixture_tree

            head_files = {
                "mod-test/data/talents.lua": self._BASE_FILES[
                    "game/modules/tome/data/talents.lua"
                ],
                "mod-test/data/effects.lua": self._BASE_FILES[
                    "game/modules/tome/data/effects.lua"
                ],
                "mod-test/data/entities.lua": self._BASE_FILES[
                    "game/modules/tome/data/entities.lua"
                ],
                "mod-test/data/misc.lua": self._BASE_FILES[
                    "game/modules/tome/data/misc.lua"
                ],
                "mod-test/data/talents/duplicate.lua": duplicate,
            }
            with tempfile.TemporaryDirectory(
                prefix="tome4-i18n-d4-head-"
            ) as head_temporary:
                head_tree = Path(head_temporary)
                write_fixture_tree(head_tree, head_files)
                head_index = build_fixture_index(head_tree)
            expected = self._assemble_duplicate(head_index, "T_BURNING_SHOCK")
            self.assertEqual(duplicates[0]["fingerprint"], expected.fingerprint)
            self.assertEqual(duplicates[0]["tu_uid"], expected.tu_uid)
            self.assertEqual(
                duplicates[0]["participants"], list(expected.participants)
            )
        finally:
            temporary.cleanup()

    def test_v8_full_head_binding_participants_without_self_check(self) -> None:
        """V8: without --self-check, affected components bind against their
        full head index. The changed definition exposes a different slot set
        than the unchanged one (name-only vs name+info), so the partial index
        would miss the unchanged file's talent.info TU and produce a
        different fingerprint; the full-head binding must match the direct
        full-head assembly exactly."""
        duplicate = (
            "newTalent{\n"
            '\tname = "Duplicate Flame",\n'
            '\tshort_name = "FLAME",\n'
            '\ttype = {"spell/fire", 9},\n'
            "}\n"
        )
        temporary, repository, base_commit, head_commit = self._repo(
            {
                "game/modules/tome/data/talents.lua": self._BASE_FILES[
                    "game/modules/tome/data/talents.lua"
                ],
                "game/modules/tome/data/effects.lua": self._BASE_FILES[
                    "game/modules/tome/data/effects.lua"
                ],
                "game/modules/tome/data/entities.lua": self._BASE_FILES[
                    "game/modules/tome/data/entities.lua"
                ],
                "game/modules/tome/data/misc.lua": self._BASE_FILES[
                    "game/modules/tome/data/misc.lua"
                ],
                "game/modules/tome/data/talents/duplicate.lua": duplicate,
            }
        )
        try:
            doc = self._translation_doc(
                ("mod-test/data/talents.lua", "Flame", "火焰"),
            )
            result = self._run_flow(
                repository, base_commit, head_commit, doc, self_check=False
            )
            duplicates = [
                record
                for record in result["records"]
                if record.get("code") == "duplicate-talent-id"
                and record.get("evidence_key") == "dup:T_FLAME"
            ]
            self.assertEqual(len(duplicates), 1)
            from tests.i18n.identity.fixture import build_fixture_index
            from tests.i18n.identity.fixture import write_fixture_tree

            head_files = {
                "mod-test/data/talents.lua": self._BASE_FILES[
                    "game/modules/tome/data/talents.lua"
                ],
                "mod-test/data/effects.lua": self._BASE_FILES[
                    "game/modules/tome/data/effects.lua"
                ],
                "mod-test/data/entities.lua": self._BASE_FILES[
                    "game/modules/tome/data/entities.lua"
                ],
                "mod-test/data/misc.lua": self._BASE_FILES[
                    "game/modules/tome/data/misc.lua"
                ],
                "mod-test/data/talents/duplicate.lua": duplicate,
            }
            with tempfile.TemporaryDirectory(
                prefix="tome4-i18n-v8-head-"
            ) as head_temporary:
                head_tree = Path(head_temporary)
                write_fixture_tree(head_tree, head_files)
                head_index = build_fixture_index(head_tree)
            expected = self._assemble_duplicate(head_index, "T_FLAME")
            # Full canonical equality with the direct full-head assembly.
            self.assertEqual(duplicates[0]["fingerprint"], expected.fingerprint)
            self.assertEqual(duplicates[0]["tu_uid"], expected.tu_uid)
            self.assertEqual(
                duplicates[0]["participants"], list(expected.participants)
            )
            # The unchanged file's talent.info TU is among the participants
            # (a slot the changed definition does not expose): the partial
            # index could never produce this binding, so the fingerprint
            # proves full-head binding.
            self.assertGreaterEqual(len(expected.participants), 2)
            full_head_tus = {
                tu.tu_uid
                for tu in head_index.tus.values()
                if tu.anchor_key == "T_FLAME"
            }
            self.assertTrue(full_head_tus.issubset(set(expected.participants)))
            self.assertIn("talent.info", {tu.semantic_slot for tu in head_index.tus.values()})
            # The same-anchor base finding persists as legacy debt (the head
            # conflict is the same finding identity, more definition sites).
            self.assertEqual(result["ci"]["new_errors"], 0)
            self.assertGreaterEqual(result["ci"]["legacy_errors"], 1)
        finally:
            temporary.cleanup()

    def _assemble_duplicate(self, head_index, anchor_key: str):
        """Build the duplicate-id record exactly as the full head would."""
        from i18nlib.findings import FindingContext, build_finding_records
        from i18nlib.fingerprint import RuleRegistry
        from i18nlib.identity import (
            RULES_REGISTRY_RELATIVE_PATH,
            UNLOADED_SOURCES_RELATIVE_PATH,
            UnloadedSources,
        )

        registry = RuleRegistry.load(
            Path(__file__).resolve().parents[3] / RULES_REGISTRY_RELATIVE_PATH
        )
        unloaded = UnloadedSources.load(
            Path(__file__).resolve().parents[3] / UNLOADED_SOURCES_RELATIVE_PATH
        )
        conflicts = [
            conflict
            for conflict in head_index.conflicts
            if conflict.code == "duplicate-talent-id"
            and conflict.anchor_key == anchor_key
        ]
        self.assertEqual(len(conflicts), 1)
        records, _ = build_finding_records(
            registry=registry,
            issues=[],
            contexts={
                "test-component": FindingContext(
                    component="test-component", entries=(), index=head_index
                )
            },
            conflicts=conflicts,
            unloaded_sources=unloaded,
        )
        self.assertEqual(len(records), 1)
        return records[0]

    def test_h3_legacy_error_is_not_new(self) -> None:
        """H3: a recomputed error whose fingerprint exists in the base error
        fingerprints is legacy (technical debt), never a CI failure."""
        talents = self._BASE_FILES["game/modules/tome/data/talents.lua"].replace(
            "tformat(10)", "tformat(20)"
        )
        temporary, repository, base_commit, head_commit = self._repo(
            {
                "game/modules/tome/data/talents.lua": talents,
                "game/modules/tome/data/effects.lua": self._BASE_FILES[
                    "game/modules/tome/data/effects.lua"
                ],
                "game/modules/tome/data/entities.lua": self._BASE_FILES[
                    "game/modules/tome/data/entities.lua"
                ],
                "game/modules/tome/data/misc.lua": self._BASE_FILES[
                    "game/modules/tome/data/misc.lua"
                ],
            }
        )
        try:
            doc = self._translation_doc(
                ("mod-test/data/talents.lua", "Deals %d fire damage.", "OK"),
                ("mod-test/data/effects.lua", "Burning", ""),
            )
            result = self._run_flow(
                repository, base_commit, head_commit, doc, self_check=True
            )
            self.assertGreater(result["ci"]["legacy_errors"], 0)
            self.assertEqual(result["ci"]["new_errors"], 0)
            self.assertEqual(result["ci"]["new_error_fingerprints"], [])
            self.assertIs(result["self_check"]["passed"], True)
        finally:
            temporary.cleanup()

    def _expected_full_records(self, repository: Path, head_commit: str, component):
        """Assemble the full-head FindingRecords exactly like the flow would
        (head tree materialized from the commit, head doc linted, bound to
        the full-head index)."""
        from i18nlib.findings import FindingContext, build_finding_records
        from i18nlib.fingerprint import RuleRegistry
        from i18nlib.identity import (
            RULES_REGISTRY_RELATIVE_PATH,
            UNLOADED_SOURCES_RELATIVE_PATH,
            UnloadedSources,
        )
        from i18nlib.pipeline import lint_translation_documents

        with tempfile.TemporaryDirectory(prefix="tome4-i18n-full-head-") as temporary:
            tree = Path(temporary)
            git_repository = GitRepository(repository)
            for source in component.sources:
                for path in self._repo_file_list(
                    repository, head_commit, source.git_path
                ):
                    relative = path[len(source.git_path) + 1 :]
                    target = tree / source.mount / relative
                    target.parent.mkdir(parents=True, exist_ok=True)
                    target.write_bytes(git_repository.read_blob(head_commit, path))
            head_index = build_fixture_index(tree, component=component.id)
        registry = RuleRegistry.load(
            Path(__file__).resolve().parents[3] / RULES_REGISTRY_RELATIVE_PATH
        )
        unloaded = UnloadedSources.load(
            Path(__file__).resolve().parents[3] / UNLOADED_SOURCES_RELATIVE_PATH
        )
        issues, contexts, _ = lint_translation_documents(
            manifest(), loader(), [component]
        )
        bound = {
            name: FindingContext(
                component=context.component,
                entries=context.entries,
                index=head_index,
            )
            for name, context in contexts.items()
        }
        records, _ = build_finding_records(
            registry=registry,
            issues=issues,
            contexts=bound,
            conflicts=list(head_index.conflicts),
            unloaded_sources=unloaded,
        )
        return records

    def _records_from_dicts(self, record_dicts):
        from i18nlib.fingerprint import FindingRecord
        from i18nlib.lint import Issue

        records = []
        for record in record_dicts:
            records.append(
                FindingRecord(
                    issue=Issue(
                        record["severity"],
                        record["code"],
                        record["message"],
                        record["logical_path"],
                        record["line"],
                        record["entry_id"],
                    ),
                    rule_id=record["rule_id"],
                    rule_schema_version=record["rule_schema_version"],
                    tu_uid=record["tu_uid"],
                    participants=tuple(record["participants"]),
                    evidence_key=record["evidence_key"],
                    fingerprint=record["fingerprint"],
                )
            )
        return records

    def test_r1_source_rename_includes_base_path(self) -> None:
        """R1: a detected rename must keep the old path in the affected set
        (git diff --no-renames); with an anchor/UID change and no self-check
        the incremental canonical form equals the full head and the old
        strong record does not linger."""
        from i18nlib.fingerprint import canonical_findings_form
        from i18nlib.identity import entity_uid, tu_uid_strong

        old_talent = (
            "newTalent{\n"
            '\tname = "Old Talent",\n'
            '\tshort_name = "OLD_TALENT",\n'
            '\ttype = {"spell/fire", 3},\n'
            "}\n"
        )
        new_talent = (
            "newTalent{\n"
            '\tname = "New Talent",\n'
            '\tshort_name = "NEW_TALENT",\n'
            '\ttype = {"spell/fire", 3},\n'
            "}\n"
        )
        base_files = {
            "game/modules/tome/data/talents/old.lua": old_talent,
            "game/modules/tome/data/effects.lua": self._BASE_FILES[
                "game/modules/tome/data/effects.lua"
            ],
            "game/modules/tome/data/entities.lua": self._BASE_FILES[
                "game/modules/tome/data/entities.lua"
            ],
            "game/modules/tome/data/misc.lua": self._BASE_FILES[
                "game/modules/tome/data/misc.lua"
            ],
        }
        head_files = {
            "game/modules/tome/data/talents/new.lua": new_talent,
            "game/modules/tome/data/effects.lua": self._BASE_FILES[
                "game/modules/tome/data/effects.lua"
            ],
            "game/modules/tome/data/entities.lua": self._BASE_FILES[
                "game/modules/tome/data/entities.lua"
            ],
            "game/modules/tome/data/misc.lua": self._BASE_FILES[
                "game/modules/tome/data/misc.lua"
            ],
        }
        temporary, repository, base_commit, head_commit = self._repo(
            head_files, base_files=base_files
        )
        try:
            doc = self._translation_doc(
                ("mod-test/data/talents/old.lua", "Old Talent", ""),
                ("mod-test/data/talents/new.lua", "New Talent", ""),
            )
            component = _component(
                id="test-component",
                translation=str(repository.parent / "mod-test.lua"),
                sources=(
                    SourceMount(git_path="game/modules/tome", mount="mod-test"),
                ),
                addon_eligible=False,
            )
            result = self._run_flow(
                repository, base_commit, head_commit, doc, self_check=False
            )
            # Both sides of the rename are in the affected sections.
            self.assertIn(
                "mod-test/data/talents/old.lua",
                result["affected_sections"]["test-component"],
            )
            self.assertIn(
                "mod-test/data/talents/new.lua",
                result["affected_sections"]["test-component"],
            )
            # The old strong TU's finding must not linger in the incremental
            # set (the base path is affected, so its records leave kept).
            old_tu = tu_uid_strong(
                entity_uid("test-component", "talent", "T_OLD_TALENT"),
                "talent.name",
                "default",
            )
            self.assertNotIn(
                old_tu, {record["tu_uid"] for record in result["records"]}
            )
            # Full canonical equality with the direct full-head assembly.
            expected = self._expected_full_records(
                repository, head_commit, component
            )
            incremental_form = canonical_findings_form(
                self._records_from_dicts(result["records"])
            )
            full_form = canonical_findings_form(expected)
            self.assertEqual(incremental_form, full_form)
        finally:
            temporary.cleanup()


if __name__ == "__main__":
    unittest.main()
